from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """
    CustomUser is a Django model that extends the AbstractUser model, adding
    additional fields and functionality specific to this application.

    Attributes:
        author_pseudonym (models.CharField): A unique pen name used by the user.
        blocked (models.BooleanField): A flag indicating whether the user account is blocked.
        created_on (models.DateTimeField): The date and time the user account was created.
        updated_on (models.DateTimeField): The date and time the user account was last updated.

    Methods:
        __str__(self) -> str:
            Returns a string representation of the user instance, using the author_pseudonym.

        block(self) -> None:
            Sets the 'blocked' attribute to True, effectively blocking the user account.
    """
    author_pseudonym = models.CharField(
        max_length=100, unique=True,
        help_text="A pen name may be used to make the "
                  "author' name more distinctive, "
                  "to disguise the author's gender, "
                  "to distance the author from their "
                  "other works, to protect the author "
                  "from retribution for their writings")
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        Returns a string representation of the CustomUser instance using the author_pseudonym.
        Returns:
            str: The author_pseudonym of the CustomUser instance.
        """
        return self.author_pseudonym
