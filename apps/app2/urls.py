from django.urls import path
from . import views

urlpatterns = [
    path('', views.show_wall),
    path('/postmessage', views.postmessage),
    path('/comment', views.makecomment),
    path('/delete_message', views.delete_message),
    path('/delete_comment', views.delete_comment),
]