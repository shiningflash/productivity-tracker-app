from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('delete_todo/<int:pk>', views.delete_todo, name='delete-todo'),
    path('update_todo/<int:pk>', views.update_todo, name='update-todo'),
    path('submit_todo', views.submit_todo, name='submit-todo'),
    path('reset_todo', views.reset_todo, name='reset-todo'),

]
