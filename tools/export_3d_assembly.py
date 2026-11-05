"""Export the populated PCB with available STEP models for the Kradex assembly.
Requires KiCad 10 CLI on PATH and CadQuery; missing components remain missing.
"""
from pathlib import Path
import subprocess,tempfile,json,hashlib
import cadquery as cq
ROOT=Path(__file__).resolve().parents[1];r=ROOT/'hardware/3dmodels';out=r/'assembly';out.mkdir(exist_ok=True)
tmp=Path(tempfile.gettempdir())/'panellog_real_populated.step'
subprocess.run(['kicad-cli','pcb','export','step','--no-dnp','--force','-o',str(tmp),str(ROOT/'hardware/kicad/panellog.kicad_pcb')],check=True)
pcb=cq.importers.importStep(str(tmp)).val().translate((0,0,-1.6))
a=cq.Assembly(name='PanelLog_external_models_INCOMPLETE');a.add(pcb,name='PCB_available_models');a.save(str(out/'PanelLog_external_models_INCOMPLETE.step'))
checks=[]
for p in sorted(r.rglob('*.st*')):
 if 'assembly' in p.parts:continue
 s=cq.importers.importStep(str(p)).val();assert s.isValid(),p
 bb=s.BoundingBox();checks.append(dict(path=str(p.relative_to(r)),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),solids=len(s.Solids()),bounds=[bb.xmin,bb.ymin,bb.zmin,bb.xmax,bb.ymax,bb.zmax]))
(r/'validation.json').write_text(json.dumps(checks,indent=2)+'\n')
print('Valid external STEP files:',len(checks))

import zipfile
f=out/"PanelLog_external_models_INCOMPLETE.step"
with zipfile.ZipFile(f.with_suffix(".zip"),"w",zipfile.ZIP_DEFLATED,compresslevel=9) as z:z.write(f,f.name)
f.unlink()
