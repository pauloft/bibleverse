from typing import List
from fastapi import FastAPI, Request, Depends, HTTPException, Query

from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

from sqlmodel import Session, select, func, alias

from app.models import Books, Verses, VersesReadWithBook
from app.database import init_db, get_session

# Initialize the FastAPI Application
app = FastAPI()
# define the templates and static files directories
templates = Jinja2Templates(directory='./app/templates')
app.mount('/static', StaticFiles(directory='./app/static'), name='static')


@app.on_event("startup")
def on_startup():
    """ Startup event handler to ensure database is ready """
    init_db()


@app.get("/", response_class=HTMLResponse)
def show_search_form(request: Request, session: Session = Depends(get_session)):
    """ Display the search form """
    context = {'request': request}
    return templates.TemplateResponse("index.html",context)


@app.get("/suggestions", response_model=List[VersesReadWithBook])
def get_suggestions(q: str, session: Session = Depends(get_session)):
    verses = session.exec(
        select(Verses)
        .filter(Verses.text.like(f"%{q}%"))
        .distinct()
        .order_by(Verses.text)
        .limit(10)
    ).all()

    if not verses:
        raise HTTPException(status_code=404, detail='No results found')
    # return [verse.text for verse in verses]
    return verses


@app.get("/books", response_model=List[Books], tags=["Books"])
def get_books(
    skip: int = 0,
    limit: int = Query(default=100, lte=100),
    session: Session = Depends(get_session)
):
    """ get list of books """
    books = session.exec(select(Books).offset(skip).limit(limit)).all()
    if not books:
        raise HTMLResponse(status_code=404, detail='Books not found')
    return books


@app.get("/books/{bkid}/count_verses", tags=["Books"])
def count_verses(bkid: int, session: Session = Depends(get_session)):
    """ Total number of verses in a given book """
    verses = session.exec(select(Verses).where(Verses.book_id == bkid)).all()
    if not verses:
        raise HTMLResponse(status_code=404, detail='The book identifier may be incorrect')
    return len(verses)

@app.get("/versesbychapter/{bkid}", tags=["Verses"])
def count_chapter_verses(bkid: int, session: Session = Depends(get_session)):
    """ Count the number of verses in each chapter for a given book (by book_id) """
    vbc = session.exec(select(Verses.chapter, func.count(Verses.text)).where(Verses.book_id == bkid).group_by(Verses.chapter)).all()
    if not vbc:
        raise HTTPException(status_code=404, detail='No data found')
    return vbc