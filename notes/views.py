from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from .models import notes
from .form import Notesform 

class update_notes(generic.edit.UpdateView):
	model=notes
	success_url = "/notes"
	form_class = Notesform

class new_notes(generic.CreateView):
	model=notes
	success_url = "/notes"
	form_class = Notesform

class notes_view(generic.ListView):
	model=notes
	context_object_name = 'note'
	template_name = 'notes/view.html'

	def get_queryset(self):
		return notes.objects.order_by('-date')

class detail_view(generic.DetailView):
	model=notes
	context_object_name = 'note'
	template_name = 'notes/detail_list.html'

