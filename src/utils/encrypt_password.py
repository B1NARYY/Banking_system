from cryptography.fernet import Fernet


def generate_encryption_key(file_path="../config/encryption_key.key"):
    """
    Generate a new encryption key and save it to a file.
    """
    key = Fernet.generate_key()
    with open(file_path, "wb") as key_file:
        key_file.write(key)
    print(f"Encryption key generated and saved to {file_path}")


def encrypt_password(plain_password, key_file="../config/encryption_key.key"):
    """
    Encrypt a plain password using an encryption key.
    Args:
        plain_password (str): The password to encrypt.
        key_file (str): Path to the encryption key file.
    Returns:
        str: Encrypted password.
    """
    with open(key_file, "rb") as file:
        key = file.read()

    fernet = Fernet(key)
    encrypted_password = fernet.encrypt(plain_password.encode()).decode()
    return encrypted_password


if __name__ == "__main__":
    "Run this script to generate an encryption key and encrypt a password."
    plain_password = ""

    key_file_path = "../config/encryption_key.key"

    try:
        with open(key_file_path, "rb") as _:
            print(f"Encryption key already exists at {key_file_path}")
    except FileNotFoundError:
        generate_encryption_key(key_file_path)

    encrypted_password = encrypt_password(plain_password, key_file_path)
    print(f"Encrypted password: {encrypted_password}")

    print(f"Replace the 'encrypted_password' field in your 'db_config.json' with the following value:")
    print(encrypted_password)
