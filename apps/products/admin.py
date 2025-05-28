from django.contrib import admin
from .models import Category, Product, Attribute

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    list_display = ('id', 'color', 'size', 'material')
    search_fields = ('color', 'size', 'material')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'price', 'category', 'in_stock', 'average_rating', 'likes_count')
    list_filter = ('category', 'in_stock', 'created_at')
    search_fields = ('title', 'description', 'attributes')
    readonly_fields = ('created_at', 'updated_at')
    autocomplete_fields = ('category',)
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'price', 'image', 'category', 'attributes')
        }),
        ('Stats', {
            'fields': ('average_rating', 'reviews_count', 'likes_count', 'is_liked', 'in_stock')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
