from django.db import models
from users.models import CustomUser


class Book(models.Model):
    """
    Book is a Django model representing a book with its title, description,
    author, cover image, price, publication date, and published status.

    Attributes:
        title (models.CharField): The title of the book.
        description (models.TextField): A description of the book.
        author (models.ForeignKey): A foreign key reference to the CustomUser model as the author of the book.
        cover_image (models.ImageField): An optional image of the book's cover.
        price (models.DecimalField): The price of the book.
        published_on (models.DateTimeField): The date and time the book was published.
        published (models.BooleanField): A flag indicating whether the book is published.

    Methods:
        __str__(self) -> str:
            Returns a string representation of the book instance, using the title.

        unpublish(self) -> None:
            Sets the 'published' attribute to False, effectively unpublishing the book.

    The Book model enforces uniqueness on the combination of 'title' and 'author' fields.
    """
    title = models.CharField(max_length=255, help_text="The title of the book")
    description = models.TextField(help_text="A description of the book")
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, help_text="Author of written work")
    cover_image = models.ImageField(upload_to='covers/', null=True, blank=True,
                                    help_text="An optional image of the book's cover")
    price = models.DecimalField(max_digits=7, decimal_places=2, help_text="The price of the book")
    published_on = models.DateTimeField(auto_now=True, help_text="The date and time the book was published")
    published = models.BooleanField(default=True, help_text="A flag indicating whether the book is published")

    class Meta:
        unique_together = ('title', 'author')

    def __str__(self):
        """
        Returns a string representation of the Book instance using the title.

        Returns:
            str: The title of the Book instance.
        """
        return self.title

    def unpublish(self):
        """
        Sets the 'published' attribute to False, effectively unpublishing the book.

        Returns:
            None
        """
        self.published = False
