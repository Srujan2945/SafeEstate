from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
import random
from .forms import CustomUserRegistrationForm, SellerKYCForm, OTPVerificationForm
from .models import SellerKYC, OTPVerification
from django.contrib.auth import get_user_model

User = get_user_model()

def register(request):
    if request.method == 'POST':
        form = CustomUserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Registration successful! Please log in.')
            return redirect('accounts:login')
    else:
        form = CustomUserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def profile(request):
    context = {
        'user': request.user,
    }
    
    # Check if user is seller and has KYC
    if request.user.role == 'seller':
        try:
            kyc = SellerKYC.objects.get(seller=request.user)
            context['kyc'] = kyc
        except SellerKYC.DoesNotExist:
            context['kyc'] = None
    
    return render(request, 'accounts/profile.html', context)

@login_required
def seller_kyc(request):
    if request.user.role != 'seller':
        messages.error(request, 'Only sellers can submit KYC documents.')
        return redirect('accounts:profile')
    
    try:
        kyc = SellerKYC.objects.get(seller=request.user)
        if kyc.status == 'approved':
            messages.info(request, 'Your KYC is already approved.')
            return redirect('accounts:profile')
    except SellerKYC.DoesNotExist:
        kyc = None
    
    if request.method == 'POST':
        form = SellerKYCForm(request.POST, request.FILES, instance=kyc)
        if form.is_valid():
            kyc = form.save(commit=False)
            kyc.seller = request.user
            kyc.status = 'pending'
            kyc.save()
            messages.success(request, 'KYC documents submitted successfully! Please wait for admin approval.')
            return redirect('accounts:profile')
    else:
        form = SellerKYCForm(instance=kyc)
    
    return render(request, 'accounts/seller_kyc.html', {'form': form, 'kyc': kyc})

@login_required
def generate_otp(request):
    # Generate random 6-digit OTP
    otp = str(random.randint(100000, 999999))
    
    # Delete any existing OTP for this user
    OTPVerification.objects.filter(user=request.user).delete()
    
    # Create new OTP
    otp_obj = OTPVerification.objects.create(
        user=request.user,
        otp=otp,
        expires_at=timezone.now() + timedelta(minutes=5)
    )
    
    # In a real application, you would send this OTP via SMS
    # For demonstration, we'll show it on the page
    messages.info(request, f'Your OTP is: {otp} (This is for demonstration only)')
    
    return redirect('accounts:verify_otp')

@login_required
def verify_otp(request):
    try:
        otp_obj = OTPVerification.objects.get(user=request.user, is_verified=False)
        if otp_obj.is_expired():
            messages.error(request, 'OTP has expired. Please generate a new one.')
            return redirect('accounts:generate_otp')
    except OTPVerification.DoesNotExist:
        messages.error(request, 'No OTP found. Please generate an OTP first.')
        return redirect('accounts:generate_otp')
    
    if request.method == 'POST':
        form = OTPVerificationForm(request.POST)
        if form.is_valid():
            entered_otp = form.cleaned_data['otp']
            if entered_otp == otp_obj.otp:
                otp_obj.is_verified = True
                otp_obj.save()
                request.user.is_verified = True
                request.user.save()
                messages.success(request, 'OTP verified successfully!')
                return redirect('accounts:profile')
            else:
                messages.error(request, 'Invalid OTP. Please try again.')
    else:
        form = OTPVerificationForm()
    
    return render(request, 'accounts/verify_otp.html', {'form': form})
