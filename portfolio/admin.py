from django.contrib import admin

from .models import Collection, Photo


class PhotoInline(admin.TabularInline):
    model = Photo
    fields = ("image", "title", "alt_text", "is_published", "display_order")
    extra = 1


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ("title", "is_published", "display_order")
    list_filter = ("is_published",)
    prepopulated_fields = {"slug": ("title",)}
    inlines = [PhotoInline]


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ("title", "collection", "is_published", "display_order")
    list_filter = ("collection", "is_published")
