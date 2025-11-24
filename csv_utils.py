import pandas as pd
import os
import tempfile
from datetime import datetime
import vcs_utils as vcs
import json


def default_columns():
    return ["nama", "umur", "hobi", "kota"]


def safe_read_csv(path="data_pengguna.csv"):
    """Baca CSV tanpa memaksa header default kecuali file benar-benar kosong."""
    if not os.path.exists(path) or os.path.getsize(path) == 0:
        # File kosong → gunakan header default
        df = pd.DataFrame(columns=default_columns())
        return df

    try:
        df = pd.read_csv(path)
    except pd.errors.EmptyDataError:
        # CSV ada tapi kosong → pakai default
        df = pd.DataFrame(columns=default_columns())
        return df
    except Exception as e:
        print(f"⚠ Gagal membaca {path}: {e}")
        df = pd.DataFrame(columns=default_columns())
        return df

    # Trim whitespace isi
    df = df.apply(lambda col: col.str.strip() if col.dtype == "object" else col)

    return df  # ← PERHATIKAN: tidak ada reorder, tidak memaksa header!


def atomic_write_csv(df, path="data_pengguna.csv"):
    """Tulis CSV secara atomik dengan menulis ke file sementara lalu mengganti target.
    Menghindari file korupsi jika proses terhenti di tengah penulisan."""
    directory = os.path.dirname(os.path.abspath(path)) or "."
    fd, tmp_path = tempfile.mkstemp(dir=directory, prefix=".tmp_", suffix=".csv")
    os.close(fd)
    try:
        df.to_csv(tmp_path, index=False)
        os.replace(tmp_path, path)
        # Commit change to VCS (git) if available
        try:
            vcs.commit_file(path, f"UPDATE {os.path.basename(path)}")
        except Exception:
            pass
    finally:
        # Pastikan file sementara tidak tertinggal
        if os.path.exists(tmp_path):
            try:
                os.remove(tmp_path)
            except Exception:
                pass


def ensure_header(path="data_pengguna.csv", columns=None):
    if columns is None:
        columns = default_columns()
    if not os.path.exists(path) or os.path.getsize(path) == 0:
        df = pd.DataFrame(columns=columns)
        atomic_write_csv(df, path)


def append_row(path, row_dict):
    if not os.path.exists(path) or os.path.getsize(path) == 0:
        # File benar-benar kosong → buat file dengan header default
        df = pd.DataFrame([row_dict], columns=default_columns())
        atomic_write_csv(df, path)
        try:
            vcs.commit_file(path, f"CREATE {os.path.basename(path)} with first row")
        except Exception:
            pass
        return

    # File ada → baca header dari CSV
    df = pd.read_csv(path)

    # Isi row sesuai header yang ada
    for col in df.columns:
        if col not in row_dict:
            row_dict[col] = ""

    df_row = pd.DataFrame([row_dict])
    df = pd.concat([df, df_row], ignore_index=True)
    atomic_write_csv(df, path)
    try:
        vcs.commit_file(path, f"APPEND row to {os.path.basename(path)}")
    except Exception:
        pass


def delete_row_by_index(path, index):
    df = safe_read_csv(path)
    if not (0 <= index < len(df)):
        return False
    df = df.drop(index=index).reset_index(drop=True)
    atomic_write_csv(df, path)
    try:
        vcs.commit_file(path, f"DELETE row {index} from {os.path.basename(path)}")
    except Exception:
        pass
    return True


def edit_row_by_index(path, index, updates, columns=None):
    df = safe_read_csv(path, columns)
    if not (0 <= index < len(df)):
        return False

    for k, v in updates.items():
        if k in df.columns:
            df.at[index, k] = v
    atomic_write_csv(df, path)
    try:
        vcs.commit_file(path, f"EDIT row {index} in {os.path.basename(path)}")
    except Exception:
        pass
    return True


def export_to_json(path="data_pengguna.csv", out_path=None, orient='records', indent=2):
    """Export CSV data to a JSON file (plaintext).

    - `path`: source CSV path
    - `out_path`: if None, create `data_pengguna.json` alongside CSV
    - `orient` and `indent` passed to pandas.DataFrame.to_json-like behavior
    Returns output path on success.
    """
    df = safe_read_csv(path)
    if out_path is None:
        out_path = os.path.splitext(path)[0] + '.json'

    # Convert DataFrame to list-of-dicts for pretty JSON
    try:
        records = df.where(pd.notnull(df), None).to_dict(orient='records')
    except Exception:
        # Fallback: coerce via string conversion
        records = []
        for _, row in df.iterrows():
            rec = {col: (None if pd.isna(row[col]) else row[col]) for col in df.columns}
            records.append(rec)

    # Write atomically
    dirn = os.path.dirname(os.path.abspath(out_path)) or '.'
    fd, tmp_path = tempfile.mkstemp(prefix='export-', suffix='.json', dir=dirn)
    os.close(fd)
    try:
        with open(tmp_path, 'w', encoding='utf-8') as fh:
            json.dump(records, fh, ensure_ascii=False, indent=indent)
        os.replace(tmp_path, out_path)
        try:
            vcs.commit_file(out_path, f"EXPORT json from {os.path.basename(path)}")
        except Exception:
            pass
        return out_path
    except Exception as e:
        try:
            os.remove(tmp_path)
        except Exception:
            pass
        try:
            vcs.commit_file(out_path, f"EXPORT_ERROR json from {os.path.basename(path)}")
        except Exception:
            pass
        raise


def validate_columns(df, required_columns):
    return all(c in df.columns for c in required_columns)
