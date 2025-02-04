# Generated by Django 5.0.4 on 2024-04-29 11:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('contact_details', models.TextField(help_text='Enter contact details of the vendor')),
                ('address', models.CharField(help_text='Enter the address of the vendor', max_length=100)),
                ('code', models.CharField(editable=False, max_length=20, unique=True)),
                ('on_time_delivery_rate', models.FloatField(blank=True, default=0.0, help_text='Percentage of purchase orders delivered on time')),
                ('quality_rating_avg', models.FloatField(blank=True, default=0.0, help_text='Quality rating based on purchase order')),
                ('average_response_time', models.FloatField(blank=True, default=0.0, help_text='Time taken to acknowledge the purchase order(in hours)')),
                ('fulfillment_rate', models.FloatField(blank=True, default=0.0, help_text='Percentage of purchase orders fulfilled on time')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='PurchaseOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('po_number', models.CharField(editable=False, max_length=20, unique=True)),
                ('order_date', models.DateTimeField(auto_now_add=True, help_text='Date when the purchase order was placed')),
                ('delivery_date', models.DateTimeField(help_text='Expected/Actual delivery date of the purchase order')),
                ('items', models.JSONField(blank=True, default=dict, help_text='Details of the items in the purchase order')),
                ('quantity', models.IntegerField(help_text='Total quantity of items in the purchase order')),
                ('status', models.CharField(choices=[('PENDING', 'Pending'), ('COMPLETED', 'Completed'), ('CANCELLED', 'Cancelled')], default='PENDING', max_length=20)),
                ('quality_rating', models.FloatField(blank=True, default=0.0, help_text='Quality rating given to the vendor for this purchase order')),
                ('issue_date', models.DateTimeField(auto_now_add=True, help_text='Date and Time when purchase order was issued to the vendor')),
                ('acknowledgment_date', models.DateTimeField(blank=True, help_text='Date and Time when the vendor acknowledged the purchase order', null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='VendorInfo.vendor')),
            ],
        ),
        migrations.CreateModel(
            name='HistoricalPerformance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(blank=True, help_text='Date of the performance record', null=True)),
                ('on_time_delivery_rate', models.FloatField(blank=True, default=0.0, help_text='Historical record of the on-time delivery rate')),
                ('quality_rating_avg', models.FloatField(blank=True, default=0.0, help_text='Historical record of the average quality rating')),
                ('average_response_time', models.FloatField(blank=True, default=0.0, help_text='Historical record of the average response time')),
                ('fulfillment_rate', models.FloatField(blank=True, default=0.0, help_text='Historical record of the fulfillment rate')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('vendor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='VendorInfo.vendor')),
            ],
        ),
    ]
