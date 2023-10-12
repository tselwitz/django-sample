from django.db import models
from django.utils import timezone
import datetime
from uuid import uuid4


class Query(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    query_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField(default=timezone.now)
    response = models.CharField(max_length=1000)
    model = models.CharField(max_length=100)
    conversation_id = models.UUIDField(primary_key=False, default=uuid4)

    def __str__(self):
        builder = (
            "{\n"
            + "\n".join(
                [
                    f'"{f.name}": {f.value_from_object(self)}'
                    for f in Query._meta.get_fields()
                ]
            )
            + "\n}"
        )
        return builder

    def conversation(self, conversation_id):
        return Query.objects.filter(conversation_id=conversation_id)

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
