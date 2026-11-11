"""Dependency-free contract regressions, including declared limits of validation."""
import argparse
from copy import deepcopy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('contract', ROOT / 'scripts/validate_case.py')
contract = importlib.util.module_from_spec(spec)
spec.loader.exec_module(contract)
BASE = contract.read_json(ROOT / 'evals/fixtures/memory-case.json')
STATE = contract.read_json(ROOT / 'evals/fixtures/memory-state.json')
results = []


def check(name, edit=lambda c, s: None, expected=None):
    case, state = deepcopy(BASE), deepcopy(STATE)
    try:
        edit(case, state)
        report = contract.validate(case, state)
        assert report['semantic'] == report['ui'] == 'not_evaluated'
        if expected:
            assert report['mechanical'] == 'fail' and report['errors'][0]['code'] == expected, report
        else:
            assert report['mechanical'] == 'pass', report
        results.append(dict(name=name, status='pass'))
    except Exception as exc:
        results.append(dict(name=name, status='fail', error=str(exc)))


def decided(c, s):
    s.update(status='decided', selected_option_id='retry', response=dict(kind='explicit',text='B로 진행해',source_ref='chat:example',decision_id=c['decision_id'],revision=c['revision'],scope=c['scope']))


check('six declared cases and isolated preview state')
check('explicit decision snapshot', decided)
def applied(c,s):
    decided(c,s);s.update(status='applied',application_evidence='test:example-run')
check('applied snapshot with reference',applied)
check('duplicate option',lambda c,s:c['options'].append(c['options'][0]),'duplicate')
check('misspelled top-level field',lambda c,s:c.update(revison=1),'unknown_field')
check('boolean is not revision',lambda c,s:c.update(revision=True),'revision')
check('unknown schema version',lambda c,s:c.update(schema_version=2),'schema_version')
check('invalid container type',lambda c,s:c.update(options={}), 'type')
check('missing combination',lambda c,s:c['cases'].pop(), 'coverage')
check('duplicate combination',lambda c,s:c['cases'].append(dict(c['cases'][0],id='copy')), 'duplicate_case')
check('foreign option reference',lambda c,s:c['controls'][0]['effects'].update(foreign=['outcome']), 'reference')
check('irrelevant condition on retry',lambda c,s:c['cases'][3]['when'].update(user_knowledge='forgotten'), 'condition_keys')
check('invalid declared condition value',lambda c,s:c['cases'][3]['when'].update(retry_result='magic'), 'condition_value')
check('missing affected field',lambda c,s:c['controls'][0]['effects'].update(ask=['missing']), 'reference')
check('unknown claim reference',lambda c,s:c['cases'][0].update(claim_ids=['missing']), 'reference')
check('observed needs run metadata',lambda c,s:c['claims'][0].update(kind='observed'), 'evidence_metadata')
check('inferred needs source',lambda c,s:c['claims'][0].update(kind='inferred'), 'evidence_metadata')
check('unknown needs limitation',lambda c,s:c['claims'][0].update(kind='unknown',limitations=''), 'type')
check('stable result fields',lambda c,s:c['cases'][0]['results'].update(extra='x'), 'result_fields')
def frozen(c,s):
    for row in c['cases'][3:]: row['results'] = dict(outcome='same',next='same')
check('frozen affected results',frozen,'ineffective_control')
check('foreign state',lambda c,s:s.update(decision_id='another'),'stale_state')
check('old revision state',lambda c,s:s.update(revision=0),'stale_state')
check('scope mismatch state',lambda c,s:s.update(scope='write operation'),'stale_state')
check('invalid saved condition',lambda c,s:s['conditions']['retry'].update(retry_result='magic'),'condition_value')
check('cross-option saved condition',lambda c,s:s['conditions']['retry'].update(user_knowledge='forgotten'),'condition_keys')
check('preview cannot commit',lambda c,s:s.update(selected_option_id='retry'),'preview_commit')
check('decision requires response',lambda c,s:s.update(status='decided',selected_option_id='retry'),'missing_response')
def bad_response(c,s):
    decided(c,s);s['response']['kind']='preview'
check('preview event cannot be response',bad_response,'response_kind')
def stale_response(c,s):
    decided(c,s);s['response']['revision']=2
check('response binds current revision',stale_response,'stale_response')
def unverified_application(c,s):
    decided(c,s);s['status']='applied'
check('application requires evidence reference',unverified_application,'application_evidence')
check('exploring cannot contain application claim',lambda c,s:s.update(application_evidence='fake'),'application_evidence')
check('oversized combination set rejected',lambda c,s:c['controls'][0].update(values=[str(i) for i in range(1001)]), 'condition_value')
# Reach the coverage guard with otherwise valid rows.
def large(c,s):
    c['controls'][0]['values'] += [str(i) for i in range(1001)]
check('coverage limit never silently samples',large,'coverage_limit')
def shared(c,s):
    c['controls'].append(dict(id='auth',values=['valid','expired'],effects={'ask':['outcome'],'retry':['outcome']}))
    original=c['cases'];c['cases']=[]
    for row in original:
        for value in ['valid','expired']:
            clone=deepcopy(row);clone['id']+='-'+value;clone['when']['auth']=value
            if value=='expired': clone['results']=dict(outcome='authorization required',next='renew authorization')
            c['cases'].append(clone)
check('shared control and contextual equal outcomes allowed',shared)
def semantic_gap(c,s):
    c['cases'][3]['results']['outcome']='Blue button causes lookup success'
    c['claims'][3]['text']='Blue button causes lookup success'
check('unsupported causal claim stays outside mechanical judgment',semantic_gap)
def consent_gap(c,s):
    decided(c,s);s['response']['text']='B가 어떻게 작동하는지 보여줘'
check('explicit metadata does not prove natural-language consent',consent_gap)
def cosmetic(c,s):
    for i,row in enumerate(c['cases'][3:]):
        row['results']=dict(outcome='same' + ' ' * i,next='same')
check('cosmetic result differences require semantic review',cosmetic)
def unsupported_observation(c,s):
    c['claims'][0].update(kind='observed',source='unverified:reference',run='unverified:run',input='claimed input',environment='claimed environment')
check('evidence metadata presence does not verify source',unsupported_observation)

# Adversarial shapes should produce structured validation errors, not crashes.
for field in BASE:
    check('reject null field: '+field,lambda c,s,key=field:c.update({key:None}),
          'schema_version' if field=='schema_version' else 'revision' if field=='revision' else 'type')

with tempfile.TemporaryDirectory() as tmp:
    for name, content in [('malformed','{'),('duplicate key','{"a":1,"a":2}'),('non-JSON constant','{"a":NaN}')]:
        try:
            path=Path(tmp)/'invalid.json';path.write_text(content,encoding='utf-8')
            proc=subprocess.run([sys.executable,'-X','utf8',str(ROOT/'scripts/validate_case.py'),str(path)],capture_output=True,text=True,encoding='utf-8')
            assert proc.returncode==1 and json.loads(proc.stdout)['errors'][0]['code']=='input',proc.stdout
            results.append(dict(name='CLI rejects '+name,status='pass'))
        except Exception as exc: results.append(dict(name='CLI rejects '+name,status='fail',error=str(exc)))
    try:
        report_path=Path(tmp)/'report.json'
        proc=subprocess.run([sys.executable,'-X','utf8',str(ROOT/'scripts/validate_case.py'),str(ROOT/'evals/fixtures/memory-case.json'),'--state',str(ROOT/'evals/fixtures/memory-state.json'),'--report',str(report_path)],capture_output=True,text=True,encoding='utf-8')
        assert proc.returncode==0 and json.loads(report_path.read_text(encoding='utf-8'))['combinations']==6
        results.append(dict(name='CLI writes pass report and exits zero',status='pass'))
    except Exception as exc: results.append(dict(name='CLI writes pass report and exits zero',status='fail',error=str(exc)))

parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--report');args=parser.parse_args()
report=dict(scope='Declared contract and CLI regressions; not semantic or browser evaluation',
            summary=dict(passed=sum(r['status']=='pass' for r in results),failed=sum(r['status']=='fail' for r in results)),results=results,
            semantic_generation_evals=dict(defined=len(contract.read_json(ROOT/'evals/evals.json')['evals']),executed=0))
output=json.dumps(report,ensure_ascii=False,indent=2)+'\n'
if args.report: Path(args.report).write_text(output,encoding='utf-8')
print(output,end='');sys.exit(bool(report['summary']['failed']))
