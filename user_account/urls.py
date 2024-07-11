from django.urls import path
from .views import UserRegistrationView,UserLoginView,UserLogoutView,TransactionCreateMixin,ReturnBook,UserAccountUpdateView,UserProfileView,CustomPasswordChangeView


urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/',UserLoginView.as_view(),name='login'),
    path('logout/',UserLogoutView.as_view(),name='logout'),
    path('profile/', UserProfileView.as_view(), name='profile' ),
    path('update/', UserAccountUpdateView.as_view(), name='update' ),
    path('change_pass/',CustomPasswordChangeView.as_view(), name='change_pass' ),
    path("deposit/", TransactionCreateMixin.as_view(), name="deposit"),
    path('return_book/<int:pk>', ReturnBook.as_view() ,name='return_book'),
]