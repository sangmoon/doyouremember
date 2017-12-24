from django.contrib import admin
from app.models import Profile, Memory
# Register your models here.


class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'email_confirmed'
    )


class MemoryAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'content', 'created_at', 'updated_at'
    )

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Memory, MemoryAdmin)

# Register your models here.
