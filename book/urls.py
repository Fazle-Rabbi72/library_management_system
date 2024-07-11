from django.urls import path,include
from . import views

urlpatterns = [
    path('book_detail/<int:pk>/',views.DetailsBookView.as_view(),name='book_detail'),
]