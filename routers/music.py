from fastapi import APIRouter,HTTPException
from models import MusicCreate,MusicResponse
from database import music

router=APIRouter()

@router.get('/',response_model=list[MusicResponse])
def get_all():
    return music


@router.get('/search')
def search_songs(q: str):
    result = []
    for i in music:
        if q.lower() in i['title'].lower() or q.lower() in i['artist'].lower():
            result.append(i)
    
    if not result:
        return {"message": f"{q} не найден", "results": []}
    
    return result



@router.post('/', status_code=201,response_model=MusicResponse)
def add_song(song:MusicCreate):
    new_song = {
        'id': len(music) + 1,
        'title': song.title,
        'artist': song.artist
    }
    music.append(new_song)
    return new_song

@router.delete('/{song_id}', status_code=204)
def delete_song(song_id: int):
    for index, song in enumerate(music):
        if song['id'] == song_id:
           detal=music.pop(index)
           print(f'вот удаленный обьект {detal}')
           return
    raise HTTPException(404, 'не найден')

@router.put('/{song_id}',response_model=MusicResponse)
def song_put(song_id:int,song_model:MusicCreate):
    for i in music:
        if i['id']==song_id:
            i['title']=song_model.title
            i['artist']=song_model.artist
            return i
    raise HTTPException(404,'не найден')

@router.get('/{song_id}',response_model=MusicResponse)
def get_one(song_id:int):
    for song in music:
        if song['id'] == song_id:
            return song
    raise HTTPException(404, 'не найден')