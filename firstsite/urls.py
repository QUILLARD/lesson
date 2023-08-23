from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('bboard.urls')),
    path('testapp/', include('testapp.urls', namespace='testapp')),
    path('auth/', include('authapp.urls', namespace='authapp')),

    path('accounts/login/', LoginView.as_view(next_page='index'), name='login'),
    path('accounts/logout/', LogoutView.as_view(), name='logout'),
    path('accounts/password_change/', PasswordChangeView.as_view(template_name='registration/change_password.html'),
         name='password_change'),
    path('accounts/password_change/done/',
         PasswordChangeDoneView.as_view(template_name='registration/password_changed.html'),
         name='change_password_done'),
]
