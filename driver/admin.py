from django.contrib import admin
from .models import Driver,Ride,activeLogin,AppSetting


# Register your models here.
admin.site.register(Driver)
admin.site.register(Ride)
admin.site.register(activeLogin)
admin.site.register(AppSetting)
