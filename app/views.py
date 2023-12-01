from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .models import Idea
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .forms import IdeaForm



def home(request):
    
    ideas = Idea.objects.all() 
    form = IdeaForm()
    user = request.user

    for idea in ideas:
        idea.user_already_vote = idea.participants.filter(pk=user.pk).exists()

    context = {'ideas':ideas,'form':form}
    return render(request,'app/home.html',context)

@login_required(login_url='login')
def myIdeas(request):
    
    ideas = Idea.objects.filter(creator=request.user) 
    user = request.user

    for idea in ideas:
        idea.user_already_vote = idea.participants.filter(pk=user.pk).exists()

    context = {'ideas':ideas}
    return render(request,'app/my_ideas.html',context)



@login_required(login_url='login')
def createIdea(request):
    form = IdeaForm()
    if request.method == 'POST':
        form = IdeaForm(request.POST)
        if form.is_valid():
            idea = form.save(commit=False)
            idea.creator = request.user  
            idea.save()
            idea.participants.add(request.user)
            idea.update_votes()
            idea.save()
            return redirect('home')  

    return render(request, 'app/ideas/create_idea.html', {'form': form})

@login_required(login_url='login')
def voteIdea(request, pk):
    
    idea = get_object_or_404(Idea, id=pk)

    if request.user not in idea.participants.all():
        idea.participants.add(request.user)
        idea.update_votes()
        idea.save()

    return redirect('home')

@login_required(login_url='login')
def unvoteIdea(request, pk):
    idea = get_object_or_404(Idea, pk=pk)

    if request.user in idea.participants.all():
        idea.participants.remove(request.user)
        idea.update_votes()
        print(idea.votes)
        print(type(idea.votes))
        if idea.votes == 0:
            idea.delete()
            return redirect('home')
        idea.save()

    return redirect('home')



## USER LOGIN, REGISTER AND LOG OUT

def loginPage(request):
    page = "login"

    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request,"User doesnt exist!")

        user = authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,"User or password is wrong!")

    context = {'page': page}
    return render(request,'app/users/login_register.html',context)

def registerPage(request):
    page = "register"
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,"Error en la creación del usuario.")

    context = {'page':page,'form':form}
    return render(request,'app/users/login_register.html',context)

def logoutPage(request):
    logout(request)
    return redirect('home')