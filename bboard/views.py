from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Min, Max, Count, Q, Sum, IntegerField, Avg
from django.forms import modelformset_factory, inlineformset_factory
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseNotFound, StreamingHttpResponse, FileResponse, \
    JsonResponse
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.template.loader import get_template, render_to_string
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, ListView, DetailView, FormView, UpdateView, DeleteView, \
    ArchiveIndexView, MonthArchiveView, RedirectView
from django.urls import reverse
from precise_bbcode.bbcode import get_parser

from bboard.forms import BbForm, SearchForm
from bboard.models import Bb, Rubric


def count_bb():
    result = dict()

    for r in Rubric.objects.annotate(num_bbs=Count('bb')):
        result.update({r.pk: r.num_bbs})

    return result


# @permission_required(('bboard.view_rubric', 'bboard.change_rubric'))
# @user_passes_test(lambda user: user.is_staff)
@login_required
def rubrics(request):
    RubricFormSet = modelformset_factory(Rubric, fields=('name',), can_delete=True, extra=3)

    if request.method == 'POST':
        formset = RubricFormSet(request.POST)
        if formset.is_valid():
            formset.save()

            return redirect('index')
    else:
        formset = RubricFormSet()

    context = {'formset': formset}

    return render(request, 'bboard/rubrics.html', context)


def bbs(request, rubric_id):
    bbsFormSet = inlineformset_factory(Rubric, Bb, form=BbForm, extra=1)
    rubric = Rubric.objects.get(pk=rubric_id)

    if request.method == 'POST':
        formset = bbsFormSet(request.POST, instance=rubric)
        if formset.is_valid():
            formset.save()

            return redirect('index')
    else:
        formset = bbsFormSet(instance=rubric)

    context = {'formset': formset, 'current_rubric': rubric}

    return render(request, 'bboard/bbs.html', context)


# class BbCreateView(LoginRequiredMixin, CreateView):
class BbCreateView(UserPassesTestMixin, CreateView):
    template_name = 'bboard/create.html'
    form_class = BbForm
    success_url = reverse_lazy('index')

    # Для UserPassesTestMixin
    def test_func(self):
        return self.request.user.is_staff
    # Конец


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.all()
        context['count_bb'] = count_bb()
        return context


class BbView(ListView):
    template_name = 'bboard/index.html'
    model = Bb
    paginate_by = 3

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
    parser = get_parser()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.all()
        context['bbs'] = get_list_or_404(Bb, rubric=context['bb'].rubric_id)
        context['count_bb'] = count_bb()
        # context['parsed_content'] = self.parser.render(self.object.content)

        return context


class BbRedirectView(RedirectView):
    url = '/detail/%(pk)d/'


class BbByRubricView(ListView):
    paginate_by = 2
    template_name = 'bboard/by_rubric.html'
    context_object_name = 'bbs'

    def get_queryset(self):
        # return Bb.objects.filter(rubric=self.kwargs['rubric_id'])
        return Bb.by_price.filter(rubric=self.kwargs['rubric_id'])

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
    }

    return HttpResponse(render_to_string('bboard/by_rubric.html', context, request))


def index(request, page=1):
    # rubrics = Rubric.objects.order_by_bb_count()
    rubrics = Rubric.objects.order_by_bb_count()
    bbs = Bb.objects.all()
    # bbs = Bb.by_price.all()
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
        # 'bbs': bbs,
        'bbs': bbs_paginator,
        'count_bb': count_bb(),
    }

    return HttpResponse(render_to_string('bboard/index.html', context, request))


def search(request):
    if request.method == 'POST':
        sf = SearchForm(request.POST)
        if sf.is_valid():
            keyword = sf.cleaned_data['keyword']
            rubric_id = sf.cleaned_data['rubric'].pk
            bbs = Bb.objects.filter(title__iregex=keyword, rubric=rubric_id)
            context = {
                'bbs': bbs,
                'form': sf,
            }
            return render(request, 'bboard/search_result.html', context)
    else:
        sf = SearchForm()

    context = {
        'form': sf,
    }
    return render(request, 'bboard/search.html', context)
