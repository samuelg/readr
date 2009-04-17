from django import forms
from django.contrib.auth import authenticate, login


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
                raise forms.ValidationError("User Id and password combination was not found")
            
        return cleaned_data
