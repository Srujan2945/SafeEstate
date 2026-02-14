#!/usr/bin/env python
import os
import sys
import django

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'safeestate.settings')
django.setup()

from properties.models import Property, PropertyImage

def check_property_images():
    """Check and display property images status"""
    print("Checking property images...")
    
    properties = Property.objects.all()
    print(f"\nFound {properties.count()} properties:")
    
    for property_obj in properties:
        images = PropertyImage.objects.filter(property=property_obj)
        print(f"\n{property_obj.title} ({property_obj.city}):")
        if images.exists():
            for img in images:
                print(f"  ✓ Image: {img.image.name}")
        else:
            print("  ✗ No images")
    
    print(f"\nTotal images in database: {PropertyImage.objects.count()}")

if __name__ == '__main__':
    check_property_images()