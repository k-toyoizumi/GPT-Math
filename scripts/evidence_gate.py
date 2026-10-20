"""Check completeness, checksums and run identity before artifact upload."""
import hashlib
import json
import os
from pathlib import Path
import sys

def validate(root, expected_sha, expected_run, expected_attempt):
    row = json.loads((root/'run.json').read_text())
    for field, expected in [('source_sha',expected_sha),('run_id',expected_run),('attempt',expected_attempt)]:
        if row[field] != expected: raise ValueError('stale_evidence: '+field)
    listed = {}
    for line in (root/'SHA256SUMS').read_text().splitlines():
        digest, name = line.split('  ',1)
        if Path(name).name != name or name in listed: raise ValueError('unsafe/duplicate checksum entry')
        listed[name] = digest
    actual = {p.name for p in root.iterdir() if p.is_file() and p.name != 'SHA256SUMS'}
    if set(listed) != actual: raise ValueError('artifact_failed: incomplete hash manifest')
    for name, digest in listed.items():
        if hashlib.sha256((root/name).read_bytes()).hexdigest() != digest: raise ValueError('artifact_failed: '+name)
    if row['status'] == 'success':
        required = {'run.json','proofs.json','experiments.json','coverage.json','faults.json','certificate.csv','handoff.json'}
        if not required <= actual: raise ValueError('artifact_failed: missing mandatory evidence')
        proofs=json.loads((root/'proofs.json').read_text())
        if not proofs: raise ValueError('empty proof evidence')
        for proof in proofs:
            if proof['source_sha'] != expected_sha or proof['run_id'] != expected_run or proof['attempt'] != expected_attempt:
                raise ValueError('stale_evidence: proof')
    return row['status']
if __name__ == '__main__':
    print(validate(Path('evidence'), os.environ['GITHUB_SHA'], os.environ['GITHUB_RUN_ID'], os.environ['GITHUB_RUN_ATTEMPT']))
