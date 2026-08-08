from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from django_fundamentals.models import User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    """*tier-3/4 admin registration for the custom User model, styled on Django's own UserAdmin*"""
