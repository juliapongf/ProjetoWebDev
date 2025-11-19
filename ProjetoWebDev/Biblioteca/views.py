from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from urllib.parse import parse_qs

# Crie suas views aqui.

def index(request):
    return render(request, "Biblioteca/index.html") # Renderiza a página principal da biblioteca


def gerenciar(request):
    return render(request, "Biblioteca/gerenciamento.html") # Renderiza a página de gerenciamento


def criar_livro(request):
    if request.method == "POST":
        # Coletar todos os campos preenchidos no formulário
        titulo = request.POST.get("titulo")
        autor = request.POST.get("autor")
        autores_novos = autor.split(',')
        genero = request.POST.get("genero")
        sinopse = request.POST.get("sinopse")
        ano = request.POST.get("ano")
        biografia = request.POST.get("biografia")
        biografias_novas = biografia.split('/')

        if not titulo:
                return render(request, "Biblioteca/partials/msg_warning.html", {
                "mensagem": "Título não informado."
                })
        if not ano:
                return render(request, "Biblioteca/partials/msg_warning.html", {
                "mensagem": "Ano não informado."
                })

        # Procura no acervo o livro com o título preenchido no formulário.
        livro_existe = Livro.objects.filter(titulo=titulo).first()

        # Se o livro já existir, não adiciona
        if livro_existe:
            return render(request, "Biblioteca/partials/msg_warning.html", {
                "mensagem": "Este livro já está adicionado ao acervo."
            })
        # Caso contrário, adiciona o novo livro ao acervo
        else:
            livro = Livro(titulo=titulo, genero=genero, sinopse=sinopse, ano_de_publicacao=ano, exemplares_disponiveis=0)
            livro.save()


        i=0
        # Para cada autor novo inserido no formulário...
        for autor_novo in autores_novos:

            # Procura no banco de dados o autor preenchido no formulário.
            autor_existe = Autor.objects.filter(nome=autor_novo).first()

            # Se o autor já existir, o "autor novo" será usado para criar a autoria de seu novo livro que ainda não estava no acervo.
            if autor_existe:
                autor_novo = autor_existe
            # Caso contrário, cria o autor novo
            else:
                biografia_nova=biografias_novas[i]
                autor_novo = Autor(nome=autor_novo, biografia=biografia_nova)
                autor_novo.save()

            # Cria a autoria (livro + autor)
            autoria = Autoria(livro=livro, autor=autor_novo)
            autoria.save()


        return render(request, "Biblioteca/partials/msg_success.html", {
            "mensagem": "Livro adicionado ao acervo com sucesso!"
        })

    return HttpResponse("NADA FOI CRIADO.")

def criar_exemplar(request):
    if request.method == "POST":

        # Checa se o campo título foi preenchido
        titulo = request.POST.get("titulo")
        if not titulo:
            return render(request, "Biblioteca/partials/msg_warning.html", {
                "mensagem": "Título não informado."
            })

        # Caso título não corresponder a nenhum livro do acervo
        try:
            livro = Livro.objects.get(titulo__icontains=request.POST.get("titulo"))
        except Livro.DoesNotExist:
            return render(request, "Biblioteca/partials/msg_error.html", {
                "mensagem": "Não há livro com este título no acervo."
            })
    
        # Cria o exemplar através do título do livro inserido no formulário.
        exemplar = Exemplar(livro=livro, disponivel=True)
        livro.exemplares_disponiveis += 1
        livro.save()
        exemplar.save()

        if exemplar:
            return render(request, "Biblioteca/partials/msg_success.html", {
                "mensagem": "Exemplar criado com sucesso!"
            })

    return HttpResponse("NADA FOI CRIADO.")

def remover_livro(request):
    if request.method == "DELETE":
        try:
            data = request.body.decode("utf-8") # decodifica o request (binário -> utf-8)
            parsed = parse_qs(data) # transforma a estrutura dos dados do formulário para um dicionário
            titulo = parsed.get("titulo", [None])[0] # acessa a chave "título" do dicionário

            if not titulo:
                return render(request, "Biblioteca/partials/msg_warning.html", {
                "mensagem": "Título não informado."
            })
  
            livro = Livro.objects.get(titulo__icontains=titulo)
            livro.delete()

            return render(request, "Biblioteca/partials/msg_success.html", {
                "mensagem": "Livro removido com sucesso!"
            })
        
        except Livro.DoesNotExist:
            return render(request, "Biblioteca/partials/msg_error.html", {
                "mensagem": "Livro não encontrado no acervo."
            })
    else:
        return HttpResponse("Método inválido", status=405)

def remover_exemplar(request):
    if request.method == "DELETE":
        try:
            data = request.body.decode("utf-8") # decodifica o request (binário -> utf-8)
            parsed = parse_qs(data) # transforma a estrutura dos dados do formulário para um dicionário
            id_exemplar = parsed.get("id_exemplar", [None])[0] # acessa a chave "id_exemplar" do dicionário

            if not id_exemplar:
                return render(request, "Biblioteca/partials/msg_warning.html", {
                "mensagem": "ID do exemplar não informado."
            })

            exemplar = Exemplar.objects.get(id=id_exemplar)

            # Obtém o livro associado ao exemplar especificado, decrementa o número de exemplares disponíveis e salva as modificações do objeto livro
            livro = exemplar.livro
            livro.exemplares_disponiveis -= 1
            livro.save()

            exemplar.delete()

            return render(request, "Biblioteca/partials/msg_success.html", {
                "mensagem": "Exemplar deletado com sucesso!"
             })
        
        except Exemplar.DoesNotExist:
            return render(request, "Biblioteca/partials/msg_error.html", {
                "mensagem": "Exemplar não encontrado."
             })

    return HttpResponse("Método inválido", status=405)

def atualizar_livro(request):
    if request.method == "PUT":
        try:
            # Pegando o corpo da requisição
            data = request.body.decode("utf-8") # Decodificando os dados enviados
            parsed = parse_qs(data)  # Usando parse_qs para obter os dados como um dicionário

            # Extraindo os valores dos campos do formulário
            id = parsed.get("id", [None])[0]
            titulo = parsed.get("titulo", [None])[0]
            autor = parsed.get("autor", [None])[0]
            autores_novos = autor.split(',') if autor else []
            genero = parsed.get("genero", [None])[0]
            sinopse = parsed.get("sinopse", [None])[0]
            ano = parsed.get("ano", [None])[0]
            biografia = parsed.get("biografia", [None])[0]
            biografias_novas = biografia.split('/') if biografia else []

            #Verificar se os campos livro id e titulo foram preenchidos
            if not id:
                return render(request, "Biblioteca/partials/msg_warning.html", {
                "mensagem": "ID do Livro não informado."
             })
            
            # Atualizando o livro 
            livro = Livro.objects.filter(id=id).first()
            if livro:
                if titulo:
                    livro.titulo = titulo
                if sinopse:
                    livro.sinopse = sinopse
                if genero:
                    livro.genero = genero
                if ano:
                    livro.ano_de_publicacao = ano
                livro.save()
            else:
                return render(request, "Biblioteca/partials/msg_warning.html", {
                "mensagem": "Este livro não faz parte do acervo. Adicione-o antes de atualizar"
             })

            # Atualizando os autores
            i = 0
            for autor_novo in autores_novos:
                autor_existe = Autor.objects.filter(nome=autor_novo).first()
                if autor_existe:
                    if biografias_novas and i < len(biografias_novas):
                        autor_existe.biografia = biografias_novas[i]
                        autor_existe.save()
                else:
                    biografia_nova = biografias_novas[i] if i < len(biografias_novas) else ''
                    autor_novo = Autor(nome=autor_novo, biografia=biografia_nova)
                    autor_novo.save()
                    autoria = Autoria(livro=livro, autor=autor_novo)
                    autoria.save()
                i += 1

            return render(request, "Biblioteca/partials/msg_success.html", {
                "mensagem": "Livro atualizado com sucesso!"
             })

        except Exception as e:
            return render(request, "Biblioteca/partials/msg_error.html", {
                "mensagem": "Erro ao atualizar livro."
             })
        

    return HttpResponse("NADA FOI ATUALIZADO.", status=400)


def pesquisa(request):
    return render(request, "Biblioteca/pesquisa.html") # Renderiza a página de pesquisa


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

    # Renderiza os resultados da pesquisa na página de pesquisa
    return render(request, "Biblioteca/parcial_resultados.html", {
        "lista": lista, "tipo": tipo
    })

def criar_reserva(request):
    if request.method == "POST":

        # Testa se campos foram preenchidos
        nome = request.POST.get("nome")
        exemplar_id = request.POST.get("exemplar") 

        if not nome:
            return render(request, "Biblioteca/partials/msg_warning.html", {
                "mensagem": "Nome de usuário não informado."
            })

        if not exemplar_id:
            return render(request, "Biblioteca/partials/msg_warning.html", {
                "mensagem": "ID  do exemplar não informado."
            })
        # Tenta carregar usuário 
        try:
            usuario = Usuario.objects.get(nome__icontains=request.POST.get("nome"))
        except Usuario.DoesNotExist:
            return render(request, "Biblioteca/partials/msg_error.html", {
                "mensagem": "Usuário não encontrado."
            })
        # Tenta carregar exemplar
        try:
            exemplar = Exemplar.objects.get(id__icontains=request.POST.get("exemplar"))
        except Exemplar.DoesNotExist:
            return render(request, "Biblioteca/partials/msg_error.html", {
                "mensagem": "Exemplar não encontrado."
            })

        # Caso exemplar não disponível
        if exemplar.disponivel == False:
            return render(request, "Biblioteca/partials/msg_error.html", {
                "mensagem": "Exemplar não disponível."
            })

        # Caso reserva repetida
        if Reserva.objects.filter(exemplar=exemplar).exists():
            return render(request, "Biblioteca/partials/msg_warning.html", {
                "mensagem": "Esta reserva já foi realizada."
            })
        
        # Criação da reserva
        reserva = Reserva(usuario=usuario, exemplar=exemplar)
        reserva.save()
        exemplar.disponivel = False
        exemplar.save()
        livro = exemplar.livro
        livro.exemplares_disponiveis -= 1
        livro.save()
        
        if reserva:
            return render(request, "Biblioteca/partials/msg_success.html", {
                "mensagem": "Reserva criada com sucesso!"
            })
    return HttpResponse("nada foi criado")

def remover_reserva(request):
    if request.method == "DELETE":
        try:
            # HTMX envia o corpo como querystring
            data = request.body.decode("utf-8") # decodifica o request (binário -> utf-8)
            parsed = parse_qs(data) # transforma a estrutura dos dados do formulário para um dicionário

            exemplar_id = parsed.get("exemplar_id", [None])[0] # acessa a chave "exemplar_id" do dicionário

            #tenta pegar nome do usuário
            nome = parsed.get("nome", [None])[0]


            if not nome:
                return render(request, "Biblioteca/partials/msg_warning.html", {
                "mensagem": "Nome de usuário não informado."
                })
            
            if not exemplar_id:
                return render(request, "Biblioteca/partials/msg_warning.html", {
                "mensagem": "ID do exemplar não informado."
                })


            # Pega o exemplar
            exemplar = Exemplar.objects.get(id=exemplar_id)

            #Verfica usuario
            usuario = Usuario.objects.get(nome=nome)

            # Verifica se ele tem reserva
            reserva = Reserva.objects.get(exemplar=exemplar,usuario__nome=nome)
            

            # Remove a reserva
            reserva.delete()

            # Marca exemplar como disponível novamente
            exemplar.disponivel = True
            exemplar.save()
            livro = exemplar.livro
            livro.exemplares_disponiveis += 1
            livro.save()

            return render(request, "Biblioteca/partials/msg_success.html", {
                "mensagem": "Reserva removida com sucesso!"
            })
        
        except Usuario.DoesNotExist:
            return render(request, "Biblioteca/partials/msg_error.html", {
                "mensagem": "Usuário não cadastrado."
            })

        except Exemplar.DoesNotExist:
            return render(request, "Biblioteca/partials/msg_error.html", {
                "mensagem": "Exemplar não encontrado."
            })

        except Reserva.DoesNotExist:
            return render(request, "Biblioteca/partials/msg_error.html", {
                "mensagem": "Reserva não encontrada."
            })

    return HttpResponse("NADA FOI REMOVIDO", status=405)

def criar_usuario(request):
    if request.method == "POST":

        nome =request.POST.get("nome")
        email =request.POST.get("email")

        if not nome:
                return render(request, "Biblioteca/partials/msg_warning.html", {
                "mensagem": "Nome de usuário não informado."
                })
        
        if Usuario.objects.filter(nome=nome).exists():
            return render(request, "Biblioteca/partials/msg_error.html", {
                "mensagem": "Nome de usuário já cadastrado."
            })
        
        if Usuario.objects.filter(email=email).exists():
            return render(request, "Biblioteca/partials/msg_error.html", {
                "mensagem": "E-mail já cadastrado."
            })

        usuario = Usuario(nome=nome, email=email)
        usuario.save()
        return render(request, "Biblioteca/partials/msg_success.html", {
                "mensagem": "Usuário criado com sucesso!"
            })

    return HttpResponse("NADA FOI CRIADO.")