import json
import os
from cryptography.fernet import Fernet

from data.Config import Config,config

from lib.Logger import logger

class SaveManager:
    def __init__(self):
        self.save_dir = self.save_dir = os.path.join(os.getenv("LOCALAPPDATA"), ".TheTextRPG")
        self.key_file = os.path.join(self.save_dir, "encryption_key.key")
        self.fernet = self._load_or_create_key()

    def _load_or_create_key(self):
        os.makedirs(self.save_dir, exist_ok=True)

        if not os.path.exists(self.key_file):
            key = Fernet.generate_key()
            with open(self.key_file, "wb") as key_file:
                key_file.write(key)
        else:
            with open(self.key_file, "rb") as key_file:
                key = key_file.read()
        return Fernet(key)

    def save_data(self, data, save_name):
        os.makedirs(self.save_dir, exist_ok=True)

        json_file = os.path.join(self.save_dir, f"{save_name}.json")
        encrypted_file = os.path.join(self.save_dir, f"{save_name}.enc")

        if hasattr(data, 'to_dict'):
            data_dict = data.to_dict()
        else:
            data_dict = data

        with open(json_file, 'w') as f:
            json.dump(data_dict, f)

        encrypted_data = self.fernet.encrypt(json.dumps(data_dict).encode())
        with open(encrypted_file, 'wb') as f:
            f.write(encrypted_data)

    def load_data(self, save_name, data_class=None):
        json_file = os.path.join(self.save_dir, f"{save_name}.json")
        encrypted_file = os.path.join(self.save_dir, f"{save_name}.enc")

        if not os.path.exists(json_file) or not os.path.exists(encrypted_file):
            logger.info(f"Save files for {save_name} not found.")
            return None

        with open(json_file, 'r') as f:
            json_data = json.load(f)

        with open(encrypted_file, 'rb') as f:
            encrypted_data = f.read()

        decrypted_data = json.loads(self.fernet.decrypt(encrypted_data))

        if json_data != decrypted_data:
            logger.warning(f"Save data mismatch detected for {save_name}. Possible tampering.")
            data_to_use = decrypted_data
        else:
            data_to_use = json_data

        if hasattr(data_class, 'from_dict'):
            logger.info(f"Loading save data for {save_name}")
            data_class.from_dict(data_to_use)
        else:
            logger.error(f"{data_class.__name__} does not have a from_dict method.")

    def list_saves(self):
        saves = []
        for file in os.listdir(self.save_dir):
            if file.endswith(".json"):
                saves.append(file[:-5])
        return saves

    def delete_save(self, save_name):
        json_file = os.path.join(self.save_dir, f"{save_name}.json")
        encrypted_file = os.path.join(self.save_dir, f"{save_name}.enc")

        if os.path.exists(json_file):
            os.remove(json_file)
        if os.path.exists(encrypted_file):
            os.remove(encrypted_file)

    def load_all_game_data(self):
        config_save = self.load_data("config", config)

        if config_save is None:
            self.save_data(config.to_dict(), "config")

    def save_all_game_data(self):
        self.save_data(config.to_dict(), "config")


save_manager = SaveManager()