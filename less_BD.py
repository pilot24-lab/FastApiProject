from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import select
from fastapi import FastAPI, Depends
from pydantic import BaseModel
from typing import Annotated

app = FastAPI()
engine = create_async_engine('sqlite+aiosqlite:///books.db')

new_session = async_sessionmaker(engine, expire_on_commit=False)

async def get_session():
    async with new_session() as session:
        yield session

SessionDep = Annotated[AsyncSession, Depends(get_session)]

class Base(DeclarativeBase):
    pass
class BookModel(Base):
    __tablename__ = 'books'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] 
    author: Mapped[str] 

@app.post('/setup_database')
async def setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    return {'message': 'Database setup complete'}

class BookAddSheme(BaseModel):
    title: str
    author: str

class BookSheme(BookAddSheme):
    id: int

@app.post('/books')
async def add_book(data: BookSheme, session: SessionDep):
    new_book = BookModel(title=data.title, author=data.author)
    session.add(new_book)
    await session.commit()
    return {'message': 'Book added successfully'}

@app.get('/books')
async def get_books(session: SessionDep):
    query = select(BookModel)
    result = await session.execute(query)
    return result.scalars().all()