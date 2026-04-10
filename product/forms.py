from django import forms
from .models import ReviewRating
from parler.forms import TranslatableModelForm


class ReviewForm(TranslatableModelForm):
    class Meta:
        model = ReviewRating
        fields = ['subject', 'review', 'rating']
        