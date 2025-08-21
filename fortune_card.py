# import os
# from datetime import datetime
# from PIL import Image, ImageDraw, ImageFont

# SAVE_DIR = "saved_fortunes"
# os.makedirs(SAVE_DIR, exist_ok=True)

# def save_fortune_card(raw_frame, fortune_text):
#     """Create and save a fortune card with camera image (left) and text (right)."""
#     img = Image.fromarray(raw_frame).convert("RGB")

#     img_width, img_height = img.size

#     # Font setup
#     try:
#         font = ImageFont.truetype("arial.ttf", 24)
#     except:
#         font = ImageFont.load_default()

#     # Wrap text
#     max_chars = 40
#     words = fortune_text.split()
#     lines, line = [], ""
#     for word in words:
#         if len(line + word) <= max_chars:
#             line += word + " "
#         else:
#             lines.append(line.strip())
#             line = word + " "
#     lines.append(line.strip())

#     line_height = font.getbbox("A")[3] + 10
#     text_height = len(lines) * line_height + 20

#     # Create fortune card canvas
#     card_width = img_width + 500
#     card_height = max(img_height, text_height)
#     card = Image.new("RGB", (card_width, card_height), "white")
#     card.paste(img, (0, 0))

#     # Draw text
#     draw = ImageDraw.Draw(card)
#     x_offset, y_offset = img_width + 20, 20
#     for line in lines:
#         draw.text((x_offset, y_offset), line, fill="black", font=font)
#         y_offset += line_height

#     # Save fortune card
#     timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
#     path = os.path.join(SAVE_DIR, f"{timestamp}_fortune_card.png")
#     card.save(path)

#     print(f"✅ Saved fortune card: {path}")
#     return path





# fortune_card.py
import os
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import numpy as np

SAVE_DIR = "saved_fortunes"
os.makedirs(SAVE_DIR, exist_ok=True)

def save_fortune_card(input_img, fortune_text, user_code: str = None):
    """Create and save a fortune card with camera image (left) and text (right)."""
    print('savign fortune')

    # Ensure input is a PIL image
    if isinstance(input_img, np.ndarray):
        img = Image.fromarray(input_img).convert("RGB")
    elif isinstance(input_img, Image.Image):
        img = input_img.convert("RGB")
    else:
        raise ValueError("Input must be a NumPy array or PIL.Image")

    img_width, img_height = img.size

    # Font setup
    try:
        font = ImageFont.truetype("arial.ttf", 24)
    except:
        font = ImageFont.load_default()

    # Wrap text
    max_chars = 40
    words = fortune_text.split()
    lines, line = [], ""
    for word in words:
        if len(line + word) <= max_chars:
            line += word + " "
        else:
            lines.append(line.strip())
            line = word + " "
    lines.append(line.strip())

    line_height = font.getbbox("A")[3] + 10
    text_height = len(lines) * line_height + 20

    # Create fortune card canvas
    card_width = img_width + 500
    card_height = max(img_height, text_height)
    card = Image.new("RGB", (card_width, card_height), "white")
    card.paste(img, (0, 0))

    # Draw text
    draw = ImageDraw.Draw(card)
    x_offset, y_offset = img_width + 20, 20
    for line in lines:
        draw.text((x_offset, y_offset), line, fill="black", font=font)
        y_offset += line_height

    # Save fortune card
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    if user_code:
        filename = f"{user_code}_{timestamp}_fortune_card.png"
    else:
        filename = f"{timestamp}_fortune_card.png"
    path = os.path.join(SAVE_DIR, filename)
    card.save(path)

    print(f"✅ Saved fortune card: {path}")
    return path
