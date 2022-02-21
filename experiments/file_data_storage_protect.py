import json
from typing import Any, Dict
from cryptography.fernet import Fernet
from secrets import token_hex

# Prepare the values.
data_payload: Dict[str, Any] = {
    "blockchain": [
        {
            "block": 1,
            "nonce": 23023,
            "prev_block_hash": token_hex(16),
            "next_block_hash": token_hex(16),
            "contents": {"document_context": token_hex(64)},
        },
        {
            "block": 1,
            "nonce": 23023,
            "prev_block_hash": token_hex(16),
            "next_block_hash": token_hex(16),
            "contents": {"document_context": token_hex(64)},
        },
    ],
}

# TODO: On later instances, when the file is accessed, it should have an encrypted contents. It should still be asserted that the file is not movable or modifiable.


# Prepare an (empty) file and write the contents.
with open("blockchain.json", "w") as _:
    json.dump(data_payload, _)

# Encrpyt the file (contents) after copying it twice as much.
with open("blockchain_encrypted.json", "wb") as __:  # Take note of this one.
    original_context = json.dumps(data_payload).encode(
        "utf-8"
    )  # It's up to us if we wanna encrypt by JSON form or by taking it raw and convert the data as dict and return as JSOn with json.loads.
    encrypted_key = (
        Fernet.generate_key()
    )  # TODO: It's up with us on how we can unlock the file. It may seem that using runtime as a basis for the generation of the key may or may not be possible, or in other words, doesn't make any sense.

    encrypted_holder = Fernet(encrypted_key)
    encrypted_context = encrypted_holder.encrypt(original_context)

    __.write(encrypted_context)


# TODO: When there's nothing to do or there are tasks that is not important for a while, save the file as hashed.

# Decrypt the file.
with open("blockchain_encrypted.json", "rb") as ___:
    data_from_file = ___.read()

decrypted_contents = json.loads(
    encrypted_holder.decrypt(data_from_file).decode("utf-8")
)
print(decrypted_contents, type(decrypted_contents))

# Assert the output from the inputs.
assert (
    data_payload == decrypted_contents
), f"Parsed data and the original input is not equal!!! Original: {original_context} | Decrypted: {decrypted_contents}"

# # Assert anti-deletion move.
"""
Note that, this is going to be two ways. With that, for us to test this for both cases, we need
to import the platform identifier to see of what commands should we use.

But if we were able to find a library that can handle platform-specific functions, then all is good.

For Windows: Find a command that ticks the read-only file. Though I don't like this since I will be using Win32API.
# For Linux: [1] Do the chmod. [2] Or the chattr +i command: https://www.quora.com/Is-it-possible-to-make-a-file-undeletable-but-still-accessible

Now I know that using subprocess or some equivalent of os.system may hit our code quality
like getting shot in the head but let's see.

TODO: When I got VM, I will do this when I get back.
"""


# # Optional Testing: Checking for an Error when an SQL file is invalid.
