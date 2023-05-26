import json
from threading import Thread
from typing import Any, Dict, List

import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage
from django.template.exceptions import TemplateDoesNotExist
from django.template.loader import get_template
from django.utils.translation import gettext_lazy as _
from requests.auth import HTTPBasicAuth

from apps.core.response import failMsg

User = get_user_model()


def sendAsyncEmail(eamil: EmailMessage) -> None:
    try:
        eamil.send()
    except ConnectionRefusedError:
        raise ValueError(failMsg["THE_EMAIL_SERVER_IS_NOT_WORKING"])
    except TemplateDoesNotExist:
        raise TemplateDoesNotExist(failMsg["THE_TEMPLATE_EMAIL_HAS_NOT_BEEN_FOUND"])


def send_email(
    subject: str,
    context: Dict[str, Any],
    to: List[str],
    template_name: str | None = None,
    _from: str = settings.EMAIL_HOST_USER,
) -> None:
    if settings.ENV != "production":
        return
    try:
        if template_name is None:
            raise TemplateDoesNotExist(failMsg["THE_TEMPLATE_EMAIL_HAS_NOT_BEEN_FOUND"])
        ext = template_name.split(".")[-1]
        htmlContent = get_template(template_name).render(context)
        email = EmailMessage(
            subject=subject,
            body=htmlContent,
            from_email=_from,
            to=to,
        )
        if ext == "html":
            email.content_subtype = "html"
        Thread(target=sendAsyncEmail, args=(email,)).start()
    except TemplateDoesNotExist:
        raise TemplateDoesNotExist(failMsg["THE_TEMPLATE_EMAIL_HAS_NOT_BEEN_FOUND"])


class SmsService:
    def __init__(self, body: str, to: str) -> None:
        self.body = body
        self.to = to

    def send(self) -> requests.Response | None:
        payload = {
            "messages": [
                {
                    "source": "php",
                    "from": settings.CLICKSEND_FROM,
                    "body": self.body,
                    "to": self.to,
                    "schedule": 1436874701,
                }
            ]
        }

        auth = HTTPBasicAuth(settings.CLICKSEND_USERNAME, settings.CLICKSEND_PASSWORD)
        if settings.ENV == "production":
            return requests.post(settings.CLICKSEND_URL, json.dumps(payload), auth=auth)
        return None


# send sms aysnc
def sendAsyncSMS(sms: SmsService) -> Any | None:
    try:
        response = sms.send()
        if response is None:
            return
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as errh:
        print("HTTP Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        print("Something went wrong:", err)


# send sms
def send_sms(body: str, to: str) -> None:
    sms = SmsService(body, to)
    Thread(target=sendAsyncSMS, args=(sms,)).start()
