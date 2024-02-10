from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string


class Email:
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def send(self, recipients):
        rendered = render_to_string(self.template, self.kwargs)
        send_mail(self.title, rendered, settings.EMAIL_HOST_USER, [recipients])


class PasswordReset(Email):
    title = "Password Reset"
    template = "emails/password_reset_email.html"


class PasswordResetDone(Email):
    title = "Your Password Has Been Changed"
    template = "emails/password_reset_done_email.html"


class EmailReset(Email):
    title = "Confirmation Required: New Email Address"
    template = "emails/email_reset_email.html"


class EmailResetDone(Email):
    title = "Email Address Successfully Changed"
    template = "emails/email_reset_done_email.html"


class AccountCreation(Email):
    title = "Your Account Creation Confirmation"
    template = "emails/account_creation_email.html"


class AccountActivation(Email):
    title = "Activate Your Account Now"
    template = "emails/account_activation_email.html"
