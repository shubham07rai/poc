from fastapi import Depends, FastAPI, HTTPException
from sqlmodel import SQLModel, Session, create_engine, select
from sqlmodel import Field
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware


# Database setup
DATABASE_URL = "sqlite:///./test.db"  # SQLite database file
engine = create_engine(DATABASE_URL, echo=True)

# Define the Book model
class Book(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    title: str
    author: str
    published_year: int

# Create the database tables
SQLModel.metadata.create_all(bind=engine)

# FastAPI app
app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"], 
)


# Pydantic model for request and response validation
class BookCreate(BaseModel):
    title: str
    author: str
    published_year: int

class BookResponse(BookCreate):
    id: int

# Dependency to get a database session
def get_session():
    with Session(engine) as session:
        yield session

# CRUD Operations

# Create a new book
@app.post("/books/", response_model=BookResponse)
def create_book(book: BookCreate, session: Session = Depends(get_session)):
    db_book = Book(**book.dict())
    session.add(db_book)
    session.commit()
    session.refresh(db_book)
    return db_book

# Read all books
@app.get("/books/", response_model=list[BookResponse])
def read_books(session: Session = Depends(get_session)):
    books = session.exec(select(Book)).all()
    return books

# Read a single book by ID
@app.get("/books/{book_id}", response_model=BookResponse)
def read_book(book_id: int, session: Session = Depends(get_session)):
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

# Update a book by ID
@app.put("/books/{book_id}", response_model=BookResponse)
def update_book(book_id: int, book: BookCreate, session: Session = Depends(get_session)):
    db_book = session.get(Book, book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    for key, value in book.dict().items():
        setattr(db_book, key, value)
    session.commit()
    session.refresh(db_book)
    return db_book

# Delete a book by ID
@app.delete("/books/{book_id}", response_model=BookResponse)
def delete_book(book_id: int, session: Session = Depends(get_session)):
    db_book = session.get(Book, book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    session.delete(db_book)
    session.commit()
    return db_book
