#!/usr/bin/env python3
"""Generate the editable ROBOSKIN pin-level circuit specification and review artifacts.
No KiCad ERC/DRC or physical verification is implied. Python 3 standard library only.
"""
import csv,json,collections,xml.etree.ElementTree as ET
from pathlib import Path
HERE=Path(__file__).resolve().parent
components=[]
def add(ref,value,pins,package='',location='controller',note=''):
    components.append(dict(ref=ref,value=value,package=package,location=location,note=note,pins={str(k):v for k,v in pins.items()}))
def r(ref,val,a,b,location='controller'):add(ref,val,{1:a,2:b},'R_0603_1608Metric',location)
def c(ref,val,a,b='GND'):add(ref,val,{1:a,2:b},'C_0603_1608Metric')
# All MCU pins accounted for: None is deliberately not connected.
mp={i:None for i in range(1,49)}
mp.update({4:'3V3',5:'3V3_A',6:'3V3',7:'GND',8:'HSE_IN',10:'NRST',11:'ADC0',12:'ADC1',13:'UART_TX',14:'UART_RX',18:'ADC2',20:'ADC3',21:'WIT_DRIVE',22:'MUX_EN0',23:'TEMP_ADC0',24:'TEMP_ADC1',25:'MUX_EN1',26:'MUX_EN2',27:'MUX_EN3',28:'CAN_STB',29:'NODE_FAULT_N',32:'SERVICE_N',35:'SWDIO',36:'SWCLK',43:'WIT_RETURN',44:'MUX_A0',45:'MUX_A1',46:'MUX_A2',47:'CAN_RX',48:'CAN_TX'})
add('U1','STM32G0B1CBT6',mp,'LQFP-48_7x7mm_P0.5mm',note='Non-N package only; MCU firmware not supplied by this generator.')
add('J1','BM04B-GHS-TBT(LF)(SN)',{1:'5V_PATCH',2:'GND',3:'CANH',4:'CANL'},'JST_GH_1x04_1.25mm')
add('U2','TPS2553DBVR-1',{1:'5V_PATCH',2:'GND',3:'NODE_EN',4:'NODE_FAULT_N',5:'NODE_ILIM',6:'5V_NODE'},'SOT-23-6')
r('R_NODE_EN','100k 1%','5V_PATCH','NODE_EN');r('R_NODE_ILIM','200k 1%','NODE_ILIM','GND');r('R_NODE_FAULT','10k 1%','NODE_FAULT_N','3V3')
c('C_NODE_IN','1uF X7R 10V','5V_PATCH');c('C_NODE_HF','100nF X7R 10V','5V_PATCH');c('C_NODE_OUT','4.7uF X7R 10V','5V_NODE')
add('U3','TPS7A2433DBVR',{1:'5V_NODE',2:'GND',3:'5V_NODE',4:'GND',5:'3V3'},'SOT-23-5',note='Fixed-output NC pin4 tied GND per datasheet permission.')
c('C_LDO_IN','4.7uF X7R 10V','5V_NODE');c('C_LDO_OUT','4.7uF X7R 10V','3V3')
c('C_MCU_HF','100nF X7R 10V','3V3');c('C_MCU_BULK','4.7uF X7R 10V','3V3')
r('R_ANALOG','10R 1%','3V3','3V3_A');c('C_ANALOG_BULK','1uF X7R 10V','3V3_A');c('C_ANALOG_HF','100nF X7R 10V','3V3_A')
r('R_RESET','10k 1%','3V3','NRST');c('C_RESET','100nF X7R 10V','NRST');r('R_SERVICE','10k 1%','3V3','SERVICE_N')
add('J_SWD','SWD test pads',{1:'3V3',2:'GND',3:'SWDIO',4:'SWCLK',5:'NRST'},'TestPads',note='Pin1 sense only; do not power from debugger.')
add('J_UART','Service test pads',{1:'GND',2:'UART_TX',3:'UART_RX',4:'SERVICE_N'},'TestPads',note='3.3V UART 115200 8N1; strap pin4 to pin1 before reset for writes.')
add('Y1','ASV-8.000MHZ-LC-T',{1:'3V3',2:'GND',3:'OSC_RAW',4:'3V3'},'Oscillator_7.0x5.08mm');r('R_CLK','33R','OSC_RAW','HSE_IN');c('C_CLK','100nF X7R 10V','3V3')
add('U4','TCAN3413DR',{1:'CAN_TX',2:'GND',3:'3V3',4:'CAN_RX',5:'3V3',6:'CANL',7:'CANH',8:'CAN_STB'},'SOIC-8_3.9x4.9mm_P1.27mm')
r('R_CAN_TX','10k','3V3','CAN_TX');r('R_CAN_STB','47k','3V3','CAN_STB');c('C_CAN_VCC','100nF X7R 10V','3V3');c('C_CAN_VIO','100nF X7R 10V','3V3');c('C_CAN_BULK','1uF X7R 10V','3V3')
add('D_CAN','PESD2CANFD24V-T',{1:'CANH',2:'CANL',3:'GND'},'SOT-23')
sp=[13,14,15,12,1,5,2,4]
refs=[('30k','10k'),('15k','10k'),('10k','15k'),('10k','30k')]
for b in range(4):
    pins={16:'3V3_A',8:'GND',11:'MUX_A0',10:'MUX_A1',9:'MUX_A2',6:f'MUX_EN{b}',7:None,3:f'MUX_OUT{b}'}
    for j in range(7):pins[sp[j]]=f'SNS_FILT{7*b+j}'
    pins[sp[7]]=f'REF{b}'
    add(f'U_MUX{b}','TMUX1308PWR',pins,'TSSOP-16_4.4x5mm_P0.65mm',note='EN low selects; high disables.')
    r(f'R_MUX_EN{b}','47k',f'MUX_EN{b}','3V3');c(f'C_MUX{b}','100nF X7R 10V','3V3_A')
    r(f'R_MUX_OUT{b}','4.7k',f'MUX_OUT{b}',f'ADC{b}');c(f'C_ADC{b}','100pF C0G 50V',f'ADC{b}')
    r(f'R_REF_TOP{b}',refs[b][0], '3V3_A',f'REF{b}');r(f'R_REF_BOT{b}',refs[b][1],f'REF{b}','GND')
for i in range(28):
    r(f'R_BIAS{i:02}','22k 1%','3V3_A',f'SNS{i}')
    r(f'R_SER{i:02}','1k 1%',f'SNS{i}',f'SNS_FILT{i}');c(f'C_SNS{i:02}','100pF C0G 50V',f'SNS_FILT{i}')
    r(f'REOL{i:02}','100k printed +/-20%',f'SNS{i}','GND','remote_sensor_sheet')
    add(f'FSR{i:02}','Independent resistive taxel',{1:f'SNS{i}',2:'GND'},'Printed_PET_Custom','remote_sensor_sheet',note='Process-dependent resistance; remote EOL must be at this cell.')
pins={i+1:f'SNS{i}' for i in range(28)};pins.update({29:None,30:None,31:'GND',32:'GND',33:'WIT_OUT',34:'WIT_IN'});pins.update({i:'GND' for i in range(35,41)})
add('J_SENSOR','FH12-40S-0.5SH(55)',pins,'Hirose_FH12_1x40_P0.50mm',note='Bottom-contact; 0.3mm stiffened tail. Thermal signals are separate pads, not reserved29/30.')
for i in range(2):
    r(f'R_TEMP_BIAS{i}','39k 1%','3V3_A',f'TEMP_EXT{i}');r(f'R_TEMP_SER{i}','1k',f'TEMP_EXT{i}',f'TEMP_ADC{i}');c(f'C_TEMP{i}','1nF C0G 50V',f'TEMP_ADC{i}')
    add(f'TH{i}','NCU18XH103F60RB',{1:f'TEMP_EXT{i}',2:'GND'},'R_0603','thermal_flex')
add('J_THERMAL','Thermal flex pads',{1:'TEMP_EXT0',2:'TEMP_EXT1',3:'GND'},'SolderPads')
r('R_WIT_DRIVE','1k','WIT_DRIVE','WIT_OUT');r('R_WIT_SER','1k','WIT_IN','WIT_RETURN');r('R_WIT_DOWN','100k','WIT_RETURN','GND')
add('WIT_LOOP','Sheet perimeter conductor',{1:'WIT_OUT',2:'WIT_IN'},'Printed_Loop','remote_sensor_sheet')
protected=[f'SNS{i}' for i in range(28)]+['TEMP_EXT0','TEMP_EXT1','WIT_OUT','WIT_IN']
for i in range(8):
    pins={2:'GND',5:None};pins.update(dict(zip([1,6,3,4],protected[i*4:i*4+4])))
    add(f'D_A{i}','TPD4E1U06DBVR',pins,'SOT-23-6',note='Entry ESD array; system ESD protection requires measurement, not just part rating.')
patch=list(components);components=[]
# Region distributor for the independent sensor bus.
add('J_IN','Regulated isolated 5V input pads',{1:'5V_SUPPLY',2:'GND'},'Terminal_Block_5.08mm',location='region')
add('U_REG','TPS259530DSGR',{1:'DV_DT',2:'REGION_EN',3:'5V_SUPPLY',4:'5V_SUPPLY',5:'5V_REGION',6:'REGION_FAULT_N',7:'REGION_ILIM',8:'GND',9:'GND'},'WSON-8_2x2mm_EP',location='region',note='Pin9 denotes exposed thermal pad; latch-off 5.7V clamp variant.')
c('C_RAMP','180nF X7R 10V','DV_DT');c('C_REG_IN','10uF X7R 10V','5V_SUPPLY');c('C_REG_HF','100nF X7R 10V','5V_SUPPLY');c('C_REG_OUT','10uF X7R 10V','5V_REGION')
r('R_REG_EN_TOP','100k 1%','5V_SUPPLY','REGION_EN');r('R_REG_EN_BOT','39k 1%','REGION_EN','GND');r('R_REG_ILIM','2.05k 1%','REGION_ILIM','GND')
add('SW_RESET','Momentary normally open',{1:'REGION_EN',2:'GND'},'Reset_Button',location='region')
# Fault indication gets its own input-side 3.3 V; node loss must not extinguish reference rail.
add('U_MON','TPS7A2433DBVR',{1:'5V_SUPPLY',2:'GND',3:'5V_SUPPLY',4:'GND',5:'3V3_MON'},'SOT-23-5',location='region')
c('C_MON_IN','4.7uF X7R 10V','5V_SUPPLY');c('C_MON_OUT','4.7uF X7R 10V','3V3_MON');r('R_FLT','10k','3V3_MON','REGION_FAULT_N');r('R_LED','2.2k','3V3_MON','LED_A')
add('D_FAULT','Red status LED',{1:'REGION_FAULT_N',2:'LED_A'},'LED_0603',location='region',note='Pin1 cathode. Advisory indication only.')
add('J_FAULT','Monitor pads',{1:'GND',2:'3V3_MON',3:'REGION_FAULT_N'},'TestPads',location='region')
add('J_CAN','PCAN USB FD mating DB9',{2:'CANL',3:'GND',6:'GND',7:'CANH',1:None,4:None,5:None,8:None,9:None},'DB9_Female',location='region',note='Never take 5V from adapter pin1. Set internal termination OFF.')
r('R_TERM_NEAR','120R 1% 0.25W','CANH','CANL','region')
for i in range(1,9):add(f'J_BRANCH{i}','GHR-04V-S + SSHL-002T-P0.2',{1:'5V_REGION',2:'GND',3:'CANH',4:'CANL'},'Cable_Housing','distributed_trunk_tap',note='Distributed along linear trunk, not eight 2m star stubs. Branch <=50mm.')
r('R_TERM_FAR','120R 1% 0.25W','CANH','CANL','far_end_trunk')
for part in components:
    if part['location']=='controller':part['location']='region'
region=list(components)
def write(name,parts):
    nets=collections.defaultdict(list)
    for p in parts:
        for pin,net in p['pins'].items():
            if net is not None:nets[net].append(dict(ref=p['ref'],pin=pin))
    data={'design':f'ROBOSKIN {name}','release_status':'PIN_LEVEL_DESIGN_REVIEW_ONLY_NOT_ROUTED_OR_HARDWARE_VALIDATED','parts':parts,'nets':dict(nets)}
    (HERE/f'{name}.json').write_text(json.dumps(data,indent=2)+'\n')
    with (HERE/f'{name}_connections.csv').open('w') as f:
        w=csv.writer(f,lineterminator='\n');w.writerow(['reference','part','package_pin','net','assembly','note'])
        for p in parts:
            for pin,net in p['pins'].items():w.writerow([p['ref'],p['value'],pin,net or 'NC',p['location'],p['note']])
    root=ET.Element('export',version='D');design=ET.SubElement(root,'design');ET.SubElement(design,'source').text=f'{name}.json';ET.SubElement(design,'tool').text='ROBOSKIN build_circuit.py (review export)'
    cs=ET.SubElement(root,'components')
    for p in parts:
        co=ET.SubElement(cs,'comp',ref=p['ref']);ET.SubElement(co,'value').text=p['value'];ET.SubElement(co,'footprint').text=p['package'];fields=ET.SubElement(co,'fields');ET.SubElement(fields,'field',name='Assembly').text=p['location']
    ns=ET.SubElement(root,'nets')
    for i,(n,nodes) in enumerate(sorted(nets.items()),1):
        ne=ET.SubElement(ns,'net',code=str(i),name=n)
        for node in nodes:ET.SubElement(ne,'node',**node)
    ET.indent(root);ET.ElementTree(root).write(HERE/f'{name}.net',encoding='utf-8',xml_declaration=True)
    return data
p=write('patch_circuit',patch);q=write('region_circuit',region)
assert len([x for x in patch if x['ref'].startswith('R_')])==88
assert len([x for x in patch if x['ref'].startswith('C_')])==52
assert len(p['parts'][0]['pins'])==48
print(f'Patch: {len(patch)} components, {len(p["nets"])} nets; region: {len(region)} components, {len(q["nets"])} nets. Controller passives: 88 R + 52 C; remote EOL excluded.')
