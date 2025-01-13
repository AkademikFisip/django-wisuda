from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponseBadRequest, JsonResponse
from .forms import UploadBerkasForm, PendaftaranForm, PendaftarForm
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

def register_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email sudah digunakan.')
        else:
            messages.success(request, 'Akun berhasil dibuat.')
            return redirect('pendaftaran:login')
    return render(request, 'pendaftaran/register.html')
    
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('pendaftaran:dashboard')  # Redirect ke dashboard
        else:
            return render(request, 'pendaftaran/login.html', {'error': 'Username atau password salah.'})
    return render(request, 'pendaftaran/login.html')

@login_required
def dashboard(request):
    mahasiswa = Pendaftar.objects.filter(user=request.user).first()
    pendaftar_form = PendaftarForm(instance=mahasiswa)  # Gunakan PendaftarForm

    context = {
        'mahasiswa': mahasiswa,
        'pendaftar_form': pendaftar_form,  # Pastikan form ini dikirimkan
        'JENIS_BERKAS_CHOICES': JENIS_BERKAS_CHOICES,
    }
    return render(request, 'pendaftaran/dashboard.html', context)

@login_required
def edit_data_mahasiswa(request):
    mahasiswa = Pendaftar.objects.filter(user=request.user).first()
    
    if not mahasiswa:
        mahasiswa = Pendaftar(user=request.user)  # Buat instance baru jika belum ada

    if request.method == 'POST':
        form = PendaftarForm(request.POST, instance=mahasiswa)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = PendaftarForm(instance=mahasiswa)

    return render(request, 'pendaftaran/edit_data_mahasiswa.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('pendaftaran/login.html')
