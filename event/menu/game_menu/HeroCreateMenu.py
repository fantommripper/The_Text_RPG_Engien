from controller.LibController import lib_controller
from controller.MenuController import menu_controller

from lib.Logger import logger

from data.Config import config
from data.Player import player

class HeroCreateMenu():
    def __init__(self):
        self.consolas = lib_controller.consolas

        # --- Widgets ---
        self.tips_entry_name_Table = None
        self.entry_name_TextBox = None
        self.chosen_class_Menu = None
        self.chosen_race_Menu = None
        self.chosen_enter_Menu = None
        self.output_Table = None

        # --- Player Variables ---
        self.player_name = "None"
        self.player_class = "None"
        self.player_race = "None"

    def _stop_menu(self):
        self.tab_control = False
        self.entry_name_TextBox.stop()
        self.chosen_class_Menu.stop()
        self.chosen_race_Menu.stop()
        self.chosen_enter_Menu.stop()

    def _update_output_table(self):
        self.output_Table = self.consolas.create_table(
            f"Name: {self.player_name} | Class: {self.player_class} | race: {self.player_race}",
            width=60,
            Ydo="-",
            y=10,
            textAlignment={0: "c"},
            clear=False,
            animation=False
        )

    def _choose_class(self, class_name):
        player.set_class(class_name)
        self.player_class = class_name
        self._update_output_table()

    def _choose_race(self, race_name):
        player.set_race(race_name)
        self.player_race = race_name
        self._update_output_table()

    def _choose_name(self, name):
        player.set_name(name)
        self.player_name = name
        self._update_output_table()

    def _enter_hero(self):
        pass

    def _back_to_main_menu(self):
        self._stop_menu()
        menu_controller.show_main_menu()

    def run(self):
        self.output_Table = self.consolas.create_table(
            f"Name: {self.player_name} | Class: {self.player_class} | race: {self.player_race}",
            width=60,
            Ydo="-",
            y=10,
            textAlignment={0: "c"}
        )

        self.tips_entry_name_Table = self.consolas.create_table(
            "Entry Name",
            width=15,
            Ydo="-",
            Xdo="-",
            y=5,
            x=25,
            textAlignment={0: "c"},
            clear=False
        )

        self.entry_name_TextBox = self.consolas.create_text_box(
            width=17,
            Ydo="-",
            Xdo="-",
            y=2,
            x=25,
            max_symbol=10,
            function=self._choose_name,
            clear=False
        )

        self.chosen_class_Menu = self.consolas.create_menu(
            title="Choose Class",
            options={
                "swordsman": lambda: self._choose_class("swordsman"),
                "magician": lambda: self._choose_class("magician"),
                "thief": lambda: self._choose_class("thief"),
                "archer": lambda: self._choose_class("archer"),
            },
            Ydo="-",
            Xdo="+",
            y=2,
            x=10,
            additional_info=["1", "2", "3", "4"],
            clear=False
        )

        self.chosen_race_Menu = self.consolas.create_menu(
            title="Choose Race",
            options={
                "Human": lambda: self._choose_race("Human"),
                "Kobold": lambda: self._choose_race("Kobold"),
                "Owlin": lambda: self._choose_race("Owlin"),
                "Naga": lambda: self._choose_race("Naga"),
            },
            Ydo="+",
            Xdo="+",
            y=7,
            x=10,
            additional_info=["1", "2", "3", "4"],
            clear=False
        )
        self.chosen_enter_Menu = self.consolas.create_menu(
            title="Enter",
            options={
                "enter": self._enter_hero,
                "back": self._back_to_main_menu,
            },
            Ydo="+",
            Xdo="-",
            y=5,
            x=24,
            table_width=17,
            clear=False,
            tips=False
        )

hero_create_menu = HeroCreateMenu()
