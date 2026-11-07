"""Regenerate plane stitching using filled copper intersections (KiCad 10).
Run with KiCad pcbnew and shapely. Preserves vias attached to routed tracks.
Refill and native DRC are mandatory after running this script.
"""
import pcbnew as p
from pathlib import Path
from shapely.geometry import Polygon,Point,LineString,box
from shapely.ops import unary_union
import json,collections,math
root=Path(__file__).resolve().parents[1]
path=root/'hardware/kicad/panellog.kicad_pcb'
b=p.LoadBoard(str(path))
footprints=list(b.GetFootprints())
removed_objects=[]
netlayers={'GND':[p.F_Cu,p.In1_Cu,p.B_Cu],'VDC':[p.F_Cu,p.In1_Cu,p.In2_Cu,p.B_Cu],'/MPPT_MINUS':[p.F_Cu,p.In1_Cu,p.In2_Cu,p.B_Cu],'/SHUNT_RETURN':[p.F_Cu,p.In1_Cu,p.In2_Cu,p.B_Cu]}
mm=lambda v: tuple(p.ToMM(v))
V=lambda x,y:p.VECTOR2I(p.FromMM(x),p.FromMM(y))
tracks=[t for t in b.GetTracks() if not isinstance(t,p.PCB_VIA)]
removed=collections.Counter();preserved=collections.Counter()
# Any via touched by a same-net track is functional and retained.
for v in list(b.GetTracks()):
 if not isinstance(v,p.PCB_VIA) or str(v.GetNetname()) not in netlayers:continue
 xy=Point(mm(v.GetPosition()))
 attached=any(t.GetNetCode()==v.GetNetCode() and LineString([mm(t.GetStart()),mm(t.GetEnd())]).distance(xy)<.001 for t in tracks)
 if attached:preserved[str(v.GetNetname())]+=1
 else:removed[str(v.GetNetname())]+=1;removed_objects.append(v);b.Remove(v)
filler=p.ZONE_FILLER(b);filler.Fill(b.Zones())
def chain(c):return [mm(c.CPoint(i)) for i in range(c.PointCount())]
def polygons(poly):
 res=[]
 for i in range(poly.OutlineCount()):
  outer=chain(poly.COutline(i));holes=[chain(poly.CHole(i,j)) for j in range(poly.HoleCount(i))]
  if len(outer)>=3:res.append(Polygon(outer,holes).buffer(0))
 return unary_union(res)
# Conservative courtyard-free pad and hole exclusion, including same-net pads.
obstacles=[]
for f in footprints:
 for pad in f.Pads():
  bb=pad.GetBoundingBox();obstacles.append(box(p.ToMM(bb.GetLeft()),p.ToMM(bb.GetTop()),p.ToMM(bb.GetRight()),p.ToMM(bb.GetBottom())).buffer(.35))
# Antenna copper keepout is already in filled zones; also prohibit drilling there.
obstacles.append(box(160,44,178,53))
base=unary_union(obstacles)
added=collections.Counter();created=[]
for net,layers in netlayers.items():
 dia=.6 if net=='GND' else .8;pitch=5 if net=='GND' else 3
 allowed=None
 for layer in layers:
  area=unary_union([polygons(z.GetFilledPolysList(layer)) for z in b.Zones() if str(z.GetNetname())==net and z.IsOnLayer(layer) and not z.GetIsRuleArea()])
  allowed=area if allowed is None else allowed.intersection(area)
 allowed=allowed.buffer(-dia/2-.25)
 other=[]
 for t in tracks:
  if str(t.GetNetname())!=net:other.append(LineString([mm(t.GetStart()),mm(t.GetEnd())]).buffer(p.ToMM(t.GetWidth())/2+dia/2+.25))
 for v in b.GetTracks():
  if isinstance(v,p.PCB_VIA):other.append(Point(mm(v.GetPosition())).buffer(p.ToMM(v.GetWidth(p.F_Cu))/2+dia/2+.3))
 allowed=allowed.difference(base.buffer(dia/2)).difference(unary_union(other))
 if allowed.is_empty:continue
 xmin,ymin,xmax,ymax=allowed.bounds
 for xi in range(math.ceil(xmin/pitch),math.floor(xmax/pitch)+1):
  for yi in range(math.ceil(ymin/pitch),math.floor(ymax/pitch)+1):
   x=xi*pitch;y=yi*pitch
   if not allowed.contains(Point(x,y)):continue
   v=p.PCB_VIA(b);v.SetPosition(V(x,y));v.SetWidth(p.FromMM(dia));v.SetDrill(p.FromMM(.3 if net=='GND' else .4));v.SetViaType(p.VIATYPE_THROUGH);v.SetLayerPair(p.F_Cu,p.B_Cu);v.SetNet(b.FindNet(net));b.Add(v)
   created.append({'uuid':v.m_Uuid.AsString(),'net':net,'x':x,'y':y,'layers':[b.GetLayerName(l) for l in layers]});added[net]+=1
filler=p.ZONE_FILLER(b);filler.Fill(b.Zones());p.SaveBoard(str(path),b)
report={'removed':dict(removed),'preserved_functional':dict(preserved),'added':dict(added),'created':created,'pitch_mm':{'GND':5,'power':3},'diameter_drill_mm':{'GND':[.6,.3],'power':[.8,.4]},'note':'Native DRC and layer connection verification required; not an ampacity qualification.'}
(root/'hardware/kicad/review_2026-11-07/stitching.json').write_text(json.dumps(report,indent=2)+'\n')
print({k:v for k,v in report.items() if k!='created'})
