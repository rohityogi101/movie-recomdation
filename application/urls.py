from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('movies/', views.movie, name='movies'),
    path('recom/<str:movie>/', views.recom, name='recom'),
    # path('try/',views.new,name='Hi')
]
