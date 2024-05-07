from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from .models import *
from .serializers import *


class Vendors(generics.GenericAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

    def get(self, request, *args, **kwargs):
        vendors = self.get_queryset()
        serializer = self.get_serializer(vendors, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

Vendors = Vendors.as_view()


class VendorID(generics.GenericAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorDetailSerializer
    lookup_field = 'vendor_code'

    def get(self, request, *args, **kwargs):
        vendor = self.get_object()
        serializer = self.get_serializer(vendor)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        vendor = self.get_object()
        serializer = self.get_serializer(vendor, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        vendor = self.get_object()
        vendor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

VendorID = VendorID.as_view()


class PurchaseOrders(generics.GenericAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        vendor_id = request.query_params.get('vendor_id')
        if vendor_id:
            queryset = queryset.filter(vendor_id=vendor_id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

PurchaseOrders = PurchaseOrders.as_view()


class PurchaseOrderID(generics.GenericAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderDetailSerializer
    lookup_field = 'po_number'

    def get(self, request, *args, **kwargs):
        purchase_order = self.get_object()
        serializer = self.get_serializer(purchase_order)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        purchase_order = self.get_object()
        serializer = self.get_serializer(purchase_order, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        purchase_order = self.get_object()
        purchase_order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

PurchaseOrderID = PurchaseOrderID.as_view()


class VendorPerformance(generics.GenericAPIView):
    queryset = HistoricalPerformance.objects.all()
    serializer_class = VendorPerformanceSerializer

    def get(self, request, *args, **kwargs):
        vendor_id = self.kwargs.get('vendor_id')
        performances = self.queryset.filter(vendor_id=vendor_id)
        serializer = self.get_serializer(performances, many=True)
        return Response(serializer.data)

VendorPerformance = VendorPerformance.as_view()


class AcknowledgePurchaseOrder(generics.UpdateAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = AcknowledgePurchaseOrderSerializer
    lookup_field = 'po_number'

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

AcknowledgePurchaseOrder = AcknowledgePurchaseOrder.as_view()
