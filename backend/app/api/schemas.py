# Request & Response Schemas → Data structures used in API endpoints

from pydantic import BaseModel

class DiseaseResponse(BaseModel):
    crop_name: str
    disease_name: str
    confidence: float
    description: str
    recommended_pesticide: str
    message: str
    audio_url: str

class SeedResponse(BaseModel):
    seed_type: str
    quality: str
    confidence: float
    observations: str
    sowing_recommendation: str
    message: str
    audio_url: str
