from django.urls import path
from login import views as login_views

urlpatterns = [
    path('', login_views.index),
    path('login/', login_views.login),
    path('signin/', login_views.signin)
]
