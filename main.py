from fastapi import FastAPI, HTTPException
import uvicorn
from pydantic import BaseModel
app = FastAPI()
books = [
    {"id": 1, "title": "1984", "author": "George Orwell"},
    {"id": 2, "title": "To Kill a Mockingbird", "author": "Harper Lee"},
    {"id": 3, "title": "The Great Gatsby", "author": "F. Scott Fitzgerald"}
]
@app.get('/books', tags = ['Книги'], summary="Получить все книги", description="Возвращает список всех книг в библиотеке")
def read_books():
    return books

@app.get('/books/{id}', tags = ['Книги'], summary="Получить книгу по ID", description="Возвращает информацию о книге по её уникальному идентификатору")
def get_book(id: int):
    for book in books:
        if book['id'] == id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")

class NewBook(BaseModel):
    title: str
    author: str

@app.post('/books')
def create_book(new_book: NewBook):
    book_id = len(books) + 1
    book = {"id": book_id, "title": new_book.title, "author": new_book.author}
    books.append(book)
    return book
    
if __name__ == "__main__":
    uvicorn.run('main:app', reload=True)