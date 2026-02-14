from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Property, PropertyImage, VisitRequest, PropertySearch

# Import custom admin actions
try:
    from admin_panel.admin_actions import (
        bulk_assign_unique_images,
        remove_all_property_images,
        assign_placeholder_images
    )
except ImportError:
    # Fallback if admin_actions module is not available
    bulk_assign_unique_images = None
    remove_all_property_images = None
    assign_placeholder_images = None

class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1
    fields = ('image', 'image_preview', 'caption', 'is_primary')
    readonly_fields = ('image_preview',)
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 100px; max-width: 150px; border-radius: 5px;"/>',
                obj.image.url
            )
        return "No Image"
    image_preview.short_description = "Preview"

class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'seller', 'property_type', 'price', 'city', 'state', 'status', 'image_count', 'date_created')
    list_filter = ('property_type', 'status', 'state', 'date_created')
    search_fields = ('title', 'city', 'seller__username', 'description')
    inlines = [PropertyImageInline]
    readonly_fields = ('date_created', 'date_updated')
    
    # Add custom bulk actions
    actions = ['assign_sample_images', 'remove_all_images']
    if bulk_assign_unique_images:
        actions.extend([bulk_assign_unique_images, remove_all_property_images, assign_placeholder_images])
    
    # Custom admin view configurations
    list_per_page = 25
    ordering = ['-date_created']
    save_on_top = True
    
    def image_count(self, obj):
        count = obj.images.count()
        if count > 0:
            return format_html(
                '<span style="color: green; font-weight: bold;">{} images</span>',
                count
            )
        else:
            return format_html(
                '<span style="color: red; font-weight: bold;">No images</span>'
            )
    image_count.short_description = "Images"
    
    def assign_sample_images(self, request, queryset):
        """Assign sample images to selected properties"""
        from django.contrib import messages
        import requests
        import uuid
        from django.core.files.base import ContentFile
        
        # Sample image URLs for different property types
        sample_images = {
            'flat': [
                'https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?w=800&h=600&fit=crop',
                'https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=800&h=600&fit=crop',
                'https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=800&h=600&fit=crop',
            ],
            'house': [
                'https://images.unsplash.com/photo-1570129477492-45c003edd2be?w=800&h=600&fit=crop',
                'https://images.unsplash.com/photo-1582268611958-ebfd161ef9cf?w=800&h=600&fit=crop',
                'https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=800&h=600&fit=crop',
            ],
            'commercial': [
                'https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=800&h=600&fit=crop',
                'https://images.unsplash.com/photo-1560472354-b33ff0c44a43?w=800&h=600&fit=crop',
                'https://images.unsplash.com/photo-1497366216548-37526070297c?w=800&h=600&fit=crop',
            ],
            'plot': [
                'https://images.unsplash.com/photo-1500382017468-9049fed747ef?w=800&h=600&fit=crop',
                'https://images.unsplash.com/photo-1500534314209-a25ddb2bd429?w=800&h=600&fit=crop',
                'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800&h=600&fit=crop',
            ]
        }
        
        success_count = 0
        for i, property_obj in enumerate(queryset):
            try:
                # Remove existing images
                property_obj.images.all().delete()
                
                # Get appropriate image URL
                prop_type = property_obj.property_type
                urls = sample_images.get(prop_type, sample_images['house'])
                image_url = urls[i % len(urls)]
                
                # Download and save image
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
                response = requests.get(image_url, headers=headers, timeout=10)
                response.raise_for_status()
                
                # Create PropertyImage
                filename = f"admin_assigned_{property_obj.id}_{uuid.uuid4().hex[:8]}.jpg"
                property_image = PropertyImage(
                    property=property_obj,
                    caption=f"Sample image for {property_obj.title}",
                    is_primary=True
                )
                property_image.image.save(filename, ContentFile(response.content), save=True)
                success_count += 1
                
            except Exception as e:
                messages.error(request, f"Failed to assign image to {property_obj.title}: {e}")
        
        messages.success(request, f"Successfully assigned sample images to {success_count} properties.")
    assign_sample_images.short_description = "Assign sample images to selected properties"
    
    def remove_all_images(self, request, queryset):
        """Remove all images from selected properties"""
        from django.contrib import messages
        
        total_removed = 0
        for property_obj in queryset:
            count = property_obj.images.count()
            property_obj.images.all().delete()
            total_removed += count
        
        messages.success(request, f"Removed {total_removed} images from {queryset.count()} properties.")
    remove_all_images.short_description = "Remove all images from selected properties"

class PropertyImageAdmin(admin.ModelAdmin):
    list_display = ('property_title', 'image_preview', 'caption', 'is_primary', 'file_size', 'date_uploaded')
    list_filter = ('is_primary', 'date_uploaded', 'property__property_type')
    search_fields = ('property__title', 'caption')
    readonly_fields = ('image_preview', 'file_size', 'date_uploaded')
    
    def property_title(self, obj):
        return obj.property.title
    property_title.short_description = "Property"
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 150px; max-width: 200px; border-radius: 5px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);"/>',
                obj.image.url
            )
        return "No Image"
    image_preview.short_description = "Image Preview"
    
    def file_size(self, obj):
        if obj.image:
            try:
                size = obj.image.size / 1024  # Convert to KB
                if size > 1024:
                    return f"{size/1024:.1f} MB"
                else:
                    return f"{size:.1f} KB"
            except:
                return "Unknown"
        return "No file"
    file_size.short_description = "File Size"

class VisitRequestAdmin(admin.ModelAdmin):
    list_display = ('property', 'buyer', 'preferred_date', 'status', 'date_requested')
    list_filter = ('status', 'date_requested', 'preferred_date')
    search_fields = ('property__title', 'buyer__username')
    readonly_fields = ('date_requested',)

class PropertySearchAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'property_type', 'state', 'city', 'date_saved')
    list_filter = ('property_type', 'state', 'date_saved')
    search_fields = ('user__username', 'name', 'city')

admin.site.register(Property, PropertyAdmin)
admin.site.register(PropertyImage, PropertyImageAdmin)
admin.site.register(VisitRequest, VisitRequestAdmin)
admin.site.register(PropertySearch, PropertySearchAdmin)
