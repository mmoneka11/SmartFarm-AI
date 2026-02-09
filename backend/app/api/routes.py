# → API logic - Image Upload Route
 
from fastapi import APIRouter, UploadFile, File, Query, HTTPException
from app.api.schemas import DiseaseResponse, SeedResponse
from app.services.image_processing import validate_image, preprocess_image
from app.services.gemini_client import (
    analyze_crop_disease,
    analyze_seed_quality
)
from app.services.voice_service import text_to_voice

router = APIRouter()

@router.post("/analyze-disease", response_model=DiseaseResponse)

async def analyze_disease(
    image: UploadFile = File(...),
    country: str = Query("Global"),
    lang: str = Query("en")
):
    image_bytes = await image.read()
    image_obj = validate_image(image_bytes)
    processed = preprocess_image(image_obj)

    result = analyze_crop_disease(processed, country, lang)
    result["audio_url"] = text_to_voice(result["message"], lang=lang)

    return result


@router.post("/analyze-seed", response_model=SeedResponse)
async def analyze_seed(
    image: UploadFile = File(...),
    seed_type: str = Query("Unknown"),
    lang: str = Query("en")
):
    """
    Receives a seed image and returns seed quality analysis
    Image → Validation → Preprocessing → Gemini → JSON → API Response
    """
    image_bytes = await image.read()
    image_obj = validate_image(image_bytes)
    processed = preprocess_image(image_obj)

    result = analyze_seed_quality(processed, seed_type, lang)
    result["audio_url"] = text_to_voice(result["message"], lang)

    return result
