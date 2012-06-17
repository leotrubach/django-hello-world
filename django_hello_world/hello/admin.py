from django.contrib import admin
from .models import Owner, Request


class OwnerAdmin(admin.ModelAdmin):
    pass

class RequestAdmin(admin.ModelAdmin):
    pass

admin.site.register(Owner, OwnerAdmin)
admin.site.register(Request, RequestAdmin)
