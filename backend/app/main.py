from fastapi import FastAPI, APIRouter, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
from app.services.image_processing import validate_image, preprocess_image
from app.api.routes import router
from app.api.schemas import DiseaseResponse, SeedResponse
from app.services.gemini_client import analyze_crop_disease, analyze_seed_quality
from app.services.voice_service import text_to_voice    
import os

load_dotenv()

app = FastAPI(
    title="SmartFarm AI Backend 👨‍🌾",
    description="AI-powered crop disease detection with voice support",
    version="1.0.0"
)

# CORS (safe default)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Routes
app.include_router(router, prefix="/api")

# Serve generated audio files
app.mount("/audio", StaticFiles(directory="app/audio"), name="audio")

@app.get("/")  
def root():
    return {"message": "SmartFarm AI Backend is running 🚀"}

@app.get("/health")
def health_check():
    return {"status": "OK"}

# @app.post("/predict")
# async def predict_disease(file: UploadFile = File(...)):
#     if not file.content_type.startswith("image/"):
#         raise HTTPException(status_code=400, detail="Please upload an image file")

#     image_bytes = await file.read()

#     try:
#         image = validate_image(image_bytes)
#         processed_image = preprocess_image(image)
#     except ValueError as e:
#         raise HTTPException(status_code=400, detail=str(e))

#     return {
#         "filename": file.filename,
#         "message": "Image validated and processed successfully ✅",
#         "processed_size_bytes": len(processed_image)
#     }
