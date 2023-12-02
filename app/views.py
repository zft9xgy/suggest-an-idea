from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .models import Idea, App
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .forms import IdeaForm, AppForm
from django.http import HttpResponseRedirect
from django.db.models import Q


def home(request):
    search = request.GET.get('search') if request.GET.get('search') != None else ''
    
    ideas = Idea.objects.filter(
        Q(title__icontains=search) |
        Q(description__icontains=search)
        )
    #ideas = Idea.objects.all() 
    form = IdeaForm()
    user = request.user

    for idea in ideas:
        idea.user_already_vote = idea.voters.filter(pk=user.pk).exists()

    context = {'ideas':ideas,'form':form}
    return render(request,'app/home.html',context)

def apps(request):

    apps = App.objects.all()
    form = AppForm()

    context = {'apps':apps,'form':form}
    return render(request,'app/apps.html',context)

@login_required(login_url='login')
def myIdeas(request):

    form = IdeaForm()
    created_ideas = Idea.objects.filter(creator=request.user)
    participated_ideas = Idea.objects.filter(voters=request.user)

    # Marcar si el usuario ya ha votado por cada idea
    for idea in participated_ideas:
        idea.user_already_vote = idea.voters.filter(pk=request.user.pk).exists()

    for idea in created_ideas:
        idea.user_already_vote = idea.voters.filter(pk=request.user.pk).exists()

    context = {
        'created_ideas': created_ideas,
        'participated_ideas': participated_ideas,
        'form': form,
    }

    return render(request, 'app/my_ideas.html', context)



@login_required(login_url='login')
def createIdea(request):
    form = IdeaForm()
    if request.method == 'POST':
        form = IdeaForm(request.POST)
        if form.is_valid():
            idea = form.save(commit=False)
            idea.creator = request.user  
            idea.save()
            idea.voters.add(request.user)
            idea.update_votes()
            idea.save()
            referer_url = request.META.get('HTTP_REFERER')
            return HttpResponseRedirect(referer_url or 'home')

    return render(request, 'app/ideas/create_idea.html', {'form': form})

@login_required(login_url='login')
def voteIdea(request, pk):
    
    idea = get_object_or_404(Idea, id=pk)
    referer_url = request.META.get('HTTP_REFERER')

    if request.user not in idea.voters.all():
        idea.voters.add(request.user)
        idea.update_votes()
        idea.save()

    return HttpResponseRedirect(referer_url or 'home')

@login_required(login_url='login')
def unvoteIdea(request, pk):
    idea = get_object_or_404(Idea, pk=pk)
    referer_url = request.META.get('HTTP_REFERER')

    if request.user in idea.voters.all():
        idea.voters.remove(request.user)
        idea.update_votes()
        print(idea.votes)
        print(type(idea.votes))
        if idea.votes == 0:
            idea.delete()
            return redirect('home')
        idea.save()

    return HttpResponseRedirect(referer_url or 'home')



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


# app CRUD

@login_required(login_url='login')
def createApp(request):
    form = AppForm()
    if request.method == 'POST':
        form = AppForm(request.POST)
        if form.is_valid():
            app = form.save(commit=False)
            app.creator = request.user  
            app.save()
            referer_url = request.META.get('HTTP_REFERER')
            return HttpResponseRedirect(referer_url or 'home')

    return render(request, 'app/components/apps_form.html', {'form': form})