from typing import Any, Dict, List
from threading import Thread

from django.conf import settings
from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model
from django.template.loader import get_template
from django.utils.translation import gettext_lazy as _
from django.template.exceptions import TemplateDoesNotExist

from apps.utils.response import failMessage


User = get_user_model()


def sendAsyncEmail(eamil: EmailMessage) -> None:
    try:
        eamil.send()
    except ConnectionRefusedError:
        raise ValueError(failMessage("THE_EMAIL_SERVER_IS_NOT_WORKING"))
    except TemplateDoesNotExist:
        raise TemplateDoesNotExist(failMessage("THE_TEMPLATE_EMAIL_HAS_NOT_BEEN_FOUND"))


def sendEmail(subject: str, context: Dict[str, Any], to: List[str], body: str = None, template_name: Any = None, _from: str = settings.EMAIL_HOST_USER) -> None:
    try:
        ext = template_name.split('.')[-1]
        htmlContent = get_template(template_name).render(context)
        email = EmailMessage(subject=subject, body=htmlContent if ext == 'html' else body, _from=_from, to=to)
        if ext == 'html':
            email.content_subtype = 'html'
        Thread(target=sendAsyncEmail, args=(email,)).start()
    except TemplateDoesNotExist:
        raise TemplateDoesNotExist(failMessage("THE_TEMPLATE_EMAIL_HAS_NOT_BEEN_FOUND"))