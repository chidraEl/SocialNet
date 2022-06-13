from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('profile/<str:username>', views.profile, name='profile'),
    path('settings/', views.settings, name='settings'),
    path('upload/', views.upload, name='upload'),
    path('like/', views.like_post, name='like'),
    path('follow/', views.follow, name='follow'),
    path('search/',views.search, name='search'),
    path('delete_post/', views.delete_post, name="delete_post")
]
