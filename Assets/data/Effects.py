from abc import ABC

class Effects(ABC):
    _instance = None

    def __init__(self, name: str, duration: int, description: str):
        self.name = name
        self.duration = duration
        self.description = description

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls(name, duration, description)
        return cls._instance

    # TODO: Хз как это работает, но надо сделать так, чтобы эффект применялся к игроку и роботали вместе с циклом ходов но его ещо нет поэтому не делаю