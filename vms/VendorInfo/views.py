from django.db.models import Prefetch
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK, 
    HTTP_404_NOT_FOUND, 
    HTTP_400_BAD_REQUEST
)
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
    permission_classes = [IsAuthenticated]
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
    permission_classes = [IsAuthenticated]
    #NOTE: Ideally `DestroyModelMixin` should'nt be used for Purchase order because it's a sensitive operation. 
    #The better option is to use a custom action to deactivate the vendor.
    queryset = (
        PurchaseOrder.objects.all()
        .select_related('vendor')
    )
    serializer_class = PurchaseOrderSerializer
    lookup_field = 'po_number'


class VenderPerformanceViewSet(GenericViewSet):
    permission_classes = [IsAuthenticated]
    @action(methods=['get'], detail=False, url_path=r'(?P<code>.+)/performance')
    def performance(self, request, *args, **kwargs):
        vendor = Vendor.objects.filter(
            code=kwargs.get('code'),
        ).prefetch_related(
            Prefetch(
                'purchaseorder_set',
                queryset=PurchaseOrder.objects.all(),
                to_attr='purchase_orders',
            ),
            Prefetch(
                'historicalperformance_set',
                queryset=HistoricalPerformance.objects.all(),
                to_attr='historical_performance_records',
            )
        ).first()

        if not vendor:
            return Response(
                dict(message='Vendor not found'),
                status=HTTP_404_NOT_FOUND,
            )
         
        total_purchase_orders = len(vendor.purchase_orders)

        if not (vendor.historical_performance_records or vendor.purchase_orders):
            return Response(
                dict(
                    on_time_delivery_rate=0,
                    quality_rating_avg=0,
                    average_response_time=0,
                    fulfillment_rate=0,
                ),
                status=HTTP_200_OK,
            )

        on_time_delivery_rate = [
            record.on_time_delivery_rate for record in vendor.historical_performance_records
            if record.on_time_delivery_rate
        ]
        if not on_time_delivery_rate:
            on_time_delivery_rate = 0
        else:
            on_time_delivery_rate = sum(on_time_delivery_rate) / len(on_time_delivery_rate)

        avg_quality_rating = [
            record.quality_rating_avg for record in vendor.historical_performance_records
            if record.quality_rating_avg
        ]
        if not avg_quality_rating:
            avg_quality_rating = 0
        else:
            avg_quality_rating = sum(avg_quality_rating) / len(avg_quality_rating)

        avg_response_time = [
            record.average_response_time for record in vendor.historical_performance_records
            if record.average_response_time
        ]
        if not avg_response_time:
            avg_response_time = 0
        else:
            avg_response_time = [
                record.average_response_time for record in vendor.historical_performance_records
                if record.average_response_time
                ]
            avg_response_time = sum(avg_response_time) / len(avg_response_time)

        completed_po = [
            po for po in vendor.purchase_orders if 
            po.status == 'COMPLETED' and 
            po.fulfillment_rate
        ]
        fulfillment_rate = sum([po.fulfillment_rate for po in completed_po]) / len(completed_po)
        fulfillment_rate = fulfillment_rate if fulfillment_rate else 0
        fulfillment_rate = fulfillment_rate / total_purchase_orders
                
        return Response(
            dict(
                on_time_delivery_rate=on_time_delivery_rate,
                quality_rating_avg=avg_quality_rating,
                average_response_time=avg_response_time,
                fulfillment_rate=fulfillment_rate,
            ),
            status=HTTP_200_OK,
        )

    @action(methods=['patch'], detail=False, url_path=r'(?P<po_number>.+)/acknowledgement')
    def acknowledgement(self, request, *args, **kwargs):
        acknowledged = request.data.get('acknowledged')
        if not acknowledged:
            return Response(
                dict(message='Cannot undo acknowledge purchase order'),
                status=HTTP_400_BAD_REQUEST,
            )
        try:
            purchase_order = PurchaseOrder.objects.get(po_number=kwargs.get('po_number'))
        except PurchaseOrder.DoesNotExist:
            return Response(
                {'message': 'Purchase order does not exist'},
                status=HTTP_400_BAD_REQUEST,
            )
        if not purchase_order.acknowledgment_date:
            purchase_order.acknowledgment_date = timezone.now()
            purchase_order.save()
            return Response(
                dict(message='Purchase order acknowledged successfully'),
                status=HTTP_200_OK,
            )
        return Response(
            dict(message='Purchase order already acknowledged'),
            status=HTTP_200_OK,
        )