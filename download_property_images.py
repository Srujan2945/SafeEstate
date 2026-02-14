#!/usr/bin/env python
import os
import sys
import django
import requests
from urllib.parse import urlparse
import uuid

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'safeestate.settings')
django.setup()

from properties.models import Property, PropertyImage
from django.core.files.base import ContentFile

def download_and_save_image(url, property_obj, caption):
    """Download image from URL and save to property"""
    try:
        # Download image
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Generate unique filename
        parsed_url = urlparse(url)
        extension = '.jpg'  # Default to jpg
        if '.' in parsed_url.path:
            extension = '.' + parsed_url.path.split('.')[-1].lower()
        
        filename = f"property_{property_obj.id}_{uuid.uuid4().hex[:8]}{extension}"
        
        # Create PropertyImage
        property_image = PropertyImage(
            property=property_obj,
            caption=caption,
            is_primary=True
        )
        
        # Save image content
        property_image.image.save(
            filename,
            ContentFile(response.content),
            save=True
        )
        
        return True, f"Successfully downloaded and saved image for {property_obj.title}"
        
    except Exception as e:
        return False, f"Error downloading image for {property_obj.title}: {str(e)}"

def add_images_to_properties():
    """Add real images from internet to properties"""
    print("🖼️  Adding Real Images from Internet to Properties...")
    print("⚠️  Note: Using sample URLs - replace with actual property photos in production")
    
    # Sample property image URLs (using placeholder/sample images)
    # In production, these would be actual property photos
    image_urls = {
        'villa': [
            'https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?w=800&h=600&fit=crop',  # Modern villa
            'https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?w=800&h=600&fit=crop',  # Luxury villa
            'https://images.unsplash.com/photo-1600566753190-17f0baa2a6c3?w=800&h=600&fit=crop',  # Villa exterior
        ],
        'apartment': [
            'https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?w=800&h=600&fit=crop',  # Modern apartment
            'https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=800&h=600&fit=crop',  # Apartment building
            'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?w=800&h=600&fit=crop',  # High-rise apartment
        ],
        'flat': [
            'https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=800&h=600&fit=crop',  # Flat interior
            'https://images.unsplash.com/photo-1484154218962-a197022b5858?w=800&h=600&fit=crop',  # Modern flat
            'https://images.unsplash.com/photo-1512917774080-9991f1c4c750?w=800&h=600&fit=crop',  # Apartment flat
        ],
        'house': [
            'https://images.unsplash.com/photo-1570129477492-45c003edd2be?w=800&h=600&fit=crop',  # Modern house
            'https://images.unsplash.com/photo-1582268611958-ebfd161ef9cf?w=800&h=600&fit=crop',  # Family house
            'https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=800&h=600&fit=crop',  # Beautiful house
        ],
        'commercial': [
            'https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=800&h=600&fit=crop',  # Office building
            'https://images.unsplash.com/photo-1560472354-b33ff0c44a43?w=800&h=600&fit=crop',  # Commercial space
            'https://images.unsplash.com/photo-1497366216548-37526070297c?w=800&h=600&fit=crop',  # Office interior
        ],
        'plot': [
            'https://images.unsplash.com/photo-1500382017468-9049fed747ef?w=800&h=600&fit=crop',  # Land plot
            'https://images.unsplash.com/photo-1500534314209-a25ddb2bd429?w=800&h=600&fit=crop',  # Residential plot
            'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800&h=600&fit=crop',  # Development land
        ],
        'penthouse': [
            'https://images.unsplash.com/photo-1600607687644-aac4c3eac7f4?w=800&h=600&fit=crop',  # Luxury penthouse
        ],
        'farmhouse': [
            'https://images.unsplash.com/photo-1449824913935-59a10b8d2000?w=800&h=600&fit=crop',  # Country farmhouse
        ],
        'cottage': [
            'https://images.unsplash.com/photo-1520637836862-4d197d17c92a?w=800&h=600&fit=crop',  # Cozy cottage
        ],
        'heritage': [
            'https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=800&h=600&fit=crop',  # Heritage building
        ],
        'beachfront': [
            'https://images.unsplash.com/photo-1544551763-46a013bb70d5?w=800&h=600&fit=crop',  # Beach property
        ],
        'mountain': [
            'https://images.unsplash.com/photo-1449824913935-59a10b8d2000?w=800&h=600&fit=crop',  # Mountain house
        ]
    }
    
    # Get all properties that need images
    properties = Property.objects.all()
    success_count = 0
    error_count = 0
    
    for i, property_obj in enumerate(properties):
        # Remove existing images first
        property_obj.images.all().delete()
        
        # Determine image type based on property title and type
        image_type = 'house'  # default
        title_lower = property_obj.title.lower()
        
        if 'villa' in title_lower:
            image_type = 'villa'
        elif 'penthouse' in title_lower:
            image_type = 'penthouse'
        elif 'farmhouse' in title_lower:
            image_type = 'farmhouse'
        elif 'cottage' in title_lower:
            image_type = 'cottage'
        elif 'heritage' in title_lower or 'haveli' in title_lower:
            image_type = 'heritage'
        elif 'beach' in title_lower or 'seaside' in title_lower:
            image_type = 'beachfront'
        elif 'mountain' in title_lower or 'hill' in title_lower:
            image_type = 'mountain'
        elif property_obj.property_type == 'flat':
            if 'apartment' in title_lower:
                image_type = 'apartment'
            else:
                image_type = 'flat'
        elif property_obj.property_type == 'house':
            image_type = 'house'
        elif property_obj.property_type == 'commercial':
            image_type = 'commercial'
        elif property_obj.property_type == 'plot':
            image_type = 'plot'
        
        # Get appropriate image URL
        urls = image_urls.get(image_type, image_urls['house'])
        url = urls[i % len(urls)]  # Cycle through available URLs
        
        # Download and save image
        caption = f"Beautiful {property_obj.get_property_type_display()} in {property_obj.city}"
        success, message = download_and_save_image(url, property_obj, caption)
        
        if success:
            success_count += 1
            print(f"  ✅ {message}")
        else:
            error_count += 1
            print(f"  ❌ {message}")
    
    print(f"\n📊 Image Download Summary:")
    print(f"  Successful: {success_count}")
    print(f"  Errors: {error_count}")
    print(f"  Total Properties: {properties.count()}")
    
    # Verify results
    properties_with_images = Property.objects.filter(images__isnull=False).distinct().count()
    print(f"  Properties with images: {properties_with_images}")

def create_media_directories():
    """Ensure media directories exist"""
    media_root = os.path.join(os.path.dirname(__file__), 'media')
    properties_dir = os.path.join(media_root, 'properties')
    
    os.makedirs(properties_dir, exist_ok=True)
    print(f"📁 Media directory ready: {properties_dir}")

if __name__ == '__main__':
    print("🌐 Downloading Real Property Images from Internet...")
    print("⚠️  This will download images from Unsplash (free stock photos)")
    print("🔄 Starting download process...\n")
    
    create_media_directories()
    add_images_to_properties()
    
    print("\n✨ Property images have been downloaded and assigned!")
    print("📷 All properties now have real images for better visual appeal")
    print("🎯 The platform is ready for demonstration with actual photos")
    print("\n⚠️  Production Notes:")
    print("  - Replace with actual property photos when available")
    print("  - Ensure proper image rights and permissions")
    print("  - Consider image optimization for faster loading")