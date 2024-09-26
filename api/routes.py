from fastapi import APIRouter, HTTPException
from api.models import TTSRequest
from services.tts_service import TTSService

router = APIRouter()

@router.post("/generate-audio-and-srt")
async def generate_audio_and_srt_api(request: TTSRequest):
    try:
        tts_service = TTSService()
        result = await tts_service.process_request(request)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))