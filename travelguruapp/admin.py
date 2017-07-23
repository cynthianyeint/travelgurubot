from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(General)
admin.site.register(Place)
admin.site.register(Image)
