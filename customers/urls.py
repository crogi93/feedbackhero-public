from django.urls import path

from customers.views import *


urlpatterns = [
    path("login", LoginView.as_view(), name="login_view"),
    path("register", RegisterView.as_view(), name="register_view"),
    path("logout", logout_view, name="logout"),
    path("dashboard", Dashboard.as_view(), name="dashboard"),
    path("password_reset", reset_password, name="password_reset"),
    path(
        "reset/<uidb64>/<token>",
        PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
]
