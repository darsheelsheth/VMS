from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save

from .models import Vendor

@receiver(post_save, sender=Vendor)
def create_vendor_code(sender, instance, created, **kwargs):
    if (
        instance.on_time_delivery_rate or 
        instance.quality_rating_avg or 
        instance.average_response_time or 
        instance.fulfillment_rate
    ):
        instance.hisoricalperformance_set.create(
            date=timezone.now(),
            on_time_delivery_rate=instance.on_time_delivery_rate,
            quality_rating_avg=instance.quality_rating_avg,
            average_response_time=instance.average_response_time,
            fulfillment_rate=instance.fulfillment_rate,
        )