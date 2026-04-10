class BookService:
    def __init__(self):
        self.books = []

    def add_book(self, book):
        self.books.append(book)

    def list_books(self):
        return self.books

    def get_book(self, book_id):
        for book in self.books:
            if str(book.book_id) == str(book_id):
                return book
        return None

    def search_books_by_title(self, keyword):
        keyword = keyword.lower().strip()
        return [book for book in self.books if keyword in book.title.lower()]