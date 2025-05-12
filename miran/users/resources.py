from import_export import resources

from .models import User


class UserResource(resources.ModelResource):
    class Meta:
        model = User
        fields = [
            "id",
            "password",
            "last_login",
            "first_name",
            "last_name",
            "date_joined",
            "email",
            "username",
            "phone",
            "verification_code",
        ]
        export_order = fields
