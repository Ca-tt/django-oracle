from allauth.account.forms import SignupForm
from django import forms

class CustomSignupForm(SignupForm):
    name = forms.CharField(max_length=150, label='Name', widget=forms.TextInput(attrs={
        'placeholder': 'Your Name',
        'class': 'form-control',
    }))

    def save(self, request):
        user = super().save(request)
        user.first_name = self.cleaned_data['name']
        user.save()
        return user
