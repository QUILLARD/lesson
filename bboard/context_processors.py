from django.contrib.auth.models import Group, User

from bboard.models import Rubric
from bboard.views import count_bb


def rubrics(request):
    context = {
        'rubrics': Rubric.objects.all(),
        'count_bb': count_bb(),
        'all_groups': Group.objects.all(),
        'all_users': User.objects.all(),
        'test': dir(Group.objects.all().first()),
    }
    return context

