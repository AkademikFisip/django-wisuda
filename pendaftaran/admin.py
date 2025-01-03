from django.contrib import admin
from .models import Berkas
from .models import Pendaftar, Berkas

admin.site.register(Pendaftar)
admin.site.register(Berkas)
