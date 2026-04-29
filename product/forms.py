from django import forms
from .models import ReviewRating
# from parler.forms import TranslatableModelForm


class ReviewForm(forms.ModelForm):
    class Meta:
        model = ReviewRating
        fields = ['subject', 'review', 'rating']
        widgets = {
            'rating': forms.NumberInput(attrs={'step': '0.5', 'min': '0', 'max': '5'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Review Title'}),
            'review': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Your review...'}),
        }
