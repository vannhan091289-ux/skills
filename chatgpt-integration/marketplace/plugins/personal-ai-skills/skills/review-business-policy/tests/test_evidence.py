"""Replay independent manual assessments, not scoring new text or invoking a model."""
import copy,hashlib,json
from pathlib import Path
import unittest
DATA=Path(__file__).resolve().parent/'fixtures/applications.json'
def verify(row,required):
    if row.get('answer_sha256')!=hashlib.sha256(row['answer'].encode()).hexdigest():
        raise ValueError('Answer differs from assessed bytes')
    if set(row['assessment'])!=set(required):raise ValueError('Missing acceptance criteria')
    for check in row['assessment'].values():
        if check['accepted'] is not True or not check['quote'] or check['quote'] not in row['answer']:
            raise ValueError('Unaccepted or untraceable manual assessment')
class Evidence(unittest.TestCase):
    def data(self):return json.loads(DATA.read_text())
    def test_five_independently_assessed_applications(self):
        d=self.data();self.assertEqual([r['sample']for r in d['responses']],list(range(1,6)))
        for r in d['responses']:verify(r,d['criteria'])
    def test_changed_answer_invalidates_assessment(self):
        d=self.data();r=copy.deepcopy(d['responses'][0]);r['answer']='fabricated output'
        with self.assertRaises(ValueError):verify(r,d['criteria'])
    def test_missing_requirement_cannot_pass(self):
        d=self.data();r=copy.deepcopy(d['responses'][0]);del r['assessment'][d['criteria'][0]]
        with self.assertRaises(ValueError):verify(r,d['criteria'])
    def test_rejected_assessment_cannot_pass(self):
        d=self.data();r=copy.deepcopy(d['responses'][0]);r['assessment'][d['criteria'][0]]['accepted']=False
        with self.assertRaises(ValueError):verify(r,d['criteria'])
    def test_rehashed_answer_without_original_quotes_cannot_pass(self):
        d=self.data();r=copy.deepcopy(d['responses'][0]);r['answer']='fabricated output'
        r['answer_sha256']=hashlib.sha256(r['answer'].encode()).hexdigest()
        with self.assertRaises(ValueError):verify(r,d['criteria'])
if __name__=='__main__':unittest.main()
