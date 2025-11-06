from django.shortcuts import render
from django.http import HttpResponse

# Crie suas views aqui.

def index(request):
    return HttpResponse("Oi Usuário!")

