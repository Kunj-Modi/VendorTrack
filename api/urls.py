from django.urls import path

from .views import *

'''
● POST /vendors/: Create a new vendor.
● GET /vendors/: List all vendors.
● GET /vendors/{vendor_id}/: Retrieve a specific vendor's details.
● PUT /vendors/{vendor_id}/: Update a vendor's details.
● DELETE /vendors/{vendor_id}/: Delete a vendor.

● POST /purchase_orders/: Create a purchase order.
● GET /purchase_orders/: List all purchase orders with an option to filter by
vendor.
● GET /purchase_orders/{po_id}/: Retrieve details of a specific purchase order.
● PUT /purchase_orders/{po_id}/: Update a purchase order.
● DELETE /purchase_orders/{po_id}/: Delete a purchase order.

● GET /vendors/{vendor_id}/performance: Retrieve a vendor's performance
metrics.
'''

urlpatterns = [
    path('vendors/<int:vendor_id>/performance', VendorPerformance, name='vendor_performance'),  # get

    path('vendors/<int:vendor_id>/', VendorID, name='vendor_detail'),  # get, put, and delete
    path('vendors/', Vendors, name='vendor_list'),  # get all and post new

    path('api/purchase_orders/<int:po_id>/acknowledge/', AcknowledgePurchaseOrder, name='acknowledge_purchase_order'),  # update

    path('purchase_orders/<int:po_id>/', PurchaseOrderID, name='purchase_order_detail'),  # get, put, and delete
    path('purchase_orders/', PurchaseOrders, name='purchase_order_list'),  # get all and post new
]
