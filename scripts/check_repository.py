#!/usr/bin/env python3
"""Static release checks only. Never import or execute reference/hardware code."""
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
DENIED_SUFFIX={'.mcap','.db3','.mp4','.mov','.pt','.pth','.safetensors','.so','.pem','.key','.deb','.npz'}
PATTERNS={
    'GitHub credential':r'\b(?:gh[pousr]_[A-Za-z0-9]{25,}|github_pat_[A-Za-z0-9_]{25,})',
    'private key':r'-----BEGIN (?:OPENSSH |RSA |EC )?PRIVATE KEY-----',
    'private network IPv4':r'\b(?:10(?:\.\d{1,3}){3}|192\.168(?:\.\d{1,3}){2}|172\.(?:1[6-9]|2\d|3[01])(?:\.\d{1,3}){2})\b',
    'personal home':r'/home/(?!robot(?:/|\b)|user(?:/|\b)|YOUR_USER(?:/|\b))[A-Za-z0-9_-]+/',
}


def check():
    issues=[]; count=0
    for p in ROOT.rglob('*'):
        rel=p.relative_to(ROOT)
        if set(rel.parts)&{'.git','runtime','local','__pycache__'}:continue
        if p.is_symlink():issues.append(f'{rel}: symlink is not an export input');continue
        if not p.is_file():continue
        if p.name.endswith('.local.json'):continue
        count+=1
        if p.suffix in DENIED_SUFFIX:issues.append(f'{rel}: binary/private artifact')
        if p.stat().st_size>2_000_000:issues.append(f'{rel}: oversized export')
        try:text=p.read_text()
        except UnicodeDecodeError:issues.append(f'{rel}: unexpected binary');continue
        for name,pat in PATTERNS.items():
            if re.search(pat,text):issues.append(f'{rel}: {name}')
        if p.name.endswith(('.py','.py.in')):
            try:ast.parse(text,filename=str(rel))
            except SyntaxError as exc:issues.append(f'{rel}: Python syntax {exc}')
        if p.name.endswith(('.sh','.sbatch','.sh.in','.sbatch.in')) or p.name=='ros_shell.rc.in':
            result=subprocess.run(['bash','-n',str(p)],capture_output=True,text=True)
            if result.returncode:issues.append(f'{rel}: shell syntax: {result.stderr.strip()}')
        if p.suffix=='.md':
            for target in re.findall(r'\]\(([^)]+)\)',text):
                if '://' in target or target.startswith(('#','mailto:')):continue
                target=target.split('#')[0]
                if target and not (p.parent/target).exists():issues.append(f'{rel}: broken link {target}')
    manifest=json.loads((ROOT/'provenance/source-manifest.json').read_text())
    for row in manifest['files']:
        path=ROOT/row['path']
        if not path.exists() or hashlib.sha256(path.read_bytes()).hexdigest()!=row['exported_sha256']:
            issues.append('Source manifest mismatch: '+row['path'])
    return count,issues


if __name__=='__main__':
    count,issues=check()
    for issue in issues:print(issue,file=sys.stderr)
    print(json.dumps(dict(files_checked=count,issues=len(issues),hardware_started=False)))
    sys.exit(bool(issues))
