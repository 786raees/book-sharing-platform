from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
# Create your models here.

# getting User model 
User = get_user_model()


class Book(models.Model):
    """This model is use to manage books."""
    name = models.CharField(max_length=100)
    cover = models.ImageField(upload_to='cover', blank=True, null=True)
    author_name = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        """Meta definition for Book."""

        verbose_name = 'Book'
        verbose_name_plural = 'Books'

    def __str__(self):
        """String representation of Book."""
        return f'{self.name}'

    def get_delete_url(self):
        return reverse('delete_book', kwargs={'id': self.pk})


class Chapter(models.Model):
    """Model to deal with multiple chapters in one book."""

    book_name = models.ForeignKey(Book, on_delete=models.CASCADE)
    chapter_no = models.FloatField()
    chapter_name = models.CharField(max_length=100)

    class Meta:
        """Meta definition for Chapter."""

        verbose_name = 'Chapter'
        verbose_name_plural = 'Chapters'

    def __str__(self):
        """String representation of Chapter."""
        return f'{self.chapter_name}'


class Section(models.Model):

    name = models.CharField(max_length=100)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, blank=True, null=True)
    super_section = models.ForeignKey('self',on_delete=models.CASCADE, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Section'
        verbose_name_plural = 'Sections'