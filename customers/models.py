from django.db import models
from django.contrib.auth.models import User


class ParkingSlot(models.Model):
    id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    lat = models.FloatField(null=False)
    lng = models.FloatField(null=False)
    status = models.CharField(max_length=10)
    
    def __str__(self):
        return  f"{self.customer} - {self.status}"
