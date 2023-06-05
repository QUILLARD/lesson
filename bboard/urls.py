from django.urls import path

from bboard.views import index, by_rubric, BbCreateView

vals = {'name': 'indexx', 'beaver': 'Бобер'}

urlpatterns = [
    path('', index, name='index'),
    path('<int:rubric_id>/', by_rubric, vals, name='by_rubric'),
    path('add/', BbCreateView.as_view(), name='add'),
]
