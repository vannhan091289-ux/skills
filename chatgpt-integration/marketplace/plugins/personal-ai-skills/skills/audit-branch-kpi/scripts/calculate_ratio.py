#!/usr/bin/env python3
"""Validate and aggregate a caller-declared, single-period generic ratio.

Reads JSON only. Uses no network, third-party packages, configuration or writes.
An approval reference is provenance supplied by the caller, never verification
of authority, accounting policy or suitability of the declared formula.
"""
from decimal import Context, Decimal, ROUND_HALF_EVEN, localcontext
import json
from pathlib import Path
import re
import sys


_NUMBER = re.compile(r'[0-9]{1,30}(?:\.[0-9]{1,12})?', re.ASCII)
_ROOT_KEYS = frozenset({'schema_version', 'source_id', 'formula', 'metric_kind', 'period', 'unit', 'rows'})
_FORMULA_KEYS = frozenset({'id', 'version', 'approval_reference', 'operation', 'additive_across_entities'})
_ROW_KEYS = frozenset({'entity_id', 'period', 'unit', 'numerator', 'denominator'})
_CAVEAT = 'Calculation only; approval reference is caller-supplied, not authority verification'


def _error(code, location):
    return {'code': code, 'location': location}


def _rework(errors):
    return {'status': 'REWORK', 'errors': errors}


def _nonempty_string(value):
    return isinstance(value, str) and bool(value.strip())


def _decimal_string(value):
    return isinstance(value, str) and _NUMBER.fullmatch(value) is not None


def _plain(value):
    text = format(value, 'f')
    return text.rstrip('0').rstrip('.') if '.' in text else text


def calculate(payload: dict) -> dict:
    """Return CALCULATED, UNDEFINED (any zero row denominator), or REWORK.

    Invalid schemas return only fixed error codes and safe schema locations.
    Valid inputs retain declared provenance and exact additive totals. The
    original payload and the caller's Decimal context are left untouched.
    """
    errors = []
    if not isinstance(payload, dict):
        return _rework([_error('INVALID_OBJECT', '$')])
    if set(payload) != _ROOT_KEYS:
        errors.append(_error('INVALID_FIELDS', '$'))
    if type(payload.get('schema_version')) is not int or payload.get('schema_version') != 1:
        errors.append(_error('INVALID_SCHEMA_VERSION', '$.schema_version'))
    for key in ('source_id', 'period', 'unit'):
        if not _nonempty_string(payload.get(key)):
            errors.append(_error('INVALID_STRING', '$.' + key))
    if not isinstance(payload.get('metric_kind'), str) or payload['metric_kind'] not in ('flow', 'snapshot'):
        errors.append(_error('INVALID_METRIC_KIND', '$.metric_kind'))

    formula = payload.get('formula')
    if not isinstance(formula, dict):
        errors.append(_error('INVALID_OBJECT', '$.formula'))
    else:
        if set(formula) != _FORMULA_KEYS:
            errors.append(_error('INVALID_FIELDS', '$.formula'))
        for key in ('id', 'version', 'approval_reference'):
            if not _nonempty_string(formula.get(key)):
                errors.append(_error('INVALID_STRING', '$.formula.' + key))
        if not isinstance(formula.get('operation'), str) or formula['operation'] != 'ratio_pct':
            errors.append(_error('UNSUPPORTED_OPERATION', '$.formula.operation'))
        if formula.get('additive_across_entities') is not True:
            errors.append(_error('NONADDITIVE_FORMULA', '$.formula.additive_across_entities'))

    rows = payload.get('rows')
    if not isinstance(rows, list) or not 1 <= len(rows) <= 10000:
        errors.append(_error('INVALID_ROWS', '$.rows'))
        return _rework(errors)
    entities = set()
    zero_denominators = []
    for index, row in enumerate(rows):
        base = '$.rows[' + str(index) + ']'
        if not isinstance(row, dict):
            errors.append(_error('INVALID_OBJECT', base))
            continue
        if set(row) != _ROW_KEYS:
            errors.append(_error('INVALID_FIELDS', base))
        entity = row.get('entity_id')
        if not _nonempty_string(entity):
            errors.append(_error('INVALID_STRING', base + '.entity_id'))
        elif entity in entities:
            errors.append(_error('DUPLICATE_ENTITY', base + '.entity_id'))
        else:
            entities.add(entity)
        for key, mismatch in (('period', 'PERIOD_MISMATCH'), ('unit', 'UNIT_MISMATCH')):
            if not _nonempty_string(row.get(key)):
                errors.append(_error('INVALID_STRING', base + '.' + key))
            elif row[key] != payload.get(key):
                errors.append(_error(mismatch, base + '.' + key))
        for key in ('numerator', 'denominator'):
            if not _decimal_string(row.get(key)):
                errors.append(_error('INVALID_DECIMAL', base + '.' + key))
            elif key == 'denominator' and Decimal(row[key]).is_zero():
                zero_denominators.append(_error('ZERO_ROW_DENOMINATOR', base + '.denominator'))
    if errors:
        return _rework(errors)

    # At most 10,000 terms with 30 integer and 12 fractional digits:
    # each exact total needs at most 46 significant digits.
    with localcontext(Context(prec=60, rounding=ROUND_HALF_EVEN)):
        numerator = sum((Decimal(row['numerator']) for row in rows), Decimal(0))
        denominator = sum((Decimal(row['denominator']) for row in rows), Decimal(0))
        ratio = None if zero_denominators else format(
            (numerator * Decimal(100) / denominator).quantize(Decimal('0.0001'), rounding=ROUND_HALF_EVEN), 'f')
    return {
        'status': 'UNDEFINED' if zero_denominators else 'CALCULATED',
        'errors': zero_denominators,
        'source_id': payload['source_id'], 'period': payload['period'], 'unit': payload['unit'],
        'formula_id': formula['id'], 'formula_version': formula['version'],
        'total_numerator': _plain(numerator), 'total_denominator': _plain(denominator),
        'ratio_pct': ratio, 'rounding': 'ROUND_HALF_EVEN;4dp', 'rows_checked': len(rows),
        'approval_reference': formula['approval_reference'], 'caveat': _CAVEAT,
    }


class _DuplicateJSONKey(ValueError):
    pass


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise _DuplicateJSONKey()
        result[key] = value
    return result


def _invalid_constant(_value):
    raise ValueError()


def main(argv=None):
    args = sys.argv[1:] if argv is None else argv
    if len(args) != 1:
        result = _rework([_error('INVALID_ARGUMENTS', '$')])
    else:
        try:
            if args[0] == '-':
                content = sys.stdin.buffer.read().decode('utf-8')
            else:
                with Path(args[0]).open('r', encoding='utf-8') as handle:
                    content = handle.read()
            payload = json.loads(content, object_pairs_hook=_unique_object, parse_constant=_invalid_constant)
            result = calculate(payload)
        except _DuplicateJSONKey:
            result = _rework([_error('DUPLICATE_JSON_KEY', '$')])
        except (OSError, ValueError) as exc:
            code = 'INPUT_IO_ERROR' if isinstance(exc, OSError) else 'INVALID_JSON'
            result = _rework([_error(code, '$')])
        except RecursionError:
            result = _rework([_error('INVALID_JSON', '$')])
    try:
        sys.stdout.write(json.dumps(result, ensure_ascii=True, allow_nan=False) + '\n')
        sys.stdout.flush()
    except OSError:
        return 2
    return {'CALCULATED': 0, 'UNDEFINED': 1, 'REWORK': 2}[result['status']]


if __name__ == '__main__':
    sys.exit(main())
