from abc import ABC

class Effects(ABC):
    def __init__(self, name: str, duration: int, description: str):
        self.name = name
        self.duration = duration
        self.description = description

    # TODO: Хз как это работает, но надо сделать так, чтобы эффект применялся к игроку и роботали вместе с циклом ходов но его ещо нет поэтому не делаю