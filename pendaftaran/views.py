from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponseBadRequest, JsonResponse
from .forms import UploadBerkasForm, PendaftarForm, MahasiswaForm
from .models import Berkas, Pendaftar, Mahasiswa
from .choices import JENIS_BERKAS_CHOICES

def home(request):
    if request.method == 'POST':
        form = PendaftarForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'pendaftaran/terima_kasih.html')
        else:
            # Render ulang dengan data error yang sudah ada
            return render(request, 'pendaftaran/home.html', {'form': form})
    else:
        form = PendaftarForm()
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
    berkas_terupload = {
        jenis[0]: mahasiswa.berkas_set.filter(jenis_berkas=jenis[0]).first() if mahasiswa else None
        for jenis in JENIS_BERKAS_CHOICES
    }

    berkas_list = [
        {
            "jenis": jenis[0],
            "nama": jenis[1],
            "file_url": berkas_terupload[jenis[0]].file.url if berkas_terupload[jenis[0]] else None,
        }
        for jenis in JENIS_BERKAS_CHOICES
    ]

    context = {
        'mahasiswa': mahasiswa,
        'pendaftar_form': PendaftarForm(instance=mahasiswa),
        'upload_berkas_form': UploadBerkasForm(),
        'berkas_list': berkas_list,
    }
    return render(request, 'pendaftaran/dashboard.html', context)

@login_required
def edit_data_mahasiswa(request):
    mahasiswa = Mahasiswa.objects.filter(user=request.user).first()
    if request.method == 'POST':
        form = MahasiswaForm(request.POST, instance=mahasiswa)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = MahasiswaForm(instance=mahasiswa)
    return render(request, 'pendaftaran/edit_data_mahasiswa.html', {'form': form})

@login_required
def upload_berkas(request):
    if request.method == 'POST':
        form = UploadBerkasForm(request.POST, request.FILES)
        if form.is_valid():
            jenis_berkas = request.POST.get('jenis_berkas')
            berkas = form.save(commit=False)
            berkas.user = request.user
            berkas.jenis_berkas = jenis_berkas
            berkas.save()
            messages.success(request, "Berkas berhasil diunggah.")
        else:
            messages.error(request, "Gagal mengunggah berkas.")
        return redirect('pendaftaran:dashboard')

def update_data(request):
    if request.method == 'POST':
        mahasiswa = Mahasiswa.objects.get(user=request.user)
        form = MahasiswaForm(request.POST, instance=mahasiswa)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = MahasiswaForm(instance=request.user.mahasiswa)
    return render(request, 'update_data.html', {'form': form})

def edit_data_mahasiswa(request):
    # Logika untuk mengedit data mahasiswa
    return render(request, 'pendaftaran/edit_data_mahasiswa.html')

def logout_view(request):
    logout(request)
    return redirect('pendaftaran/login.html')

def validate_jenis_berkas(jenis):
    valid_choices = [choice[0] for choice in JENIS_BERKAS_CHOICES]
    if jenis not in valid_choices:
        raise ValueError("Jenis berkas tidak valid.")
