from django.db import transaction
from django.shortcuts import render, redirect
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

# @transaction.non_atomic_requests
# def my_view(request):
#     pass
#
#
# @transaction.atomic
# def my_view(request):
#     with transaction.atomic():
#         pass
#     return redirect('index')
#
#
# def my_function():
#     transaction.set_autocommit(False)
#     try:
#         pass
#
#     except Exception:
#         transaction.rollback()
#
#     else:
#         transaction.commit()
#
#     finally:
#         transaction.set_autocommit(True)
#
#
# def my_controller():
#     if form.valid():
#         try:
#             form.save()
#             transaction.commit()
#         except:
#             transaction.rollback()
#
#
# def commit_handler():
#     pass
#     # После подтверждения транзакции
#
#
# def my_view():
#     for form in formset:
#         if form.cleaned_data:
#             sp = transaction.savepoint()
#             try:
#                 form.save()
#                 transaction.savepoint_commit(sp)
#             except:
#                 transaction.savepoint_rollback(sp)
#                 transaction.commit()
#             finally:
#                 transaction.on_commit(commit_handler)
