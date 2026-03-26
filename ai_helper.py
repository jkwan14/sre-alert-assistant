import os
import json
from openai import OpenAI
from dotenv import load_dotenv

# AI usage note:
# I used ChatGPT to help me fine tune my prompt and to help me debug portions of this file.
# All code was reviewed, edited, and understood by me.

load_dotenv()

def ai_helper(alert):
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        return None

    client = OpenAI(api_key=api_key)

    reply = client.chat.completions.create(
        model = "gpt-4o-mini",
        messages = [
            {"role": "user", "content": f"Based on the provided alert, in plain English, provide a short and clear beginner-friendly explanation, severity, possible_causes, and next_steps so that a junior SRE with no experience may be able to understand. Avoid jargon. Return your responses as JSON with keys: explanation, severity(Low, Medium, High, Critical), possible_causes, next_steps. Return ONLY valid JSON. Do not include any extra text. Alert: '{alert}'."}
        ],
        max_tokens=400,
    )
    text = reply.choices[0].message.content.strip()
    text = text.replace("```json", "").replace("```", "").strip()

    try:
        data = json.loads(text)
        return data
    except Exception:
        return None



