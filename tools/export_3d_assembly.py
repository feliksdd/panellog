import cadquery as cq
from pathlib import Path
import subprocess,tempfile
ROOT=Path(__file__).resolve().parents[1]
tmp=Path(tempfile.gettempdir())/'panellog_populated.step'
subprocess.run(['kicad-cli','pcb','export','step','--no-dnp','--force','-o',str(tmp),str(ROOT/'hardware/kicad/panellog.kicad_pcb')],check=True)
r=ROOT/'hardware/3dmodels';out=r/'assembly';out.mkdir(exist_ok=True)
pcb=cq.importers.importStep(str(tmp)).val()
print('PCB bounds',pcb.BoundingBox().zmin,pcb.BoundingBox().zmax)
# KiCad STEP bottom at z=0, top at z=1.6; project envelopes use top at z=0.
pcb=pcb.translate((0,0,-1.6))
base=cq.importers.importStep(str(r/'generated/Spelsberg_12741501_BASE_ENVELOPE.step')).val()
lid=cq.importers.importStep(str(r/'generated/Spelsberg_12741501_LID_ENVELOPE.step')).val()
a=cq.Assembly(name='PanelLog_enclosure_preview')
a.add(pcb,name='PCB_populated',color=cq.Color(.1,.45,.2));a.add(base,name='BASE_simplified',color=cq.Color(.65,.65,.65));a.add(lid,name='LID_simplified',color=cq.Color(.7,.7,.7))
a.save(str(out/'PanelLog_in_Spelsberg_ENVELOPE.step'))
# Check all locally referenced models load successfully as solids.
import json,hashlib
manifest=[]
for p in sorted(r.rglob('*.step')):
 sh=cq.importers.importStep(str(p)).val();assert sh.isValid(),p
 manifest.append(dict(path=str(p.relative_to(r)),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),solids=len(sh.Solids())))
(r/'validation.json').write_text(json.dumps(manifest,indent=2)+'\n')
print('Validated',len(manifest),'STEP files')
# Honest technical preview: open base; assembled lid intentionally omitted.
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
fig=plt.figure(figsize=(12,8));ax=fig.add_subplot(111,projection='3d',computed_zorder=False)
for sh,color,alpha in [(base,'#cccccc',.12)]+[(solid,'#367c52' if solid.BoundingBox().zmax<.2 else '#666666',1) for solid in pcb.Solids()]:
 verts,tris=sh.tessellate(.35)
 mesh=[[(verts[j].x,verts[j].y,verts[j].z) for j in t] for t in tris]
 ax.add_collection3d(Poly3DCollection(mesh,facecolors=color,edgecolors='none',alpha=alpha,zsort='min',zorder=1 if alpha<1 else (2 if color=='#367c52' else 3)))
ax.set_xlim(-20,170);ax.set_ylim(-125,15);ax.set_zlim(-15,45);ax.set_box_aspect((190,140,60));ax.view_init(48,-65)
ax.set_xlabel('X / mm');ax.set_ylabel('Y / mm');ax.set_zlabel('Z / mm');ax.set_title('PanelLog – offene Gehäusevorschau\nVereinfachtes Gehäusemodell; Deckel ausgeblendet')
fig.tight_layout();fig.savefig(str(out/'preview.png'),dpi=140)
