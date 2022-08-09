from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from .models import notes,Comment,User
from .form import Notesform, CommentForm
from django.contrib.auth.views import LogoutView,LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q # new


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
		if(self.request.user.notes_set.all()):
			return self.request.user.notes_set.all()
		else:
			raise KeyError("You are not the author of this note")

class new_notes(LoginRequiredMixin,generic.CreateView):
	model=notes
	success_url = "/"
	form_class = Notesform
	login_url='/login'

	def form_valid(self, form):
		self.object = form.save(commit=False)
		self.user=self.request.user.id
		self.object.save()

		self.object.user.add(self.request.user.id)
		self.object.save()
		form.save_m2m()
		return HttpResponseRedirect(self.get_success_url())


class notes_view(generic.ListView):
	model=notes
	context_object_name = 'note'
	template_name = 'notes/view.html'


	def get_queryset(self):
		#if self.request.user.is_authenticated:
		#		return self.request.user.notes.all()

		return notes.objects.filter(privacy=False)

class mynotes(generic.ListView):
	model=notes
	context_object_name = 'note'
	template_name = 'notes/view.html'
	login_url="/login"

	def get_queryset(self):

		return self.request.user.notes_set.all().order_by('-date')

class search(generic.ListView):
	model=[notes,User]
	context_object_name = 'note'
	template_name = 'notes/view.html'
	
	def get_queryset(self):  # newnot
		choice= self.request.GET.get("c")
		if(choice=='w'):
			query = self.request.GET.get("q")
			object_list = notes.objects.filter(Q(title__icontains=query) & Q(privacy=False))
			if self.request.user.is_authenticated:
				user=self.request.user
				object_list |= notes.objects.filter(Q(privacy=True) & Q(title__icontains=query))
			return object_list.order_by('-date')
		else:
			query = self.request.GET.get("q")
			if(not User.objects.filter(username=query)):
				return 
			i=User.objects.get(username=query)
			object_list = notes.objects.filter(Q(user=i) & Q(privacy=False))
			if self.request.user.is_authenticated:
				object_list |= self.request.user.notes_set.filter(Q(user=i) & Q(privacy=True))
			return object_list.order_by('-date')

class detail_view(generic.DetailView):
	model=notes
	context_object_name = 'note'
	template_name = 'notes/detail_list.html'

@login_required(login_url="/login")
def comment(request, pk):
    post = notes.objects.get(pk=pk)
    user = request.user.username
    form = CommentForm()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comment(
            	author=user,
                body=form.cleaned_data["body"],
                post=post
            )
            comment.save()
            return HttpResponseRedirect('/%d/' % pk)

    comments = Comment.objects.filter(post=post)
    context = {
        "note": post, 	
        "comments": comments,
        "form": form,
    }
    return render(request, "notes/write.html", context)

@login_required(login_url="/login")
def grouping(request,pk):
	note=notes.objects.get(pk=pk)
	if(request.user in note.user.all()):
		users = request.POST.get("adduser")
		if users:
			users=User.objects.get(username=users).id
			note.user.add(users)
			note.save()
			return HttpResponseRedirect('/%d/' % pk)
	else:
		return HttpResponse("You are not allowed to share this note") 
	return render(request, "notes/adduser.html")

