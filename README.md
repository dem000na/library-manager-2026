# 📚 Library Manager

A simple command-line program written in Python for managing a small book collection. Add books, search them, borrow and return them, and your data is saved automatically between runs.

This project was built to practice object-oriented programming (classes, methods, `__str__`), file handling with JSON, input validation, and Python's `match` statement.

## Features

- Add books with a title, author, and page count (with input validation)
- View all books or only the available ones
- Search for a book by title
- Borrow, return and remove books
- Data is saved to a `books.json` file and loaded on the next start

## Requirements

- Python **3.10 or newer** (the program uses `match` statements)
- No external libraries - only the Python standard library

Check your version:

```bash
python --version
```

## How to run

1. Clone the repository:

   ```bash
   git clone https://github.com/dem000na/library-manager.git
   cd library-manager
   ```

2. Run the program:

   ```bash
   # Windows
   py library.py

   # macOS / Linux
   python3 library.py
   ```

## Usage

```
=== LIBRARY MENU ===
1. Add a book
2. Show all books
3. Show available books
4. Search for a book
5. Borrow a book
6. Return a book
7. Remove a book
8. Save and exit
```

Type the number of the action you want and press Enter. Choose **7** to save your books and quit. **Your changes are only saved when you exit with option 8.**

Titles search is not case-senesetive.

## Where is my data stored?

Books are saved in `books.json`, created automatically in the same folder as `library.py`. Example:

```json
[
    {
        "title": "Dune",
        "author": "Frank Herbert",
        "pages": 412,
        "available": true
    }
]
```

`books.json` is listed in `.gitignore`, so your personal data is not uploaded to GitHub.

## Project structure

```
library-manager/
├── library.py    # the whole program
├── README.md     # this file
└── .gitignore    # files Git should ignore
```

## How it works

| Part | Purpose |
|------|---------|
| `Book` class | Holds one book's data and can convert itself to a dictionary for JSON |
| `Library` class | Holds a list of `Book` objects and implements list, search, borrow, return |
| `save_file` / `load_file` | Write and read the library as JSON |
| `number_choice` / `name_choice` | Reusable, validated input helpers |
| `main` | Loads data, then runs the menu loop |

## Ideas for improvement

- Store the borrower's name and due date
- Unit tests with `pytest`


