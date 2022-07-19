from . import views
from django.urls import path

urlpatterns = [
    path('',views.main,name='main'),
    path('<int:pk>/new_post',views.PostCreateView.as_view(),name='new_post'),
    path('anonymous_user/new_post', views.no_user_new_post,name='no_user_new_post'),
    path('<int:pk>/profile',views.profile,name='profile'),
    path('<int:pk>/edit_profile',views.ProfileUpdateView.as_view(),name='edit_profile'),
    path('anonymous_user/profile',views.no_user_profile,name='no_user_profile'),
    path('search/',views.search,name='search')
]
