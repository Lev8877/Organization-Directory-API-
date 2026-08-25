from pydantic import BaseModel

class ActivityInfo(BaseModel):
    id: int
    name: str
    parent_id: int | None