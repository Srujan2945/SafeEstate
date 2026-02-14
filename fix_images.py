#!/usr/bin/env python
import os
import sys
import django

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'safeestate.settings')
django.setup()

from properties.models import Property, PropertyImage

def fix_property_image_assignments():
    """Fix property image assignments to match better"""
    print("Fixing property image assignments...")
    
    # Clear existing images
    PropertyImage.objects.all().delete()
    
    # Get properties
    properties = list(Property.objects.all().order_by('id'))
    
    # Image mappings based on property types and locations
    image_mappings = [
        {
            'title_contains': 'Mumbai',
            'image': 'properties/mumbai_apartment.jpg',
            'caption': 'Beautiful Mumbai Apartment with modern amenities'
        },
        {
            'title_contains': 'Delhi',
            'image': 'properties/delhi_house.jpg',
            'caption': 'Spacious Delhi House with garden space'
        },
        {
            'title_contains': 'Bangalore',
            'image': 'properties/bangalore_commercial.jpg',
            'caption': 'Prime Bangalore Commercial Property'
        },
        {
            'title_contains': 'Pune',
            'image': 'properties/pune_plot.jpg',
            'caption': 'Ready to construct plot in Pune'
        },
        {
            'title_contains': 'Chennai',
            'image': 'properties/chennai_flat.jpg',
            'caption': 'Compact Chennai Flat in prime location'
        }
    ]
    
    # Assign images based on city/title matching
    for property_obj in properties:
        for mapping in image_mappings:
            if mapping['title_contains'].lower() in property_obj.title.lower():
                PropertyImage.objects.create(
                    property=property_obj,
                    image=mapping['image'],
                    caption=mapping['caption'],
                    is_primary=True
                )
                print(f"✓ Assigned {mapping['image']} to {property_obj.title}")
                break
    
    print(f"\n✅ Image assignment completed!")
    print(f"Total images: {PropertyImage.objects.count()}")

if __name__ == '__main__':
    fix_property_image_assignments()