from django.contrib import admin

from .models import Project, SaleRecord, UserRecord

admin.site.register(Project)
admin.site.register(SaleRecord)
admin.site.register(UserRecord)
