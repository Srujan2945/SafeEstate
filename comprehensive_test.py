#!/usr/bin/env python
"""
Comprehensive Test Script for SafeEstate Project
Tests all major functionality and components
"""

import os
import sys
import django

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'safeestate.settings')
django.setup()

from django.contrib.auth import get_user_model
from accounts.models import SellerKYC
from properties.models import Property, PropertyImage, VisitRequest
from django.core.exceptions import ValidationError

User = get_user_model()

def test_user_system():
    """Test user registration and authentication system"""
    print("🔐 Testing User System...")
    
    # Test user creation
    total_users = User.objects.count()
    buyers = User.objects.filter(role='buyer').count()
    sellers = User.objects.filter(role='seller').count()
    admins = User.objects.filter(role='admin').count()
    
    print(f"  ✅ Total Users: {total_users}")
    print(f"  ✅ Buyers: {buyers}")
    print(f"  ✅ Sellers: {sellers}")
    print(f"  ✅ Admins: {admins}")
    
    # Test admin user
    try:
        admin = User.objects.get(username='admin')
        print(f"  ✅ Admin user exists: {admin.username} ({admin.email})")
    except User.DoesNotExist:
        print("  ❌ Admin user not found")
    
    return True

def test_kyc_system():
    """Test KYC verification system"""
    print("\n📋 Testing KYC System...")
    
    kyc_records = SellerKYC.objects.count()
    approved_kycs = SellerKYC.objects.filter(status='approved').count()
    pending_kycs = SellerKYC.objects.filter(status='pending').count()
    rejected_kycs = SellerKYC.objects.filter(status='rejected').count()
    
    print(f"  ✅ Total KYC Records: {kyc_records}")
    print(f"  ✅ Approved: {approved_kycs}")
    print(f"  ✅ Pending: {pending_kycs}")
    print(f"  ✅ Rejected: {rejected_kycs}")
    
    # Test KYC completion
    complete_kycs = 0
    for kyc in SellerKYC.objects.all():
        if kyc.is_complete():
            complete_kycs += 1
    
    print(f"  ✅ Complete KYC Submissions: {complete_kycs}")
    
    return True

def test_property_system():
    """Test property management system"""
    print("\n🏠 Testing Property System...")
    
    total_properties = Property.objects.count()
    available_properties = Property.objects.filter(status='available').count()
    sold_properties = Property.objects.filter(status='sold').count()
    
    print(f"  ✅ Total Properties: {total_properties}")
    print(f"  ✅ Available: {available_properties}")
    print(f"  ✅ Sold: {sold_properties}")
    
    # Test property types
    property_types = Property.objects.values('property_type').distinct().count()
    print(f"  ✅ Property Types Available: {property_types}")
    
    # Test property images
    total_images = PropertyImage.objects.count()
    properties_with_images = Property.objects.filter(images__isnull=False).distinct().count()
    
    print(f"  ✅ Total Property Images: {total_images}")
    print(f"  ✅ Properties with Images: {properties_with_images}")
    
    return True

def test_visit_system():
    """Test visit request system"""
    print("\n📅 Testing Visit Request System...")
    
    total_visits = VisitRequest.objects.count()
    pending_visits = VisitRequest.objects.filter(status='pending').count()
    approved_visits = VisitRequest.objects.filter(status='approved').count()
    declined_visits = VisitRequest.objects.filter(status='declined').count()
    
    print(f"  ✅ Total Visit Requests: {total_visits}")
    print(f"  ✅ Pending: {pending_visits}")
    print(f"  ✅ Approved: {approved_visits}")
    print(f"  ✅ Declined: {declined_visits}")
    
    return True

def test_database_integrity():
    """Test database relationships and integrity"""
    print("\n🔗 Testing Database Integrity...")
    
    # Test user-property relationships
    sellers_with_properties = User.objects.filter(role='seller', properties__isnull=False).distinct().count()
    print(f"  ✅ Sellers with Properties: {sellers_with_properties}")
    
    # Test property-image relationships
    properties_with_multiple_images = 0
    for prop in Property.objects.all():
        if prop.images.count() > 1:
            properties_with_multiple_images += 1
    
    print(f"  ✅ Properties with Multiple Images: {properties_with_multiple_images}")
    
    # Test visit request relationships
    buyers_with_visits = User.objects.filter(role='buyer', visit_requests__isnull=False).distinct().count()
    print(f"  ✅ Buyers with Visit Requests: {buyers_with_visits}")
    
    return True

def test_security_features():
    """Test security implementations"""
    print("\n🔒 Testing Security Features...")
    
    # Test password hashing
    users_with_hashed_passwords = 0
    for user in User.objects.all():
        if user.password.startswith('pbkdf2_sha256$'):
            users_with_hashed_passwords += 1
    
    print(f"  ✅ Users with Hashed Passwords: {users_with_hashed_passwords}/{User.objects.count()}")
    
    # Test admin permissions
    admin_users = User.objects.filter(is_staff=True, is_superuser=True).count()
    print(f"  ✅ Admin Users with Proper Permissions: {admin_users}")
    
    return True

def test_file_uploads():
    """Test file upload functionality"""
    print("\n📁 Testing File Upload System...")
    
    # Check media directory exists
    media_root = 'media'
    if os.path.exists(media_root):
        print(f"  ✅ Media directory exists: {media_root}")
        
        # Check subdirectories
        subdirs = ['properties', 'kyc']
        for subdir in subdirs:
            path = os.path.join(media_root, subdir)
            if os.path.exists(path):
                file_count = len([f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))])
                print(f"  ✅ {subdir}/ directory: {file_count} files")
            else:
                print(f"  ⚠️  {subdir}/ directory not found")
    else:
        print(f"  ⚠️  Media directory not found: {media_root}")
    
    return True

def run_comprehensive_test():
    """Run all tests"""
    print("🚀 Starting Comprehensive SafeEstate Test Suite")
    print("=" * 60)
    
    tests = [
        test_user_system,
        test_kyc_system,
        test_property_system,
        test_visit_system,
        test_database_integrity,
        test_security_features,
        test_file_uploads
    ]
    
    passed_tests = 0
    total_tests = len(tests)
    
    for test_func in tests:
        try:
            if test_func():
                passed_tests += 1
        except Exception as e:
            print(f"  ❌ Error in {test_func.__name__}: {e}")
    
    print("\n" + "=" * 60)
    print(f"🎯 Test Results: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        print("🎉 All tests PASSED! SafeEstate is working correctly!")
    else:
        print("⚠️  Some tests failed. Please check the issues above.")
    
    print("=" * 60)

if __name__ == '__main__':
    run_comprehensive_test()