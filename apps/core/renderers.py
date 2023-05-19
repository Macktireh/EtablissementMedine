import json

from rest_framework import renderers


class CustomJSONRenderer(renderers.JSONRenderer):
    charset = "utf-8"

    def render(self, data, accepted_media_types=None, renderer_context=None) -> str:
        response = ""
        if "ErrorDetail" in str(data):
            new_error = {}
            for field_name, field_errors in data.items():
                new_error[field_name] = field_errors[0]
            response = json.dumps({"status": "fail", "errors": new_error})
        else:
            response = json.dumps(data)
        return response
