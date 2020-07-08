from django.urls import path

from . import views

app_name = 'my_app'
urlpatterns = [
    path('', views.index, name='index'),
    path('project/<int:project_id>/', views.project_detail, name='project'),
]
