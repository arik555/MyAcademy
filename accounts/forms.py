from django import forms
from django.contrib import auth
from courses.models import Author


class CustomerForm(auth.forms.UserCreationForm):
    password2 = forms.CharField(widget=forms.PasswordInput, help_text='Use exactly as above. Case Sensitive.',
                                label='Confirm Password')
    password1 = forms.CharField(widget=forms.PasswordInput, help_text='Use a strong password.', label='Password')

    class Meta:
        model = auth.models.User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2',)

    def clean(self):
        password2 = self.cleaned_data.get('password2')
        password1 = self.cleaned_data.get('password2')
        if password1 != password2:
            raise forms.ValidationError('Passwords Mismatch!')
        return self.cleaned_data


class AuthorForm(forms.ModelForm):

    class Meta:
        model = Author
        exclude = ('user', )


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        u = self.cleaned_data.get('username')
        p = self.cleaned_data.get('password')

        user = auth.authenticate(username=u, password=p)
        if user is None:
            raise forms.ValidationError('Invalid Username or Password')

        return self.cleaned_data

