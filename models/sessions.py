from datetime import datetime

from pydantic import BaseModel, Field


class Session(BaseModel):
    id: int = Field(..., alias='id')
    created_time: datetime = Field(..., alias='created_time')
