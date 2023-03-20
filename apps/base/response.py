from typing import Dict

from django.conf.global_settings import LANGUAGE_CODE


LANG = "fr" if "fr" in LANGUAGE_CODE else "en"
toggleLangMsg = lambda msgFR, msgEN: msgFR if LANG == 'fr' else msgEN

def errorMessages(type: str, field: str) -> str | None:
    if type == "blank":
        if LANG == 'fr':
            return f"Le champ {field} ne doit pas être vide !"
        return f"The {field} field must not be blank!"
    if type == "required":
        if LANG == 'fr':
            return f"Le champ {field} est obligatoire !"
        return f"The {field} field is required!"


def succesMessage() -> Dict[str, str]:
    return {
        "YOUR_ACCOUNT_HAS_BEEN_SUCCESSFULLY_REGISTERED": toggleLangMsg(
            msgFR = "Votre compte a été enregistré avec succès.",
            msgEN = "Your account has been successfully registered."
        ),
        "YOUR_ACCOUNT_HAS_BEEN_SUCCESSFULLY_ACTIVATED": toggleLangMsg(
            msgFR = "votre compte a été activé avec succès.",
            msgEN = "Your account has been successfully activated."
        ),
        "LOGIN_SUCCESS": toggleLangMsg(
            msgFR = "Connexion réussie.",
            msgEN = "Login success."
        ),
        "THE_PASSWORD_HAS_BEEN_CHANGED_SUCCESSFULLY": toggleLangMsg(
            msgFR = "Le mot de passe a été changé avec succès.",
            msgEN = "The password has been changed successfully."
        ),
        "PASSWORD_RESET_SUCCESSFULLY": toggleLangMsg(
            msgFR = "Réinitialisation du mot de passe réussie.",
            msgEN = "Password reset successfully."
        ),
        "THE_PASSWORD_RESET_LINK_HAS_BEEN_SENT": toggleLangMsg(
            msgFR = "Le lien de réinitialisation du mot de passe a été envoyé. Veuillez vérifier votre e-mail.",
            msgEN = "The password reset link has been sent. Please check your e-mail."
        ),
        "LOGOUT_SUCCESS": toggleLangMsg(
            msgFR = "Déconnexion réussie.",
            msgEN = "Logout success."
        )
    }


def failMessage() -> Dict[str, str]:
    return {
        "PLEASE_ENTER_A_VALID_DJIBOUTIAN_TELEPHONE_NUMBER": toggleLangMsg(
            msgFR = "Veuillez entrer un numéro de télépnone Djiboutien valide.",
            msgEN = "Please enter a valid Djiboutian telephone number."
        ),
        "THE_TELEPHONE_NUMBER_ALREADY_EXISTS": toggleLangMsg(
            msgFR = "Le numéro de télépnone existe déjà.",
            msgEN = "The telephone number already exists."
        ),
        "THE_EMAIL_ADDRESS_DOES_NOT_EXIST": toggleLangMsg(
            msgFR = "L'adresse e-mail n'existe pas.",
            msgEN = "The email address does not exist."
        ),
        "PLEASE_CONFIRM_YOUR_ADDRESS_EMAIL": toggleLangMsg(
            msgFR = "Veuillez confirmer votre adresse e-mail.",
            msgEN = "Please confirm your address email."
        ),
        "PLEASE_ENTER_A_VALID_EMAIL_ADDRESS": toggleLangMsg(
            msgFR = "Veuillez entrer une adresse email valide.",
            msgEN = "Please enter a valid email address."
        ),
        "THE_EMAIL_ADDRESS_ALREADY_EXISTS": toggleLangMsg(
            msgFR = "L'adresse email existe déjà.",
            msgEN = "The email address already exists."
        ),
        "THE_TEMPLATE_EMAIL_HAS_NOT_BEEN_FOUND": toggleLangMsg(
            msgFR = "Le template email n'a pas été trouvé.",
            msgEN = "The template email has not been found."
        ),
        "THE_EMAIL_SERVER_IS_NOT_WORKING": toggleLangMsg(
            msgFR = "Le serveur de messagerie ne fonctionne pas.",
            msgEN = "The email server is not working."
        ),
        "THE_EMAIL_OR_PASSWORD_IS_INCORRECT": toggleLangMsg(
            msgFR = "Email ou le mot de passe est incorrect.",
            msgEN = "The email or password is incorrect."
        ),
        "THE_PASSWORD_AND_PASSWORD_CONFIRMATION_DO_NOT_MATCH": toggleLangMsg(
            msgFR = "Le mot de passe et le mot de passe de confirmation ne correspondent pas.", 
            msgEN = "The password and password confirmation do not match."
        ),
        "INVALID_PASSWORD": toggleLangMsg(
            msgFR = "Le mot de passe doit contenir au moins 8 caractères, une lettre majuscule, minuscule, un chiffre et un caractère spécial.",
            msgEN = "The password must contain at least 8 characters, a uppercase letter, a lowercase letter, a number and a special character."
        ),
        "THE_TOKEN_IS_NOT_VALID_OR_HAS_EXPIRED": toggleLangMsg(
            msgFR = "Le jeton n'est pas valide ou a expiré.", 
            msgEN = "The token is not valid or has expired."
        ),
        "YOU_ARE_NOT_AUTHORIZED_TO_PERFORM_THIS_ACTION": toggleLangMsg(
            msgFR = "Vous n'êtes pas autorisé à effectuer cette action.",
            msgEN = "You are not authorized to perform this action."
        ),
        "MISSING_PARAMETER": toggleLangMsg(
            msgFR = "paramètre manquant.",
            msgEN = "Missing parameter."
        ),
        "SOMETHING_WENT_WRONG": toggleLangMsg(
            msgFR = "Quelque chose a mal tourné.",
            msgEN = "Something went wrong."
        ),
        "USER_DOES_NOT_EXIST": toggleLangMsg(
            msgFR = "L'utilisateur n'existe pas.",
            msgEN = "The user does not exist."
        )
    }


succesMsg = succesMessage()
failMsg = failMessage()
