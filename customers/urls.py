from django.urls import path

from customers.views import *

urlpatterns = [
    path("", Index.as_view(), name="index"),
    path("login", LoginView.as_view(), name="login"),
    path("singup", RegisterView.as_view(), name="singup"),
    path("activate/<uidb64>/<token>", ActivationView.as_view(), name="activate"),
    path("logout", logout_view, name="logout"),
    path("resetpassword", reset_password, name="resetpassword"),
    path(
        "resetpassword/<uidb64>/<token>",
        PasswordResetConfirmView.as_view(),
        name="resetpassword_confirm",
    ),
    path("dashboard", Dashboard.as_view(), name="dashboard"),
    path("dashboard/profile", Profile.as_view(), name="dashboard_profile"),
    path("dashboard/settings", CustomerSettings.as_view(), name="dashboard_settings"),
    path("dashboard/changepassword", change_password, name="dashboard_changepassword"),
    path("dashboard/changeemail", change_email, name="dashboard_changeemail"),
    path("dashboard/createboard", CreateBoard.as_view(), name="dashboard_createboard"),
    path(
        "dashboard/statusboard/<int:id>",
        StatusBoard.as_view(),
        name="dashboard_statusboard",
    ),
    path(
        "dashboard/statusboard/<int:bid>/default",
        set_default_status,
        name="dashboard_setdefaultstatus",
    ),
    path(
        "dashboard/statusboard/<int:bid>/iconset/<int:id>",
        iconset_status,
        name="dashboard_iconsetstatus",
    ),
    path(
        "dashboard/statusboard/<int:bid>/rename/<int:id>",
        rename_status,
        name="dashboard_renamestatus",
    ),
    path(
        "dashboard/statusboard/<int:bid>/delete/<int:id>",
        delete_status,
        name="dashboard_deletestatus",
    ),
    path("dashboard/deleteboard/<int:id>", delete_board, name="dashboard_deleteboard"),
    path("dashboard/activeboard/<int:id>", active_board, name="dashboard_boardactive"),
    path(
        "dashboard/deactiveboard/<int:id>",
        deactive_board,
        name="dashboard_boarddeactive",
    ),
    path("dashboard/previewboard", PreviewBoard.as_view(), name="preview_board"),
    path(
        "confirmemail/<uidb64>/<eidb64>/<token>",
        ConfirmNewEmail.as_view(),
        name="confirmemail",
    ),
]
