from django.db import models

# Create your models here.
class Livro (models.Model):
    titulo = models.CharField(max_length=1000, unique=True) #Não sei se faz sentido um max_lenght aqui, apenas seguindo o exemplo da aula
    sinopse =  models.CharField(blank=True)
    ano_de_publicacao = models.IntegerField()
    genero = models.CharField(max_length=1000)
    exemplares_disponiveis = models.IntegerField() #erro: min_value=0


#Relação Exemplar: many-to-one (Um livro pode ter vários exemplares, um exemplar pode ser de apenas um livro)
class Exemplar(models.Model):
    livro = models.ForeignKey(Livro,on_delete=models.CASCADE, related_name="exemplares")
    disponivel = models.BooleanField(default=True)

class Autor(models.Model):
    nome = models.CharField(max_length=1000, unique=True) 
    biografia = models.CharField(blank=True)


#Relação Autoria: many-to-many (Um livro pode ter multiplos autores e Um autor pode ter escrito vários livros)
class Autoria(models.Model):
    livro = models.ForeignKey(Livro, on_delete=models.CASCADE, related_name='autoria')
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE, related_name='autoria')

    class Meta:
        unique_together = ('livro', 'autor') # Previne duplicatas

class Usuario(models.Model): 
    nome = models.CharField(max_length=50, unique=True)
    email = models.CharField(unique=True)


#Relação Reserva: many-to-one (Um usuario pode ter várias reservas, uma reserva pode ser de apenas um usuario)
class Reserva(models.Model):
    usuario  = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='reserva')
    exemplar = models.ForeignKey(Exemplar, on_delete=models.CASCADE, related_name='reserva')