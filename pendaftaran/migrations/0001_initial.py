# Generated by Django 5.1.4 on 2024-12-30 06:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pendaftar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('nomor_mahasiswa', models.CharField(max_length=20, unique=True)),
                ('jurusan', models.CharField(max_length=100)),
                ('tanggal_daftar', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
