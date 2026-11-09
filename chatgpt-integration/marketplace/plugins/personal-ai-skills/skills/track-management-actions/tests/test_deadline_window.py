"""Independent deadline boundary/precision regressions for the read-only helper."""
import json,subprocess,sys,unittest
from pathlib import Path
SCRIPT=Path(__file__).resolve().parents[1]/'scripts/deadline_window.py'
class Deadline(unittest.TestCase):
 def run_request(self,data,code=0,raw=False):
  p=subprocess.run([sys.executable,'-B',str(SCRIPT),'-'],input=data if raw else json.dumps(data),capture_output=True,text=True)
  self.assertEqual(p.returncode,code,p.stderr or p.stdout);self.assertEqual(p.stderr,'');return json.loads(p.stdout)
 def payload(self,due):return {'schema_version':1,'as_of':'2026-11-09T10:00:00+07:00','deadlines':[{'id':'D','due':due}]}
 def test_thirty_one_hours_not_fifty_five(self):
  r=self.run_request(self.payload('2026-11-10T17:00:00+07:00'))['rows'][0]
  self.assertEqual((r['hours_until_due'],r['relation']),('31','future_timestamp'))
 def test_date_only_never_invents_exact_hours(self):
  for due,relation,days in [('2026-11-08','past_date',-1),('2026-11-09','due_date',0),('2026-11-10','future_date',1)]:
   with self.subTest(due=due):
    r=self.run_request(self.payload(due))['rows'][0];self.assertEqual((r['hours_until_due'],r['relation'],r['calendar_days_until_due']),(None,relation,days))
 def test_equal_instant_across_offsets(self):
  r=self.run_request(self.payload('2026-11-09T03:00:00Z'))['rows'][0];self.assertEqual((r['hours_until_due'],r['relation']),('0','due_timestamp'))
 def test_past_timestamp_and_fractional_hours(self):
  for due,h in [('2026-11-08T10:00:00+07:00','-24'),('2026-11-09T10:30:00+07:00','0.5')]:
   self.assertEqual(self.run_request(self.payload(due))['rows'][0]['hours_until_due'],h)
 def test_missing_timezone_and_invalid_calendar_date(self):
  for due in ['2026-11-10T17:00:00','2026-02-30','2026-11-10Z','nonsense']:
   self.assertEqual(self.run_request(self.payload(due),1)['status'],'REWORK')
 def test_duplicate_id_and_key_rejected(self):
  p=self.payload('2026-11-10');p['deadlines']*=2
  self.assertEqual(self.run_request(p,1)['status'],'REWORK')
  self.assertEqual(self.run_request('{"schema_version":1,"schema_version":1}',1,True)['status'],'REWORK')
 def test_wrong_type_and_missing_asof_timezone(self):
  p=self.payload('2026-11-10');p['as_of']='2026-11-09T10:00:00'
  self.assertEqual(self.run_request(p,1)['status'],'REWORK')
 def test_invalid_offset_components_are_not_silently_normalized(self):
  for offset in ['+07:99','-07:99','+07:60','+24:00']:
   with self.subTest(offset=offset):
    self.assertEqual(self.run_request(self.payload('2026-11-10T17:00:00'+offset),1)['status'],'REWORK')
    p=self.payload('2026-11-10T17:00:00+07:00');p['as_of']='2026-11-09T10:00:00'+offset
    self.assertEqual(self.run_request(p,1)['status'],'REWORK')
 def test_utc_conversion_outside_calendar_returns_json_rework(self):
  for due in ['0001-01-01T00:00:00+01:00','9999-12-31T23:59:59-01:00']:
   with self.subTest(due=due):
    self.assertEqual(self.run_request(self.payload(due),1)['status'],'REWORK')
    p=self.payload('2026-11-10T17:00:00+07:00');p['as_of']=due
    self.assertEqual(self.run_request(p,1)['status'],'REWORK')
  p=self.payload('2026-11-10');p['schema_version']=True
  self.assertEqual(self.run_request(p,1)['status'],'REWORK')
if __name__=='__main__':unittest.main()
