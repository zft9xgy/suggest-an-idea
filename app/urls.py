from django.urls import path
from .views import main_views

urlpatterns = [
    path('',main_views.home,name='home'),
    path('apps',main_views.apps,name='apps'),
    path('my-ideas/',main_views.myIdeas,name='my-ideas'),
    path('new-idea/',main_views.createIdea,name='new-idea'),
    path('new-app/',main_views.createApp,name='new-app'),
    path('login/',main_views.loginPage,name='login'),
    path('register/',main_views.registerPage,name='register'),
    path('logout/',main_views.logoutPage,name='logout'),
    path('vote-idea/<int:pk>/',main_views.voteIdea,name='vote-idea'),
    path('unvote-idea/<int:pk>/',main_views.unvoteIdea,name='unvote-idea'),
    path('unvote-idea/<int:pk>/',main_views.unvoteIdea,name='unvote-idea'),
]
