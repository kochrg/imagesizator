from django.contrib import admin
from api.models.core import ImagesizatorFile, Parameters


@admin.register(Parameters)
class ParametersAdmin(admin.ModelAdmin):
    list_display = (
        "key",
        "value",
    )
    search_fields = ("key", "value")
    ordering = ("-created_at",)
    list_display_links = ("key",)


@admin.register(ImagesizatorFile)
class ImagesizatorFileAdmin(admin.ModelAdmin):
    list_display = (
        "created_at",
        "path",
    )
    search_fields = ("created_at", "path")
    ordering = ("-created_at",)
    list_display_links = ("path",)
    actions = ["delete_model", "delete_queryset"]
    readonly_fields = ["expiration_date"]

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            obj.delete()

    def delete_model(self, request, obj):
        obj.delete()
