from django.utils import timezone

from django.db import models
from django.db.models import Sum, Avg, F

from django.db.models.signals import post_save
from django.dispatch import receiver

class Vendor(models.Model):
    """
    ● vendor_code: CharField - A unique identifier for the vendor.
    ● name: CharField - Vendor's name.
    ● contact_details: TextField - Contact information of the vendor.
    ● address: TextField - Physical address of the vendor.
    ● on_time_delivery_rate: FloatField - Tracks the percentage of on-time deliveries.
    ● quality_rating_avg: FloatField - Average rating of quality based on purchase orders.
    ● average_response_time: FloatField - Average time taken to acknowledge purchase orders.
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
    ● acknowledgment_date: DateTimeField, nullable - Timestamp when the vendor acknowledged the PO.
    """
    status_choices = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ]

    po_number = models.CharField(max_length=100, primary_key=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=50, choices=status_choices, default='pending')
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField()
    acknowledgment_date = models.DateTimeField(null=True, blank=True)

    def calculate_on_time_delivery_rate(self):
        completed_orders_count = PurchaseOrder.objects.filter(
            vendor=self.vendor,
            status='completed',
            delivery_date__lte=F('acknowledgment_date')
        ).count()

        total_completed_orders = PurchaseOrder.objects.filter(
            vendor=self.vendor,
            status='completed'
        ).count()

        if total_completed_orders > 0:
            on_time_delivery_rate = (completed_orders_count / total_completed_orders) * 100
        else:
            on_time_delivery_rate = 0
        
        return on_time_delivery_rate
    
    def calculate_quality_rating_average(self):
        completed_orders = PurchaseOrder.objects.filter(
            vendor=self.vendor,
            status='completed',
            quality_rating__isnull=False
        )

        total_ratings = completed_orders.count()
        if total_ratings > 0:
            quality_rating_sum = completed_orders.aggregate(Sum('quality_rating'))['quality_rating__sum']
            quality_rating_average = quality_rating_sum / total_ratings
        else:
            quality_rating_average = 0
        
        return quality_rating_average

    def calculate_average_response_time(self):
        completed_orders = PurchaseOrder.objects.filter(
            vendor=self.vendor,
            status='completed',
            acknowledgment_date__isnull=False
        )

        average_response_time_result = completed_orders.aggregate(
            avg_response_time=Avg(F('acknowledgment_date') - F('issue_date'))
        )
        average_response_timedelta = average_response_time_result.get('avg_response_time')

        # Convert timedelta to seconds
        if average_response_timedelta:
            average_response_seconds = average_response_timedelta.total_seconds()

            # Convert seconds to desired unit for average response time (e.g., minutes)
            average_response_time = average_response_seconds / 60  # Assuming you want the result in minutes
        else:
            average_response_time = 0

        return average_response_time

    def calculate_fulfillment_rate(self):
        successful_orders_count = PurchaseOrder.objects.filter(
            vendor=self.vendor,
            status='completed',
            quality_rating__isnull=False,
            acknowledgment_date__isnull=False
        ).count()

        total_orders = PurchaseOrder.objects.filter(
            vendor=self.vendor,
            status='completed'
        ).count()

        if total_orders > 0:
            fulfillment_rate = (successful_orders_count / total_orders) * 100
        else:
            fulfillment_rate = 0
        
        return fulfillment_rate

    def __str__(self):
        return self.po_number


class HistoricalPerformance(models.Model):
    """
    ● vendor: ForeignKey - Link to the Vendor model.
    ● date: DateTimeField - Date of the performance record.
    ● on_time_delivery_rate: FloatField - Historical record of the on-time delivery rate.
    ● quality_rating_avg: FloatField - Historical record of the quality rating average.
    ● average_response_time: FloatField - Historical record of the average response time.
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


@receiver(post_save, sender=PurchaseOrder)
def update_performance_metrics(sender, instance, **kwargs):
    vendor = instance.vendor
    vendor.on_time_delivery_rate = instance.calculate_on_time_delivery_rate()
    vendor.quality_rating_avg = instance.calculate_quality_rating_average()
    vendor.average_response_time = instance.calculate_average_response_time()
    vendor.fulfillment_rate = instance.calculate_fulfillment_rate()
    vendor.save()

    # Update HistoricalPerformance metrics
    historical_performance, created = HistoricalPerformance.objects.get_or_create(
        vendor=vendor,
        defaults={
            'date': timezone.now(),
            'on_time_delivery_rate': vendor.on_time_delivery_rate,
            'quality_rating_avg': vendor.quality_rating_avg,
            'average_response_time': vendor.average_response_time,
            'fulfillment_rate': vendor.fulfillment_rate,
        }
    )
    if not created:
        historical_performance.date = timezone.now()
        historical_performance.on_time_delivery_rate = vendor.on_time_delivery_rate
        historical_performance.quality_rating_avg = vendor.quality_rating_avg
        historical_performance.average_response_time = vendor.average_response_time
        historical_performance.fulfillment_rate = vendor.fulfillment_rate
    historical_performance.save()
