from fastapi import APIRouter, status

from models.audio import Audio
from services.score import ScoreService

audio_app = APIRouter(prefix="/audio", tags=["Audio"])
score_service = ScoreService()


@audio_app.post('', status_code=status.HTTP_200_OK)
async def run_ranking(audio: Audio):
    score_service.check_audio(audio)
