from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column
engin=create_async_engine('sqlite+aiosqlite:///music.db')

new_session=async_sessionmaker(engin,expire_on_commit=False)

async def get_session():
    with new_session() as session:
        yield session

class Base(DeclarativeBase):
    pass

class MusicModel(Base):
    __tablename__='music'

    id:Mapped[int] = mapped_column(primary_key=True)
    title:Mapped[str]
    artist:Mapped[str]
    file_path:Mapped[str] = mapped_column(default='')


async def setup_database():
    async with engin.begin() as con:
        await con.run_sync(Base.metadata.create_all)



# music = [
#     {'id': 1, 'title': 'Bohemian Rhapsody', 'artist': 'Queen'},
#     {'id': 2, 'title': 'Shape of You', 'artist': 'Ed Sheeran'},
#     {'id': 3, 'title': 'Smells Like Teen Spirit', 'artist': 'Nirvana'},
#     {'id': 4, 'title': 'Blinding Lights', 'artist': 'The Weeknd'},
# ]