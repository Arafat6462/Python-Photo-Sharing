from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Photo, Comment, Rating

class CustomUserCreationForm(UserCreationForm):
    is_creator = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('is_creator',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = None
        for field_name, field in self.fields.items():
            if not isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({'class': 'form-control'})

class PhotoUploadForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['title', 'caption', 'location', 'image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
            if isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({'rows': '3'})

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Add a comment...'}),
        }

class RatingForm(forms.ModelForm):
    score = forms.ChoiceField(
        choices=[(i, str(i)) for i in range(5, 0, -1)], # Reversed order
        widget=forms.RadioSelect(attrs={'class': 'star-rating-input'})
    )
    class Meta:
        model = Rating
        fields = ['score']
