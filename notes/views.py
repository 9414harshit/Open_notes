from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from .models import notes,Comment,User
from .form import Notesform, CommentForm, SignUpForm
from django.contrib.auth.views import LogoutView,LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q # new
from datetime import datetime
from django.utils.timezone import now
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm


class LoginInterfaceView(LoginView):
	template_name ='notes/login.html'

class LogoutInterfaceView(LogoutView):
	template_name ='notes/logout.html'

class Signup(generic.edit.CreateView):
	form_class=SignUpForm
	template_name='notes/register.html'
	success_url='/login'

class update_notes(LoginRequiredMixin,generic.edit.UpdateView):
	model=notes
	success_url = "/"
	form_class = Notesform
	login_url="/login"

	def get_queryset(self):
		user=self.request.user
		return notes.objects.filter(user=user)

	def form_valid(self, form):
		self.object = form.save(commit=False)
		self.object.save()
		self.object.last = self.request.user.username
		self.object.save()
		form.save_m2m()
		messages.info(self.request, 'Successfully Edited by %s!' %self.request.user)
		return HttpResponseRedirect(self.get_success_url())


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
		self.object.last = self.request.user.username
		self.object.creator=self.request.user.username
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

		return notes.objects.filter(privacy=False).order_by('-date')

class deletenotes(LoginRequiredMixin,generic.DeleteView):
	model=notes
	context_object_name = 'note'
	template_name = 'notes/delete.html'
	success_url= '/'
	login_url="/login"

	def get_queryset(self):
		user=self.request.user
		return notes.objects.filter(creator=user)

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

	def get_queryset(self):
		object_list = notes.objects.filter(privacy=False)
		if self.request.user.is_authenticated:
			user=self.request.user
			object_list |= notes.objects.filter((Q(user=user) & Q(privacy=True)))

		return object_list.distinct()
		#return notes.objects.filter(privacy=False)

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
	if(request.user.username==note.creator):
		users = request.POST.get("adduser")
		if User.objects.filter(username=users):
			users=User.objects.get(username=users)
			note.user.add(users.id)
			note.save()
			messages.info(request, 'User "%s" was successfully added!' %users.username)
			return HttpResponseRedirect('/%d/' % pk)
	else:
		raise Http404(("You are not allowed to share this note"))
	return render(request, "notes/adduser.html")

@login_required(login_url="/login")
def removing(request,pk):
	note = notes.objects.get(pk=pk)
	if(request.user.username==note.creator):
		users = request.POST.get("adduser")
		if users == note.creator:
			messages.warning(request, 'Creator can not be removed!')
			return HttpResponseRedirect('/%d/' % pk)

		if User.objects.filter(username=users):
			users=User.objects.get(username=users)
			note.user.remove(users.id)
			note.save()
			messages.info(request, 'User "%s" was successfully removed!' %users.username)
			return HttpResponseRedirect('/%d/' % pk)
	else:
		raise Http404(("You are not allowed to remove users for this note"))
	return render(request, "notes/adduser.html")

@login_required(login_url="/login")
def remove_self(request,pk):
	note = notes.objects.get(pk=pk)
	if(request.user in note.user.all()):
		users = request.user.username
		if users == note.creator:
			return HttpResponse("Creator can not remove")
		if User.objects.filter(username=users):
			users=User.objects.get(username=users).id
			note.user.remove(users)
			note.save()
			return HttpResponseRedirect('/%d/' % pk)
	else:
		raise Http404(("You are not allowed to share this note"))
	return

def page_not_found_view(request, exception):
    return render(request, 'notes/404.html', status=404)

@login_required(login_url="/login")
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('/login')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'notes/change_password.html', {
        'form': form
    })