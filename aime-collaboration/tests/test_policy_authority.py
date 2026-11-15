import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'scripts/check_policy_authority.py'
spec = importlib.util.spec_from_file_location('authority', SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def fixture(phase):
    source = {'kind': 'document' if phase == 'before' else 'git',
              'id': 'document-A' if phase == 'before' else 'repository-B/policy',
              'revision': 'native-1' if phase == 'before' else 'a' * 40,
              'version': 'test-1', 'sha256': hashlib.sha256(b'Synthetic complete policy.').hexdigest()}
    return {'schema': 1, 'record': {'id': 'decision-A', 'revision': 'record-1', 'phase': phase,
                                   'approval_ref': 'approval-A', 'source': source},
            'observed_record_revision': 'record-1',
            'approval': {'verified': True, 'current': True, 'ref': 'approval-A', 'record_id': 'decision-A'},
            'policy': source | {'text': 'Synthetic complete policy.', 'complete': True, 'accessible': True},
            'pointers': [{'role': 'normative', 'source_id': source['id']}]}


class AuthorityTests(unittest.TestCase):
    def test_both_phases_full_read_only(self):
        for phase in ('before', 'after'):
            with self.subTest(phase=phase):
                value = fixture(phase)
                result = module.check(value)
                self.assertEqual(result['action'], 'read_full_policy')
                self.assertEqual(result['source_id'], value['record']['source']['id'])
                self.assertFalse(result['selective_loading'])
                self.assertFalse(result['mutations_authorized'])

    def test_failures_never_select_another_source(self):
        cases = []
        for phase in ('before', 'after'):
            for key, bad in [('id', 'wrong'), ('revision', 'old'), ('version', 'old'),
                             ('kind', 'git' if phase == 'before' else 'document'),
                             ('accessible', False), ('complete', False), ('text', 'Changed policy.')]:
                value = fixture(phase); value['policy'][key] = bad; cases.append(value)
        for field in ('verified', 'current'):
            value = fixture('after'); value['approval'][field] = False; cases.append(value)
        value = fixture('after'); value['observed_record_revision'] = 'stale'; cases.append(value)
        value = fixture('after'); value['record']['phase'] = 'transition'; cases.append(value)
        value = fixture('after'); value['record']['source']['revision'] = value['policy']['revision'] = 'main'; cases.append(value)
        value = fixture('after'); value['pointers'].append({'role': 'normative', 'source_id': 'document-A'}); cases.append(value)
        value = fixture('after'); del value['record']; cases.append(value)
        value = fixture('after'); value['approval']['record_id'] = 'other-decision'; cases.append(value)
        for number, value in enumerate(cases):
            with self.subTest(case=number):
                result = module.check(value)
                self.assertEqual(result['action'], 'block_dependent_work')
                self.assertNotIn('source_id', result)
                self.assertFalse(result['mutations_authorized'])

    def test_cutover_explicitly_supersedes_legacy_link(self):
        value = fixture('after')
        value['pointers'].append({'role': 'normative', 'source_id': 'document-A', 'superseded_by': 'decision-A'})
        self.assertEqual(module.check(value)['source_id'], 'repository-B/policy')
        value['pointers'][-1]['superseded_by'] = 'unverified-other-decision'
        self.assertEqual(module.check(value)['action'], 'block_dependent_work')

    def test_fresh_process_source_selection_smoke_is_offline(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'fixture.json'
            for phase in ('before', 'after'):
                path.write_text(json.dumps(fixture(phase)))
                run = subprocess.run([sys.executable, '-B', str(SCRIPT), str(path)], capture_output=True, text=True)
                self.assertEqual(run.returncode, 0)
                self.assertEqual(json.loads(run.stdout)['source_id'], fixture(phase)['record']['source']['id'])
            value = fixture('after'); value['policy']['accessible'] = False
            path.write_text(json.dumps(value))
            run = subprocess.run([sys.executable, '-B', str(SCRIPT), str(path)], capture_output=True, text=True)
            self.assertEqual(run.returncode, 1)
            self.assertEqual(json.loads(run.stdout)['action'], 'block_dependent_work')


if __name__ == '__main__':
    unittest.main()
