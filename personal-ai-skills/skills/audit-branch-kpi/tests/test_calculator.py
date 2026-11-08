"""Behavioral contract for the local, read-only ratio calculator (stdlib only)."""
import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / 'scripts/calculate_ratio.py'


def fixture():
    return {
        'schema_version': 1, 'source_id': 'local-export',
        'formula': {'id': 'generic-ratio', 'version': '1',
                    'approval_reference': 'caller-reference', 'operation': 'ratio_pct',
                    'additive_across_entities': True},
        'metric_kind': 'flow', 'period': '2026-10', 'unit': 'count',
        'rows': [
            {'entity_id': 'a', 'period': '2026-10', 'unit': 'count', 'numerator': '80', 'denominator': '100'},
            {'entity_id': 'b', 'period': '2026-10', 'unit': 'count', 'numerator': '30', 'denominator': '50'},
        ],
    }


class RatioCalculatorTests(unittest.TestCase):
    def calculate(self, payload):
        self.assertTrue(SCRIPT.is_file(), 'ratio calculator implementation is missing')
        spec = importlib.util.spec_from_file_location('ratio_calculator', SCRIPT)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module.calculate(payload)

    def invalid(self, payload, code=None):
        result = self.calculate(payload)
        self.assertEqual(result['status'], 'REWORK')
        self.assertTrue(result['errors'])
        self.assertEqual(set(result), {'status', 'errors'})
        for error in result['errors']:
            self.assertEqual(set(error), {'code', 'location'})
        if code:
            self.assertIn(code, [error['code'] for error in result['errors']])
        return result

    def cli(self, data, path='-', raw=False):
        self.assertTrue(SCRIPT.is_file(), 'ratio calculator implementation is missing')
        return subprocess.run([sys.executable, str(SCRIPT), path],
                              input=data if raw else json.dumps(data).encode(),
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)

    def test_weighted_aggregation_is_not_mean_of_percentages(self):
        r = self.calculate(fixture())
        self.assertEqual((r['status'], r['total_numerator'], r['total_denominator'], r['ratio_pct']),
                         ('CALCULATED', '110', '150', '73.3333'))
        self.assertEqual(r['errors'], [])
        self.assertEqual(r['rows_checked'], 2)
        self.assertEqual(r['rounding'], 'ROUND_HALF_EVEN;4dp')
        self.assertEqual(r['approval_reference'], 'caller-reference')
        self.assertIn('caller-supplied, not authority verification', r['caveat'])

    def test_decimal_sums_are_exact(self):
        p = fixture()
        p['rows'][0].update(numerator='0.1', denominator='0.1')
        p['rows'][1].update(numerator='0.2', denominator='0.2')
        r = self.calculate(p)
        self.assertEqual((r['total_numerator'], r['total_denominator'], r['ratio_pct']), ('0.3', '0.3', '100.0000'))

    def test_repeating_decimal(self):
        p = fixture(); p['rows'] = p['rows'][:1]
        p['rows'][0].update(numerator='1', denominator='3')
        self.assertEqual(self.calculate(p)['ratio_pct'], '33.3333')

    def test_half_even_rounds_tie_to_even(self):
        p = fixture(); p['rows'] = p['rows'][:1]
        p['rows'][0].update(numerator='0.0000005', denominator='1')
        self.assertEqual(self.calculate(p)['ratio_pct'], '0.0000')
        p['rows'][0]['numerator'] = '0.0000015'
        self.assertEqual(self.calculate(p)['ratio_pct'], '0.0002')

    def test_zero_numerator_is_valid(self):
        p = fixture()
        for row in p['rows']: row['numerator'] = '0'
        self.assertEqual(self.calculate(p)['ratio_pct'], '0.0000')

    def test_zero_total_denominator_is_undefined(self):
        p = fixture()
        for row in p['rows']: row['denominator'] = '0'
        r = self.calculate(p)
        self.assertEqual((r['status'], r['ratio_pct'], r['total_denominator']), ('UNDEFINED', None, '0'))
        self.assertIn('ZERO_ROW_DENOMINATOR', [e['code'] for e in r['errors']])

    def test_one_zero_row_denominator_blocks_nonzero_total(self):
        p = fixture(); p['rows'][0]['denominator'] = '0'
        r = self.calculate(p)
        self.assertEqual((r['status'], r['ratio_pct'], r['total_denominator']), ('UNDEFINED', None, '50'))
        self.assertEqual(r['errors'][0], {'code': 'ZERO_ROW_DENOMINATOR', 'location': '$.rows[0].denominator'})

    def test_negative_rejected(self):
        p = fixture(); p['rows'][0]['numerator'] = '-1'; self.invalid(p)

    def test_nonplain_decimal_strings_rejected(self):
        for value in ('NaN', 'Infinity', '1e2', '+1', '.1', '1.', ' 1', '1\n', ''):
            with self.subTest(value=value):
                p = fixture(); p['rows'][0]['numerator'] = value; self.invalid(p)

    def test_float_bool_int_null_and_container_rejected(self):
        for value in (0.5, True, 1, None, [], {}):
            with self.subTest(value=repr(value)):
                p = fixture(); p['rows'][0]['denominator'] = value; self.invalid(p)

    def test_integer_digit_limit(self):
        p = fixture(); p['rows'][0]['numerator'] = '9' * 31; self.invalid(p)

    def test_fraction_digit_limit(self):
        p = fixture(); p['rows'][0]['numerator'] = '0.' + '1' * 13; self.invalid(p)

    def test_maximum_numeric_values_and_small_denominator(self):
        p = fixture(); p['rows'] = p['rows'][:1]
        p['rows'][0].update(numerator='999999999999999999999999999999.999999999999', denominator='0.000000000001')
        self.assertEqual(self.calculate(p)['ratio_pct'], '99999999999999999999999999999999999999999900.0000')

    def test_empty_rows_rejected(self):
        p = fixture(); p['rows'] = []; self.invalid(p)

    def test_limit_accepts_10000_rows_exact_sum(self):
        p = fixture(); row = p['rows'][0]
        p['rows'] = [dict(row, entity_id=str(i), numerator='0.000000000001', denominator='1') for i in range(10000)]
        r = self.calculate(p)
        self.assertEqual((r['rows_checked'], r['total_numerator'], r['total_denominator']), (10000, '0.00000001', '10000'))

    def test_too_many_rows_rejected(self):
        p = fixture(); p['rows'] = [dict(p['rows'][0], entity_id=str(i)) for i in range(10001)]; self.invalid(p)

    def test_duplicate_entity_even_identical_is_rejected(self):
        p = fixture(); p['rows'][1] = copy.deepcopy(p['rows'][0]); self.invalid(p, 'DUPLICATE_ENTITY')

    def test_period_mismatch_rejected(self):
        p = fixture(); p['rows'][0]['period'] = '2026-09'; self.invalid(p, 'PERIOD_MISMATCH')

    def test_unit_mismatch_rejected(self):
        p = fixture(); p['rows'][0]['unit'] = 'VND'; self.invalid(p, 'UNIT_MISMATCH')

    def test_snapshot_single_period_valid(self):
        p = fixture(); p['metric_kind'] = 'snapshot'
        self.assertEqual(self.calculate(p)['ratio_pct'], '73.3333')

    def test_snapshot_cannot_aggregate_reporting_dates(self):
        p = fixture(); p['metric_kind'] = 'snapshot'; p['rows'][1]['period'] = '2026-11'; self.invalid(p)

    def test_nonadditive_formula_rejected(self):
        for value in (False, 1, 'true', None):
            with self.subTest(value=value):
                p = fixture(); p['formula']['additive_across_entities'] = value; self.invalid(p)

    def test_unknown_and_unhashable_operation_rejected(self):
        for value in ('sum', [], {}, None):
            with self.subTest(value=value):
                p = fixture(); p['formula']['operation'] = value; self.invalid(p)

    def test_wrong_typed_or_empty_metadata_rejected(self):
        for key in ('source_id', 'period', 'unit', 'metric_kind'):
            for value in ([], {}, True, None, '', '  '):
                with self.subTest(key=key, value=value):
                    p = fixture(); p[key] = value; self.invalid(p)
        for key in ('id', 'version', 'approval_reference'):
            p = fixture(); p['formula'][key] = []; self.invalid(p)

    def test_unknown_fields_rejected(self):
        for target in ('root', 'formula', 'row'):
            p = fixture()
            obj = p if target == 'root' else p['formula'] if target == 'formula' else p['rows'][0]
            obj['extra'] = 'secret-marker'
            self.assertNotIn('secret-marker', json.dumps(self.invalid(p)))

    def test_missing_fields_and_invalid_containers(self):
        for payload in (None, [], 'abc', 1, {}): self.invalid(payload)
        for key in fixture():
            p = fixture(); del p[key]; self.invalid(p)
        for key in ('formula', 'rows'):
            for value in (None, 'abc', True, {} if key == 'rows' else []):
                p = fixture(); p[key] = value; self.invalid(p)
        p = fixture(); p['rows'][0] = []; self.invalid(p)

    def test_schema_version_rejects_bool_or_unsupported(self):
        for value in (True, '1', 2, None):
            p = fixture(); p['schema_version'] = value; self.invalid(p)

    def test_calculate_does_not_mutate_input_or_decimal_context(self):
        from decimal import getcontext
        p = fixture(); original = copy.deepcopy(p); precision = getcontext().prec
        self.calculate(p)
        self.assertEqual(p, original); self.assertEqual(getcontext().prec, precision)

    def test_calculation_is_independent_of_callers_decimal_traps(self):
        from decimal import Inexact, localcontext
        with localcontext() as context:
            context.prec = 2
            context.traps[Inexact] = True
            self.assertEqual(self.calculate(fixture())['ratio_pct'], '73.3333')
            self.assertEqual(context.prec, 2)
            self.assertTrue(context.traps[Inexact])

    def test_cli_stdin_calculated_exit_0(self):
        process = self.cli(fixture())
        self.assertEqual(process.returncode, 0)
        self.assertEqual(json.loads(process.stdout)['ratio_pct'], '73.3333')
        self.assertEqual(process.stderr, b'')

    def test_cli_undefined_exit_1(self):
        p = fixture(); p['rows'][0]['denominator'] = '0'
        process = self.cli(p)
        self.assertEqual(process.returncode, 1)
        self.assertEqual(json.loads(process.stdout)['status'], 'UNDEFINED')

    def test_cli_invalid_schema_exit_2(self):
        process = self.cli({'secret-marker': 'do not echo'})
        self.assertEqual(process.returncode, 2)
        self.assertNotIn(b'secret-marker', process.stdout + process.stderr)

    def test_cli_duplicate_json_keys_rejected_at_any_depth(self):
        for raw in (b'{"schema_version":1,"schema_version":1}',
                    json.dumps(fixture()).replace('"id": "generic-ratio"', '"id":"generic-ratio","id":"generic-ratio"').encode()):
            process = self.cli(raw, raw=True)
            self.assertEqual(process.returncode, 2)
            self.assertIn('DUPLICATE_JSON_KEY', [e['code'] for e in json.loads(process.stdout)['errors']])

    def test_cli_malformed_json_utf8_and_nonstandard_constants(self):
        for raw in (b'{"private":"secret-marker"', b'\xff', b'{"x":NaN}', b'{"x":Infinity}'):
            with self.subTest(raw=raw):
                process = self.cli(raw, raw=True)
                self.assertEqual(process.returncode, 2)
                self.assertEqual(json.loads(process.stdout)['status'], 'REWORK')
                self.assertNotIn(b'Traceback', process.stderr + process.stdout)
                self.assertNotIn(b'secret-marker', process.stderr + process.stdout)

    def test_cli_file_read_only_and_missing_or_directory_io(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'input.json'; content = json.dumps(fixture()).encode(); path.write_bytes(content)
            process = self.cli(b'', str(path), raw=True)
            self.assertEqual(process.returncode, 0); self.assertEqual(path.read_bytes(), content)
            for failed_path in (Path(tmp) / 'missing.json', Path(tmp)):
                process = self.cli(b'', str(failed_path), raw=True)
                self.assertEqual(process.returncode, 2)
                self.assertEqual(json.loads(process.stdout)['errors'][0]['code'], 'INPUT_IO_ERROR')
                self.assertEqual(process.stderr, b'')

    def test_cli_argument_errors_return_json(self):
        self.assertTrue(SCRIPT.is_file(), 'ratio calculator implementation is missing')
        for args in ([], ['-', 'extra']):
            process = subprocess.run([sys.executable, str(SCRIPT), *args], capture_output=True, check=False)
            self.assertEqual(process.returncode, 2)
            self.assertEqual(json.loads(process.stdout)['status'], 'REWORK')
            self.assertEqual(process.stderr, b'')


if __name__ == '__main__':
    unittest.main()
