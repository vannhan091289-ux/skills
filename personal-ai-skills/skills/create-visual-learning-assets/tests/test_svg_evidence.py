"""Verify captured SVG artifacts, not new model output or pixel/screen-reader quality."""
import json,re,unittest,xml.etree.ElementTree as ET
from pathlib import Path
DATA=Path(__file__).resolve().parent/'fixtures/applications.json'
def parse(answer):
 m=re.search(r'<svg\b[\s\S]*?</svg>',answer)
 if not m:raise ValueError('No SVG source')
 if re.search(r'<!DOCTYPE|<!ENTITY|<\?xml-stylesheet',m.group(),re.I):raise ValueError('Active/external XML forbidden')
 return ET.fromstring(m.group())
class SvgEvidence(unittest.TestCase):
 def roots(self):return[parse(r['answer'])for r in json.loads(DATA.read_text())['responses']]
 def test_five_well_formed_svg_sources(self):
  roots=self.roots();self.assertEqual(len(roots),5)
  for r in roots:self.assertEqual(r.tag.split('}')[-1],'svg')
 def test_static_sources_have_accessible_titles_and_descriptions(self):
  for r in self.roots():
   tags={p.tag.split('}')[-1]for p in r.iter()};self.assertTrue({'title','desc'}<=tags);self.assertFalse({'script','foreignObject'}&tags)
   for p in r.iter():
    for key,value in p.attrib.items():
     self.assertFalse(key.lower().startswith('on'))
     if key.split('}')[-1]=='href':self.assertTrue(value.startswith('#'),'External asset not permitted in fixture')
 def test_canvas_matches_supplied_dimensions(self):
  for r in self.roots():
   if 'viewBox'in r.attrib:dimensions=list(map(float,r.attrib['viewBox'].replace(',',' ').split()))[2:]
   else:dimensions=[float(r.attrib[k].removesuffix('px'))for k in ['width','height']]
   self.assertEqual(dimensions,[800,500])
 def test_text_preserves_ratios_units_period_and_source(self):
  for r in self.roots():
   text=' '.join(r.itertext()).replace(',','.');compact=re.sub(r'\s+','',text)
   for value in ['80%','60%','73.33%','points','2026-10','DEMO']:self.assertIn(value,compact)
if __name__=='__main__':unittest.main()
