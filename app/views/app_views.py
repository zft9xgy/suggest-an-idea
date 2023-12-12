from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from app.models import Idea, App
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from app.forms import IdeaForm, AppForm
from django.http import HttpResponseRedirect
from django.db.models import Q


def apps(request):

    apps = App.objects.all()
    form = AppForm()

    context = {'apps':apps,'form':form}
    return render(request,'app/apps/apps.html',context)