"""Produce failure metadata even if setup/dependency resolution failed before runner."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
root=Path('evidence')
root.mkdir(exist_ok=True)
p=root/'run.json'
if not p.exists():
    p.write_text(json.dumps(dict(source_sha=os.getenv('GITHUB_SHA'),
        tree_sha=subprocess.check_output(['git','rev-parse','HEAD^{tree}'],text=True).strip(),
        run_id=os.getenv('GITHUB_RUN_ID'),attempt=os.getenv('GITHUB_RUN_ATTEMPT'),
        event=os.getenv('GITHUB_EVENT_NAME'),status='not_executed',
        failure='setup_or_dependency_failed', steps=[]),indent=2)+'\n')
(root/'SHA256SUMS').write_text(''.join(f'{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.name}\n' for p in sorted(root.iterdir()) if p.is_file() and p.name!='SHA256SUMS'))
