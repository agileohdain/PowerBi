#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extracteur canonique  donnees.xlsx  ->  bloc DATA JavaScript (grain MENSUEL).

Pourquoi ce script existe
-------------------------
Le skill `powerbi-prototype` embarque les données DANS le HTML (grain mensuel +
séries par dimension + masques d'activité + dimensions statiques) pour rendre les
filtres fonctionnels et la variation vs N-1 possibles. Dériver ce modèle « à la
main » depuis l'Excel mène à des KPI mal interprétés et à des dimensions oubliées
(ex. `USURE_STATUT`, `VILLE_CYCLISTES`). Ce script produit le bloc DATA complet et
canonique ; la maquette l'embarque tel quel (jamais un sous-ensemble).

Schéma attendu (style VELOH) :
  DIM_UTILISATEUR(ID_Utilisateur, Nom, Prenom, Pays, Ville, Email)
  DIM_VELO(ID_Velo, Marque, Modele, Annee_Sortie)
  ASSOC_UTILISATEUR_VELO(ID_UTILISATEUR_VELO, ID_Utilisateur, ID_Velo)
  DIM_COMPOSANT(ID_Composant, ID_UTILISATEUR_VELO, Nom_Composant, ...)
  FAIT_SORTIES(ID_Sortie, ID_UTILISATEUR_VELO, DATE_HEURE, DATE, NB_KM, MINUTES)
  FAIT_USURE_COMPOSANT(ID_Composant, ..., Statut_Alerte, ...)

Pour un autre schéma : adapter `load()` puis réémettre les mêmes identifiants.

Usage :
  python extract-data.py clients/<client>/donnees.xlsx
Sortie : le bloc `const ... = ...;` sur stdout (à copier dans le <script> de la
maquette), et un récapitulatif sur stderr.

Dépendance : openpyxl  (pip install openpyxl)
"""
import sys
import json
from collections import defaultdict, Counter

try:
    import openpyxl
except ImportError:
    sys.stderr.write("ERREUR: openpyxl manquant -> pip install openpyxl\n")
    sys.exit(2)


def load(path):
    wb = openpyxl.load_workbook(path, data_only=True)

    def rows(name):
        ws = wb[name]
        it = ws.iter_rows(values_only=True)
        hdr = next(it)
        return [dict(zip(hdr, r)) for r in it if any(v is not None for v in r)]

    return {n: rows(n) for n in wb.sheetnames}


def month_index(dates):
    """Grain mensuel continu du 1er au dernier mois présent dans les faits."""
    ym = sorted({(d.year, d.month) for d in dates})
    (y0, m0), (y1, m1) = ym[0], ym[-1]
    months = []
    y, m = y0, m0
    while (y, m) <= (y1, m1):
        months.append((y, m))
        y, m = (y + 1, 1) if m == 12 else (y, m + 1)
    return months, {t: i for i, t in enumerate(months)}


def main(path):
    data = load(path)
    users = data.get("DIM_UTILISATEUR", [])
    velos = data.get("DIM_VELO", [])
    assoc = data.get("ASSOC_UTILISATEUR_VELO", [])
    sorties = data.get("FAIT_SORTIES", [])
    usure = data.get("FAIT_USURE_COMPOSANT", [])
    if not sorties:
        sys.stderr.write("ERREUR: FAIT_SORTIES vide ou absent.\n")
        sys.exit(1)

    dates = [r["DATE"] for r in sorties if r.get("DATE")]
    months, idx = month_index(dates)
    N = len(months)

    uvel_velo = {int(a["ID_UTILISATEUR_VELO"]): int(a["ID_Velo"]) for a in assoc}
    uvel_uid = {int(a["ID_UTILISATEUR_VELO"]): int(a["ID_Utilisateur"]) for a in assoc}
    velo_marque = {int(v["ID_Velo"]): v["Marque"] for v in velos}
    uid_pays = {int(u["ID_Utilisateur"]): u["Pays"] for u in users}
    uid_ville = {int(u["ID_Utilisateur"]): u["Ville"] for u in users}

    KM = [0.0] * N
    RIDES = [0] * N
    MINUTES = [0.0] * N
    active = [set() for _ in range(N)]
    KM_PAYS = defaultdict(lambda: [0.0] * N)
    RIDES_PAYS = defaultdict(lambda: [0] * N)
    KM_MARQUE = defaultdict(lambda: [0.0] * N)
    KM_VILLE = defaultdict(lambda: [0.0] * N)

    for r in sorties:
        d = r.get("DATE")
        if not d:
            continue
        i = idx[(d.year, d.month)]
        km = float(r.get("NB_KM") or 0)
        mn = float(r.get("MINUTES") or 0)
        KM[i] += km
        RIDES[i] += 1
        MINUTES[i] += mn
        uvel = int(r["ID_UTILISATEUR_VELO"])
        uid = uvel_uid.get(uvel)
        velo = uvel_velo.get(uvel)
        if uid:
            active[i].add(uid)
            KM_PAYS[uid_pays[uid]][i] += km
            RIDES_PAYS[uid_pays[uid]][i] += 1
            KM_VILLE[uid_ville[uid]][i] += km
        if velo:
            KM_MARQUE[velo_marque[velo]][i] += km

    rnd = lambda arr: [round(x, 1) for x in arr]
    KM = rnd(KM)
    MINUTES = rnd(MINUTES)
    for d in (KM_PAYS, KM_MARQUE, KM_VILLE):
        for k in d:
            d[k] = rnd(d[k])

    # Masques d'activité par cycliste (bit i = actif au mois i). Les cyclistes
    # sans aucune sortie (masque 0) sont omis : ils comptent pour 0.
    USER_MASKS = {}
    for uid in sorted(uid_pays):
        mask = 0
        for i in range(N):
            if uid in active[i]:
                mask |= (1 << i)
        if mask:
            USER_MASKS[uid] = mask

    PAYS_CYCLISTES = dict(sorted(Counter(uid_pays.values()).items(), key=lambda kv: -kv[1]))
    VILLE_CYCLISTES = dict(sorted(Counter(uid_ville.values()).items(), key=lambda kv: -kv[1]))
    MARQUE_VELOS = dict(sorted(Counter(v["Marque"] for v in velos).items(), key=lambda kv: -kv[1]))
    USURE_STATUT = dict(sorted(Counter(u.get("Statut_Alerte") for u in usure if u.get("Statut_Alerte")).items(),
                               key=lambda kv: -kv[1]))

    assigned_velos = {int(a["ID_Velo"]) for a in assoc}
    users_with_bike = len({int(a["ID_Utilisateur"]) for a in assoc})

    out = {
        "N": N,
        "MONTH_META": [{"year": y, "month": m, "quarter": (m - 1) // 3 + 1} for y, m in months],
        "KM_LABELS": [f"{y}-{m:02d}" for y, m in months],
        "KM": KM,
        "RIDES": RIDES,
        "MINUTES": MINUTES,
        "USER_MASKS": USER_MASKS,
        "KM_PAYS_M": dict(KM_PAYS),
        "RIDES_PAYS_M": dict(RIDES_PAYS),
        "KM_MARQUE_M": dict(KM_MARQUE),
        "KM_VILLE_M": dict(KM_VILLE),
        "PAYS_CYCLISTES": PAYS_CYCLISTES,
        "VILLE_CYCLISTES": VILLE_CYCLISTES,
        "MARQUE_VELOS": MARQUE_VELOS,
        "USURE_STATUT": USURE_STATUT,
        "NB_UTILISATEURS": len(users),
        "NB_PAYS": len(PAYS_CYCLISTES),
        "NB_VILLES": len(VILLE_CYCLISTES),
        "NB_VELOS": len(velos),
        "NB_MARQUES": len(MARQUE_VELOS),
        "ANNEE_MOY": round(sum(int(v["Annee_Sortie"]) for v in velos) / len(velos), 1) if velos else 0,
        "USERS_AVEC_VELO": users_with_bike,
        "VELOS_ATTRIBUES": len(assigned_velos),
    }

    js = "const DATA = " + json.dumps(out, ensure_ascii=False, separators=(",", ":")) + ";\n"
    sys.stdout.write(js)
    sys.stderr.write(
        "OK: {N} mois ({a}-{b}), {u} utilisateurs, {v} vélos, {m} marques, "
        "{s} sorties, usure={w}\n".format(
            N=N, a=out["KM_LABELS"][0], b=out["KM_LABELS"][-1],
            u=out["NB_UTILISATEURS"], v=out["NB_VELOS"], m=out["NB_MARQUES"],
            s=sum(RIDES), w=USURE_STATUT))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.stderr.write("usage: python extract-data.py clients/<client>/donnees.xlsx\n")
        sys.exit(2)
    main(sys.argv[1])
