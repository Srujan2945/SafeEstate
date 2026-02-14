from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model

# Custom User Model
class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('buyer', 'Buyer'),
        ('seller', 'Seller'),
        ('admin', 'Admin'),
    ]
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='buyer')
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    is_verified = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.username} ({self.get_role_display()})'

# Seller KYC Verification Model
class SellerKYC(models.Model):
    VERIFICATION_STATUS = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    seller = models.OneToOneField('CustomUser', on_delete=models.CASCADE, related_name='kyc')
    
    # Required Identity Documents
    pan_card = models.FileField(upload_to='kyc/pan/', help_text='Upload PAN Card (Required) - Images or PDF')
    aadhaar_card = models.FileField(upload_to='kyc/aadhaar/', blank=True, help_text='Upload Aadhaar Card (Required) - Images or PDF')
    
    # Required Property Documents
    ownership_proof = models.FileField(upload_to='kyc/ownership/', blank=True, help_text='Upload Ownership Proof Document (Required) - Images or PDF')
    revenue_records = models.FileField(upload_to='kyc/revenue/', blank=True, help_text='Upload Revenue Records (Required) - Images or PDF')
    tax_receipt = models.FileField(upload_to='kyc/tax/', blank=True, help_text='Upload Tax Receipt (Required) - Images or PDF')
    encumbrance_certificate = models.FileField(upload_to='kyc/encumbrance/', blank=True, help_text='Upload Encumbrance Certificate (Required) - Images or PDF')
    
    # Optional Additional Documents
    voter_id = models.FileField(upload_to='kyc/voter/', blank=True, help_text='Upload Voter ID (Optional) - Images or PDF')
    additional_documents = models.FileField(upload_to='kyc/additional/', blank=True, help_text='Any additional supporting documents - Images or PDF')
    
    # Verification Status
    status = models.CharField(max_length=10, choices=VERIFICATION_STATUS, default='pending')
    remarks = models.TextField(blank=True, help_text='Admin remarks for verification')
    verified_by = models.ForeignKey('CustomUser', on_delete=models.SET_NULL, null=True, blank=True, related_name='verified_kycs')
    date_submitted = models.DateTimeField(auto_now_add=True)
    date_verified = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f'KYC for {self.seller.username} - {self.get_status_display()}'
    
    def get_required_documents(self):
        """Return list of required documents for display"""
        return [
            {'name': 'PAN Card', 'field': 'pan_card', 'uploaded': bool(self.pan_card)},
            {'name': 'Aadhaar Card', 'field': 'aadhaar_card', 'uploaded': bool(self.aadhaar_card)},
            {'name': 'Ownership Proof', 'field': 'ownership_proof', 'uploaded': bool(self.ownership_proof)},
            {'name': 'Revenue Records', 'field': 'revenue_records', 'uploaded': bool(self.revenue_records)},
            {'name': 'Tax Receipt', 'field': 'tax_receipt', 'uploaded': bool(self.tax_receipt)},
            {'name': 'Encumbrance Certificate', 'field': 'encumbrance_certificate', 'uploaded': bool(self.encumbrance_certificate)},
        ]
    
    def is_complete(self):
        """Check if all required documents are uploaded"""
        return all([
            self.pan_card,
            self.aadhaar_card,
            self.ownership_proof,
            self.revenue_records,
            self.tax_receipt,
            self.encumbrance_certificate,
        ])

# OTP Model for simulation
class OTPVerification(models.Model):
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    
    def __str__(self):
        return f'OTP for {self.user.username}'
    
    def is_expired(self):
        from django.utils import timezone
        return timezone.now() > self.expires_at
