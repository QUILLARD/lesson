from django.urls import path, re_path

from bboard.views import BbCreateView, BbByRubricView, BbView, BbDetailView, DetailViewBb, BbAddView, BbEditView, \
    BbDeleteView

vals = {'name': 'indexx', 'beaver': 'Бобер'}

# app_name = 'bboard'

urlpatterns = [
    path('', BbView.as_view(), name='index'),
    path('<int:rubric_id>/', BbByRubricView.as_view(), name='by_rubric'),
    path('read/<int:rec_id>/', BbDetailView.as_view(), name='read'),
    path('add/', BbAddView.as_view(), name='add'),
    path('detail/<int:pk>/', DetailViewBb.as_view(), name='detail'),
    path('update/<int:pk>/', BbEditView.as_view(), name='update'),
    path('delete/<int:pk>/', BbDeleteView.as_view(), name='delete'),
]

# urlpatterns = [
#     re_path(r'^$', index, name='index'),
#     re_path(r'^(?P<rubric_id>[0-9]*)/$', by_rubric, vals, name='by_rubric'),
#     re_path(r'^add/$', BbCreateView.as_view(), name='add'),
# ]
