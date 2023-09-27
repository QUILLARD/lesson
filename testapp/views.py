import os
from datetime import datetime
from django.db import transaction
from django.http import FileResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, DeleteView, UpdateView
from django.contrib import messages
from firstsite.settings import BASE_DIR
from testapp.forms import SMSCreateForm, ImgForm
from testapp.models import SMS, Img

FILES_ROOT = os.path.join(BASE_DIR, 'files')


class AddSms(CreateView):
    template_name = 'testapp/create.html'
    form_class = SMSCreateForm
    success_url = reverse_lazy('index')


class ReadSms(DetailView):
    model = SMS
    template_name = 'testapp/read.html'


def index(request):
    imgs = []
    for entry in os.scandir(FILES_ROOT):
        imgs.append(os.path.basename(entry))
    context = {'imgs': imgs}
    return render(request, 'testapp/index.html', context)


def get(request, filename):
    fn = os.path.join(FILES_ROOT, filename)
    return FileResponse(open(fn, 'rb'), content_type='application/octet-stream')


def add(request):
    if request.method == 'POST':
        form = ImgForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['img']
            fn = '%s%s' % (datetime.now().timestamp(), os.path.splitext(uploaded_file.name)[1])
            fn = os.path.join(FILES_ROOT, fn)
            with open(fn, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)
                return redirect('testapp:index')
    else:
        form = ImgForm()
    context = {'form': form}
    return render(request, 'testapp/add.html', context)


def edit(request, pk):
    img = Img.objects.get(pk=pk)
    if request.method == 'POST':
        form = ImgForm(request.POST, request.FILES, instance=img)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Картинка изменена.', extra_tags='')
            # return redirect('index')

            msgs = messages.get_messages(request)
            print(msgs[0].message)
    else:
        form = ImgForm(instance=img)

    context = {
        'form': form,
        'img': img,
    }

    return render(request, 'testapp/edit.html', context)


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


def test_cookie(request):

    if request.session.test_cookie_worked():
        request.session.delete_test_cookie()
        print('COOKIES удалены!!!')
    else:
        print("Необходимо включить COOKIES")

    request.session.set_test_cookie()
    return render(request, 'testapp/test_cookie.html')
