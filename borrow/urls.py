from django.urls import path
from . import views

urlpatterns = [
    path('create_borrow/<int:id>', views.borrow_book, name='create_borrow'),
]