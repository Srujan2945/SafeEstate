#!/usr/bin/env python
import os
import sys
import django

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'safeestate.settings')
django.setup()

from django.contrib.auth import get_user_model
from accounts.models import SellerKYC
from properties.models import Property, PropertyImage

User = get_user_model()

def create_sample_data():
    print("Creating sample data...")
    
    # Create admin user
    if not User.objects.filter(username='admin').exists():
        admin_user = User.objects.create_user(
            username='admin',
            email='admin@safeestate.com',
            password='admin123',
            role='admin',
            is_staff=True,
            is_superuser=True
        )
        print("✓ Admin user created (username: admin, password: admin123)")
    
    # Create sample seller
    if not User.objects.filter(username='seller1').exists():
        seller1 = User.objects.create_user(
            username='seller1',
            email='seller1@example.com',
            password='seller123',
            role='seller',
            phone='9876543210',
            address='123 Main Street, Mumbai',
            is_verified=True
        )
        print("✓ Seller user created (username: seller1, password: seller123)")
        
        # Create KYC for seller (approved)
        SellerKYC.objects.create(
            seller=seller1,
            status='approved',
            remarks='Documents verified successfully'
        )
        print("✓ KYC created for seller1")
    
    # Create sample buyer
    if not User.objects.filter(username='buyer1').exists():
        buyer1 = User.objects.create_user(
            username='buyer1',
            email='buyer1@example.com',
            password='buyer123',
            role='buyer',
            phone='9876543211',
            address='456 Oak Avenue, Delhi',
            is_verified=True
        )
        print("✓ Buyer user created (username: buyer1, password: buyer123)")
    
    # Create sample properties
    if not Property.objects.exists():
        seller1 = User.objects.get(username='seller1')
        
        properties_data = [
            {
                'title': '3BHK Luxury Apartment in Mumbai',
                'description': 'Beautiful 3BHK apartment with modern amenities, located in prime area of Mumbai. Close to schools, hospitals, and shopping centers.',
                'price': 8500000,
                'property_type': 'flat',
                'state': 'maharashtra',
                'city': 'Mumbai',
                'pincode': '400001',
                'address': 'Bandra West, Mumbai',
                'area': 1200,
                'bedrooms': 3,
                'bathrooms': 2,
            },
            {
                'title': '2BHK Independent House in Delhi',
                'description': 'Spacious 2BHK independent house with parking space and small garden. Perfect for families.',
                'price': 6500000,
                'property_type': 'house',
                'state': 'delhi',
                'city': 'New Delhi',
                'pincode': '110001',
                'address': 'Connaught Place, New Delhi',
                'area': 1000,
                'bedrooms': 2,
                'bathrooms': 2,
            },
            {
                'title': 'Commercial Plot in Bangalore',
                'description': 'Prime commercial plot suitable for office complex or retail space. Located in IT corridor.',
                'price': 15000000,
                'property_type': 'commercial',
                'state': 'karnataka',
                'city': 'Bangalore',
                'pincode': '560001',
                'address': 'Electronic City, Bangalore',
                'area': 2000,
                'bedrooms': None,
                'bathrooms': None,
            },
            {
                'title': 'Residential Plot in Pune',
                'description': 'Ready to construct residential plot in developing area of Pune. All utilities available.',
                'price': 3500000,
                'property_type': 'plot',
                'state': 'maharashtra',
                'city': 'Pune',
                'pincode': '411001',
                'address': 'Hinjewadi, Pune',
                'area': 800,
                'bedrooms': None,
                'bathrooms': None,
            },
            {
                'title': '1BHK Compact Flat in Chennai',
                'description': 'Compact and efficient 1BHK flat perfect for bachelors or small families. Good connectivity.',
                'price': 2500000,
                'property_type': 'flat',
                'state': 'tamil_nadu',
                'city': 'Chennai',
                'pincode': '600001',
                'address': 'T Nagar, Chennai',
                'area': 600,
                'bedrooms': 1,
                'bathrooms': 1,
            }
        ]
        
        for prop_data in properties_data:
            property_obj = Property.objects.create(
                seller=seller1,
                **prop_data
            )
            print(f"✓ Property created: {property_obj.title}")
    
    print("\n✅ Sample data creation completed!")
    print("\nLogin credentials:")
    print("Admin: username=admin, password=admin123")
    print("Seller: username=seller1, password=seller123")
    print("Buyer: username=buyer1, password=buyer123")

if __name__ == '__main__':
    create_sample_data()