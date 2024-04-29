
from django.db.models import Prefetch
from django.utils import timezone
from django.db.models import F, Avg
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import (
    CreateModelMixin,
    RetrieveModelMixin,
    ListModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
)

from .models import Vendor, PurchaseOrder, HistoricalPerformance
from .serializers import VendorSerializer, PurchaseOrderSerializer

class VendorViewSet(
    GenericViewSet,
    CreateModelMixin,
    RetrieveModelMixin,
    ListModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
):
    #NOTE: Ideally `DestroyModelMixin` should'nt be used for Vendor because it's a sensitive operation. 
    #The better option is to use a custom action to deactivate the vendor.
    queryset = (
        Vendor.objects.all()
        .prefetch_related(
            Prefetch(
                'purchaseorder_set',
                queryset=PurchaseOrder.objects.all(),
                to_attr='purchase_orders',
            ),
        )
    )
    serializer_class = VendorSerializer
    lookup_field = 'code'


class PurchaseOrderViewSet(
    GenericViewSet,
    CreateModelMixin,
    RetrieveModelMixin,
    ListModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
):
    #NOTE: Ideally `DestroyModelMixin` should'nt be used for Purchase order because it's a sensitive operation. 
    #The better option is to use a custom action to deactivate the vendor.
    queryset = (
        PurchaseOrder.objects.all()
        .select_related('vendor')
    )
    serializer_class = PurchaseOrderSerializer
    lookup_field = 'po_number'


class VenderPerformanceViewSet(GenericViewSet):
    @action(methods=['get'], detail=False, url_path='(<code>)/performance')
    def performance(self, request, *args, **kwargs):
        vendor = Vendor.objects.filter(
            code=kwargs.get('code'),
        ).prefetch_related(
            Prefetch(
                'purchaseorder_set',
                queryset=PurchaseOrder.objects.filter(status='COMPLETED'),
                to_attr='completed_purchase_orders',
            ),
            Prefetch(
                'historicalperformance_set',
                queryset=HistoricalPerformance.objects.all(),
                to_attr='historical_performance_records',
            )
        )

        if not (vendor.completed_purchase_orders or vendor.historical_performance_records):
            return Response(
                dict(message='Vendor details not found'),
                    status=HTTP_404_NOT_FOUND,
                )

        avg_quality_rating = vendor.historical_performance_records.filter(
            quality_rating_avg__isnull=False
        ).aggregate(
            avg_quality_rating=Avg('quality_rating_avg')
        )['avg_quality_rating']

        avg_response_time = vendor.historical_performance_records.filter(
            average_response_time__isnull=False
        ).aggregate(
            time_diff_btwn=(
                F('vendor__purchaseorder__acknowledgment_date') - F('vendor__purchaseorder__issue_date')
            ),
            avg_response_time=Avg('time_diff_btwn')
        )['avg_response_time']

        fulfillment_rate = vendor.completed_purchase_orders.filter(
            fulfillment_rate__isnull=False
        ).aggregate(
            fulfillment_rate=Avg('fulfillment_rate')
        )['fulfillment_rate']
                
        return Response(
            dict(
                quality_rating_avg=avg_quality_rating,
                average_response_time=avg_response_time,
                fulfillment_rate=fulfillment_rate,
            ),
            status=HTTP_200_OK,
        )
    
    @action(methods=['post'], detail=False, url_path='(<po_number>)/acknowledgment')
    def acknowledgment(self, request, *args, **kwargs):
        purchase_order = PurchaseOrder.objects.filter(
            po_number=kwargs.get('po_number'),
        ).update(
            acknowledgment_date=timezone.now(),
        )

        if not purchase_order:
            return Response(
                dict(message='Purchase order not found'),
                status=HTTP_404_NOT_FOUND,
            )

        return Response(
            dict(message='Purchase order acknowledged successfully'),
            status=HTTP_200_OK,
        )