import pandas as pd
from dotenv import load_dotenv
from cryptography.fernet import Fernet
import os
# Muat .env sekali saat modul diimpor
load_dotenv()

def load_key():
    key = os.getenv("APP_SECRET_KEY")

    if not key:
        raise ValueError("❌ Key tidak ditemukan di .env")

    return key.encode()

def encrypt_csv(input_file, output_file):
    key = load_key()
    f = Fernet(key)

    with open(input_file, "rb") as file:
        data = file.read()

    encrypted = f.encrypt(data)

    with open(output_file, "wb") as file:
        file.write(encrypted)

    print(f"✔ File {output_file} berhasil disimpan")

def decrypt_csv(input_file, output_file):
    key = load_key()
    f = Fernet(key)

    with open(input_file, "rb") as file:
        data = file.read()

    decrypted = f.decrypt(data)

    with open(output_file, "wb") as file:
        file.write(decrypted)

def save_and_encrypt():
    encrypt_csv("data_pengguna.csv", "data_pengguna.enc")
    os.remove("data_pengguna.csv")

def decrypt_on_start():
    if os.path.exists("data_pengguna.enc"):
        decrypt_csv("data_pengguna.enc", "data_pengguna.csv")
        print("File berhasil dimuat dan siap untuk digunakan")
    else:
        print("⚠ File terenkripsi tidak ditemukan, menggunakan file CSV biasa.")


def safe_read_csv(path="data_pengguna.csv"):
    try:
        df = pd.read_csv(path)
    except (FileNotFoundError, pd.errors.EmptyDataError):
        df = pd.DataFrame(columns=["nama", "umur", "hobi", "kota"])
    except Exception as e:
        print(f"⚠ Gagal membaca {path}: {e}")
        df = pd.DataFrame(columns=["nama", "umur", "hobi", "kota"])
    return df

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
    for i,nama in enumerate(DF['nama']):
        print(f"{i:04d} {nama}")

def register():
    print('=== === === form registrasi === === ===')
    while True:
        nama, umur, hobi, kota = registrasi()

        while True:
            Auth = input(f'''apakah data ini sudah benar?
Nama\t: {nama}
Umur\t: {umur}
Hobi\t: {hobi}
Kota\t: {kota}
[Y]/[N]? >>> ''').strip().lower()

            if Auth == 'n':
                print('Silakan masukkan ulang data Anda')
                break  # keluar konfirmasi, ulang registrasi
            elif Auth == 'y':
                # Simpan data menggunakan pandas (safely append)
                row = {"nama": nama, "umur": umur, "hobi": hobi, "kota": kota}
                df_row = pd.DataFrame([row])
                write_header = not (os.path.exists("data_pengguna.csv") and os.path.getsize("data_pengguna.csv") > 0)
                df_row.to_csv("data_pengguna.csv", mode="a", header=write_header, index=False)
                print('✔ Data registrasi disimpan')
                return
            else:
                print('Silakan masukkan Y atau N saja')

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

    print(f"""\n=== === === Data pengguna {id_user:04d} === === ===
Nama    : {row['nama']}
Umur    : {row['umur']}
Hobi    : {row['hobi']}
Kota    : {row['kota']}""")

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

        print(f"""
Data ditemukan:

ID      : {id_user:04d}
Nama    : {row['nama']}
Umur    : {row['umur']}
Hobi    : {row['hobi']}
Kota    : {row['kota']}
""")

        # Loop konfirmasi
        while True:
            konfirmasi = input("Apakah benar ingin menghapus data ini? (Y/N) >>> ").strip().lower()

            if konfirmasi == "y":
                df = df.drop(index=id_user).reset_index(drop=True)
                df.to_csv("data_pengguna.csv", index=False)
                print(f"✔ Data ID {id_user:04d} berhasil dihapus.")
                return

            elif konfirmasi == "n":
                print("❌ Penghapusan dibatalkan.")
                return

            else:
                print("⚠ Hanya boleh memasukkan 'Y' atau 'N'.")



def editPengguna():
    df = safe_read_csv()

    df.columns = df.columns.str.strip()
    df = df.apply(lambda col: col.str.strip() if col.dtype == "object" else col)

    print("\n=== Edit Data Pengguna ===")
    print("Contoh format ID: 0000, 0001, 0002")

    id_str = input("Masukkan ID yang ingin diedit datanya (4 digit) >>> ")

    while True:
        if not id_str.isdigit() or len(id_str) != 4:
            print("⚠ ID harus terdiri dari 4 digit angka!")
            id_str = input("Masukkan ID sesuai format >>> ")
            continue

        id_user = int(id_str)

        if not (0 <= id_user < len(df)):
            print(f"⚠ ID {id_str} tidak ditemukan dalam data!")
            id_str = input("Masukkan ID yang valid sesuai daftar >>> ")
            continue

        break

    row = df.loc[id_user]

    while True:
        print(f"""
=== Data Pengguna {id_user:04d} ===
Nama    : {row['nama']}
Umur    : {row['umur']}
Hobi    : {row['hobi']}
Kota    : {row['kota']}

1. Edit Nama
2. Edit Umur
3. Edit Hobi
4. Edit kota
5. Edit Semua
0. Kembali
""")

        pilih = input("Pilih data yang ingin diedit >>> ").strip()

        # === EDIT NAMA ===
        if pilih == "1":
            nama_baru = input("Masukkan nama baru >>> ").strip()
            if nama_baru == "":
                print("⚠ Input tidak boleh kosong!")
                continue
            df.loc[id_user, "nama"] = nama_baru

        # === EDIT UMUR (DENGAN VALIDASI BARU) ===
        elif pilih == "2":
            while True:
                umur_baru = input("Masukkan umur baru >>> ").strip()

                if umur_baru == "":
                    print("⚠ Input tidak boleh kosong!")
                    continue

                if not umur_baru.isdigit():
                    print("⚠ Umur harus berupa angka!")
                    continue

                if int(umur_baru) <= 0:
                    print("⚠ Umur harus angka positif!")
                    continue

                df.loc[id_user, "umur"] = umur_baru
                break

        # === EDIT HOBI ===
        elif pilih == "3":
            hobi_baru = input("Masukkan hobi baru >>> ").strip()
            if hobi_baru == "":
                print("⚠ Input tidak boleh kosong!")
                continue
            df.loc[id_user, "hobi"] = hobi_baru

        # === EDIT KOTA ===
        elif pilih == "4":
            kota_baru = input("Masukkan kota baru >>> ").strip()
            if kota_baru == "":
                print("⚠ Input tidak boleh kosong!")
                continue
            df.loc[id_user, "kota"] = kota_baru

        # === EDIT SEMUA FIELD SEKALIGUS ===
        elif pilih == "5":
            nama_baru = input("Masukkan nama baru >>> ").strip()
            umur_baru = input("Masukkan umur baru >>> ").strip()
            hobi_baru = input("Masukkan hobi baru >>> ").strip()
            kota_baru = input("Masukkan kota baru >>> ").strip()

            # Validasi untuk semua
            if not (nama_baru and umur_baru and hobi_baru and kota_baru):
                print("⚠ Tidak boleh ada data kosong!")
                continue

            if not umur_baru.isdigit():
                print("⚠ Umur harus berupa angka!")
                continue

            df.loc[id_user] = [nama_baru, umur_baru, hobi_baru, kota_baru]

        elif pilih == "0":
            print("⏪ Kembali ke menu utama.")
            return

        else:
            print("⚠ Pilihan tidak valid, coba lagi!")
            continue

        # === KONFIRMASI SIMPAN ===
        while True:
            konfirmasi = input("Simpan perubahan? (Y/N) >>> ").strip().lower()
            if konfirmasi == "y":
                df.to_csv("data_pengguna.csv", index=False)
                print(f"✔ Data ID {id_user:04d} berhasil disimpan!")
                return
            elif konfirmasi == "n":
                print("❌ Perubahan dibatalkan.")
                return
            else:
                print("⚠ Hanya boleh memasukkan 'Y' atau 'N'.")

def main():
    while True:
        try:
            pilih = int(input('''=== === === Menu Aplikasi === === ===
1. lihat data semua pengguna
2. masukkan data pengguna baru
3. lihat data pengguna
4. hapus pengguna
5. edit data pengguna
>>> '''))
            if pilih == 1:
                dataPengguna()
            elif pilih == 2:
                register()
            elif pilih == 3:
                lihatPengguna()
            elif pilih == 4:
                hapusPengguna()
            elif pilih == 5:
                editPengguna()
            elif pilih == 6:
                save_and_encrypt()
        except ValueError:
            print('harap masukkan angka')
            continue
        except KeyboardInterrupt:
            save_and_encrypt()
            break
decrypt_on_start()
main()
