from django import forms
from .models import UpcomingBook

class UpcomingBookForm(forms.ModelForm):
    '''Form for creating or updating an upcoming book entry.'''
    class Meta:
        model = UpcomingBook
        fields = ['title', 'author', 'description', 'release_date', 'cover_image']
