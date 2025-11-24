import os
import json
import hashlib
import secrets
import tempfile
from datetime import datetime
import vcs_utils as vcs

USERS_FILE = 'users.json'


def _users_path():
    return os.path.abspath(USERS_FILE)


def _atomic_write(obj, path):
    dirn = os.path.dirname(path) or '.'
    fd, tmp = tempfile.mkstemp(prefix='u-', suffix='.tmp', dir=dirn)
    os.close(fd)
    try:
        with open(tmp, 'w', encoding='utf-8') as fh:
            json.dump(obj, fh, ensure_ascii=False, indent=2)
        os.replace(tmp, path)
    finally:
        try:
            if os.path.exists(tmp):
                os.remove(tmp)
        except Exception:
            pass


def load_users():
    path = _users_path()
    if not os.path.exists(path):
        return []
    with open(path, 'r', encoding='utf-8') as fh:
        return json.load(fh)


def save_users(users):
    path = _users_path()
    _atomic_write(users, path)


def _hash_password(password: str, salt: bytes) -> str:
    # PBKDF2-HMAC-SHA256
    dk = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 200_000)
    return dk.hex()


def create_user(username: str, password: str, role: str = 'user') -> dict:
    users = load_users()
    if any(u['username'] == username for u in users):
        raise ValueError('username already exists')
    salt = secrets.token_bytes(16)
    pw_hash = _hash_password(password, salt)
    user = {
        'username': username,
        'salt': salt.hex(),
        'pw_hash': pw_hash,
        'role': role,
        'created_at': datetime.utcnow().isoformat() + 'Z'
    }
    users.append(user)
    save_users(users)
    try:
        vcs.commit_file(_users_path(), f"USER CREATE: {username} (role={role})")
    except Exception:
        pass
    return user


def authenticate(username: str, password: str) -> dict | None:
    users = load_users()
    for u in users:
        if u.get('username') != username:
            continue
        salt = bytes.fromhex(u.get('salt', ''))
        expected = u.get('pw_hash')
        if expected == _hash_password(password, salt):
            return u
    return None
    return None


def list_users():
    users = load_users()
    return [{'username': u['username'], 'role': u.get('role', 'user'), 'created_at': u.get('created_at')} for u in users]


def ensure_admin_exists():
    users = load_users()
    if any(u.get('role') == 'admin' for u in users):
        return
    # Create default admin with random password and print instruction
    pw = secrets.token_urlsafe(12)
    admin = create_user('admin', pw, role='admin')
    print('=== Default admin created ===')
    print('Username: admin')
    print('Password:', pw)
    print('Please change this password after first login.')


def require_role(user: dict | None, allowed: list[str]) -> bool:
    if not user:
        return False
    return user.get('role') in allowed


def prompt_create_user_interactive():
    print('\n=== Buat Pengguna Baru ===')
    username = input('Username >>> ').strip()
    if not username:
        print('Username tidak boleh kosong')
        return
    pw = input('Password >>> ').strip()
    if not pw:
        print('Password tidak boleh kosong')
        return
    role = input("Role ('admin' atau 'user', default 'user') >>> ").strip() or 'user'
    if role not in ('admin', 'user'):
        print('Role tidak valid')
        return
    try:
        create_user(username, pw, role=role)
        print('✔ Pengguna berhasil dibuat')
    except ValueError as e:
        print(f'⚠ {e}')
