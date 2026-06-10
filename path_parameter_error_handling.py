"""Right now, we can view all books. But what if a user wants to view just one specific book? we use Path Parameters. we'll also need to handle the scenario where a user asks for a book ID that doesn't exist using FastAPI's HTTPException."""

"""
Complete Book Inventory API

Features:-
1. GET /books -> View all books (with optional 'author' search)
2. GET /books/{book_id} -> View a single book
3. POST /books -> Add a new book
4. PUT /books/{book_id} -> Update an existing book
5. DELETE /books/{book_id} -> Remove a book

"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

# Initialize the FastAPI application
app = FastAPI()

# --- Data Models ---
class Book(BaseModel):
    id: int
    title: str
    author: str
    is_available: bool = True

# Mock Database
books_db = [
    {"id": 1, "title": "The Hobbit", "author": "J.R.R. Toklkien", "is_available": True}
]

# --- API ENDPOINTS ---
# 1. GET ALL BOOKS & SEARCH BY AUTHOR (Query Parameter)
# Notice `author: Optional[str] = None`. Because it's not in the path string,
# FastAPI automatically makes this a query parameter (e.g., /books?author=Tolkien).

@app.get("/books", response_model=List[Book])
async def get_books(author: Optional[str] = None):
    if author:
        # Filter the list if an author is provided (case-insensitive)
        filtered_books = [
            book for book in books_db
            if book["author"].lower() == author.lower()
        ]
        return filtered_books
    
    # If no author query is provided, return all books
    return books_db

# 2. GET A SINGLE BOOK (Path Parameter)
# The {book_id} in the route matches the book_id parameter in the function.
@app.get("/books/{book_id}", response_model=Book)
async def get_book(book_id: int):
    for book in books_db:
        if book["id"] == book_id:
            return book
        
    # If the loop finishes without returing, the book wasn't found!
    raise HTTPException(status_code=404, detail="Book not Found!")

#3. ADD A NEW BOOK (POST)
@app.post("/books")
async def add_books(book: Book):
    # Optional safety check: Ensure we don't add duplicates IDs
    for existing_book in books_db:
        if existing_book["id"] == book.id:
            raise HTTPException(status_code=404, details="Book with this ID already exists.")
        
    # Convert pydantic model to dictionary
    books_db.append(book.dict())
    return {"message": "Book added successfully", "book": book}

# 4. UPDATE AN EXISTING BOOK (PUT)
@app.put("/books/{book_id}")
async def update_book(book_id: int, update_book: Book):
    # Enumerate gives us the both the index and the item in the list
    for index, book in enumerate(books_db):
        if book["id"] == book_id:
            # Replace the old dictionary with the new one.
            books_db[index] = update_book.dict()
            return {"message": "Book updated successfully", "book": books_db[index]}
        
    # If we don't find the book to update, through a 404 error
    raise HTTPException(status_code=404, detail="Book not found!")

# 5. DELETE A BOOK (DELETE)
@app.delete("/books/{book_id}")
async def delete_book(book_id: int):
    for index, book in enumerate(books_db):
        if book["id"] == book_id:
            # .pop() removes the item at the specified index and returns it
            delete_book = books_db.pop(index)
            return {"message": "Book deleted successfully", "deleted_book": delete_book}
        
    # If we don't find the book to delete, through a 404 error
    raise HTTPException(status_code=404, detail="Book not found!")

        
        