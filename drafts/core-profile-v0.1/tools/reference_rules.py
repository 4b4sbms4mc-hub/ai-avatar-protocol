"""Finite fixture rules for contract tests only.
No network, authentication, credential verification, persistence, membership
resolver, encryption, policy administration, or production authorization.
Inputs to access() MUST be treated as synthetic trusted test records.
"""
from datetime import datetime,timedelta
import hashlib

def time(s):return datetime.fromisoformat(s.replace('Z','+00:00'))
def critical(items):
    seen=set();found=False
    for x in items:
        if x['namespace'] in seen:return False
        seen.add(x['namespace'])
        known=(x['namespace'],x['version'])==('x-aiap-core-profile','0.1-draft')
        if x['critical'] and not known:return False
        if known and x['critical']:found=True
    return found

def bundle_unique(bundle):
    return len({x['avatar_id'] for x in bundle['cores']})==len(bundle['cores'])

def archive(record,policy,now):
    now=time(now);lc=record['lifecycle'];ret=record['retention']
    if time(record['created_at'])>now:return 'E_TIME'
    if lc['last_used_at'] and time(lc['last_used_at'])>now:return 'E_TIME'
    if record['status']!='active' or record['level'] not in ('M1','M2') or not policy['automatic_archive']:return 'keep'
    if ret['pinned'] or ret['decay_exempt'] or lc['stable_preference'] or lc['recurrence_ref'] or lc['active_task_refs']:return 'protected'
    if lc['expected_next_use'] and time(lc['expected_next_use'])<=now+timedelta(days=policy['expected_use_protection_days']):return 'protected'
    last=time(lc['last_used_at'] or record['created_at'])
    return 'archive-to-M3' if (now-last).total_seconds()>=policy['archive_after_days'][record['level']]*86400 else 'keep'

def access(record,request,policy,now,*,revoked=False,deleted=False):
    """Exact fixture decisions; assumes request/policy identity already trusted.
    All shared memberships are unsupported and denied. Production must also
    resolve consent, parent scopes, derived sources, processors and revocation.
    """
    if revoked or deleted or record['status'] not in ('active',):return False
    now=time(now)
    if not time(request['issued_at'])<=now<time(request['expires_at']):return False
    sc=record['scope']
    if sc['space_ref'] not in request['space_refs'] or policy['space_ref']!=sc['space_ref']:return False
    if sc['policy_ref']!={'id':policy['policy_id'],'version':policy['revision']}:return False
    if policy['controller_ref']!=sc['owner_ref']:return False
    effects=[]
    for rule in policy['rules']:
        if rule['status']!='active' or rule['membership_ref'] is not None:continue
        if not time(rule['valid_from'])<=now<time(rule['expires_at']):continue
        if request['authenticated_subject_ref'] not in rule['subjects']:continue
        if record['memory_id'] not in rule['object_ids']:continue
        if request['action'] not in rule['actions'] or request['purpose'] not in rule['purposes']:continue
        if request['runtime_ref'] not in rule['runtime_refs']:continue
        if rule['session_refs'] and request['session_ref'] not in rule['session_refs']:continue
        # Deny cannot be evaded by adding a processor. Finite oracle grants no outbound processing.
        if rule['effect']=='deny':effects.append('deny');continue
        if request['processor_refs']:continue
        effects.append('allow')
    return 'allow' in effects and 'deny' not in effects

def delta_bindings(envelope,current):
    d=envelope['delta'];q=envelope['request'];b=envelope['bindings']
    if d['status']!='proposed' or q['action']!='write':return False
    if d['avatar_id']!=q['avatar_id'] or d['runtime_id']!=q['runtime_ref']:return False
    changes=d['changes'];ids=[x['change_id'] for x in changes];bids=[x['change_id'] for x in b]
    if len(set(ids))!=len(ids) or len(set(bids))!=len(bids) or set(ids)!=set(bids):return False
    by={x['change_id']:x for x in b}
    for ch in changes:
        binding=by[ch['change_id']];target=binding['target_object_id']
        if ch['domain']!='aiap.memory':return False
        if ch['operation'] not in ('add','update'):return False
        c=ch['candidate'];cur=current.get(target)
        if c.get('memory_id')!=target or c.get('scope')!=binding['scope']:return False
        if binding['scope']['space_ref'] not in q['space_refs']:return False
        if cur is None:
            if binding['base_revision']!=0 or ch['operation']!='add':return False
        elif ch['operation']=='add' or binding['base_revision']!=cur['revision'] or binding['scope']!=cur['scope']:return False
        # Active inferred content cannot be submitted as confirmed fact through this finite oracle.
        if c.get('source',{}).get('source_type')=='inferred' and c.get('status')=='active':return False
    return True

def transfer_consistency(certificate,manifest,manifest_bytes,now,destination):
    """Only pre-signature consistency. True NEVER means transfer is authorized."""
    p=certificate['payload'];n=time(now)
    if not time(p['issued_at'])<=n<time(p['expires_at']):return False
    if p['destination_ref']!=destination:return False
    if p['manifest_sha256']!=hashlib.sha256(manifest_bytes).hexdigest():return False
    if not critical(p['required_extensions']):return False
    for k in ('avatar_ids','space_refs'):
        if set(p[k])!=set(manifest[k]):return False
    if p['mode']!=manifest['mode']:return False
    if manifest['restore_guarantee']=='offline-complete' and any(e['disposition'] in ('unresolved','reference-only') for e in manifest['entries']):return False
    return True

def activate_transfer(*args,**kwargs):
    # No production crypto profile has been selected or implemented in this package.
    return 'E_CRYPTO_PROFILE_UNSUPPORTED'
