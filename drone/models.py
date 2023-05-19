from django.db import models

class Drone(models.Model):
    id = models.AutoField(primary_key=True)
    current_position = models.CharField(max_length=2)

class Position(models.Model):
    id = models.AutoField(primary_key=True)
    coordinate = models.CharField(max_length=2, unique=True)

class Trip(models.Model):
    id = models.AutoField(primary_key=True)
    drone = models.ForeignKey(Drone, on_delete=models.CASCADE)
    pickup = models.ForeignKey(Position, on_delete=models.CASCADE, related_name="pickup")
    destination = models.ForeignKey(Position, on_delete=models.CASCADE, related_name="destination")
    total_time = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
