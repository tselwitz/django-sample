from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
from chatbot.services.chatbot import DevBot, ProdBot
from chatbot.models import Query
from chatbot import config
from django.utils import timezone


# The dev bot is extremely limited in scope! Only use in testing
chatbot = (
    DevBot() if config.dev == True else ProdBot("mistralai/Mistral-7B-Instruct-v0.1")
)


@require_http_methods(["GET"])
def index(request):
    return render(request, "index.html")


@require_http_methods(["POST"])
def ask(request):
    query_text = str(request.body)
    response = chatbot(query_text)
    query = Query(
        query_text=query_text,
        pub_date=timezone.now(),
        response=response,
        model=chatbot.name,
    )
    query.save()
    return HttpResponse(response)
