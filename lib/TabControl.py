import curses
import curses.ascii
from typing import List, TYPE_CHECKING

from Assets.controller.LibController import lib_controller
from Assets.controller.AudioController import audio_controller

if TYPE_CHECKING:
    from lib.widgets.BaseActiveWidget import BaseActiveWidget

class TabControl:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = TabControl()
        return cls._instance

    def __init__(self):
        if TabControl._instance is not None:
            raise Exception("TabControl уже создан! Используйте TabControl.get_instance()")
        
        self._widgets: List['BaseActiveWidget'] = []
        self._current_focus = 0

        self._input_controller = lib_controller.input_controller

        self.start_tab_control()

    def start_tab_control(self):
        curses.mousemask(1)

        if self._widgets:  # Проверяем, есть ли виджеты
            for i in self._widgets:
                if not i.paused:
                    i.set_pause(True)

            self._widgets[self._current_focus].set_pause(False)

        self._tab_input_event = self._input_controller.add_input_event(curses.ascii.TAB, self._next_widget)
        self._btab_input_event = self._input_controller.add_input_event(curses.KEY_BTAB, self._preceding_widget)

    def set_widgets(self, widgets: List['BaseActiveWidget']):
        self._tab_input_event.set_pause(True)
        self._btab_input_event.set_pause(True)

        self._widgets = widgets
        self._update_tab_control()

        self._tab_input_event.set_pause(False)
        self._btab_input_event.set_pause(False)

    def add_widget(self, widget: 'BaseActiveWidget'):
        self._tab_input_event.set_pause(True)
        self._btab_input_event.set_pause(True)

        self._widgets.append(widget)

        self._update_tab_control()

        self._tab_input_event.set_pause(False)
        self._btab_input_event.set_pause(False)

    def remove_widget(self, widget: 'BaseActiveWidget'):
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
        self._input_controller.remove_input_event(self.tab_input_event)
        self._input_controller.remove_input_event(self.btab_input_event)

        curses.mousemask(0)

    def _update_tab_control(self):
        if not self._widgets:  # Если нет виджетов, ничего не делаем
            return

        self._current_focus = 0

        for i in self._widgets:
            if not i.paused:
                i.set_pause(True)

        self._widgets[self._current_focus].set_pause(False)

    def _next_widget(self):
        if not self._widgets:  # Проверка на пустой список
            return

        self._widgets[self._current_focus].set_pause(True)
        self._current_focus = (self._current_focus + 1) % len(self._widgets)
        audio_controller.play_random_print_sound()
        self._widgets[self._current_focus].set_pause(False)

    def _preceding_widget(self):
        if not self._widgets:  # Проверка на пустой список
            return

        self._widgets[self._current_focus].set_pause(True)
        self._current_focus = (self._current_focus - 1) % len(self._widgets)
        audio_controller.play_random_print_sound()
        self._widgets[self._current_focus].set_pause(False)