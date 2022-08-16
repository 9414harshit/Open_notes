#form.py

from .models import notes,Comment,User
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth import password_validation

from django.contrib.auth.validators import UnicodeUsernameValidator

username_validator = UnicodeUsernameValidator()

class PasswordChangecustomForm(PasswordChangeForm):
    """
    A form that lets a user change their password by entering their old
    password.
    """
    old_password = forms.CharField(label=('Password'),
                                widget=(forms.PasswordInput(attrs={'class': 'form-control'})),
                                )
    new_password1 = forms.CharField(label=('Password'),
                                widget=(forms.PasswordInput(attrs={'class': 'form-control'})),
                                )
    new_password2 = forms.CharField(label=('Password'),
                                widget=(forms.PasswordInput(attrs={'class': 'form-control'})),
                                )
    class Meta:
    	model = User
    	fields = ["old_password", "new_password1", "new_password2"]

    

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=12, min_length=3, required=True, 
                                widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=12, min_length=3, required=True, 
                               widget=(forms.TextInput(attrs={'class': 'form-control'})))
    email = forms.EmailField(max_length=50, 
                             widget=(forms.TextInput(attrs={'class': 'form-control'})))
    password1 = forms.CharField(label=('Password'),
                                widget=(forms.PasswordInput(attrs={'class': 'form-control'})),
                                )
    password2 = forms.CharField(label=('Password Confirmation'), widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                                )
    username = forms.CharField(
        label=('Username'),
        max_length=150,
        validators=[username_validator],
        error_messages={'unique': ("A user with that username already exists.")},
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    class Meta:
    	model = User
    	fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)

    def clean(self):
       email = self.cleaned_data.get('email')
       if User.objects.filter(email=email).exists():
            raise ValidationError("This Email already exists")
       return self.cleaned_data

class Notesform(forms.ModelForm):
	title = forms.CharField(max_length=100, min_length=3, required=True, 
                                widget=forms.TextInput(attrs={'class': 'form-control'}))
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
	body = forms.CharField(max_length=150, label=(""), 
                                widget=forms.TextInput(attrs={'class': 'form-control' , 'placeholder':"Add a Comment...",}))
	class Meta:
		model=Comment
		fields = ['body']
		widgets = {
			'body': forms.TextInput(attrs={'class':'form-control'}),
			}
		label= {'body' : 'Comment Here' }

class shareForm(forms.Form):
	adduser = forms.CharField(max_length=20, min_length=3, required=False, label="",
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':"Enter a Username...",}))
	class Meta:
		fields = ['adduser']

