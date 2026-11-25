"""Train the FairView scoring model on SYNTHETIC past decisions.
Writes model.json (used by index.html). No real data is involved.
Run: pip install numpy scikit-learn ; python train_model.py
"""
import json
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

rng = np.random.default_rng(0)
n = 300
grades = rng.normal(70, 12, n).clip(40, 100)
hours = rng.normal(30, 20, n).clip(0, 100)
income = rng.integers(1, 6, n)
# Past decisions with a deliberately seeded income effect (the bias the audit should find)
z = 0.08 * (grades - 70) + 0.03 * (hours - 30) + 0.35 * (income - 3)
y = (z + rng.normal(0, 0.8, n) > 0).astype(int)

X = np.c_[grades, hours, income]
sc = StandardScaler().fit(X)
m = LogisticRegression().fit(sc.transform(X), y)

model = {
    "features": ["Grades", "Volunteering", "Income band"],
    "mean": sc.mean_.round(4).tolist(),
    "std": sc.scale_.round(4).tolist(),
    "coef": m.coef_[0].round(4).tolist(),
    "intercept": round(float(m.intercept_[0]), 4),
}
json.dump(model, open("model.json", "w"), indent=2)
print(model)

# ---- Audit numbers (SYNTHETIC applicants, scored with the trained model) ----
def prob(g, h, i):
    x = np.c_[g, h, i]
    return m.predict_proba(sc.transform(x))[:, 1]

rng2 = np.random.default_rng(1)
N = 500
G = rng2.normal(70, 12, N).clip(40, 100)
H = rng2.normal(30, 20, N).clip(0, 100)
I = rng2.integers(1, 6, N)
p = prob(G, H, I)
rate = {int(b): round(float((p[I == b] >= 0.6).mean() * 100)) for b in range(1, 6)}
flip = float(((prob(G, H, np.ones(N)) >= 0.6) != (prob(G, H, np.full(N, 5.0)) >= 0.6)).mean() * 100)
model["audit"] = {"n": N, "rate_by_band": rate, "gap": max(rate.values()) - min(rate.values()),
                  "flip_pct": round(flip)}
json.dump(model, open("model.json", "w"), indent=2)
print(model["audit"])
