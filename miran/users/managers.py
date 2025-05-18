from django.contrib.auth.models import UserManager


class CustomUserManager(UserManager):
    def create_user(self, username, email, password, **extra_fields):
        # Remove the username argument from the create_user method to use email only.
        return super().create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        """
        Creates and saves an activated superuser with the credentials.

        Args:
            username: User's username
            email: User's email address
            password: Password for the superuser

        Returns:
            The created superuser User instance
        """
        extra_fields.setdefault("is_active", True)
        return super().create_superuser(username, email, password, **extra_fields)
