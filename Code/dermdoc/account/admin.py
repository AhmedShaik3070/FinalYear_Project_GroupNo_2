from django.contrib import admin
from .models import Role

# Register the Role model with the admin site
@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'role')  # Fields to display in the list view
    search_fields = ('id', 'role')  # Add a search box for these fields
    list_filter = ('role',)  # Optional: Add a filter by role
    ordering = ('role',)  # Optional: Order by the 'role' field
