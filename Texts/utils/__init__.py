from pydantic import BaseModel

class Paratranz(BaseModel):
    key: str
    original: str
    translation: str|None = None
    context: str|None = None
