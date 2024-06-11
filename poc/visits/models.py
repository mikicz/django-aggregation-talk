from django.db import models

# Create your models here.


class PageVisit(models.Model):
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    section = models.CharField(max_length=100)
    visit_time = models.DateTimeField()
