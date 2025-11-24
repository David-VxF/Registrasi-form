import os
import shutil
from datetime import datetime
from dotenv import load_dotenv
from cryptography.fernet import Fernet, InvalidToken
import vcs_utils as vcs

# Muat .env bila belum dimuat
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

    return output_file


def decrypt_csv(input_file, output_file):
    key = load_key()
    f = Fernet(key)

    with open(input_file, "rb") as file:
        data = file.read()

    try:
        decrypted = f.decrypt(data)
    except InvalidToken:
        raise InvalidToken("Kunci dekripsi tidak valid atau file rusak")

    # Tulis ke file output
    with open(output_file, "wb") as file:
        file.write(decrypted)

    return output_file


def save_and_encrypt():
    """Encrypt `data_pengguna.csv` to `data_pengguna.enc` with backup and audit log.

    Returns path to encrypted file on success.
    """
    plain = "data_pengguna.csv"
    enc = "data_pengguna.enc"

    if not os.path.exists(plain):
        raise FileNotFoundError(plain)

    # encrypt
    enc_path = encrypt_csv(plain, enc)
    try:
        os.remove(plain)
    except Exception:
        pass
    try:
        vcs.commit_file(enc_path, 'ENCRYPT data_pengguna.csv -> data_pengguna.enc')
    except Exception:
        pass
    return enc_path


def decrypt_on_start():
    if os.path.exists("data_pengguna.enc"):
        try:
            decrypt_csv("data_pengguna.enc", "data_pengguna.csv")
            try:
                vcs.commit_file('data_pengguna.csv', 'DECRYPT data_pengguna.enc -> data_pengguna.csv')
            except Exception:
                pass
            print("File berhasil dimuat dan siap untuk digunakan")
        except Exception as e:
            try:
                vcs.commit_file('data_pengguna.enc', f'DECRYPT_ERROR: {e}')
            except Exception:
                pass
            print(f"⚠ Gagal mendekripsi: {e}")
    else:
        print("⚠ File terenkripsi tidak ditemukan, menggunakan file CSV biasa.")
