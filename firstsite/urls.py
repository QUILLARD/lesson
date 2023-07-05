from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('bboard.urls')),
    path('testapp/', include('testapp.urls', namespace='testapp')),
    path('auth/', include('authapp.urls', namespace='authapp')),
]
