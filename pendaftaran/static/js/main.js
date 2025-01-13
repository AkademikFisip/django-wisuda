function togglePasswordVisibility() {
    const passwordInput = document.getElementById('password');
    const toggleIcon = document.querySelector('.toggle-password');
    if (passwordInput.type === "password") {
        passwordInput.type = "text";
        toggleIcon.textContent = "🙈"; // Ikon mata tertutup
    } else {
        passwordInput.type = "password";
        toggleIcon.textContent = "👁️"; // Ikon mata terbuka
    }
}

document.getElementById('editDataForm').addEventListener('submit', function (event) {
    event.preventDefault();

    const form = this;
    const url = "{% url 'pendaftaran:edit_data_mahasiswa' %}";  // Pastikan URL benar
    const formData = new FormData(form);

    fetch(url, {
        method: 'POST',
        body: formData,
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            const modal = bootstrap.Modal.getInstance(document.getElementById('editDataModal'));
            modal.hide();  // Tutup modal
            location.reload();  // Reload halaman untuk menampilkan perubahan
        } else {
            alert('Gagal menyimpan data. Periksa input Anda.');
        }
    })
    .catch(error => console.error('Error:', error));
});

document.getElementById('loginBtn').addEventListener('click', function (e) {
    const npmInput = document.getElementById('npm');
    const passwordInput = document.getElementById('password');
    
    if (!npmInput.value.trim() || !passwordInput.value.trim()) {
        e.preventDefault();
        alert('Mohon isi NPM dan Password!');
    }
});

document.querySelectorAll('.btn-upload').forEach(button => {
    button.addEventListener('click', () => {
        alert('Fungsi Upload belum diimplementasikan.');
    });
});

document.querySelectorAll('.btn-edit').forEach(button => {
    button.addEventListener('click', () => {
        alert('Fungsi Edit belum diimplementasikan.');
    });
});

function previewFoto() {
    const input = document.getElementById("foto-input");
    const preview = document.getElementById("foto-preview");

    if (input.files && input.files[0]) {
        const reader = new FileReader();

        reader.onload = function (e) {
            preview.src = e.target.result;
        };

        reader.readAsDataURL(input.files[0]);
    }
}

function uploadFile(form, previewId) {
    const formData = new FormData(form);
    fetch(form.action, {
        method: 'POST',
        body: formData,
    })
        .then(response => response.text())
        .then(data => {
            console.log(data); // Debugging
            if (data.includes("File berhasil diunggah:")) {
                const filePath = data.split("File berhasil diunggah: ")[1].trim();
                const previewElement = document.getElementById(previewId);

                // Update preview untuk gambar atau dokumen
                if (filePath.match(/\.(jpg|png|jpeg|gif)$/)) {
                    previewElement.innerHTML = `<img src="${filePath}" alt="Preview" style="max-width: 100%; height: auto;">`;
                } else {
                    previewElement.innerHTML = `<a href="${filePath}" target="_blank">Preview File</a>`;
                }
            } else {
                alert("Gagal mengunggah file.");
            }
        })
        .catch(error => console.error('Error:', error));

    return false; // Mencegah reload form
}

function previewFile(event, previewId) {
    const file = event.target.files[0]; // File yang dipilih
    const previewElement = document.getElementById(previewId); // Elemen preview

    if (file) {
        const reader = new FileReader();

        reader.onload = function (e) {
            const fileType = file.type;

            if (fileType.startsWith("image/")) {
                // Preview untuk file gambar
                previewElement.innerHTML = `<img src="${e.target.result}" alt="Preview" style="max-width: 100%; height: auto;">`;
            } else if (fileType === "application/pdf") {
                // Preview untuk file PDF
                previewElement.innerHTML = `<embed src="${e.target.result}" type="application/pdf" style="width: 100%; height: 200px;" />`;
            } else {
                // Preview untuk file lainnya
                previewElement.innerHTML = `<p>${file.name}</p>`;
            }
        };

        reader.readAsDataURL(file); // Membaca file
    } else {
        previewElement.innerHTML = "Preview doc"; // Reset preview jika file dihapus
    }
}

function previewPDF(event, canvasId) {
    const file = event.target.files[0];
    if (file && file.type === "application/pdf") {
        const reader = new FileReader();

        reader.onload = function (e) {
            const loadingTask = pdfjsLib.getDocument({ data: e.target.result });

            loadingTask.promise.then(function (pdf) {
                pdf.getPage(1).then(function (page) {
                    const scale = 1.5; // Skala untuk resolusi PDF
                    const viewport = page.getViewport({ scale: scale });

                    const canvas = document.getElementById(canvasId);
                    const context = canvas.getContext("2d");
                    canvas.width = viewport.width;
                    canvas.height = viewport.height;

                    const renderContext = {
                        canvasContext: context,
                        viewport: viewport,
                    };
                    page.render(renderContext);
                });
            });
        };

        reader.readAsArrayBuffer(file); // Membaca file PDF
    } else {
        alert("File yang dipilih bukan PDF!");
    }
}

console.log(file); // Debugging
console.log(previewElement); // Debugging

console.log("File Name: ", file.name);
console.log("File Type: ", file.type);
console.log("Preview Element: ", previewElement);

