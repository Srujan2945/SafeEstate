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

def interactive_image_assignment():
    """Interactive tool to assign your images to properties"""
    print("Interactive Property Image Assignment Tool")
    print("=" * 50)
    
    # Get available image files
    media_dir = 'media/properties'
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif']
    available_images = []
    
    if os.path.exists(media_dir):
        for file in os.listdir(media_dir):
            if any(file.lower().endswith(ext) for ext in image_extensions):
                available_images.append(file)
    
    if not available_images:
        print("No image files found in media/properties/")
        print("Please place your image files there first.")
        return
    
    print(f"Found {len(available_images)} image files:")
    for i, img in enumerate(available_images, 1):
        file_size = os.path.getsize(os.path.join(media_dir, img)) / 1024
        print(f"  {i:2d}. {img} ({file_size:.1f} KB)")
    
    print("\nProperties that need images:")
    properties = Property.objects.all().order_by('id')
    
    for prop in properties:
        current_image = "None"
        if prop.images.exists():
            current_image = prop.images.first().image.name.split('/')[-1]
        
        print(f"  {prop.id:2d}. {prop.title[:40]:<40} [Current: {current_image}]")
        print(f"      {prop.city}, {prop.get_state_display()} - {prop.get_property_type_display()}")
    
    print(f"\nInteractive Assignment:")
    print(f"Enter 'property_id:image_number' (e.g., '1:5' to assign image 5 to property 1)")
    print(f"Enter 'auto' for automatic assignment based on filenames")
    print(f"Enter 'quit' to exit")
    
    while True:
        try:
            user_input = input(f"\nCommand: ").strip().lower()
            
            if user_input == 'quit':
                break
            elif user_input == 'auto':
                auto_assign_by_filename(available_images, properties)
                break
            elif ':' in user_input:
                prop_id, img_num = user_input.split(':')
                prop_id = int(prop_id)
                img_num = int(img_num)
                
                if 1 <= prop_id <= len(properties) and 1 <= img_num <= len(available_images):
                    assign_single_image(properties[prop_id-1], available_images[img_num-1])
                else:
                    print("Invalid property ID or image number")
            else:
                print("Invalid format. Use 'property_id:image_number' or 'auto' or 'quit'")
                
        except ValueError:
            print("Please enter numbers for property ID and image number")
        except Exception as e:
            print(f"Error: {e}")

def auto_assign_by_filename(available_images, properties):
    """Automatically assign images based on filename matching"""
    print("\nAutomatic assignment based on filename matching...")
    
    success_count = 0
    
    for prop in properties:
        best_match = None
        best_score = 0
        
        # Create search terms from property info
        search_terms = [
            prop.city.lower().replace(' ', ''),
            prop.get_property_type_display().lower(),
            str(prop.id),
            # Extract key words from title
            *[word.lower() for word in prop.title.split() if len(word) > 3]
        ]
        
        # Find best matching image
        for img_file in available_images:
            img_lower = img_file.lower()
            score = 0
            
            for term in search_terms:
                if term in img_lower:
                    score += 1
            
            if score > best_score:
                best_score = score
                best_match = img_file
        
        # If no good match, try simple patterns
        if best_score == 0:
            for img_file in available_images:
                img_lower = img_file.lower()
                # Check for property ID in filename
                if str(prop.id) in img_file:
                    best_match = img_file
                    break
                # Check for sequential naming
                elif f"property{prop.id}" in img_lower or f"prop{prop.id}" in img_lower:
                    best_match = img_file
                    break
        
        # Assign the best match
        if best_match:
            if assign_single_image(prop, best_match):
                success_count += 1
                # Remove from available list to avoid duplicates
                available_images.remove(best_match)
    
    print(f"\nAutomatic assignment completed:")
    print(f"  Successfully assigned: {success_count}")
    print(f"  Total properties: {len(properties)}")

def assign_single_image(property_obj, image_filename):
    """Assign a single image to a property"""
    try:
        image_path = os.path.join('media/properties', image_filename)
        
        # Remove existing images
        property_obj.images.all().delete()
        
        # Create new PropertyImage
        with open(image_path, 'rb') as img_file:
            property_image = PropertyImage(
                property=property_obj,
                caption=f"Image for {property_obj.title}",
                is_primary=True
            )
            property_image.image.save(
                image_filename,
                File(img_file),
                save=True
            )
        
        print(f"SUCCESS: {property_obj.title[:35]:<35} <- {image_filename}")
        return True
        
    except Exception as e:
        print(f"ERROR: {property_obj.title[:35]:<35} - {e}")
        return False

if __name__ == '__main__':
    interactive_image_assignment()