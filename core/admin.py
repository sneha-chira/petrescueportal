from django.contrib import admin
from .models import Pet, AdoptionRequest


@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ['name', 'breed', 'color', 'status', 'location', 'reported_by', 'created_at', 'is_active']
    list_filter = ['status', 'gender', 'size', 'created_at', 'is_active']
    search_fields = ['name', 'breed', 'color', 'location', 'description']
    list_editable = ['is_active']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'breed', 'color', 'age', 'gender', 'size')
        }),
        ('Status & Location', {
            'fields': ('status', 'location', 'is_active')
        }),
        ('Description', {
            'fields': ('description',)
        }),
        ('Contact Information', {
            'fields': ('contact_phone', 'contact_email')
        }),
        ('Media', {
            'fields': ('image',)
        }),
        ('System Information', {
            'fields': ('reported_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(AdoptionRequest)
class AdoptionRequestAdmin(admin.ModelAdmin):
    list_display = ['pet', 'requester', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['pet__breed', 'pet__name', 'requester__username', 'message']
    list_editable = ['status']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'
