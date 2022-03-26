from asyncio import get_event_loop, sleep
from copy import deepcopy
from datetime import datetime, timedelta
from hashlib import sha256
from logging import Logger, getLogger
from random import randint
from sys import maxsize as MAX_INT_PYTHON
from time import time
from typing import Any, Callable, Final

from aiofiles import open as aopen
from blueprint.models import file_signatures
from blueprint.schemas import Block, HashableBlock, NodeMasterInformation, Transaction
from frozendict import frozendict
from orjson import dumps as export_to_json
from orjson import loads as import_raw_json_to_dict
from pympler.asizeof import asizeof
from utils.processors import unconventional_terminate

from core.consensus import AdaptedPoETConsensus
from core.constants import (
    ASYNC_TARGET_LOOP,
    BLOCK_HASH_LENGTH,
    BLOCKCHAIN_HASH_BLOCK_DIFFICULTY,
    BLOCKCHAIN_NAME,
    BLOCKCHAIN_RAW_PATH,
    BLOCKCHAIN_REQUIRED_GENESIS_BLOCKS,
    AddressUUID,
    BlockchainIOAction,
    HashUUID,
    JWTToken,
    NodeType,
)
from core.dependencies import get_db_instance, get_identity_tokens
from core.tasks import AsyncTaskQueue

logger: Logger = getLogger(ASYNC_TARGET_LOOP)

# TODO: Should we seperate consensus from this class?
class BlockchainMechanism(AsyncTaskQueue, AdaptedPoETConsensus):
    def __init__(
        self,
        *,
        block_timer: int = 5,
        auth_tokens: tuple[AddressUUID, JWTToken],
        client_role: NodeType,
    ) -> None:

        # TODO: After finalization, seperate some methods and attributes for the ARCHIVAL_MINER_NODE and MASTER_NODE.
        # Required since this class will be invoked no matter what the role of the client instance is.

        # * Required Variables for the Blockchain Operaetion.
        self.node_role: NodeType = client_role
        self.auth_token: tuple[AddressUUID, JWTToken] = auth_tokens
        self.block_timer: Final[int] = block_timer
        self.consensus_timer: datetime = (
            datetime.now()
        )  # TODO: This will be computed based on the information by the MASTER_NODE node on how much is being participated, along with its computed value based on the average mining and iteration.

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

                unconventional_terminate(message=message)
                return None

            return instance

        return deco

    async def initialize(self) -> None:
        """
        A method that initialize resources needed for the blockchain system to work.

        TODO
        * If client_role is ARCHIVAL_MINER_NODE, then fetch or call update from the AdaptedPoERTConsensus to the MASTER_NODE node that is available. Also consider checking for unfinished tasks.
        """

        # Load the blockchain.

        self._chain: frozendict | None = await self._process_file_state(
            operation=BlockchainIOAction.TO_READ
        )

        # * Check if there's a context inside of the JSON. If there's none then create 1 to 3 genesis blocks.
        if (
            self._chain is not None
            and "chain" in self._chain
            and not self._chain["chain"]
        ):
            for _ in range(0, BLOCKCHAIN_REQUIRED_GENESIS_BLOCKS):
                await self.create_genesis_block()  # * We can only afford to do per block since async will not detect other variable changes. I think we don't have a variable classifier that is meant to change dramatically without determined time. And that is 'volatile'.

            # @o When on initial instance, we need to handle the property for the blockchain system to run. Otherwise we just lock out the system even we already created.
            self.blockchain_ready = True

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

            # @o If a certain block has been inserted in a way that it is way over far or less than the current self.cached_block_id, then disregard this block.
            if block_context["id"] != self.cached_block_id:
                logger.error(
                    f"This block #{block_context['id']} is way too far or behind than the one that is saved in the local blockchain file. Will attempt to fetch a new blockchain file from the MASTER_NODE node. This block will be DISREGARDED."
                )
                return

            self._chain["chain"].append(frozendict(block_context))
            self.cached_block_id += 1
            await self._process_file_state(operation=BlockchainIOAction.TO_WRITE)
            await self.sleeping_phase()

        else:
            unconventional_terminate(
                message="There's no 'chain' from the root dictionary of blockchain! This is a developer-implementation issue, please report to the developers as soon as possible!",
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
                    byte_json_content: bytes = export_to_json(
                        self._chain, default=self.serialize_to_file_blockchain
                    )

                    logger.debug(
                        f"Updating blockchain file's hash signature on database. | Targets: {BLOCKCHAIN_RAW_PATH}"
                    )
                    new_blockchain_hash: str = sha256(byte_json_content).hexdigest()

                    blockchain_hash_update_stmt = (
                        file_signatures.update()
                        .where(file_signatures.c.filename == BLOCKCHAIN_NAME)
                        .values(hash_signature=new_blockchain_hash)
                    )
                    logger.debug(
                        f"Blockchain's file signature has been changed! | Current Hash: {new_blockchain_hash}"
                    )

                    await get_db_instance().execute(blockchain_hash_update_stmt)

                    await content_buffer.write(byte_json_content.decode("utf-8"))
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

        unconventional_terminate(
            message=f"Supplied value at 'operation' is not a valid enum! Got {operation} ({type(operation)}) instead. This is an internal error.",
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
                        dict_data["prev_hash_block"]
                        != context["chain"][dict_idx - 1]["hash_block"]
                    ):
                        logger.critical(
                            f"Block #{dict_data['id']}'s backward reference to Block #{dict_data['id'] - 1} is invalid! | Expects (from Current Block): {dict_data['hash_block']}, got {context['chain'][dict_idx - 1]['prev_hash_block']} instead."
                        )

                        logger.critical(
                            "Due to potential fraudalent local blockchain file, please wait for the MASTER_NODE node to acknowledge your replacement of blockchain file."
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
                    unconventional_terminate(
                        message=f"Blockchain is currently unchained! (Currently Cached: {self.cached_block_id} | Block ID: {dict_data['id']}) Some blocks are missing or is modified. This a developer-issue.",
                    )
                    return None

            logger.info(
                f"The blockchain context from the file (via deserialiation) has been loaded in-memory and is secured by immutability! | Next Block ID is Block #{self.cached_block_id}."
            )
            self.blockchain_ready = True
            return frozendict(context)

        unconventional_terminate(
            message=f"The given `context` is not a valid dictionary object! | Received: {context} ({type(context)}). This is a logic error, please report to the developers as soon as possible.",
        )

    async def create_genesis_block(self) -> None:
        """
        Generates a block, hash it and append it within the context of the blockchain, for both the file and the in-memory.
        """

        # Check for the genesis_block before inserting it.
        # TODO: We may need to use create_block since we have an unallocated_block.

        mined_genesis_block = await get_event_loop().run_in_executor(
            None,
            self.mine_block,
            self.create_block(transactions=None),
        )

        await self._append(
            context=mined_genesis_block, auth_context=get_identity_tokens()
        )

    def create_block(
        self,
        *,
        transactions: list[Transaction] | None,
    ) -> Block | None:

        # @o When building a block, we first have to consider that there are some properties were undefined. The nonce, block_size, and hash_block.
        # @o With this, we need to seperate the contents of the block, providing a way from the inside of the block to be hashable and identifiable for hash verification.
        # ! Several properties have to be seperated due to their nature of being able to overide the computed hash block.

        if self.get_last_block is not None:
            if self.get_last_block.id >= self.cached_block_id:
                logger.critical(
                    f"Cannot create a block! Last block is greater than or equal to the ID of the currently cached available-to-allocate block. | Last Block ID: {self.get_last_block.id} | Currently Cached: {self.cached_block_id}"
                )
                return None
        else:
            logger.warning(
                f"This new block wil be the first block from this blockchain."
            )

        _block: Block = Block(
            id=self.cached_block_id,
            block_size=None,  # * Unsolvable at instantiation but can be filled before returning it.
            hash_block=None,  # ! Unsolvable, mine_block will handle it.
            prev_hash_block=HashUUID("0" * BLOCK_HASH_LENGTH) if self.get_last_block is None else HashUUID(self.get_last_block.hash_block),  # type: ignore
            contents=HashableBlock(
                nonce=None,  # ! Unsolvable, these are determined during the process of mining.
                validator=get_identity_tokens()[0],
                transactions=transactions,
                timestamp=datetime.now(),
            ),
        )

        _block.block_size = asizeof(_block.contents.json())
        return _block

    async def create_transaction(self) -> None:
        return

    # # Cannot do keyword arguments here as per stated on excerpt: https://stackoverflow.com/questions/23946895/requests-in-asyncio-keyword-arguments
    def mine_block(self, block: Block) -> Block:
        # If success, then return the hash of the block based from the difficulty.
        self.blockchain_ready = False
        prev: float = time()
        nth: int = 1

        logger.info(f"Attempting to mine a Block #{block.id} ...")

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
                self.blockchain_ready = True
                return block

            nth += 1

    @ensure_blockchain_ready(
        message="Houston, we have a problem. Calling this method is not possible unless blockchain is ready! You may be attempting to perform operations that is beyond acceptable. We cannot continue from this.",
    )
    def get_sizeof(self, *, block: Block) -> int | None:
        return asizeof(block)

    @property
    def get_blockchain_public_state(self) -> NodeMasterInformation | None:
        if self.node_role == NodeType.MASTER_NODE:
            return NodeMasterInformation(
                block_timer=self.block_timer,
                total_addresses=9999,
                total_blocks=len(self._chain["chain"])
                if self._chain is not None
                else 0,
                total_transactions=69420,
            )
        logger.critical(
            f"This client node requests for the `public_state` when their role is {self.node_role}! | Expects: {NodeType.MASTER_NODE}."
        )
        return None

    @property
    def get_blockchain_private_state(self) -> dict[str, Any]:
        return {
            "sleeping": self.is_node_ready,
            "mining": self.is_blockchain_ready,
            "consensus_timer": self.consensus_timer,
            "last_mined_block": self.get_last_block.id if self.get_last_block is not None else 0,  # type: ignore | Ignoring the 'None' case,
        }

    def get_blocks(self, limit_to: int) -> None:
        if self._chain is not None:
            return self._chain["chain"][len(self._chain["chain"]) - limit_to :]

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
        if not self.is_blockchain_ready:
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

    async def sleeping_phase(self) -> None:
        while not self.is_node_ready:
            await sleep(
                (datetime.now() - self.consensus_timer).seconds
            )  # Avoids spamming.
            self.set_node_state()

    async def close(self) -> None:
        return


# # This approach was (not completely) taken from stackoverflow.
# * Please refer to the node/core/email.py:132 for more information.
blockchain_service: BlockchainMechanism | None = None


def get_blockchain_instance(
    *,
    role: NodeType | None = None,
) -> BlockchainMechanism:

    global blockchain_service
    token_ref: tuple[AddressUUID, JWTToken] | None = get_identity_tokens()

    logger.debug("Initializing or returning blockchain instance ...")

    if role and blockchain_service is None and token_ref is not None:
        # # Note that this will create an issue later when we tried ARCHIVAL_MINER_NODE node mode later on.
        blockchain_service = BlockchainMechanism(
            auth_tokens=token_ref,
            client_role=role,
        )

    # If there are no resulting objective, then we can log this as an error, otherwise return the object.
    if blockchain_service is None:
        logger.critical("There are no blockchain instance.")

    if token_ref is None:
        logger.critical(
            "There are no identity tokens inferred from your instance. A login authentication should not bypass this method from running. This a developer issue, please report as possible or try again."
        )

    logger.debug("Blockchain instance retrieved, returning to the requestor ...")
    return blockchain_service  # type: ignore # Not sure how can I comprehend where's the mistake, or I just got caffeine overdose to understand mypy's complaint.
