from . import views
from django.urls import path

urlpatterns = [
    path('',views.main,name='main'),
    path('<int:pk>/new_post',views.PostCreateView.as_view(),name='new_post'),
    path('<int:pk>/profile',views.profile,name='profile'),
    path('<int:pk>/edit_profile',views.ProfileUpdateView.as_view(),name='edit_profile'),

]