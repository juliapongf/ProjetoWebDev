from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Livro)
admin.site.register(Exemplar)
admin.site.register(Autor)
admin.site.register(Autoria)
admin.site.register(Usuario)
admin.site.register(Reserva)