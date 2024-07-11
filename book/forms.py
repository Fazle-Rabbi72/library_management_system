from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields =['body']
        widgets = {
            'body': forms.Textarea(attrs={
                'class': 'focus:bg-white focus:border-gray-500 py-3 px-4 leading-tight focus:outline-none text-gray-700 border border-gray-200 rounded-xl appearance-none block w-full bg-white',
                'rows': 3
            }),
        }
        