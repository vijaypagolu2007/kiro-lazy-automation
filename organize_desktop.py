#!/usr/bin/env python3
"""
organize_desktop.py
Desktop declutter + backup automation
Usage:
  python organize_desktop.py --source C:\Path\To\Folder --backup C:\Path\To\Backup --dry-run
"""

import argparse
import os
import shutil
import json
from datetime import datetime
from pathlib import Path
import zipfile

# File type mapping
EXT_FOLDERS = {
    'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.heic'],
    'Documents': ['.pdf', '.docx', '.doc', '.txt', '.md', '.pptx', '.xlsx'],
    'Archives': ['.zip', '.tar', '.gz', '.rar'],
    'Code': ['.py', '.java', '.c', '.cpp', '.js', '.html', '.css'],
    'Media': ['.mp3', '.mp4', '.mov', '.mkv'],
    'Installers': ['.exe', '.msi', '.dmg']
}

def ext_to_folder(ext):
    ext = ext.lower()
    for folder, exts in EXT_FOLDERS.items():
        if ext in exts:
            return folder
    return 'Others'

def collect_files(src_path):
    files = []
    for entry in os.scandir(src_path):
        if entry.is_file():
            files.append(entry.path)
    return files

def ensure_path(p, dry_run):
    if not os.path.exists(p):
        if dry_run:
            print(f"[DRY] mkdir {p}")
        else:
            os.makedirs(p, exist_ok=True)

def move_file(src, dest_dir, dry_run):
    ensure_path(dest_dir, dry_run)
    dest = os.path.join(dest_dir, os.path.basename(src))
    if dry_run:
        print(f"[DRY] mv {src} -> {dest}")
    else:
        shutil.move(src, dest)
    return dest

def make_backup(src_dir, backup_dir, dry_run):
    ensure_path(backup_dir, dry_run)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = os.path.join(backup_dir, f"desktop_backup_{ts}.zip")
    if dry_run:
        print(f"[DRY] zip {backup_path} <- {src_dir}")
        return backup_path

    with zipfile.ZipFile(backup_path, 'w', compression=zipfile.ZIP_DEFLATED) as zf:
        for root, _, files in os.walk(src_dir):
            for f in files:
                full = os.path.join(root, f)
                rel = os.path.relpath(full, src_dir)
                zf.write(full, rel)
    return backup_path

def write_index(index_path, entries, dry_run):
    if dry_run:
        print(f"[DRY] write index to {index_path} (entries: {len(entries)})")
    else:
        with open(index_path, 'w') as f:
            json.dump(entries, f, indent=2)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--source', required=True, help='Source folder to organize')
    ap.add_argument('--backup', required=True, help='Backup folder')
    ap.add_argument('--dry-run', action='store_true', help='Show actions but do not modify')
    args = ap.parse_args()

    src = os.path.abspath(args.source)
    backup = os.path.abspath(args.backup)
    dry = args.dry_run

    files = collect_files(src)
    index = []

    for f in files:
        ext = Path(f).suffix
        folder = ext_to_folder(ext)
        dest_dir = os.path.join(src, folder)

        dest = move_file(f, dest_dir, dry)
        entry = {
            'original': f,
            'moved_to': dest,
            'folder': folder,
            'moved_at': datetime.now().isoformat()
        }
        index.append(entry)

    index_path = os.path.join(src, 'organize_index.json')
    write_index(index_path, index, dry)

    backup_path = make_backup(src, backup, dry)

    print("\nDone.")
    if not dry:
        print(f"Index file created: {index_path}")
        print(f"Backup created at: {backup_path}")

if __name__ == '__main__':
    main()
