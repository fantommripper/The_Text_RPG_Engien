from lib.Logger import logger

class InputController:
    def __init__(self, win):
        self._events = []
        self._win = win

    def handle_key(self, c):
        for event in self._events:
            if event.key == c and not event.pause:
                event.function()

    def _generate_id(self):
        used_ids = {event.id for event in self._events}
        candidate = 0
        while candidate in used_ids:
            candidate += 1
        return candidate

    class InputEvent:
        def __init__(self, controller):
            self.id = controller._generate_id()
            self.key = None
            self.function = None
            self.pause = False

    def add_input_event(self, key, function, pause=False):
        event = self.InputEvent(self)
        if isinstance(key, str) and len(key) == 1:
            event.key = ord(key)
        else:
            event.key = key
        event.function = function
        event.pause = pause
        self._events.append(event)
        return event.id

    def remove_input_event(self, id):
        self._events = [event for event in self._events if event.id != id]

    def set_input_event_pause(self, id, bool):
        for event in self._events:
            if event.id == id:
                event.pause = bool
                return