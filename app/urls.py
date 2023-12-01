from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('my-ideas/',views.myIdeas,name='my-ideas'),
    path('new-idea/',views.createIdea,name='new-idea'),
    path('login/',views.loginPage,name='login'),
    path('register/',views.registerPage,name='register'),
    path('logout/',views.logoutPage,name='logout'),
    path('vote-idea/<int:pk>/',views.voteIdea,name='vote-idea'),
    path('unvote-idea/<int:pk>/',views.unvoteIdea,name='unvote-idea'),
    path('unvote-idea/<int:pk>/',views.unvoteIdea,name='unvote-idea'),
]
