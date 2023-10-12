# Simple Chatbot

This project showcases a Django REST API that makes a call to a Natural Language Processing machine learning model, answers the question, writes both the query and the response to an SQLite database, and returns the response.

# Getting started

## Requirements
- Python3

## How to install

Create python virtual environment (Optional)
```
$ python3 -m venv .env
$ source .env/bin/activate
```
Install dependencies
```
$ pip3 install -r req.txt
```
Start the app
```
$ cd simplechatbot
$ python3 manage.py runserver
```

## How to stop
Shut down the server
```
CTRL+C
```
Deactivate python virtual environment
```
$ deactivate
```

# Routes

```
 > GET /chatbot # Test Route
 > GET /chatbot/conversation?conversation_id=${UUID} <- Retrieve the contents of a conversation with that UUID
 > POST /chatbot/ask # Takes a question in the request and replies with an answer.

```