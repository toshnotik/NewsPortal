from django.urls import path
from .views import PostList, PostDetail, PostSearch, PostEdit, PostAdd, PostDelete, CategoriesList

urlpatterns = [
    path('', PostList.as_view()),
    path('<int:pk>', PostDetail.as_view(), name='post'),
    path('search/', PostSearch.as_view(), name='search'),
    path('add/', PostAdd.as_view(), name='add'),
    path('edit/<int:pk>', PostEdit.as_view(), name='edit'),
    path('delete/<int:pk>', PostDelete.as_view(), name='delete'),
    path('category/', CategoriesList.as_view(), name='categories'),

]