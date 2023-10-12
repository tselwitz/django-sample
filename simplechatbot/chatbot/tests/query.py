from django.test import TestCase

from chatbot.models import Query
from uuid import UUID, uuid4
import datetime

test_conversation_id = uuid4()


class QueryTests(TestCase):
    def setUp(self):
        Query.objects.create(
            query_text="First",
            conversation_id=test_conversation_id,
            model="Test",
        )
        Query.objects.create(
            query_text="Second",
            response="Second",
            conversation_id=test_conversation_id,
            model="Test",
        )
        return True

    def test_conversation(self):
        query = Query(conversation_id=test_conversation_id)
        self.assertEqual(
            len(query.conversation(conversation_id=test_conversation_id)), 2
        )

    def test_was_published_recently(self):
        query = Query(conversation_id=test_conversation_id)
        self.assertEqual(query.was_published_recently(), True)
