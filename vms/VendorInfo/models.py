from django.db import models

from .utils import generate_random_identifier

# Create your models here.

class Vendor(models.Model):
    name = models.CharField(max_length=100)
    contact_details = models.TextField(
        help_text='Enter contact details of the vendor'
    )
    address = models.CharField(
        max_length=100, 
        help_text='Enter the address of the vendor'
    )
    code = models.CharField(
        max_length=20, 
        unique=True, 
        editable=False
    )
    on_time_delivery_rate = models.FloatField(
        default=0.0, 
        blank=True, 
        help_text='Percentage of purchase orders delivered on time'
    )
    quality_rating_avg = models.FloatField(
        default=0.0, 
        blank=True, 
        help_text='Quality rating based on purchase order'
    )
    average_response_time = models.FloatField(
        default=0.0, 
        blank=True, 
        help_text='Time taken to acknowledge the purchase order(in hours)'
    )
    fulfillment_rate = models.FloatField(
        default=0.0, 
        blank=True, 
        help_text='Percentage of purchase orders fulfilled on time'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name} - {self.id}'
    
    def save(self, *args, **kwargs):
        if not self.code:
            code = generate_random_identifier('code')
            while Vendor.objects.filter(code=code).exists():
                code = generate_random_identifier('code')
            self.code = code
        super().save(*args, **kwargs)


class PurchaseOrder(models.Model):
    class PoStatus(models.TextChoices):
        PENDING = 'PENDING'
        COMPLETED = 'COMPLETED'
        CANCELLED = 'CANCELLED'

    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    po_number = models.CharField(
        max_length=20, 
        unique=True, 
        editable=False
    )
    order_date = models.DateTimeField(
        auto_now_add=True, 
        help_text='Date when the purchase order was placed'
    )
    delivery_date = models.DateTimeField(
        help_text='Expected/Actual delivery date of the purchase order'
    )
    items = models.JSONField(
        default=dict, 
        blank=True,
        help_text='Details of the items in the purchase order'
    )
    quantity = models.IntegerField(
        help_text='Total quantity of items in the purchase order'
    )
    status = models.CharField(
        max_length=20, 
        choices=PoStatus.choices, 
        default=PoStatus.PENDING
    )
    quality_rating = models.FloatField(
        default=0.0, 
        blank=True,
        help_text='Quality rating given to the vendor for this purchase order'
    )
    issue_date = models.DateTimeField(
        auto_now_add=True,
        help_text='Date and Time when purchase order was issued to the vendor'
    )
    acknowledgment_date = models.DateTimeField(
        null=True, 
        blank=True,
        help_text='Date and Time when the vendor acknowledged the purchase order'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.po_number} - {self.vendor.name}'
    
    def save(self, *args, **kwargs):
        if not self.po_number:
            code = generate_random_identifier('po_number')
            while PurchaseOrder.objects.filter(po_number=code).exists():
                code = generate_random_identifier('po_number')
            self.po_number = code
        super().save(*args, **kwargs)


class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField(
        blank=True,
        null=True,
        help_text='Date of the performance record'
    )
    on_time_delivery_rate = models.FloatField(
        default=0.0, 
        blank=True,
        help_text='Historical record of the on-time delivery rate'
    )
    quality_rating_avg = models.FloatField(
        default=0.0, 
        blank=True,
        help_text='Historical record of the average quality rating'
    )
    average_response_time = models.FloatField(
        default=0.0, 
        blank=True,
        help_text='Historical record of the average response time'
    )
    fulfillment_rate = models.FloatField(
        default=0.0, 
        blank=True,
        help_text='Historical record of the fulfillment rate'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.vendor.name} - {self.date}'