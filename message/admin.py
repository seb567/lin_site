from django.contrib import admin

# Register your models here.
from message import models
admin.site.register(models.qqinfo)
admin.site.register(models.tiebaads)
admin.site.register(models.tiebainfo)
admin.site.register(models.lastpos)
