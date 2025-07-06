class GameFlags:
    _instance = None

    def __init__(self):
        self.open_terminal = False

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance