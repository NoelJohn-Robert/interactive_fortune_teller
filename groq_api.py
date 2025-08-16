import os
import random
import requests
from dotenv import load_dotenv
from groq import Groq


# Load environment variables from .env
load_dotenv()

# Read API key from environment
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "").strip()
MODEL_NAME = "meta-llama/llama-4-scout-17b-16e-instruct"  # Replace with the actual available vision model

# Automatically switch to mock mode if no API key is found
MOCK_MODE = not bool(GROQ_API_KEY)


def get_fortune_from_groq(image_b64):
    """Takes a base64 JPEG image and returns a humorous fortune."""
    if MOCK_MODE or not GROQ_API_KEY:
        fortunes = [
            "You will soon meet someone who changes your perspective on pizza.",
            "A great surprise awaits you... possibly involving coffee.",
            "Beware of sock thieves this week.",
            "Your WiFi will mysteriously get faster tomorrow.",
            "Someone will compliment your choice of browser tabs."
        ]
        return random.choice(fortunes)

    try:
        client = Groq(api_key=GROQ_API_KEY)

        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a witty yet gentle fortune teller who examines photographs "
                        "and delivers short, humorous, and sarcastic fortunes. "
                        "Base your fortune on visual cues such as facial expression, apparent age, clothing, "
                        "and background, but keep it playful and never insulting. "
                        "If there is more than one person, address the group as a whole and make your fortune relevant to the shared vibe or situation. "
                        "Use subtle humor and light sarcasm that feels personal but kind. "
                        "Have utmost four short sentences."
                    )
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
            model=MODEL_NAME,
            max_tokens=80
        )

        return chat_completion.choices[0].message.content

    except Exception as e:
        return f"Error getting fortune: {e}"
