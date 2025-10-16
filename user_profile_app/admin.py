from django.contrib import admin

# Register your models here.
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'type')
    list_filter = ('type',)
    search_fields = ('user__username',)