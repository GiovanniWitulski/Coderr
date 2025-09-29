from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    
    class UserType(models.TextChoices):
        BUSINESS = 'business', 'Business'
        CUSTOMER = 'customer', 'Customer'

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    type = models.CharField(
        max_length=10,
        choices=UserType.choices,
        default=UserType.CUSTOMER
    )
    
    file = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, default='')
    tel = models.CharField(max_length=30, blank=True, default='')
    description = models.TextField(blank=True, default='')
    working_hours = models.CharField(max_length=100, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.get_type_display()}"