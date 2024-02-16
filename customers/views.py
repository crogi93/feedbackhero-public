from django.conf import settings
from django.contrib import messages
from django.contrib.auth import (
    authenticate,
    login,
    logout,
    update_session_auth_hash,
)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import (
    default_token_generator,
    PasswordResetTokenGenerator,
)
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods
from django.utils.encoding import force_str, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views.generic.base import View

from core.models import Suggestion

from customers import emails
from customers.forms import *
from customers.tokens import account_activation_token


def get_user(uidb64):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        return User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError):
        return None


class Index(View):
    template_name = "customers/index.html"

    def get(self, request):
        return render(request, self.template_name)


class LoginView(View):
    template_name = "customers/login_page.html"

    def get(self, request):
        if request.user.is_authenticated:
            return redirect("dashboard")
        return render(request, self.template_name)

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            login(request, form.user)
            messages.success(request, "You have successfully logged in.")
            return redirect("dashboard")

        [messages.warning(request, errors[0]) for errors in form.errors.values()]
        return redirect("login")


class RegisterView(View):
    template_name = "customers/singup_page.html"

    def get(self, request):
        if request.user.is_authenticated:
            return redirect("dashboard")
        return render(request, self.template_name)

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            token = account_activation_token.make_token(user)
            confirm_url = reverse("activate", kwargs={"uidb64": uidb64, "token": token})
            confirm_url = request.build_absolute_uri(confirm_url)
            emails.AccountActivation(user=user, confirm_url=confirm_url).send(
                user.email
            )
            messages.success(
                request,
                "Please go to your email inbox and click on received activation link to confirm and complete the registration. Note: Check your spam folder.",
            )
            return redirect("login")

        [messages.warning(request, errors[0]) for errors in form.errors.values()]
        return redirect("singup")


class ActivationView(View):
    template_name = "customers/succesfull_account_activation_page.html"

    def get(self, request, uidb64, token):
        user = get_user(uidb64)
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            emails.AccountCreation(user=user).send(user.email)
            messages.success(
                request,
                "Thank you for your email confirmation. Now you can login your account.",
            )
            return redirect("dashboard")

        messages.error(request, "Activation link is invalid!")
        return render(request, self.template_name)


@require_http_methods(["POST"])
def reset_password(request):
    form = ResetPasswordForm(request.POST)

    if form.is_valid():
        token_generator = PasswordResetTokenGenerator()
        uidb64 = urlsafe_base64_encode(force_bytes(form.user.pk))
        token = token_generator.make_token(form.user)
        reset_url = reverse(
            "resetpassword_confirm", kwargs={"uidb64": uidb64, "token": token}
        )
        reset_url = request.build_absolute_uri(reset_url)
        emails.PasswordReset(user=form.user, reset_url=reset_url).send(
            form.cleaned_data.get("email")
        )
        messages.success(request, "Recovery email have been send to you!")
        return redirect("login")

    [messages.warning(request, errors[0]) for errors in form.errors.values()]
    return redirect("login")


class PasswordResetConfirmView(View):
    template_name = "customers/reset_password_confirm_page.html"

    def get(self, request, uidb64, token):
        context = {
            "uidb64": uidb64,
            "token": token,
        }
        return render(request, self.template_name, context=context)

    def post(self, request, uidb64, token):
        user = get_user(uidb64)
        if user is not None and default_token_generator.check_token(user, token):
            form = SetPasswordForm(request.POST)
            if form.is_valid():
                form.save(user=user)
                update_session_auth_hash(request, user)
                emails.PasswordResetDone(user=user).send(user.email)
                messages.success(request, "Your password has been reset successfully.")
                return redirect("login")

            [messages.warning(request, errors[0]) for errors in form.errors.values()]
            return redirect(
                reverse(
                    "resetpassword_confirm", kwargs={"uidb64": uidb64, "token": token}
                )
            )

        messages.error(request, "The password reset link is invalid or has expired.")
        return redirect(
            reverse("resetpassword_confirm", kwargs={"uidb64": uidb64, "token": token})
        )


@login_required(login_url=reverse_lazy("login"))
def logout_view(request):
    logout(request)
    return redirect("login")


@method_decorator(login_required(login_url=reverse_lazy("login")), name="dispatch")
class Dashboard(View):
    template_name = "customers/dashboard_general_page.html"

    def get(self, request):
        boards = Board.objects.filter(
            user=request.user, deleted_at__isnull=True
        ).annotate(
            suggestion_count=Count("suggestion", distinct=True),
            vote_count=Count("suggestion__votes", distinct=True),
        )
        context = {"boards": boards}
        return render(request, self.template_name, context)


@login_required(login_url=reverse_lazy("login"))
@require_http_methods(["POST"])
def delete_board(request, id):
    board = get_object_or_404(Board, user=request.user, deleted_at__isnull=True, id=id)

    if request.user.check_password(request.POST.get("password")):
        board.soft_delete()
        board.save()
        messages.success(request, "Your board has been deleted successfully.")
        return redirect("dashboard")

    messages.success(request, "The password entered is invalid")
    return redirect("dashboard")


@login_required(login_url=reverse_lazy("login"))
@require_http_methods(["GET"])
def active_board(request, id):
    board = get_object_or_404(Board, user=request.user, deleted_at__isnull=True, id=id)
    board.is_active = True
    board.save()
    messages.success(request, "Your board is live now!")
    return redirect("dashboard")


@login_required(login_url=reverse_lazy("login"))
@require_http_methods(["GET"])
def deactive_board(request, id):
    board = get_object_or_404(Board, user=request.user, deleted_at__isnull=True, id=id)
    board.is_active = False
    board.save()
    messages.success(request, "Your board is offline now!")
    return redirect("dashboard")


@method_decorator(login_required(login_url=reverse_lazy("login")), name="dispatch")
class Profile(View):
    template_name = "customers/dashboard_profile_page.html"

    def get(self, request):
        context = {}
        return render(request, self.template_name, context)


@method_decorator(login_required(login_url=reverse_lazy("login")), name="dispatch")
class CustomerSettings(View):
    template_name = "customers/dashboard_customer_settings_page.html"

    def get(self, request):
        context = {
            "user": request.user,
        }
        return render(request, self.template_name, context)


@method_decorator(login_required(login_url=reverse_lazy("login")), name="dispatch")
class CreateBoard(View):
    template_name = "customers/dashboard_create_board_page.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        footer = {
            "footer_text": request.POST.get("footer_text"),
            "footer_extra": request.POST.get("footer_extra"),
            "contacts": {
                "twitter": request.POST.get("twitter"),
                "instagram": request.POST.get("instagram"),
                "email": request.POST.get("email"),
                "discord": request.POST.get("discord"),
                "website": request.POST.get("website"),
            },
        }
        data = {**request.POST.dict(), "footer": footer, "user": request.user}
        form = CreateBoardForm(data)
        if form.is_valid():
            form.save()
            messages.success(request, "Your board has been created successfully.")
            return redirect("dashboard_settings")

        [messages.warning(request, errors[0]) for errors in form.errors.values()]
        return render(request, self.template_name)


class PreviewBoard(View):
    template_name = "customers/preview_board_page.html"

    def get(self, request):
        return render(request, self.template_name)


@login_required(login_url=reverse_lazy("login"))
@require_http_methods(["POST"])
def change_password(request):
    data = {**request.POST.dict(), "email": request.user.email}
    form = ChangePasswordForm(data)

    if form.is_valid():
        form.save(user=request.user)
        update_session_auth_hash(request, request.user)
        emails.PasswordResetDone(user=request.user).send(request.user.email)
        messages.success(request, "Your password has been reset successfully.")
        return redirect("dashboard_settings")

    [messages.warning(request, errors[0]) for errors in form.errors.values()]
    return redirect("dashboard_settings")


@login_required(login_url=reverse_lazy("login"))
@require_http_methods(["POST"])
def change_email(request):
    form = ChangeEmailForm(request.POST)

    if form.is_valid():
        uidb64 = urlsafe_base64_encode(force_bytes(request.user.pk))
        eidb64 = urlsafe_base64_encode(force_bytes(form.cleaned_data.get("email")))
        token = account_activation_token.make_token(request.user)
        confirm_url = reverse(
            "confirmemail",
            kwargs={"uidb64": uidb64, "eidb64": eidb64, "token": token},
        )
        confirm_url = request.build_absolute_uri(confirm_url)
        emails.EmailReset(user=request.user, confirm_url=confirm_url).send(
            form.cleaned_data.get("email")
        )
        messages.success(
            request,
            "Please go to your email inbox and click on received activation link to confirm. Note: Check your spam folder.",
        )
        return redirect("dashboard_settings")

    [messages.warning(request, errors[0]) for errors in form.errors.values()]
    return redirect("dashboard_settings")


class ConfirmNewEmail(View):
    template_name = "customers/succesfull_change_email_page.html"

    def get(self, request, uidb64, eidb64, token):
        email = force_str(urlsafe_base64_decode(eidb64))
        form = ChangeEmailForm({"email": email})
        if form.is_valid():
            user = get_user(uidb64)
            if user is not None and account_activation_token.check_token(user, token):
                user.email = email
                user.save()
                update_session_auth_hash(request, user)
                emails.EmailResetDone(user=user).send(user.email)
                messages.success(
                    request,
                    "Thank you for your email confirmation. Now you can login your account.",
                )
                return render(request, self.template_name)

        messages.error(request, "Activation link is invalid!")
        return redirect("dashboard_settings")
