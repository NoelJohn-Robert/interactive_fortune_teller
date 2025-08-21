# import os
# import random
# import requests
# from dotenv import load_dotenv
# from groq import Groq


# # Load environment variables from .env
# load_dotenv()

# last_model_used = None 

# # Read API key from environment
# GROQ_API_KEY = os.getenv("GROQ_API_KEY", "").strip()
# MODEL_NAME_1 = "meta-llama/llama-4-scout-17b-16e-instruct"  # Replace with the actual available vision model
# MODEL_NAME_2 = "meta-llama/llama-4-maverick-17b-128e-instruct"

# # Automatically switch to mock mode if no API key is found
# MOCK_MODE = not bool(GROQ_API_KEY)


# def get_fortune_from_groq(image_b64):
#     global last_model_used
#     """Takes a base64 JPEG image and returns a humorous fortune."""
#     if MOCK_MODE or not GROQ_API_KEY:
#         fortunes = [
#             "You will soon meet someone who changes your perspective on pizza.",
#             "A great surprise awaits you... possibly involving coffee.",
#             "Beware of sock thieves this week.",
#             "Your WiFi will mysteriously get faster tomorrow.",
#             "Someone will compliment your choice of browser tabs."
#         ]
#         return random.choice(fortunes)

#     try:
#         client = Groq(api_key=GROQ_API_KEY)

#         # chat_completion = client.chat.completions.create(
#         #     messages=[
#         #         {
#         #             "role": "system",
#         #             "content": (
#         #                 "You are a witty yet gentle fortune teller who examines photographs "
#         #                 "and delivers short, humorous, and sarcastic fortunes. "
#         #                 "Base your fortune on visual cues such as facial expression, apparent age, clothing, "
#         #                 "and background, but keep it playful and never insulting. "
#         #                 "If there is more than one person, address the group as a whole and make your fortune relevant to the shared vibe or situation. "
#         #                 "Use subtle humor and light sarcasm that feels personal but kind. "
#         #                 "Have utmost four short sentences."
#         #             )
#         #         },
#         #         {
#         #             "role": "user",
#         #             "content": [
#         #                 {"type": "text", "text": "Look at this face or group and tell a witty, lighthearted fortune."},
#         #                 {
#         #                     "type": "image_url",
#         #                     "image_url": {
#         #                         "url": f"data:image/jpeg;base64,{image_b64}",
#         #                     },
#         #                 },
#         #             ],
#         #         }
#         #     ],
#         #     model=MODEL_NAME,
#         #     temperature=0.7,
#         #     max_tokens=80
#         # )
#         if last_model_used == MODEL_NAME_1:
#             model_to_use = MODEL_NAME_2
#         else:
#             model_to_use = MODEL_NAME_1
#         last_model_used = model_to_use

#         chat_completion = client.chat.completions.create(
#     messages=[
#         {
#             "role": "system",
#             "content": """You are a professional, witty fortune-teller persona whose job is to read photographs and produce short, realistic, and playful fortunes grounded only in what is visibly present in the image. Follow these rules exactly:
 
# A. OBSERVATION ORDER (must anchor on visible, concrete details - but never revolve the whole fortune on that one anchor):
#    1. Try to mention at least ONE **distinctive visual detail** (facial expression, hand gesture, posture, prop, clothing detail, background object, or lighting effect). The fortune must feel impossible to reuse on a different photo.
#    2. Use secondary cues (color palette, textures, accessories, positioning in frame) to make each response unique.
#    3. Avoid vague or generic descriptors like "sharp mind," "clever spirit," or "bright future" unless clearly tied to a visible detail.
#    4. When analyzing the image, ignore background, but focus only on the human(s) and their features.
#    5. Should make the reader(s) feel like they can relate to the fortune that is said.
 
# B. TONE & ETHICS:
#    1. Respectful, witty, and concise - but still suitable for a corporate~ish environment. Humor should be warm, dry, or lightly sarcastic — but never too mean-spirited.
#    2. Never infer protected attributes (race, religion, nationality, orientation), medical/financial predictions, or private facts. Try not to speculate about relationships or personal lives [but can make light-hearted predictions].
 
# C. FORTUNE STRUCTURE:
#    1. Anchor fortune in **specific observed cues** (e.g., “That crooked tie,” “The raised eyebrow,” “The coffee mug by your hand,” “The neon glow behind you”). But always try using cues that that don't stand out much and are subtle enough to be missed.
#    2. Blend observation with a witty, imaginative outcome or prediction, but keep it lighthearted - never crossing ethical or personal boundaries.
#    3. Vary style — sometimes playful, sometimes poetic, sometimes teasing, and only sometimes romantic/flirtatious — but still suitable in a professional environment.
 
# D. OUTPUT FORMAT:
#    1. Output ONLY the fortune (no meta text, no lists).
#    2. Max **four short sentences** (6–14 words each).
#    3. Must include a clearly unique reference to THIS photo’s visual cues, as we mentioned cues before.
#    4. Must provide detailed Fortune in funny and professional.
#    5. Never make joke on personailties.
#    6. Never recycle stock phrases or overly abstract lines.
 
# E. FAILURE MODE:
#    1. If no clear cues are visible, return: “The image hides its secrets well — a small mystery awaits.”
 
# Strictly follow A–E. Each output must feel specific, unique, and visibly grounded — no generic fortunes."""
#         },
#         {
#             "role": "user",
#             "content": [
#                 {"type": "text", "text": "Look at this face or group and tell a witty, lighthearted fortune."},
#                 {
#                     "type": "image_url",
#                     "image_url": {
#                         "url": f"data:image/jpeg;base64,{image_b64}",
#                     },
#                 },
#             ],
#         }
#     ],
#     model=model_to_use,
#     temperature=1,
#     # max_tokens=80
# )
 

#         return chat_completion.choices[0].message.content

#     except Exception as e:
#         return f"Error getting fortune: {e}"




import os
import random
from dotenv import load_dotenv
from groq import Groq

# Load environment variables from .env
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "").strip()
MODEL_NAME_1 = "meta-llama/llama-4-scout-17b-16e-instruct"
MODEL_NAME_2 = "meta-llama/llama-4-maverick-17b-128e-instruct"

MOCK_MODE = not bool(GROQ_API_KEY)

MOCK_FORTUNES = [
    "You will soon meet someone who changes your perspective on pizza.",
    "A great surprise awaits you... possibly involving coffee.",
    "Beware of sock thieves this week.",
    "Your WiFi will mysteriously get faster tomorrow.",
    "Someone will compliment your choice of browser tabs."
]


def get_fortune_from_groq(image_b64: str) -> str:
    if MOCK_MODE:
        return random.choice(MOCK_FORTUNES)

    try:
        client = Groq(api_key=GROQ_API_KEY)
        model_to_use = random.choice([MODEL_NAME_1, MODEL_NAME_2])

        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": """You are a witty but respectful fortune-teller who examines photographs
                    and delivers short, playful fortunes. Base each fortune on *visible cues* (facial
                    expressions, gestures, clothing, props, or subtle background hints). Never guess
                    private facts, and keep it light, witty, and professional. Max 4 short sentences."""
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Look at this face or group and tell a witty, lighthearted fortune."},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_b64}",
                            },
                        },
                    ],
                }
            ],
            model=model_to_use,
            temperature=0.9,
            max_tokens=80
        )

        return chat_completion.choices[0].message.content.strip()

    except Exception as e:
        return f"[API error: {e}]"
