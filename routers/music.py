from fastapi import APIRouter, HTTPException
from models import MusicCreate, MusicResponse
from database import new_session, MusicModel, setup_database
from sqlalchemy import select
import asyncio

# Создаём таблицу при запуске
asyncio.run(setup_database())

router = APIRouter()

@router.get('/', response_model=list[MusicResponse])
async def get_all():
    async with new_session() as session:
        result = await session.execute(select(MusicModel))
        songs = result.scalars().all()
        return [{'id': s.id, 'title': s.title, 'artist': s.artist} for s in songs]

@router.get('/search')
async def search_songs(q: str):
    async with new_session() as session:
        result = await session.execute(
            select(MusicModel).where(
                MusicModel.title.contains(q) | MusicModel.artist.contains(q)
            )
        )
        songs = result.scalars().all()
        return [{'id': s.id, 'title': s.title, 'artist': s.artist} for s in songs]

@router.post('/', status_code=201, response_model=MusicResponse)
async def add_song(song: MusicCreate):
    async with new_session() as session:
        new_song = MusicModel(title=song.title, artist=song.artist)
        session.add(new_song)
        await session.commit()
        return {'id': new_song.id, 'title': new_song.title, 'artist': new_song.artist}

@router.delete('/{song_id}', status_code=204)
async def delete_song(song_id: int):
    async with new_session() as session:
        song = await session.get(MusicModel, song_id)
        if not song:
            raise HTTPException(404, 'не найден')
        await session.delete(song)
        await session.commit()

@router.put('/{song_id}', response_model=MusicResponse)
async def song_put(song_id: int, song_model: MusicCreate):
    async with new_session() as session:
        song = await session.get(MusicModel, song_id)
        if not song:
            raise HTTPException(404, 'не найден')
        song.title = song_model.title
        song.artist = song_model.artist
        await session.commit()
        return {'id': song.id, 'title': song.title, 'artist': song.artist}

@router.get('/{song_id}', response_model=MusicResponse)
async def get_one(song_id: int):
    async with new_session() as session:
        song = await session.get(MusicModel, song_id)
        if not song:
            raise HTTPException(404, 'не найден')
        return {'id': song.id, 'title': song.title, 'artist': song.artist}