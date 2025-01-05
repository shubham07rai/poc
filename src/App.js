import React, { useState, useEffect } from 'react';
import axios from 'axios';

const App = () => {
  const [books, setBooks] = useState([]);
  const [newBook, setNewBook] = useState({ title: '', author: '', published_year: '' });
  
  // Fetch all books
  const fetchBooks = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:8000/books/');
      setBooks(response.data);
    } catch (error) {
      console.error('There was an error fetching the books!', error);
    }
  };

  // Create a new book
  const createBook = async () => {
    try {
      const response = await axios.post('http://127.0.0.1:8000/books/', newBook);
      setBooks([...books, response.data]);
      setNewBook({ title: '', author: '', published_year: '' });
    } catch (error) {
      console.error('There was an error creating the book!', error);
    }
  };

  // Delete a book
  const deleteBook = async (id) => {
    try {
      await axios.delete(`http://127.0.0.1:8000/books/${id}`);
      setBooks(books.filter(book => book.id !== id));
    } catch (error) {
      console.error('There was an error deleting the book!', error);
    }
  };

  // UseEffect to fetch books on initial load
  useEffect(() => {
    fetchBooks();
  }, []);

  return (
    <><div>
      <h1>Books CRUD Operations</h1>

      <div>
        <input
          type="text"
          placeholder="Title"
          value={newBook.title}
          onChange={(e) => setNewBook({ ...newBook, title: e.target.value })} />
        <input
          type="text" 
          placeholder="Author"
          value={newBook.author}
          onChange={(e) => setNewBook({ ...newBook, author: e.target.value })} />
        <input
          type="number"
          placeholder="Published Year"
          value={newBook.published_year}
          onChange={(e) => setNewBook({ ...newBook, published_year: e.target.value })} />
        <button onClick={createBook}>Add Book</button>
      </div>

      <h2>Book List</h2>
      <ul>
        {books.map((book) => (
          <li key={book.id}>
            {book.title} by {book.author} ({book.published_year})
            <button onClick={() => deleteBook(book.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
    <div>
        <React.Fragment>
          <title>Get Book Details</title>
          <button onClick={fetchBooks}> Fetch Books</button>
        </React.Fragment>
      </div>
      </>
  );
};

export default App;
