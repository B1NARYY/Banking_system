import socket
import threading
import random
import time
from config import HOST, PORT, TIMEOUT, CLIENT_TIMEOUT
from utils.logger import Logger
from commands import CommandHandler
from database.account_repository import AccountRepository


class BankServer:
    """
    Class representing a bank server in a P2P banking system.
    It handles incoming client connections, processes commands,
    and supports peer-to-peer communication with other bank servers.
    """

    def __init__(self):
        """Initializes the bank server, sets up networking, logging, and database connections."""
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((HOST, PORT))
        self.server_socket.listen(5)

        self.command_handler = CommandHandler(self)
        self.account_repository = AccountRepository()
        self.logger = Logger()
        self.ip_address = self.get_local_ip()

        self.logger.info(f"P2P Bank server started at {self.ip_address}:{PORT}")

    def get_local_ip(self):
        """
        Returns the IP address from the configuration file.
        """
        return HOST  # Use the configured IP instead of dynamically detecting it

    def handle_client(self, client_socket, address):
        """
        Handles communication with a connected client.
        Reads incoming data, processes commands, and sends responses.

        :param client_socket: The socket object for communication.
        :param address: The client's address (IP, port).
        """
        self.logger.info(f"Client connected: {address}")
        client_socket.settimeout(CLIENT_TIMEOUT)

        buffer = ""

        try:
            while True:
                try:
                    data = client_socket.recv(1024).decode("utf-8")
                    if not data:
                        break

                    buffer += data

                    while "\n" in buffer:
                        line, buffer = buffer.split("\n", 1)
                        command = line.strip()

                        if command:
                            self.logger.info(f"Received command from {address}: {command}")
                            start_time = time.time()  # Measure execution time

                            response = self.command_handler.process_command(command, address)

                            # Enforce timeout on processing
                            if time.time() - start_time > TIMEOUT:
                                self.logger.error(f"Command timeout: {command}")
                                response = "ER Processing timeout"

                            client_socket.sendall((response + "\n").encode("utf-8"))

                        client_socket.settimeout(CLIENT_TIMEOUT)

                except socket.timeout:
                    self.logger.error(f"Client {address} timed out – connection closed")
                    client_socket.sendall("ER Connection timed out\n".encode("utf-8"))
                    break

        except Exception as e:
            self.logger.error(f"Error communicating with {address}: {str(e)}")
            client_socket.sendall("ER Internal server error\n".encode("utf-8"))

        finally:
            client_socket.close()
            self.logger.info(f"Client {address} disconnected")

    def create_account(self, ip_address):
        """
        Creates a new bank account and stores it in the database.

        :param ip_address: The IP address associated with the account.
        :return: Success response with account number or error message.
        """
        self.logger.info(f"Creating account for IP: {ip_address}")

        for i in range(5):  # Attempt up to 5 times to find a unique account number
            account_number = random.randint(10000, 99999)

            if not self.account_repository.account_exists(account_number):
                self.logger.info(f"Generated unique account number: {account_number}")

                success = self.account_repository.create_account(account_number, ip_address)

                if success:
                    self.logger.info(f"Account {account_number}/{ip_address} successfully created and saved to DB")
                    return f"AC {account_number}/{ip_address}"
                else:
                    self.logger.error("Database error while creating account")
                    return "ER Database error"

        self.logger.error("Failed to generate a unique account number")
        return "ER Unable to create account"

    def forward_to_peer(self, peer_ip, command):
        """
        Attempts to connect to another bank's server on multiple ports and forwards the command.

        :param peer_ip: The IP address of the target bank.
        :param command: The command to be sent.
        :return: The response from the peer bank or an error message if the connection fails.
        """
        possible_ports = range(65525, 65536)  # Range of valid ports
        start_time = time.time()

        for peer_port in possible_ports:
            if time.time() - start_time > TIMEOUT:
                self.logger.error("Exceeded maximum allowed time for peer communication")
                return "ER Request timeout"

            try:
                self.logger.info(f"Trying {peer_ip}:{peer_port} for forwarding command: {command}")

                with socket.create_connection((peer_ip, peer_port), timeout=TIMEOUT) as s:
                    s.sendall((command + "\n").encode("utf-8"))
                    response = s.recv(1024).decode("utf-8").strip()

                self.logger.info(f"Received response from {peer_ip}:{peer_port}: {response}")
                return response
            except Exception as e:
                self.logger.error(f"Failed to connect to {peer_ip}:{peer_port}: {e}")

        self.logger.error(f"Unable to connect to peer {peer_ip} on any port")
        return "ER Peer connection failed"

    def start(self):
        """
        Starts the bank server and listens for incoming client connections.
        Runs indefinitely, accepting multiple clients in parallel.
        """
        self.logger.info("Bank server is running and waiting for clients...")
        while True:
            client_socket, address = self.server_socket.accept()
            client_socket.settimeout(CLIENT_TIMEOUT)
            threading.Thread(target=self.handle_client, args=(client_socket, address), daemon=True).start()
