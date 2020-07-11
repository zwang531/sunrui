from django.urls import path

from . import views

app_name = 'sunrui'
urlpatterns = [
    path('', views.index, name='index'),
    path('birthday', views.birthday, name='birthday'),
]
