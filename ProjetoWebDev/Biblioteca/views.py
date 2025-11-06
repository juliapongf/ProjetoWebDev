from django.shortcuts import render
from django.http import HttpResponse

# Crie suas views aqui.

def index(request):
    return render(request, "Biblioteca/pesquisa.html")


