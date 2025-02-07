from src.database.connection import DatabaseConnection
from src.utils.logger import Logger


class AccountRepository:
    """
    Class responsible for managing bank accounts in the database.
    Provides functionalities such as account creation, deposits, withdrawals, balance checks, and account removal.
    """

    def __init__(self):
        """
        Initializes the repository with a database connection and a logger.
        """
        self.db = DatabaseConnection()
        self.logger = Logger()

    def create_account(self, account_number, ip_address):
        """
        Inserts a new bank account into the database.

        :param account_number: Unique identifier for the account.
        :param ip_address: IP address associated with the account.
        :return: True if the account was created successfully, False otherwise.
        """
        query = "INSERT INTO accounts (account_number, ip_address, balance) VALUES (%s, %s, %s)"
        values = (account_number, ip_address, 0)  # New accounts start with a balance of 0

        try:
            conn = self.db.connect()
            cursor = conn.cursor()
            cursor.execute(query, values)
            conn.commit()
            cursor.close()
            self.logger.info(f"Account {account_number}/{ip_address} created in database")
            return True
        except Exception as e:
            self.logger.error(f"Error creating account: {e}")
            return False

    def get_balance(self, account_number):
        """
        Retrieves the balance of a given account.

        :param account_number: The account number to check the balance for.
        :return: The balance if the account exists, otherwise None.
        """
        query = "SELECT balance FROM accounts WHERE account_number = %s"

        try:
            conn = self.db.connect()
            cursor = conn.cursor()
            cursor.execute(query, (account_number,))
            balance = cursor.fetchone()
            cursor.close()
            return balance[0] if balance else None
        except Exception as e:
            self.logger.error(f"Error retrieving balance: {e}")
            return None

    def deposit(self, account_number, amount):
        """
        Deposits money into an account.

        :param account_number: The account number to deposit money into.
        :param amount: The amount to deposit.
        :return: True if the deposit was successful, False otherwise.
        """
        query = "UPDATE accounts SET balance = balance + %s WHERE account_number = %s"

        try:
            conn = self.db.connect()
            cursor = conn.cursor()
            cursor.execute(query, (amount, int(account_number)))  # Ensure account_number is an integer
            conn.commit()
            cursor.close()
            return cursor.rowcount > 0  # Returns True if at least one row was updated
        except Exception as e:
            self.logger.error(f"Error depositing money: {e}")
            return False

    def withdraw(self, account_number, amount):
        """
        Withdraws money from an account, ensuring the account has sufficient funds.

        :param account_number: The account number to withdraw from.
        :param amount: The amount to withdraw.
        :return: True if the withdrawal was successful, False otherwise.
        """
        query = "UPDATE accounts SET balance = balance - %s WHERE account_number = %s AND balance >= %s"

        try:
            conn = self.db.connect()
            cursor = conn.cursor()
            cursor.execute(query, (amount, int(account_number), amount))  # Ensure account_number is an integer
            conn.commit()
            cursor.close()
            return cursor.rowcount > 0  # Returns True if at least one row was updated
        except Exception as e:
            self.logger.error(f"Error withdrawing money: {e}")
            return False

    def remove(self, account_number):
        """
        Deletes an account from the database only if its balance is 0.

        :param account_number: The account number to remove.
        :return: True if the account was removed, False otherwise.
        """
        query = "DELETE FROM accounts WHERE account_number = %s AND balance = 0"

        try:
            conn = self.db.connect()
            cursor = conn.cursor()
            cursor.execute(query, (int(account_number),))  # Ensure account_number is an integer
            conn.commit()
            cursor.close()
            return cursor.rowcount > 0  # Returns True if at least one row was deleted
        except Exception as e:
            self.logger.error(f"Error removing account: {e}")
            return False

    def get_total_balance(self):
        """
        Retrieves the total balance across all accounts in the bank.

        :return: Total balance of the bank, or None in case of an error.
        """
        query = "SELECT SUM(balance) FROM accounts"

        try:
            conn = self.db.connect()
            cursor = conn.cursor()
            cursor.execute(query)
            total_balance = cursor.fetchone()[0] or 0
            cursor.close()
            return total_balance
        except Exception as e:
            self.logger.error(f"Error getting total bank balance: {e}")
            return None

    def count_accounts(self):
        """
        Counts the total number of accounts in the bank.

        :return: Number of accounts, or None in case of an error.
        """
        query = "SELECT COUNT(*) FROM accounts"

        try:
            conn = self.db.connect()
            cursor = conn.cursor()
            cursor.execute(query)
            count = cursor.fetchone()[0]
            cursor.close()
            return count
        except Exception as e:
            self.logger.error(f"Error counting accounts: {e}")
            return None

    def account_exists(self, account_number):
        """
        Checks whether an account exists in the database.

        :param account_number: The account number to check.
        :return: True if the account exists, False otherwise.
        """
        query = "SELECT COUNT(*) FROM accounts WHERE account_number = %s"

        try:
            conn = self.db.connect()
            cursor = conn.cursor()
            cursor.execute(query, (account_number,))
            count = cursor.fetchone()[0]
            cursor.close()
            return count > 0
        except Exception as e:
            self.logger.error(f"Error checking account existence: {e}")
            return False

    def get_all_accounts(self):
        """
        Retrieves all accounts from the database along with their balances.

        :return: A list of dictionaries containing account_number and balance, or an empty list in case of an error.
        """
        query = "SELECT account_number, balance FROM accounts"

        try:
            conn = self.db.connect()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query)
            accounts = cursor.fetchall()
            cursor.close()
            return accounts
        except Exception as e:
            self.logger.error(f"Error fetching accounts: {e}")
            return []
