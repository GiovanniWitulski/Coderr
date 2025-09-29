from django.db import models

from user_profile_app.models import UserProfile

# Create your models here.

class Order(models.Model):

    class Status(models.TextChoices):
        IN_PROGRESS = 'in_progress', 'In Progress'
        COMPLETED = 'completed', 'Completed'
        CANCELLED = 'cancelled', 'Cancelled'

    offer_detail = models.ForeignKey(
        'offers_app.OfferDetail',
        on_delete=models.CASCADE,
        related_name='orders'
    )

    customer = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='customer_orders',
        limit_choices_to={'type': UserProfile.UserType.CUSTOMER},
    )

    business = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='business_orders',
        limit_choices_to={'type': UserProfile.UserType.BUSINESS},
    )

    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default='pending')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    status = models.CharField(
        max_length=25,
        choices=Status.choices,
        default=Status.IN_PROGRESS
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.id} by {self.customer.user.username} for {self.offer_detail.title}"