"""Train one model.   Examples:
  python train.py --model baseline --aug basic --epochs1 12 --epochs2 0 --run baseline_basic
  python train.py --model mobilenet_v3 --aug basic --run mobilenet_basic
  python train.py --model mobilenet_v3 --aug field --run mobilenet_field
  python train.py --model efficientnet_b0 --aug field --run effnet_field
Stage 1: frozen pretrained backbone, train the classifier head.
Stage 2: unfreeze the last blocks and fine-tune with a lower learning rate.
"""
import argparse, json, time
from collections import Counter
from pathlib import Path
import torch, torch.nn as nn
from torch.utils.data import DataLoader
from tqdm import tqdm
import data, models
from config import SEED

def pick_device():
    if torch.cuda.is_available(): return "cuda"
    if getattr(torch.backends, "mps", None) and torch.backends.mps.is_available(): return "mps"
    return "cpu"

def run_epoch(model, loader, loss_fn, opt, device, scaler=None, train=True):
    model.train(train); tot = correct = n = 0; loss_sum = 0.0
    for x, y in tqdm(loader, leave=False):
        x, y = x.to(device), y.to(device)
        with torch.set_grad_enabled(train):
            with torch.autocast(device_type="cuda", enabled=(device == "cuda")):
                out = model(x); loss = loss_fn(out, y)
        if train:
            opt.zero_grad(set_to_none=True)
            if scaler: scaler.scale(loss).backward(); scaler.step(opt); scaler.update()
            else: loss.backward(); opt.step()
        loss_sum += loss.item() * len(y); correct += (out.argmax(1) == y).sum().item(); n += len(y)
    return loss_sum / n, correct / n

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="mobilenet_v3", choices=models.NAMES)
    ap.add_argument("--aug", default="basic", choices=["basic", "field"])
    ap.add_argument("--epochs1", type=int, default=4, help="stage 1 epochs (frozen backbone)")
    ap.add_argument("--epochs2", type=int, default=6, help="stage 2 epochs (partial unfreeze)")
    ap.add_argument("--bs", type=int, default=32)
    ap.add_argument("--workers", type=int, default=2)
    ap.add_argument("--no_pretrained", action="store_true")
    ap.add_argument("--run", default=None)
    ap.add_argument("--limit", type=int, default=0, help="debug: use only N training images")
    a = ap.parse_args()
    run = a.run or f"{a.model}_{a.aug}"
    torch.manual_seed(SEED)
    device = pick_device(); print("device:", device, "| run:", run)

    classes = json.load(open("data/classes.json"))
    tr = data.read_csv("data/pv_splits.csv", "train"); va = data.read_csv("data/pv_splits.csv", "val")
    if a.limit: tr = tr[: a.limit]
    dl_tr = DataLoader(data.LeafDS(tr, data.train_tf(a.aug)), a.bs, shuffle=True, num_workers=a.workers, pin_memory=device == "cuda")
    dl_va = DataLoader(data.LeafDS(va, data.eval_tf()), a.bs, num_workers=a.workers)

    # class-weighted loss for imbalance
    cnt = Counter(y for _, y in tr)
    w = torch.tensor([len(tr) / (len(classes) * max(cnt.get(i, 1), 1)) for i in range(len(classes))], dtype=torch.float32).to(device)
    loss_fn = nn.CrossEntropyLoss(weight=w, label_smoothing=0.05)

    model = models.build(a.model, len(classes), pretrained=not a.no_pretrained).to(device)
    scaler = torch.amp.GradScaler("cuda") if device == "cuda" else None
    hist, best = [], 0.0
    Path("outputs").mkdir(exist_ok=True)

    def phase(name, epochs, params, lr):
        nonlocal best
        if epochs <= 0: return
        for p in model.parameters(): p.requires_grad = False
        for p in params: p.requires_grad = True
        opt = torch.optim.AdamW([p for p in model.parameters() if p.requires_grad], lr=lr, weight_decay=1e-4)
        for ep in range(epochs):
            t0 = time.time()
            trl, tra = run_epoch(model, dl_tr, loss_fn, opt, device, scaler, True)
            val, vaa = run_epoch(model, dl_va, loss_fn, None, device, None, False)
            hist.append(dict(phase=name, epoch=ep + 1, train_loss=trl, train_acc=tra, val_loss=val, val_acc=vaa))
            print(f"[{name}] ep{ep+1}/{epochs} train_acc={tra:.3f} val_acc={vaa:.3f} ({time.time()-t0:.0f}s)")
            if vaa >= best:
                best = vaa
                torch.save(dict(model=a.model, classes=classes, state_dict=model.state_dict(), aug=a.aug, val_acc=vaa), f"outputs/{run}.pt")

    if a.model == "baseline":
        phase("scratch", a.epochs1 + a.epochs2, list(model.parameters()), 1e-3)
    else:
        phase("stage1_head", a.epochs1, models.head_params(model, a.model), 1e-3)
        phase("stage2_finetune", a.epochs2, models.head_params(model, a.model) + models.last_block_params(model, a.model), 1e-4)
    json.dump(hist, open(f"outputs/{run}_history.json", "w"), indent=1)
    print(f"done. best val_acc={best:.4f} -> outputs/{run}.pt")

if __name__ == "__main__":
    main()
