from django import forms

NEIGHBORHOOD_CHOICES = sorted([
    ('Blmngtn', 'Bloomington Heights'),
    ('Blueste', 'Bluestem'),
    ('BrDale', 'Briardale'),
    ('BrkSide', 'Brookside'),
    ('ClearCr', 'Clear Creek'),
    ('CollgCr', 'College Creek'),
    ('Crawfor', 'Crawford'),
    ('Edwards', 'Edwards'),
    ('Gilbert', 'Gilbert'),
    ('IDOTRR', 'Iowa DOT & Rail Road'),
    ('MeadowV', 'Meadow Valley'),
    ('Mitchel', 'Mitchell'),
    ('NAmes', 'North Ames'),
    ('NPkVill', 'Northpark Villa'),
    ('NWAmes', 'Northwest Ames'),
    ('NoRidge', 'Northridge'),
    ('NridgHt', 'Northridge Heights'),
    ('OldTown', 'Old Town'),
    ('SWISU', 'South & West of ISU'),
    ('Sawyer', 'Sawyer'),
    ('SawyerW', 'Sawyer West'),
    ('Somerst', 'Somerset'),
    ('StoneBr', 'Stone Bridge'),
    ('Timber', 'Timberland'),
    ('Veenker', 'Veenker'),
], key=lambda x: x[1])

QUALITY_CHOICES = [(i, f"{i} - " + {
    10: "Very Excellent", 9: "Excellent", 8: "Very Good", 7: "Good",
    6: "Above Average", 5: "Average", 4: "Below Average", 3: "Fair",
    2: "Poor", 1: "Very Poor"
}.get(i, "")) for i in range(10, 0, -1)]

CONDITION_CHOICES = QUALITY_CHOICES

class HousePricePredictionForm(forms.Form):
    overall_quality = forms.ChoiceField(
        choices=QUALITY_CHOICES,
        initial=5,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Overall Quality"
    )
    overall_condition = forms.ChoiceField(
        choices=CONDITION_CHOICES,
        initial=5,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Overall Condition"
    )
    living_area = forms.FloatField(
        min_value=100.0,
        initial=1500.0,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 1500'}),
        label="Above Grade Living Area (sqft)"
    )
    basement_area = forms.FloatField(
        min_value=0.0,
        initial=800.0,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 800 (Enter 0 if no basement)'}),
        label="Basement Area (sqft)"
    )
    bedrooms = forms.IntegerField(
        min_value=0,
        max_value=10,
        initial=3,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 3'}),
        label="Bedrooms Above Grade"
    )
    bathrooms = forms.FloatField(
        min_value=0.0,
        max_value=10.0,
        initial=2.0,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.5', 'placeholder': 'e.g. 2.5'}),
        label="Number of Bathrooms"
    )
    total_rooms = forms.IntegerField(
        min_value=1,
        initial=6,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 6'}),
        label="Total Rooms (excluding bathrooms)"
    )
    lot_area = forms.FloatField(
        min_value=500.0,
        initial=8000.0,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 8000'}),
        label="Lot Area (sqft)"
    )
    neighborhood = forms.ChoiceField(
        choices=NEIGHBORHOOD_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label="Neighborhood Location"
    )
    garage_capacity = forms.IntegerField(
        min_value=0,
        max_value=5,
        initial=2,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 2 (Enter 0 if no garage)'}),
        label="Garage Capacity (Cars)"
    )
    garage_area = forms.FloatField(
        min_value=0.0,
        initial=400.0,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 400 (Enter 0 if no garage)'}),
        label="Garage Area (sqft)"
    )
    year_built = forms.IntegerField(
        min_value=1800,
        max_value=2026,
        initial=2000,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 2000'}),
        label="Year Built"
    )
    fireplaces = forms.IntegerField(
        min_value=0,
        max_value=4,
        initial=1,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 1'}),
        label="Number of Fireplaces"
    )

    def clean(self):
        cleaned_data = super().clean()
        living_area = cleaned_data.get('living_area')
        total_rooms = cleaned_data.get('total_rooms')
        bedrooms = cleaned_data.get('bedrooms')
        
        # Validation checks
        if total_rooms and bedrooms and total_rooms <= bedrooms:
            self.add_error('total_rooms', "Total rooms should exceed number of bedrooms.")
            
        return cleaned_data
