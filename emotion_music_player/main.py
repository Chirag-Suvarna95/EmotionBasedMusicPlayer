import cv2
from src.emotion_detector import EmotionDetector
from src.music_player import MusicPlayer
from src.gui_manager import GUI

def main():
    print("Initializing camera...")
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    
    if not cap.isOpened():
        print("Error: Could not open camera")
        return
        
    print("Camera opened successfully")
    
    emotion_detector = EmotionDetector()
    music_player = MusicPlayer("music")
    gui = GUI(emotion_detector, music_player)

    def update():
        ret, frame = cap.read()
        if ret:
            emotion = emotion_detector.detect_emotion(frame)
            music_player.play_music(emotion)
            gui.update_frame(frame, emotion)
        gui.root.after(100, update)

    update()
    gui.root.mainloop()

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
