from django.db import models
from django.utils import timezone

class URL(models.Model):
    url_long = models.URLField(unique=True)
    url_short = models.URLField(unique=True)
    created_date = models.DateTimeField(default=timezone.now)
    nickname = models.CharField(max_length=200, blank=True, null=True)
    redirect_number = models.IntegerField(default=0)

    def __str__(self):
        return self.url_long
