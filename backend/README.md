# Cemas.AI Backend API

Backend API untuk aplikasi Cemas.AI yang terintegrasi dengan front end React.js. Diimplementasikan menggunakan FastAPI Python sebagai framework utama.

## Teknologi yang Digunakan

- **FastAPI**: Framework web API modern dan cepat
- **PostgreSQL (Supabase)**: Database utama
- **Groq Cloud**: Layanan AI untuk akses API Meta Llama
- **LangChain**: Framework untuk manajemen model bahasa
- **SQLAlchemy**: ORM untuk interaksi database
- **Alembic**: Tool migrasi database
- **JWT**: Autentikasi berbasis token

## Struktur Proyek

```
backend/
├── alembic/              # Konfigurasi dan migrasi database
├── app/
│   ├── api/              # API endpoints
│   │   ├── auth.py       # Autentikasi API
│   │   ├── chat.py       # Chat dan AI API
│   │   └── user.py       # User API
│   ├── core/             # Konfigurasi inti
│   │   ├── config.py     # Pengaturan aplikasi
│   │   ├── database.py   # Koneksi database
│   │   └── security.py   # Keamanan dan autentikasi
│   ├── models/           # Model database
│   │   ├── chat.py       # Model percakapan dan pesan
│   │   └── user.py       # Model pengguna
│   ├── schemas/          # Skema validasi data
│   │   ├── chat.py       # Skema percakapan dan pesan
│   │   ├── token.py      # Skema token
│   │   └── user.py       # Skema pengguna
│   ├── services/         # Layanan aplikasi
│   │   └── ai_service.py # Layanan AI
│   └── main.py           # Entrypoint aplikasi
├── logs/                 # Log aplikasi
├── .env                  # Variabel lingkungan (tidak di-commit)
├── .env.example          # Contoh variabel lingkungan
├── alembic.ini           # Konfigurasi Alembic
└── requirements.txt      # Dependensi Python
```

## Memulai

### Prasyarat

- Python 3.9+
- PostgreSQL
- Groq API Key

### Instalasi

1. Clone repositori
2. Buat virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```
3. Install dependensi:
   ```bash
   pip install -r requirements.txt
   ```
4. Salin `.env.example` ke `.env` dan sesuaikan nilai-nilainya
5. Jalankan migrasi database:
   ```bash
   alembic upgrade head
   ```
6. Jalankan server:
   ```bash
   uvicorn app.main:app --reload
   ```

## Dokumentasi API

Setelah menjalankan server, dokumentasi API tersedia di:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Endpoint API

### Autentikasi

- `POST /api/auth/register` - Registrasi pengguna baru
- `POST /api/auth/token` - Login dan dapatkan token akses
- `GET /api/auth/me` - Dapatkan informasi pengguna saat ini

### Pengguna

- `GET /api/users/` - Dapatkan daftar pengguna (admin)
- `POST /api/users/` - Buat pengguna baru (admin)

### Percakapan

- `POST /api/conversations/` - Buat percakapan baru
- `GET /api/conversations/` - Dapatkan semua percakapan pengguna
- `GET /api/conversations/{id}` - Dapatkan detail percakapan
- `PUT /api/conversations/{id}` - Perbarui percakapan
- `DELETE /api/conversations/{id}` - Hapus percakapan

### Pesan

- `POST /api/conversations/{id}/messages/` - Kirim pesan baru (otomatis mendapatkan respons AI)
- `GET /api/conversations/{id}/messages/` - Dapatkan semua pesan dalam percakapan

### Wawasan AI

- `POST /api/conversations/{id}/insights/` - Dapatkan wawasan kesehatan mental dari percakapan

## Integrasi dengan Frontend

Frontend React.js dapat berkomunikasi dengan API ini menggunakan permintaan HTTP standar. Contoh penggunaan dengan fetch API:

```javascript
// Login dan dapatkan token
async function login(email, password) {
  const response = await fetch('http://localhost:8000/api/auth/token', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded'
    },
    body: new URLSearchParams({
      'username': email,
      'password': password
    })
  });
  return await response.json();
}

// Kirim pesan dan dapatkan respons AI
async function sendMessage(conversationId, content, token) {
  const response = await fetch(`http://localhost:8000/api/conversations/${conversationId}/messages/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify({
      role: 'user',
      content: content
    })
  });
  return await response.json();
}
```

## Keamanan

- Autentikasi JWT dengan token yang kedaluwarsa
- Password hashing dengan bcrypt
- CORS dikonfigurasi untuk domain frontend yang diizinkan
- Validasi data dengan Pydantic

## Skalabilitas

- Arsitektur modular untuk penambahan fitur dengan mudah
- Penggunaan async/await untuk performa yang lebih baik
- Logging untuk pemantauan dan debugging
- Penanganan kesalahan yang konsisten

## Pengembangan Lanjutan

- Menambahkan lebih banyak model AI dan penyedia
- Implementasi caching untuk respons AI
- Penambahan fitur analitik dan wawasan lanjutan
- Integrasi dengan layanan pihak ketiga untuk notifikasi