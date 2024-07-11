from django.contrib.auth.forms import UserCreationForm
from django import forms
from .constants import GENDER_TYPE
from django.contrib.auth.models import User
from .models import UserAccount,Transaction

class UserRegistrationForm(UserCreationForm):
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    gender = forms.ChoiceField(choices=GENDER_TYPE)
    
    class Meta:
        model = User
        fields = ['username','first_name',  'last_name', 'email', 'birth_date', 'gender','password1', 'password2']
    
    def save(self, commit=True):
        our_user = super().save(commit=False)
        if commit:
            our_user.save()
            gender = self.cleaned_data.get('gender')
            birth_date = self.cleaned_data.get('birth_date')
            
            # Check if UserAccount already exists
            if not UserAccount.objects.filter(user=our_user).exists():
                UserAccount.objects.create(
                    user=our_user,
                    gender=gender,
                    birth_date=birth_date,
                    account_no=our_user.id
                )
        return our_user

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = [
            'amount',
        ]
    def __init__(self, *args, **kwargs):
        self.account = kwargs.pop('account') # account value ke pop kore anlam
        super().__init__(*args, **kwargs)
    def save(self, commit=True):
        self.instance.account = self.account
        return super().save()

    def clean_amount(self): # amount field ke filter korbo
        min_deposit_amount = 100
        amount = self.cleaned_data.get('amount') # user er fill up kora form theke amra amount field er value ke niye aslam, 50
        if amount < min_deposit_amount:
            raise forms.ValidationError(
                f'You need to deposit at least {min_deposit_amount} $'
            )

        return amount
    
class UserUpdateForm(forms.ModelForm):
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    gender = forms.ChoiceField(choices=GENDER_TYPE)
    account_no=forms.IntegerField()
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # jodi user er account thake 
        if self.instance:
            try:
                user_account = self.instance.account
                
            except UserAccount.DoesNotExist:
                user_account = None
                
            if user_account:
                self.fields['gender'].initial = user_account.gender
                self.fields['birth_date'].initial = user_account.birth_date
                
    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()

            user_account, created = UserAccount.objects.get_or_create(user=user) # jodi account thake taile seta jabe user_account ar jodi account na thake taile create hobe ar seta created er moddhe jabe
            
            user_account.gender = self.cleaned_data['gender']
            user_account.birth_date = self.cleaned_data['birth_date']
            user_account.save()

            
        return user