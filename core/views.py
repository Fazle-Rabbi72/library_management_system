from django.shortcuts import render, get_object_or_404
from user_account.models import UserAccount
from book.models import Books
from categories.models import Categories
from django.http import Http404 

def HomeView(request, category_slug=None):
    if request.user.is_authenticated:
        user_account = UserAccount.objects.get(user=request.user)
        gender = user_account.gender
    else:
        gender = None

    categories = Categories.objects.all()
    if category_slug:
        category = get_object_or_404(Categories, slug=category_slug)
        books = Books.objects.filter(categories=category)
    else:
        books = Books.objects.all()

    return render(request, 'index.html', {'books': books, 'categories': categories, 'gender': gender})
