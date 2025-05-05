import pygame
import os
import random as r

class AudioController:
    def __init__(self):
        self.volume = 0.5
        pygame.mixer.init()

    def load_sound(self, filename):

        return pygame.mixer.Sound(os.path.join("data", "sound", filename))

    def play_sound(self, sound):
        sound.play()

    def stop_music(self):
        pygame.mixer.music.stop()

    def play_sound_print(self):
        self.print_sound = self.load_sound("print.wav")
        self.print_sound.set_volume(0.1)
        self.play_sound(self.print_sound)

    def play_sound_print2(self):
        self.print2_sound = self.load_sound("print2.wav")
        self.print2_sound.set_volume(0.1)
        self.play_sound(self.print2_sound)

    def play_random_sound_print(self):
        self.sound = r.choice(["print.wav", "print2.wav"])
        self.sound = self.load_sound(self.sound)
        self.sound.set_volume(0.1)
        self.play_sound(self.sound)

    def play_background_music(self):
        self.stop_music()

        bg_music_path = os.path.join("data", "sound", "BGmusic.wav")
        pygame.mixer.music.load(bg_music_path)
        pygame.mixer.music.play(-1)

    def play_battle_music(self):
        self.stop_music()

        battle_music_path = os.path.join("data", "sound", "Battle Music.wav")
        pygame.mixer.music.load(battle_music_path)
        pygame.mixer.music.play(-1)

    def play_shop_music(self):
        self.stop_music()

        shop_music_path = os.path.join("data", "sound", "Shop Music.wav")
        pygame.mixer.music.load(shop_music_path)
        pygame.mixer.music.play(-1)

    def play_forest_music(self):
        self.stop_music()

        forest_music_path = os.path.join("data", "sound", "Forest Music.wav")
        pygame.mixer.music.load(forest_music_path)
        pygame.mixer.music.play(-1)

    def play_the_void(self):
        self.stop_music()

        the_void_music_path = os.path.join("data", "sound", "The Void.wav")
        pygame.mixer.music.load(the_void_music_path)
        pygame.mixer.music.play(-1)

audio_controller = AudioController()
