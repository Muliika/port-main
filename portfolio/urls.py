from django.urls import path
from . import views


app_name = 'portfolio'

urlpatterns = [
    path('', views.home, name='homepage'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('<slug:post>/', views.post_single, name='post_single'),
    path('category/<category>/', views.CatListView.as_view(), name='category'),
    path('post/tag/<slug:tag_slug>/', views.tags_list, name='tags'),
    path('search/', views.search_view, name='search'),
]

