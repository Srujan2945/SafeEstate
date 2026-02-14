from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone
from .models import Property, PropertyImage, VisitRequest
from .forms import (
    PropertyForm, PropertyImageUploadForm, PropertySearchForm,
    VisitRequestForm, VisitResponseForm
)

def property_list(request):
    properties = Property.objects.filter(status='available').order_by('-date_created')
    search_form = PropertySearchForm()
    
    # Handle search
    if request.GET:
        search_form = PropertySearchForm(request.GET)
        if search_form.is_valid():
            filters = Q(status='available')
            
            if search_form.cleaned_data.get('property_type'):
                filters &= Q(property_type=search_form.cleaned_data['property_type'])
            
            if search_form.cleaned_data.get('state'):
                filters &= Q(state=search_form.cleaned_data['state'])
            
            if search_form.cleaned_data.get('city'):
                filters &= Q(city__icontains=search_form.cleaned_data['city'])
            
            if search_form.cleaned_data.get('pincode'):
                filters &= Q(pincode=search_form.cleaned_data['pincode'])
            
            if search_form.cleaned_data.get('min_price'):
                filters &= Q(price__gte=search_form.cleaned_data['min_price'])
            
            if search_form.cleaned_data.get('max_price'):
                filters &= Q(price__lte=search_form.cleaned_data['max_price'])
            
            if search_form.cleaned_data.get('min_area'):
                filters &= Q(area__gte=search_form.cleaned_data['min_area'])
            
            if search_form.cleaned_data.get('max_area'):
                filters &= Q(area__lte=search_form.cleaned_data['max_area'])
            
            properties = Property.objects.filter(filters).order_by('-date_created')
    
    # Pagination
    paginator = Paginator(properties, 12)  # Show 12 properties per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_form': search_form,
        'total_properties': properties.count(),
    }
    
    return render(request, 'properties/property_list.html', context)

def property_detail(request, pk):
    property_obj = get_object_or_404(Property, pk=pk)
    visit_requests = None
    
    # If user is the seller, show visit requests
    if request.user.is_authenticated and request.user == property_obj.seller:
        visit_requests = VisitRequest.objects.filter(property=property_obj).order_by('-date_requested')
    
    context = {
        'property': property_obj,
        'visit_requests': visit_requests,
    }
    
    return render(request, 'properties/property_detail.html', context)

@login_required
def add_property(request):
    if request.user.role != 'seller':
        messages.error(request, 'Only sellers can add properties.')
        return redirect('properties:property_list')
    
    # Check if seller is verified
    if not hasattr(request.user, 'kyc') or request.user.kyc.status != 'approved':
        messages.error(request, 'Please complete KYC verification before listing properties.')
        return redirect('accounts:seller_kyc')
    
    if request.method == 'POST':
        property_form = PropertyForm(request.POST)
        image_form = PropertyImageUploadForm(request.POST, request.FILES)
        
        if property_form.is_valid() and image_form.is_valid():
            property_obj = property_form.save(commit=False)
            property_obj.seller = request.user
            property_obj.save()
            
            # Handle single image upload
            if request.FILES.get('image'):
                PropertyImage.objects.create(
                    property=property_obj,
                    image=request.FILES['image'],
                    is_primary=True
                )
            
            messages.success(request, 'Property listed successfully!')
            return redirect('properties:property_detail', pk=property_obj.pk)
    else:
        property_form = PropertyForm()
        image_form = PropertyImageUploadForm()
    
    context = {
        'property_form': property_form,
        'image_form': image_form,
    }
    
    return render(request, 'properties/add_property.html', context)

@login_required
def edit_property(request, pk):
    property_obj = get_object_or_404(Property, pk=pk)
    
    # Only allow the seller to edit their own property
    if property_obj.seller != request.user:
        messages.error(request, 'You can only edit your own properties.')
        return redirect('properties:property_detail', pk=pk)
    
    if request.method == 'POST':
        form = PropertyForm(request.POST, instance=property_obj)
        if form.is_valid():
            form.save()
            messages.success(request, 'Property updated successfully!')
            return redirect('properties:property_detail', pk=pk)
    else:
        form = PropertyForm(instance=property_obj)
    
    context = {
        'form': form,
        'property': property_obj,
    }
    
    return render(request, 'properties/edit_property.html', context)

@login_required
def my_properties(request):
    if request.user.role != 'seller':
        messages.error(request, 'Only sellers can view their properties.')
        return redirect('properties:property_list')
    
    properties = Property.objects.filter(seller=request.user).order_by('-date_created')
    
    context = {
        'properties': properties,
    }
    
    return render(request, 'properties/my_properties.html', context)

@login_required
def request_visit(request, pk):
    property_obj = get_object_or_404(Property, pk=pk)
    
    if request.user.role != 'buyer':
        messages.error(request, 'Only buyers can request property visits.')
        return redirect('properties:property_detail', pk=pk)
    
    if property_obj.seller == request.user:
        messages.error(request, 'You cannot request to visit your own property.')
        return redirect('properties:property_detail', pk=pk)
    
    # Check if user already has a pending request
    existing_request = VisitRequest.objects.filter(
        property=property_obj,
        buyer=request.user,
        status='pending'
    ).exists()
    
    if existing_request:
        messages.info(request, 'You already have a pending visit request for this property.')
        return redirect('properties:property_detail', pk=pk)
    
    if request.method == 'POST':
        form = VisitRequestForm(request.POST)
        if form.is_valid():
            visit_request = form.save(commit=False)
            visit_request.property = property_obj
            visit_request.buyer = request.user
            visit_request.save()
            
            messages.success(request, 'Visit request sent successfully!')
            return redirect('properties:property_detail', pk=pk)
    else:
        form = VisitRequestForm()
    
    context = {
        'form': form,
        'property': property_obj,
    }
    
    return render(request, 'properties/request_visit.html', context)

@login_required
def respond_visit_request(request, pk):
    visit_request = get_object_or_404(VisitRequest, pk=pk)
    
    # Only the property seller can respond
    if visit_request.property.seller != request.user:
        messages.error(request, 'You can only respond to visit requests for your own properties.')
        return redirect('properties:property_list')
    
    if request.method == 'POST':
        form = VisitResponseForm(request.POST, instance=visit_request)
        if form.is_valid():
            visit_request = form.save(commit=False)
            visit_request.date_responded = timezone.now()
            visit_request.save()
            
            messages.success(request, 'Response sent successfully!')
            return redirect('properties:property_detail', pk=visit_request.property.pk)
    else:
        form = VisitResponseForm(instance=visit_request)
    
    context = {
        'form': form,
        'visit_request': visit_request,
    }
    
    return render(request, 'properties/respond_visit_request.html', context)

@login_required
@login_required
def my_visit_requests(request):
    if request.user.role != 'buyer':
        messages.error(request, 'Only buyers can view their visit requests.')
        return redirect('properties:property_list')
    
    visit_requests = VisitRequest.objects.filter(buyer=request.user).order_by('-date_requested')
    
    context = {
        'visit_requests': visit_requests,
    }
    
    return render(request, 'properties/my_visit_requests.html', context)

@login_required
def manage_property_images(request, pk):
    property_obj = get_object_or_404(Property, pk=pk)
    
    # Only allow the seller to manage their own property images
    if property_obj.seller != request.user:
        messages.error(request, 'You can only manage images for your own properties.')
        return redirect('properties:property_detail', pk=pk)
    
    if request.method == 'POST':
        # Handle image upload
        if 'upload_image' in request.POST:
            if request.FILES.get('image'):
                # Remove existing images first
                property_obj.images.all().delete()
                
                # Create new image
                PropertyImage.objects.create(
                    property=property_obj,
                    image=request.FILES['image'],
                    caption=request.POST.get('caption', ''),
                    is_primary=True
                )
                messages.success(request, 'Property image updated successfully!')
            else:
                messages.error(request, 'Please select an image file.')
        
        # Handle image deletion
        elif 'delete_image' in request.POST:
            image_id = request.POST.get('image_id')
            try:
                image = PropertyImage.objects.get(id=image_id, property=property_obj)
                image.delete()
                messages.success(request, 'Image deleted successfully!')
            except PropertyImage.DoesNotExist:
                messages.error(request, 'Image not found.')
        
        return redirect('properties:manage_property_images', pk=pk)
    
    context = {
        'property': property_obj,
        'images': property_obj.images.all(),
    }
    
    return render(request, 'properties/manage_images.html', context)
