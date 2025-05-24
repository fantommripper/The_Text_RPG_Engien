import pygame
import os
import random
from lib.Logger import logger

class AudioController:
    def __init__(self):
        self.volume = 0.5
        self.sounds = {}
        self.music_volume = 0.5
        try:
            pygame.mixer.init()
            self._load_resources()
            logger.info("AudioController initialized successfully.")
        except Exception as e:
            logger.error(f"AudioController initialization error: {e}", exc_info=True)

    def _get_sound_path(self, filename):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(base_dir, "..", "data", "sound", filename)

    def _load_resources(self):
        sound_files = ['print.wav', 'print2.wav']
        for sound_file in sound_files:
            try:
                self.sounds[sound_file] = self._load_sound(sound_file)
            except Exception as e:
                logger.error(f"Error loading sound {sound_file}: {e}", exc_info=True)

        for sound in self.sounds.values():
            try:
                sound.set_volume(0.1)
            except Exception as e:
                logger.error(f"Error setting volume for sound: {e}", exc_info=True)

        self.music_tracks = {
            'background': 'BGmusic.wav',
            'battle': 'Battle Music.wav',
            'shop': 'Shop Music.wav',
            'forest': 'Forest Music.wav',
            'void': 'The Void.wav'
        }

    def _load_sound(self, filename):
        path = self._get_sound_path(filename)
        if not os.path.isfile(path):
            raise FileNotFoundError(f"Sound file not found: {path}")
        return pygame.mixer.Sound(path)

    def play_sound(self, sound_name):
        try:
            if sound_name in self.sounds:
                self.sounds[sound_name].play()
            else:
                logger.warning(f"Sound {sound_name} not found in self.sounds")
        except Exception as e:
            logger.error(f"Error playing sound {sound_name}: {e}", exc_info=True)

    def play_random_print_sound(self):
        sound_name = random.choice(['print.wav', 'print2.wav'])
        self.play_sound(sound_name)

    def play_music(self, track_name, loops=-1):
        try:
            if track_name not in self.music_tracks:
                logger.warning(f"Track {track_name} not found in music_tracks")
                return

            pygame.mixer.music.stop()
            path = self._get_sound_path(self.music_tracks[track_name])
            if not os.path.isfile(path):
                logger.error(f"Music file not found: {path}")
                return
            pygame.mixer.music.load(path)
            pygame.mixer.music.set_volume(self.music_volume)
            pygame.mixer.music.play(loops)
        except Exception as e:
            logger.error(f"Error playing music {track_name}: {e}", exc_info=True)

    def stop_music(self):
        try:
            pygame.mixer.music.stop()
        except Exception as e:
            logger.error(f"Error stopping music: {e}", exc_info=True)

    def set_volume(self, volume):
        self.volume = max(0.0, min(1.0, volume))
        for sound in self.sounds.values():
            try:
                sound.set_volume(self.volume)
            except Exception as e:
                logger.error(f"Error setting volume for sound: {e}", exc_info=True)

    def set_music_volume(self, volume):
        self.music_volume = max(0.0, min(1.0, volume))
        try:
            pygame.mixer.music.set_volume(self.music_volume)
        except Exception as e:
            logger.error(f"Error setting music volume: {e}", exc_info=True)

audio_controller = AudioController()