import ctypes
import tkinter as tk
from PIL import Image, ImageTk

from camera import Camera
from utils import save_frame_to_disk, encode_image_to_base64
from groq_api import get_fortune_from_groq

# Fix DPI scaling for Windows
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    try:
        ctypes.windll.user32.SetProcessDPIAware()
    except Exception:
        pass

camera = Camera()

# Track face detection
face_detected = False

def update_frame():
    global face_detected
    raw_frame, display_frame = camera.get_frame()
    
    if display_frame is not None:
        img = Image.fromarray(display_frame)
        imgtk = ImageTk.PhotoImage(image=img)
        video_label.imgtk = imgtk
        video_label.configure(image=imgtk)

        # If a face was detected, enable button
        if camera.face_detection.process(camera.raw_frame).detections:
            face_detected = True
            save_button.config(state=tk.NORMAL, bg="blue")
        else:
            face_detected = False
            save_button.config(state=tk.DISABLED, bg="gray")

    root.after(10, update_frame)

def save_and_get_fortune():
    if not face_detected:
        return
    
    raw_frame = camera.raw_frame
    if raw_frame is not None:
        # # Save (optional)
        # save_frame_to_disk(raw_frame)

        # Encode for Groq
        pil_img = Image.fromarray(raw_frame)
        img_b64 = encode_image_to_base64(pil_img)

        # Get fortune
        fortune = get_fortune_from_groq(img_b64)

        # Show in the fortune text area
        fortune_display.config(state=tk.NORMAL)
        fortune_display.delete(1.0, tk.END)
        fortune_display.insert(tk.END, fortune)
        fortune_display.config(state=tk.DISABLED)

# Tkinter setup
root = tk.Tk()
root.title("Fortune Teller Camera")

# Main layout: two columns
left_frame = tk.Frame(root)
left_frame.pack(side=tk.LEFT, padx=10, pady=10)

right_frame = tk.Frame(root)
right_frame.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.BOTH, expand=True)

# Camera feed
video_label = tk.Label(left_frame)
video_label.pack()

# Button (disabled by default)
save_button = tk.Button(left_frame, text="Tell My Fortune", command=save_and_get_fortune,
                        bg="gray", fg="white", font=("Arial", 14), state=tk.DISABLED)
save_button.pack(pady=10)

# Fortune display area
fortune_label = tk.Label(right_frame, text="Your Fortune:", font=("Arial", 16, "bold"))
fortune_label.pack(anchor="w")

fortune_display = tk.Text(right_frame, wrap=tk.WORD, height=15, width=40,
                          font=("Arial", 14), state=tk.DISABLED, bg="#f9f9f9")
fortune_display.pack(fill=tk.BOTH, expand=True)

update_frame()
root.protocol("WM_DELETE_WINDOW", lambda: (camera.release(), root.destroy()))
root.mainloop()





# import requests
# import os
# from dotenv import load_dotenv


# load_dotenv()

# api_key = os.getenv("GROQ_API_KEY")
# url = "https://api.groq.com/openai/v1/models"

# headers = {
#     "Authorization": f"Bearer {api_key}",
#     "Content-Type": "application/json"
# }

# response = requests.get(url, headers=headers)

# print(response.json())
