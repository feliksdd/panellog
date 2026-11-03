"""Generate OEM-dimensioned PanelLog prototype lands; see docs/review_2026-11-03.md."""
from pathlib import Path
import uuid
ROOT=Path(__file__).resolve().parents[1]/'hardware/footprints/PanelLog.pretty'
def uid(): return str(uuid.uuid4())
def rect(x1,y1,x2,y2,layer='F.Fab',w=.1):return f'(fp_rect (start {x1} {y1}) (end {x2} {y2}) (stroke (width {w}) (type default)) (fill no) (layer "{layer}"))'
def pad(n,x,y,w,h,layers='"F.Cu" "F.Paste" "F.Mask"',extra=''):
 return f'(pad "{n}" smd rect (at {x} {y}) (size {w} {h}) (layers {layers}) {extra})'
def text(t,x,y,layer='F.SilkS'):return f'(fp_text user "{t}" (at {x} {y}) (layer "{layer}") (effects (font (size .8 .8) (thickness .12))))'
def write(name,desc,body,court):
 x,y=court
 s=f'''(footprint "{name}" (version 20241229) (generator "pcbnew") (layer "F.Cu")
(descr "{desc}") (attr smd)
(property "Reference" "REF**" (at 0 {-y-.8}) (layer "F.SilkS") (effects (font (size .8 .8) (thickness .12))))
(property "Value" "{name}" (at 0 {y+.8}) (layer "F.Fab") (effects (font (size .8 .8) (thickness .12))))
{rect(-x,-y,x,y,'F.CrtYd',.05)}
'''+ '\n'.join(body)+'\n)\n'
 (ROOT/(name+'.kicad_mod')).write_text(s)
# TI DDA0008B drawing 4214849/B 09/2025: signal pad centers +/-2.7, 1.55x.6.
b=[rect(-1.95,-2.45,1.95,2.45),text('1',-3.1,-2.9)]
for n in range(1,9):
 x=-2.7 if n<=4 else 2.7;y=(-1.905+(n-1)*1.27) if n<=4 else (-1.905+(8-n)*1.27)
 b.append(pad(n,x,y,1.55,.6))
b.append(pad(9,0,0,2.95,3.64,'"F.Cu" "F.Mask"','(solder_mask_margin -0.12)'))
for x in [-.65,.65]:
 for y in [-.82,.82]:b.append(pad('',x,y,1.15,1.45,'"F.Paste"'))
write('LM5164_DDA','TI LM5164 DDA0008B; 9=grounded EP; 2.71x3.40 mask opening; divided paste',b,(3.8,2.9))
# BVB manufacturer page2: a=2.9,c=2.0,e=.9,f=.8,g=5.6.
b=[rect(-3.45,-3.3,3.45,3.3),text('F+',-2.45,-4.3),text('S+',-2.45,4.3)]
for x,force,sense in [(-2.45,1,3),(2.45,2,4)]:
 b.extend([pad(force,x,-.85,2.9,5.6),pad(sense,x,3.2,2.9,.9)])
write('BVB_M_R0007_Kelvin','Isabellenhuette BVB 18-Feb-2025 p2; force 1/2 sense 3/4; no copper bridge between force/sense',b,(4.15,3.9))
# Infineon PG-HSOF-8-1 OEM footprint, same top-view orientation as drawing.
b=[rect(-5.15,-5.85,5.15,5.85),text('1',-4.2,7.4)]
# Copper drain outline: extra-width top lip, recessed sides then main pad.
b.extend([pad(9,0,-2.65,9.7,8.08,'"F.Cu" "F.Mask"'),pad(9,0,-5.94,10.1,1.5,'"F.Cu" "F.Mask"')])
for n in range(1,9):
 x=-4.2+1.2*(n-1);b.append(pad(n,x,5.29,.8,2.8,'"F.Cu" "F.Mask"'));b.append(pad('',x,5.29,.8,2.7,'"F.Paste"'))
# Join source lead fingers (2..8) as recommended. Gate remains separate.
b.append(pad(2,.6,4.29,8,.8,'"F.Cu" "F.Mask"'))
# OEM 42 circular paste apertures, six rows (8,6,6,6,8,8).
for j in range(6):
 for i in range(8):
  if j in [1,2,3] and i in [0,7]:continue
  b.append(f'(pad "" smd circle (at {-4.2+i*1.2} {-5.79+j*1.2}) (size 1 1) (layers "F.Paste"))')
write('IPT015N10N5_TOLL','Infineon PG-HSOF-8-1; G1 S2..8 D9; OEM copper envelope and 42 aperture stencil',b,(5.7,7))
# Ebyte user manual v1.9 p5, top view rotated 180deg to put antenna at north edge.
b=[rect(-6.5,-9,6.5,9),text('ANTENNA',0,-7.5,'F.Fab'),text('1',-7.4,-4.8)]
for n in range(1,11):b.append(pad(n,-6.25,-4.03+(n-1)*1.27,1.5,.8))
for n in range(11,26,2):b.append(pad(n,-4.44+(n-11)/2*1.27,8.65,.8,1.5))
for n in range(12,25,2):b.append(pad(n,-3.81+(n-12)/2*1.27,6.9,.8,.8))
for idx,n in enumerate([26,27,29,31,33,35,37,39,41,43]):b.append(pad(n,6.25,7.4-idx*1.27,1.5,.8))
for n in range(28,43,2):b.append(pad(n,4.4,5.495-(n-28)/2*1.27,.8,.8))
b.append('''(zone (net 0) (net_name "") (layers "F.Cu" "B.Cu") (hatch edge .5)
 (connect_pads (clearance 0)) (min_thickness .25)
 (keepout (tracks not_allowed) (vias not_allowed) (pads not_allowed) (copperpour not_allowed) (footprints allowed))
 (fill (thermal_gap .3) (thermal_bridge_width .3))
 (polygon (pts (xy -9.5 -12) (xy 9.5 -12) (xy 9.5 -5.2) (xy -9.5 -5.2))))''')
write('E73_2G4M08S1C','Ebyte E73 v1.9 p5 top view rotated 180; 43 SMD lands; antenna copper keepout both layers',b,(7.3,9.7))
# Panasonic FN standard size F per RDE0000C1259, land a=3.1 gap,b=4.0,c=2.0.
write('Panasonic_F_8x10p2','Panasonic EEEFN2A100P FN size F 8x10.2; positive pad1; OEM 3.1 gap 4.0x2.0 lands',[rect(-4.15,-4.15,4.15,4.15),pad(1,-3.55,0,4,2),pad(2,3.55,0,4,2),text('+',-4,-2.2)],(5.85,4.5))
# SXN SMMS1040 drawing F=4.1 pad width,G=13.6 outside,H=5.4 gap.
write('SMMS1040','SXN SMMS1040 OEM family landpattern: 13.6 outside,5.4 gap,4.1 height',[rect(-5.75,-5.25,5.75,5.25),pad(1,-4.75,0,4.1,4.1),pad(2,4.75,0,4.1,4.1)],(7.1,5.6))
write('Wurth_7447709680','Wuerth 7447709680 OEM rev003.001: 68uH,120V; 2.9x5.4 lands with 7mm gap',[rect(-6.25,-6.25,6.25,6.25),pad(1,-4.95,0,2.9,5.4),pad(2,4.95,0,2.9,5.4)],(6.8,6.5))
