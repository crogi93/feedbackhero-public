from django import forms
from django.contrib.auth import authenticate

from customers.models import User


class LowercaseEmailField(forms.EmailField):
    def clean(self, value):
        value = super(LowercaseEmailField, self).clean(value)
        return value.lower()


class LoginForm(forms.Form):
    email = LowercaseEmailField()
    password = forms.CharField()

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        if email and password:
            self.user = authenticate(email=email, password=password)
            if self.user is None or not self.user.is_active:
                raise forms.ValidationError("Incorrect email or password.")

        return self.cleaned_data


class RegisterForm(forms.ModelForm):
    password_confirmation = forms.CharField()

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "terms_accepted", "password"]

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use.")
        return email

    def clean(self):
        password = self.cleaned_data.get("password")
        password_confirmation = self.cleaned_data.get("password_confirmation")
        terms_accepted = self.cleaned_data.get("terms_accepted")

        if password and password_confirmation and password != password_confirmation:
            raise forms.ValidationError("Passwords do not match")

        if not terms_accepted:
            raise forms.ValidationError(
                "Terms and conditions must be accepted to proceed."
            )

        return self.cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get("password"))
        if commit:
            user.save()
        return user


class ResetPasswordForm(forms.Form):
    email = LowercaseEmailField()

    def clean_email(self):
        email = self.cleaned_data.get("email")
        self.user = User.objects.filter(email=email).first()

        if self.user is None or not self.user.is_active:
            raise forms.ValidationError("This email does not exist in our database.")
        return email


class SetPasswordForm(forms.ModelForm):
    password_confirmation = forms.CharField()

    class Meta:
        model = User
        fields = ["password"]

    def clean(self):
        password = self.cleaned_data.get("password")
        password_confirmation = self.cleaned_data.get("password_confirmation")

        if password and password_confirmation and password != password_confirmation:
            raise forms.ValidationError("Passwords do not match")

    def save(self, user, commit=True):
        user.set_password(self.cleaned_data.get("password"))
        if commit:
            user.save()
        return user


class ChangePasswordForm(forms.ModelForm):
    current_password = forms.CharField()
    password_confirmation = forms.CharField()
    email = LowercaseEmailField()

    class Meta:
        model = User
        fields = ["password"]

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        current_password = cleaned_data.get("current_password")
        if email and current_password:
            user = authenticate(email=email, password=current_password)
            if user is None:
                raise forms.ValidationError("Invalid current password.")

        return cleaned_data

    def clean_new_password(self):
        password = self.cleaned_data.get("password")
        password_confirmation = self.cleaned_data.get("password_confirmation")

        if password and password_confirmation and password != password_confirmation:
            raise forms.ValidationError("Passwords do not match")
        return password_confirmation

    def save(self, user, commit=True):
        user.set_password(self.cleaned_data.get("password"))
        if commit:
            user.save()
        return user


class ChangeEmailForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["email"]

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use.")
        return email
