from django.contrib import admin
from .models import Drone, Position, Trip

admin.site.register(Drone)
admin.site.register(Position)
admin.site.register(Trip)
