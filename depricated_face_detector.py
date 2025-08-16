import ctypes
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)  # Windows 8.1+
except Exception:
    try:
        ctypes.windll.user32.SetProcessDPIAware()  # Windows Vista – 8.0
    except Exception:
        pass


import cv2
import mediapipe as mp
import tkinter as tk
from PIL import Image, ImageTk
import time
import os

# Folder to save frames
SAVE_DIR = "saved_frames"
os.makedirs(SAVE_DIR, exist_ok=True)  # Create folder if it doesn't exist

# MediaPipe setup
mp_face_detection = mp.solutions.face_detection
face_detection = mp_face_detection.FaceDetection(min_detection_confidence=0.7)

# OpenCV Video Capture
cap = cv2.VideoCapture(0)

# Force higher resolution
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)


# Global variables for saving
raw_frame = None  # Without overlays
current_frame = None  # With overlays

# Save frame function
def save_frame():
    global raw_frame
    if raw_frame is not None:
        filename = os.path.join(SAVE_DIR, f"fortune_frame_{int(time.time())}.png")
        cv2.imwrite(filename, cv2.cvtColor(raw_frame, cv2.COLOR_RGB2BGR))
        print(f"Frame saved as {filename}")

# Update video feed
def update_frame():
    global raw_frame, current_frame
    ret, frame = cap.read()
    if not ret:
        root.after(10, update_frame)
        return
    
    # Convert to RGB for MediaPipe & PIL
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    raw_frame = rgb_frame.copy()  # Keep clean version for saving
    display_frame = rgb_frame.copy()

    results = face_detection.process(rgb_frame)

    if results.detections:
        for detection in results.detections:
            bboxC = detection.location_data.relative_bounding_box
            ih, iw, _ = display_frame.shape
            x = int(bboxC.xmin * iw)
            y = int(bboxC.ymin * ih)
            w = int(bboxC.width * iw)
            h = int(bboxC.height * ih)

            cv2.rectangle(display_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(display_frame, "Face Detected!", (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    current_frame = display_frame

    # Convert to PIL image for Tkinter
    img = Image.fromarray(current_frame)
    imgtk = ImageTk.PhotoImage(image=img)
    video_label.imgtk = imgtk
    video_label.configure(image=imgtk)

    root.after(10, update_frame)  # Schedule next frame update

# Tkinter window setup
root = tk.Tk()
root.title("Fortune Teller Camera")

video_label = tk.Label(root)
video_label.pack()

save_button = tk.Button(root, text="Save Frame", command=save_frame, bg="blue", fg="white", font=("Arial", 14))
save_button.pack(pady=10)

update_frame()
root.protocol("WM_DELETE_WINDOW", lambda: (cap.release(), root.destroy()))
root.mainloop()
