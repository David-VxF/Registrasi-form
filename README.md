![Banner](https://david-vxf.my.id/public/logo/logo.png)

------------------------------------------------------------------------

# Form Registrasi Sederhana (Python)

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Status](https://img.shields.io/badge/Status-Active-success)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Learning_Project](https://img.shields.io/badge/Type-Learning_Project-orange)

------------------------------------------------------------------------

# 🇮🇩 Deskripsi (Bahasa Indonesia)

Proyek ini adalah latihan pribadi untuk memahami dasar pemrograman
Python melalui pembuatan form registrasi yang berjalan di terminal.
Program meminta pengguna memasukkan: - Nama - Umur - Hobi - Kota tempat
tinggal

Program juga melakukan validasi input dan meminta konfirmasi sebelum
menyimpan data.

------------------------------------------------------------------------

# 🇬🇧 Description (English)

This project is a personal learning exercise to understand Python basics
by creating a simple terminal-based registration form. The program asks
the user to input: - Name - Age - Hobby - City of residence

The program includes input validation and a confirmation step before
saving the data.

------------------------------------------------------------------------

## ✨ Features / Fitur

-   Input validation (empty field checks, numeric validation)
-   Data confirmation (Y/N)
-   Looping mechanism to re-enter incorrect data
-   Simple and beginner-friendly Python logic

------------------------------------------------------------------------

## 🧩 Flow Diagram / Diagram Alur

                +---------------------------+
                               |        Mulai Program      |
                               +--------------+------------+
                                              |
                                              v
                         +--------------------+--------------------+
                         |  Tampilkan judul: "form registrasi"     |
                         +--------------------+--------------------+
                                              |
                                              v
                       +----------------------+----------------------+
                       |      Panggil fungsi registrasi()           |
                       +----------------------+----------------------+
                                              |
                                              v
          +-----------------------------------+-----------------------------------+
          |                         Fungsi registrasi()                           |
          +-----------------------------------+-----------------------------------+
                                              |
            +------------------------------ Input Nama ----------------------------+
            |  • Minta input nama                                                |
            |  • Jika kosong → tampilkan pesan dan ulangi                        |
            +----------------------------------+----------------------------------+
                                              |
                                              v
            +------------------------------ Input Umur ----------------------------+
            |  • Minta input umur                                                |
            |  • Validasi angka (try/except)                                     |
            |  • Jika bukan angka → pesan error → ulangi                         |
            +----------------------------------+----------------------------------+
                                              |
                                              v
              +---------------------------- Input Hobi ----------------------------+
              |  • Minta input hobi                                               |
              |  • Jika kosong → tampilkan pesan → ulangi                         |
              +--------------------------------+----------------------------------+
                                              |
                                              v
            +------------------------------ Input Kota ----------------------------+
            |  • Minta input kota                                                |
            |  • Jika kosong → pesan error → ulangi                              |
            +----------------------------------+----------------------------------+
                                              |
                                              v
                   +------------------------------+-------------------------------+
                   | Kembalikan data: nama, umur, hobi, kota                    |
                   +------------------------------+-------------------------------+
                                              |
                                              v
                     +--------------------------+--------------------------+
                     |  Tampilkan semua data yang telah diinput            |
                     +--------------------------+--------------------------+
                                              |
                                              v
                   +-----------------------------+-----------------------------+
                   |  Minta konfirmasi pengguna (Y/N)                          |
                   +-----------------------------+-----------------------------+
                                              |
                   +------------------+------------------+
                   |                  |                  |
                   v                  |                  v
             [Input Y]                |              [Input N]
                   |                  |                  |
                   |                  |        +---------+---------+
                   |                  |        | Panggil registrasi() | (ulang input)
                   |                  |        +---------+---------+
                   |                  |                  |
                   |                  +------------------+
                   v
     +-------------------------------+
     |  Simpan data & tampilkan pesan |
     |     "data registrasi disimpan" |
     +-------------------------------+
                   |
                   v
         +---------+---------+
         |     Program Selesai     |
         +-------------------------+

------------------------------------------------------------------------

## 🚀 Cara Menjalankan Program / How to Run

Pastikan Python terinstal.

Run:

``` bash
python main.py
```

------------------------------------------------------------------------

## 📌 Example Output / Contoh Output

    === === === form registrasi === === ===
    Masukkan nama anda: Azusa
    Masukkan umur anda: 18
    Masukkan hobi: Menggambar
    Masukkan nama kota: Bandung
    apakah data ini sudah benar?
        nama    : Shirasu Azusa
        umur    : 18
        hobi    : Menggambar
        kota    : Jawa
    [Y]/[N]?y
    data registrasi disimpan

------------------------------------------------------------------------

## 🧠 Learning Goals / Tujuan Pembelajaran

-   Practice using functions in Python
-   Basic error handling with try-except
-   Understanding loops
-   Creating simple terminal applications

------------------------------------------------------------------------

## 📜 License / Lisensi

Free to use and modify. Created as a personal learning project.
