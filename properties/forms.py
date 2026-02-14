from django import forms
from .models import Property, PropertyImage, VisitRequest, PropertySearch, INDIAN_STATES

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = [
            'title', 'description', 'price', 'property_type',
            'state', 'city', 'pincode', 'address',
            'area', 'bedrooms', 'bathrooms',
            'latitude', 'longitude'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500'}),
            'description': forms.Textarea(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500', 'rows': 4}),
            'price': forms.NumberInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500'}),
            'property_type': forms.Select(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500'}),
            'state': forms.Select(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500'}),
            'city': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500'}),
            'pincode': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500', 'pattern': '[0-9]{6}'}),
            'address': forms.Textarea(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500', 'rows': 3}),
            'area': forms.NumberInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500', 'step': '0.01'}),
            'bedrooms': forms.NumberInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500'}),
            'bathrooms': forms.NumberInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500'}),
            'latitude': forms.NumberInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500', 'step': '0.000001'}),
            'longitude': forms.NumberInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500', 'step': '0.000001'}),
        }

class PropertyImageForm(forms.ModelForm):
    class Meta:
        model = PropertyImage
        fields = ['image', 'caption', 'is_primary']
        widgets = {
            'image': forms.FileInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg', 'accept': 'image/*'}),
            'caption': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500'}),
            'is_primary': forms.CheckboxInput(attrs={'class': 'rounded'}),
        }

class PropertyImageUploadForm(forms.Form):
    image = forms.ImageField(
        widget=forms.FileInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg',
            'accept': 'image/*'
        })
    )

class PropertySearchForm(forms.Form):
    property_type = forms.ChoiceField(
        choices=[('', 'Any Type')] + Property.PROPERTY_TYPES,
        required=False,
        widget=forms.Select(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500'})
    )
    state = forms.ChoiceField(
        choices=[('', 'Any State')] + INDIAN_STATES,
        required=False,
        widget=forms.Select(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500'})
    )
    city = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500', 'placeholder': 'Enter city name'})
    )
    pincode = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500', 'placeholder': 'Enter pincode'})
    )
    min_price = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500', 'placeholder': 'Min Price'})
    )
    max_price = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500', 'placeholder': 'Max Price'})
    )
    min_area = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500', 'placeholder': 'Min Area (sq ft)'})
    )
    max_area = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500', 'placeholder': 'Max Area (sq ft)'})
    )

class VisitRequestForm(forms.ModelForm):
    class Meta:
        model = VisitRequest
        fields = ['preferred_date', 'preferred_time', 'phone', 'message']
        widgets = {
            'preferred_date': forms.DateInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                'type': 'date'
            }),
            'preferred_time': forms.TimeInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                'type': 'time'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Your contact number'
            }),
            'message': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                'rows': 3,
                'placeholder': 'Any additional message for the seller...'
            }),
        }

class VisitResponseForm(forms.ModelForm):
    class Meta:
        model = VisitRequest
        fields = ['status', 'seller_response']
        widgets = {
            'status': forms.Select(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500'}),
            'seller_response': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                'rows': 3,
                'placeholder': 'Your response to the buyer...'
            }),
        }