from . import views
from django.urls import path

urlpatterns = [
    path('main',views.main,name='main'),

]
