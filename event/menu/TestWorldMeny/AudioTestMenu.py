from controller.AudioController import audio_controller
from controller.LibController import lib_controller as lc

from data.GameFlags import game_flags

class AudioTestMenu():
    def __init__(self):
        pass

    def run(self):
        while True:
            self.action = lc.table_menu.menu(
                title="Audio Test",
                options=["exit", "Battle Music.wav", "BGmusic.wav", "Forest Music.wav", "Shop Music.wav"],
                y=20,
                tips=False,
            )

            if self.action == "0":
                game_flags.meny["test_audio"] = False
                break
            elif self.action == "1":
                audio_controller.play_battle_music()

            elif self.action == "2":
                audio_controller.play_background_music()

            elif self.action == "3":
                audio_controller.play_forest_music()

            elif self.action == "4":
                audio_controller.play_shop_music()

audio_test_menu = AudioTestMenu()