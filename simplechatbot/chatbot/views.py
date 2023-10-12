from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.http import HttpResponseBadRequest, JsonResponse
from chatbot.services.chatbot import DevBot, ProdBot
from chatbot.models import Query
from chatbot import config
from django.utils import timezone
import json
from uuid import uuid4, UUID

# The dev bot is extremely limited in scope! Only use in testing
# The prod bot is extremely slow to initialize and very slow to query as well.
chatbot = (
    DevBot() if config.dev == True else ProdBot("mistralai/Mistral-7B-Instruct-v0.1")
)


def body_to_json(request):
    body_unicode = request.body.decode("utf-8")
    body = json.loads(body_unicode)
    return body


@require_http_methods(["GET"])
def index(request):
    return render(request, "index.html")


@require_http_methods(["GET"])
def conversation(request):
    try:
        conversation_id = request.GET.get("conversation_id")
        if conversation_id is None:
            raise KeyError
        print(conversation_id)
    except KeyError:
        return HttpResponseBadRequest("Not provided: conversation_id")
    query = list(
        Query.objects.filter(conversation_id=UUID(conversation_id).hex)
        .order_by("pub_date")
        .values()
    )
    return JsonResponse(query, safe=False)


@require_http_methods(["POST"])
def ask(request):
    body = body_to_json(request)
    print(body)
    try:
        query_text = body["query_text"]
        if query_text is None:
            raise KeyError
    except KeyError:
        return HttpResponseBadRequest("Not provided: conversation_id")
    if "conversation_id" in body.keys():
        conversation_id = body["conversation_id"]
        conversation_objects = Query.objects.filter(conversation_id=conversation_id)
        conversation = []
        for query in conversation_objects:
            conversation.append({"role": "user", "content": query.query_text})
            conversation.append({"role": "assistant", "content": query.response})
    else:
        conversation_id = uuid4()
        conversation = [{"role": "user", "content": query_text}]
    response = chatbot(conversation)
    response = "Hello!"
    query = Query(
        query_text=query_text,
        pub_date=timezone.now(),
        response=response,
        model="Test",
        conversation_id=conversation_id,
    )
    query.save()
    return JsonResponse({"response": response, "conversation_id": str(conversation_id)})
