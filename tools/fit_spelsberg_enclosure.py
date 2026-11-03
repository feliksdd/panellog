"""Apply once to the routed 116x86 mm revision; dimensions in mm."""
import pcbnew as p
from pathlib import Path
root=Path(__file__).resolve().parents[1]
f=root/'hardware/kicad/panellog.kicad_pcb'; b=p.LoadBoard(str(f))
assert not any(fp.GetReference()=="H1" for fp in b.GetFootprints()), "Enclosure adaptation already applied"
def v(x,y):return p.VECTOR2I(p.FromMM(x),p.FromMM(y))
# Center old circuit in 150x104 outline: old edge (2,2) -> (17,12).
for item in list(b.GetFootprints())+list(b.GetTracks())+list(b.Zones())+list(b.GetDrawings()):item.Move(v(15,10))
# Save moved native objects, then insert mechanical primitives.
p.SaveBoard(str(f),b)
s=f.read_text()
import re,uuid
s=re.sub(r'\(start (?:17|133) (?:12|98)\)\n\s*\(end (?:17|133) (?:12|98)\)',lambda m:m.group(0),s)
# Replace only four Edge.Cuts line blocks.
pat=r'\(gr_line\s+\(start [^)]*\)\s+\(end [^)]*\)\s+\(stroke.*?\(layer "Edge.Cuts"\).*?\)'
lines=[]
for a,c in [((0,3),(150,3)),((150,3),(150,107)),((150,107),(0,107)),((0,107),(0,3))]:
 lines.append(f'(gr_line (start {a[0]} {a[1]}) (end {c[0]} {c[1]}) (stroke (width .1) (type default)) (layer "Edge.Cuts") (uuid "{uuid.uuid4()}"))')
# Match balanced top-level forms to avoid touching footprint graphics.
spans=[];depth=0;quoted=False;esc=False
for i,ch in enumerate(s):
 if quoted:
  if esc:esc=False
  elif ch==chr(92):esc=True
  elif ch=='"':quoted=False
 elif ch=='"':quoted=True
 elif ch=='(':
  if depth==1:start=i
  depth+=1
 elif ch==')':
  depth-=1
  if depth==1 and s[start:i+1].startswith('(gr_line') and '(layer "Edge.Cuts")' in s[start:i+1]:spans.append((start,i+1))
assert len(spans)==4
for a,c in reversed(spans):s=s[:a]+s[c:]
extra='\n'.join(lines)
for i,(x,y) in enumerate([(25,10),(125,10),(25,100),(125,100)],1):
 mod=(root/'hardware/footprints/PanelLog.pretty/MountingHole_3p2_Nylon.kicad_mod').read_text().replace('(footprint "MountingHole_3p2_Nylon"','(footprint "PanelLog:MountingHole_3p2_Nylon"').replace('(version 20241229) (generator "pcbnew")','').replace('(layer "F.Cu")',f'(layer "F.Cu") (at {x} {y})',1).replace('"H?"',f'"H{i}"')
 extra+=mod
 pts=' '.join(f'(xy {xx} {yy})' for xx,yy in [(x-3.5,y-3.5),(x+3.5,y-3.5),(x+3.5,y+3.5),(x-3.5,y+3.5)])
 extra+=f'(zone (net 0) (net_name "") (layers "F.Cu" "B.Cu") (hatch edge .5) (keepout (tracks not_allowed) (vias not_allowed) (pads allowed) (copperpour not_allowed) (footprints allowed)) (polygon (pts {pts})))'
s=s.rstrip();assert s.endswith(')');f.write_text(s[:-1]+extra+'\n)\n')
print('Applied 150x104 outline and four insulated mounting holes')
