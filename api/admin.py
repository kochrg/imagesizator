from django.contrib import admin
from api.models import ImagesizatorFile, Parameters, ImagesizatorTemporaryFile


@admin.register(Parameters)
class ParametersAdmin(admin.ModelAdmin):
    list_display = (
        'key',
        'value',
    )
    search_fields = ('key', 'value')
    ordering = ('-created_at',)
    list_display_links = ('key',)


@admin.register(ImagesizatorFile)
class ImagesizatorFileAdmin(admin.ModelAdmin):
    list_display = (
        'created_at',
        'path',
    )
    search_fields = ('created_at', 'path')
    ordering = ('-created_at',)
    list_display_links = ('path',)
    actions = ['delete_model', 'delete_queryset']

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            obj.delete()

    def delete_model(self, request, obj):
        obj.delete()


@admin.register(ImagesizatorTemporaryFile)
class ImagesizatorTemporaryFileAdmin(admin.ModelAdmin):
    list_display = (
        'created_at',
        'path',
        'expiration_date'
    )
    search_fields = ('created_at', 'path')
    ordering = ('-created_at',)
    list_display_links = ('path',)
    actions = ['delete_model', 'delete_queryset']

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            obj.delete()

    def delete_model(self, request, obj):
        obj.delete()
