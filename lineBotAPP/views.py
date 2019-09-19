from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def sayHello(request, username):
    return HttpResponse("Hello!! " + username)