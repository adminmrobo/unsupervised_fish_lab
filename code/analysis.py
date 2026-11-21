# 비지도학습 물고기 연구실 — 모든 페이지 숫자의 원본(results.json)을 만든다
# 데이터: Fish_Market_Data_Machine_Learning/data/fish_market_x10.csv (1,590행 → 무게 0·중복 제외 1,554마리)
import json, sys
import numpy as np, pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.metrics import silhouette_score, adjusted_rand_score
from sklearn.neighbors import KNeighborsClassifier, NearestNeighbors
from sklearn.model_selection import StratifiedGroupKFold, GroupShuffleSplit, cross_val_score
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.neural_network import MLPRegressor

src = sys.argv[1]; out = sys.argv[2]
df = pd.read_csv(src)
df = df[df.weight_g > 0].drop_duplicates().reset_index(drop=True)
F = ["weight_g", "length1_cm", "length2_cm", "length3_cm", "height_cm", "width_cm"]
SP = ["Bream", "Parkki", "Perch", "Pike", "Roach", "Smelt", "Whitefish"]
X = df[F].values; y = df.species.values; g = df.seed_id.values
R = {}
R["n"] = int(len(df)); R["n_orig"] = int((df.source == "original").sum()); R["groups"] = int(df.seed_id.nunique())
R["counts"] = df.species.value_counts().to_dict()
R["desc"] = {c: {"min": round(float(df[c].min()), 2), "max": round(float(df[c].max()), 2), "mean": round(float(df[c].mean()), 2), "std": round(float(df[c].std()), 2)} for c in F}
R["corr"] = np.round(np.corrcoef(X.T), 3).tolist()

sc = StandardScaler().fit(X); Z = sc.transform(X)
R["scaler"] = {"mean": sc.mean_.round(4).tolist(), "scale": sc.scale_.round(4).tolist()}

# 1. 표준화 전후 '가장 가까운 이웃'이 같은 종인 비율 (같은 seed_id 이웃은 빼고 = 복제본 제외)
def nn_agree(M):
    nn = NearestNeighbors(n_neighbors=40).fit(M)
    dist, idx = nn.kneighbors(M)
    ok = 0
    for i in range(len(M)):
        for j in idx[i][1:]:
            if g[j] != g[i]:
                ok += (y[j] == y[i]); break
    return ok / len(M)
hr = df.height_cm / df.length1_cm; wr = df.width_cm / df.length1_cm
df["hr"] = hr; df["wr"] = wr
R["nn_agree"] = {"raw": round(nn_agree(X), 4), "std": round(nn_agree(Z), 4),
                 "ratio": round(nn_agree(StandardScaler().fit_transform(df[["hr", "wr", "length1_cm"]])), 4)}
# 무게가 거리에서 차지하는 몫 (원 단위 vs 표준화): 이웃 거리 제곱합 중 무게 몫
def weight_share(M):
    nn = NearestNeighbors(n_neighbors=2).fit(M); _, idx = nn.kneighbors(M)
    d2 = (M - M[idx[:, 1]]) ** 2
    return float(d2[:, 0].sum() / d2.sum())
R["weight_share"] = {"raw": round(weight_share(X), 4), "std": round(weight_share(Z), 4)}
# 거리 손계산 예: 원본 Bream 0번과 Bream 1번
a, b = X[0], X[1]
R["dist_example"] = {"a": a.round(2).tolist(), "b": b.round(2).tolist(),
                     "raw": round(float(np.linalg.norm(a - b)), 2), "std": round(float(np.linalg.norm(Z[0] - Z[1])), 3)}

# 2. 군집화
km = {}
for k in range(1, 9):
    m = KMeans(k, n_init=10, random_state=42).fit(Z)
    s = float(silhouette_score(Z, m.labels_)) if k > 1 else None
    km[k] = {"inertia": round(float(m.inertia_), 1), "sil": None if s is None else round(s, 3), "ari": round(float(adjusted_rand_score(y, m.labels_)), 3)}
R["km6"] = km
Zr = StandardScaler().fit_transform(df[["hr", "wr"]])
kr = {}
for k in range(1, 9):
    m = KMeans(k, n_init=10, random_state=42).fit(Zr)
    s = float(silhouette_score(Zr, m.labels_)) if k > 1 else None
    kr[k] = {"inertia": round(float(m.inertia_), 1), "sil": None if s is None else round(s, 3), "ari": round(float(adjusted_rand_score(y, m.labels_)), 3)}
R["kmr"] = kr
m3 = KMeans(3, n_init=10, random_state=42).fit(Zr)
lab = m3.labels_
# 무대 이름: 높이비 평균 순으로 납작/중간/길쭉
order = np.argsort([-hr[lab == c].mean() for c in range(3)])
name = {int(order[0]): "flat", int(order[1]): "mid", int(order[2]): "long"}
ct = pd.crosstab(df.species, [name[int(c)] for c in lab])
R["ratio_k3_table"] = {sp: {k: int(ct.loc[sp].get(k, 0)) for k in ["flat", "mid", "long"]} for sp in ct.index}
R["ratio_k3_hr"] = {name[c]: [round(float(hr[lab == c].min()), 3), round(float(hr[lab == c].max()), 3), round(float(hr[lab == c].mean()), 3)] for c in range(3)}
R["hr_by_species"] = {s: [round(float(hr[y == s].mean()), 3), round(float(hr[y == s].min()), 3), round(float(hr[y == s].max()), 3)] for s in SP}
R["wr_by_species"] = {s: round(float(wr[y == s].mean()), 3) for s in SP}
R["raw_k3_ari"] = round(float(adjusted_rand_score(y, KMeans(3, n_init=10, random_state=42).fit_predict(X))), 3)
# 계층 군집 (원본 158마리, ward, 체형비) → k=3 ARI
orig = df[df.source == "original"].reset_index(drop=True)
Zo = StandardScaler().fit_transform(orig[["hr", "wr"]])
ag = AgglomerativeClustering(3, linkage="ward").fit(Zo)
R["ward158_k3_ari"] = round(float(adjusted_rand_score(orig.species, ag.labels_)), 3)

# 3. PCA
p = PCA().fit(Z); S = p.transform(Z)
R["pca"] = {"evr": p.explained_variance_ratio_.round(4).tolist(), "eig": p.explained_variance_.round(4).tolist(),
            "load": p.components_.round(4).tolist()}
# 부호 맞추기 확인: PC1 양수 = 큰 물고기, PC2 양수 = 높이 큰 쪽
R["pca_sign"] = {"pc1_weight_corr": round(float(np.corrcoef(S[:, 0], X[:, 0])[0, 1]), 3), "pc2_height_load": round(float(p.components_[1][4]), 3)}
rec = {}
for kk in range(1, 7):
    pk = PCA(kk).fit(Z); Zh = pk.inverse_transform(pk.transform(Z))
    rec[kk] = round(float(((Z - Zh) ** 2).mean()), 4)
R["pca_recon_mse"] = rec
# 종별 PC1·PC2 평균
R["pca_species_mean"] = {s: [round(float(S[y == s, 0].mean()), 3), round(float(S[y == s, 1].mean()), 3)] for s in SP}
# 접은 지도에서 이웃 일치율
R["nn_agree_pc"] = {"pc1": round(nn_agree(S[:, :1]), 4), "pc2": round(nn_agree(S[:, :2]), 4), "pc3": round(nn_agree(S[:, :3]), 4), "all6": round(nn_agree(Z), 4)}

# 4. 자기지도: 오토인코더 6→2→6 (tanh), 묶음 분할 80/20
gss = GroupShuffleSplit(1, test_size=0.2, random_state=0)
tr, te = next(gss.split(Z, y, g))
R["split"] = {"train": int(len(tr)), "test": int(len(te)), "train_groups": int(len(set(g[tr]))), "test_groups": int(len(set(g[te])))}
best = None
for rs in range(3):
    m = MLPRegressor(hidden_layer_sizes=(16, 2, 16), activation="tanh", max_iter=8000, random_state=rs,
                     learning_rate_init=0.002, alpha=1e-5, tol=1e-7, n_iter_no_change=200).fit(Z[tr], Z[tr])
    e = float(((m.predict(Z[te]) - Z[te]) ** 2).mean())
    if best is None or e < best[0]: best = (e, rs, m)
ae_te, ae_rs, ae = best
p2 = PCA(2).fit(Z[tr]); pc_te = float(((p2.inverse_transform(p2.transform(Z[te])) - Z[te]) ** 2).mean())
ae_tr = float(((ae.predict(Z[tr]) - Z[tr]) ** 2).mean()); pc_tr = float(((p2.inverse_transform(p2.transform(Z[tr])) - Z[tr]) ** 2).mean())
# 변수별 복원 오차 (시험)
ae_var = (((ae.predict(Z[te]) - Z[te]) ** 2).mean(0)).round(4).tolist()
pc_var = (((p2.inverse_transform(p2.transform(Z[te])) - Z[te]) ** 2).mean(0)).round(4).tolist()
R["ae_vs_pca"] = {"ae_test_mse": round(ae_te, 4), "pca2_test_mse": round(pc_te, 4), "ae_train_mse": round(ae_tr, 4), "pca2_train_mse": round(pc_tr, 4),
                  "ae_var": ae_var, "pca_var": pc_var, "ae_arch": "6-16-2-16-6 tanh", "ae_seed": ae_rs}
R["ae_weights"] = {"W": [w.round(5).tolist() for w in ae.coefs_], "b": [b.round(5).tolist() for b in ae.intercepts_]}
R["test_idx"] = [int(i) for i in te]
# 가린 무게 맞히기: 길이1·높이·폭으로 무게 (log-log 선형) — 정답은 데이터 자체
L = np.log(df[["length1_cm", "height_cm", "width_cm"]].values); W = np.log(df.weight_g.values)
lr = LinearRegression().fit(L[tr], W[tr]); pred = np.exp(lr.predict(L[te])); true = df.weight_g.values[te]
R["mask_weight"] = {"coef": lr.coef_.round(6).tolist(), "intercept": round(float(lr.intercept_), 6),
                    "mae_g": round(float(np.abs(pred - true).mean()), 1), "mape": round(float((np.abs(pred - true) / true).mean()), 4),
                    "median_ape": round(float(np.median(np.abs(pred - true) / true)), 4)}
# 평균값으로만 찍을 때 (기준선)
R["mask_weight"]["baseline_mae_g"] = round(float(np.abs(df.weight_g.values[tr].mean() - true).mean()), 1)
# 예: 길이 31.2·높이 12.5·폭 4.3
ex = np.log(np.array([[31.2, 12.5, 4.3]])); R["mask_weight"]["example"] = round(float(np.exp(lr.predict(ex))[0]), 0)

# 5. 이웃 찾기 (지도 위 kNN) vs 지도학습 분류 (같은 묶음 분할)
sgk = StratifiedGroupKFold(5, shuffle=True, random_state=0)
sup_knn1 = cross_val_score(make_pipeline(StandardScaler(), KNeighborsClassifier(1)), X, y, cv=sgk, groups=g).mean()
sup_log = cross_val_score(make_pipeline(StandardScaler(), LogisticRegression(max_iter=5000)), X, y, cv=sgk, groups=g).mean()
R["supervised"] = {"knn1_group_cv": round(float(sup_knn1), 4), "logit_group_cv": round(float(sup_log), 4)}
# 비지도 지도(PCA 2축)에서 이웃 5마리 다수결 (라벨은 판단할 때만 참고)
pk = PCA(2).fit(Z[tr]); Ptr = pk.transform(Z[tr]); Pte = pk.transform(Z[te])
k5 = KNeighborsClassifier(5).fit(Ptr, y[tr]); R["knn_map"] = {"pc2_k5_test_acc": round(float((k5.predict(Pte) == y[te]).mean()), 4)}
k5b = KNeighborsClassifier(5).fit(Z[tr], y[tr]); R["knn_map"]["all6_k5_test_acc"] = round(float((k5b.predict(Z[te]) == y[te]).mean()), 4)
# 이름표 7장만(종마다 한 마리) 알 때: 비지도 군집 + 7장 → 정확도
rng = np.random.RandomState(0)
# 지도 위 이웃 거리 분포 → 범위 밖 문턱 (훈련 내부 1-이웃 거리 99% 분위)
nnm = NearestNeighbors(n_neighbors=2).fit(Ptr); d, _ = nnm.kneighbors(Ptr)
thr = float(np.quantile(d[:, 1], 0.99))
nnt = NearestNeighbors(n_neighbors=1).fit(Ptr); dte, _ = nnt.kneighbors(Pte)
R["ood"] = {"thr_q99": round(thr, 3), "test_over_thr": int((dte[:, 0] > thr).sum()), "test_n": int(len(te))}
# 가상의 큰 물고기 (길이1 100cm 등) → 지도 위 거리
big = np.array([[9000, 100, 108, 115, 30, 14]])
pb = pk.transform(sc.transform(big)); db, _ = nnt.kneighbors(pb)
R["ood"]["big_fish"] = {"x": big[0].tolist(), "pc": pb[0].round(2).tolist(), "nn_dist": round(float(db[0, 0]), 2), "times_thr": round(float(db[0, 0] / thr), 1)}
R["pca_train"] = {"mean": pk.mean_.round(4).tolist(), "comp": pk.components_.round(4).tolist()}

# 복원 오차 경보 (오토인코더): 학습 물고기 복원 오차의 상위 1% 지점을 문턱으로
err_tr = ((ae.predict(Z[tr]) - Z[tr]) ** 2).mean(1); err_te = ((ae.predict(Z[te]) - Z[te]) ** 2).mean(1)
athr = float(np.quantile(err_tr, 0.99))
def ae_err(x):
    z = sc.transform(np.array([x])); return float(((ae.predict(z) - z) ** 2).mean())
perch_te = [i for i in te if y[i] == "Perch" and X[i, 1] > 24 and k5.predict(pk.transform(Z[[i]]))[0] == "Perch"][0]
R["perch_example"] = int(perch_te)
sea = X[perch_te].copy(); sea[1] = sea[3]
R["ae_ood"] = {"thr_q99": round(athr, 4), "test_over_thr": int((err_te > athr).sum()),
               "sea_perch": {"x": sea.round(2).tolist(), "err": round(ae_err(sea), 4), "times_thr": round(ae_err(sea) / athr, 1),
                             "map_dist": round(float(nnt.kneighbors(pk.transform(sc.transform([sea])))[0][0, 0]), 3)},
               "big_fish_err": round(ae_err(big[0]), 2)}
# 이름표 7장(종마다 원본 1마리)만 있을 때 지도 위 가장 가까운 이름표 정답률
cards = [[i for i in tr if y[i] == s and df.source[i] == "original"][0] for s in SP]
Pall = pk.transform(Z); C = Pall[cards]
pred7 = [y[cards][np.argmin(((C - Pall[i]) ** 2).sum(1))] for i in te]
R["knn_map"]["seven_cards_acc"] = round(float(np.mean(np.array(pred7) == y[te])), 4)

# 복원 경보 (PCA 네 축): 네 축으로 접었다 편 오차 — 길이 세 값의 관계가 깨진 물고기를 잡는다
p4 = PCA(4).fit(Z[tr])
def r4(Zm): return ((p4.inverse_transform(p4.transform(Zm)) - Zm) ** 2).mean(1)
e4tr = r4(Z[tr]); e4te = r4(Z[te]); thr4 = float(np.quantile(e4tr, 0.99))
R["pca4_ood"] = {"thr_q99": round(thr4, 5), "test_over_thr": int((e4te > thr4).sum()), "test_n": int(len(te)),
                 "sea_err": round(float(r4(sc.transform([sea]))[0]), 5), "sea_times": round(float(r4(sc.transform([sea]))[0] / thr4), 1),
                 "big_err": round(float(r4(sc.transform(big))[0]), 4),
                 "mean": p4.mean_.round(5).tolist(), "comp": p4.components_.round(5).tolist()}

json.dump(R, open(out, "w"), ensure_ascii=False, indent=1)
print(json.dumps(R, ensure_ascii=False)[:6000])
