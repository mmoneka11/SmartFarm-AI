# # Gemini Client Service

import os
import json
import re
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MODEL = os.getenv("GEMINI_MODEL", "gemini-3-flash-preview")

# ---------- Helpers ----------

def _extract_json(text: str) -> dict:
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        raise ValueError("Gemini response not in JSON format")
    return json.loads(match.group())


def _image_part(image_bytes: bytes):
    return types.Part.from_bytes(
        data=image_bytes,
        mime_type="image/jpeg"
    )


# ---------- Crop Disease Analysis ----------

def analyze_crop_disease(
    image_bytes: bytes,
    country: str = "Global",
    lang: str = "en"
) -> dict:
    """
    Crop disease detection using Gemini Vision
    """

    prompt = f"""
You are an agricultural crop disease expert.

Country context: {country}

Analyze the uploaded crop leaf image and return ONLY valid JSON:

{{
  "crop_name": "",
  "disease_name": "",
  "confidence": 0.0,
  "description": "",
  "recommended_pesticide": "",
  "message": ""   // short farmer-friendly advice in language: {lang}
}}

Rules:
- Focus ONLY on crops (plants, leaves, farm produce)
- Do NOT mention animals or livestock
- Keep recommendations safe and generally applicable
- Confidence must be between 0 and 1
"""

    response = client.models.generate_content(
        model=MODEL,
        contents=[prompt, _image_part(image_bytes)]
    )

    return _extract_json(response.text or "")


# ---------- Seed Quality Analysis ----------

def analyze_seed_quality(
    image_bytes: bytes,
    seed_type: str = "Unknown",
    lang: str = "en"
) -> dict:
    """
    Seed quality inspection using Gemini Vision
    """

    prompt = f"""
You are an agricultural seed quality expert.

Analyze the seed image and return ONLY valid JSON:

{{
  "seed_type": "{seed_type}",
  "quality": "High | Medium | Low",
  "confidence": 0.0,
  "observations": "",
  "sowing_recommendation": "",
  "message": ""   // farmer advice in language: {lang}
}}

Rules:
- Focus ONLY on seeds (shape, color, damage, mold)
- Confidence between 0 and 1
- Recommendations should be practical for farmers
"""

    response = client.models.generate_content(
        model=MODEL,
        contents=[prompt, _image_part(image_bytes)]
    )

    return _extract_json(response.text or "")
