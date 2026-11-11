"""Validate declared decision data, never user intent or causal truth. Python 3.9+."""
import argparse
import itertools
import json
from pathlib import Path


class Invalid(ValueError):
    def __init__(self, code, path, message):
        self.issue = dict(code=code, path=path, message=message)


def require(ok, code, path, message):
    if not ok:
        raise Invalid(code, path, message)


def obj(value, path, required, optional=()):
    require(isinstance(value, dict), 'type', path, 'Expected object')
    require(set(required) <= value.keys(), 'missing_field', path, 'Missing: ' + ', '.join(sorted(set(required) - value.keys())))
    require(value.keys() <= set(required) | set(optional), 'unknown_field', path, 'Unexpected fields')


def string(value, path):
    require(isinstance(value, str) and bool(value.strip()), 'type', path, 'Expected nonempty string')


def array(value, path, nonempty=True):
    require(isinstance(value, list) and (bool(value) or not nonempty), 'type', path, 'Expected array' + (' with entries' if nonempty else ''))


def strings(value, path):
    array(value, path)
    for item in value:
        string(item, path)
    require(len(set(value)) == len(value), 'duplicate', path, 'Duplicate values')


def index(items, path, required, optional=()):
    array(items, path, False)
    result = {}
    for i, item in enumerate(items):
        at = f'{path}[{i}]'
        obj(item, at, required, optional)
        string(item['id'], at + '.id')
        require(item['id'] not in result, 'duplicate', at, 'Duplicate ID')
        result[item['id']] = item
    return result


def validate(case, state=None):
    """Return first actionable structural error; semantic review always remains required."""
    report = {'mechanical': 'fail', 'semantic': 'not_evaluated', 'ui': 'not_evaluated', 'errors': []}
    try:
        obj(case, '$', ['schema_version', 'decision_id', 'revision', 'scope', 'question', 'input', 'event', 'options', 'controls', 'claims', 'cases'])
        require(type(case['schema_version']) is int and case['schema_version'] == 1, 'schema_version', '$', 'Supported schema_version is 1')
        for key in ['decision_id', 'scope', 'question', 'input', 'event']:
            string(case[key], '$.' + key)
        require(type(case['revision']) is int and case['revision'] > 0, 'revision', '$.revision', 'Expected positive integer')
        options = index(case['options'], '$.options', ['id', 'label'])
        require(bool(options), 'empty_options', '$.options', 'At least one option required')
        for option in options.values():
            string(option['label'], '$.options.label')
        controls = index(case['controls'], '$.controls', ['id', 'values', 'effects'])
        for control in controls.values():
            at = '$.controls.' + control['id']
            strings(control['values'], at + '.values')
            require(isinstance(control['effects'], dict) and bool(control['effects']), 'type', at + '.effects', 'Expected option ID to affected fields map')
            for option_id, fields in control['effects'].items():
                require(option_id in options, 'reference', at, 'Unknown applicable option')
                strings(fields, at + '.effects.' + option_id)
        claims = index(case['claims'], '$.claims', ['id', 'text', 'kind'], ['source', 'run', 'input', 'environment', 'limitations'])
        for claim in claims.values():
            at = '$.claims.' + claim['id']
            string(claim['text'], at + '.text')
            require(isinstance(claim['kind'], str) and claim['kind'] in ['observed', 'inferred', 'illustrative', 'unknown'], 'evidence_kind', at, 'Unsupported evidence kind')
            for key in set(claim) - {'id', 'text', 'kind'}:
                string(claim[key], at + '.' + key)
            needed = {'observed': ['source', 'run', 'input', 'environment'], 'inferred': ['source'], 'unknown': ['limitations']}.get(claim['kind'], [])
            require(all(key in claim for key in needed), 'evidence_metadata', at, 'Required evidence metadata: ' + ', '.join(needed))
        rows = index(case['cases'], '$.cases', ['id', 'option_id', 'when', 'results', 'claim_ids'])
        seen = set()
        by_option = {key: [] for key in options}
        for row in rows.values():
            at = '$.cases.' + row['id']
            string(row['option_id'], at + '.option_id')
            require(row['option_id'] in options, 'reference', at, 'Unknown option')
            active = {key: control for key, control in controls.items() if row['option_id'] in control['effects']}
            require(isinstance(row['when'], dict) and row['when'].keys() == active.keys(), 'condition_keys', at, 'Use exactly the applicable controls')
            for key, value in row['when'].items():
                require(isinstance(value, str) and value in active[key]['values'], 'condition_value', at, 'Invalid condition value')
            require(isinstance(row['results'], dict) and bool(row['results']), 'type', at + '.results', 'Expected nonempty result fields')
            for key, value in row['results'].items():
                string(key, at + '.results'); string(value, at + '.results.' + key)
            strings(row['claim_ids'], at + '.claim_ids')
            require(set(row['claim_ids']) <= claims.keys(), 'reference', at, 'Unknown claim ID')
            signature = (row['option_id'], tuple(sorted(row['when'].items())))
            require(signature not in seen, 'duplicate_case', at, 'Duplicate condition combination')
            seen.add(signature)
            by_option[row['option_id']].append(row)
        count = 0
        for option_id, option_rows in by_option.items():
            active = {key: c for key, c in controls.items() if option_id in c['effects']}
            size = 1
            for control in active.values():
                size *= len(control['values'])
            count += size
            require(count <= 1000, 'coverage_limit', '$.controls', 'More than 1000 combinations: split the case; no exhaustive pass claimed')
            for values in itertools.product(*(c['values'] for c in active.values())):
                signature = (option_id, tuple(sorted(zip(active, values))))
                require(signature in seen, 'coverage', '$.cases', 'Missing declared combination: ' + str(signature))
            field_sets = [set(row['results']) for row in option_rows]
            require(all(fields == field_sets[0] for fields in field_sets), 'result_fields', '$.cases', 'Result fields must be stable within each option')
            for key, control in active.items():
                fields = control['effects'][option_id]
                require(set(fields) <= field_sets[0], 'reference', '$.controls.' + key, 'Affected result field missing')
                # Compare conditions with all other inputs held fixed. Cosmetic text
                # differences can still pass; the agent must review significance.
                for value in control['values']:
                    changed = any(a['when'][key] == value and b['when'][key] != value
                                  and all(a['when'][other] == b['when'][other] for other in active if other != key)
                                  and any(a['results'][field] != b['results'][field] for field in fields)
                                  for a in option_rows for b in option_rows)
                    require(changed, 'ineffective_control', '$.controls.' + key, 'Value has no declared result effect; remove/merge invariant control, never invent effects')
        if state is not None:
            validate_state(state, case, options, controls)
        report.update(mechanical='pass', combinations=count)
    except Invalid as exc:
        report['errors'].append(exc.issue)
    return report


def validate_state(state, case, options, controls):
    obj(state, '$state', ['decision_id', 'revision', 'scope', 'status', 'preview_option_id', 'selected_option_id', 'response', 'conditions'], ['application_evidence'])
    for key in ['decision_id', 'revision', 'scope']:
        require(type(state[key]) is type(case[key]) and state[key] == case[key], 'stale_state', '$state.' + key, 'State does not match current case; preserve historical record separately')
    require(isinstance(state['status'], str) and state['status'] in ['exploring', 'decided', 'applied', 'needs-review'], 'status', '$state.status', 'Invalid status')
    for key in ['preview_option_id', 'selected_option_id']:
        value = state[key]
        require(value is None or isinstance(value, str) and value in options, 'reference', '$state.' + key, 'Unknown option')
    require(isinstance(state['conditions'], dict), 'type', '$state.conditions', 'Expected per-option saved conditions')
    for option_id, values in state['conditions'].items():
        require(option_id in options and isinstance(values, dict), 'reference', '$state.conditions', 'Invalid option state')
        for key, value in values.items():
            require(key in controls and option_id in controls[key]['effects'], 'condition_keys', '$state.conditions', 'Irrelevant saved condition')
            require(isinstance(value, str) and value in controls[key]['values'], 'condition_value', '$state.conditions', 'Invalid saved value')
    if state['status'] == 'exploring':
        require(state['selected_option_id'] is None and state['response'] is None, 'preview_commit', '$state', 'Exploration cannot contain a decision')
    if state['status'] in ['decided', 'applied']:
        require(state['selected_option_id'] is not None and state['response'] is not None, 'missing_response', '$state', 'Decision requires selected option and response record')
    if state['response'] is not None:
        response = state['response']
        obj(response, '$state.response', ['kind', 'text', 'source_ref', 'decision_id', 'revision', 'scope'])
        require(response['kind'] == 'explicit', 'response_kind', '$state.response', 'Preview/default/timeout is not a decision response')
        for key in ['text', 'source_ref']:
            string(response[key], '$state.response.' + key)
        for key in ['decision_id', 'revision', 'scope']:
            require(type(response[key]) is type(case[key]) and response[key] == case[key], 'stale_response', '$state.response', 'Response bound to another case')
    if state['status'] == 'applied':
        require('application_evidence' in state, 'application_evidence', '$state', 'Verified work reference required')
    if 'application_evidence' in state:
        require(state['status'] == 'applied', 'application_evidence', '$state', 'Application evidence only belongs to applied state')
        string(state['application_evidence'], '$state.application_evidence')


def read_json(path):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError('Duplicate JSON key: ' + key)
            result[key] = value
        return result
    return json.loads(Path(path).read_text(encoding='utf-8-sig'), object_pairs_hook=unique,
                      parse_constant=lambda value: (_ for _ in ()).throw(ValueError('Non-JSON constant: ' + value)))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('case'); parser.add_argument('--state'); parser.add_argument('--report')
    args = parser.parse_args()
    try:
        result = validate(read_json(args.case), read_json(args.state) if args.state else None)
    except (OSError, ValueError) as exc:
        result = dict(mechanical='fail', semantic='not_evaluated', ui='not_evaluated', errors=[dict(code='input', path='$', message=str(exc))])
    output = json.dumps(result, ensure_ascii=False, indent=2) + '\n'
    if args.report:
        Path(args.report).write_text(output, encoding='utf-8')
    print(output, end='')
    return 0 if result['mechanical'] == 'pass' else 1


if __name__ == '__main__':
    raise SystemExit(main())
