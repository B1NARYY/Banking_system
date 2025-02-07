import socket
from utils.logger import Logger


class CommandHandler:
    """
    Class responsible for processing incoming banking commands and routing them to the appropriate handlers.

    Each command follows the P2P banking protocol and interacts with either the local bank or forwards requests
    to another bank if needed.
    """

    def __init__(self, server):
        """
        Initializes the CommandHandler.

        :param server: Instance of the BankServer to interact with.
        """
        self.server = server
        self.logger = Logger()

    def process_command(self, command, address):
        """
        Processes incoming commands and routes them to the appropriate handler.

        :param command: The received command as a string.
        :param address: The address of the client sending the command.
        :return: The response string to be sent back to the client.
        """
        parts = command.strip().split()
        if not parts:
            return "ER Invalid command"

        cmd = parts[0].upper()

        try:
            if cmd == "BC":
                return self.handle_bc()
            elif cmd == "AC":
                return self.handle_ac(address[0])
            elif cmd == "AD":
                return self.handle_ad(parts)
            elif cmd == "AW":
                return self.handle_aw(parts)
            elif cmd == "AB":
                return self.handle_ab(parts)
            elif cmd == "AR":
                return self.handle_ar(parts)
            elif cmd == "BA":
                return self.handle_ba()
            elif cmd == "BN":
                return self.handle_bn()
            else:
                return "ER Unknown command"
        except Exception as e:
            self.logger.error(f"Error processing command {command}: {str(e)}")
            return "ER Internal processing error"

    def handle_bc(self):
        """
        Handles the BC (Bank Code) command.

        :return: The IP address of the current bank node.
        """
        try:
            ip_address = self.server.get_local_ip()
            self.logger.info(f"Response to BC: {ip_address}")
            return f"BC {ip_address}"
        except Exception as e:
            self.logger.error(f"Error getting IP: {e}")
            return "ER Unable to retrieve IP"

    def handle_ac(self, ip_address):
        """
        Handles the AC (Account Creation) command.

        :param ip_address: The IP address of the client requesting the account creation.
        :return: A response indicating the success or failure of the operation.
        """
        return self.server.create_account(ip_address)

    def handle_ad(self, parts):
        """
        Handles the AD (Account Deposit) command.

        :param parts: List of command parts where parts[1] is account information and parts[2] is the amount.
        :return: A response indicating success or failure of the deposit operation.
        """
        if len(parts) != 3:
            return "ER Invalid AD format"

        try:
            account_info, amount = parts[1], int(parts[2])
            account_number, bank_ip = account_info.split("/")

            if bank_ip != self.server.get_local_ip():
                return self.server.forward_to_peer(bank_ip, f"AD {account_number}/{bank_ip} {amount}")

            return "AD" if self.server.account_repository.deposit(account_number, amount) else "ER Deposit failed"
        except ValueError:
            return "ER Invalid deposit format"

    def handle_aw(self, parts):
        """
        Handles the AW (Account Withdrawal) command.

        :param parts: List of command parts where parts[1] is account information and parts[2] is the amount.
        :return: A response indicating success or failure of the withdrawal operation.
        """
        if len(parts) != 3:
            return "ER Invalid AW format"

        try:
            account_info, amount = parts[1], int(parts[2])
            account_number, bank_ip = account_info.split("/")

            # If the target bank is different, forward the request
            if bank_ip != self.server.get_local_ip():
                return self.server.forward_to_peer(bank_ip, f"AW {account_number}/{bank_ip} {amount}")

            return "AW" if self.server.account_repository.withdraw(account_number, amount) else "ER Not enough funds"
        except ValueError:
            return "ER Invalid withdrawal format"

    def handle_ab(self, parts):
        """
        Handles the AB (Account Balance) command.

        :param parts: List of command parts where parts[1] is the account information.
        :return: The balance of the specified account or an error message.
        """
        if len(parts) != 2:
            return "ER Invalid AB format"

        try:
            account_info = parts[1]
            account_number, bank_ip = account_info.split("/")

            if bank_ip != self.server.get_local_ip():
                return self.server.forward_to_peer(bank_ip, f"AB {account_number}/{bank_ip}")

            balance = self.server.account_repository.get_balance(account_number)
            return f"AB {balance}" if balance is not None else "ER Account not found"
        except ValueError:
            return "ER Invalid account format"

    def handle_ar(self, parts):
        """
        Handles the AR (Account Removal) command.

        :param parts: List of command parts where parts[1] is the account information.
        :return: A response indicating success or failure of the account removal operation.
        """
        if len(parts) != 2:
            return "ER Invalid AR format"

        try:
            account_info = parts[1]
            account_number, bank_ip = account_info.split("/")

            if bank_ip != self.server.get_local_ip():
                return self.server.forward_to_peer(bank_ip, f"AR {account_number}/{bank_ip}")

            return "AR" if self.server.account_repository.remove(account_number) else "ER Cannot remove account"
        except ValueError:
            return "ER Invalid account format"

    def handle_ba(self):
        """
        Handles the BA (Bank Total Balance) command.

        :return: The total balance of all accounts in the bank.
        """
        return f"BA {self.server.account_repository.get_total_balance()}"

    def handle_bn(self):
        """
        Handles the BN (Bank Number of Clients) command.

        :return: The total number of clients with accounts in the bank.
        """
        return f"BN {self.server.account_repository.count_accounts()}"
