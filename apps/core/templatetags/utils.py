from typing import Any, Dict

from django.template.defaultfilters import register
from django.urls import translate_url as dj_translate_url


@register.simple_tag(takes_context=True)
def translate_url(context: Dict[str, Any], lang_code: str) -> str:
    path = context.get("request").get_full_path()
    return dj_translate_url(path, lang_code)
