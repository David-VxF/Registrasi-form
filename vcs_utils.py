import os
import subprocess
import tempfile
from datetime import datetime


def _run_git(args, cwd=None):
    cwd = cwd or os.getcwd()
    try:
        res = subprocess.run(['git'] + args, cwd=cwd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return res.stdout.strip()
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"git error: {e.stderr.strip()}")


def init_repo_if_needed(path=None):
    path = path or os.getcwd()
    # If .git exists, nothing to do
    if os.path.exists(os.path.join(path, '.git')):
        return
    try:
        _run_git(['init'], cwd=path)
    except Exception as e:
        raise


def commit_file(filepath, message: str, author: str | None = None):
    """Stage and commit a single file with a message. Author optional."""
    repo_dir = os.getcwd()
    if not os.path.exists(filepath):
        raise FileNotFoundError(filepath)
    init_repo_if_needed(repo_dir)
    # Stage file
    _run_git(['add', filepath], cwd=repo_dir)
    cmd = ['commit', '-m', message]
    if author:
        # author should be 'Name <email>' ideally; we only have name, use placeholder email
        cmd += ['--author', f"{author} <{author.replace(' ', '').lower()}@local>"]
    try:
        out = _run_git(cmd, cwd=repo_dir)
        return out
    except RuntimeError as e:
        # If no changes to commit, ignore
        if 'nothing to commit' in str(e).lower():
            return ''
        raise


def list_commits_for_file(filepath, max_count=50):
    init_repo_if_needed()
    try:
        out = _run_git(['log', f'--pretty=%H|%an|%ad|%s', f'--max-count={max_count}', '--', filepath])
        commits = []
        if not out:
            return commits
        for line in out.splitlines():
            parts = line.split('|', 3)
            if len(parts) == 4:
                commits.append({'hash': parts[0], 'author': parts[1], 'date': parts[2], 'message': parts[3]})
        return commits
    except Exception:
        return []


def show_file_at_commit(filepath, commit_hash):
    init_repo_if_needed()
    # git show <commit>:<path>
    try:
        out = _run_git(['show', f'{commit_hash}:{filepath}'])
        return out
    except Exception as e:
        raise


def create_backup(filepath):
    if not os.path.exists(filepath):
        raise FileNotFoundError(filepath)
    backup_dir = os.path.join(os.path.dirname(os.path.abspath(filepath)), 'backups')
    os.makedirs(backup_dir, exist_ok=True)
    timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
    backup_path = os.path.join(backup_dir, f"{os.path.basename(filepath)}.{timestamp}.bak")
    import shutil
    shutil.copy2(filepath, backup_path)
    return backup_path


def list_backups(filepath):
    backup_dir = os.path.join(os.path.dirname(os.path.abspath(filepath)), 'backups')
    if not os.path.exists(backup_dir):
        return []
    entries = sorted([os.path.join(backup_dir, f) for f in os.listdir(backup_dir) if f.startswith(os.path.basename(filepath))])
    return entries


def restore_from_backup(backup_path, dest_path=None):
    if not os.path.exists(backup_path):
        raise FileNotFoundError(backup_path)
    dest_path = dest_path or os.path.join(os.getcwd(), os.path.basename(backup_path).split('.', 1)[0])
    import shutil
    shutil.copy2(backup_path, dest_path)
    return dest_path


def restore_file_from_commit(filepath, commit_hash):
    content = show_file_at_commit(filepath, commit_hash)
    # write content to filepath atomically
    dirn = os.path.dirname(os.path.abspath(filepath)) or '.'
    fd, tmp = tempfile.mkstemp(dir=dirn, prefix='.tmp_restore_', suffix='.tmp')
    os.close(fd)
    with open(tmp, 'w', encoding='utf-8') as fh:
        fh.write(content)
    os.replace(tmp, filepath)
    return filepath
