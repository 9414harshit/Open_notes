#form.py

from .models import notes,Comment,User
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import password_validation

from django.contrib.auth.validators import UnicodeUsernameValidator

username_validator = UnicodeUsernameValidator()

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



