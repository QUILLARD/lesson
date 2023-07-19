from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Min, Max, Count, Q, Sum, IntegerField, Avg
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseNotFound, StreamingHttpResponse, FileResponse, \
    JsonResponse
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.template.loader import get_template, render_to_string
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, ListView, DetailView, FormView, UpdateView, DeleteView, \
    ArchiveIndexView, MonthArchiveView, RedirectView
from django.urls import reverse

from bboard.forms import BbForm
from bboard.models import Bb, Rubric


def count_bb():
    result = dict()

    for r in Rubric.objects.annotate(num_bbs=Count('bb')):
        result.update({r.pk: r.num_bbs})

    return result


class BbCreateView(CreateView):
    template_name = 'bboard/create.html'
    form_class = BbForm
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.all()
        context['count_bb'] = count_bb()
        return context


class BbView(ListView):
    template_name = 'bboard/index.html'
    model = Bb

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bbs'] = Bb.objects.all()
        context['rubrics'] = Rubric.objects.all()
        context['count_bb'] = count_bb()

        return context


# class BbByRubricView(TemplateView):
#     template_name = 'bboard/by_rubric.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['current_rubric'] = Rubric.objects.get(pk=context['rubric_id'])
#         context['bbs'] = Bb.objects.filter(rubric=context['rubric_id'])
#         context['rubrics'] = Rubric.objects.all()
#         context['count_bb'] = count_bb()
#
#         return context


class BbReadView(TemplateView):
    template_name = 'bboard/detail.html'
    model = Bb

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bb'] = get_object_or_404(Bb, pk=context['rec_id'])
        context['bbs'] = get_list_or_404(Bb, rubric=context['bb'].rubric_id)
        context['count_bb'] = count_bb()

        return context


class BbDetailView(DetailView):
    model = Bb

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.all()
        context['bbs'] = get_list_or_404(Bb, rubric=context['bb'].rubric_id)
        context['count_bb'] = count_bb()

        return context


class BbRedirectView(RedirectView):
    url = '/detail/%(pk)d/'


class BbByRubricView(ListView):
    paginate_by = 1
    template_name = 'bboard/by_rubric.html'
    context_object_name = 'bbs'

    def get_queryset(self):
        return Bb.objects.filter(rubric=self.kwargs['rubric_id'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.all()
        context['current_rubric'] = Rubric.objects.get(pk=self.kwargs['rubric_id'])
        context['count_bb'] = count_bb()

        return context


class BbAddView(FormView):
    template_name = 'bboard/create.html'
    form_class = BbForm
    initial = {'price': 0.0}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.all()
        context['count_bb'] = count_bb()

        return context

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_form(self, form_class=None):
        self.object = super().get_form(form_class)
        return self.object

    def get_success_url(self):
        return reverse('by_rubric', kwargs={'rubric_id': self.object.cleaned_data['rubric'].pk})


class BbEditView(UpdateView):
    model = Bb
    form_class = BbForm
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.all()
        context['count_bb'] = count_bb()

        return context


class BbDeleteView(DeleteView):
    model = Bb
    success_url = reverse_lazy('index')


class BbIndexView(ArchiveIndexView):
    model = Bb
    date_field = 'published'
    date_list_period = 'year'
    template_name = 'bboard/index.html'
    context_object_name = 'bbs'
    allow_empty = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.all()
        context['count_bb'] = count_bb()

        return context


class BbMonthArchiveView(MonthArchiveView):
    model = Bb
    date_field = 'published'
    month_format = '%m'
    context_object_name = 'bbs'
    # template_name = 'bboard/index.html'


def index(request):
    rubrics = Rubric.objects.all()
    bbs = Bb.objects.all()
    paginator = Paginator(bbs, 4)

    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1

    page = paginator.get_page(page_num)

    context = {
        'rubrics': rubrics,
        'bbs': page.object_list,
        'page': page,
        'count_bb': count_bb(),
    }

    return HttpResponse(render_to_string('bboard/index.html', context, request))


def by_rubric(request, rubric_id):
    rubrics = Rubric.objects.all()
    bbs = Bb.objects.filter(rubric=rubric_id)
    paginator = Paginator(bbs, 1)

    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1

    page = paginator.get_page(page_num)

    context = {
        'rubrics': rubrics,
        'bbs': page.object_list,
        'page': page,
        'count_bb': count_bb(),
    }

    return HttpResponse(render_to_string('bboard/by_rubric.html', context, request))


def index(request, page=1):
    rubrics = Rubric.objects.all()
    bbs = Bb.objects.all()
    paginator = Paginator(bbs, 2)

    try:
        bbs_paginator = paginator.get_page(page)

    except EmptyPage:
        bbs_paginator = paginator.get_page(paginator.num_pages)
    except PageNotAnInteger:
        bbs_paginator = paginator.get_page(1)

    context = {
        'rubrics': rubrics,
        'page': page,
        'bbs': bbs_paginator,
    }

    return HttpResponse(render_to_string('bboard/index.html', context, request))
