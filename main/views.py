from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from .forms import *
# Create your views here.

def tutorial_series(request,pk):

	objs=TutorialSeries.objects.all()
	obj1=objs.filter(tutorial_category__tutorial_category=pk)
	print('printing',obj1)
	content={'series':obj1}
	return render(request,"category.html",content)
def tutorials(request,pk1):
	print('pk1=',pk1)
	objs=Tutorial.objects.all()
	print('hello hello',objs)
	this_tutorial = objs.filter(tutorial_slug=pk1)

	tutorials_from_series = objs.filter(tutorial_series__tutorial_series=pk1).order_by('tutorial_published')
	print('filtered tutorial series',tutorials_from_series)
	this_tutorial_idx = list(tutorials_from_series).index(this_tutorial)
	content={'tutorial':this_tutorial,'sidebar':tutorials_from_series,"this_tut_idx": this_tutorial_idx}
	return render(request,"tutorial.html",content)


def homepage(request):
	return render(request=request,template_name="categories.html",context={"categories":TutorialCategory.objects.all})

def register(request):
	form = CreateUserForm()
	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password1')
			role = form.cleaned_data.get('role')
			print("username=",username,"password=",password,"role=",role)
			
			

			messages.success(request, 'Account was created for ' + username)

			return redirect('loginemp')
		

	context = {'form':form}
	return render(request, 'register.html', context)

def logout_request(request):
	logout(request)
	messages.info(request,"logged out sucessfully...")
	return redirect("loginemp")
def login_request(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password =request.POST.get('password')

		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			return redirect('homepage')
		else:
			messages.info(request, 'Username OR password is incorrect')

	context = {}
	return render(request, 'login.html', context)
def tutorial_sample(request):
	if(request.method=='POST'):
		tutorial_category=request.POST["tutorial_category"]
		category_summary=request.POST["category_summary"]
		category_slug=request.POST["category_slug"]
		obj=TutorialCategory.objects.create(tutorial_category=tutorial_category,category_summary=category_summary,category_slug=category_slug)
		obj.save()
		return HttpResponse("Success")
	else:
		return render(request,'tutorial_sample.html')
