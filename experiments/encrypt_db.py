from cryptography.fernet import Fernet


TARGET_DB = "test.db"
OUTPUT_ENCRYPT_DB = "test-encrypt.db"
OUTPUT_DECRYPT_DB = "test-decrypted.db"
# First let's copy the original file.

# Read the file.
with open(TARGET_DB, "rb") as db_contents:
    data_from_file = db_contents.read()

# Encrypt a file.
with open(OUTPUT_ENCRYPT_DB, "wb") as db_encrypt_writer:
    key = Fernet.generate_key()
    context = Fernet(key)
    encrypted_context = context.encrypt(data_from_file)
    db_encrypt_writer.write(encrypted_context)

# Assert by decrypting it and creating a new file from it.

with open(OUTPUT_ENCRYPT_DB, "rb") as db_encrypted_reader:
    decrypted_from_file = db_encrypted_reader.read()

with open(OUTPUT_DECRYPT_DB, "wb") as db_decrypted_encrypt_writer:  # w?
    decrypted_context = context.decrypt(decrypted_from_file)
    db_decrypted_encrypt_writer.write(decrypted_context)

print("Done.")
