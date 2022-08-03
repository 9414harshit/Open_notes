from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from .models import notes
from .form import Notesform
from django.contrib.auth.views import LogoutView,LoginView
from django.contrib.auth.mixins import LoginRequiredMixin  
from django.contrib.auth.forms import UserCreationForm

class LoginInterfaceView(LoginView):
	template_name ='notes/login.html'

class LogoutInterfaceView(LogoutView):
	template_name ='notes/logout.html'

class Signup(generic.edit.CreateView):
	form_class=UserCreationForm
	template_name='notes/register.html'
	success_url='/login'

class update_notes(LoginRequiredMixin,generic.edit.UpdateView):
	model=notes
	success_url = "/"
	form_class = Notesform
	login_url="/login"

	def get_queryset(self):
		if(self.request.user.notes.all()):
			return self.request.user.notes.all()
		else:
			raise Invalid("You are not the author of this note")

class new_notes(LoginRequiredMixin,generic.CreateView):
	model=notes
	success_url = "/"
	form_class = Notesform
	login_url='/login'

	def form_valid(self, form):
		self.object = form.save(commit=False)
		self.object.user= self.request.user
		self.object.save()
		return HttpResponseRedirect(self.get_success_url())

class notes_view(generic.ListView):
	model=notes
	context_object_name = 'note'
	template_name = 'notes/view.html'

	#def get_queryset(self):
	#	return self.request.user.notes.all()

class detail_view(generic.DetailView):
	model=notes
	context_object_name = 'note'
	template_name = 'notes/detail_list.html'

