from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save)
def post_save_dispatcher(*args, **kwargs):
    print("Объявление создано!")

