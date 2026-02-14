"""
Admin actions for bulk property image management
"""
import requests
import uuid
from django.contrib import messages
from django.core.files.base import ContentFile
from properties.models import PropertyImage

def bulk_assign_unique_images(modeladmin, request, queryset):
    """Assign unique images to selected properties"""
    
    # Diverse image pool for different property types
    image_pool = {
        'flat': [
            'https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?w=800&h=600&fit=crop',
            'https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=800&h=600&fit=crop',
            'https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=800&h=600&fit=crop',
            'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?w=800&h=600&fit=crop',
        ],
        'house': [
            'https://images.unsplash.com/photo-1570129477492-45c003edd2be?w=800&h=600&fit=crop',
            'https://images.unsplash.com/photo-1582268611958-ebfd161ef9cf?w=800&h=600&fit=crop',
            'https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=800&h=600&fit=crop',
            'https://images.unsplash.com/photo-1564013799919-ab600027ffc6?w=800&h=600&fit=crop',
        ],
        'commercial': [
            'https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=800&h=600&fit=crop',
            'https://images.unsplash.com/photo-1560472354-b33ff0c44a43?w=800&h=600&fit=crop',
            'https://images.unsplash.com/photo-1497366216548-37526070297c?w=800&h=600&fit=crop',
            'https://images.unsplash.com/photo-1481026469463-66327c86e544?w=800&h=600&fit=crop',
        ],
        'plot': [
            'https://images.unsplash.com/photo-1500382017468-9049fed747ef?w=800&h=600&fit=crop',
            'https://images.unsplash.com/photo-1500534314209-a25ddb2bd429?w=800&h=600&fit=crop',
            'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800&h=600&fit=crop',
            'https://images.unsplash.com/photo-1442544213729-6a15f1611937?w=800&h=600&fit=crop',
        ]
    }
    
    # Additional special images
    special_images = [
        'https://images.unsplash.com/photo-1449824913935-59a10b8d2000?w=800&h=600&fit=crop',  # Rural
        'https://images.unsplash.com/photo-1518780664697-55e3ad937233?w=800&h=600&fit=crop',  # Cottage
        'https://images.unsplash.com/photo-1571896349842-33c89424de2d?w=800&h=600&fit=crop',  # Beachfront
        'https://images.unsplash.com/photo-1572120360610-d971b9d7767c?w=800&h=600&fit=crop',  # Luxury
    ]
    
    success_count = 0
    error_count = 0
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    for i, property_obj in enumerate(queryset):
        try:
            # Remove existing images
            property_obj.images.all().delete()
            
            # Select image based on property type and index for uniqueness
            prop_type = property_obj.property_type
            if prop_type in image_pool:
                available_images = image_pool[prop_type] + special_images
            else:
                available_images = image_pool['house'] + special_images
            
            # Use index to ensure different images for each property
            image_url = available_images[i % len(available_images)]
            
            # Download image
            response = requests.get(image_url, headers=headers, timeout=15)
            response.raise_for_status()
            
            # Create PropertyImage
            filename = f"admin_bulk_{property_obj.id}_{uuid.uuid4().hex[:8]}.jpg"
            property_image = PropertyImage(
                property=property_obj,
                caption=f"Professional {property_obj.get_property_type_display().lower()} image for {property_obj.city}",
                is_primary=True
            )
            property_image.image.save(filename, ContentFile(response.content), save=True)
            success_count += 1
            
        except Exception as e:
            error_count += 1
            messages.error(request, f"Failed to assign image to {property_obj.title}: {str(e)[:100]}...")
    
    if success_count > 0:
        messages.success(request, f"Successfully assigned unique images to {success_count} properties.")
    if error_count > 0:
        messages.warning(request, f"Failed to assign images to {error_count} properties.")

bulk_assign_unique_images.short_description = "🖼️ Assign unique professional images"

def remove_all_property_images(modeladmin, request, queryset):
    """Remove all images from selected properties"""
    total_removed = 0
    for property_obj in queryset:
        count = property_obj.images.count()
        property_obj.images.all().delete()
        total_removed += count
    
    messages.success(request, f"🗑️ Removed {total_removed} images from {queryset.count()} properties.")

remove_all_property_images.short_description = "🗑️ Remove all images from selected properties"

def assign_placeholder_images(modeladmin, request, queryset):
    """Assign placeholder images to properties without images"""
    
    placeholder_url = "https://images.unsplash.com/photo-1560518883-ce09059eeffa?w=800&h=600&fit=crop"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    assigned_count = 0
    for property_obj in queryset:
        if not property_obj.images.exists():
            try:
                response = requests.get(placeholder_url, headers=headers, timeout=10)
                response.raise_for_status()
                
                filename = f"placeholder_{property_obj.id}_{uuid.uuid4().hex[:6]}.jpg"
                property_image = PropertyImage(
                    property=property_obj,
                    caption=f"Placeholder image for {property_obj.title}",
                    is_primary=True
                )
                property_image.image.save(filename, ContentFile(response.content), save=True)
                assigned_count += 1
                
            except Exception as e:
                messages.error(request, f"Failed to assign placeholder to {property_obj.title}: {e}")
    
    if assigned_count > 0:
        messages.success(request, f"📷 Assigned placeholder images to {assigned_count} properties.")
    else:
        messages.info(request, "All selected properties already have images.")

assign_placeholder_images.short_description = "📷 Assign placeholder images to properties without images"