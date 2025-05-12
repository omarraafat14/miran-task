import os

from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def create_model(self):
        with open(f"{self.project_path}/{self.app_name}/models.py", "a") as f:
            f.write(
                f"""
class {self.model_name}(validations.{self.model_name}Validation, mixins.{self.model_name}Mixin,models.Model):
    #relations


    #fields
    objects:managers.{self.model_name}QuerySet = managers.{self.model_name}QuerySet.as_manager()
    def __str__(self):
        return str(self.pk)
"""
            )

    def create_model_validation(self):
        with open(f"{self.project_path}/{self.app_name}/validations.py", "a") as f:
            f.write(
                f"""
class {self.model_name}Validation(Validation):
    ...
"""
            )

    def create_model_mixin(self):
        with open(f"{self.project_path}/{self.app_name}/mixins.py", "a") as f:
            f.write(
                f"""    
class {self.model_name}Mixin(LifecycleModelMixin):
    ...
"""
            )

    def create_model_manager(self):
        with open(f"{self.project_path}/{self.app_name}/managers.py", "a") as f:
            f.write(
                f"""
class {self.model_name}QuerySet(models.QuerySet):
    ...
"""
            )

    def register_admin(self):
        with open(f"{self.project_path}/{self.app_name}/admin.py", "a") as f:
            f.write(
                f"""
@admin.register(models.{self.model_name})
class {self.model_name}Admin(BaseModelAdmin):
    "Admin View for {self.model_name}"

"""
            )

    def create_view(self):
        with open(f"{self.project_path}/{self.app_name}/views.py", "a") as f:
            f.write(
                f"""
class {self.model_name}ViewSet(viewsets.ModelViewSet):
    queryset = models.{self.model_name}.objects.all()
    serializer_class = serializers.{self.model_name}Serializer
    #filterset_class = filters.{self.model_name}Filter
    #search_fields = [""]
    #filterset_fields = [""]
    #ordering = [""]
"""
            )

    def create_serializer(self):
        with open(f"{self.project_path}/{self.app_name}/serializers.py", "a") as f:
            f.write(
                f"""
class {self.model_name}Serializer(serializers.ModelSerializer):
    class Meta:
        model = models.{self.model_name}
        fields = "__all__"
"""
            )

    def add_view_path(self):
        target_text = "urlpatterns = ["
        new_text = (
            f"""router.register("{self.url_path}",views.{self.model_name}ViewSet)"""
        )
        file_path = f"{self.project_path}/{self.app_name}/urls.py"
        with open(file_path, "r") as f:
            lines = f.readlines()

        with open(file_path, "w") as f:
            for line in lines:
                if target_text in line:
                    f.write(new_text + "\n")
                f.write(line)

    def handle(self, *args, **options):
        self.project_path = os.path.join(os.getcwd(), "miran")
        apps = [app.split(".")[-1] for app in settings.LOCAL_APPS]
        print(f"here you are all the available apps {apps}")

        self.app_name = input("Give me the app name ")
        self.model_name = input("Give me the model name ")
        is_admin_register = input(
            "Do you want to register this model in the admin [Y/n]"
        )
        is_create_view = input("Do you want to create view to this model [Y/n]")

        self.create_model()
        self.create_model_mixin()
        self.create_model_validation()
        self.create_model_manager()

        if is_admin_register not in ["N", "n", "no"]:
            self.register_admin()
        if is_create_view not in ["N", "n", "no"]:
            self.url_path = input("Give me url path: ")
            if self.url_path == "":
                self.url_path = self.model_name.lower()
            self.create_view()
            self.create_serializer()
            self.add_view_path()
