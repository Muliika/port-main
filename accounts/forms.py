from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordResetForm,
    SetPasswordForm,
)
from .models import UserBase


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "u-fullwidth",
                "placeholder": "Email",
                "id": "login-username",
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "u-fullwidth",
                "placeholder": "Password",
                "id": "login-pwd",
            }
        )
    )


class RegistrationForm(forms.ModelForm):
    user_name = forms.CharField(
        label="Enter Username",
        min_length=4,
        max_length=50,
        help_text="Required",
        widget=forms.TextInput(
            attrs={
                "class": "account__login--input",
                "placeholder": "Enter Username",
            }
        ),
    )
    email = forms.EmailField(
        max_length=100,
        help_text="Required",
        error_messages={"required": "Sorry, you will need an email"},
        widget=forms.EmailInput(
            attrs={
                "class": "account__login--input",
                "placeholder": "Email",
            }
        ),
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "account__login--input",
                "placeholder": "Password",
            }
        ),
    )
    password2 = forms.CharField(
        label="Repeat password",
        widget=forms.PasswordInput(
            attrs={
                "class": "account__login--input",
                "placeholder": "Confirm Password",
            }
        ),
    )

    class Meta:
        model = UserBase
        fields = (
            "user_name",
            "email",
        )

    def clean_user_name(self):
        user_name = self.cleaned_data["user_name"].lower()
        r = UserBase.objects.filter(user_name=user_name)
        if r.count():
            raise forms.ValidationError("Username already exists")
        return user_name

    def clean_password2(self):
        cd = self.cleaned_data
        if cd["password"] != cd["password2"]:
            raise forms.ValidationError("Passwords do not match.")
        return cd["password2"]

    def clean_email(self):
        email = self.cleaned_data["email"]
        if UserBase.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "Please use another Email, that is already taken"
            )
        return email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["user_name"].widget.attrs.update(
            {"class": "account__login--input", "placeholder": "Enter Username"}
        )
        self.fields["email"].widget.attrs.update(
            {
                "class": "account__login--input",
                "placeholder": "E-mail",
                "name": "email",
                "id": "id_email",
            }
        )
        self.fields["password"].widget.attrs.update(
            {"class": "account__login--input", "placeholder": "Password"}
        )
        self.fields["password2"].widget.attrs.update(
            {"class": "account__login--input", "placeholder": "Repeat Password"}
        )


class PwdResetForm(PasswordResetForm):
    email = forms.EmailField(
        max_length=254,
        widget=forms.TextInput(
            attrs={
                "class": "account__login--input",
                "placeholder": "Email",
                "id": "form-email",
            }
        ),
    )

    def clean_email(self):
        email = self.cleaned_data["email"]
        u = UserBase.objects.filter(email=email)
        if not u:
            raise forms.ValidationError(
                "Unfortunately we can not find that email address"
            )
        return email


class PwdResetConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label="New password",
        widget=forms.PasswordInput(
            attrs={
                "class": "account__login--input",
                "placeholder": "New Password",
                "id": "form-newpass",
            }
        ),
    )
    new_password2 = forms.CharField(
        label="Repeat password",
        widget=forms.PasswordInput(
            attrs={
                "class": "account__login--input",
                "placeholder": "Confirm New Password",
                "id": "form-new-pass2",
            }
        ),
    )


class UserEditForm(forms.ModelForm):
    email = forms.EmailField(
        label="Account email (can not be changed)",
        max_length=200,
        widget=forms.TextInput(
            attrs={
                "class": "account__login--input",
                "placeholder": "email",
                "id": "form-email",
                "readonly": "readonly",
            }
        ),
    )

    user_name = forms.CharField(
        label="Firstname",
        min_length=4,
        max_length=50,
        widget=forms.TextInput(
            attrs={
                "class": "account__login--input",
                "placeholder": "Username",
                "id": "form-firstname",
                "readonly": "readonly",
            }
        ),
    )

    first_name = forms.CharField(
        label="Username",
        min_length=4,
        max_length=50,
        widget=forms.TextInput(
            attrs={
                "class": "account__login--input",
                "placeholder": "Firstname",
                "id": "form-lastname",
            }
        ),
    )

    class Meta:
        model = UserBase
        fields = (
            "email",
            "user_name",
            "first_name",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["user_name"].required = True
        self.fields["email"].required = True
