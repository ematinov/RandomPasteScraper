from pydantic import BaseModel


class Text(BaseModel):
    text: str

class TextWithId(BaseModel):
    id: int
    text: str
