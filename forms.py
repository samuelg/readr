from django import forms
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    user_id = forms.CharField(max_length=50, widget=forms.TextInput)
    password = forms.CharField(max_length=16, widget=forms.PasswordInput(render_value=False))

    def clean(self):
        """
            Validates the user_id's existence and the password provided for that user.
        """
        cleaned_data = self.cleaned_data
        user_id = cleaned_data.get('user_id')
        password = cleaned_data.get('password')

        if user_id and password:
            user = authenticate(username=user_id, password=password)

            if user is None or not user.is_active:
                raise forms.ValidationError('user id and password combination not found')
            
        return cleaned_data

class RegisterForm(forms.Form):
    user_id = forms.CharField(max_length=50, widget=forms.TextInput)
    password = forms.CharField(max_length=16, widget=forms.PasswordInput(render_value=False))
    password_confirm = forms.CharField(max_length=16, widget=forms.PasswordInput(render_value=False))

    def clean(self):
        """
            Validates that the user id is not taken and that the password confirmation matches
            the password given.
        """
        cleaned_data = self.cleaned_data
        user_id = cleaned_data.get('user_id')
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if user_id and password and password_confirm:            
            try:
                user = User.objects.get(username=user_id)
            except User.DoesNotExist:
                user = None

            if user is not None:
                raise forms.ValidationError('the user id is already in use')
            if password != password_confirm:
                raise forms.ValidationError('password_confirm must match password')
            
        return cleaned_data
