import os
import json
from cryptography.fernet import Fernet
import mysql.connector
from mysql.connector import Error


class DatabaseConnection:
    """
    Singleton class to manage the database connection.

    This class ensures that only one database connection is active at a time.
    It handles encrypted passwords for secure authentication.
    """

    _instance = None  # Stores the singleton instance
    _connection = None  # Stores the active database connection

    def __new__(cls, *args, **kwargs):
        """
        Ensures that only one instance of the DatabaseConnection class is created.

        :return: The singleton instance of DatabaseConnection.
        """
        if not cls._instance:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        """
        Initializes the database connection by setting paths for configuration and encryption key files.
        """
        # Set paths relative to the src/config directory
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "config"))
        self.config_file = os.path.join(base_dir, "db_config.json")
        self.key_file = os.path.join(base_dir, "encryption_key.key")

    def decrypt_password(self, encrypted_password):
        """
        Decrypts the encrypted password using the stored encryption key.

        :param encrypted_password: The encrypted password as a string.
        :return: The decrypted password as a string.
        :raises ValueError: If decryption fails or the key file is missing.
        """
        try:
            if not os.path.exists(self.key_file):
                raise FileNotFoundError(f"Encryption key file '{self.key_file}' not found.")

            with open(self.key_file, "rb") as key_file:
                key = key_file.read()

            fernet = Fernet(key)
            return fernet.decrypt(encrypted_password.encode()).decode()  # Decrypt the password
        except Exception as e:
            raise ValueError(f"Failed to decrypt password: {e}")

    def connect(self):
        """
        Establishes a connection to the MySQL database using configuration settings.

        If a connection is already established, it reuses the existing connection.

        :return: A MySQL connection object.
        :raises FileNotFoundError: If the database configuration file is missing.
        :raises ConnectionError: If there is an issue connecting to the database.
        """
        if not os.path.exists(self.config_file):
            raise FileNotFoundError(f"Database configuration file '{self.config_file}' not found.")

        # If no connection exists or it's disconnected, establish a new connection
        if not self._connection or not self._connection.is_connected():
            try:
                # Load database configuration from the JSON file
                with open(self.config_file, "r", encoding="utf-8") as file:
                    config = json.load(file)

                host = config["host"]
                database = config["database"]
                user = config["user"]
                encrypted_password = config["encrypted_password"]

                # Connect to the MySQL database using decrypted password
                self._connection = mysql.connector.connect(
                    host=host,
                    database=database,
                    user=user,
                    password=self.decrypt_password(encrypted_password)
                )
            except Error as e:
                raise ConnectionError(f"Error connecting to the database: {e}")

        return self._connection

    def close(self):
        """
        Closes the database connection if it is currently open.
        """
        if self._connection and self._connection.is_connected():
            self._connection.close()
            self._connection = None  # Reset the connection

    def __enter__(self):
        """
        Enables the use of the DatabaseConnection class as a context manager.

        :return: The active database connection.
        """
        return self.connect()

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Ensures that the database connection is closed when exiting the context.

        :param exc_type: The type of exception raised (if any).
        :param exc_val: The exception instance (if any).
        :param exc_tb: The traceback object (if any).
        """
        self.close()
