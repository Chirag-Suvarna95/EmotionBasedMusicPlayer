import pygame
import os
import random
from pathlib import Path

class MusicPlayer:
    def __init__(self, music_dir):
        pygame.mixer.init()
        self.music_dir = Path(music_dir)
        self.current_track = None
        self.current_emotion = None
        self.volume = 0.5
        self._load_tracks()

    def _load_tracks(self):
        self.tracks = {}
        for emotion_dir in self.music_dir.iterdir():
            if emotion_dir.is_dir():
                self.tracks[emotion_dir.name] = [
                    f for f in emotion_dir.glob("*.mp3")
                ]

    def play_music(self, emotion):
        if emotion in self.tracks and self.tracks[emotion]:
            if emotion != self.current_emotion or not pygame.mixer.music.get_busy():
                track = random.choice(self.tracks[emotion])
                try:
                    pygame.mixer.music.load(str(track))
                    pygame.mixer.music.play()
                    pygame.mixer.music.set_volume(self.volume)
                    self.current_track = track
                    self.current_emotion = emotion
                except Exception as e:
                    print(f"Error playing track: {e}")

    def set_volume(self, volume):
        self.volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.volume)

    def stop_music(self):
        pygame.mixer.music.stop()
        self.current_track = None
        self.current_emotion = None
