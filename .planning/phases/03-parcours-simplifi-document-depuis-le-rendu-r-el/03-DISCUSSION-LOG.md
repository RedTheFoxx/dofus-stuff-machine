# Phase 3 - Journal de discussion

**Date :** 2026-09-11
**Commande :** `discuss-phase 3`
**Référence humaine uniquement** — non consommé par la recherche, la planification ni l'exécution.

## Zones grises présentées

Les quatre zones proposées ont toutes été retenues.

| # | Zone grise | Retenue |
|---|-----------|---------|
| 1 | Source du rendu réel | oui |
| 2 | Périmètre de la page | oui |
| 3 | Hypothèses & limites (critère 4) | oui |
| 4 | Frontière phases 4 et 5 | oui |

## Résolutions

### 1. Source du rendu réel
- Écrans web → **client de test Flask en processus** (patron `tests/test_recommend.py`), hors-ligne, aucune écriture sous `.data/`.
- Questions guidées CLI → libellés **lus dans leur module source** et ancrés par test, car D-15 interdit d'exécuter `main()`.
- Assertion négative du critère 5 → dérivée de la **correspondance réellement rendue** numéro ↔ libellé, donc de la même source que les libellés positifs.
- Une sous-commande ou un écran dont le libellé n'est pas lisible ne donne lieu à **aucune affirmation** (D-19).
- Décisions : D-32, D-33, D-34, D-35.

### 2. Périmètre de la page
- La page décrit le parcours guidé tel que le lecteur le vit ; les **écrans web sont la référence de rendu**, le parcours CLI est mentionné sans être redupliqué.
- La **surface de commandes reste dans `docs/cli.md`** ; renvoi en prose, pas de recopie (D-17 appliqué entre deux pages).
- « Lire le résultat » et « Sauvegarder et exporter » sont des **sections de cette page** : les reporter laisserait le critère 3 sans support.
- `docs/sommaire.md` gagne son entrée à cette phase (D-05) ; `README.md` garde son lien unique vers le sommaire (D-10, D-29).
- Décisions : D-36, D-37, D-38, D-39.

### 3. Hypothèses & limites
- Chaque hypothèse (points par niveau, paliers PA/PM, heuristiques de classe, ni exo ni parchemins) porte la **valeur réellement présente dans le code**, contrôlée par test.
- Une limite non adossée à du code lisible est **retirée** ou explicitement présentée comme **interprétation du parcours lecteur** — jamais comme vérité de code.
- Aucune constante écrite de mémoire ; message d'échec citant page + valeur attendue + fichier de code (D-13).
- Décisions : D-40, D-41, D-42.

### 4. Frontière phases 4 et 5
- Aucune re-description des écrans du wizard avancé (phase 4) ni du fonctionnement de la base locale (phase 5) — D-17.
- Renvoi **en prose sans lien** tant que la cible n'existe pas ; le lien est ajouté par la phase qui crée la page cible, dans le même commit que la cible (D-44).
- Décisions : D-43, D-44.

### Conventions
- D-45 : conventions des phases 1 et 2 réappliquées (D-01, D-11 à D-15).

## Rappels du porteur de projet maintenus

Documentation en français ; vérification par pytest réellement exécuté ; aucun compteur, durée ni résultat de test inventé ; aucune validation humaine inventée ; hors-ligne d'abord sur `.data/dofus.sqlite3` ; aucune publication ni déploiement distant ; commits locaux uniquement avec `git add` par chemin explicite ; aucun `db clear`, drop SQLite ni suppression sous `.data/` ; aucune modification de `dofus_stuff/**` pour aligner la doc.

## Suite

Recherche de la phase 3, puis plans.
