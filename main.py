# 01. Practical Task: Build a "Book Inventory" API

"""This a simple Book Inventory API.
It allows user to:

1. View all books --> GET /books
2. Add a new books --> POST /books
The data is currently stored in a Python list (books_db), which acts as a mock database."""

from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional

# Create FastAPI application
# Think of it as start my API server
app = FastAPI()

# Create Book Model
# This define what a books look like
class Book(BaseModel):
    id: int
    title: str
    author: str
    is_available: bool = True # This is a default value

# Mock Database
books_db = [
    {"id": 1, "title": "The Hobbit", "author": "J.R.R. Tolkien", "is_available":
True}
]

# GET Endpoint
# When someone visit http://127.0.0.1:8000/books this function runs
@app.get("/books", response_model=List[Book])
async def get_books():
    return books_db

# POST Endpoint
# http://127.0.0.1:8000/books Used to add a new book
@app.post("/books")
async def add_book(book: Book): # FastAPI expect data in a book format
    books_db.append(book.dict()) # Converts the book object to dictionary
    return {"message": "book added successfully", "book" : book}

