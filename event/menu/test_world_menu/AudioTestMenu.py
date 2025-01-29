from controller.AudioController import audio_controller
from controller.LibController import lib_controller

from lib.Logger import logger
from lib.ConsoleSettings import console_settings

class AudioTestMenu():
    def __init__(self):
        pass

    def run(self):
        main_menu_widget = lib_controller.consolas.create_menu(
                        title="Audio Test",
                        options=["exit", "Battle Music.wav", "BGmusic.wav", "Forest Music.wav", "Shop Music.wav"],
                        tips=False,
                    )
        self.action = main_menu_widget.get_menu_result()

        while True:
            if self.action:
                logger.info(f"Selected option: {self.action}")
                if self.action == "0":
                    logger.info("Exiting audio test menu")
                    console_settings.exit_terminal()

                elif self.action == "1":
                    logger.info("Playing Battle Music")
                    audio_controller.play_battle_music()

                elif self.action == "2":
                    logger.info("Playing BGmusic")
                    audio_controller.play_background_music()

                elif self.action == "3":
                    logger.info("Playing Forest Music")
                    audio_controller.play_forest_music()

                elif self.action == "4":
                    logger.info("Playing Shop Music")
                    audio_controller.play_shop_music()

audio_test_menu = AudioTestMenu()