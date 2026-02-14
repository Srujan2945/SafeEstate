from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from .models import SellerKYC, OTPVerification

User = get_user_model()

class CustomUserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=15, required=False)
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False)
    role = forms.ChoiceField(choices=[('buyer', 'Buyer'), ('seller', 'Seller')], initial='buyer')

    class Meta:
        model = User
        fields = ('username', 'email', 'phone', 'address', 'role', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500'})

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.phone = self.cleaned_data['phone']
        user.address = self.cleaned_data['address']
        user.role = self.cleaned_data['role']
        if commit:
            user.save()
        return user

class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500'})

class SellerKYCForm(forms.ModelForm):
    class Meta:
        model = SellerKYC
        fields = [
            # Required Documents
            'pan_card', 'aadhaar_card', 'ownership_proof', 'revenue_records', 'tax_receipt', 'encumbrance_certificate',
            # Optional Documents
            'voter_id', 'additional_documents'
        ]
        widgets = {
            # Required Documents
            'pan_card': forms.FileInput(attrs={
                'class': 'w-full px-3 py-2 border-2 border-red-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-red-500',
                'accept': 'image/*,application/pdf',
                'required': True
            }),
            'aadhaar_card': forms.FileInput(attrs={
                'class': 'w-full px-3 py-2 border-2 border-red-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-red-500',
                'accept': 'image/*,application/pdf',
                'required': True
            }),
            'ownership_proof': forms.FileInput(attrs={
                'class': 'w-full px-3 py-2 border-2 border-red-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-red-500',
                'accept': 'image/*,application/pdf',
                'required': True
            }),
            'revenue_records': forms.FileInput(attrs={
                'class': 'w-full px-3 py-2 border-2 border-red-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-red-500',
                'accept': 'image/*,application/pdf',
                'required': True
            }),
            'tax_receipt': forms.FileInput(attrs={
                'class': 'w-full px-3 py-2 border-2 border-red-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-red-500',
                'accept': 'image/*,application/pdf',
                'required': True
            }),
            'encumbrance_certificate': forms.FileInput(attrs={
                'class': 'w-full px-3 py-2 border-2 border-red-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-500 focus:border-red-500',
                'accept': 'image/*,application/pdf',
                'required': True
            }),
            # Optional Documents
            'voter_id': forms.FileInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                'accept': 'image/*,application/pdf'
            }),
            'additional_documents': forms.FileInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                'accept': 'image/*,application/pdf'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add required asterisk to labels
        required_fields = ['pan_card', 'aadhaar_card', 'ownership_proof', 'revenue_records', 'tax_receipt', 'encumbrance_certificate']
        for field_name in required_fields:
            if field_name in self.fields:
                self.fields[field_name].required = True
                if self.fields[field_name].label:
                    self.fields[field_name].label += ' *'
    
    def clean(self):
        cleaned_data = super().clean()
        required_fields = ['pan_card', 'aadhaar_card', 'ownership_proof', 'revenue_records', 'tax_receipt', 'encumbrance_certificate']
        
        # Check required fields
        for field_name in required_fields:
            if not cleaned_data.get(field_name) and not getattr(self.instance, field_name, None):
                self.add_error(field_name, 'This document is required for KYC verification.')
        
        # Check file size and type for all uploaded files
        allowed_types = ['image/jpeg', 'image/png', 'image/gif', 'application/pdf']
        allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.pdf']
        
        for field_name in self.fields:
            file_field = cleaned_data.get(field_name)
            if file_field and hasattr(file_field, 'size'):
                # Check file size (10MB limit)
                if file_field.size > 10 * 1024 * 1024:  # 10MB in bytes
                    self.add_error(field_name, 'File size cannot exceed 10MB.')
                
                # Check file type
                if hasattr(file_field, 'content_type'):
                    if file_field.content_type not in allowed_types:
                        self.add_error(field_name, 'Only images (JPG, PNG, GIF) and PDF files are allowed.')
                
                # Check file extension
                if hasattr(file_field, 'name'):
                    file_extension = '.' + file_field.name.split('.')[-1].lower()
                    if file_extension not in allowed_extensions:
                        self.add_error(field_name, 'Only images (JPG, PNG, GIF) and PDF files are allowed.')
        
        return cleaned_data

class OTPVerificationForm(forms.Form):
    otp = forms.CharField(
        max_length=6, 
        min_length=6,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-center text-lg tracking-widest',
            'placeholder': '123456'
        })
    )