"""Offline circuit-structure checks; these do not replace ERC, DRC or bench tests."""
import json,unittest,xml.etree.ElementTree as ET
from pathlib import Path
HERE=Path(__file__).resolve().parent
class CircuitTests(unittest.TestCase):
 def setUp(self):
  self.patch=json.loads((HERE/'patch_circuit.json').read_text());self.region=json.loads((HERE/'region_circuit.json').read_text())
  self.p={p['ref']:p for p in self.patch['parts']};self.r={p['ref']:p for p in self.region['parts']}
 def test_references_and_connectivity(self):
  for data in [self.patch,self.region]:
   self.assertEqual(len(data['parts']),len({p['ref'] for p in data['parts']}))
   assignments={}
   for net,nodes in data['nets'].items():
    self.assertGreaterEqual(len(nodes),2,net)
    for n in nodes:
     key=(n['ref'],n['pin']);self.assertNotIn(key,assignments);assignments[key]=net
   for p in data['parts']:
    for pin,net in p['pins'].items():
     if net is not None:self.assertEqual(assignments[(p['ref'],pin)],net)
 def test_no_robot_power_net(self):
  for data in [self.patch,self.region]:
   self.assertFalse(any('48V' in n or '30V' in n or 'MOTOR' in n for n in data['nets']))
 def test_sensor_banks_are_independent(self):
  channelpins=[13,14,15,12,1,5,2]
  for b in range(4):
   mux=self.p[f'U_MUX{b}']['pins']
   for j,pin in enumerate(channelpins):self.assertEqual(mux[str(pin)],f'SNS_FILT{7*b+j}')
   self.assertEqual(mux['4'],f'REF{b}')
   self.assertEqual(mux['6'],f'MUX_EN{b}')
  self.assertEqual(len([x for x in self.p if x.startswith('REOL')]),28)
  self.assertTrue(all(self.p[f'REOL{i:02}']['location']=='remote_sensor_sheet' for i in range(28)))
 def test_connector_identity_and_thermal(self):
  self.assertEqual(self.p['J1']['pins'],{'1':'5V_PATCH','2':'GND','3':'CANH','4':'CANL'})
  sensor=self.p['J_SENSOR']['pins'];self.assertEqual(len(sensor),40)
  for i in range(28):self.assertEqual(sensor[str(i+1)],f'SNS{i}')
  self.assertIsNone(sensor['29']);self.assertIsNone(sensor['30'])
  self.assertEqual(self.p['J_THERMAL']['pins']['1'],'TEMP_EXT0')
 def test_power_and_standby(self):
  self.assertEqual(self.p['U2']['pins']['6'],'5V_NODE');self.assertEqual(self.p['U3']['pins']['1'],'5V_NODE')
  self.assertEqual(self.p['R_CAN_STB']['pins'],{'1':'3V3','2':'CAN_STB'})
  self.assertEqual(self.p['U1']['pins']['47'],'CAN_RX');self.assertEqual(self.p['U1']['pins']['48'],'CAN_TX')
 def test_exact_termination_and_passive_counts(self):
  self.assertFalse(any('TERM' in p for p in self.p))
  self.assertEqual(len([x for x in self.r if x.startswith('R_TERM')]),2)
  self.assertEqual(len([x for x in self.p if x.startswith('R_')]),88)
  self.assertEqual(len([x for x in self.p if x.startswith('C_')]),52)
  self.assertEqual(len([x for x in self.r if x.startswith('J_BRANCH')]),8)
 def test_protection_and_isolated_adapter(self):
  mapped=[]
  for i in range(8):mapped += [self.p[f'D_A{i}']['pins'][str(pin)] for pin in [1,6,3,4]]
  self.assertEqual(len(set(mapped)),32)
  self.assertEqual(self.r['J_CAN']['pins']['7'],'CANH');self.assertIsNone(self.r['J_CAN']['pins']['1'])
 def test_xml_matches_json(self):
  for name,data in [('patch_circuit',self.patch),('region_circuit',self.region)]:
   root=ET.parse(HERE/f'{name}.net').getroot()
   self.assertEqual(len(root.findall('components/comp')),len(data['parts']))
   self.assertEqual(len(root.findall('nets/net')),len(data['nets']))
if __name__=='__main__':unittest.main()
