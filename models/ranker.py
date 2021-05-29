from pydantic import BaseModel


class Ranker(BaseModel):
    session_id: int
    status: str = None
