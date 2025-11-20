import pandas as pd
dummy = ''
flag = True
DF = pd.read_csv("data_pengguna.csv")
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
    DF = pd.read_csv("data_pengguna.csv")
    for i,nama in enumerate(DF['nama']):
        print(f"{i:04d} {nama}")
        dummy = input()

def register():
    flag = True
    print('=== === === form registrasi === === ===')
    nama, umur, hobi, kota = registrasi()
    while flag == True:
        Auth = input(f'''apakah data ini sudah benar?
Nama\t: {nama}
Umur\t: {umur}
Hobi\t: {hobi}
Kota\t: {kota}
[Y]/[N]? >>> ''')
        Auth = Auth.lower()
        if Auth == 'n':
            print('silahkan masukan ulang data anda')
            nama, umur, hobi, kota = registrasi()
        elif Auth == 'y':
            nama, umur, hobi, kota
            with open("data_pengguna.csv", "a+") as file:
                file.write(f"{nama}, {umur}, {hobi}, {kota}\n")            
            print('data registrasi disimpan')
            break
        else:
            while True:
                Auth = input('silahkan masukkan Y/N saja!!')
                Auth = Auth.lower()
                if Auth == 'n':
                    print('silahkan masukan ulang data anda')
                    nama, umur, hobi, kota = registrasi()
                    break
                elif Auth == 'y':
                    print('data registrasi disimpan')
                    nama, umur, hobi, kota
                    with open("data_pengguna.csv", "a+") as file:
                        file.write(f"{nama}, {umur}, {hobi}, {kota}\n")            
                    print('data registrasi disimpan')
                    flag = False
                    dummy = input()
                    break
def lihatPengguna():
    while True:
        id_str = input("Masukkan ID (4 digit) >>> ")

        if len(id_str) != 4 or not id_str.isdigit():
            print("ID tidak valid\n")
            continue

        id_user = int(id_str)

        if id_user >= len(DF):
            print("ID tidak ditemukan\n")
            continue
        elif id_user < 0 or id_user >= len(DF):
            print("ID tidak ditemukan")
            continue
        break

    row = DF.loc[id_user]

    print(f"""\n=== === === Data pengguna {id_user:04d} === === ===
Nama    : {row['nama']}
Umur    : {row['umur']}
Hobi    : {row['hobi']}
Kota    : {row['kota']}""")
    dummy = input()

def hapusPengguna():
    df = pd.read_csv("data_pengguna.csv")

    print("\n=== Hapus Data Pengguna ===")
    print("Contoh format ID: 0000, 0001, 0002")  # tampil sekali

    # Prompt pertama (hanya sekali)
    id_str = input("Masukkan ID yang ingin dihapus (4 digit) >>> ")

    while True:
        # Cek format input
        if not id_str.isdigit() or len(id_str) != 4:
            print("⚠ Input salah. ID harus terdiri dari 4 angka (contoh: 0003)")
            id_str = input("Harap masukkan ID sesuai format >>> ")
            continue

        id_user = int(id_str)

        # Cek apakah ID ada
        if id_user < 0 or id_user >= len(df):
            print(f"⚠ ID {id_str} tidak ditemukan dalam data.")
            id_str = input("Silakan masukkan ID yang valid sesuai daftar >>> ")
            continue
        
        # Jika valid, tampilkan datanya
        row = df.loc[id_user]

        print(f"""
Data ditemukan:

ID      : {id_user:04d}
Nama    : {row['nama'.strip()]}
Umur    : {row['umur'.strip()]}
Hobi    : {row['hobi'.strip()]}
Kota    : {row['kota'.strip()]}
""")

        konfirmasi = input("Apakah benar ingin menghapus data ini? (Y/N) >>> ").lower()

        if konfirmasi != "y":
            print("❌ Penghapusan dibatalkan.")
            return

        # Hapus data
        df = df.drop(index=id_user).reset_index(drop=True)
        df.to_csv("data_registrasi.csv", index=False)

        print(f"✔ Data ID {id_user:04d} berhasil dihapus.")
        dummy = input()
        break


def main():
    while True:
        try:
            pilih = int(input('''=== === === Menu Aplikasi === === ===
1. lihat data semua pengguna
2. masukkan data pengguna baru
3. lihat data pengguna
4. hapus pengguna
>>> '''))
        except ValueError:
            print('harap masukkan angka')
            continue
        if pilih == 1:
            dataPengguna()
        elif pilih == 2:
            register()
        elif pilih == 3:
            lihatPengguna()
        elif pilih == 4:
            hapusPengguna()
main()
