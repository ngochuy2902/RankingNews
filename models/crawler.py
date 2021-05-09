from datetime import datetime
from pydantic import BaseModel


class Crawler(BaseModel):
    created_time: datetime
