from typing import Dict, Union

from django.conf.global_settings import LANGUAGE_CODE
from django.utils.translation import gettext as _

LANG = "fr" if "fr" in LANGUAGE_CODE else "en"


def toggleLangMsg(msgFR: str, msgEN: str) -> str:
    return msgFR if LANG == "fr" else msgEN


def errorMessages(type: str, field: str) -> Union[str, None]:
    if type == "blank":
        if LANG == "fr":
            return f"Le champ {field} ne doit pas être vide !"
        return f"The {field} field must not be blank!"
    if type == "required":
        if LANG == "fr":
            return f"Le champ {field} est obligatoire !"
        return f"The {field} field is required!"


def succesMessage() -> Dict[str, str]:
    return {
        "YOUR_ACCOUNT_HAS_BEEN_SUCCESSFULLY_REGISTERED": _("Your account has been successfully registered."),
        "YOUR_ACCOUNT_HAS_BEEN_SUCCESSFULLY_ACTIVATED": _("Your account has been successfully activated."),
        "LOGIN_SUCCESS": _("Login success."),
        "THE_PASSWORD_HAS_BEEN_CHANGED_SUCCESSFULLY": _("The password has been changed successfully."),
        "PASSWORD_RESET_SUCCESSFULLY": _("Password reset successfully."),
        "THE_PASSWORD_RESET_LINK_HAS_BEEN_SENT": _("The password reset link has been sent. Please check your e-mail."),
        "LOGOUT_SUCCESS": _("Logout success."),
    }


def failMessage() -> Dict[str, str]:
    return {
        "PLEASE_ENTER_A_VALID_DJIBOUTIAN_TELEPHONE_NUMBER": _("Please enter a valid Djiboutian telephone number."),
        "THE_TELEPHONE_NUMBER_ALREADY_EXISTS": _("The telephone number already exists."),
        "THE_EMAIL_ADDRESS_DOES_NOT_EXIST": _("The email address does not exist."),
        "PLEASE_CONFIRM_YOUR_ADDRESS_EMAIL": _("Please confirm your address email."),
        "PLEASE_ENTER_A_VALID_EMAIL_ADDRESS": _("Please enter a valid email address."),
        "THE_EMAIL_ADDRESS_ALREADY_EXISTS": _("The email address already exists."),
        "THE_TEMPLATE_EMAIL_HAS_NOT_BEEN_FOUND": _("The template email has not been found."),
        "THE_EMAIL_SERVER_IS_NOT_WORKING": _("The email server is not working."),
        "THE_EMAIL_OR_PASSWORD_IS_INCORRECT": _("The email or password is incorrect."),
        "THE_PASSWORD_AND_PASSWORD_CONFIRMATION_DO_NOT_MATCH": _(
            "The password and password confirmation do not match."
        ),
        "INVALID_PASSWORD": _(
            "The password must contain at least 8 characters, a uppercase letter, \
                a lowercase letter, a number and a special character."
        ),
        "THE_TOKEN_IS_NOT_VALID_OR_HAS_EXPIRED": _("The token is not valid or has expired."),
        "YOU_ARE_NOT_AUTHORIZED_TO_PERFORM_THIS_ACTION": _("You are not authorized to perform this action."),
        "MISSING_PARAMETER": _("Missing parameter."),
        "SOMETHING_WENT_WRONG": _("Something went wrong."),
        "USER_DOES_NOT_EXIST": _("The user does not exist."),
    }


succesAuthMsg = succesMessage()
failAuthMsg = failMessage()
