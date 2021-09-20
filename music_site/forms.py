from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from musix.models import Audio, Sample


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()


class AudioUploadForm(forms.ModelForm):
    class Meta:
        model = Audio
        fields = ['title', 'genre', 'key', 'instrument', 'mp3']


# class SampleAddForm(forms.ModelForm):
#     class Meta:
#         model = Sample
#         fields = ['main', 'sub']

