import pandas as pd
from dotenv import load_dotenv
from cryptography.fernet import Fernet
import os
# Muat .env sekali saat modul diimpor
load_dotenv()
from csv_utils import (
    safe_read_csv,
    atomic_write_csv,
    append_row,
    delete_row_by_index,
    ensure_header,
)
import vcs_utils as vcs
from crypto_utils import (
    save_and_encrypt,
    decrypt_on_start,
)
from data_utils import (
    tambah_header,
    hapus_header,
    edit_header,
    search_pengguna,
)
import auth_utils as auth
from difflib import SequenceMatcher
from csv_utils import export_to_json
import hashlib

# Admin passphrase hash (hex) stored in .env as ADMIN_PASSPHRASE_HASH
ADMIN_PASSPHRASE_HASH = os.getenv('ADMIN_PASSPHRASE')

# crypto functions moved to crypto_utils.py


# safe_read_csv moved to csv_utils.safe_read_csv

def registrasi():
    while True:
        nama = input("Masukkan nama anda: ")
        if nama == '':
            print('mohon masukkan nama anda!')
        else:
            break
    while True:
        try:
            umur = int(input("Masukkan umur anda: "))
            break
        except ValueError:
            print('harap masukkan angka')        
    while True:
        hobi = input("Masukkan hobi: ")
        if hobi == '':
            print('mohon masukkan hobi anda!')
        else:
            break
    while True:
        kota = input("Masukkan nama kota: ")
        if kota == '':
            print('mohon masukkan nama kota anda tinggal!')
        else:
            break
    return nama,umur,hobi,kota
def dataPengguna():
    print("=== === === Daftar Nama Pengguna === === ===")
    DF = safe_read_csv()
    # Pilih kolom tampil utama: jika ada 'nama' gunakan itu, kalau tidak gunakan kolom pertama
    cols = list(DF.columns)
    display_col = 'nama' if 'nama' in cols else (cols[0] if cols else '')
    for i, val in enumerate(DF[display_col] if display_col else []):
        print(f"{i:04d} {val}")

def register():
    print('=== === === form registrasi === === ===')
    # Ambil header saat ini (atau buat default jika belum ada)
    df_template = safe_read_csv()
    columns = list(df_template.columns)
    if not columns:
        ensure_header("data_pengguna.csv")
        df_template = safe_read_csv()
        columns = list(df_template.columns)

    while True:
        row = {}
        for col in columns:
            while True:
                val = input(f"Masukkan {col}: ").strip()
                if val == "":
                    print(f"mohon masukkan {col}!")
                    continue
                if 'umur' in col.lower() or 'age' in col.lower():
                    if not val.isdigit() or int(val) <= 0:
                        print('harap masukkan angka positif untuk umur')
                        continue
                row[col] = val
                break

        print("\napakah data ini sudah benar?")
        for col in columns:
            print(f"{col}\t: {row.get(col, '')}")

        Auth = input("[Y]/[N]? >>> ").strip().lower()
        if Auth == 'n':
            print('Silakan masukkan ulang data Anda')
            continue
        elif Auth == 'y':
            append_row("data_pengguna.csv", row)
            print('✔ Data registrasi disimpan')
            return
        else:
            print('Silakan masukkan Y atau N saja')

def auto_cast(value):
    """
    Mencoba mengubah input user ke tipe data paling cocok:
    urutan: int -> float -> bool -> str
    """
    value = value.strip()

    # Jika kosong, anggap string kosong saja
    if value == "":
        return ""

    # Integer
    try:
        return int(value)
    except ValueError:
        pass

    # Float
    try:
        return float(value)
    except ValueError:
        pass

    # Boolean
    lower = value.lower()
    if lower in ["true", "false"]:
        return lower == "true"

    # Default string
    return value

def lihatPengguna():
    # Load ulang data setiap fungsi dipanggil
    df = safe_read_csv()

    # Bersihkan header
    df.columns = df.columns.str.strip()

    # Bersihkan isi data (tiap sel string)
    df = df.apply(lambda col: col.str.strip() if col.dtype == "object" else col)

    while True:
        id_str = input("Masukkan ID (4 digit) >>> ")

        if len(id_str) != 4 or not id_str.isdigit():
            print("ID tidak valid\n")
            continue

        id_user = int(id_str)

        if not (0 <= id_user < len(df)):
            print("ID tidak ditemukan\n")
            continue

        break

    row = df.loc[id_user]

    print(f"\n=== === === Data pengguna {id_user:04d} === === ===")
    for col in df.columns:
        print(f"{col:15} : {row.get(col, '')}")

def hapusPengguna():
    df = safe_read_csv()

    # Strip header
    df.columns = df.columns.str.strip()

    # Strip seluruh data (hanya string)
    df = df.apply(lambda col: col.str.strip() if col.dtype == "object" else col)

    print("\n=== Hapus Data Pengguna ===")
    print("Contoh format ID: 0000, 0001, 0002")

    id_str = input("Masukkan ID yang ingin dihapus (4 digit) >>> ")

    while True:
        # Validasi format ID
        if not id_str.isdigit() or len(id_str) != 4:
            print("⚠ Input salah. ID harus terdiri dari 4 angka (contoh: 0003)")
            id_str = input("Harap masukkan ID sesuai format >>> ")
            continue

        id_user = int(id_str)

        # Validasi ID ada
        if id_user < 0 or id_user >= len(df):
            print(f"⚠ ID {id_str} tidak ditemukan dalam data.")
            id_str = input("Silakan masukkan ID yang valid sesuai daftar >>> ")
            continue
        
        row = df.loc[id_user]

        print("\nData ditemukan:\n")
        print(f"ID      : {id_user:04d}")
        for col in df.columns:
            print(f"{col:7} : {row.get(col, '')}")

        # Loop konfirmasi
        while True:
            konfirmasi = input("Apakah benar ingin menghapus data ini? (Y/N) >>> ").strip().lower()

            if konfirmasi == "y":
                # Gunakan helper atomik untuk menghapus baris
                ok = delete_row_by_index("data_pengguna.csv", id_user)
                if ok:
                    print(f"✔ Data ID {id_user:04d} berhasil dihapus.")
                else:
                    print(f"⚠ Gagal menghapus ID {id_user:04d}.")
                return

            elif konfirmasi == "n":
                print("❌ Penghapusan dibatalkan.")
                return

            else:
                print("⚠ Hanya boleh memasukkan 'Y' atau 'N'.")

# Header management functions are provided by `data_utils.py` and imported at module top.


# search_pengguna moved to data_utils to avoid circular imports

def editPengguna(id_user=None, current_user=None):
    # Load data dan bersihkan
    df = safe_read_csv()
    df.columns = df.columns.str.strip()
    df = df.apply(lambda col: col.str.strip() if col.dtype == "object" else col)

    # Jika id_user tidak diberikan, minta dari user
    if id_user is None:
        print("\n=== Edit Data Pengguna ===")
        print("Contoh format ID: 0000, 0001, 0002")
        id_str = input("Masukkan ID yang ingin diedit datanya (4 digit) >>> ").strip()
        while True:
            if not id_str.isdigit() or len(id_str) != 4:
                print("ID harus terdiri dari 4 digit angka.")
                id_str = input("Masukkan ID sesuai format >>> ").strip()
                continue
            id_user = int(id_str)
            if not (0 <= id_user < len(df)):
                print(f"ID {id_str} tidak ditemukan dalam data.")
                id_str = input("Masukkan ID yang valid sesuai daftar >>> ").strip()
                continue
            break

    # Validasi akhir id_user
    if not isinstance(id_user, int) or not (0 <= id_user < len(df)):
        print("⚠ ID tidak valid atau di luar jangkauan.")
        return

    row = df.loc[id_user]
    columns = list(df.columns)

    while True:
        print(f"\n=== === === Data Pengguna {id_user:04d} === === ===")
        for col in columns:
            print(f"{col:15} : {row.get(col, '')}")

        print("\nPilih kolom yang ingin diedit:")
        for idx, col in enumerate(columns, start=1):
            print(f"{idx}. Edit {col}")
        print(f"{len(columns)+1}. Edit Semua")
        print("0. Kembali")

        pilihan = input("Pilih data yang ingin diedit >>> ").strip()

        if not pilihan.isdigit():
            print("Pilihan harus berupa angka.")
            continue

        pilihan = int(pilihan)

        if pilihan == 0:
            print("Kembali ke menu utama.")
            return

        if 1 <= pilihan <= len(columns):
            col_to_edit = columns[pilihan - 1]

            while True:
                new_val = input(
                    f"Masukkan {col_to_edit} baru (sebelumnya: {row.get(col_to_edit, '')}) >>> "
                ).strip()

                if new_val == "":
                    print("Input tidak boleh kosong.")
                    continue

                # Jika butuh konversi tipe, gunakan auto_cast jika ada
                try:
                    new_val_cast = auto_cast(new_val)
                except NameError:
                    new_val_cast = new_val
                break

            print("\nPreview Perubahan:")
            print(f"{col_to_edit:15} : {row.get(col_to_edit, '')}  -->  {new_val_cast}")

            # Konfirmasi
            while True:
                konfirmasi = input("Simpan perubahan? (Y/N) >>> ").strip().lower()
                if konfirmasi == "y":
                    # Ensure column can hold string/object values to avoid pandas dtype warnings
                    try:
                        if df[col_to_edit].dtype != object:
                            df[col_to_edit] = df[col_to_edit].astype(object)
                    except Exception:
                        pass

                    df.at[id_user, col_to_edit] = str(new_val_cast)
                    atomic_write_csv(df, "data_pengguna.csv")
                    actor = current_user.get('username') if isinstance(current_user, dict) else None
                    try:
                        vcs.commit_file('data_pengguna.csv', f"EDIT: ID {id_user:04d} - set {col_to_edit} -> {new_val_cast} By {actor}")
                    except Exception:
                        pass
                    print(f"Data ID {id_user:04d} berhasil disimpan.")
                    return
                elif konfirmasi == "n":
                    print("Perubahan dibatalkan.")
                    return
                else:
                    print("Input harus Y atau N saja.")

        elif pilihan == len(columns) + 1:
                updates = {}

                for col in columns:
                    while True:
                        val = input(f"Masukkan {col} baru (sebelumnya: {row[col]}) >>> ").strip()
                        if val == "":
                            print("Input tidak boleh kosong.")
                            continue
                        updates[col] = auto_cast(val)
                        break

                print("\nPreview perubahan:")
                for col in columns:
                    print(f"{col:15} : {row[col]}  -->  {updates[col]}")

                while True:
                    konfirmasi = input("Simpan semua perubahan? (Y/N) >>> ").strip().lower()
                    if konfirmasi == "y":
                        # Ensure each column can accept string/object values before assignment
                        for col in columns:
                            try:
                                if df[col].dtype != object:
                                    df[col] = df[col].astype(object)
                            except Exception:
                                pass
                            df.at[id_user, col] = str(updates[col])
                        atomic_write_csv(df, "data_pengguna.csv")
                        actor = current_user.get('username') if isinstance(current_user, dict) else None
                        try:
                            vcs.commit_file('data_pengguna.csv', f"EDIT: ID {id_user:04d} - multiple fields {updates} By {actor}")
                        except Exception:
                            pass
                        print(f"Data ID {id_user:04d} berhasil disimpan.")
                        return
                    elif konfirmasi == "n":
                        print("Perubahan dibatalkan.")
                        return
                    else:
                        print("Masukkan hanya Y atau N.")
        else:
            print("Pilihan tidak valid.")

def main():
    # Ensure at least one admin exists before starting (creates default admin if none)
    auth.ensure_admin_exists()

    # Auto-login as guest by default
    current_user = {'username': 'guest', 'role': 'guest'}
    print("✔ Masuk otomatis sebagai 'guest'. Untuk mengakses admin, masukkan passphrase di prompt menu.")

    while True:
        try:
            raw = input('''=== === === Menu Aplikasi === === ===
1. lihat semua pengguna
2. masukkan data pengguna baru
3. lihat data pengguna
4. hapus pengguna
5. edit data pengguna
6. simpan dan keluar
7. tambah header / pastikan header
8. hapus kolom header
9. edit nama kolom header
10. cari pengguna
11. ekspor data ke JSON
12. manajemen pengguna (admin)
13. buat backup manual (CSV)
14. restore dari backup
15. restore dari version control (git)
pilih menu >>> ''').strip()

            # Allow entering a passphrase at the main prompt to become admin 'Shirasu Azusa'
            if raw:
                try:
                    hashed = hashlib.sha256(raw.encode('utf-8')).hexdigest()
                except Exception:
                    hashed = None
                if ADMIN_PASSPHRASE_HASH and hashed and hashed == ADMIN_PASSPHRASE_HASH:
                    # promote to admin user named 'Shirasu Azusa'
                    current_user = {'username': 'Shirasu Azusa', 'role': 'admin'}
                    print("✔ Terautentikasi sebagai admin [Shirasu Azusa]")
                    # continue to menu as admin
                    continue

            try:
                pilih = int(raw)
            except ValueError:
                print('harap masukkan angka atau passphrase yang valid')
                continue

            if pilih == 1:
                dataPengguna()
            elif pilih == 2:
                register()
            elif pilih == 3:
                lihatPengguna()
            elif pilih == 4:
                # delete users - admin only
                if not auth.require_role(current_user, ['admin']):
                    print('⚠ Akses ditolak: hanya admin yang boleh menghapus data')
                else:
                    hapusPengguna()
            elif pilih == 5:
                # edit - allow users to edit but admins can edit anyone; simple policy: allow both
                editPengguna(current_user=current_user)
            elif pilih == 6:
                # Only admin may encrypt/save final data
                if not auth.require_role(current_user, ['admin']):
                    print('⚠ Akses ditolak: hanya admin yang boleh menyimpan/encrypt data')
                else:
                    save_and_encrypt()
                    print('✔ Data berhasil disimpan Keluar dari aplikasi')
                    exit()
            elif pilih == 7:
                if not auth.require_role(current_user, ['admin']):
                    print('⚠ Akses ditolak: hanya admin yang boleh memodifikasi header')
                else:
                    tambah_header()
            elif pilih == 8:
                if not auth.require_role(current_user, ['admin']):
                    print('⚠ Akses ditolak: hanya admin yang boleh memodifikasi header')
                else:
                    hapus_header()
            elif pilih == 9:
                if not auth.require_role(current_user, ['admin']):
                    print('⚠ Akses ditolak: hanya admin yang boleh memodifikasi header')
                else:
                    edit_header()
            elif pilih == 10:
                _id = search_pengguna()
                if isinstance(_id, int):
                    editPengguna(_id, current_user=current_user)
            elif pilih == 11:
                # Ekspor data sebagai JSON plaintext
                print('\n=== Ekspor Data ===')
                out = input("Nama file keluaran (atau kosong untuk 'data_pengguna.json') >>> ").strip()
                out_path = out if out else None
                try:
                    path = export_to_json('data_pengguna.csv', out_path=out_path)
                    print(f"✔ Data berhasil diekspor ke {path}")
                except Exception as e:
                    print(f"⚠ Gagal mengekspor data: {e}")
            elif pilih == 12:
                # User management (admin only)
                if not auth.require_role(current_user, ['admin']):
                    print('⚠ Akses ditolak: hanya admin yang boleh mengelola pengguna')
                else:
                    print('\n=== Manajemen Pengguna ===')
                    print('1. Daftar pengguna')
                    print('2. Buat pengguna baru')
                    sub = input('pilih >>> ').strip()
                    if sub == '1':
                        for u in auth.list_users():
                            print(f"- {u['username']} (role={u['role']}) created={u.get('created_at')}")
                    elif sub == '2':
                        auth.prompt_create_user_interactive()
                    else:
                        print('Pilihan tidak valid')
            elif pilih == 13:
                # Manual backup of CSV
                try:
                    bp = vcs.create_backup('data_pengguna.csv')
                    print(f"✔ Backup dibuat: {bp}")
                except Exception as e:
                    print(f"⚠ Gagal membuat backup: {e}")
            elif pilih == 14:
                # Restore from backup file
                try:
                    bks = vcs.list_backups('data_pengguna.csv')
                    if not bks:
                        print('⚠ Tidak ada backup tersedia.')
                    else:
                        print('Backup tersedia:')
                        for i, p in enumerate(bks, start=1):
                            print(f"{i}. {p}")
                        sel = input('Pilih nomor backup untuk restore >>> ').strip()
                        if sel.isdigit() and 1 <= int(sel) <= len(bks):
                            chosen = bks[int(sel)-1]
                            vcs.restore_from_backup(chosen, dest_path='data_pengguna.csv')
                            print(f"✔ Berhasil merestore dari {chosen}")
                        else:
                            print('Pilihan tidak valid')
                except Exception as e:
                    print(f"⚠ Gagal merestore backup: {e}")
            elif pilih == 15:
                # Restore from VCS (git) history
                try:
                    commits = vcs.list_commits_for_file('data_pengguna.csv', max_count=50)
                    if not commits:
                        print('⚠ Tidak ada riwayat versi untuk file ini.')
                    else:
                        for i, c in enumerate(commits, start=1):
                            print(f"{i}. {c['hash'][:7]} {c['date']} {c['author']} - {c['message']}")
                        sel = input('Pilih nomor commit untuk restore >>> ').strip()
                        if sel.isdigit() and 1 <= int(sel) <= len(commits):
                            chosen = commits[int(sel)-1]
                            vcs.restore_file_from_commit('data_pengguna.csv', chosen['hash'])
                            print(f"✔ Berhasil merestore dari commit {chosen['hash']}")
                        else:
                            print('Pilihan tidak valid')
                except Exception as e:
                    print(f"⚠ Gagal merestore dari version control: {e}")
        except ValueError:
            print('harap masukkan angka')
            continue
        except KeyboardInterrupt:
            save_and_encrypt()
            break
decrypt_on_start()
main()
