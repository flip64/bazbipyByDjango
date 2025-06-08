from django import forms
from .models import WatchedURL

class WatchedURLForm(forms.ModelForm):
    class Meta:
        model = WatchedURL
        fields = ['url']
        widgets = {
            'url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'آدرس لینک محصول'}),
        }
