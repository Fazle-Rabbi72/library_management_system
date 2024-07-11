from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from .models import Borrow
from book.models import Books
from user_account.models import UserAccount
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

def send_borrow_email(user_account, borrow, subject, template):
    message = render_to_string(template, {
        'user_account': user_account,
        'borrow': borrow,
    })
    send_email = EmailMultiAlternatives(subject, '', to=[user_account.user.email])
    send_email.attach_alternative(message, "text/html")
    send_email.send()

@login_required(login_url='/user_account/login/')
def borrow_book(request, id):
    if request.method == 'POST':
        book = get_object_or_404(Books, pk=id)
        user_account = UserAccount.objects.get(user=request.user)
        if user_account.balance >= book.price:
            user_account.balance -= book.price
            user_account.save()
            borrow = Borrow.objects.create(borrower=user_account, book=book, balance_after_borrow=user_account.balance)
            messages.success(request, f"{book.title} has been borrowed successfully! Email Has Been Sent!")
            send_borrow_email(user_account, borrow, "Book Borrowing Message", "borrow_email.html")
            return redirect('book_detail', pk=book.pk)
        else:
            messages.error(request, "Insufficient balance to borrow this book.")
            return redirect('book_detail', pk=book.pk)
    else:
        # Handle GET request (optional: add additional logic for viewing the borrow form)
        user_account = UserAccount.objects.get(user=request.user)
        gender = user_account.gender
        print(gender, "checking")
        book = get_object_or_404(Books, pk=id)
        return render(request, 'book_detail.html', {'gender': gender, 'book': book})