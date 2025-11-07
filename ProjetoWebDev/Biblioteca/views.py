from django.shortcuts import render
from django.http import HttpResponse
from .models import Livro

# Crie suas views aqui.

def index(request):
    livros = Livro.objects.all()
    return render(request, "Biblioteca/gerenciamento.html", {"livros": livros})

def criar_livro(request):    
    if request.method == "POST":
        titulo = request.POST.get("titulo")
        autor = request.POST.get("autor")
        genero = request.POST.get("genero")
        sinopse = request.POST.get("sinopse")
        ano = request.POST.get("ano")

        livro = Livro(titulo=titulo, genero=genero, sinopse=sinopse, ano_de_publicacao=ano, exemplares_disponiveis=0)
        livro.save()
        livros = Livro.objects.all()
        return render(request, "Biblioteca/divteste.html", {"livros": livros})

    return HttpResponse("NADA FOI CRIADO.")

def pesquisa(request):
    livros = Livro.objects.all()
    return render(request, "Biblioteca/pesquisa.html", {"livros": livros})


def pesquisa_livros(request):
    busca = request.GET.get('busca', '')
    print(f"Valor da busca: {busca}")
    if busca:
        livros = Livro.objects.filter(titulo__icontains=busca)
    else:
        livros = Livro.objects.all()

    return render(request, "Biblioteca/parcial_resultados.html", {
        "livros": livros
    })