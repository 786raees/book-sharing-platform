from pyexpat import model
from statistics import mode
from django.contrib import admin
from .models import Book,Chapter, Section

class ChapterInline(admin.TabularInline):
    model = Chapter
    extra = 1

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    '''Admin View for Book'''

    list_display = ("id",'name','author_name')

    inlines = [
        ChapterInline,
    ]




@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    '''Admin View for Chapter'''

    list_display = ('book_name','chapter_no','chapter_name')


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    '''Admin View for Section'''

    list_display = ('name','chapter','super_section')