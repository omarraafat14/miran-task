from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.views import exception_handler


class Http400(APIException):
    status_code = 400


def validation_error_handler(exc, context):
    try:
        status = exc.args[1] or 400
        errors = exc.args[0]
        if errors.get("__all__"):
            errors["details"] = errors.pop("__all__")

        all_errors = []
        for key, values in errors.items():
            values = values if isinstance(values, list) else [values]
            for value in values:
                all_errors.append(f"{f'{key} ' if key != 'details' else ''}{value}")

        errors["all_errors"] = all_errors
        return Response(errors, status)
    except:
        return exception_handler(exc, context)
