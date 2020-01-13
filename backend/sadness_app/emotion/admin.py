from django.contrib import admin

from .models import AppUser, Image, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass

@admin.register(AppUser)
class AppUser(admin.ModelAdmin):
    pass

@admin.register(Image)
class Image(admin.ModelAdmin):
    pass
