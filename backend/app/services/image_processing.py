# Image handling - Validation & Preprocessing

from PIL import Image
import io

MAX_IMAGE_SIZE_MB = 5
ALLOWED_FORMATS = ["JPEG", "PNG", "JPG"]

def validate_image(image_bytes: bytes):
    size_mb = len(image_bytes) / (1024 * 1024)
    if size_mb > MAX_IMAGE_SIZE_MB:
        raise ValueError("Image size exceeds 5MB limit")

    try:
        image = Image.open(io.BytesIO(image_bytes))
        if image.format not in ALLOWED_FORMATS:
            raise ValueError("Unsupported image format")
    except Exception:
        raise ValueError("Invalid or corrupted image file")

    return image


def preprocess_image(image: Image.Image):
    """
    Resize & normalize image for AI model
    """
    image = image.convert("RGB")   # Convert to RGB (important for consistency)
    image.thumbnail((1024, 1024))  # Resize safely

    buffer = io.BytesIO()  # Save back to bytes
    image.save(buffer, format="JPEG")
    buffer.seek(0)

    return buffer.getvalue()
