#form.py

from .models import notes,Comment,User
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import password_validation

from django.contrib.auth.validators import UnicodeUsernameValidator

username_validator = UnicodeUsernameValidator()

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=12, min_length=4, required=True, 
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=12, min_length=4, required=True, 
                               widget=(forms.TextInput(attrs={'class': 'form-control'})))
    email = forms.EmailField(max_length=50, help_text='Required. Inform a valid email address.',
                             widget=(forms.TextInput(attrs={'class': 'form-control'})))
    password1 = forms.CharField(label=('Password'),
                                widget=(forms.PasswordInput(attrs={'class': 'form-control'})),
                                help_text=password_validation.password_validators_help_text_html())
    password2 = forms.CharField(label=('Password Confirmation'), widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                                help_text=('Just Enter the same password, for confirmation'))
    username = forms.CharField(
        label=('Username'),
        max_length=150,
        help_text=('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={'unique': ("A user with that username already exists.")},
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    class Meta:
    	model = User
    	fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)

'''

class SignUpForm(UserCreationForm):
    #username = forms.CharField(max_length=50)
    #first_name = forms.CharField( max_length=32, help_text='First name')
    #last_name=forms.CharField( max_length=32, help_text='Last name')
    #email=forms.EmailField( max_length=64, help_text='Enter a valid email address')
    #password1=forms.CharField()
    #password2=forms.CharField()

    class Meta(UserCreationForm.Meta):
        model = User
        # I've tried both of these 'fields' declaration, result is the same
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )
        #fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email',)
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password Again'}),
        }

'''
class Notesform(forms.ModelForm):
	class Meta:
		model=notes
		fields = ['title','write','privacy']
		widgets = {
			'title': forms.TextInput(attrs={'class':'form-control' }),
			'write': forms.Textarea(attrs={'class':'form-control'}),

		}
		label= {
			'write' : 'Text here'
		}

	def clean_title(self):
		title = self.cleaned_data['title']
		return title



class CommentForm(forms.ModelForm):
	class Meta:
		model=Comment
		fields = ['body']
		widgets = {
			'body': forms.Textarea(attrs={'class':'form-control'}),
			}



