from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string


def password_reset(to_email, user, url):
    email_template = render_to_string(
        "emails/password_reset_email.html",
        {
            "user": user,
            "reset_url": url,
        },
    )
    send_mail(
        "FeedbackHero password reset.",
        email_template,
        settings.EMAIL_HOST_USER,
        [to_email],
    )


def password_reset_done(to_email):
    email_template = render_to_string(
        "emails/password_reset_done_email.html", context=None
    )

    send_mail(
        "Your password have been changed.",
        email_template,
        settings.EMAIL_HOST_USER,
        [to_email],
    )
