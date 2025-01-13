from django.urls import path
from . import views

app_name = 'pendaftaran'

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('upload-berkas/', views.upload_berkas, name='upload_berkas'),
    path('edit-data/', views.edit_data_mahasiswa, name='edit_data_mahasiswa'),
    path('logout/', views.logout_view, name='logout'),
]
