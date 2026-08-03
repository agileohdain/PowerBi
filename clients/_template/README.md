# Dossier template

Copiez ce dossier pour créer un nouveau client :

```powershell
Copy-Item -Recurse clients/_template clients/<mon-client>
```

Puis :
1. Remplissez `CLIENT.md`.
2. Préparez le fond visuel (voir README.md racine du dépôt, étapes 3-4).

Fichiers produits par le skill (ne pas créer à la main) :
- `donnees.xlsx`, `DATA.md` (données fictives + glossaire)
- `bg.png` (fond exporté du .pptx)
- `maquette/index.html` (la maquette)
