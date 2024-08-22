
from django import forms
from django.core.exceptions import ValidationError


from django.core.exceptions import ValidationError
from main.models import CustomUser

def validate_password(value):
    if len(value) < 8:
        raise ValidationError('Password must be at least 8 characters long.')
    if not any(char.isdigit() for char in value):
        raise ValidationError('Password must contain at least one digit.')


class RegisterForm(forms.Form):

    confirmation = forms.BooleanField()
    email = forms.EmailField(required=True)

    password = forms.CharField(
        max_length=50,
        widget=forms.PasswordInput,
        validators=[validate_password]
    )

    password_repeat = forms.CharField(
        max_length=50,
        widget=forms.PasswordInput
    )

    def clean_confirmation(self):
        if self.cleaned_data["confirmation"] is not True:
            raise ValidationError("You must confirm!")
        

    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get("password")
        password_repeat = cleaned_data.get("password_repeat")
        
        if password and password_repeat and password != password_repeat:
            raise ValidationError("Passwords do not match.")
        
        
        email = cleaned_data.get("email")

        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("There is already a user with this email.")
        
        return cleaned_data
