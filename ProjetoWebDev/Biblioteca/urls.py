from django.urls import path
from . import views

urlpatterns = [
    path("",       views.index,       name="index"),
    path("criar/", views.criar_livro, name="criar_livro")
]

