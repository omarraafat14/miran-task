from django.core.exceptions import ValidationError


class Validation:
    """
    This class manages all validation methods in your project.

    **How it works:**

    - The `save` method automatically finds and runs all registered validation methods
    for the model being saved.
    - Any errors collected during validation will be raised as a single exception.

    **How to use:**
    1. Inherit from this class in your validation classes.
    2. Decorate your validation methods with `@Validation.register()`,
    optionally specifying an event ("create" or "update").
    3. Implement your validation logic in the methods.
    - Set errors in `self.errors_dict["field_name"] = "message"` format or make it array or messages.
    - Alternatively, append messages to `self.errors_messages("string")`.

    **Example:**
    ```py
    @Validation.register()
    def validate_value(self):
        if self.value >= 1:
            self.errors_dict["value"] = ["have to be lower than one", "have to be 0 or negative"]
            self.errors_dict["value"] = "value can't be more than 1"
            self.errors_messages("error that's not related to a specific field")
    ```
    """

    create_validations = {}
    update_validations = {}

    def __init__(self, *args, **kwargs):
        self.errors_messages = []
        self.errors_dict = {}
        super().__init__(*args, **kwargs)

    @classmethod
    def register(cls, when=None):
        def decorator(func):
            class_name = func.__qualname__.split(".")[0].split("Validation")[0]
            if when == "create":
                cls.add_to_dict(cls, func, cls.create_validations, class_name)
            elif when == "update":
                cls.add_to_dict(cls, func, cls.update_validations, class_name)
            else:
                cls.add_to_dict(cls, func, cls.create_validations, class_name)
                cls.add_to_dict(cls, func, cls.update_validations, class_name)

        return decorator

    def add_to_dict(cls, func, dict, class_name):
        if class_name in dict.keys():
            dict[class_name].append(func)
        else:
            dict[class_name] = [func]

    def save(self, *args, **kwargs):
        self.clean()
        return super().save(*args, **kwargs)

    def clean(self, *args, **kwargs):
        class_name = self.__class__.__name__
        if self.id:
            self.before_update(class_name)
        else:
            self.before_create(class_name)
        return self.raise_errors()

    def before_update(self, class_name):
        if class_name in set(self.update_validations.keys()):
            self.fire_validation_methods(self.update_validations[class_name])

    def before_create(self, class_name):
        if class_name in set(self.create_validations.keys()):
            self.fire_validation_methods(self.create_validations[class_name])

    def fire_validation_methods(self, array):
        for method in set(array):
            method(self)

    def raise_errors(self):
        if self.errors_messages:
            self.errors_dict["__all__"] = self.errors_messages

        if self.errors_dict:
            raise ValidationError(self.errors_dict)

        return super().clean()
