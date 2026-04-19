from contextlib import asynccontextmanager  
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from database import setup_database
from routers import music

@asynccontextmanager
async def lifespan(app: FastAPI):
    await setup_database()
    print("✅ База данных готова")
    yield

app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

app.include_router(music.router, prefix='/music')

@app.get('/')
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})