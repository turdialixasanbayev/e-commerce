from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Product
from user.hashid import encode_id


@receiver(post_save, sender=Product)
def generate_product_slug(sender, instance, created, **kwargs):
    """
    Signal to set the slug of a Product after it is created.
    """
    if created and not instance.slug:
        instance.slug = encode_id(instance.pk)
        instance.save(update_fields=['slug'])
