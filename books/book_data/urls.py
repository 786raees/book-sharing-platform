from django.urls import path
from .views import (
    book_details, chapter_form, create_sub_section,
    delete_book, delete_chapter, delete_subsection, edit_book, home, create_book,
    delete_book, books_by_author, create_heading, login_view, logout_view, signup
)


urlpatterns = [
    path('', home, name="home"),
    path('create_book/', create_book, name="create_book"),
    path('delete_book/<int:id>/', delete_book, name="delete_book"),
    path('edit_book/<int:id>/', edit_book, name="edit_book"),
    path('book/<int:id>/', book_details, name="book_details"),
    path('books_by_author/<int:id>/', books_by_author, name="books_by_author"),
    path('chapter_form/<int:bookid>/', chapter_form, name="chapter_form"),
    path('create_sub_section/<int:sectionid>/<int:bootid>/',
         create_sub_section, name="create_sub_section"),
    path('create_heading/<int:chapterid>/<int:bootid>/',
         create_heading, name="create_heading"),
    path('delete_chapter/<int:id>/<int:bookid>/',
         delete_chapter, name="delete_chapter"),
    path('delete_subsection/<int:id>/<int:bookid>/',
         delete_subsection, name="delete_subsection"),
    path('logout_view/ ',
         logout_view, name="logout_view"),
    path('login_view/ ',
         login_view, name="login_view"),
    path('signup/ ',
         signup, name="signup"),
]
