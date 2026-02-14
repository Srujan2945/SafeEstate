from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, SellerKYC, OTPVerification

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'is_verified', 'is_active', 'date_joined')
    list_filter = ('role', 'is_verified', 'is_active', 'date_joined')
    search_fields = ('username', 'email', 'phone')
    
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('role', 'phone', 'address', 'is_verified')}),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('role', 'phone', 'address')}),
    )

class SellerKYCAdmin(admin.ModelAdmin):
    list_display = ('seller', 'status', 'date_submitted', 'verified_by', 'date_verified')
    list_filter = ('status', 'date_submitted', 'date_verified')
    search_fields = ('seller__username', 'seller__email')
    readonly_fields = ('date_submitted',)

class OTPVerificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'otp', 'is_verified', 'created_at', 'expires_at')
    list_filter = ('is_verified', 'created_at')
    search_fields = ('user__username',)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(SellerKYC, SellerKYCAdmin)
admin.site.register(OTPVerification, OTPVerificationAdmin)
