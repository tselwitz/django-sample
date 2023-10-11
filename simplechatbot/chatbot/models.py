from django.db import models
from django.utils import timezone
import datetime


class Query(models.Model):
    query_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")
    response = models.CharField(max_length=1000)
    model = models.CharField(max_length=100)

    def __str__(self):
        return self.query_text

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
