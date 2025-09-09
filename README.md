# Library System 

from datetime import date, timedelta

class Book:
    def __init__(self, title: str, author: str, isbn: str, genre: str):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.genre = genre
        self.available = True
        self.borrower_id = None
        self.due_date = None

    def is_available(self):
        return self.available

    def borrow(self, user_id, due_date):
        if not self.available:
            raise ValueError(f"Book '{self.title}' is not available.")
        self.available = False
        self.borrower_id = user_id
        self.due_date = due_date

    def return_book(self, today):
        if self.available:
            raise ValueError(f"Book '{self.title}' is already available.")
        self.available = True
        self.borrower_id = None
        self.due_date = None


class PointsManager:
    def __init__(self):
        self._pts = {}

    def add_points(self, user_id, amount, reason):
        if amount <= 0:
            raise ValueError("Amount of points must be positive.")
        if user_id not in self._pts:
            self._pts[user_id] = 0
        self._pts[user_id] += amount

    def get_points(self, user_id):
        return self._pts.get(user_id, 0)

    def top_n(self, n):
        return sorted(self._pts.items(), key=lambda x: x[1], reverse=True)[:n]


class Library:
    _instance = None

    def __init__(self):
        self.books = []
        self.users = {}
        self.points = PointsManager()
        self.fine_strategy = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = Library()
        return cls._instance

    def add_book(self, book):
        self.books.append(book)

    def find_book_by_isbn(self, isbn):
        for book in self.books:
            if book.isbn == isbn:
                return book
        raise ValueError(f"No book found with ISBN {isbn}")

    def register_user(self, user):
        user_id = user["id"]
        if user_id in self.users:
            raise ValueError(f"User '{user_id}' already exists.")
        self.users[user_id] = user

    def borrow_book(self, user_id, isbn, today):
        if user_id not in self.users:
            raise ValueError(f"User '{user_id}' not found.")

        user = self.users[user_id]

        # borrow limit = 2 books
        borrow_limit = 2  

        borrowed_books = [b for b in self.books if b.borrower_id == user_id]

        if len(borrowed_books) >= borrow_limit:
            raise ValueError("You can't borrow more than 2 books at a time.")

        book = self.find_book_by_isbn(isbn)
        if not book.is_available():
            raise ValueError(f"Book '{isbn}' is not available.")

        due_date = today + timedelta(days=14)
        book.borrow(user_id, due_date)
        self.points.add_points(user_id, 10, "Borrowed a book")
        return due_date

    def return_book(self, user_id, isbn, today):
        book = self.find_book_by_isbn(isbn)
        if book.borrower_id != user_id:
            raise ValueError(f"Book '{isbn}' was not borrowed by user '{user_id}'.")
        fine = 0
        if self.fine_strategy:
            fine = self.fine_strategy(book, today)
        book.return_book(today)
        self.points.add_points(user_id, 5, "Returned a book")
        return fine


# Run Program

if __name__ == "__main__":
    library = Library.get_instance()

    # Add books
    books_to_add = [
    ]
    for b in books_to_add:
        library.add_book(b)

    # Register default user
    library.register_user({"id": "u1", "role": "student", "borrow_limit": 2})

    # Interactive menu
    while True:
        print("1. Borrow a Book")
        print("2. Return a Book")
        print("3. Show All Books")
        print("4. Exit")

        choice = input("Choose an option (1-4): ").strip()

        try:
            if choice == "1":
                isbn = input("Enter the book ISBN: ")
                due = library.borrow_book("u1", isbn, date.today())
                print(f"Book borrowed successfully. Due date: {due}")

            elif choice == "2":
                isbn = input("Enter the book ISBN: ")
                fine = library.return_book("u1", isbn, date.today())
                print(f"Book returned successfully. Fine: {fine}")

            elif choice == "3":
                print("\nAvailable Books:")
                for book in library.books:
                    status = "Available" if book.is_available() else f"Borrowed by {book.borrower_id}"
                    print(f"- {book.title} | ISBN: {book.isbn} | {status}")

            elif choice == "4":
                print("Exiting the system.")
                break

            else:
                print("Error: Please enter the correct number (1-4).")

        except ValueError as e:
            print(f"Error: {e}")
