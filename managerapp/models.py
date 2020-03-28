from django.db import models


class LectureHall(models.Model):
    name = models.CharField(max_length=64)
    capacity = models.IntegerField()
    projector = models.BooleanField(default=False)


class Reservation(models.Model):
    lecture_hall = models.ForeignKey(LectureHall, on_delete=models.CASCADE)
    date = models.DateField()
    comment = models.TextField()
