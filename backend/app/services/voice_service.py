# Google Text-to-Speech (gTTS)

from gtts import gTTS
import uuid
import os

AUDIO_DIR = "app/audio"
os.makedirs(AUDIO_DIR, exist_ok=True)

def text_to_voice(text: str, lang: str = "ur") -> str:
    filename = f"{uuid.uuid4()}.mp3"
    filepath = os.path.join(AUDIO_DIR, filename)

    tts = gTTS(text=text, lang=lang)
    tts.save(filepath)

    return filepath

# from google.cloud import texttospeech

# def text_to_voice(text: str, filename="output.mp3"):
#     client = texttospeech.TextToSpeechClient()

#     input_text = texttospeech.SynthesisInput(text=text)

#     voice = texttospeech.VoiceSelectionParams(
#         language_code="ur-PK",
#         ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
#     )

#     audio_config = texttospeech.AudioConfig(
#         audio_encoding=texttospeech.AudioEncoding.MP3
#     )

#     response = client.synthesize_speech(
#         input=input_text,
#         voice=voice,
#         audio_config=audio_config
#     )

#     with open(filename, "wb") as f:
#         f.write(response.audio_content)

#     return filename
