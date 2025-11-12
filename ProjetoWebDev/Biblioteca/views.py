from django.shortcuts import render
from django.http import HttpResponse
from .models import Livro, Autor, Autoria

# Crie suas views aqui.

def index(request):
    return render(request, "Biblioteca/index.html")

def gerenciar(request):
    livros = Livro.objects.all()
    return render(request, "Biblioteca/gerenciamento.html", {"livros": livros})

def criar_livro(request):    
    if request.method == "POST":
        titulo = request.POST.get("titulo")
        autor = request.POST.get("autor")
        autores_novos = autor.split(',')
        genero = request.POST.get("genero")
        sinopse = request.POST.get("sinopse")
        ano = request.POST.get("ano")
        biografia = request.POST.get("biografia")
        biografias_novas = biografia.split('/')

        livro_existe = Livro.objects.filter(titulo=titulo).first()
        if livro_existe:
            return HttpResponse("O livro já existe.")
        else:
            livro = Livro(titulo=titulo, genero=genero, sinopse=sinopse, ano_de_publicacao=ano, exemplares_disponiveis=0)
            livro.save()

        i=0
        for autor_novo in autores_novos:
            autor_existe = Autor.objects.filter(nome=autor_novo).first()
            if autor_existe:
                autor_novo = autor_existe
            else:
                biografia_nova=biografias_novas[i]
                autor_novo = Autor(nome=autor_novo, biografia=biografia_nova)
                autor_novo.save()
            autoria = Autoria(livro=livro, autor=autor_novo)
            autoria.save()

        
        livros = Livro.objects.all()
        autores = Autor.objects.all()
        autorias = Autoria.objects.all()
        return render(request, "Biblioteca/divteste.html", {"livros": livros, "autores": autores, "autorias": autorias})

    return HttpResponse("NADA FOI CRIADO.")

def pesquisa(request):
    livros = Livro.objects.all()
    return render(request, "Biblioteca/pesquisa.html", {"livros": livros})


def pesquisar(request):
    busca = request.GET.get('busca', '')
    tipo = request.GET.get('tipodapesquisa', 'livro')
    
    print(f"Valor da busca: {busca}")
    if tipo == "livro":
        lista = Livro.objects.filter(titulo__icontains=busca)
    elif tipo == "autor":
        lista = Autor.objects.filter(nome__icontains=busca)
    else:
        lista = []

    return render(request, "Biblioteca/parcial_resultados.html", {
        "lista": lista, "tipo": tipo
    })