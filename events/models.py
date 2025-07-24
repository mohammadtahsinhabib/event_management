from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()

    def __str__(self):
        return self.name


class Event(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=250)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    participants = models.ManyToManyField(
        User,
        related_name="rsvped_events",
        blank=True,
    )
    image = models.ImageField(upload_to="event_images/", default="default.jpg")

    def __str__(self):
        return self.name
