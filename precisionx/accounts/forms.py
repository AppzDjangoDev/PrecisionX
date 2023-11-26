from django import forms
from accounts.models import User  
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(
        label='First Name',
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'full-width', 'placeholder': 'First Name'})
    )
    last_name = forms.CharField(
        label='Last Name',
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'full-width', 'placeholder': 'Last Name'})
    )
    email = forms.EmailField(
        label='Email',
        required=True,
        widget=forms.EmailInput(attrs={'class': 'full-width', 'placeholder': 'Email'})
    )
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['first_name', 'last_name', 'email','username',  'password1']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None
        self.fields['username'].help_text = None
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'full-width', 'placeholder': field.label, 'id': 'login' + field_name})


class UserLoginForm(forms.Form):  
    username = forms.CharField(label="Username",max_length=50)  
    password = forms.CharField(label="Password", max_length = 100)  
    
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control m-2'

def validate_username(username):        
    if User.objects.filter(username=username).exists():
        raise ValidationError("Username already exists.")
    
def validate_email(user_email):        
    if User.objects.filter(email=user_email).exists():
        raise ValidationError("Email  already exists.")


class UserprofileUpdate(forms.ModelForm):
    # specify the name of model to use
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username" ,  "email" ]

    def __init__(self, *args, **kwargs):
        super(UserprofileUpdate, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control m-1'