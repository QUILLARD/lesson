from django.urls import path

from testapp.views import AddSms, ReadSms, add, edit, index, get

app_name = 'testapp'

urlpatterns = [
    path('addsms/', AddSms.as_view(), name='add_sms'),
    path('readsms/<int:pk>/', ReadSms.as_view(), name='read_sms'),
    path('add/', add, name='testapp_add'),
    path('edit/<int:pk>/', edit, name='edit'),
    path('', index, name='index'),
    path('get/<path:filename>/', get, name='get')
]
