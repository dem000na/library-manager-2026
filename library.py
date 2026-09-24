"""
Library Manager - a small command-line program to manage a book collection.

Features: add books, list all/available books, search, borrow, return,
and save/load everything to a JSON file.
"""

import json
from pathlib import Path

# The save file lives in the same folder as this script, so the program
# works on any computer (Windows, macOS, Linux) without editing any paths.
DATA_FILE = Path(__file__).resolve().parent / "books.json"

LINE = "-" * 90


class Book:
    """Represents a single book with title, author, page count, and availability."""

    def __init__(self, title: str, author: str, pages: int, is_available: bool = True) -> None:
        self.title = title
        self.author = author
        self.pages = pages
        self.is_available = is_available

    def __str__(self) -> str:
        return f"Title: {self.title} | Author: {self.author} | Pages: {self.pages} | Available: {"Yes" if self.is_available else "No"}"

    def to_dict(self) -> dict:
        """Convert this Book into a plain dictionary so it can be saved as JSON."""
        return {
            "title": self.title,
            "author": self.author,
            "pages": self.pages,
            "available": self.is_available,
        }


class Library:
    """Represents a library that holds a collection of Book objects."""

    def __init__(self) -> None:
        self.books: list[Book] = []  # instance variable: THIS library's own list of books

    def add_book(self, book: Book) -> None:
        """Add a Book object into this library's collection."""
        self.books.append(book)

    def all_books(self) -> None:
        """Print every book in the library, regardless of availability."""
        print(f"All books: {len(self.books)}")

        if self.books:
            for book in self.books:
                print(book)
                print(LINE)
        else:
            print("Currently you have no books!")
            print(LINE)

    def available_books(self) -> None:
        """Print only the books that are currently available to borrow."""
        available = [book for book in self.books if book.is_available]
        print(f"Available books: {len(available)}")

        if available:
            for book in available:
                print(book)
                print(LINE)
        else:
            print("No books are available right now!")
            print(LINE)

    def find_book(self, title: str) -> None:
        """Search for a book by exact title match and print it if found."""
        for book in self.books:
            if title == book.title:
                print(book)
                return

        print("Book not found!")

    def borrow_book(self, title: str) -> None:
        """Mark a book as borrowed (is_available = False), if it exists and is free."""
        for book in self.books:
            if title == book.title and book.is_available:
                book.is_available = False
                print(f"You borrowed {book.title} successfully!")
                return

        print(f"{title} is already borrowed or was not found!")
        print("Check all books!")

    def return_book(self, title: str) -> None:
        """Mark a book as returned (is_available = True), if it exists and was borrowed."""
        for book in self.books:
            if title == book.title and not book.is_available:
                book.is_available = True
                print(f"You returned {book.title} successfully!")
                return

        print(f"{title} is already available or was not found!")
        print("Check all books!")


def show_menu() -> None:
    """Print the list of menu options for the user to choose from."""
    print("\n=== LIBRARY MENU ===")
    print("1. Add a book")
    print("2. Show all books")
    print("3. Show available books")
    print("4. Search for a book")
    print("5. Borrow a book")
    print("6. Return a book")
    print("7. Save and exit")
    print(LINE)


def number_choice(prompt: str = "Enter your choice: ") -> int | None:
    """
    Ask the user for a whole number and return it as an int.
    Returns None if the input can't be converted (caller must handle that case).
    """
    try:
        user_input = int(input(prompt))
        print(LINE)
        return user_input
    except ValueError:
        print("Enter a whole NUMBER!")
        return None


def name_choice(prompt: str = "Enter a title: ") -> str:
    """Ask the user for a plain text answer (title, author, search term, etc.)."""
    user_input = input(prompt).strip()
    print(LINE)
    return user_input


def create_book() -> Book:
    """Collect title, author, and a validated page count, then build a Book."""
    title = name_choice("Enter a title: ")
    author = name_choice("Enter an author: ")
    pages = number_choice("Enter pages: ")

    # Keep re-asking until we get a valid number greater than 0
    while True:
        if pages is None:
            pass  # conversion failed inside number_choice, ask again
        elif pages <= 0:
            print("Pages must be more than 0!")
        else:
            break

        pages = number_choice("Enter pages: ")

    return Book(title, author, pages)


def save_file(file_path: Path, lib: Library) -> None:
    """Write every Book in the library to disk as JSON (overwrites the file)."""
    data = [book.to_dict() for book in lib.books]

    try:
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
    except OSError as error:
        print(f"Could not save the file: {error}")


def load_file(file_path: Path, lib: Library) -> None:
    """Read Book data from a JSON file and add each Book to the given Library."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        for item in data:
            lib.add_book(Book(item["title"], item["author"], item["pages"], item["available"]))

    except FileNotFoundError:
        print("No save file found yet - starting with an empty library.")

    except (json.JSONDecodeError, KeyError, TypeError):
        print("Save file is empty or damaged - starting with an empty library.")


def main() -> None:
    """Entry point: sets up the library, loads saved data, then runs the menu loop."""
    lib = Library()
    load_file(DATA_FILE, lib)

    while True:
        show_menu()
        choice = number_choice()

        if choice is None:
            continue

        match choice:
            case 1:
                lib.add_book(create_book())
            case 2:
                lib.all_books()
            case 3:
                lib.available_books()
            case 4:
                lib.find_book(name_choice())
            case 5:
                lib.borrow_book(name_choice())
            case 6:
                lib.return_book(name_choice())
            case 7:
                save_file(DATA_FILE, lib)
                print("Saved. See you again!")
                break
            case _:
                print("Enter a number between 1 and 7!")


if __name__ == "__main__":
    main()
