from django.contrib import admin
from django.urls import path
from . import views

app_name = 'webapp'

urlpatterns = [
    path(r'',views.index,name='index'),
    path(r'my_blog/',views.myBlog,name='my_blog'),
    path(r'register/',views.register,name='register'),
    path(r'login/',views.login,name='login'),
    path(r'logout/',views.logout,name='logout'),
    path(r'add_blog/',views.addBlog,name='add_blog'),
    path(r'update_blog/<int:blog_id>/',views.updateBlog,name='update_blog'),
    path(r'delete_blog/<int:blog_id>/',views.deleteBlog,name='delete_blog'),
    path(r'csp/',views.csp,name='csp'),
    path(r'cloud_run/',views.make_authorized_get_request,name='cloud_run'),
    path(r'images/', views.download_image, name='download_image'),
    path('call_cloud_run/', views.make_authorized_get_request, name='make_authorized_get_request')
]
