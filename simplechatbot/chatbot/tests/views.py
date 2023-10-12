from django.test import TestCase
from django.http.request import HttpRequest
from chatbot.models import Query
from chatbot.views import conversation, ask, index, body_to_json
from django.http import HttpResponseBadRequest
from uuid import uuid4
from chatbot.services.chatbot import DevBot
from unittest.mock import MagicMock

test_conversation_id = uuid4()


class ViewsTests(TestCase):
    def setUp(self):
        Query.objects.create(
            query_text="First",
            conversation_id=test_conversation_id,
            model="Test",
        )

    def test_conversation(self):
        req = HttpRequest()
        req.method = "GET"
        req.GET["conversation_id"] = test_conversation_id

        bad_req = HttpRequest()
        bad_req.method = "GET"

        self.assertNotEquals(conversation(req), None)
        self.assertEquals(
            conversation(bad_req).status_code,
            HttpResponseBadRequest("Not provided: conversation_id").status_code,
        )
        conversation(bad_req)
