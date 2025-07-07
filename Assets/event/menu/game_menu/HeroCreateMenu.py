from controller.LibController import LibController
from controller.MenuController import MenuController

from lib.Logger import logger
from lib.Localization import loc

from data.Player import Player

class HeroCreateMenu():
    def __init__(self):
        self.consolas = LibController.get_instance().consolas
        self.player = Player.get_instance()

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

        self.displayed_class = "None"
        self.displayed_race = "None"

    def _stop_menu(self):
        self.tab_control = False
        self.entry_name_TextBox.stop()
        self.chosen_class_Menu.stop()
        self.chosen_race_Menu.stop()
        self.chosen_enter_Menu.stop()

    def _update_output_table(self):
        if self.player_class != "None": self.displayed_class = loc.t(self.player_class)
        if self.player_race != "None": self.displayed_race = loc.t(self.player_race.lower())

        self.output_Table = self.consolas.create_table(
            f"{loc.t("name")}: {self.player_name} | {loc.t("class")}: {self.displayed_class} | {loc.t("race")}: {self.displayed_race}",
            width=60,
            Ydo="-",
            y=10,
            textAlignment={0: "c"},
            clear=False,
            animation=False
        )

    def _choose_class(self, class_name):
        self.player_class = class_name
        self._update_output_table()

    def _choose_race(self, race_name):
        self.player_race = race_name
        self._update_output_table()

    def _choose_name(self, name):
        self.player.set_name(name)
        self.player_name = name
        self._update_output_table()

    def _enter_hero(self):
        if self.player_name == "None" or self.player_race == "None" or self.player_class == "None": return

        self.player.set_class(self.player_class)
        self.player.set_race(self.player_race)

    def _back_to_main_menu(self):
        self._stop_menu()
        MenuController.get_instance().show_main_menu()

    def run(self):
        if self.player_class != "None": self.displayed_class = loc.t(self.player_class)
        if self.player_race != "None": self.displayed_race = loc.t(self.player_race.lower())

        self.output_Table = self.consolas.create_table(
            f"{loc.t("name")}: {self.player_name} | {loc.t("class")}: {self.displayed_class} | {loc.t("race")}: {self.displayed_race}",
            width=60,
            Ydo="-",
            y=10,
            textAlignment={0: "c"}
        )

        self.tips_entry_name_Table = self.consolas.create_table(
            loc.t("entry_name"),
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
            title=loc.t("entry_class"),
            options={
                loc.t("swordsman"): lambda: self._choose_class("swordsman"),
                loc.t("magician"): lambda: self._choose_class("magician"),
                loc.t("thief"): lambda: self._choose_class("thief"),
                loc.t("archer"): lambda: self._choose_class("archer"),
            },
            Ydo="-",
            Xdo="+",
            y=2,
            x=10,
            additional_info=["1", "2", "3", "4"],
            clear=False
        )

        self.chosen_race_Menu = self.consolas.create_menu(
            title=loc.t("entry_race"),
            options={
                loc.t("human"): lambda: self._choose_race("human"),
                loc.t("kobold"): lambda: self._choose_race("kobold"),
                loc.t("owlin"): lambda: self._choose_race("owlin"),
                loc.t("naga"): lambda: self._choose_race("naga"),
            },
            Ydo="+",
            Xdo="+",
            y=7,
            x=10,
            additional_info=["1", "2", "3", "4"],
            clear=False
        )
        self.chosen_enter_Menu = self.consolas.create_menu(
            title=loc.t("enter"),
            options={
                loc.t("enter"): self._enter_hero,
                loc.t("back"): self._back_to_main_menu,
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
