from rest_framework import routers

from .views import VendorViewSet, PurchaseOrderViewSet, VenderPerformanceViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register('vendor', VendorViewSet)
router.register('vendor-purchase-order', PurchaseOrderViewSet)   
router.register('vendor-performance', VenderPerformanceViewSet, basename='vendor-performance')

urlpatterns = router.urls