from pydantic import BaseModel

class MusicCreate(BaseModel):
    title:str
    artist:str

class MusicResponse(BaseModel):
    id:int
    title:str
    artist:str
