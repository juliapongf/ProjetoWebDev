from django.urls import path
from . import views

urlpatterns = [
    path("",                  views.index,            name="index"),
    path("gerenciar/",        views.gerenciar,        name="gerenciar"),
    path("criar/",            views.criar_livro,      name="criar_livro"),
    path("criar-exemplar/",   views.criar_exemplar,   name="criar_exemplar"),
    path("remover-livro/",    views.remover_livro,    name="remover_livro"),
    path("remover-exemplar/", views.remover_exemplar, name="remover_exemplar"),
    path('divteste/',         views.index,            name='urlteste'),
    path("pesquisa/",         views.pesquisa,         name="pesquisa"),
    path("pesquisar/",        views.pesquisar,        name="pesquisar")
]

