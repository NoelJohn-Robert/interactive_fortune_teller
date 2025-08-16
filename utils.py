import os
import time
import base64
from io import BytesIO
from PIL import Image
import cv2

SAVE_DIR = "saved_frames"
os.makedirs(SAVE_DIR, exist_ok=True)

def save_frame_to_disk(frame):
    filename = os.path.join(SAVE_DIR, f"fortune_frame_{int(time.time())}.png")
    cv2.imwrite(filename, cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
    return filename

def encode_image_to_base64(pil_img):
    buf = BytesIO()
    pil_img.save(buf, format="JPEG")
    return base64.b64encode(buf.getvalue()).decode("utf-8")
