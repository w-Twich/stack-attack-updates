"""Reassemble and validate a runtime-only package before publishing it."""
import base64
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import stat
import zipfile

ROOT = Path(__file__).resolve().parent


def prepare(root=ROOT):
    root = Path(root)
    metadata = json.loads((root/'release'/'StackAttack_update.json').read_text())
    bundle = json.loads((root/'release'/'bundle.json').read_text())
    version = metadata['version']
    assert re.fullmatch(r'\d{1,4}\.\d{1,4}\.\d{1,4}', version), 'Invalid version'
    name = 'StackAttack_'+version.replace('.','_')+'_update.zip'
    assert metadata['archive'] == name and metadata['format'] == 1 and metadata['bootstrap'] == 1
    assert 0 < metadata['size'] <= 100*1024*1024
    parts = bundle['parts']
    assert 0 < len(parts) < 300
    assert parts == ['parts/'+str(i).zfill(3)+'.b64' for i in range(len(parts))]
    data = b''.join(base64.b64decode((root/'release'/p).read_bytes(), validate=True) for p in parts)
    assert len(data) == metadata['size'], 'Archive size mismatch'
    assert hashlib.sha256(data).hexdigest() == metadata['sha256'], 'Archive checksum mismatch'
    output = root/'dist';output.mkdir(exist_ok=True)
    archive = output/name;archive.write_bytes(data)
    with zipfile.ZipFile(archive) as z:
        infos=z.infolist();names=set();expanded=0
        for info in infos:
            path=PurePosixPath(info.filename);name=info.filename
            assert not info.is_dir() and not path.is_absolute() and str(path)==name
            assert '\\' not in name and ':' not in name
            assert not any(p.startswith('.') for p in name.split('/'))
            assert name.casefold() not in names and not stat.S_ISLNK(info.external_attr>>16)
            names.add(name.casefold());expanded+=info.file_size
            assert info.file_size < 25*1024*1024
            assert name in ('game.py','update_manifest.json') or (name.startswith('stackattack/') and name.endswith('.py')) or (name.startswith('assets/backgrounds/') and name.endswith('.jpg')), 'Unexpected public content'
        assert len(infos) < 500 and expanded < 200*1024*1024
        manifest=json.loads(z.read('update_manifest.json'))
        assert manifest['version']==version
        assert set(manifest['files'])==set(z.namelist())-{'update_manifest.json'}
        assert {'game.py','stackattack/app.py','stackattack/updater.py','stackattack/__init__.py'} <= set(manifest['files'])
        for name,digest in manifest['files'].items():
            assert hashlib.sha256(z.read(name)).hexdigest()==digest, 'File checksum mismatch: '+name
        assert z.testzip() is None
    (output/'StackAttack_update.json').write_text(json.dumps(metadata,indent=2)+'\n')
    print('Verified Stack Attack '+version+' / '+str(len(data))+' bytes; no music or settings included.')
    return metadata


if __name__=='__main__':prepare()
