from django.contrib import admin
from .models import GeneralNotification, UserNotification


admin.site.register(GeneralNotification)
admin.site.register(UserNotification)
