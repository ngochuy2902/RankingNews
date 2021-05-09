from fastapi import APIRouter, BackgroundTasks
from starlette.responses import JSONResponse

from models.crawler import Crawler
from services.rank import RankService

rank_app = APIRouter(prefix="/rank", tags=["Rank"])
rank_service = RankService()


@rank_app.post('/')
async def start_ranking(crawler: Crawler):
    background_tasks = BackgroundTasks()
    background_tasks.add_task(rank_service.rank_by_session, crawler)
    response = JSONResponse(status_code=200, content="Ranking is run", background=background_tasks)
    return response
