from django.shortcuts import render
from properties.models import Property

def home_view(request):
    """Landing page view with featured properties"""
    # Get featured properties (first 3 available properties)
    featured_properties = Property.objects.filter(status='available')[:3]
    
    context = {
        'featured_properties': featured_properties,
    }
    
    return render(request, 'base/index.html', context)