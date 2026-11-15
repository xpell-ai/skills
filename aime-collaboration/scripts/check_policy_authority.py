#!/usr/bin/env python3
"""Offline evidence checker. No connectors, authority changes or write authorization."""
import hashlib
import json
import re
import sys


def check(value):
    try:
        r, a, p = value['record'], value['approval'], value['policy']
        s = r['source']
        if value['schema'] != 1 or r['phase'] not in ('before', 'after'):
            raise ValueError('unsupported schema or unresolved transition')
        if not all(isinstance(r[k], str) and r[k] for k in ('id', 'revision', 'approval_ref')):
            raise ValueError('missing record identity')
        if value['observed_record_revision'] != r['revision']:
            raise ValueError('stale authority observation')
        if a['verified'] is not True or a['current'] is not True or a['ref'] != r['approval_ref'] or a['record_id'] != r['id']:
            raise ValueError('unverified or conflicting approval')
        kind = 'document' if r['phase'] == 'before' else 'git'
        if s['kind'] != kind or p['kind'] != kind:
            raise ValueError('wrong source system; no fallback')
        for key in ('id', 'revision', 'version'):
            if not isinstance(s[key], str) or not s[key] or p[key] != s[key]:
                raise ValueError('wrong or stale source ' + key)
        if kind == 'git' and not re.fullmatch('[0-9a-f]{40}', s['revision']):
            raise ValueError('Git authority must pin a commit')
        if p['accessible'] is not True or p['complete'] is not True or not isinstance(p['text'], str) or not p['text']:
            raise ValueError('inaccessible or incomplete full policy')
        if not re.fullmatch('[0-9a-f]{64}', s['sha256']) or hashlib.sha256(p['text'].encode()).hexdigest() != s['sha256']:
            raise ValueError('changed policy content')
        if not isinstance(value['pointers'], list):
            raise ValueError('missing pointer inventory')
        for ptr in value['pointers']:
            if ptr['role'] == 'normative' and ptr['source_id'] != s['id'] and ptr.get('superseded_by') != r['id']:
                raise ValueError('conflicting active pointer')
            if ptr['role'] not in ('normative', 'historical', 'candidate'):
                raise ValueError('unclassified pointer')
        return {'action': 'read_full_policy', 'source_id': s['id'], 'revision': s['revision'],
                'policy_version': s['version'], 'selective_loading': False, 'mutations_authorized': False}
    except (KeyError, TypeError, ValueError) as error:
        return {'action': 'block_dependent_work', 'reason': str(error),
                'selective_loading': False, 'mutations_authorized': False}


if __name__ == '__main__':
    try:
        with open(sys.argv[1]) as stream:
            result = check(json.load(stream))
    except (OSError, ValueError, IndexError) as error:
        result = {'action': 'block_dependent_work', 'reason': str(error),
                  'selective_loading': False, 'mutations_authorized': False}
    print(json.dumps(result, sort_keys=True))
    sys.exit(0 if result['action'] == 'read_full_policy' else 1)
