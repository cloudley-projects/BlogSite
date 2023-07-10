from django.contrib import admin
from django.urls import path
from . import views

app_name = 'webapp'

urlpatterns = [
    path(r'',views.index,name='index'),
    path(r'create_task',views.create_task,name='create_task'),
    path(r'process_task',views.task_handler,name='task_handler'),
    path(r'create_task_cf',views.create_task_cf,name='create_task_cf'),
    path(r'wait_time',views.wait_time,name='wait_time'),
]
