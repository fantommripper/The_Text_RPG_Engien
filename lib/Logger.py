import datetime
import logging
import os
import inspect

class Logger:
    def __init__(self, log_folder: str):
        self.log_folder = log_folder
        self.logger = None
        self.root_dir = os.path.abspath(os.getcwd())
        self.setup_logger()

    def setup_logger(self):
        if not os.path.exists(self.log_folder):
            os.makedirs(self.log_folder)

        current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        log_filename = f"LOG__{current_time}__.log"
        log_path = os.path.join(self.log_folder, log_filename)

        self.logger = logging.getLogger("GameLogger")
        self.logger.setLevel(logging.DEBUG)

        file_handler = logging.FileHandler(log_path, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)

        self.logger.addHandler(file_handler)

    def _get_caller_info(self):
        frame = inspect.currentframe()
        caller_frame = frame.f_back.f_back
        module = inspect.getmodule(caller_frame)

        if module and module.__file__:
            abs_path = os.path.abspath(module.__file__)
            rel_path = os.path.relpath(abs_path, self.root_dir)
            return rel_path.replace(os.sep, ".")
        return "Unknown File"

    def debug(self, message):
        caller_info = self._get_caller_info()
        self.logger.debug(f"{caller_info} : {message}")

    def info(self, message):
        caller_info = self._get_caller_info()
        self.logger.info(f"{caller_info} : {message}")

    def warning(self, message):
        caller_info = self._get_caller_info()
        self.logger.warning(f"{caller_info} : {message}")

    def error(self, message, exc_info=True):
        caller_info = self._get_caller_info()
        self.logger.error(f"{caller_info} : {message}", exc_info=exc_info)

    def critical(self, message):
        caller_info = self._get_caller_info()
        self.logger.critical(f"{caller_info} : {message}")


logger = Logger(log_folder='LOG')
