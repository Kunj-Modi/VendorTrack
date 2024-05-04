from django.db import models


class Vendor(models.Model):
    """
    ● vendor_code: CharField - A unique identifier for the vendor.
    ● name: CharField - Vendor's name.
    ● contact_details: TextField - Contact information of the vendor.
    ● address: TextField - Physical address of the vendor.
    ● on_time_delivery_rate: FloatField - Tracks the percentage of on-time deliveries.
    ● quality_rating_avg: FloatField - Average rating of quality based on purchase
    orders.
    ● average_response_time: FloatField - Average time taken to acknowledge
    purchase orders.
    ● fulfillment_rate: FloatField - Percentage of purchase orders fulfilled successfully.
    """
    vendor_code = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=255)
    contact_details = models.TextField()
    address = models.TextField()
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()

    def __str__(self):
        return self.name


class PurchaseOrder(models.Model):
    """
    ● po_number: CharField - Unique number identifying the PO.
    ● vendor: ForeignKey - Link to the Vendor model.
    ● order_date: DateTimeField - Date when the order was placed.
    ● delivery_date: DateTimeField - Expected or actual delivery date of the order.
    ● items: JSONField - Details of items ordered.
    ● quantity: IntegerField - Total quantity of items in the PO.
    ● status: CharField - Current status of the PO (e.g., pending, completed, canceled).
    ● quality_rating: FloatField - Rating given to the vendor for this PO (nullable).
    ● issue_date: DateTimeField - Timestamp when the PO was issued to the vendor.
    ● acknowledgment_date: DateTimeField, nullable - Timestamp when the vendor
    acknowledged the PO.
    """
    po_number = models.CharField(max_length=100, primary_key=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=50)
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField()
    acknowledgment_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.po_number


class HistoricalPerformance(models.Model):
    """
    ● vendor: ForeignKey - Link to the Vendor model.
    ● date: DateTimeField - Date of the performance record.
    ● on_time_delivery_rate: FloatField - Historical record of the on-time delivery rate.
    ● quality_rating_avg: FloatField - Historical record of the quality rating average.
    ● average_response_time: FloatField - Historical record of the average response
    time.
    ● fulfillment_rate: FloatField - Historical record of the fulfilment rate.
    """
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()

    def __str__(self):
        return f"{self.vendor} - {self.date}"
