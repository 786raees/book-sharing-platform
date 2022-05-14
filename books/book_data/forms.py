from django import forms
from croppie.fields import CroppieField

from .models import Book, Chapter, Section

class BookForm(forms.ModelForm):
    cover = CroppieField(
        options={
            'viewport': {
                'width': 300,
                'height': 450,
            },
            'boundary': {
                'width': 325,
                'height': 475
            },
            'showZoomer': True,
        },
        required=False
    )
    class Meta:
        model = Book
        fields = ('name','cover')

class ChapterForm(forms.ModelForm):
    
    class Meta:
        model = Chapter
        fields = ("chapter_no",'chapter_name')

class SectionForm(forms.ModelForm):

    class Meta:

        model = Section
        fields = ('name','description')
