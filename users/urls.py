from . import views
from django.urls import path

urlpatterns = [
    path('login/',views.thelogin,name='login'),
    path('register/',views.register,name='register'),  
    path('logout/',views.logout_user, name='logout'),
]
