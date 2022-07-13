#form.py

from .models import notes
from django import forms
from django.core.exceptions import ValidationError


class Notesform(forms.ModelForm):
	class Meta:
		model=notes
		fields = ['title','write']
		widgets = {
			'title': forms.TextInput(attrs={'class':'form-control' }),
			'write': forms.Textarea(attrs={'class':'form-control'})
		}
		label= {
			'write' : 'Text here'
		}

	'''def clean_title(self):
		title = self.cleaned_data['title']
		if 'Django' not in title:
			raise ValidationError("Haha you have to add this")
		return title
	'''