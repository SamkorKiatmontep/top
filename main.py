from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from contextlib import asynccontextmanager
from database import setup_database
from routers import music

@asynccontextmanager
async def lifespan(app: FastAPI):
    await setup_database()
    print(" База данных готова")
    yield

    print("Приложение остановлено")

app = FastAPI(lifespan=lifespan)

templates = Jinja2Templates(directory="templates")

app.include_router(music.router, prefix='/music')

@app.get('/')
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})