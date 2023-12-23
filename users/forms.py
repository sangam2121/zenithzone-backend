from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from django_registration.forms import RegistrationForm
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name',
                  'user_type', 'phone', 'address', 'bio',  'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data['email']
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("Email already exists")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if (password1 and password2 and password1 != password2):
            raise ValidationError("Password doesn't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        # user.is_active = False
        if commit:
            user.save()
        return user


class CustomUserChangeForm(UserChangeForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name',
                  'phone', 'address', 'bio', 'user_type')


class CustomRegistrationForm(RegistrationForm):
    class Meta(RegistrationForm.Meta):
        model = CustomUser
        fields = ('email', 'first_name', 'last_name',
                  'user_type', 'phone', 'address', 'bio')
