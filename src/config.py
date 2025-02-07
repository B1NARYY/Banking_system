import os
import json

# Get the absolute path to the directory where config.py is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, "config.json")

def load_config(config_path=CONFIG_PATH):
    """
    Loads the configuration from the JSON file.

    :param config_path: Path to the configuration file.
    :return: A dictionary containing configuration values.
    :raises FileNotFoundError: If the configuration file is missing.
    """
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file '{config_path}' not found.")
    
    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)
    
    return config

# Load the configuration
config = load_config()

# Configuration parameters
HOST = config.get("HOST", "0.0.0.0")  # Default to all network interfaces
PORT = config.get("PORT", 65530)  # Default listening port
TIMEOUT = config.get("TIMEOUT", 5)  # Response timeout for processing commands
CLIENT_TIMEOUT = config.get("CLIENT_TIMEOUT", 5)  # Client inactivity timeout
LOG_FILE = config.get("LOG_FILE", "logs/bank.log")  # Path to log file
