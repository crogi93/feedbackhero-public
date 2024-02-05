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
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.encoding import force_str, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views.generic.base import View

from customers.emails import *
from customers.forms import *


class LoginView(View):
    template_name = "customers/login_view.html"

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

        error_messages = "\n".join(
            [", ".join(errors) for errors in form.errors.values()]
        )
        messages.warning(request, error_messages)
        return redirect("login_view")


class RegisterView(View):
    template_name = "customers/register_view.html"

    def get(self, request):
        if request.user.is_authenticated:
            return redirect("dashboard")
        return render(request, self.template_name)

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user = authenticate(
                email=form.cleaned_data.get("email"),
                password=form.cleaned_data.get("password"),
            )
            if user is not None:
                login(request, user)
            messages.success(request, "You have successfully created an account.")
            return redirect("dashboard")

        error_messages = "\n".join(
            [", ".join(errors) for errors in form.errors.values()]
        )
        messages.warning(request, error_messages)
        return redirect("register_view")


def reset_password(request):
    form = PasswordResetForm(request.POST)

    if form.is_valid():
        token_generator = PasswordResetTokenGenerator()
        uidb64 = urlsafe_base64_encode(force_bytes(form.user.pk))
        token = token_generator.make_token(form.user)
        reset_url = reverse(
            "password_reset_confirm", kwargs={"uidb64": uidb64, "token": token}
        )
        reset_url = request.build_absolute_uri(reset_url)
        password_reset(form.cleaned_data.get("email"), form.user, reset_url)
        messages.success(request, "Recovery email have been send to you!")
        return redirect("login_view")

    error_messages = "\n".join([", ".join(errors) for errors in form.errors.values()])
    messages.warning(request, error_messages)
    return redirect("login_view")


class PasswordResetConfirmView(View):
    template_name = "customers/password_reset_confirm_view.html"

    def get_user(self, uidb64):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            return User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError):
            return None

    def get(self, request, uidb64, token):
        context = {
            "uidb64": uidb64,
            "token": token,
        }
        return render(request, self.template_name, context=context)

    def post(self, request, uidb64, token):
        user = self.get_user(uidb64)
        if user is not None and default_token_generator.check_token(user, token):
            form = SetPasswordForm(request.POST)
            if form.is_valid():
                form.save(user=user)
                update_session_auth_hash(request, user)
                password_reset_done(user.email)
                messages.success(request, "Your password has been reset successfully.")
                return redirect("login_view")

            error_messages = "\n".join(
                [", ".join(errors) for errors in form.errors.values()]
            )

            messages.warning(request, error_messages)
            return redirect(
                reverse(
                    "password_reset_confirm", kwargs={"uidb64": uidb64, "token": token}
                )
            )

        messages.error(request, "The password reset link is invalid or has expired.")
        return redirect(
            reverse("password_reset_confirm", kwargs={"uidb64": uidb64, "token": token})
        )


@login_required(login_url=reverse_lazy("login_view"))
def logout_view(request):
    logout(request)
    return redirect("login_view")


@method_decorator(login_required(login_url=reverse_lazy("login_view")), name="dispatch")
class Dashboard(View):
    template_name = "customers/dashboard_view.html"

    def get(self, request):
        context = {}
        return render(request, self.template_name, context)
