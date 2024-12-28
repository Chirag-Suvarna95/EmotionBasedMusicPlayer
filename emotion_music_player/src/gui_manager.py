import tkinter as tk
from tkinter import ttk
import cv2
from PIL import Image, ImageTk

class GUI:
    def __init__(self, emotion_detector, music_player):
        self.root = tk.Tk()
        self.root.title("Emotion-Based Music Player")
        self.emotion_detector = emotion_detector
        self.music_player = music_player
        self.setup_gui()

    def setup_gui(self):
        # Video frame
        self.video_frame = ttk.Frame(self.root)
        self.video_frame.grid(row=0, column=0, padx=10, pady=10)
        
        self.video_label = ttk.Label(self.video_frame)
        self.video_label.grid(row=0, column=0)

        # Controls frame
        controls = ttk.Frame(self.root)
        controls.grid(row=1, column=0, padx=10, pady=5)

        ttk.Button(controls, text="Stop", command=self.music_player.stop_music).grid(
            row=0, column=0, padx=5
        )

        # Volume control
        self.volume_var = tk.DoubleVar(value=0.5)
        ttk.Scale(controls, from_=0, to=1, variable=self.volume_var,
                 command=self.update_volume).grid(row=0, column=1, padx=5)

        # Status frame
        status = ttk.Frame(self.root)
        status.grid(row=2, column=0, padx=10, pady=5)
        
        self.emotion_label = ttk.Label(status, text="Emotion: --")
        self.emotion_label.grid(row=0, column=0)

    def update_volume(self, value):
        self.music_player.set_volume(float(value))

    def update_frame(self, frame, emotion):
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)
        photo = ImageTk.PhotoImage(image=image)
        self.video_label.configure(image=photo)
        self.video_label.image = photo
        self.emotion_label.configure(text=f"Emotion: {emotion}")
