from django.contrib import admin
from .models import Location, Category, Board, UserProfile


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'image')
    search_fields = ('name',)


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'is_active_board', 'created_at', 'location', 'category')
    list_filter = ('is_active_board', 'category', 'location')
    search_fields = ('title', 'description')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)


