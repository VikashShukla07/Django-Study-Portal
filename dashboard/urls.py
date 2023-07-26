from django.urls import path
from .import views


urlpatterns=[
    path('',views.home,name='home'),
    path('notes/',views.notes,name='notes'),
    path('delete/<int:pk>',views.delete_note,name='delete_note'),
    path('homework/',views.homework,name='homework'),
    path('deletehomework/<int:pk>',views.deletehomework,name='delete_homework'),
    path('youtube/',views.youtube,name='youtube'),
    path('books/',views.books,name='books'),
    path('dictionary/',views.dictionary,name='dictionary'),
    path('profile/',views.profile,name='profile'),
    path('chat/',views.chat_view, name='chat'),
    
]