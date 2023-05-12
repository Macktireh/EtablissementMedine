import json

from rest_framework import renderers


class CustomJSONRenderer(renderers.JSONRenderer):

    charset = "utf-8"

    def render(self, data, accepted_media_types=None, renderer_context=None) -> str:
        response = ""
        if "ErrorDetail" in str(data):
            response = json.dumps({"status": "fail", "errors": data})
        else:
            response = json.dumps(data)
        return response
