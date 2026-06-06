# 🛡️ NAGA CSRF Scanner

> Automated CSRF Security Assessment Tool for Authorized Security Testing

NAGA CSRF Scanner adalah alat bantu keamanan yang dirancang untuk membantu pengembang, pentester, dan tim keamanan dalam mengidentifikasi serta mengevaluasi implementasi perlindungan Cross-Site Request Forgery (CSRF) pada aplikasi web.

## ✨ Fitur Utama

* Deteksi token CSRF otomatis
* Analisis cookie sesi
* Identifikasi endpoint sensitif
* Analisis parameter formulir
* Pemeriksaan validasi keamanan
* Laporan hasil pemindaian yang mudah dipahami
* Mendukung berbagai framework web populer

---

## 🚀 Instalasi

```bash
https://github.com/Krez-code/SCAN-CSRF-EXPLOITER-.git
cd naga-csrf-scanner
pip install -r requirements.txt
```

---

## 📌 Penggunaan

```bash
python scan.py https://example.com
```

Contoh:

```bash
python scan.py https://target.com
```

---

## 📋 Menu Pengujian

### 1️⃣ Password Change Endpoint Analysis

Melakukan analisis terhadap endpoint yang digunakan untuk proses perubahan kata sandi.

**Fitur:**

* Mendeteksi endpoint perubahan password secara otomatis.
* Memeriksa keberadaan token CSRF.
* Menganalisis parameter formulir yang digunakan.
* Mengidentifikasi potensi kesalahan konfigurasi keamanan.

**Contoh endpoint yang diperiksa:**

```text
/user/password
/profile/password
/settings/password
/api/change-password
```

---

### 2️⃣ Email Change Endpoint Analysis

Melakukan analisis terhadap endpoint yang digunakan untuk proses perubahan alamat email akun.

**Fitur:**

* Mendeteksi endpoint perubahan email.
* Memeriksa implementasi proteksi CSRF.
* Mengidentifikasi parameter email yang digunakan.
* Membantu validasi konfigurasi keamanan akun.

**Contoh endpoint yang diperiksa:**

```text
/profile/email
/user/email
/settings/account
```

---

### 3️⃣ Password Change Validation Test

Melakukan pengujian validasi keamanan pada fitur perubahan kata sandi.

**Fitur:**

* Memeriksa validasi input.
* Memastikan mekanisme konfirmasi password berfungsi.
* Menganalisis proses autentikasi tambahan jika tersedia.
* Membantu memastikan perubahan password mengikuti praktik keamanan yang baik.

---

### 4️⃣ Skip

Melewati pengujian lanjutan dan hanya menjalankan pemindaian dasar.

---

## 📊 Contoh Output

```text
============================================================
NAGA CSRF Scanner
============================================================

Target: https://example.com

[✓] Halaman berhasil dimuat
[✓] Token CSRF ditemukan
[✓] Cookie sesi terdeteksi

Analisis Endpoint:
 - /login
 - /profile
 - /settings

Hasil:
[PASS] Proteksi CSRF aktif
[PASS] Validasi token berjalan dengan baik
[PASS] Cookie menggunakan atribut keamanan yang sesuai

Ringkasan:
Tidak ditemukan kerentanan CSRF kritis.
```

---

## ⚠️ Disclaimer

Alat ini hanya boleh digunakan pada sistem yang:

* Anda miliki sendiri.
* Telah memberikan izin tertulis untuk dilakukan pengujian keamanan.
* Digunakan dalam lingkungan laboratorium atau pembelajaran yang sah.

Penggunaan tanpa izin dapat melanggar hukum dan kebijakan keamanan yang berlaku.

---

## 🤝 Kontribusi

Kontribusi berupa perbaikan bug, peningkatan dokumentasi, dan pengembangan fitur baru sangat diterima.

---

## 📄 Lisensi

MIT License

---

### 👨‍💻 Developer

**Muhammad Reza Nandaka**

* Portfolio: https://krez-portfolio.vercel.app
* GitHub: https://github.com/Krez-code

Keamanan bukan hanya menemukan celah, tetapi juga membantu memperbaikinya agar sistem menjadi lebih kuat.
