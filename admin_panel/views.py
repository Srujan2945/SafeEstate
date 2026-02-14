from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from accounts.models import SellerKYC
from properties.models import Property, VisitRequest, PropertyImage
from django.db.models import Count, Q
import requests
import uuid
from django.core.files.base import ContentFile

User = get_user_model()

def admin_required(view_func):
    """Decorator to ensure only admin users can access admin views"""
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.role != 'admin':
            messages.error(request, 'Access denied. Admin privileges required.')
            return redirect('properties:property_list')
        return view_func(request, *args, **kwargs)
    return wrapper

@login_required
@admin_required
def dashboard(request):
    # Get statistics
    total_users = User.objects.count()
    total_buyers = User.objects.filter(role='buyer').count()
    total_sellers = User.objects.filter(role='seller').count()
    total_properties = Property.objects.count()
    available_properties = Property.objects.filter(status='available').count()
    
    # KYC Statistics
    pending_kycs = SellerKYC.objects.filter(status='pending').count()
    approved_kycs = SellerKYC.objects.filter(status='approved').count()
    rejected_kycs = SellerKYC.objects.filter(status='rejected').count()
    
    # Recent activities
    recent_users = User.objects.order_by('-date_joined')[:5]
    recent_properties = Property.objects.order_by('-date_created')[:5]
    recent_kycs = SellerKYC.objects.order_by('-date_submitted')[:5]
    
    context = {
        'total_users': total_users,
        'total_buyers': total_buyers,
        'total_sellers': total_sellers,
        'total_properties': total_properties,
        'available_properties': available_properties,
        'pending_kycs': pending_kycs,
        'approved_kycs': approved_kycs,
        'rejected_kycs': rejected_kycs,
        'recent_users': recent_users,
        'recent_properties': recent_properties,
        'recent_kycs': recent_kycs,
    }
    
    return render(request, 'admin_panel/dashboard.html', context)

@login_required
@admin_required
def manage_users(request):
    users = User.objects.all().order_by('-date_joined')
    
    # Get filter parameters
    role_filter = request.GET.get('role')
    status_filter = request.GET.get('status')
    verification_filter = request.GET.get('verification')
    search_query = request.GET.get('search')
    
    # Apply filters
    if role_filter and role_filter != '':
        users = users.filter(role=role_filter)
    
    if status_filter and status_filter != '':
        if status_filter == 'active':
            users = users.filter(is_active=True)
        elif status_filter == 'inactive':
            users = users.filter(is_active=False)
    
    if verification_filter and verification_filter != '':
        if verification_filter == 'verified':
            users = users.filter(is_verified=True)
        elif verification_filter == 'unverified':
            users = users.filter(is_verified=False)
    
    if search_query and search_query.strip():
        users = users.filter(
            Q(username__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(users, 20)  # Show 20 users per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'users': page_obj,  # For backward compatibility
        'role_filter': role_filter,
        'status_filter': status_filter,
        'verification_filter': verification_filter,
        'search_query': search_query,
        'total_count': paginator.count,
    }
    
    return render(request, 'admin_panel/manage_users.html', context)

@login_required
@admin_required
def manage_properties(request):
    properties = Property.objects.all().order_by('-date_created')
    
    # Get filter parameters
    status_filter = request.GET.get('status')
    property_type_filter = request.GET.get('property_type')
    state_filter = request.GET.get('state')
    city_filter = request.GET.get('city')
    search_query = request.GET.get('search')
    seller_filter = request.GET.get('seller')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    
    # Apply filters
    if status_filter and status_filter != '':
        properties = properties.filter(status=status_filter)
    
    if property_type_filter and property_type_filter != '':
        properties = properties.filter(property_type=property_type_filter)
    
    if state_filter and state_filter != '':
        properties = properties.filter(state=state_filter)
    
    if city_filter and city_filter.strip():
        properties = properties.filter(city__icontains=city_filter)
    
    if seller_filter and seller_filter.strip():
        properties = properties.filter(seller__username__icontains=seller_filter)
    
    if search_query and search_query.strip():
        properties = properties.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(address__icontains=search_query) |
            Q(city__icontains=search_query)
        )
    
    if min_price and min_price.strip():
        try:
            properties = properties.filter(price__gte=float(min_price))
        except ValueError:
            pass
    
    if max_price and max_price.strip():
        try:
            properties = properties.filter(price__lte=float(max_price))
        except ValueError:
            pass
    
    # Get unique states and cities for dropdowns
    from properties.models import INDIAN_STATES
    states = INDIAN_STATES
    
    # Pagination
    paginator = Paginator(properties, 12)  # Show 12 properties per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'properties': page_obj,  # For backward compatibility
        'status_filter': status_filter,
        'property_type_filter': property_type_filter,
        'state_filter': state_filter,
        'city_filter': city_filter,
        'search_query': search_query,
        'seller_filter': seller_filter,
        'min_price': min_price,
        'max_price': max_price,
        'states': states,
        'total_count': paginator.count,
    }
    
    return render(request, 'admin_panel/manage_properties.html', context)

@login_required
@admin_required
def kyc_verification(request):
    kycs = SellerKYC.objects.all().order_by('-date_submitted')
    
    # Get filter parameters
    status_filter = request.GET.get('status')
    completion_filter = request.GET.get('completion')
    search_query = request.GET.get('search')
    date_filter = request.GET.get('date_filter')
    
    # Apply filters
    if status_filter and status_filter != '':
        kycs = kycs.filter(status=status_filter)
    
    if completion_filter and completion_filter != '':
        if completion_filter == 'complete':
            # Filter KYCs that have all required documents
            kycs = kycs.exclude(
                Q(pan_card='') | Q(pan_card__isnull=True) |
                Q(aadhaar_card='') | Q(aadhaar_card__isnull=True) |
                Q(ownership_proof='') | Q(ownership_proof__isnull=True) |
                Q(revenue_records='') | Q(revenue_records__isnull=True) |
                Q(tax_receipt='') | Q(tax_receipt__isnull=True) |
                Q(encumbrance_certificate='') | Q(encumbrance_certificate__isnull=True)
            )
        elif completion_filter == 'incomplete':
            # Filter KYCs that are missing required documents
            kycs = kycs.filter(
                Q(pan_card='') | Q(pan_card__isnull=True) |
                Q(aadhaar_card='') | Q(aadhaar_card__isnull=True) |
                Q(ownership_proof='') | Q(ownership_proof__isnull=True) |
                Q(revenue_records='') | Q(revenue_records__isnull=True) |
                Q(tax_receipt='') | Q(tax_receipt__isnull=True) |
                Q(encumbrance_certificate='') | Q(encumbrance_certificate__isnull=True)
            )
    
    if search_query and search_query.strip():
        kycs = kycs.filter(
            Q(seller__username__icontains=search_query) |
            Q(seller__email__icontains=search_query) |
            Q(seller__first_name__icontains=search_query) |
            Q(seller__last_name__icontains=search_query)
        )
    
    if date_filter and date_filter != '':
        from datetime import datetime, timedelta
        today = timezone.now().date()
        
        if date_filter == 'today':
            kycs = kycs.filter(date_submitted__date=today)
        elif date_filter == 'week':
            week_ago = today - timedelta(days=7)
            kycs = kycs.filter(date_submitted__date__gte=week_ago)
        elif date_filter == 'month':
            month_ago = today - timedelta(days=30)
            kycs = kycs.filter(date_submitted__date__gte=month_ago)
    
    # Pagination
    paginator = Paginator(kycs, 15)  # Show 15 KYCs per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'kycs': page_obj,  # For backward compatibility
        'status_filter': status_filter,
        'completion_filter': completion_filter,
        'search_query': search_query,
        'date_filter': date_filter,
        'total_count': paginator.count,
    }
    
    return render(request, 'admin_panel/kyc_verification.html', context)

@login_required
@admin_required
def kyc_detail(request, pk):
    kyc = get_object_or_404(SellerKYC, pk=pk)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        remarks = request.POST.get('remarks', '')
        
        if action in ['approved', 'rejected']:
            kyc.status = action
            kyc.remarks = remarks
            kyc.verified_by = request.user
            kyc.date_verified = timezone.now()
            kyc.save()
            
            # Update seller verification status
            if action == 'approved':
                kyc.seller.is_verified = True
                kyc.seller.save()
                messages.success(request, f'KYC for {kyc.seller.username} has been approved.')
            else:
                kyc.seller.is_verified = False
                kyc.seller.save()
                messages.success(request, f'KYC for {kyc.seller.username} has been rejected.')
            
            return redirect('admin_panel:kyc_verification')
    
    context = {
        'kyc': kyc,
    }
    
    return render(request, 'admin_panel/kyc_detail.html', context)

@login_required
@admin_required
def toggle_user_status(request, pk):
    user = get_object_or_404(User, pk=pk)
    
    if request.method == 'POST':
        user.is_active = not user.is_active
        user.save()
        
        status = 'activated' if user.is_active else 'deactivated'
        messages.success(request, f'User {user.username} has been {status}.')
    
    return redirect('admin_panel:manage_users')

@login_required
@admin_required
def toggle_property_status(request, pk):
    property_obj = get_object_or_404(Property, pk=pk)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in ['available', 'sold', 'pending']:
            property_obj.status = new_status
            property_obj.save()
            messages.success(request, f'Property status updated to {new_status}.')
    
    return redirect('admin_panel:manage_properties')

@login_required
@admin_required
def manage_property_images(request):
    """Admin view for comprehensive property image management"""
    properties = Property.objects.all().order_by('-date_created')
    
    # Apply filters
    property_type_filter = request.GET.get('property_type')
    status_filter = request.GET.get('status')
    search_query = request.GET.get('search')
    image_status_filter = request.GET.get('image_status')
    
    if property_type_filter:
        properties = properties.filter(property_type=property_type_filter)
    
    if status_filter:
        properties = properties.filter(status=status_filter)
    
    if search_query:
        properties = properties.filter(
            Q(title__icontains=search_query) |
            Q(city__icontains=search_query) |
            Q(seller__username__icontains=search_query)
        )
    
    if image_status_filter:
        if image_status_filter == 'with_images':
            properties = properties.filter(images__isnull=False).distinct()
        elif image_status_filter == 'without_images':
            properties = properties.filter(images__isnull=True)
    
    # Pagination
    paginator = Paginator(properties, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get image statistics
    total_properties = Property.objects.count()
    properties_with_images = Property.objects.filter(images__isnull=False).distinct().count()
    properties_without_images = total_properties - properties_with_images
    total_images = PropertyImage.objects.count()
    
    context = {
        'page_obj': page_obj,
        'properties': page_obj,
        'property_type_filter': property_type_filter,
        'status_filter': status_filter,
        'search_query': search_query,
        'image_status_filter': image_status_filter,
        'total_properties': total_properties,
        'properties_with_images': properties_with_images,
        'properties_without_images': properties_without_images,
        'total_images': total_images,
    }
    
    return render(request, 'admin_panel/manage_property_images.html', context)

@login_required
@admin_required
def bulk_assign_images(request):
    """Handle bulk image operations and file uploads"""
    if request.method == 'POST':
        try:
            # Handle JSON requests (for bulk operations)
            if request.content_type == 'application/json':
                import json
                data = json.loads(request.body)
                action = data.get('action')
                property_ids = data.get('property_ids', [])
                
                if action == 'assign_unique':
                    properties = Property.objects.filter(id__in=property_ids)
                    success_count = assign_unique_images_to_properties(properties)
                    return JsonResponse({
                        'success': True, 
                        'message': f'Successfully assigned unique images to {success_count} properties.',
                        'updated_count': success_count
                    })
                
                elif action == 'remove_all':
                    properties = Property.objects.filter(id__in=property_ids)
                    total_removed = 0
                    for prop in properties:
                        count = prop.images.count()
                        prop.images.all().delete()
                        total_removed += count
                    return JsonResponse({
                        'success': True,
                        'message': f'Removed {total_removed} images from {properties.count()} properties.',
                        'updated_count': properties.count()
                    })
                
                elif action == 'assign_placeholder':
                    properties = Property.objects.filter(id__in=property_ids)
                    success_count = assign_placeholder_images_to_properties(properties)
                    return JsonResponse({
                        'success': True,
                        'message': f'Assigned placeholder images to {success_count} properties.',
                        'updated_count': success_count
                    })
                
                elif action == 'remove_specific':
                    image_id = data.get('image_id')
                    try:
                        image = PropertyImage.objects.get(id=image_id)
                        image.delete()
                        return JsonResponse({
                            'success': True,
                            'message': 'Image removed successfully.'
                        })
                    except PropertyImage.DoesNotExist:
                        return JsonResponse({
                            'success': False,
                            'message': 'Image not found.'
                        })
            
            # Handle form data requests (for file uploads)
            else:
                action = request.POST.get('action')
                
                if action == 'upload':
                    property_ids_str = request.POST.get('property_ids', '')
                    if ',' in property_ids_str:
                        property_ids = [int(id.strip()) for id in property_ids_str.split(',') if id.strip().isdigit()]
                    else:
                        property_ids = [int(property_ids_str)] if property_ids_str.isdigit() else []
                    
                    uploaded_files = request.FILES.getlist('images')
                    
                    if not property_ids or not uploaded_files:
                        return JsonResponse({
                            'success': False,
                            'message': 'No properties selected or no files uploaded.'
                        })
                    
                    properties = Property.objects.filter(id__in=property_ids)
                    success_count = 0
                    
                    # Distribute images among selected properties
                    for i, uploaded_file in enumerate(uploaded_files):
                        property_obj = properties[i % len(properties)]
                        
                        # Validate file type
                        if not uploaded_file.content_type.startswith('image/'):
                            continue
                        
                        # Create PropertyImage
                        property_image = PropertyImage(
                            property=property_obj,
                            caption=f"Uploaded image for {property_obj.title}",
                            is_primary=not property_obj.images.exists()  # First image is primary
                        )
                        property_image.image.save(uploaded_file.name, uploaded_file, save=True)
                        success_count += 1
                    
                    return JsonResponse({
                        'success': True,
                        'message': f'Successfully uploaded {success_count} images.',
                        'updated_count': len(properties)
                    })
        
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Error: {str(e)}'
            })
    
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})

def assign_unique_images_to_properties(properties):
    """Helper function to assign unique images to properties"""
    image_pool = [
        'https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?w=800&h=600&fit=crop',
        'https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=800&h=600&fit=crop',
        'https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=800&h=600&fit=crop',
        'https://images.unsplash.com/photo-1570129477492-45c003edd2be?w=800&h=600&fit=crop',
        'https://images.unsplash.com/photo-1582268611958-ebfd161ef9cf?w=800&h=600&fit=crop',
        'https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=800&h=600&fit=crop',
        'https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=800&h=600&fit=crop',
        'https://images.unsplash.com/photo-1560472354-b33ff0c44a43?w=800&h=600&fit=crop',
        'https://images.unsplash.com/photo-1497366216548-37526070297c?w=800&h=600&fit=crop',
        'https://images.unsplash.com/photo-1500382017468-9049fed747ef?w=800&h=600&fit=crop',
        'https://images.unsplash.com/photo-1500534314209-a25ddb2bd429?w=800&h=600&fit=crop',
        'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800&h=600&fit=crop',
        'https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?w=800&h=600&fit=crop',
        'https://images.unsplash.com/photo-1564013799919-ab600027ffc6?w=800&h=600&fit=crop',
        'https://images.unsplash.com/photo-1481026469463-66327c86e544?w=800&h=600&fit=crop',
        'https://images.unsplash.com/photo-1442544213729-6a15f1611937?w=800&h=600&fit=crop',
        'https://images.unsplash.com/photo-1449824913935-59a10b8d2000?w=800&h=600&fit=crop',
        'https://images.unsplash.com/photo-1518780664697-55e3ad937233?w=800&h=600&fit=crop',
        'https://images.unsplash.com/photo-1571896349842-33c89424de2d?w=800&h=600&fit=crop',
        'https://images.unsplash.com/photo-1572120360610-d971b9d7767c?w=800&h=600&fit=crop',
    ]
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    success_count = 0
    for i, property_obj in enumerate(properties):
        try:
            # Remove existing images
            property_obj.images.all().delete()
            
            # Select unique image
            image_url = image_pool[i % len(image_pool)]
            
            # Download and save
            response = requests.get(image_url, headers=headers, timeout=10)
            response.raise_for_status()
            
            filename = f"admin_bulk_{property_obj.id}_{uuid.uuid4().hex[:8]}.jpg"
            property_image = PropertyImage(
                property=property_obj,
                caption=f"Professional image for {property_obj.title}",
                is_primary=True
            )
            property_image.image.save(filename, ContentFile(response.content), save=True)
            success_count += 1
        except:
            continue
    
    return success_count

def assign_placeholder_images_to_properties(properties):
    """Helper function to assign placeholder images to properties"""
    placeholder_url = "https://images.unsplash.com/photo-1560518883-ce09059eeffa?w=800&h=600&fit=crop"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    success_count = 0
    for property_obj in properties:
        if not property_obj.images.exists():
            try:
                response = requests.get(placeholder_url, headers=headers, timeout=10)
                response.raise_for_status()
                
                filename = f"placeholder_{property_obj.id}_{uuid.uuid4().hex[:6]}.jpg"
                property_image = PropertyImage(
                    property=property_obj,
                    caption=f"Placeholder for {property_obj.title}",
                    is_primary=True
                )
                property_image.image.save(filename, ContentFile(response.content), save=True)
                success_count += 1
            except:
                continue
    
    return success_count
