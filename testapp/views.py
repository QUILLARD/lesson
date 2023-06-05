from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, DeleteView, UpdateView

from testapp.forms import SMSCreateForm
from testapp.models import SMS


class AddSms(CreateView):
    template_name = 'testapp/create.html'
    form_class = SMSCreateForm
    success_url = reverse_lazy('index')


class ReadSms(DetailView):
    model = SMS
    template_name = 'testapp/read.html'



