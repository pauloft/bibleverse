from typing import List
from fastapi import FastAPI, Request, Depends

from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models import Books, Verses, VersesReadWithBook
from app.database import init_db, get_session

# Initialize the FastAPI Application
app = FastAPI()
# define the templates and static files directories
templates = Jinja2Templates(directory='./app/templates')
app.mount('/static', StaticFiles(directory='./app/static'), name='static')


@app.on_event("startup")
async def on_startup():
    """ Startup event handler to ensure database is ready """
    await init_db()


@app.get("/", response_class=HTMLResponse)
async def show_search_form(request: Request, session: AsyncSession = Depends(get_session)):
    """ Display the search form """
    context = {'request': request}
    return templates.TemplateResponse("index.html",context)