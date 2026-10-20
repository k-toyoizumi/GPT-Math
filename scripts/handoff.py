"""Record a task attempt atomically; identical input/result is not new progress."""
import argparse
import hashlib
import json
from pathlib import Path
import os

CATEGORIES = {'success', 'not_executed', 'inventory_failed', 'dependency_failed', 'lean_failed',
              'python_failed', 'artifact_failed', 'publication_blocked', 'stale_evidence'}
def record(state, task, source, result, status, next_action):
    if status not in CATEGORIES or not next_action: raise ValueError('invalid handoff')
    key = hashlib.sha256(json.dumps([task, source, result], separators=(',', ':')).encode()).hexdigest()
    lock = state.with_suffix('.lock')
    fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    try:
        previous = json.loads(state.read_text()) if state.exists() else {'seen': [], 'attempts': 0, 'progress_count': 0}
        duplicate = key in previous['seen']
        row = dict(previous, task_id=task, source_sha=source, result_hash=result, status=status,
                   next_action=next_action, duplicate=duplicate, attempts=previous['attempts']+1,
                   progress_count=previous['progress_count']+(not duplicate),
                   seen=previous['seen'] if duplicate else previous['seen']+[key])
        tmp = state.with_suffix('.tmp')
        tmp.write_text(json.dumps(row, indent=2)+'\n')
        tmp.replace(state)
        return row
    finally:
        os.close(fd)
        lock.unlink()
if __name__ == '__main__':
    p = argparse.ArgumentParser()
    for name in ('state','task','source','result','status','next'): p.add_argument('--'+name, required=True)
    a = p.parse_args()
    print(json.dumps(record(Path(a.state), a.task, a.source, a.result, a.status, getattr(a, 'next'))))
