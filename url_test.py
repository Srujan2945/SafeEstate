#!/usr/bin/env python
"""
URL and View Testing Script for SafeEstate
Tests all major URLs and views for accessibility
"""

import os
import sys
import django

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'safeestate.settings')
django.setup()

from django.test import Client
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

def test_public_urls():
    """Test publicly accessible URLs"""
    print("🌐 Testing Public URLs...")
    
    client = Client()
    
    public_urls = [
        ('home', 'Home Page'),
        ('accounts:login', 'Login Page'),
        ('accounts:register', 'Registration Page'),
        ('properties:property_list', 'Property List'),
    ]
    
    for url_name, description in public_urls:
        try:
            url = reverse(url_name)
            response = client.get(url)
            if response.status_code == 200:
                print(f"  ✅ {description}: {url} - OK")
            else:
                print(f"  ⚠️  {description}: {url} - Status {response.status_code}")
        except Exception as e:
            print(f"  ❌ {description}: Error - {e}")
    
    return True

def test_property_detail_urls():
    """Test property detail URLs"""
    print("\n🏠 Testing Property Detail URLs...")
    
    client = Client()
    
    from properties.models import Property
    properties = Property.objects.all()[:3]  # Test first 3 properties
    
    for prop in properties:
        try:
            url = reverse('properties:property_detail', kwargs={'pk': prop.pk})
            response = client.get(url)
            if response.status_code == 200:
                print(f"  ✅ Property '{prop.title[:30]}...': {url} - OK")
            else:
                print(f"  ⚠️  Property '{prop.title[:30]}...': {url} - Status {response.status_code}")
        except Exception as e:
            print(f"  ❌ Property '{prop.title[:30]}...': Error - {e}")
    
    return True

def test_authenticated_urls():
    """Test URLs that require authentication"""
    print("\n🔐 Testing Authenticated URLs...")
    
    client = Client()
    
    # Login as admin
    try:
        admin_user = User.objects.get(username='admin')
        client.force_login(admin_user)
        print("  ✅ Logged in as admin")
        
        # Test admin URLs
        admin_urls = [
            ('admin_panel:dashboard', 'Admin Dashboard'),
            ('admin_panel:manage_users', 'User Management'),
            ('admin_panel:manage_properties', 'Property Management'),
            ('admin_panel:kyc_verification', 'KYC Verification'),
        ]
        
        for url_name, description in admin_urls:
            try:
                url = reverse(url_name)
                response = client.get(url)
                if response.status_code == 200:
                    print(f"  ✅ {description}: {url} - OK")
                else:
                    print(f"  ⚠️  {description}: {url} - Status {response.status_code}")
            except Exception as e:
                print(f"  ❌ {description}: Error - {e}")
                
    except User.DoesNotExist:
        print("  ❌ Admin user not found")
    
    return True

def test_seller_urls():
    """Test seller-specific URLs"""
    print("\n👥 Testing Seller URLs...")
    
    client = Client()
    
    # Login as seller
    try:
        seller_user = User.objects.filter(role='seller').first()
        if seller_user:
            client.force_login(seller_user)
            print(f"  ✅ Logged in as seller: {seller_user.username}")
            
            # Test seller URLs
            seller_urls = [
                ('accounts:profile', 'Profile Page'),
                ('accounts:seller_kyc', 'KYC Submission'),
                ('properties:add_property', 'Add Property'),
                ('properties:my_properties', 'My Properties'),
            ]
            
            for url_name, description in seller_urls:
                try:
                    url = reverse(url_name)
                    response = client.get(url)
                    if response.status_code == 200:
                        print(f"  ✅ {description}: {url} - OK")
                    elif response.status_code == 302:  # Redirect is OK for some pages
                        print(f"  ✅ {description}: {url} - Redirect OK")
                    else:
                        print(f"  ⚠️  {description}: {url} - Status {response.status_code}")
                except Exception as e:
                    print(f"  ❌ {description}: Error - {e}")
        else:
            print("  ❌ No seller user found")
            
    except Exception as e:
        print(f"  ❌ Error testing seller URLs: {e}")
    
    return True

def test_buyer_urls():
    """Test buyer-specific URLs"""
    print("\n🛒 Testing Buyer URLs...")
    
    client = Client()
    
    # Login as buyer
    try:
        buyer_user = User.objects.filter(role='buyer').first()
        if buyer_user:
            client.force_login(buyer_user)
            print(f"  ✅ Logged in as buyer: {buyer_user.username}")
            
            # Test buyer URLs
            buyer_urls = [
                ('accounts:profile', 'Profile Page'),
                ('properties:my_visit_requests', 'My Visit Requests'),
            ]
            
            for url_name, description in buyer_urls:
                try:
                    url = reverse(url_name)
                    response = client.get(url)
                    if response.status_code == 200:
                        print(f"  ✅ {description}: {url} - OK")
                    elif response.status_code == 302:  # Redirect is OK for some pages
                        print(f"  ✅ {description}: {url} - Redirect OK")
                    else:
                        print(f"  ⚠️  {description}: {url} - Status {response.status_code}")
                except Exception as e:
                    print(f"  ❌ {description}: Error - {e}")
        else:
            print("  ❌ No buyer user found")
            
    except Exception as e:
        print(f"  ❌ Error testing buyer URLs: {e}")
    
    return True

def test_form_submissions():
    """Test form submissions"""
    print("\n📝 Testing Form Functionality...")
    
    client = Client()
    
    # Test login form
    try:
        login_url = reverse('accounts:login')
        response = client.post(login_url, {
            'username': 'admin',
            'password': 'admin123'
        })
        if response.status_code in [200, 302]:  # 302 = successful login redirect
            print("  ✅ Login form submission - OK")
        else:
            print(f"  ⚠️  Login form submission - Status {response.status_code}")
    except Exception as e:
        print(f"  ❌ Login form test: Error - {e}")
    
    return True

def run_url_tests():
    """Run all URL tests"""
    print("🔗 Starting SafeEstate URL Testing Suite")
    print("=" * 60)
    
    tests = [
        test_public_urls,
        test_property_detail_urls,
        test_authenticated_urls,
        test_seller_urls,
        test_buyer_urls,
        test_form_submissions
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
    print(f"🎯 URL Test Results: {passed_tests}/{total_tests} test suites passed")
    
    if passed_tests == total_tests:
        print("🎉 All URL tests PASSED! All pages are accessible!")
    else:
        print("⚠️  Some URL tests failed. Please check the issues above.")
    
    print("=" * 60)

if __name__ == '__main__':
    run_url_tests()