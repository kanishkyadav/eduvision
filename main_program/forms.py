from ckeditor.fields import CKEditorWidget
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UsernameField, UserCreationForm
from django.contrib.auth.models import User
from .models import Post


class PostForm(forms.Form):
    content = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Post
        fields = ["title", "content", "category", "author"]


class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'placeholder': 'username'}))
    password = forms.CharField(strip=False, widget=forms.PasswordInput(
        attrs={'autocomplete': 'current-password', 'placeholder': '******'}))


class UserSignUpForm(UserCreationForm):
    is_active = True
    password1 = forms.CharField(label='Password',
                                widget=forms.PasswordInput(attrs={'placeholder': '*****'}))
    password2 = forms.CharField(label='Password(again)',
                                widget=forms.PasswordInput(attrs={'placeholder': '*****'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'is_staff']
        labels = {'email': 'Email', 'first_name': 'Firest Name', 'last_name': 'Last Name', 'is_staff': 'Choice'}
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'placeholder': 'eg. xyz@mail.com'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'Firstname'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Lastname'}),
        }
