"""Restore and verify the original assets using Python 3 standard library."""
import argparse
import hashlib
import json
import shutil
import zipfile
from pathlib import Path


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        while chunk := stream.read(8 * 1024 * 1024):
            h.update(chunk)
    return h.hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--parts-dir', type=Path, default=Path('downloads'))
    parser.add_argument('--output-dir', type=Path, default=Path('assets'))
    args = parser.parse_args()
    manifest = json.loads(Path(__file__).with_name('assets-manifest.json').read_text(encoding='utf-8'))
    archive_meta = manifest['archive']
    for part in archive_meta['parts']:
        path = args.parts_dir / part['name']
        if path.stat().st_size != part['size'] or digest(path) != part['sha256']:
            raise RuntimeError(f'Part checksum mismatch: {path}')
        print(f'Verified {path.name}', flush=True)
    archive = args.parts_dir / archive_meta['name']
    if archive.exists():
        if archive.stat().st_size != archive_meta['size'] or digest(archive) != archive_meta['sha256']:
            raise RuntimeError(f'Existing archive differs; move it aside first: {archive}')
    else:
        with archive.open('xb') as target:
            for part in archive_meta['parts']:
                with (args.parts_dir / part['name']).open('rb') as source:
                    shutil.copyfileobj(source, target, 8 * 1024 * 1024)
        if digest(archive) != archive_meta['sha256']:
            raise RuntimeError('Combined archive checksum mismatch')
    args.output_dir.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(archive) as z:
        if sorted(z.namelist()) != sorted(entry['name'] for entry in manifest['files']):
            raise RuntimeError('Unexpected archive contents')
        for entry in manifest['files']:
            name = entry['name']
            if '/' in name or '\\' in name or ':' in name or name in ('.', '..'):
                raise RuntimeError(f'Unsafe asset name: {name}')
            target = args.output_dir / name
            if target.exists():
                if target.stat().st_size == entry['size'] and digest(target) == entry['sha256']:
                    print(f'Already verified: {name}', flush=True)
                    continue
                raise RuntimeError(f'Existing file differs; move it aside first: {target}')
            temp = target.with_name(target.name + '.restoring')
            h = hashlib.sha256()
            size = 0
            with z.open(name) as source, temp.open('xb') as out:
                while chunk := source.read(8 * 1024 * 1024):
                    out.write(chunk)
                    h.update(chunk)
                    size += len(chunk)
            if size != entry['size'] or h.hexdigest() != entry['sha256']:
                raise RuntimeError(f'Asset checksum mismatch: {name}')
            temp.rename(target)
            print(f'Restored and verified: {name}', flush=True)
    print(f'Complete: {len(manifest["files"])} assets restored to {args.output_dir.resolve()}')


if __name__ == '__main__':
    main()
