from fastapi import APIRouter, BackgroundTasks
from starlette.responses import JSONResponse

from models.ranker import Ranker
from services.rank import RankService

rank_app = APIRouter(prefix="/ranker", tags=["Rank"])
rank_service = RankService()


@rank_app.post('')
async def run_ranking(ranker: Ranker):
    background_tasks = BackgroundTasks()
    background_tasks.add_task(rank_service.rank_by_session, ranker)
    response = JSONResponse(status_code=200, content="Ranking is running", background=background_tasks)
    return response
