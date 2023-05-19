from django.utils.translation import gettext as _
from drf_yasg import openapi
from rest_framework import status

from apps.core.response import failMsg, succesMsg

signup_responses = {
    status.HTTP_201_CREATED: openapi.Response(
        description=_("Account created successfully."),
        examples={
            "application/json": {
                "status": _("success"),
                "message": succesMsg["YOUR_ACCOUNT_HAS_BEEN_SUCCESSFULLY_REGISTERED"],
            }
        },
    ),
    status.HTTP_400_BAD_REQUEST: "Validation error.",
}

activation_responses = {
    status.HTTP_200_OK: openapi.Response(
        description=_("Account activated successfully."),
        examples={
            "application/json": {
                "status": _("success"),
                "message": succesMsg["YOUR_ACCOUNT_HAS_BEEN_SUCCESSFULLY_ACTIVATED"],
            }
        },
    ),
    status.HTTP_400_BAD_REQUEST: "Validation error.",
}

login_responses = {
    status.HTTP_200_OK: openapi.Response(
        description=_("User logged in successfully."),
        examples={
            "application/json": {
                "status": _("success"),
                "message": succesMsg["LOGIN_SUCCESS"],
            }
        },
    ),
    status.HTTP_400_BAD_REQUEST: openapi.Response(
        description="Email or password is incorrect.",
        examples={
            "application/json": {
                "status": _("fail"),
                "message": failMsg["THE_EMAIL_OR_PASSWORD_IS_INCORRECT"],
            }
        },
    ),
    status.HTTP_403_FORBIDDEN: openapi.Response(
        description="Email is not verified.",
        examples={
            "application/json": {
                "status": _("fail"),
                "message": failMsg["PLEASE_CONFIRM_YOUR_ADDRESS_EMAIL"],
            }
        },
    ),
}


request_reset_passwoard_responses = {
    status.HTTP_200_OK: openapi.Response(
        description="Requested password reset successfully.",
        examples={
            "application/json": {
                "status": "success",
                "message": succesMsg["THE_PASSWORD_RESET_LINK_HAS_BEEN_SENT"],
            }
        },
    ),
    status.HTTP_400_BAD_REQUEST: "Validation error.",
}
