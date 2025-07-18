from lib.Logger import logger

class InputController:
    """
    Class for managing input and handling keyboard events
    """
    def __init__(self):
        self._events = []

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
        """
        Class representing an input event
        """
        def __init__(self, controller):
            self.controller = controller

            self.id = self.controller._generate_id()
            self.key = None
            self.function = None
            self.pause = False

        def set_pause(self, pause):
            self.pause = pause

        def remove(self):
            self.controller.remove_input_event(self.id)
            del self

    def add_input_event(self, key, function, pause=False) -> InputEvent:
        """
        Add an input event
    
        Args:
            key: Key or key code
            function: Event handling function
            pause: Pause event processing
    
        Returns:
            InputEvent: Created input event
        """
        event = self.InputEvent(self)
        if isinstance(key, str) and len(key) == 1:
            event.key = ord(key)
        else:
            event.key = key
        event.function = function
        event.pause = pause
        self._events.append(event)
        return event

    def remove_input_event(self, id):
        """
        Remove an input event by its identifier
    
        Args:
            id: Event identifier
        """
        self._events = [event for event in self._events if event.id != id]

    def set_input_event_pause(self, id, bool):
        """
        Set input event pause
    
        Args:
            id: Event identifier
            bool: True to pause, False to resume
        """
        for event in self._events:
            if event.id == id:
                event.pause = bool
                return