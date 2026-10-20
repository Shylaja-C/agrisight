"""Evaluate a trained checkpoint on:
   1) PlantVillage test split        (in-distribution, lab images)
   2) PlantDoc                        (external real-field images)  <- the cross-dataset test
   3) PlantVillage test + perturbations (brightness, contrast, blur, noise)  <- robustness
Outputs results/<run>.json, a PlantDoc confusion-matrix PNG, and (optionally) Grad-CAM failure examples.

  python evaluate.py --ckpt outputs/mobilenet_field.pt --failures 8
"""
import argparse, json
from pathlib import Path
import numpy as np, torch
from torch.utils.data import DataLoader
from sklearn.metrics import classification_report, confusion_matrix, f1_score
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
import data, models
from train import pick_device

@torch.no_grad()
def predict_rows(model, rows, device, perturb=None, bs=32, workers=2):
    dl = DataLoader(data.LeafDS(rows, data.eval_tf(), perturb), bs, num_workers=workers)
    P, Y = [], []
    for x, y in dl:
        P.append(torch.softmax(model(x.to(device)), 1).cpu().numpy()); Y.append(y.numpy())
    P = np.concatenate(P); Y = np.concatenate(Y)
    return P, Y

def summarize(P, Y):
    pred = P.argmax(1)
    return dict(n=int(len(Y)), accuracy=float((pred == Y).mean()),
                macro_f1=float(f1_score(Y, pred, average="macro", zero_division=0)),
                mean_confidence=float(P.max(1).mean()))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ckpt", required=True)
    ap.add_argument("--workers", type=int, default=2)
    ap.add_argument("--failures", type=int, default=0, help="save N misclassified PlantDoc images with Grad-CAM")
    a = ap.parse_args()
    device = pick_device()
    model, ck = models.load_checkpoint(a.ckpt, device)
    classes, run = ck["classes"], Path(a.ckpt).stem
    Path("results").mkdir(exist_ok=True)
    res = dict(run=run, model=ck["model"], aug=ck.get("aug"), classes=classes)

    pv = data.read_csv("data/pv_splits.csv", "test")
    pdr = data.read_csv("data/pd_test.csv")
    P, Y = predict_rows(model, pv, device, workers=a.workers); res["plantvillage_test"] = summarize(P, Y)
    Pd, Yd = predict_rows(model, pdr, device, workers=a.workers); res["plantdoc_test"] = summarize(Pd, Yd)
    res["domain_gap_accuracy"] = res["plantvillage_test"]["accuracy"] - res["plantdoc_test"]["accuracy"]
    res["robustness"] = {}
    for p in data.PERTURBATIONS:
        Pp, Yp = predict_rows(model, pv, device, perturb=p, workers=a.workers)
        res["robustness"][p] = summarize(Pp, Yp)

    pred = Pd.argmax(1)
    res["plantdoc_report"] = classification_report(Yd, pred, labels=list(range(len(classes))),
                                                   target_names=classes, output_dict=True, zero_division=0)
    json.dump(res, open(f"results/{run}.json", "w"), indent=1)

    cm = confusion_matrix(Yd, pred, labels=list(range(len(classes))))
    fig, ax = plt.subplots(figsize=(9, 8)); ax.imshow(cm, cmap="Greens")
    ax.set_xticks(range(len(classes))); ax.set_yticks(range(len(classes)))
    short = [c.split("___")[0][:6] + ":" + c.split("___")[-1][:10] for c in classes]
    ax.set_xticklabels(short, rotation=90, fontsize=7); ax.set_yticklabels(short, fontsize=7)
    ax.set_title(f"{run}: PlantDoc confusion matrix"); ax.set_xlabel("predicted"); ax.set_ylabel("true")
    plt.tight_layout(); plt.savefig(f"results/{run}_plantdoc_cm.png", dpi=130); plt.close()

    print(f"\n{run}\n  PlantVillage test : acc={res['plantvillage_test']['accuracy']:.3f} F1={res['plantvillage_test']['macro_f1']:.3f}")
    print(f"  PlantDoc (field)  : acc={res['plantdoc_test']['accuracy']:.3f} F1={res['plantdoc_test']['macro_f1']:.3f}")
    print(f"  domain gap (acc)  : {res['domain_gap_accuracy']:.3f}")
    for k, v in res["robustness"].items(): print(f"  robustness {k:13s}: acc={v['accuracy']:.3f}")

    if a.failures:
        from PIL import Image
        import gradcam_utils as gu
        out = Path(f"results/{run}_failures"); out.mkdir(exist_ok=True)
        bad = [i for i in range(len(Yd)) if pred[i] != Yd[i]][: a.failures]
        for i in bad:
            img = Image.open(pdr[i][0]).convert("RGB")
            ov, cam = gu.gradcam_overlay(model, ck["model"], img, int(pred[i]), device)
            fig, ax = plt.subplots(1, 2, figsize=(7, 3.6)); ax[0].imshow(img.resize((224, 224))); ax[1].imshow(ov)
            for x in ax: x.axis("off")
            ax[0].set_title(f"true: {classes[Yd[i]][:28]}", fontsize=7)
            ax[1].set_title(f"pred: {classes[pred[i]][:28]} ({Pd[i].max():.2f})\nborder attention {gu.background_reliance(cam):.2f}", fontsize=7)
            plt.tight_layout(); plt.savefig(out / f"fail_{i}.png", dpi=110); plt.close()
        print(f"  saved {len(bad)} failure examples -> {out}")

if __name__ == "__main__":
    main()
