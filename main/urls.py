from . import views
from django.urls import path

urlpatterns = [
    path('',views.main,name='main'),
    path('<str:pk>/new_post',views.PostCreateView.as_view(),name='new_post'),

]
