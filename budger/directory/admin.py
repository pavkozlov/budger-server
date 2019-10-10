from django.contrib import admin
from .models.entity import Entity
from .models.kso import Kso
from .models.kso import KsoEmployee


admin.site.register(Entity)
admin.site.register(Kso)
admin.site.register(KsoEmployee)
