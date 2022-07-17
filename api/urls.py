from . import views
from django.urls import path

urlpatterns = [
    path('users',views.usersapi,name='usersapi'),
    path('post/create',views.PostCreateApiView.as_view(),name='post_create'),
    path('post/update/',views.PostUpdateApiView.as_view(),name='post_update'),
    path('posts',views.PostApiView.as_view(),name='posts'),
    path('posts/<int:pk>',views.PostDetailApiView.as_view(),name='post_detail'),
    path('follow/create/',views.FollowCreateApiView.as_view(),name='follow_create'),
    path('comment/create/',views.CommentCreateApiView.as_view(),name='comment_create'),
]