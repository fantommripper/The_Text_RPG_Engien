import curses
import curses.ascii
from typing import List, TYPE_CHECKING

from controller.LibController import LibController
from controller.AudioController import AudioController

if TYPE_CHECKING:
    from lib.widgets.BaseActiveWidget import BaseActiveWidget

class TabControl:
    """
    Class for managing tabs and focus on interface elements
    Implements the singleton pattern to ensure only one instance exists
    """
    _instance = None

    @classmethod
    def get_instance(cls):
        """
        Get the singleton instance of TabControl
    
        Returns:
            TabControl: The existing instance of TabControl
        """
        if cls._instance is None:
            cls._instance = TabControl()
        return cls._instance

    def __init__(self):
        """
        Initialize the TabControl instance
    
        Raises:
            Exception: If an attempt is made to create a second instance
        """
        if TabControl._instance is not None:
            raise Exception("TabControl is already created! Use TabControl.get_instance()")

        self._widgets: List['BaseActiveWidget'] = []
        self._current_focus = 0

        self._input_controller = LibController.get_instance().input_controller

        self.start_tab_control()

    def start_tab_control(self):
        """
        Start the tab control system
    
        Enables mouse support and initializes tab navigation
        """

        curses.mousemask(1)

        if self._widgets:  # Проверяем, есть ли виджеты
            for i in self._widgets:
                if not i.paused:
                    i.set_pause(True)

            self._widgets[self._current_focus].set_pause(False)

        self._tab_input_event = self._input_controller.add_input_event(curses.ascii.TAB, self._next_widget)
        self._btab_input_event = self._input_controller.add_input_event(curses.KEY_BTAB, self._preceding_widget)

    def set_widgets(self, widgets: List['BaseActiveWidget']):
        """
        Set the list of managed widgets
    
        Args:
            widgets: List of widgets to manage focus for
        """
        self._tab_input_event.set_pause(True)
        self._btab_input_event.set_pause(True)

        self._widgets = widgets
        self._update_tab_control()

        self._tab_input_event.set_pause(False)
        self._btab_input_event.set_pause(False)

    def add_widget(self, widget: 'BaseActiveWidget'):
        """
        Add a widget to the list of managed widgets
    
        Args:
            widget: Widget to add to the management list
        """
        self._tab_input_event.set_pause(True)
        self._btab_input_event.set_pause(True)

        self._widgets.append(widget)

        self._update_tab_control()

        self._tab_input_event.set_pause(False)
        self._btab_input_event.set_pause(False)

    def remove_widget(self, widget: 'BaseActiveWidget'):
        """
        Remove a widget from the list of managed widgets
    
        Args:
            widget: Widget to remove from the management list
    
        Raises:
            ValueError: If the widget is not found
        """
        self._tab_input_event.set_pause(True)
        self._btab_input_event.set_pause(True)

        if widget in self._widgets:
            self._widgets.remove(widget)
        else:
            raise ValueError("Widget not found in TabControl")

        self._update_tab_control()

        self._tab_input_event.set_pause(False)
        self._btab_input_event.set_pause(False)

    def stop_tab_control(self):
        """
        Stop the tab control system
    
        Disables mouse support and cleans up input handlers
        """
        self._input_controller.remove_input_event(self.tab_input_event)
        self._input_controller.remove_input_event(self.btab_input_event)

        curses.mousemask(0)

    def _update_tab_control(self):
        """
        Update the tab control state

        Ensures only the focused widget is active
        """
        if not self._widgets:  # Если нет виджетов, ничего не делаем
            return

        self._current_focus = 0

        for i in self._widgets:
            if not i.paused:
                i.set_pause(True)

        self._widgets[self._current_focus].set_pause(False)

    def _next_widget(self):
        """
        Switch to the next widget

        Handles focus and audio feedback
        """
        if not self._widgets:  # Проверка на пустой список
            return

        self._widgets[self._current_focus].set_pause(True)
        self._current_focus = (self._current_focus + 1) % len(self._widgets)
        AudioController.get_instance().play_random_print_sound()
        self._widgets[self._current_focus].set_pause(False)

    def _preceding_widget(self):
        """
        Switch to the previous widget

        Handles focus and audio feedback
        """
        if not self._widgets:  # Проверка на пустой список
            return

        self._widgets[self._current_focus].set_pause(True)
        self._current_focus = (self._current_focus - 1) % len(self._widgets)
        AudioController.get_instance().play_random_print_sound()
        self._widgets[self._current_focus].set_pause(False)