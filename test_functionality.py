#!/usr/bin/env python
import os
import sys
import django

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'safeestate.settings')
django.setup()

from django.contrib.auth import get_user_model
from properties.models import VisitRequest

User = get_user_model()

def test_functionality():
    """Test the login and visit request functionality"""
    print("Testing SafeEstate functionality...")
    
    # Check users
    users = User.objects.all()
    print(f"\nTotal users: {users.count()}")
    for user in users:
        print(f"  {user.username} - {user.get_role_display()} - Active: {user.is_active}")
    
    # Check visit requests
    visit_requests = VisitRequest.objects.all()
    print(f"\nTotal visit requests: {visit_requests.count()}")
    
    # Check buyers specifically
    buyers = User.objects.filter(role='buyer')
    print(f"\nBuyers:")
    for buyer in buyers:
        requests = VisitRequest.objects.filter(buyer=buyer)
        print(f"  {buyer.username} has {requests.count()} visit requests")
    
    print("\n✅ Functionality test completed!")

if __name__ == '__main__':
    test_functionality()