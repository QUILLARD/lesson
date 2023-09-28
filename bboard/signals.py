from django.db.models.signals import post_save
from django.dispatch import receiver, Signal

from bboard.models import Bb

add_bb = Signal()


@receiver(post_save, sender=Bb)
def post_save_dispatcher(created, *args, **kwargs):
    instance = kwargs['instance']
    if created:
        print(f"Объявление {instance.title} создано!")
    else:
        print(f'Объявление {instance.title} изменено!')


def add_bb_dispatcher(sender, **kwargs):
    print(f"Объявление в рубрике {sender.rubric} с ценой {sender.price}")


add_bb.connect(add_bb_dispatcher)
