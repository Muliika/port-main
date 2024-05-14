from django.urls import path
from . import views
from .forms import PwdResetConfirmForm, PwdResetForm, UserLoginForm
from django.contrib.auth import views as auth_views

app_name = "accounts"

urlpatterns = [
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="accounts/registration/login.html",
            form_class=UserLoginForm,
            next_page="/",
        ),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(next_page="/"), name="logout"),
    path("register/", views.account_register, name="register"),
    path("profile/", views.profile, name="profile"),
    # path("login/", views.login_view, name="login"),
    # path("logout/", views.logout_view, name="logout"),
]
