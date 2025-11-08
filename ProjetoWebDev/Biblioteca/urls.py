from django.urls import path
from . import views

urlpatterns = [
    path("",       views.index,       name="index"),
    path("gerenciar",       views.gerenciar,       name="gerenciar"),
    path("criar/", views.criar_livro, name="criar_livro"),
    path('divteste/', views.index,    name='urlteste'), path("pesquisa/", views.pesquisa, name="pesquisa"),
    path("pesquisar/", views.pesquisar, name="pesquisar")
]

