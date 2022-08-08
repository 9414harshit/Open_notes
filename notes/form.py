#form.py

from .models import notes,Comment
from django import forms
from django.core.exceptions import ValidationError


class Notesform(forms.ModelForm):
	class Meta:
		model=notes
		fields = ['title','tags','write','privacy']
		widgets = {
			'title': forms.TextInput(attrs={'class':'form-control' }),
			'write': forms.Textarea(attrs={'class':'form-control'}),
			'tags': forms.TextInput(attrs={'class':'form-control' }),

		}
		label= {
			'write' : 'Text here'
		}

	def clean_title(self):
		title = self.cleaned_data['title']
		s=['fuck', 'ASS','sex']
		for x in s:
		    if x.casefold() in title.casefold():
		    	raise ValidationError("You can not use any slang words")

		return title

class CommentForm(forms.ModelForm):
	class Meta:
		model=Comment
		fields = ['body']
		widgets = {
			'body': forms.Textarea(attrs={'class':'form-control'}),
			}



