#!/usr/bin/env python3
"""Render a NEW local source tree. No imports, commands, network or hardware."""
import argparse
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
TOKEN = re.compile(r'\{\{([A-Z_0-9]+)\}\}')
SAFE_VALUE = re.compile(r'[A-Za-z0-9_/.:@+\-]+\Z')


def render(config, output, source=None):
    source = ROOT/'reference' if source is None else Path(source)
    output = Path(output).resolve()
    if output == source.resolve() or source.resolve() in output.parents:
        raise ValueError('Output must not be inside reference sources')
    if output.exists():
        raise FileExistsError('Output already exists; preserve it and choose a new directory')
    sources = sorted(source.rglob('*.in'))
    keys = {key for p in sources for key in TOKEN.findall(p.read_text())}
    missing = keys-set(config)
    if missing:
        raise ValueError('Missing configuration keys: '+', '.join(sorted(missing)))
    for key in keys:
        value = config[key]
        if not isinstance(value,str) or not SAFE_VALUE.fullmatch(value) or 'REPLACE_' in value:
            raise ValueError('Unsafe/unset value for '+key+'; use simple ASCII paths without spaces')
    plans=[]
    for path in sources:
        text=TOKEN.sub(lambda m:config[m[1]],path.read_text())
        if '{{' in text:
            # Source may legitimately contain literal C++/dict braces; only tokens matter.
            if TOKEN.search(text):raise ValueError('Unresolved placeholder')
        name=path.relative_to(source).as_posix()[:-3]
        plans.append((name,text))
    output.mkdir(parents=True,exist_ok=False)
    rows=[]
    for name,text in plans:
        target=output/name
        target.parent.mkdir(parents=True,exist_ok=True)
        target.write_text(text)
        rows.append(dict(path=name,sha256=hashlib.sha256(text.encode()).hexdigest()))
    (output/'MATERIALIZED.json').write_text(json.dumps(dict(
        status='CONFIGURATION_RENDERED_NOT_HARDWARE_ACCEPTED',files=rows,
        hardware_started=False,jobs_submitted=False),indent=2)+'\n')
    return rows


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--config',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    args=p.parse_args()
    rows=render(json.loads(args.config.read_text()),args.output)
    print(f'Rendered {len(rows)} files. No ROS/CAN, jobs or motion started.')


if __name__=='__main__':main()
