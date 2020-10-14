from django import forms
from django.contrib.auth.forms import UserCreationForm
from customuser.models import User, Post, Like


class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')
    givenName = forms.CharField(max_length=150, required=False)
    familyName = forms.CharField(max_length=150, required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'givenName', 'familyName')


class PostForm(forms.ModelForm):
    post_text = forms.CharField(max_length=200)

    class Meta:
        model = Post
        fields = ('user', 'post_text')


class LikeForm(forms.ModelForm):
    likingUser = forms.CharField(max_length=200)
    upvote = forms.BooleanField()

    class Meta:
        model = Like
        fields = ('likingUser', 'upvote', 'user', 'post')
