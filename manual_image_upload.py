#!/usr/bin/env python
"""
Manual Image Upload Script for SafeEstate Properties

This script allows you to manually add images to properties by:
1. Copying image files to the media/properties directory
2. Updating the database to reference the new images

Usage:
1. Place your image files in the media/properties directory
2. Run this script and follow the prompts
3. The script will associate images with properties
"""

import os
import sys
import django
from pathlib import Path

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'safeestate.settings')
django.setup()

from properties.models import Property, PropertyImage
from django.core.files import File

def list_properties():
    """List all properties for selection"""
    properties = Property.objects.all().order_by('id')
    print("📋 Available Properties:")
    print("-" * 50)
    for prop in properties:
        has_image = "✅" if prop.images.exists() else "❌"
        print(f"{prop.id:2d}. {has_image} {prop.title[:40]:<40} ({prop.city})")
    print("-" * 50)
    return properties

def list_available_images():
    """List available image files in media directory"""
    media_dir = Path('media/properties')
    if not media_dir.exists():
        media_dir.mkdir(parents=True, exist_ok=True)
        
    image_files = []
    for ext in ['*.jpg', '*.jpeg', '*.png', '*.gif']:
        image_files.extend(media_dir.glob(ext))
        image_files.extend(media_dir.glob(ext.upper()))
    
    if not image_files:
        print("❌ No image files found in media/properties directory")
        print("📁 Please place your image files in: media/properties/")
        return []
    
    print("\n📸 Available Image Files:")
    print("-" * 50)
    for i, img_file in enumerate(image_files, 1):
        file_size = img_file.stat().st_size / 1024  # KB
        print(f"{i:2d}. {img_file.name:<30} ({file_size:.1f} KB)")
    print("-" * 50)
    
    return image_files

def upload_image_to_property():
    """Interactive function to upload image to property"""
    properties = list_properties()
    if not properties:
        print("❌ No properties found in database")
        return
    
    image_files = list_available_images()
    if not image_files:
        return
    
    try:
        # Select property
        prop_id = int(input(f"\n🏠 Enter Property ID (1-{len(properties)}): "))
        if prop_id < 1 or prop_id > len(properties):
            print("❌ Invalid property ID")
            return
        
        selected_property = properties[prop_id - 1]
        print(f"✅ Selected: {selected_property.title}")
        
        # Select image
        img_num = int(input(f"\n📸 Enter Image Number (1-{len(image_files)}): "))
        if img_num < 1 or img_num > len(image_files):
            print("❌ Invalid image number")
            return
        
        selected_image = image_files[img_num - 1]
        print(f"✅ Selected: {selected_image.name}")
        
        # Get caption
        caption = input(f"\n📝 Enter image caption (optional): ").strip()
        
        # Replace existing image?
        if selected_property.images.exists():
            replace = input(f"\n⚠️  Property already has images. Replace them? (y/N): ").lower()
            if replace == 'y':
                selected_property.images.all().delete()
                print("🗑️  Existing images removed")
        
        # Create PropertyImage record
        with open(selected_image, 'rb') as img_file:
            property_image = PropertyImage(
                property=selected_property,
                caption=caption or f"Image for {selected_property.title}",
                is_primary=True
            )
            property_image.image.save(
                selected_image.name,
                File(img_file),
                save=True
            )
        
        print(f"✅ Image successfully uploaded to {selected_property.title}")
        print(f"🔗 Image URL: {property_image.image.url}")
        
    except ValueError:
        print("❌ Please enter a valid number")
    except Exception as e:
        print(f"❌ Error: {e}")

def show_instructions():
    """Show detailed instructions for manual image management"""
    print("""
🎯 Manual Image Management Instructions
======================================

Method 1: Using This Script
--------------------------
1. Place your image files in: media/properties/
2. Run this script: python manual_image_upload.py
3. Follow the interactive prompts
4. Select property and image to associate them

Method 2: Django Admin Panel
---------------------------
1. Go to: http://127.0.0.1:8000/admin/
2. Login with admin credentials
3. Navigate to: Properties → Property images
4. Click "Add Property image" or edit existing ones
5. Upload your image file and set properties

Method 3: Application Interface
------------------------------
1. Login as property owner
2. Go to property detail page
3. Click "📷 Manage Images" button
4. Upload new image or delete existing ones

Method 4: Direct Database + File System
--------------------------------------
1. Copy image to: media/properties/your_image.jpg
2. Use Django shell to create PropertyImage record:
   
   python manage.py shell
   >>> from properties.models import Property, PropertyImage
   >>> prop = Property.objects.get(id=1)  # Your property ID
   >>> img = PropertyImage.objects.create(
   ...     property=prop,
   ...     image='properties/your_image.jpg',
   ...     caption='Your caption',
   ...     is_primary=True
   ... )
   >>> print(f"Image URL: {img.image.url}")

File Requirements:
- Supported formats: JPG, JPEG, PNG, GIF
- Maximum size: 10MB
- Recommended resolution: 800x600 or higher
- File naming: Use descriptive names

Tips:
- Each property should have at least one image
- First image is automatically set as primary
- Images are served from /media/properties/ URL
- Always backup before making changes
""")

def main():
    print("🏠 SafeEstate Manual Image Upload Tool")
    print("=" * 40)
    
    while True:
        print("\nOptions:")
        print("1. Upload image to property")
        print("2. List all properties")
        print("3. List available images")
        print("4. Show instructions")
        print("5. Exit")
        
        choice = input("\n👆 Choose an option (1-5): ").strip()
        
        if choice == '1':
            upload_image_to_property()
        elif choice == '2':
            list_properties()
        elif choice == '3':
            list_available_images()
        elif choice == '4':
            show_instructions()
        elif choice == '5':
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please enter 1-5.")

if __name__ == '__main__':
    main()