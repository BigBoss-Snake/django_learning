from django.contrib import admin
from users.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'last_name', 'is_active')
    list_filter = ('email', 'last_name', 'is_active')


admin.site.register(User, UserAdmin)
