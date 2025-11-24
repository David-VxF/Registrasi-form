import os
import pandas as pd
from difflib import SequenceMatcher
from csv_utils import safe_read_csv, atomic_write_csv, ensure_header
import vcs_utils as vcs


def tambah_header(path="data_pengguna.csv"):
    """Tambah atau pastikan header pada file CSV.
    Sama seperti versi sebelumnya, tapi terpisah agar modul utama lebih bersih.
    """
    print("\n=== Tambah / Pastikan Header CSV ===")
    cols = input("Masukkan nama kolom dipisah koma (atau ketik 'default' untuk nama default) >>> ").strip()
    if cols.lower() == 'default' or cols == '':
        ensure_header(path)
        print("✔ Header default diterapkan jika file kosong.")
        try:
            vcs.commit_file(path, 'HEADER ensure/default applied')
        except Exception:
            pass
        return

    columns = [c.strip() for c in cols.split(',') if c.strip()]
    if not columns:
        print("⚠ Tidak ada kolom valid yang diberikan.")
        return

    if not os.path.exists(path) or os.path.getsize(path) == 0:
        df = pd.DataFrame(columns=columns)
        atomic_write_csv(df, path)
        try:
            vcs.commit_file(path, f"HEADER created with columns: {','.join(columns)}")
        except Exception:
            pass
        print("✔ File dibuat dengan header baru.")
        return

    df = safe_read_csv(path)
    missing = [c for c in columns if c not in df.columns]
    if not missing:
        print("✔ Semua kolom sudah ada.")
        return

    for c in missing:
        df[c] = ""

    new_order = list(df.columns)
    atomic_write_csv(df[new_order], path)
    try:
        vcs.commit_file(path, f"HEADER added columns: {','.join(missing)}")
    except Exception:
        pass
    print(f"✔ Kolom ditambahkan: {', '.join(missing)}")


def hapus_header(path="data_pengguna.csv"):
    print("\n=== Hapus Kolom Header CSV ===")
    df = safe_read_csv(path)
    cols = list(df.columns)
    print("Kolom saat ini:")
    for c in cols:
        print(f"- {c}")

    col = input("Masukkan nama kolom yang ingin dihapus >>> ").strip()
    if col not in df.columns:
        print("⚠ Kolom tidak ditemukan.")
        return

    if len(df.columns) <= 1:
        print("⚠ Tidak boleh menghapus semua kolom.")
        return

    konfirmasi = input(f"Yakin ingin menghapus kolom '{col}'? (Y/N) >>> ").strip().lower()
    if konfirmasi != 'y':
        print("❌ Penghapusan kolom dibatalkan.")
        return

    df = df.drop(columns=[col])
    atomic_write_csv(df, path)
    try:
        vcs.commit_file(path, f"HEADER removed column: {col}")
    except Exception:
        pass
    print(f"✔ Kolom '{col}' berhasil dihapus.")


def edit_header(path="data_pengguna.csv"):
    print("\n=== Edit Nama Kolom Header CSV ===")
    df = safe_read_csv(path)
    cols = list(df.columns)
    print("Kolom saat ini:")
    for c in cols:
        print(f"- {c}")

    old = input("Masukkan nama kolom yang ingin diganti >>> ").strip()
    if old not in df.columns:
        print("⚠ Kolom tidak ditemukan.")
        return

    new = input(f"Masukkan nama baru untuk kolom '{old}' >>> ").strip()
    if not new:
        print("⚠ Nama baru tidak boleh kosong.")
        return

    if new in df.columns:
        print("⚠ Sudah ada kolom dengan nama tersebut.")
        return

    df = df.rename(columns={old: new})
    atomic_write_csv(df, path)
    try:
        vcs.commit_file(path, f"HEADER renamed column {old} -> {new}")
    except Exception:
        pass
    print(f"✔ Kolom '{old}' berhasil diganti menjadi '{new}'.")


def search_pengguna(path="data_pengguna.csv"):
    """Cari pengguna berdasarkan keyword. Kembalikan ID (int) jika user
    memilih untuk mengedit salah satu hasil, atau None.
    """
    df = safe_read_csv(path)
    if df.empty:
        print("⚠ Tidak ada data untuk dicari.")
        return None

    keyword = input("Masukkan kata kunci pencarian >>> ").strip()
    if not keyword:
        print("⚠ Kata kunci kosong.")
        return None

    kw = keyword.lower()
    matches = []

    for idx, row in df.iterrows():
        found = False
        for col in df.columns:
            val = row[col]
            if pd.isna(val):
                continue
            s = str(val).strip()
            if kw in s.lower():
                found = True
                break
            ratio = SequenceMatcher(None, kw, s.lower()).ratio()
            if ratio >= 0.6:
                found = True
                break
            for token in s.lower().split():
                if SequenceMatcher(None, kw, token).ratio() >= 0.8:
                    found = True
                    break
            if found:
                break
        if found:
            matches.append((idx, row))

    if not matches:
        print(f"🔍 Tidak ditemukan hasil untuk '{keyword}'")
        return None

    print(f"🔍 Ditemukan {len(matches)} hasil untuk '{keyword}':")
    cols = list(df.columns)
    display_col = 'nama' if 'nama' in cols else (cols[0] if cols else None)
    for idx, row in matches:
        if display_col:
            preview = row.get(display_col, '')
        else:
            preview = ', '.join(str(row[c]) for c in cols)
        print(f"{idx:04d} - {preview}")

    lihat = input("Lihat detail salah satu ID? (masukkan 4 digit atau kosong untuk batal) >>> ").strip()
    if len(lihat) == 4 and lihat.isdigit():
        id_user = int(lihat)
        if 0 <= id_user < len(df):
            row = df.loc[id_user]
            print(f"\n=== Detail ID {id_user:04d} ===")
            for col in df.columns:
                print(f"{col:7} : {row.get(col, '')}")
            editor = input("Ingin mengedit data ini? (Y/N) >>> ").strip().lower()
            if editor == 'y':
                return id_user
        else:
            print("⚠ ID tidak ditemukan pada hasil.")

    return None
