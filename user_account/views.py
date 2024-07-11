from django.shortcuts import render,redirect,HttpResponseRedirect
from django.views.generic import FormView,View
from django.contrib.auth import login ,logout
from .forms import UserRegistrationForm,UserUpdateForm,TransactionForm
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView,LogoutView
from django.contrib import messages
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import UserAccount,Transaction
from django.views.generic import CreateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.views import View
from datetime import datetime
from django.db.models import Sum
from borrow.models import Borrow
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from .models import UserAccount
from .forms import UserUpdateForm
from django.contrib.auth.models import User
def send_email_password(user, subject, template):
        user_account = UserAccount.objects.get(user=user)
        message = render_to_string(template, {
            'user_account' : user_account,
        })
        send_email = EmailMultiAlternatives(subject, '', to=[user.email])
        send_email.attach_alternative(message, "text/html")
        send_email.send()
def send_transaction_email(user_account, amount, subject, template):
        message = render_to_string(template, {
            'user_account' : user_account,
            'amount' : amount,
        })
        send_email = EmailMultiAlternatives(subject, '', to=[user_account.user.email])
        send_email.attach_alternative(message, "text/html")
        send_email.send()
class UserProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'user_account/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        form = UserUpdateForm(instance=user)

        try:
            user_account = UserAccount.objects.get(user=user)
        except UserAccount.DoesNotExist:
            user_account = None

        borrows = Borrow.objects.filter(borrower=user_account)
        gender = user_account.gender if user_account else None

        context.update({
            'form': form,
            'user_account': user_account,
            'borrows': borrows,
            'gender': gender,
        })
        return context

    def post(self, request, *args, **kwargs):
        form = UserUpdateForm(request.POST, instance=request.user)
        
        try:
            user_account = UserAccount.objects.get(user=request.user)
        except UserAccount.DoesNotExist:
            user_account = None

        borrows = Borrow.objects.filter(borrower=user_account)
        gender = user_account.gender if user_account else None

        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('profile')

        context = self.get_context_data(form=form, user_account=user_account, borrows=borrows, gender=gender)
        return self.render_to_response(context)


from django.contrib.auth.models import User
class UserRegistrationView(CreateView):
    model = User
    form_class = UserRegistrationForm
    title = 'Registration'
    template_name = 'user_account/user_resistration.html'
    success_url = reverse_lazy('home')  # Redirect to home after successful registration

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) # template e context data pass kor
        context.update({
            'title': self.title,
        })
        return context
    def form_valid(self, form):
        user = form.save()  # Save the form and create the user
        login(self.request, user)  # Log the user in
        messages.success(self.request, 'Registration successful. You are now logged in.')
        return super().form_valid(form) # Call the superclass method to handle redirection

class UserLoginView(LoginView):
    template_name='user_account/login.html'
    title = 'Login'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) # template e context data pass kor
        context.update({
            'title': self.title,
        })
        return context
    
    def get_success_url(self):
        messages.success(self.request, 'You have successfully logged in')
        return reverse_lazy('home')
    
    

class UserLogoutView(LogoutView):
     def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            logout(self.request)
            messages.success(self.request, 'You have successfully logged out')
        return HttpResponseRedirect(reverse_lazy('home'))

class TransactionCreateMixin(LoginRequiredMixin, CreateView):
    template_name = 'user_account/transaction_form.html'
    model = Transaction
    title = 'Deposit'
    success_url = reverse_lazy('profile')
    form_class = TransactionForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'account': self.request.user.account
        })
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) # template e context data pass kora
        user_account = UserAccount.objects.get(user=self.request.user)
        gender=user_account.gender
        print(gender,"checking")
        context.update({
            'title': self.title,
            'gender': gender
        })
        return context
    def form_valid(self, form):
        amount = form.cleaned_data.get('amount')
        account = self.request.user.account
        account.balance += amount # amount = 200, tar ager balance = 0 taka new balance = 0+200 = 200
        account.save(
            update_fields=[
                'balance'
            ]
        )
        user=UserAccount.objects.get(user=self.request.user)
        messages.success(
            self.request,
            f'{"{:,.2f}".format(float(amount))}$ was deposited to your account successfully! Email Has Been Sent!'
        )
        send_transaction_email(user, amount, "Deposite Message", "user_account/deposit_email.html")
        return super().form_valid(form)
    
class UserAccountUpdateView(LoginRequiredMixin,View):
    template_name ='user_account/update.html'
    def get(self, request):
        form = UserUpdateForm(instance=request.user)
        try:
            user_account = UserAccount.objects.get(user=request.user)
        except UserAccount.DoesNotExist:
            user_account = None
        borrows = Borrow.objects.filter(borrower=user_account)
        gender=user_account.gender
        print(gender,"checking")
        context = {
            'form': form,
            'user_account': user_account,
            'borrows': borrows,
            'gender':gender,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = UserUpdateForm(request.POST, instance=request.user)
        user_account = UserAccount.objects.filter(user=request.user)
        borrows = Borrow.objects.filter(borrower=request.user_account)
        gender=user_account.gender
        print(gender,"checking")
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('profile')
        context = {
            'form': form,
            'user_account': user_account,
            'borrows': borrows,
            'gender':gender,
        }
        return render(request, self.template_name, context)
    
class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'user_account/password_change.html'
    success_url = reverse_lazy('profile')
    
    def form_valid(self, form):
        messages.success(self.request, 'Password has been changed successfully!')
        send_email_password(self.request.user, "Reset Password", "user_account/pass_change_email.html")
        return super().form_valid(form)        

class ReturnBook(View):
    def post(self, request, *args, **kwargs):
        # Retrieve the object to be deleted
        borrow = Borrow.objects.get(pk=self.kwargs['pk'])
        
        # Perform the book return logic
        book_price = borrow.book.price
        user_account = UserAccount.objects.get(user=self.request.user)
        user_account.balance += book_price
        user_account.save()
        
        # Add success message
        messages.success(self.request, f"{borrow.book.title} has been returned successfully!")
        
        # Delete the Borrow record
        borrow.delete()
        
        # Redirect to the success URL
        return redirect('profile')