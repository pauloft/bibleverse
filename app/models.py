from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship


class TestamentBase(SQLModel):
    name: str = Field(index=True, unique=True)


class Testaments(TestamentBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    books: List['Books'] = Relationship(back_populates='testament')


class BooksBase(SQLModel):
    abbrev: str = Field(index=True, unique=True)
    name: str = Field(index=True, unique=True)


class Books(BooksBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    testament_id: Optional[int] = Field(default=None, foreign_key='testaments.id')
    testament: Optional['Testaments'] = Relationship(back_populates='books')
    verses: List['Verses'] = Relationship(back_populates='book')


class VersesBase(SQLModel):
    chapter: int
    number: int
    text: str


class Verses(VersesBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    book_id: Optional[int] = Field(default=None, foreign_key='books.id')
    book: Optional['Books'] = Relationship(back_populates='verses')


class VersesRead(VersesBase):
    id: int


class VersesReadWithBook(VersesRead):
    book: Optional['Books'] = None
