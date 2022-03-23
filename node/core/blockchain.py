from asyncio import create_task, gather, get_event_loop
from copy import deepcopy
from datetime import datetime, timedelta
from hashlib import sha256
from logging import Logger, getLogger
from random import randint
from sys import maxsize as MAX_INT_PYTHON
from time import time
from typing import Any, Callable

from aiofiles import open as aopen
from blueprint.schemas import (
    Block,
    Blockchain,
    Blocks,
    HashableBlock,
    SearchContext,
    Transaction,
    Transactions,
)
from frozendict import frozendict
from orjson import dumps as export_to_json
from orjson import loads as import_raw_json_to_dict
from pympler.asizeof import asizeof
from utils.processors import logger_exception_handler

from core.consensus import AdaptedPoETConsensus
from core.constants import (
    ASYNC_TARGET_LOOP,
    BLOCK_HASH_LENGTH,
    BLOCKCHAIN_HASH_BLOCK_DIFFICULTY,
    BLOCKCHAIN_NODE_JSON_TEMPLATE,
    BLOCKCHAIN_RAW_PATH,
    BLOCKCHAIN_REQUIRED_GENESIS_BLOCKS,
    AddressUUID,
    BlockchainIOAction,
    HashUUID,
    JWTToken,
    NodeRoles,
    ObjectProcessAction,
)
from core.dependencies import get_identity_tokens
from core.tasks import AsyncTaskQueue

logger: Logger = getLogger(ASYNC_TARGET_LOOP)

# TODO: Should we seperate consensus from this class?
class BlockchainMechanism(AsyncTaskQueue, AdaptedPoETConsensus):
    def __init__(
        self,
        *,
        auth_tokens: tuple[AddressUUID, JWTToken],
        client_role: NodeRoles,
    ) -> None:

        # TODO: After finalization, seperate some methods and attributes for the SIDE and MASTER.
        # Required since this class will be invoked no matter what the role of the client instance is.

        # * Required Variables for the Blockchain Operaetion.
        self.client_role = client_role
        self.auth_token = auth_tokens
        self.consensus_timer: datetime = (
            datetime.now()
        )  # TODO: This will be computed based on the information by the MASTER node on how much is being participated, along with its computed value based on the average mining and iteration.

        # * State and Variable References
        self.node_ready = False  # * This bool property is used for determining if this node is ready in terms of participating from the master node, this is where the consensus will be used.
        self.blockchain_ready = False  # * This bool property is used for determining if the blockchain is ready to take its request from its master or side nodes.
        self.cached_block_id: int = (
            1  # * The current ID of the block to be rendered from the blockchain.
        )

        super().__init__()

    # - Parameterized Decorator | Based: https://www.geeksforgeeks.org/creating-decorator-inside-a-class-in-python/, Adapted from https://stackoverflow.com/questions/5929107/decorators-with-parameters
    def ensure_blockchain_ready(message: str) -> Callable:  # type: ignore
        def deco(fn: Callable) -> Callable:
            def instance(
                self: Any, *args: list[Any], **kwargs: dict[Any, Any]
            ) -> Callable | None:
                if self.is_blockchain_ready:
                    return fn(self, *args, **kwargs)

                logger_exception_handler(message=message, press_enter_to_continue=True)
                return None

            return instance

        return deco

    async def initialize(self) -> None:
        """
        A method that initialize resources needed for the blockchain system to work.

        TODO
        * If client_role is SIDE, then fetch or call update from the AdaptedPoERTConsensus to the MASTER node that is available. Also consider checking for unfinished tasks.
        """

        # Load the blockchain.

        self._chain: frozendict | None = await self._process_file_state(
            operation=BlockchainIOAction.TO_READ
        )

        # Test
        print(
            "\n\n\n Test #1 - Load the blockchain on file and render at least one block to see if its going to abort. \n\n\n"
        )
        await self.create_genesis_block()

        # * Check if there's a context inside of the JSON. If there's none then create 1 to 3 genesis blocks.
        if (
            self._chain is not None
            and "chain" in self._chain
            and not self._chain["chain"]
        ):
            for _ in range(BLOCKCHAIN_REQUIRED_GENESIS_BLOCKS):
                await self.create_genesis_block()  # * We can only afford to do per block since async will not detect other variable changes. I think we don't have a variable classifier that is meant to change dramatically without determined time. And that is 'volatile'.

            logger.info(
                "Genesis block generation has been finished! Blockchain system ready."
            )

    async def _append(
        self,
        *,
        context: Block | Transaction,
        auth_context: tuple[AddressUUID, JWTToken],
    ) -> None:
        """
        A method that is callad whenever a new block is ready to be inserted from the blockchain, both in-memory and to the file.

        Args:
            context (Block | Transaction): The context of the block as is.
            auth_context (tuple[AddressUUID, JWTToken]): Authentication attribute, not sure what to do on this one yet.

        TODO
        * Implement security of some sort, use `auth_context` or something. | We may use this and compute its hash for comparing context and also length.
        """
        if self._chain is not None:
            block_context = context.dict()
            block_context["contents"] = frozendict(block_context["contents"])
            self._chain["chain"].append(frozendict(block_context))
            await self._process_file_state(operation=BlockchainIOAction.TO_WRITE)

        else:
            logger_exception_handler(
                message="There's no 'chain' from the root dictionary of blockchain! This is a developer-implementation issue, please report to the developers as soon as possible!",
                press_enter_to_continue=True,
            )

    # Overwrites existing buffer from the frozendict if consensus has been established.
    async def _process_file_state(
        self,
        *,
        operation: BlockchainIOAction,
    ) -> frozendict | None:
        if operation in BlockchainIOAction:
            async with aopen(
                BLOCKCHAIN_RAW_PATH,
                "w" if operation == BlockchainIOAction.TO_WRITE else "r",
            ) as content_buffer:

                if operation == BlockchainIOAction.TO_WRITE:
                    await content_buffer.write(
                        export_to_json(
                            self._chain, default=self.serialize_to_file_blockchain
                        ).decode("utf-8")
                    )
                    return None

                else:
                    raw_data = await content_buffer.read()
                    partial_deserialized_data = import_raw_json_to_dict(raw_data)
                    deserialized_data = self.load_deserialized_blockchain(
                        partial_deserialized_data
                    )
                    logger.info(
                        f"Chain has been loaded from the file to the in-memory!"
                    )

                    return deserialized_data

        logger_exception_handler(
            message=f"Supplied value at 'operation' is not a valid enum! Got {operation} ({type(operation)}) instead. This is an internal error.",
            press_enter_to_continue=True,
        )
        return None

    def serialize_to_file_blockchain(self, o: frozendict) -> dict[str, Any]:
        """
        A method that serializes the python objects to the blockchain file. This represents the JSON form of the blockchain.

        Args:
            o (frozendict): The whole chain, wrapped in frozendict.

        Raises:
            TypeError: Cast TypeError when the constraint from the `o` is not followed.

        Returns:
            dict[str, Any]: Returns the JSON form of the blockchain that is in-memory.

        Note:
        TODO By this point, I still haven't consider for scalability and its impact from processing such data.
        * Until there's an impact, I will implement in-memory caching to reduce processing time and insert only data that is missing from the data pool.
        """

        if isinstance(o, frozendict):  # * Cast mutability on the whole chain.
            _o = dict(deepcopy(o))
            for block_idx, each_block in enumerate(_o["chain"]):
                # * Then cast mutability from the whole block of the chain.
                _o["chain"][block_idx] = dict(each_block)

                # * Lastly, cast mutability to the content of the whole block of the chain.
                _o["chain"][block_idx]["contents"] = dict(each_block["contents"])

            return _o

        raise TypeError

    def load_deserialized_blockchain(
        self,
        context: dict[str, Any],
    ) -> frozendict | None:
        """
        A method that deserializes the blockchain into an immutable dictionary (frozendict) from the outsourced-data of the blockchain file.

        Args:
            context (dict[str, Any]): The consumable data (type-compatible) that is loaded by the orjson.

        Returns:
            frozendict: Returns the immutable version of the given `context`.
        """

        # *  Ensure that the wrapped object is 'dict' regardless of their recent forms.
        if isinstance(context, dict):

            for dict_idx, dict_data in enumerate(context["chain"]):
                # * For every block, we have to deserialize (1) timestamps to `datetime`, (2) `content` to immutable 'dict' (frozendict) and transactions.

                context["chain"][dict_idx]["contents"] = frozendict(
                    dict_data["contents"]
                )
                # * Then, make the whole block immutable and insert it as reference from the blockchain.
                context["chain"][dict_idx] = frozendict(dict_data)

                # @o Check backward reference from the current block to recent block.
                if dict_idx:  # ! Mind the zero-based list access.
                    if (
                        dict_data["contents"]["prev_hash_block"]
                        != context["chain"][dict_idx - 1]["hash_block"]
                    ):
                        logger.critical(
                            f"Block #{dict_data['id']}'s backward reference to Block #{dict_data['id'] - 1} is invalid! | Expects (from Current Block): {dict_data['hash_block']}, got {context['chain'][dict_idx - 1]['contents']['prev_hash_block']} instead."
                        )

                        logger.critical(
                            "Due to potential fraudalent local blockchain file, please wait for the MASTER node to acknowledge your replacement of blockchain file."
                        )
                        self.blockchain_ready = False
                        # TODO: Create a task that waits for it to do something to fetch a valid blockchain file.

                        return None

                    logger.info(
                        f"Block #{dict_idx} backward reference to Block# {dict_idx - 1} is valid!"
                    )
                else:
                    logger.debug(
                        f"Block #{dict_data['id']} doesn't have a prev or leading block to compare reference, probably the latest block."
                    )

                # @o If cached_block_id is equal to dict_data["id"]. Then increment it easily.
                if self.cached_block_id == dict_data["id"]:
                    self.cached_block_id += 1
                    logger.debug(
                        f"Block has a valid recent reference. | Currently (Incremented) Cached ID: {self.cached_block_id}, Recent Block ID (Decremented by 1): {dict_data['id']}"
                    )

                # @o However, when its not equal then then something is wrong.
                else:
                    logger_exception_handler(
                        message=f"Blockchain is currently unchained! (Currently Cached: {self.cached_block_id} | Block ID: {dict_data['id']}) Some blocks are missing or is modified. This a developer-issue.",
                        press_enter_to_continue=True,
                    )

            logger.info(
                f"The blockchain context from the file (via deserialiation) has been loaded in-memory and is secured by immutability! | Next Block ID is Block #{self.cached_block_id}."
            )
            self.blockchain_ready = True
            return frozendict(context)

        logger_exception_handler(
            message=f"The given `context` is not a valid dictionary object! | Received: {context} ({type(context)}). This is a logic error, please report to the developers as soon as possible.",
            press_enter_to_continue=True,
        )

    async def create_genesis_block(self) -> None:
        """
        Generates a block, hash it and append it within the context of the blockchain, for both the file and the in-memory.
        """

        # Check for the genesis_block before inserting it.
        # TODO: We may need to use create_block since we have an unallocated_block.

        mined_genesis_block = await get_event_loop().run_in_executor(
            None, self.mine_block, self.create_block(transactions=None)
        )

        await self._append(
            context=mined_genesis_block, auth_context=get_identity_tokens()
        )

    def create_block(
        self,
        *,
        transactions: list[Transaction] | None,
    ) -> Block:

        # @o When building a block, we first have to consider that there are some properties were undefined. The nonce, block_size, and hash_block.
        # @o With this, we need to seperate the contents of the block, providing a way from the inside of the block to be hashable and identifiable for hash verification.
        # ! Several properties have to be seperated due to their nature of being able to overide the computed hash block.

        _block: Block = Block(
            id=self.cached_block_id,
            block_size=None,  # * Unsolvable at instantiation but can be filled before returning it.
            hash_block=None,  # ! Unsolvable, mine_block will handle it.
            contents=HashableBlock(
                nonce=None,  # ! Unsolvable, these are determined during the process of mining.
                validator=get_identity_tokens()[0],
                prev_hash_block=HashUUID("0" * BLOCK_HASH_LENGTH)
                if self.get_last_block is None
                else HashUUID(self.get_last_block.hash_block),  # type: ignore
                transactions=transactions,
                timestamp=datetime.now(),
            ),
        )

        _block.block_size = asizeof(_block.contents.json())
        self.cached_block_id += 1

        return _block

    async def create_transaction(self) -> None:
        return

    # # Cannot do keyword arguments here as per stated on excerpt: https://stackoverflow.com/questions/23946895/requests-in-asyncio-keyword-arguments
    def mine_block(self, block: Block) -> Block:
        # If success, then return the hash of the block based from the difficulty.
        prev: float = time()
        nth: int = 1

        logger.debug(f"Attempting to mine a Block #{block.id} ...")

        while True:
            # https://stackoverflow.com/questions/869229/why-is-looping-over-range-in-python-faster-than-using-a-while-loop, not sure if this works here as well.

            block.contents.nonce = randint(0, MAX_INT_PYTHON)
            computed_hash: HashUUID = HashUUID(
                sha256(block.json().encode("utf-8")).hexdigest()
            )

            if (
                computed_hash[:BLOCKCHAIN_HASH_BLOCK_DIFFICULTY]
                == "0" * BLOCKCHAIN_HASH_BLOCK_DIFFICULTY
            ):
                block.hash_block = computed_hash
                logger.info(
                    f"Block #{block.id} with a nonce value of {block.contents.nonce} has a resulting hash value of `{computed_hash}`, which has been mined for {time() - prev} under {nth} iteration/s!"
                )
                self.calculate_sleep_time(
                    mine_duration=time() - prev, mine_iteration=nth
                )
                return block

            nth += 1

    def get_sizeof(self, *, block: Block) -> int | None:
        if self.is_blockchain_ready:
            return asizeof(block)

        logger_exception_handler(
            message="Houston, we have a problem. Calling this method is not possible unless blockchain is ready! You may be attempting to perform operations that is beyond acceptable. We cannot continue from this.",
            press_enter_to_continue=True,
        )

    @ensure_blockchain_ready(
        message="Houston, we have a problem. This is illegal! There are no blocks to mine and you have parameters for this? This may be a developer-issue in regards to logic error. Though, we cannot recover from this due to some reason."
    )
    def calculate_sleep_time(
        self, *, mine_duration: float | int, mine_iteration: int
    ) -> None:
        if not self.is_blockchain_ready:
            self.consensus_timer = datetime.now() + timedelta(
                seconds=mine_duration + (mine_iteration / 1000)
            )
            return

    def set_node_state(self) -> None:
        self.node_ready = (
            True
            if datetime.now() >= self.consensus_timer and self.is_blockchain_ready
            else False
        )

    @property
    def is_node_ready(self) -> bool:
        return self.node_ready and self.is_blockchain_ready

    @property
    def is_blockchain_ready(self) -> bool:
        return self.blockchain_ready

    # I think this should work only on miner nodes.
    async def update_chain(self) -> None:
        # TODO: This should trigger when blockchain_ready is not True.
        pass

    # Ensure to follow the rule that we made last time.
    async def search_for(self, *, type: str, uid: AddressUUID | str) -> None:
        pass

    @property
    @ensure_blockchain_ready(
        message="Blockchain is not ready! It may have halted due to fraudalent actions which may have resulted to integrity loss. Please read back on the logs to see of what would have caused it."
    )
    def get_last_block(self) -> Block | None:
        # ! This return seems confusing but I have to sacrafice for my own sake of readability.
        # @o First we access the list by calling the key 'chain'.
        # @o Since we got to the list, we might wanna get the last block by slicing the list with the use of its own length - 1 to get the last block.
        # @o But before we do that, ensure that last item has a content. Accessing the last item with the use of index while it doesn't contain anything will result in `IndexError`.

        if len(self._chain["chain"]):
            last_block_ref = Block.parse_obj(
                self._chain["chain"][len(self._chain["chain"]) - 1 :][0]
            )
            logger.debug(f"Last block has been fetched. Context | {last_block_ref}")
            return last_block_ref

        logger.warning("There's no block inside blockchain.")

    async def close(self) -> None:
        pass


# # This approach was (not completely) taken from stackoverflow.
# * Please refer to the node/core/email.py:132 for more information.
blockchain_service: BlockchainMechanism | None = None


def get_blockchain_instance(
    *,
    role: NodeRoles | None = None,
) -> BlockchainMechanism:

    global blockchain_service
    token_ref: tuple[AddressUUID, JWTToken] | None = get_identity_tokens()

    logger.debug("Initializing or returning blockchain instance ...")

    if role and blockchain_service is None and token_ref is not None:
        # # Note that this will create an issue later when we tried SIDE node mode later on.
        blockchain_service = BlockchainMechanism(
            auth_tokens=token_ref,
            client_role=role,
        )

    # If there are no resulting objective, then we can log this as an error, otherwise return the object.
    if blockchain_service is None:
        logger.critical(
            "Unresolved role from this instance. Please specify your role. This may be a developer issue, please report this as possible or try again."
        )

    if token_ref is None:
        logger.critical(
            "There are no identity tokens inferred from your instance. A login authentication should not bypass this method from running. This a developer issue, please report as possible or try again."
        )

    logger.debug("Blockchain instance retrieved, returning to the requestor ...")
    return blockchain_service  # type: ignore # Not sure how can I comprehend where's the mistake, or I just got caffeine overdose to understand mypy's complaint.
