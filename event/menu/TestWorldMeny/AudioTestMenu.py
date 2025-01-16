from controller.AudioController import audio_controller
from controller.LibController import lib_controller

from data.GameFlags import game_flags

from lib.Logger import logger

class AudioTestMenu():
    def __init__(self):
        pass

    def run(self):
        while True:
            lib_controller.table_menu.menu(
                title="Audio Test",
                options=["exit", "Battle Music.wav", "BGmusic.wav", "Forest Music.wav", "Shop Music.wav"],
                y=20,
                tips=False,
            )
            self.action = lib_controller.table_menu.get_menu_result()

            if self.action:
                logger.debug(f"Selected option: {self.action}")
                if self.action == "0":
                    logger.debug("Exiting audio test menu")
                    break
                elif self.action == "1":
                    logger.debug("Playing Battle Music")
                    audio_controller.play_battle_music()

                elif self.action == "2":
                    logger.debug("Playing BGmusic")
                    audio_controller.play_background_music()

                elif self.action == "3":
                    logger.debug("Playing Forest Music")
                    audio_controller.play_forest_music()

                elif self.action == "4":
                    logger.debug("Playing Shop Music")
                    audio_controller.play_shop_music()

audio_test_menu = AudioTestMenu()