from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()

# Indian States and Cities (simplified)
INDIAN_STATES = [
    ('andhra_pradesh', 'Andhra Pradesh'),
    ('assam', 'Assam'),
    ('bihar', 'Bihar'),
    ('chhattisgarh', 'Chhattisgarh'),
    ('goa', 'Goa'),
    ('gujarat', 'Gujarat'),
    ('haryana', 'Haryana'),
    ('himachal_pradesh', 'Himachal Pradesh'),
    ('jharkhand', 'Jharkhand'),
    ('karnataka', 'Karnataka'),
    ('kerala', 'Kerala'),
    ('madhya_pradesh', 'Madhya Pradesh'),
    ('maharashtra', 'Maharashtra'),
    ('manipur', 'Manipur'),
    ('meghalaya', 'Meghalaya'),
    ('mizoram', 'Mizoram'),
    ('nagaland', 'Nagaland'),
    ('odisha', 'Odisha'),
    ('punjab', 'Punjab'),
    ('rajasthan', 'Rajasthan'),
    ('sikkim', 'Sikkim'),
    ('tamil_nadu', 'Tamil Nadu'),
    ('telangana', 'Telangana'),
    ('tripura', 'Tripura'),
    ('uttar_pradesh', 'Uttar Pradesh'),
    ('uttarakhand', 'Uttarakhand'),
    ('west_bengal', 'West Bengal'),
    ('delhi', 'Delhi'),
]

class Property(models.Model):
    PROPERTY_TYPES = [
        ('plot', 'Plot'),
        ('flat', 'Flat'),
        ('house', 'House'),
        ('commercial', 'Commercial'),
    ]
    
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('sold', 'Sold'),
        ('pending', 'Pending'),
    ]
    
    # Basic Information
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPES)
    
    # Location
    state = models.CharField(max_length=50, choices=INDIAN_STATES)
    city = models.CharField(max_length=100)
    pincode = models.CharField(max_length=6)
    address = models.TextField()
    
    # Optional Location Coordinates
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    
    # Property Details
    area = models.DecimalField(max_digits=10, decimal_places=2, help_text='Area in square feet')
    bedrooms = models.IntegerField(null=True, blank=True)
    bathrooms = models.IntegerField(null=True, blank=True)
    
    # Seller and Status
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='properties')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    
    # Timestamps
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = 'Properties'
        ordering = ['-date_created']
    
    def __str__(self):
        return f'{self.title} - {self.city}, {self.get_state_display()}'
    
    def get_absolute_url(self):
        return reverse('properties:property_detail', kwargs={'pk': self.pk})

class PropertyImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='properties/')
    caption = models.CharField(max_length=200, blank=True)
    is_primary = models.BooleanField(default=False)
    date_uploaded = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-is_primary', 'date_uploaded']
    
    def __str__(self):
        return f'Image for {self.property.title}'

class VisitRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('declined', 'Declined'),
        ('completed', 'Completed'),
    ]
    
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='visit_requests')
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='visit_requests')
    preferred_date = models.DateField()
    preferred_time = models.TimeField()
    message = models.TextField(blank=True, help_text='Additional message for the seller')
    phone = models.CharField(max_length=15)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    seller_response = models.TextField(blank=True)
    
    date_requested = models.DateTimeField(auto_now_add=True)
    date_responded = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-date_requested']
    
    def __str__(self):
        return f'Visit request for {self.property.title} by {self.buyer.username}'

class PropertySearch(models.Model):
    """Model to save user search preferences"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_searches')
    name = models.CharField(max_length=100, help_text='Name for this saved search')
    
    # Search Filters
    property_type = models.CharField(max_length=20, choices=Property.PROPERTY_TYPES, blank=True)
    state = models.CharField(max_length=50, choices=INDIAN_STATES, blank=True)
    city = models.CharField(max_length=100, blank=True)
    pincode = models.CharField(max_length=6, blank=True)
    min_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    max_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    min_area = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    max_area = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    date_saved = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.name} - {self.user.username}'
