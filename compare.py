"""Merge all results/*.json into results/summary.md (paste this table into your README / slides)."""
import json
from pathlib import Path
rows = [json.load(open(f)) for f in sorted(Path("results").glob("*.json"))]
hdr = "| Run | Model | Aug | PV acc | PV F1 | PlantDoc acc | PlantDoc F1 | Gap | Blur acc | Noise acc | Dim-light acc |\n|---|---|---|---|---|---|---|---|---|---|---|\n"
lines = []
for r in rows:
    rb = r["robustness"]
    lines.append(f"| {r['run']} | {r['model']} | {r['aug']} | {r['plantvillage_test']['accuracy']:.3f} | {r['plantvillage_test']['macro_f1']:.3f} | "
                 f"{r['plantdoc_test']['accuracy']:.3f} | {r['plantdoc_test']['macro_f1']:.3f} | {r['domain_gap_accuracy']:.3f} | "
                 f"{rb['blur']['accuracy']:.3f} | {rb['noise']['accuracy']:.3f} | {rb['bright_low']['accuracy']:.3f} |")
Path("results/summary.md").write_text(hdr + "\n".join(lines) + "\n", encoding="utf8")
print(hdr + "\n".join(lines))
