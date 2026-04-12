from fastapi import FastAPI,Request
from routers import music
from fastapi.templating import Jinja2Templates

app=FastAPI()

templates = Jinja2Templates(directory="templates")

app.include_router(music.router,prefix='/music')


@app.get('/')
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})