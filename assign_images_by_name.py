#!/usr/bin/env python
import os
import sys
import django

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'safeestate.settings')
django.setup()

from properties.models import Property, PropertyImage
from django.core.files import File

def assign_images_by_name():
    """Assign images to properties based on naming convention"""
    print("Assigning Images Based on Your Naming Convention...")
    print("=" * 60)
    
    media_dir = 'media/properties'
    properties = Property.objects.all().order_by('id')
    
    # Suggested naming mapping based on property characteristics
    name_mapping = {
        1: "flat_mumbai_1.jpg",
        2: "house_new_delhi_2.jpg", 
        3: "commercial_bangalore_3.jpg",
        4: "plot_pune_4.jpg",
        5: "flat_chennai_5.jpg",
        6: "flat_pune_6.jpg",
        7: "villa_gurgaon_7.jpg",
        8: "flat_hyderabad_8.jpg",
        9: "commercial_chennai_9.jpg",
        10: "plot_noida_10.jpg",
        11: "beachfront_kochi_11.jpg",
        12: "heritage_jaipur_12.jpg",
        13: "commercial_bangalore_13.jpg",
        14: "villa_shimla_14.jpg",
        15: "penthouse_mumbai_15.jpg",
        16: "farmhouse_lonavala_16.jpg",
        17: "plot_ahmedabad_17.jpg",
        18: "flat_chandigarh_18.jpg",
        19: "beachfront_panaji_19.jpg",
        20: "house_dehradun_20.jpg",
        21: "cottage_rishikesh_21.jpg"
    }
    
    success_count = 0
    total_count = len(properties)
    
    for prop in properties:
        suggested_name = name_mapping.get(prop.id)
        if not suggested_name:
            print(f"No suggested name for property {prop.id}")
            continue
        
        # Look for the image file
        image_path = os.path.join(media_dir, suggested_name)
        
        if os.path.exists(image_path):
            try:
                # Remove existing images
                prop.images.all().delete()
                
                # Create new PropertyImage
                with open(image_path, 'rb') as img_file:
                    property_image = PropertyImage(
                        property=prop,
                        caption=f"Image for {prop.title}",
                        is_primary=True
                    )
                    property_image.image.save(
                        suggested_name,
                        File(img_file),
                        save=True
                    )
                
                print(f"SUCCESS: {prop.id:2d}. {prop.title[:35]:<35} <- {suggested_name}")
                success_count += 1
                
            except Exception as e:
                print(f"ERROR: {prop.id:2d}. {prop.title[:35]:<35} - {e}")
        else:
            print(f"MISSING: {prop.id:2d}. {prop.title[:35]:<35} - File not found: {suggested_name}")
    
    print(f"\nResults:")
    print(f"  Successfully assigned: {success_count}")
    print(f"  Total properties: {total_count}")
    print(f"  Success rate: {(success_count/total_count)*100:.1f}%")
    
    if success_count < total_count:
        print(f"\nMissing images - place these files in media/properties/:")
        for prop in properties:
            suggested_name = name_mapping.get(prop.id)
            image_path = os.path.join(media_dir, suggested_name)
            if not os.path.exists(image_path):
                print(f"  {suggested_name}")

if __name__ == '__main__':
    assign_images_by_name()