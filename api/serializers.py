from rest_framework import serializers
from .models import *

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ['vendor_code', 'name', 'contact_details', 'address', 'on_time_delivery_rate', 'quality_rating_avg', 'average_response_time', 'fulfillment_rate']

    def create(self, validated_data):
        return Vendor.objects.create(**validated_data)


class VendorDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ['vendor_code', 'name', 'contact_details', 'address', 'on_time_delivery_rate', 'quality_rating_avg', 'average_response_time', 'fulfillment_rate']
        read_only_fields = ['vendor_code', 'on_time_delivery_rate', 'quality_rating_avg', 'average_response_time', 'fulfillment_rate']


class PurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = ['po_number', 'vendor', 'order_date', 'delivery_date', 'items', 'quantity', 'status', 'quality_rating', 'issue_date', 'acknowledgment_date']


class PurchaseOrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = ['po_number', 'vendor', 'order_date', 'delivery_date', 'items', 'quantity', 'status', 'quality_rating', 'issue_date', 'acknowledgment_date']


class VendorPerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricalPerformance
        fields = ['date', 'on_time_delivery_rate', 'quality_rating_avg', 'average_response_time', 'fulfillment_rate']


class AcknowledgePurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = ['acknowledgment_date']
