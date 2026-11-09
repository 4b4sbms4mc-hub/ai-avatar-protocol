"""Offline structural validation. Does not authenticate any identity or proof."""
from pathlib import Path
import argparse,json
import rfc3339_validator  # Required: fail closed instead of silently skipping date-time formats.
from jsonschema import Draft202012Validator,FormatChecker
from referencing import Registry,Resource
ROOT=Path(__file__).resolve().parents[1]
def load(p):return json.loads((ROOT/p).read_text(encoding='utf-8'))
def make_registry():
    registry=Registry()
    ids={}
    for base in ['schemas','upstream']:
        for p in sorted((ROOT/base).rglob('*.schema.json')):
            s=json.loads(p.read_text(encoding='utf-8'))
            Draft202012Validator.check_schema(s)
            uri=s['$id']
            if uri in ids and ids[uri]!=s:raise ValueError('Conflicting schema ID: '+uri)
            ids[uri]=s
            registry=registry.with_resource(uri,Resource.from_contents(s))
    return registry,len(ids)
REGISTRY,SCHEMA_COUNT=make_registry()
def errors(schema,data):
    return sorted(Draft202012Validator(load(schema),registry=REGISTRY,format_checker=FormatChecker()).iter_errors(data),key=lambda e:str(list(e.path)))
def check(schema,data):
    e=errors(schema,data)
    if e:raise ValueError('; '.join(str(list(x.path))+': '+x.message for x in e))
def examples():
    result=[]
    for item in load('examples/INDEX.json'):
        check(item['schema'],load(item['file']))
        result.append({'file':item['file'],'status':'passed'})
    return result
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--schema');ap.add_argument('--input');a=ap.parse_args()
    if bool(a.schema)!=bool(a.input):ap.error('--schema and --input must be supplied together')
    if a.schema:check(a.schema,load(a.input));print('Structure valid; authorization not evaluated.')
    else:print(json.dumps({'registered_schemas':SCHEMA_COUNT,'examples':examples(),'network_schema_fetch':False},ensure_ascii=False,indent=2))
