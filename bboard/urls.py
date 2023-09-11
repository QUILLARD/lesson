from django.urls import path, re_path
from django.views.generic import WeekArchiveView

from bboard.models import Bb
from bboard.views import BbCreateView, BbByRubricView, BbView, BbDetailView, BbAddView, BbEditView, \
    BbDeleteView, BbIndexView, BbMonthArchiveView, BbReadView, BbRedirectView, by_rubric, rubrics, bbs, search, index

vals = {'name': 'indexx', 'beaver': 'Бобер'}

# app_name = 'bboard'

urlpatterns = [
    # path('', BbView.as_view(), name='index'),
    # path('', BbIndexView.as_view(), name='index'),
    path('', index, name='index'),
    path('page/<int:page>/', index, name='page'),
    # path('<int:rubric_id>/', BbByRubricView.as_view(), name='by_rubric'),
    path('<int:rubric_id>/', BbByRubricView.as_view(), name='by_rubric'),
    path('<int:rubric_id>/page/<int:page>/', BbByRubricView.as_view(), name='rubric_page'),
    # path('<int:rubric_id>/', by_rubric, name='by_rubric'),
    path('read/<int:rec_id>/', BbReadView.as_view(), name='read'),
    path('add/', BbCreateView.as_view(), name='add'),
    path('detail/<int:pk>/', BbDetailView.as_view(), name='detail'),
    path('update/<int:pk>/', BbEditView.as_view(), name='update'),
    path('delete/<int:pk>/', BbDeleteView.as_view(), name='delete'),
    path('<int:year>/<int:month>/', BbMonthArchiveView.as_view()),
    path('<int:year>/week/<int:week>/', WeekArchiveView.as_view(model=Bb, date_field='published')),
    path('detail/<int:year>/<int:month>/<int:day>/<int:pk>/', BbRedirectView.as_view(), name='old_detail'),
    path('rubrics/', rubrics, name='rubrics'),
    path('bbs/<int:rubric_id>/', bbs, name='bbs'),
    path('search/', search, name='search'),
]

# urlpatterns = [
#     re_path(r'^$', index, name='index'),
#     re_path(r'^(?P<rubric_id>[0-9]*)/$', by_rubric, vals, name='by_rubric'),
#     re_path(r'^add/$', BbCreateView.as_view(), name='add'),
# ]
