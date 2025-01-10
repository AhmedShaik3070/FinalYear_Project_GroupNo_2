from django.contrib import admin
from .models import Child

class ChildAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'age', 'gender', 'status')
    search_fields = ('name', 'description')
    list_filter = ('status', 'gender')
    
admin.site.register(Child, ChildAdmin)