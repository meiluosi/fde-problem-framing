"""Build, verify and install an entire skill using a SHA-256 manifest.
Hashes detect missing/corrupted files, not publisher authenticity.
"""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import shutil
import tempfile
import uuid
import zipfile

EXCLUDED = {'.git', '__pycache__', '.DS_Store'}
REQUIRED = {'SKILL.md', 'README.md', 'VERSION', 'references/decision.md',
            'references/dialogue.md', 'templates/problem-card.md',
            'agents/openai.yaml', 'scripts/package.py'}

def inventory(root):
    result = {}
    for path in sorted(root.rglob('*')):
        rel = path.relative_to(root)
        if any(part in EXCLUDED for part in rel.parts):
            continue
        if path.is_symlink():
            raise ValueError('Symlink not allowed: ' + str(rel))
        if path.is_file() and str(rel) != 'MANIFEST.json':
            result[rel.as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
    return result

def safe_name(name):
    path = PurePosixPath(name)
    return (bool(name) and not path.is_absolute() and '\\' not in name
            and ':' not in name and all(p not in ('', '.', '..') for p in name.split('/'))
            and name != 'MANIFEST.json' and not any(p in EXCLUDED for p in path.parts))

def verify(root):
    root = Path(root)
    if root.is_symlink() or (root / 'MANIFEST.json').is_symlink():
        raise ValueError('Root/manifest symlink not allowed')
    manifest = json.loads((root / 'MANIFEST.json').read_text())
    if not isinstance(manifest, dict) or not manifest:
        raise ValueError('Manifest must be a nonempty mapping')
    for name, digest in manifest.items():
        if not safe_name(name) or not isinstance(digest, str) or len(digest) != 64 or any(c not in '0123456789abcdef' for c in digest):
            raise ValueError('Invalid manifest entry: ' + name)
    if not REQUIRED.issubset(manifest):
        raise ValueError('Required skill resources missing')
    actual = inventory(root)
    if actual != manifest:
        missing = sorted(set(manifest) - set(actual))
        extra = sorted(set(actual) - set(manifest))
        changed = sorted(k for k in actual.keys() & manifest.keys() if actual[k] != manifest[k])
        raise ValueError(f'Integrity mismatch: missing={missing}, extra={extra}, changed={changed}')
    return manifest

def build(root, output):
    root, output = Path(root).resolve(), Path(output).resolve()
    if output == root or root in output.parents:
        raise ValueError('Release must be outside source directory')
    rows = inventory(root)
    if not REQUIRED.issubset(rows):
        raise ValueError('Required skill resources missing')
    (root / 'MANIFEST.json').write_text(json.dumps(rows, ensure_ascii=False, indent=2) + '\n')
    verify(root)
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, 'w', zipfile.ZIP_DEFLATED) as archive:
        for name in sorted(list(rows) + ['MANIFEST.json']):
            info = zipfile.ZipInfo('fde-problem-framing/' + name, (2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, (root / name).read_bytes())
    return output

def install(root, dest, update=False, backup_dir=None):
    root, dest = Path(root).resolve(), Path(dest).absolute()
    rows = verify(root)
    if dest.is_symlink():
        raise ValueError('Destination symlink not allowed')
    resolved_dest = dest.resolve()
    if resolved_dest == root or root in resolved_dest.parents or resolved_dest in root.parents:
        raise ValueError('Source and destination must not overlap')
    if dest.exists():
        if not update:
            raise ValueError('Destination exists; use --update after checking local changes')
        if backup_dir is None:
            raise ValueError('Update requires --backup-dir outside the skill discovery directory')
        backup_dir = Path(backup_dir).resolve()
        if backup_dir == dest.parent.resolve() or dest.parent.resolve() in backup_dir.parents or backup_dir == root or root in backup_dir.parents:
            raise ValueError('Backup directory must be outside source and skill discovery directory')
        # Permit pre-v0.3 packages while still protecting every existing managed file.
        old = json.loads((dest / 'MANIFEST.json').read_text())
        if not isinstance(old, dict) or any(not safe_name(n) for n in old) or inventory(dest) != old:
            raise ValueError('Existing install changed or incomplete; preserved unchanged')
    dest.parent.mkdir(parents=True, exist_ok=True)
    stage = Path(tempfile.mkdtemp(prefix='.fde-stage-', dir=dest.parent))
    backup = None
    try:
        for name in list(rows) + ['MANIFEST.json']:
            out = stage / name
            out.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(root / name, out)
        verify(stage)
        if dest.exists():
            backup_dir.mkdir(parents=True, exist_ok=True)
            backup = backup_dir / (dest.name + '.backup-' + uuid.uuid4().hex[:8])
            dest.rename(backup)
        try:
            stage.rename(dest)
        except Exception:
            if backup is not None:
                backup.rename(dest)
            raise
    finally:
        if stage.exists():
            shutil.rmtree(stage)
    return backup

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['build', 'verify', 'install'])
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--output', type=Path)
    parser.add_argument('--dest', type=Path)
    parser.add_argument('--update', action='store_true')
    parser.add_argument('--backup-dir', type=Path)
    args = parser.parse_args()
    try:
        if args.command == 'build':
            if not args.output: parser.error('build requires --output')
            print('Built', build(args.root, args.output))
        elif args.command == 'verify':
            print('Verified', len(verify(args.root)), 'files')
        else:
            if not args.dest: parser.error('install requires --dest')
            backup = install(args.root, args.dest, args.update, args.backup_dir)
            print('Installed', args.dest)
            if backup: print('Previous install preserved at', backup)
    except (ValueError, OSError, json.JSONDecodeError) as error:
        parser.exit(1, str(error) + '\n')

if __name__ == '__main__':
    main()
