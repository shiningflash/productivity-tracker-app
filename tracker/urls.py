from django.conf import settings, urls
from django.conf.urls import url
from django.conf.urls.static import static
from django.urls import path
from django.views.static import serve

from . import views

urlpatterns = [
    url(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}), 
    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
    
    path('', views.home, name='home'),
    path('delete_todo/<int:pk>', views.delete_todo, name='delete-todo'),
    path('update_todo/<int:pk>', views.update_todo, name='update-todo'),
    path('submit_todo', views.submit_todo, name='submit-todo'),
    path('reset_todo', views.reset_todo, name='reset-todo'),

]
