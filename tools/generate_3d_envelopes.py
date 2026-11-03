"""Reproducible simplified CAD envelopes; requires cadquery 2.7.
These are project-created visual envelopes, NOT manufacturer CAD.
Coordinates: mm, footprint local origin, positive Z above PCB top.
"""
from pathlib import Path
import cadquery as cq
OUT=Path(__file__).resolve().parents[1]/'hardware/3dmodels/generated'
OUT.mkdir(parents=True,exist_ok=True)
def box(x,y,z,cx=0,cy=0,bottom=0):return cq.Workplane('XY').box(x,y,z,centered=(True,True,False)).translate((cx,cy,bottom)).val()
def cylinder(r,h,x=0,y=0,z=0):return cq.Workplane('XY').circle(r).extrude(h).translate((x,y,z)).val()
def save(name,parts):
 s=cq.Compound.makeCompound(parts);assert s.isValid();cq.exporters.export(s,str(OUT/(name+'.step')))
 return s
# Package bodies and simple lead envelopes. Overall z heights are conservative visual estimates.
def ic(name,x,y,h,n,pitch,span):
 parts=[box(x,y,h,bottom=.15)]
 for side in [-1,1]:
  for i in range(n//2):parts.append(box(.7,.25,.15,side*span/2,(i-(n/2-1)/2)*pitch))
 save(name,parts)
ic('LM5164_DDA_ENVELOPE',3.9,4.9,1.6,8,1.27,5.4)
ic('INA228_DGS10_ENVELOPE',3,3,1.0,10,.5,4.4)
save('IPT015N10N5_ENVELOPE',[box(10.3,11.7,2.3,bottom=.1)]+[box(.7,1.5,.1,-4.2+i*1.2,-6) for i in range(8)])
save('BVB_M_ENVELOPE',[box(6.9,6.6,1.6,bottom=.1)])
save('Wurth_7447709680_ENVELOPE',[cylinder(6.25,8),box(2.9,5.4,.3,-4.95),box(2.9,5.4,.3,4.95)])
save('Panasonic_F_8x10p2_ENVELOPE',[box(8.3,8.3,.5),cylinder(4,9.7,z=.5),box(2.5,3.5,.2,-3.55),box(2.5,3.5,.2,3.55)])
save('E73_2G4M08S1C_ENVELOPE',[box(13,18,.8),box(11,11,2,bottom=.8,cy=-1),box(9,2.5,2.2,bottom=.8,cy=7)])
save('Crystal_3215_ENVELOPE',[box(3.2,1.5,.9,bottom=.1)])
# Wires are assembly illustrations; no plug connector bodies on direct solder pads.
save('PV_SOLDER_WIRES_ENVELOPE',[cylinder(1.1,3.5,0,y) for y in [-9,9]]+[cylinder(3,10,0,y,3.5) for y in [-9,9]])
save('PT1000_SOLDER_WIRES_ENVELOPE',[cylinder(.25,4,0,y) for y in [-1.27,1.27]]+[cylinder(.6,8,0,y,4) for y in [-1.27,1.27]])
# Hollow enclosure: board center (75,-55); PCB top z=0, bottom=-1.6.
# Floor top=-9.6; 8mm insulated supports. No claim of OEM wall/rib/dome geometry.
cx,cy=75,-55
floor=-12.6
base=cq.Workplane('XY').box(180,130,48,centered=(True,True,False)).translate((cx,cy,floor))
inner=cq.Workplane('XY').box(174,124,46,centered=(True,True,False)).translate((cx,cy,floor+3))
base=base.cut(inner)
for x,y in [(25,-10),(125,-10),(25,-100),(125,-100)]:
 post=cq.Workplane('XY').circle(3.5).circle(1.25).extrude(8).translate((x,y,-9.6));base=base.union(post)
save('Spelsberg_12741501_BASE_ENVELOPE',[base.val()])
lid=cq.Workplane('XY').box(180,130,14.5,centered=(True,True,False)).translate((cx,cy,35.4))
cavity=cq.Workplane('XY').box(174,124,12,centered=(True,True,False)).translate((cx,cy,35.3))
save('Spelsberg_12741501_LID_ENVELOPE',[lid.cut(cavity).val()])
print('Generated',len(list(OUT.glob('*.step'))),'valid STEP envelopes')
