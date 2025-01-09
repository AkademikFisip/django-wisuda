from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponseBadRequest
from .forms import UploadBerkasForm, PendaftaranForm
from .models import Berkas, Pendaftar
from .choices import JENIS_BERKAS_CHOICES

def home(request):
    if request.method == 'POST':
        form = PendaftaranForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'pendaftaran/terima_kasih.html')
        else:
            # Render ulang dengan data error yang sudah ada
            return render(request, 'pendaftaran/home.html', {'form': form})
    else:
        form = PendaftaranForm()
        return render(request, 'pendaftaran/home.html', {'form': form})
    
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Validasi input
        if not username or not email or not password:
            messages.error(request, 'Semua field wajib diisi.')
            return redirect('pendaftaran:register')

        # Cek apakah email sudah digunakan
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email sudah digunakan.')
            return redirect('pendaftaran:register')

        # Buat pengguna baru
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        messages.success(request, 'Akun berhasil dibuat. Silakan login.')
        return redirect('pendaftaran:login')

    return render(request, 'pendaftaran/register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('pendaftaran:dashboard')  # Ubah sesuai dengan nama URL dashboard Anda
        else:
            messages.error(request, 'Username atau password salah.')
    return render(request, 'pendaftaran/login.html')

@login_required
def dashboard(request):
    mahasiswa = Pendaftar.objects.filter(user=request.user).first()
    form = UploadBerkasForm()

    context = {
        'mahasiswa': mahasiswa,
        'form': form,
        'JENIS_BERKAS_CHOICES': JENIS_BERKAS_CHOICES,
    }
    return render(request, 'pendaftaran/dashboard.html', context)

def logout_view(request):
    logout(request)
    return redirect('pendaftaran/login.html')
