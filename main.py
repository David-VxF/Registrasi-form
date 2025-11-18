flag = True
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
print('=== === === form registrasi === === ===')
nama, umur, hobi, kota = registrasi()
while flag == True:
    Auth = input(f'''apakah data ini sudah benar?
    nama\t: {nama}
    umur\t: {umur}
    hobi\t: {hobi}
    kota\t: {kota}
[Y]/[N]?''')
    Auth = Auth.lower()
    if Auth == 'n':
        print('silahkan masukan ulang data anda')
        registrasi()
    elif Auth == 'y':
        print('data registrasi disimpan')
        break
    else:
        while True:
            Auth = input('silahkan masukkan Y/N saja!!')
            Auth = Auth.lower()
            if Auth == 'n':
                print('silahkan masukan ulang data anda')
                registrasi()
                break
            elif Auth == 'y':
                print('data registrasi disimpan')
                flag = False
                break
