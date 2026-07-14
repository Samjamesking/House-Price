from django.contrib import admin
from .models import PredictionHistory

@admin.register(PredictionHistory)
class PredictionHistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_username', 'neighborhood', 'overall_quality', 'predicted_price_usd', 'model_used', 'created_at')
    list_filter = ('neighborhood', 'overall_quality', 'model_used', 'created_at')
    search_fields = ('user__username', 'neighborhood', 'model_used')
    readonly_fields = (
        'user', 'overall_quality', 'living_area', 'bedrooms', 'bathrooms',
        'garage_capacity', 'year_built', 'total_rooms', 'lot_area', 'neighborhood',
        'overall_condition', 'basement_area', 'garage_area', 'fireplaces',
        'predicted_price_usd', 'predicted_price_inr', 'model_used', 'confidence_score', 'created_at'
    )
    date_hierarchy = 'created_at'
    
    def get_username(self, obj):
        return obj.user.username if obj.user else "Guest"
    get_username.short_description = 'User'
