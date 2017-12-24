from django.contrib import admin
from app.models import Profile
# Register your models here.


class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'email_confirmed'
    )

admin.site.register(Profile, ProfileAdmin)

# Register your models here.
