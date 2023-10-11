from django.db import models


class Query(models.Model):
    query_text = models.CharField(max_length=300)
    created_at = models.DateTimeField()
    ml_model = models.CharField(max_length=100)
    response = models.CharField(max_length=3000)
