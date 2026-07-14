from django.db import models
from django.contrib.auth.models import User

class PredictionHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='predictions', null=True, blank=True)
    
    # 13 Input Features
    overall_quality = models.IntegerField(help_text="Overall material and finish quality (1-10)")
    living_area = models.FloatField(help_text="Above grade (ground) living area square feet")
    bedrooms = models.IntegerField(help_text="Number of bedrooms above basement")
    bathrooms = models.FloatField(help_text="Number of bathrooms (FullBath + 0.5 * HalfBath)")
    garage_capacity = models.IntegerField(help_text="Size of garage in car capacity")
    year_built = models.IntegerField(help_text="Original construction date")
    total_rooms = models.IntegerField(help_text="Total rooms above grade (does not include bathrooms)")
    lot_area = models.FloatField(help_text="Lot size in square feet")
    neighborhood = models.CharField(max_length=50, help_text="Physical location within Ames city limits")
    overall_condition = models.IntegerField(help_text="Overall condition rating (1-10)")
    basement_area = models.FloatField(help_text="Total square feet of basement area")
    garage_area = models.FloatField(help_text="Size of garage in square feet")
    fireplaces = models.IntegerField(help_text="Number of fireplaces")
    
    # Prediction Outputs
    predicted_price_usd = models.FloatField()
    predicted_price_inr = models.FloatField()
    model_used = models.CharField(max_length=100)
    confidence_score = models.FloatField(help_text="Confidence percentage based on R2 score")
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Prediction Histories"

    def __str__(self):
        user_str = self.user.username if self.user else "Guest"
        return f"Prediction for {user_str} on {self.created_at.strftime('%Y-%m-%d %H:%M')}"
