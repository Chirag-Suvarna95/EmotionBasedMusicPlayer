from deepface import DeepFace
import cv2
import numpy as np
from collections import deque

class EmotionDetector:
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
        # Add emotion history for smoothing
        self.emotion_history = deque(maxlen=5)
        # Configure analysis parameters
        self.analysis_config = {
            'actions': ['emotion'],
            'enforce_detection': False,
            'detector_backend': 'opencv'
        }
        
    def detect_emotion(self, frame):
        try:
            # Analyze face with multiple models
            result = DeepFace.analyze(
                frame,
                **self.analysis_config
            )
            
            emotion = result[0]['dominant_emotion']
            
            # Smooth emotion detection
            self.emotion_history.append(emotion)
            smoothed_emotion = max(set(self.emotion_history), 
                                 key=list(self.emotion_history).count)
            
            # Draw face rectangle and emotion
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
            
            if len(faces) > 0:
                (x, y, w, h) = faces[0]
                # Draw blue rectangle around face
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
                
                # Add emotion label with background
                label_size = cv2.getTextSize(smoothed_emotion, 
                                           cv2.FONT_HERSHEY_SIMPLEX, 
                                           0.9, 2)[0]
                cv2.rectangle(frame, 
                            (x, y-30), 
                            (x + label_size[0], y), 
                            (255, 0, 0), 
                            cv2.FILLED)
                cv2.putText(frame, 
                           smoothed_emotion, 
                           (x, y-10),
                           cv2.FONT_HERSHEY_SIMPLEX, 
                           0.9,
                           (255, 255, 255), 
                           2)
                
                # Add confidence score if available
                if 'emotion' in result[0]:
                    confidence = result[0]['emotion'][smoothed_emotion]
                    conf_text = f"Confidence: {confidence:.1f}%"
                    cv2.putText(frame, 
                               conf_text,
                               (x, y+h+25),
                               cv2.FONT_HERSHEY_SIMPLEX,
                               0.7,
                               (0, 255, 0),
                               2)
            
            return smoothed_emotion
            
        except Exception as e:
            print(f"Error in emotion detection: {e}")
            return "neutral"
            
    def release(self):
        # Cleanup method
        self.emotion_history.clear()
