import json

from rest_framework import renderers


class CustomJSONRenderer(renderers.JSONRenderer):
    charset = "utf-8"

    def render(self, data, accepted_media_types=None, renderer_context=None) -> str:
        response = ""
        if "ErrorDetail" in str(data):
            new_error = {}
            field_names_errors = []
            for field_name, field_errors in data.items():
                new_error[field_name] = field_errors[0] if isinstance(field_errors, list) else field_errors
                field_names_errors.append(field_name)
            response = json.dumps({"status": "fail", "Errorsfield": field_names_errors, "errors": new_error})
        else:
            response = json.dumps(data)
        return response
