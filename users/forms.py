from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Field

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser
        fields = '__all__' #('username', 'email')

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email')

class AccountInfoForm(forms.ModelForm):
    first_name = forms.CharField(
        #label='',
        widget=forms.TextInput(attrs={'maxlength': '32'})
    )
    #email = forms.CharField(widget=forms.EmailInput(attrs={'maxlength': '64','disabled':'disabled'}))
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('first_name', css_class='form-group col-md-6 mb-0', autocomplete="given-name"),
                Column('last_name', css_class='form-group col-md-6 mb-0', autocomplete="family-name"),
                css_class='form-row'
            ),
            Field('email', autocomplete='email'),
            Submit('submit', 'Save Details')
        )
    
    class Meta:
        model = CustomUser
        fields = ['first_name','last_name']
    
    def clean(self):
        cleaned_data = super(AccountInfoForm, self).clean()
        #email = cleaned_data.get("email")
        
        """ if CustomUser.objects.filter(email=email):
            raise forms.ValidationError('Email already exists.') """
        return self.cleaned_data