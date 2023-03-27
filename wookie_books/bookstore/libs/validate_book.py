from bookstore.models import Book
from .constants import BLOCK_USER
from .constants import BOOK_SCHEMA
import jsonschema


class ValidateBook:
    """
    The ValidateBook class contains a method to validate whether a book title can be added
    by a specific author based on certain conditions.

    Args:
    author: An instance of CustomUser representing the author who wants to add a book.

    Methods:
    validate(title): This method takes in a title parameter which is the title of the book to be added.
    validate(data): This method takes data parameter to validate the schema.
    It checks data with the schema, if a book with different data type which not match with the schema, the same title,
    and author already exists and returns appropriate code and status.

    Returns:
    Returns four values, code and status, j_path, j_schema, where:
    code: A string representing a code for a specific message or error.
    status: A boolean indicating whether the book title can be added or not.
    True means the title is valid, False means the title is invalid.
    j_path: A key path of the json.
    j_schema: type of the schema.
    """

    def __init__(self, author):
        self.author = author

    def validate(self, title, data):
        try:
            jsonschema.validate(data, BOOK_SCHEMA)
        except jsonschema.exceptions.ValidationError as e:
            path = ",".join(e.path)
            return "1006", False, path, e.schema

        if self.author.username.lower() == BLOCK_USER:
            return "1005", False, None, None
        book = Book.objects.filter(title=title, author=self.author)

        if book.exists():
            return "1002", False, None, None

        return "1003", True, None, None
