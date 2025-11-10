from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Photo

class CustomUserCreationForm(UserCreationForm):
    is_creator = forms.BooleanField(required=False, help_text="Check this box if you are a creator.")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('is_creator',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = None
        self.fields['password2'].help_text = None
        # self.is_creator.help_text = None

class PhotoUploadForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['title', 'caption', 'location', 'image']
