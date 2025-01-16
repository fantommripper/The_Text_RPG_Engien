import datetime
import logging
import os
import traceback

class Logger:
    def __init__(self, log_folder: str):
        self.log_folder = log_folder
        self.logger = None
        self.setup_logger()

    def setup_logger(self):
        if not os.path.exists(self.log_folder):
            os.makedirs(self.log_folder)

        current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        log_filename = f"LOG__{current_time}__.log"
        log_path = os.path.join(self.log_folder, log_filename)

        self.logger = logging.getLogger("GameLogger")
        self.logger.setLevel(logging.DEBUG)

        file_handler = logging.FileHandler(log_path)
        file_handler.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)

        self.logger.addHandler(file_handler)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message, exc_info=True):  # Добавлен параметр exc_info
        self.logger.error(message, exc_info=exc_info)

    def critical(self, message):
        self.logger.critical(message)



logger = Logger(log_folder='LOG')