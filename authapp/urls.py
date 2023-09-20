from django.urls import path

from authapp.views import login, logout

app_name = 'authapp'

urlpatterns = [
    path('login/', login, name='auth_login'),
    path('logout/', logout, name='auth_logout'),
]
