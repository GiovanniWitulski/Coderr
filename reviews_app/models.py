from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from user_profile_app.models import UserProfile

class Review(models.Model):
    business_user = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='reviews_received',
        limit_choices_to={'type': UserProfile.UserType.BUSINESS}
    )
    
    reviewer = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='reviews_written',
        limit_choices_to={'type': UserProfile.UserType.CUSTOMER}
    )
    
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    
    description = models.TextField()


    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('business_user', 'reviewer')

    def __str__(self):
        return f"Review from {self.reviewer.user.username} for {self.business_user.user.username} ({self.rating} stars)"