from django.contrib import admin
from .models import CustomUser



class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        'username', 'first_name', 'last_name', 'date_of_birth', 'email', 'number_phone', 'password',
        'profile_picture', 'description'
    )
    search_fields = (
        'username', 'first_name', 'last_name', 'email', 'number_phone', 'password'
    )


admin.site.register(CustomUser, CustomUserAdmin)

