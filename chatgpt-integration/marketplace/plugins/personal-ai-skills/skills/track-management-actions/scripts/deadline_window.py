#!/usr/bin/env python3
"""Read-only deadline arithmetic; does not infer completion, SLA or working days."""
import json
import re
import sys
from datetime import date, datetime, timezone
from decimal import Decimal, localcontext
from pathlib import Path


def unique(pairs):
    out = {}
    for key, value in pairs:
        if key in out:
            raise ValueError('duplicate JSON key')
        out[key] = value
    return out


def timestamp(value):
    if type(value) is not str or not re.fullmatch(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}(?::\d{2}(?:\.\d{1,6})?)?(?:Z|[+-]\d{2}:\d{2})', value):
        raise ValueError('timestamp requires ISO calendar date, T, time and explicit offset')
    if not value.endswith('Z'):
        offset = value[-6:]
        if int(offset[1:3]) > 23 or int(offset[4:6]) > 59:
            raise ValueError('timezone offset components out of range')
    parsed = datetime.fromisoformat(value.replace('Z', '+00:00'))
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValueError('timezone required')
    return parsed


def calculate(data):
    if type(data) is not dict or set(data) != {'schema_version', 'as_of', 'deadlines'}:
        raise ValueError('expected schema_version, as_of and deadlines only')
    if type(data['schema_version']) is not int or data['schema_version'] != 1:
        raise ValueError('schema_version must be integer1')
    as_of = timestamp(data['as_of'])
    if type(data['deadlines']) is not list or not data['deadlines']:
        raise ValueError('deadlines must be a nonempty list')
    seen, rows = set(), []
    for row in data['deadlines']:
        if type(row) is not dict or set(row) != {'id', 'due'}:
            raise ValueError('deadline needs id and due only')
        key, due = row['id'], row['due']
        if type(key) is not str or not key.strip() or key in seen:
            raise ValueError('deadline id must be nonempty and unique')
        seen.add(key)
        if type(due) is not str:
            raise ValueError('due must be an ISO string')
        if re.fullmatch(r'\d{4}-\d{2}-\d{2}', due):
            days = (date.fromisoformat(due) - as_of.date()).days
            relation = 'past_date' if days < 0 else 'future_date' if days > 0 else 'due_date'
            precision, hours = 'date', None
        else:
            end = timestamp(due)
            delta = end.astimezone(timezone.utc) - as_of.astimezone(timezone.utc)
            days = (end.astimezone(as_of.tzinfo).date() - as_of.date()).days
            with localcontext() as ctx:
                ctx.prec = 28
                seconds = Decimal(delta.days * 86400 + delta.seconds) + Decimal(delta.microseconds) / 1000000
                value = seconds / 3600
                hours = format(value.normalize(), 'f') if value else '0'
            relation = 'past_timestamp' if delta.total_seconds() < 0 else 'future_timestamp' if delta.total_seconds() > 0 else 'due_timestamp'
            precision = 'timestamp'
        rows.append({'id': key, 'due': due, 'precision': precision, 'relation': relation,
                     'calendar_days_until_due': days, 'hours_until_due': hours})
    return {'status': 'CALCULATED', 'as_of': data['as_of'], 'hours_method': 'Decimal seconds/3600, precision28; null for date-only', 'rows': rows}


def main():
    try:
        if len(sys.argv) != 2:
            raise ValueError('Usage: python deadline_window.py INPUT.json|-')
        raw = sys.stdin.read() if sys.argv[1] == '-' else Path(sys.argv[1]).read_text(encoding='utf-8')
        def invalid_constant(_):
            raise ValueError('non-finite JSON constant forbidden')
        result = calculate(json.loads(raw, object_pairs_hook=unique, parse_constant=invalid_constant))
    except (ValueError, TypeError, KeyError, OSError, OverflowError) as exc:
        print(json.dumps({'status': 'REWORK', 'error': str(exc)}, ensure_ascii=False))
        return 1
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
