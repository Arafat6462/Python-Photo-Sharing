from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Photo, Comment, Rating

# Register your models here.

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_creator', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('is_creator',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('is_creator',)}),
    )

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('title', 'creator', 'file_type')
    list_filter = ('file_type', 'creator')
    search_fields = ('title', 'caption', 'creator__username')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'photo', 'text', 'created_at')
    list_filter = ('created_at',)

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('user', 'photo', 'score')
