from django.contrib import admin

from api.models import Parameters

# Register your models here.
@admin.register(Parameters)
class ParametersAdmin(admin.ModelAdmin):
    list_display = (
        'key',
        'value',
    )
    search_fields = ('key', 'value')
    ordering = ('-created_at',)
    list_display_links = ('key',)