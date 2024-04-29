from django.contrib import admin

from .models import Vendor, PurchaseOrder, HistoricalPerformance


admin.site.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = (
        'code', 
        'quality_rating_avg', 
        'average_response_time', 
        'fulfillment_rate',
    )
    search_fields = ('name__istartswith', 'code',)
    list_filter = (
        'quality_rating_avg', 
        'average_response_time', 
        'fulfillment_rate',
    )
    readonly_fields = ('code',)


admin.site.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = (
        'po_number', 
        'order_date', 
        'delivery_date', 
        'status',
    )
    search_fields = ('po_number', 'vendor__name__istartswith')
    list_filter = ('status',)
    readonly_fields = ('po_number',)

admin.site.register(HistoricalPerformance)
class HistoricalPerformanceAdmin(admin.ModelAdmin):
    list_display = (
        'vendor', 
        'date', 
        'on_time_delivery_rate', 
        'quality_rating_avg', 
        'average_response_time', 
        'fulfillment_rate',
    )
    search_fields = ('vendor__name__istartswith')