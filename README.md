# P2P Bank System

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [Command List](#command-list)
- [Logging](#logging)
- [Database Persistence](#database-persistence)
- [Security](#security)
- [Troubleshooting](#troubleshooting)
- [License](#license)

---

## Introduction
The **P2P Bank System** is a decentralized peer-to-peer banking network where each node represents a bank. Users can create accounts, deposit and withdraw money, check balances, and communicate with other banks in the network. The system allows seamless interbank communication and transactions between different instances running on separate machines.

---

## Features
- Supports **account creation**, **deposits**, **withdrawals**, **balance inquiries**, and **account removal**.
- **Interbank communication**: Can forward transactions to other nodes if the target account belongs to another bank.
- **Fault tolerance**: Uses timeouts for client handling and interbank requests.
- **Persistent data storage**: Ensures account and balance data remains intact across restarts.
- **Command-based interface**: Can be accessed via **PuTTY, telnet, or other TCP clients**.
- **Logging system**: Tracks all transactions, errors, and server activity for debugging and monitoring.

---

## Installation
### Prerequisites
Ensure your system has the following installed:
- **Python 3.8+**
- Required Python libraries:
  ```sh
  pip install -r requirements.txt
  ```


---

## Configuration
The server settings are stored in `config.json`. Update it as needed:
```json
{
    "HOST": "0.0.0.0",
    "PORT": 65530,
    "TIMEOUT": 5,
    "CLIENT_TIMEOUT": 10,
    "LOG_FILE": "logs/bank.log"
}
```
- **HOST**: IP address where the server listens (default: `0.0.0.0` for all interfaces).
- **PORT**: TCP port for communication (must be within `65525-65535`).
- **TIMEOUT**: Maximum wait time (in seconds) for responses from other banks.
- **CLIENT_TIMEOUT**: Maximum time before disconnecting an inactive client.
- **LOG_FILE**: Path to the log file.

---

## Running the Application
To start the server, run the following commands in the CMD
```sh
python -m venv venv

venv\Scripts\activate

pip install -r requirements.txt

set PYTHONPATH=%CD%

python src/main.py
```

To connect to the server using PuTTY, use from configuration file:
```sh
    Host Name: "HOST"
    Port: "PORT"
    Connection type: "RAW"
```


---

## Command List
| Command | Description | Example |
|---------|-------------|---------|
| `BC` | Get bank's IP address | `BC` → `BC 192.168.1.100` |
| `AC` | Create a new account | `AC` → `AC 12345/192.168.1.100` |
| `AD` | Deposit money into an account | `AD 12345/192.168.1.100 500` → `AD` |
| `AW` | Withdraw money | `AW 12345/192.168.1.100 200` → `AW` |
| `AB` | Get account balance | `AB 12345/192.168.1.100` → `AB 300` |
| `AR` | Remove an account (if balance is 0) | `AR 12345/192.168.1.100` → `AR` |
| `BA` | Get total bank balance | `BA` → `BA 100000` |
| `BN` | Get total number of clients | `BN` → `BN 5` |

---

## Logging
All server activity is logged in `logs/bank.log`. This includes:
- Client connections and disconnections
- Commands received and responses sent
- Errors and warnings
- Interbank communication attempts

---

## Database Persistence
The application uses **MySQL** to store bank accounts and balances. Ensure MySQL is running and configured properly. The database connection details are stored in `config/db_config.json`.
If you want to use a different database, view `encrypt_password.py` and follow the instructions to encrypt the password.
Database structure:
```sql
CREATE TABLE accounts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    account_number INT UNIQUE NOT NULL,
    ip_address VARCHAR(15) NOT NULL,
    balance DECIMAL(15,2) NOT NULL DEFAULT 0
);
```

---

## Security
- **Encrypted database credentials**: Passwords are stored in an encrypted format.
- **Connection timeouts**: Prevents abuse by limiting inactive connections.
- **Input validation**: Ensures all commands follow strict formatting rules.

---

## Troubleshooting
### Connection Issues
- Ensure the server is running on the correct port.
- Check firewall settings to allow incoming TCP connections.
- Verify MySQL is running and the database is properly configured.

### Command Issues
- Ensure commands are formatted correctly (`COMMAND ACCOUNT/IP AMOUNT` where applicable).
- Check the log file (`logs/bank.log`) for errors.

### Interbank Communication Failures
- Ensure other banks are online and accessible.
- Verify that the correct IP addresses are being used.

---

## Sources 
### Reused Code 
logger.py:          
[https://github.com/B1NARYY/Sleeping-barber-problem/blob/master/src/logger.py](https://github.com/B1NARYY/Sleeping-barber-problem/blob/master/src/logger.py)

connection.py:
[https://github.com/B1NARYY/Database_system_with_transactions/blob/master/src/connection.py](https://github.com/B1NARYY/Database_system_with_transactions/blob/master/src/connection.py)

encrypt_password.py:
[https://github.com/B1NARYY/Database_system_with_transactions/blob/master/src/passwordEncryption.py](https://github.com/B1NARYY/Database_system_with_transactions/blob/master/src/passwordEncryption.py)


### Sources 
- **MySQL in Python**: [https://www.w3schools.com/python/python_mysql_getstarted.asp](https://www.w3schools.com/python/python_mysql_getstarted.asp)
- **Cryptography in Python (Fernet Encryption)**: [https://cryptography.io/en/latest/fernet/](https://cryptography.io/en/latest/fernet/)
- **Logging Guide**: [https://www.dataset.com/blog/the-10-commandments-of-logging/](https://www.dataset.com/blog/the-10-commandments-of-logging/)
- **ChatGPT (Sharing conversations with user uploaded images is not yet supported)**: [https://chatgpt.com/c/67a1039e-4054-8001-886f-f17594b370d9](https://chatgpt.com/c/67a1039e-4054-8001-886f-f17594b370d9)
- **Python Documentation (ChatGPT)**: [https://docs.python.org/3/](https://docs.python.org/3/)

---