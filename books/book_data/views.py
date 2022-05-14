from unicodedata import name
from django.urls import reverse
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import get_user_model
from .forms import BookForm, ChapterForm, SectionForm
from .models import Book, Chapter, Section
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.forms import UserCreationForm


def home(request):
    if request.method == 'POST':
        search = request.POST.get('search')
        books = Book.objects.select_related('author_name').filter(name__startswith=search)
    else:
        books = Book.objects.select_related('author_name').all()
    context = {
        'books': books,
        'title': 'ALL BOOK'
    }
    return render(request, 'book_data/home.html', context)


def create_book(request):
    form = BookForm(request.POST, request.FILES or None)
    if form.is_valid():
        book = form.save(commit=False)
        book.author_name = request.user
        book.save()
        form = BookForm()

    context = {'form': form}
    return render(request, 'book_data/book_form.html', context)


def edit_book(request, id):
    bookobj = Book.objects.get(id=id)
    if request.user == bookobj.author_name:
        if request.method == 'POST':
            form = BookForm(request.POST, request.FILES, instance=bookobj)
            if form.is_valid():
                book = form.save(commit=False)
                book.author_name = request.user
                book.save()
                messages.add_message(
                    request, messages.SUCCESS, f"Book has been updated successfully")
                return redirect('home')
        form = BookForm(instance=bookobj)
        context = {'form': form}
        return render(request, 'book_data/book_form.html', context)
    else:
        messages.add_message(request, messages.WARNING,
                             f"You don't have permissions to change this {bookobj.name}")
    return redirect('home')


def books_by_author(request, id):
    try:
        books = Book.objects.select_related(
            'author_name').filter(author_name__id=id)
        context = {
            'books': books,
            'title': f'ALL BOOK OF {str(books.last().author_name.username).upper()}'

        }
    except:
        context = {
            'title':'Author do not have any book yet'
        }
    return render(request, 'book_data/home.html', context)


def delete_book(request, id):
    book = Book.objects.get(id=id)
    if request.user == book.author_name:
        book.delete()
        messages.add_message(request, messages.SUCCESS,
                             f"  Your book {book.name} has been deleted successfully")
    else:
        messages.add_message(request, messages.WARNING,
                             f"You don't have permissions to delete this {book.name}")
    return redirect('home')


def book_details(request, id):
    book = Book.objects.prefetch_related(
        'chapter_set', 'chapter_set__section_set__section_set__section_set__section_set__section_set__section_set__section_set__section_set__section_set__section_set__section_set').select_related('author_name').get(id=id)

    context = {
        'book': book,
    }
    return render(request, 'book_data/book_details.html', context)


def chapter_form(request, **kwargs):
    form = ChapterForm()
    book_id = kwargs.get('bookid')
    book = Book.objects.get(id=book_id)
    if request.method == "POST":
        form = ChapterForm(request.POST)
        if form.is_valid():
            chapter = form.save(commit=False)
            chapter.book_name = book
            chapter.save()
            return redirect(reverse('book_details', kwargs={'id': book_id}))
    context = {'form': form, 'BOOK_id': book_id}
    return render(request, 'book_data/chapter_form.html', context)


def create_sub_section(request, **kwargs):
    section_id = kwargs.get('sectionid')
    book_id = kwargs.get('bootid')
    section = Section.objects.get(id=section_id)
    form = SectionForm()
    if request.method == "POST":
        form = SectionForm(request.POST)
        if form.is_valid():
            new_section = form.save(commit=False)
            new_section.super_section = section
            new_section.save()
            return redirect(reverse('book_details', kwargs={'id': book_id}))

    context = {
        'section_id': section_id,
        'book_id': book_id,

        'form': form
    }
    return render(request, 'book_data/section_form.html', context)


def create_heading(request, **kwargs):
    chapter_id = kwargs.get('chapterid')
    book_id = kwargs.get('bootid')
    chapter = Chapter.objects.get(id=chapter_id)

    form = SectionForm()
    if request.method == "POST":
        form = SectionForm(request.POST)
        if form.is_valid():
            section = form.save(commit=False)
            section.chapter = chapter
            section.save()
            return redirect(reverse('book_details', kwargs={'id': book_id}))
    context = {
        'chapter_id': chapter_id,
        'book_id': book_id,
        'form': form
    }
    return render(request, 'book_data/heading_form.html', context)


def delete_chapter(request, id, bookid):
    chapter = Chapter.objects.get(id=id)
    chapter.delete()
    messages.add_message(request, messages.SUCCESS,
                         f"Your chapter {chapter.chapter_name} has been deleted successfully")

    return redirect(reverse('book_details', kwargs={'id': bookid}))


def delete_subsection(request, id, bookid):
    Sub_Section = Section.objects.get(id=id)
    Sub_Section.delete()
    messages.add_message(request, messages.SUCCESS,
                         f"Your Sub Section {Sub_Section.name} has been deleted successfully")

    return redirect(reverse('book_details', kwargs={'id': bookid}))


# we can use Django all auth but the nature
# of project was simple so
# use functional base aproach

def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        messages.add_message(request, messages.SUCCESS,
                             f"You are logged out successfully")
    else:
        messages.add_message(request, messages.WARNING,
                             f"You are allready logged out")
    return redirect('home')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')


        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.add_message(request, messages.SUCCESS,
                                f"You are logged in successfully")
            return redirect('home')
        else:
            messages.add_message(request, messages.WARNING,
                                f"Your username or password are not correct")
    return render(request, 'book_data/login_form.html')



def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'book_data/signup.html', {'form': form})
