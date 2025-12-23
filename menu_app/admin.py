# menu_app/admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import Dish


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'display_image']
    list_filter = ['category']
    search_fields = ['name']

    def display_image(self, obj):
        if obj.image_url:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 5px;" />', obj.image_url)
        return "—"

    display_image.short_description = 'Картинка'