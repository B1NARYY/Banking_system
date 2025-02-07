import logging
import os
from datetime import datetime

class Logger:
    """
    Logger class for structured logging in the banking system.
    - Ensures logs are stored in a structured directory.
    - Supports logging to a unique file per run.
    """

    _instance = None  # Singleton instance

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance._setup_logger()
        return cls._instance

    def _setup_logger(self):
        """
        Initializes the logger, sets up log directory, and configures handlers.
        """
        # Define the root directory for logs
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
        logs_dir = os.path.join(project_root, 'logs')

        # Ensure the logs directory exists
        if not os.path.exists(logs_dir):
            os.makedirs(logs_dir)

        # Create a unique directory for each run
        run_dir_name = datetime.now().strftime("run_%Y%m%d_%H%M%S")
        self.run_dir_path = os.path.join(logs_dir, run_dir_name)

        if not os.path.exists(self.run_dir_path):
            os.makedirs(self.run_dir_path)

        # Path to the main log file
        total_log_path = os.path.join(self.run_dir_path, "total.log")

        # Configure the logger
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

        # Define the log format
        formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

        # Set up the file handler for logging
        file_handler = logging.FileHandler(total_log_path, mode='a')
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def info(self, message):
        """Logs an INFO level message."""
        self.logger.info(message)
        print(f"[INFO] {message}")

    def error(self, message):
        """Logs an ERROR level message."""
        self.logger.error(message)
        print(f"[ERROR] {message}")

    def get_run_dir_path(self):
        """Returns the path to the log directory for the current run."""
        return self.run_dir_path
