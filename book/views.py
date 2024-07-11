from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from . import forms
from . import models
from borrow.models import Borrow
from user_account.models import UserAccount
from django.views.generic import DetailView

class DetailsBookView(DetailView):
    model = models.Books
    template_name = 'book_detail.html'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()  # Retrieve the book object
        review_form = forms.ReviewForm(data=self.request.POST)
        
        if not request.user.is_authenticated:
            messages.error(self.request, "You need to be logged in to leave a review.")
            return redirect('login')

        user_account = get_object_or_404(UserAccount, user=self.request.user)
        borrow = Borrow.objects.filter(borrower=user_account, book=self.object).exists()

        if not borrow:
            messages.error(self.request, "You have to borrow this book to give a review.")
            return redirect('book_detail', pk=self.object.pk)
        else:
            if review_form.is_valid():
                new_review = review_form.save(commit=False)
                new_review.books = self.object  # Assign the book to the review
                first_name = request.user.first_name
                last_name = request.user.last_name
                new_review.name = f'{first_name} {last_name}'  # Assign the user's name to the review
                new_review.save()
                messages.success(self.request, "Review has been added successfully!")
                return redirect('book_detail', pk=self.object.pk)
            else:
                return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        books = self.object

        if self.request.user.is_authenticated:
            user_account = get_object_or_404(UserAccount, user=self.request.user)
            has_borrow = Borrow.objects.filter(borrower=user_account, book=books).exists()
            gender = user_account.gender
            context['gender'] = gender
            context['has_borrow'] = has_borrow
        else:
            context['gender'] = None
            context['has_borrow'] = False

        reviews = books.reviews.all()
        review_form = forms.ReviewForm()
        context['reviews'] = reviews
        context['review_form'] = review_form
        return context