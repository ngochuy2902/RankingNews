from pydantic import BaseModel, Field


class Audio(BaseModel):
    uuid: str
    result: str
