from django.db.models import Min, Max, Count, Q, Sum, IntegerField, Avg
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseNotFound
from django.shortcuts import render
from django.template.loader import get_template, render_to_string
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.urls import reverse

from bboard.forms import BbForm
from bboard.models import Bb, Rubric


def print_request(request):
    for attr in dir(request):
        value = getattr(request, attr)
        print(attr, ":", value)


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


def index_resp(request):
    resp = HttpResponse('Здесь будет', content_type='text/plain; charset=utf-8')
    resp.write(' главная')
    resp.writelines((' страница', ' сайта'))
    resp['keywords'] = 'Python, Django'
    return resp


def index(request):
    bbs = Bb.objects.all()
    rubrics = Rubric.objects.all()
    context = {'bbs': bbs,
               'rubrics': rubrics}
    # template = get_template('bboard/index.html')
    # return HttpResponse(template.render(context=context, request=request))

    return HttpResponse(render_to_string('bboard/index.html', context=context, request=request))


def index_str(request):
    bbs = Bb.objects.all()
    rubrics = Rubric.objects.all()
    text = 'Строка на фронтенд'
    context = {'bbs': bbs,
               'rubrics': rubrics,
               'text': text}

    return HttpResponse(render_to_string('bboard/index.html', context=context, request=request))


def index_old(request):
    bbs = Bb.objects.order_by('-published')
    rubrics = Rubric.objects.all()

    # min_price = Bb.objects.aggregate(Min('price'))
    # max_price = Bb.objects.aggregate(mp=Max('price'))
    result = Bb.objects.aggregate(min_price=Min('price'),
                                  max_price=Max('price'),
                                  diff_price=Max('price') - Min('price'),)
    count__ = Rubric.objects.annotate(num_bbs=Count('bb'))

    # for r in Rubric.objects.annotate(Count('bb')):
    #     print(r.name, ': ', r.bb__count, sep='')

    # for r in Rubric.objects.annotate(cnt=Count('bb', filter=Q(bb__price__gt=100_000))):
    #                                  # min=Min('bb__price')).filter(cnt__gt=0):
    #     # print(r.name, ': ', r.min, sep='')
    #     print(r.name, ': ', r.cnt, sep='')

    # print(Bb.objects.aggregate(sum=Sum('price', output_field=IntegerField(), filter=Q(rubric__name='Бытовая техника'))))

    # print(Bb.objects.aggregate(avg=Avg('price', output_field=IntegerField(), filter=Q(rubric__name='Сельхозтехника'), distinct=False,)))

    context = {
        'bbs': bbs,
        'rubrics': rubrics,
        # 'min_price': min_price.get('price__min'),
        # 'max_price': max_price.get('mp'),
        'min_price': result.get('min_price'),
        'max_price': result.get('max_price'),
        'diff_price': result.get('diff_price'),
        'count__': count__,
        'count_bb': count_bb(),
    }
    return render(request, 'bboard/index.html', context)


def by_rubric(request, rubric_id, **kwargs):

    # print_request(request)

    try:
        rub_id = Rubric.objects.get(pk=rubric_id)

    except Rubric.DoesNotExist:
        return render(request, 'bboard/does_not_exist.html')

    bbs = Bb.objects.filter(rubric=rubric_id)
    rubrics = Rubric.objects.all()
    current_rubric = Rubric.objects.get(pk=rubric_id)
    count__ = Rubric.objects.annotate(num_bbs=Count('bb'))
    context = {
        'bbs': bbs,
        'rubrics': rubrics,
        'current_rubric': current_rubric,
        'count__': count__,
        'count_bb': count_bb(),
        'kwargs': kwargs,
    }
    return render(request, 'bboard/by_rubric.html', context)


def add(request):
    bbf = BbForm()
    context = {'form': bbf}

    return render(request, 'bboard/create.html', context)


def add_save(request):
    bbf = BbForm(request.POST)

    if bbf.is_valid():
        bbf.save()

        return HttpResponseRedirect(reverse('by_rubric', kwargs={'rubric_id': bbf.cleaned_data['rubric'].pk}))
    else:
        context = {'form': bbf}
        return render(request, 'bboard/create.html', context)


def add_and_save(request):
    if request.method == 'POST':

        bbf = BbForm(request.POST)
        if bbf.is_valid():
            bbf.save()

            return HttpResponseRedirect(reverse('by_rubric', kwargs={'rubric_id': bbf.cleaned_data['rubric'].pk}))

        else:
            context = {'form': bbf}
            return render(request, 'bboard/create.html', context)

    else:
        bbf = BbForm()
        context = {'form': bbf}
        return render(request, 'bboard/create.html', context)


def detail(request, rubric_id):
    try:
        bb = Bb.objects.get(pk=rubric_id)
    except Bb.DoesNotExist:
        return HttpResponseNotFound('Такого объявления не существует!')
    return HttpResponse(...)
