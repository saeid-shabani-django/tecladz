from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Customer

@receiver(post_save,sender=settings.AUTH_USER_MODEL,)
def create_customer_after_custom_user(sender,**kwargs):
    # created(boolean), instance(object)
    if kwargs['created']:
        Customer.objects.create(user=kwargs['instance'])