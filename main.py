# import ctypes
# import tkinter as tk
# from PIL import Image, ImageTk

# from camera import Camera
# from utils import save_frame_to_disk, encode_image_to_base64
# from groq_api import get_fortune_from_groq
# from fortune_card import save_fortune_card


# # Fix DPI scaling for Windows
# try:
#     ctypes.windll.shcore.SetProcessDpiAwareness(1)
# except Exception:
#     try:
#         ctypes.windll.user32.SetProcessDPIAware()
#     except Exception:
#         pass

# camera = Camera()
# face_detected = False # Track face detection

# def update_frame():
#     global face_detected
#     raw_frame, display_frame = camera.get_frame()
    
#     if display_frame is not None:
#         img = Image.fromarray(display_frame)
#         imgtk = ImageTk.PhotoImage(image=img)
#         video_label.imgtk = imgtk
#         video_label.configure(image=imgtk)

#         # If a face was detected, enable button
#         if camera.face_detection.process(camera.raw_frame).detections:
#             face_detected = True
#             fortune_button.config(state=tk.NORMAL, bg="blue")
#         else:
#             face_detected = False
#             fortune_button.config(state=tk.DISABLED, bg="gray")

#     root.after(10, update_frame)


# last_raw_frame = None
# last_fortune_text = ""

# def save_and_get_fortune():
#     global last_raw_frame, last_fortune_text

#     if not face_detected:
#         return

#     # 🔹 Reset Save button as soon as user asks for a new fortune
#     save_card_button.config(text="💾 Save Fortune Card", bg="purple")

#     raw_frame = camera.raw_frame
#     if raw_frame is not None:
#         pil_img = Image.fromarray(raw_frame)
#         img_b64 = encode_image_to_base64(pil_img)

#         fortune = get_fortune_from_groq(img_b64)

#         # Keep track of what was actually sent
#         last_raw_frame = raw_frame.copy()
#         last_fortune_text = fortune

#         # Show in the fortune text area
#         fortune_display.config(state=tk.NORMAL)
#         fortune_display.delete(1.0, tk.END)
#         fortune_display.insert(tk.END, fortune)
#         fortune_display.config(state=tk.DISABLED)


# def save_card_locally():
#     global last_raw_frame, last_fortune_text
#     if last_raw_frame is not None and last_fortune_text:
#         save_fortune_card(last_raw_frame, last_fortune_text)
#         save_card_button.config(text="✅ Saved!", bg="green")


# # Tkinter setup
# root = tk.Tk()
# root.title("Fortune Teller Camera")

# left_frame = tk.Frame(root)
# left_frame.pack(side=tk.LEFT, padx=10, pady=10)

# right_frame = tk.Frame(root)
# right_frame.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.BOTH, expand=True)

# # Camera feed
# video_label = tk.Label(left_frame)
# video_label.pack()

# fortune_button = tk.Button(left_frame, text="Tell My Fortune", 
#                            command=save_and_get_fortune,
#                            bg="gray", fg="white", font=("Arial", 14), 
#                            state=tk.DISABLED)
# fortune_button.pack(pady=10)

# save_card_button = tk.Button(left_frame, text="💾 Save Fortune Card", 
#                              command=save_card_locally,
#                              bg="purple", fg="white", font=("Arial", 14))
# save_card_button.pack(pady=5)

# fortune_label = tk.Label(right_frame, text="Your Fortune:", font=("Arial", 16, "bold"))
# fortune_label.pack(anchor="w")

# fortune_display = tk.Text(right_frame, wrap=tk.WORD, height=15, width=40,
#                           font=("Arial", 14), state=tk.DISABLED, bg="#f9f9f9")
# fortune_display.pack(fill=tk.BOTH, expand=True)

# update_frame()
# root.protocol("WM_DELETE_WINDOW", lambda: (camera.release(), root.destroy()))
# root.mainloop()






# # main.py
# import streamlit as st
# from groq_api import get_fortune_from_groq
# from fortune_card import save_fortune_card
# from utils import encode_image_to_base64
# import io
# from PIL import Image

# st.set_page_config(page_title="AI Fortune Teller", page_icon="🔮", layout="centered")

# st.title("🔮 AI Fortune Teller")
# st.markdown("Take a photo, and let the AI tell your fortune!")

# # Camera input widget
# photo = st.camera_input("📸 Take a photo")

# if photo:
#     # Load photo into PIL
#     image = Image.open(photo)

#     # Convert to Base64 for API
#     buf = io.BytesIO()
#     image.save(buf, format="JPEG")
#     image_bytes = buf.getvalue()
#     image_b64 = encode_image_to_base64(Image.open(io.BytesIO(image_bytes)))

#     # Tell fortune
#     if st.button("✨ Tell Fortune"):
#         with st.spinner("Consulting the stars..."):
#             fortune = get_fortune_from_groq(image_b64)
#             st.success(f"**Your Fortune:** {fortune}")

#             # Option to save fortune card
#             if st.button("💾 Save Fortune Card"):
#                 save_fortune_card(image, fortune)
#                 st.info("Your fortune card has been saved!")






# main.py
import streamlit as st
import cv2
import av
import mediapipe as mp
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase
from groq_api import get_fortune_from_groq
from fortune_card import save_fortune_card
from utils import encode_image_to_base64
from PIL import Image

st.set_page_config(page_title="AI Fortune Teller", page_icon="🔮", layout="centered")
st.title("🔮 AI Fortune Teller")
st.warning(
    "⚠️ **Heads up!**\n"
    "The fortune results are AI-generated.\n"
    "Neither **UST** nor the **Data Services** team is responsible.\n"
    "Please avoid taking photos of the generated results."
)
# -----------------------------
# Face Detection Processor
# -----------------------------
mp_face_detection = mp.solutions.face_detection

class FaceDetectionProcessor(VideoProcessorBase):
    def __init__(self):
        self.face_detection = mp_face_detection.FaceDetection(min_detection_confidence=0.7)
        self.last_frame = None

    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")
        self.last_frame = img.copy()

        results = self.face_detection.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        if results.detections:
            for detection in results.detections:
                bboxC = detection.location_data.relative_bounding_box
                ih, iw, _ = img.shape
                x, y, w, h = int(bboxC.xmin * iw), int(bboxC.ymin * ih), int(bboxC.width * iw), int(bboxC.height * ih)
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)
                cv2.putText(img, "Face Detected!", (x, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        return av.VideoFrame.from_ndarray(img, format="bgr24")

# -----------------------------
# Start WebRTC Stream
# -----------------------------
ctx = webrtc_streamer(
    key="face-detection",
    video_processor_factory=FaceDetectionProcessor,
    media_stream_constraints={"video": True, "audio": False},
    async_processing=True,
)

# -----------------------------
# Fortune Teller Actions
# -----------------------------
# Display current fortune if it exists
# if "fortune" in st.session_state:
#     st.success(f"**Your Fortune:** {st.session_state['fortune']}")

# Generate new fortune
if ctx.video_processor:
    if st.button("✨ Tell Fortune"):
        # Clear previous fortune & related states BEFORE anything else
        st.session_state["fortune"] = None
        st.session_state["fortune_img"] = None
        st.session_state["download_path"] = None
        st.session_state["show_save_form"] = False

        frame_bgr = ctx.video_processor.last_frame
        if frame_bgr is not None:
            frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
            pil_img = Image.fromarray(frame_rgb)
            image_b64 = encode_image_to_base64(pil_img)

            with st.spinner("Consulting the stars..."):
                fortune = get_fortune_from_groq(image_b64)

            # Store new fortune in session state
            st.session_state["fortune"] = fortune
            st.session_state["fortune_img"] = pil_img

# Display the fortune ONLY if it exists
if st.session_state.get("fortune") and st.session_state.get("fortune_img"):
    st.success(f"**Your Fortune:** {st.session_state['fortune']}")

# Initialize state for Save form
if "show_save_form" not in st.session_state:
    st.session_state["show_save_form"] = False

if "download_path" not in st.session_state:
    st.session_state["download_path"] = None

# Show Save button if fortune exists
if "fortune" in st.session_state and "fortune_img" in st.session_state:
    if st.button("💾 Save Fortune Card"):
        st.session_state["show_save_form"] = True


# Show form to enter UID
if st.session_state["show_save_form"]:
    if "user_code_input" not in st.session_state:
        st.session_state["user_code_input"] = ""

    with st.form("save_form"):
        user_uid = st.text_input(
            "🔑 Enter your UID (any format):", 
            key="user_code_input"
        )
        confirm = st.form_submit_button("Confirm Save")

        if confirm:
            if user_uid.strip():  # just check it's not empty
                path = save_fortune_card(
                    st.session_state["fortune_img"],
                    st.session_state["fortune"],
                    user_code=user_uid.strip()  # use whatever user entered
                )
                st.session_state["download_path"] = path
                st.session_state["save_message"] = f"✅ Saved with UID `{user_uid.strip()}`\n📂 Location: `{path}`"
                st.session_state["show_save_form"] = False
            else:
                st.warning("⚠️ Please enter your UID before saving.")



# Show download button outside the form
if st.session_state["download_path"]:
    with open(st.session_state["download_path"], "rb") as f:
        st.download_button(
            label="📥 Download Fortune Card",
            data=f,
            file_name=st.session_state["download_path"].split("/")[-1],
            mime="image/png"
        )
