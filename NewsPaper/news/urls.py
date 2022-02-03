from django.urls import path
from .views import PostList, PostDetail, PostsSeach

urlpatterns = [
    path('', PostList.as_view()),
    path('<int:pk>', PostDetail.as_view()),
    path('search/', PostsSeach.as_view()),
]