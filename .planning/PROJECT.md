# dofus-stuff-machine — Documentation utilisateur

## What This Is

`dofus-stuff-machine` est un outil Python qui aide les joueurs de Dofus à constituer
une panoplie (un « stuff ») : base locale Dofusdude en SQLite, catalogue en mémoire,
CLI `fetcher.py`, interface web type terminal rétro (Flask) et solveur ortools.

Ce projet-ci ne modifie pas ces fonctionnalités : il livre la **documentation
user-friendly en français** qui manque au produit — un ensemble `docs/` clair,
exact et vérifié automatiquement, destiné d'abord au joueur qui veut un stuff,
avec des sections techniques identifiées (CLI, base locale, dépannage).

## Core Value

Un utilisateur qui n'a jamais vu le projet peut installer l'outil, lancer le flux
simplifié **classe → éléments → niveau**, lire son résultat et retrouver chaque
commande/menu cité dans le code réel — sans lire le code et sans rencontrer de
documentation périmée.

## Requirements

### Validated

Capacités déjà livrées par le code existant (état vérifié à l'initialisation,
utilisées comme source de vérité pour la documentation) :

- ✓ Base locale Dofusdude en SQLite (`.data/dofus.sqlite3`) + catalogue en mémoire — existing
- ✓ CLI `fetcher.py` : `version`, `search`, `item`, `list`, `self-test`, `db status|sync`, `optimize` — existing
- ✓ Options globales CLI : `--timeout`, `--data-dir`, `--force-sync`, `--offline` — existing
- ✓ Interface web Flask type terminal rétro (`python -m dofus_stuff.web`, port 5000 par défaut) — existing
- ✓ Menu web : recherche d'objets, liste des équipements, panoplies, optimisation, système — existing
- ✓ Flux simplifié d'optimisation en trois questions (classe → éléments → niveau) — existing (`1d475f9`)
- ✓ Flux avancé (wizard) : slots/filtres, options solveur, caractéristiques, PA/PM/PO, résistances, dommages, divers, items interdits/forcés, récapitulatif — existing
- ✓ Solveur ortools CP-SAT + recherche locale, score partagé, préfiltrage par caractéristique — existing
- ✓ Sauvegardes locales de stuffs dans le navigateur (localStorage) et export Dofusbook — existing
- ✓ Suite de tests pytest (`tests/`) — existing
- ✓ DOCS-06 : Les commandes et options CLI documentées existent réellement dans le parsing d'arguments (`docs/cli.md`, 8 sous-commandes, 4 options globales, 30 options d'`optimize`, exemples analysés par `shlex` + `parse_args`) — Phase 2

### Active

Hypothèses à valider par la livraison :

- [ ] DOCS-01 : Un `docs/` français existe avec un sommaire qui référence chaque document livré
- [ ] DOCS-02 : Le `README.md` racine renvoie vers le sommaire `docs/` pour l'usage produit
- [ ] DOCS-03 : Une page d'installation & démarrage permet d'aller de Python 3.11+ jusqu'au premier lancement (CLI et web)
- [ ] DOCS-04 : Le flux simplifié classe → éléments → niveau est décrit tel qu'il existe réellement dans le code
- [ ] DOCS-05 : Le flux avancé (wizard) est décrit écran par écran, aligné sur les libellés et écrans réels
- [ ] DOCS-07 : La base locale et la fenêtre de resynchronisation 24 h sont expliquées, en mode hors-ligne par défaut
- [ ] DOCS-08 : Une FAQ / dépannage couvre les erreurs courantes (base absente, saisie invalide, calcul long, clavier inactif)
- [ ] DOCS-09 : Un glossaire définit le vocabulaire Dofus/tooling utilisé par la doc
- [ ] DOCS-10 : `GUIDE_WIZARD.md` est corrigé là où il décrit l'ancienne arborescence de menus
- [ ] DOCS-11 : Des tests pytest vérifient l'intégrité documentaire (liens internes résolus, sommaire exhaustif et cohérent, absence de renvois obsolètes)
- [ ] DOCS-12 : Des tests pytest vérifient l'ancrage au code (commandes/options CLI présentes dans le parsing ; libellés de flux et d'étapes wizard présents dans les routes/templates Flask)

### Out of Scope

- Refonte de l'interface web ou du solveur — le besoin est documentaire, pas fonctionnel
- Documentation d'architecture interne et guide de contribution — le public visé est « Utilisateur + dev », pas « Développeur »
- Site statique généré (MkDocs, Sphinx) — outillage et dépendance supplémentaires sans nécessité démontrée
- Traductions de la documentation en d'autres langues — le besoin est explicitement « en Français »
- Publication ou déploiement distant (site, PyPI, PR publiée) — interdits par les règles du projet

## Context

- **Produit existant, brownfield** : package `dofus_stuff` (Python ≥ 3.11), CLI `fetcher.py`,
  web Flask, solveur ortools, base SQLite Dofusdude sous `.data/`, tests pytest.
- **Documentation existante** : `README.md` (français, orienté technique, plutôt à jour) et
  `GUIDE_WIZARD.md` (français, détaillé, mais **périmé** : il décrit encore une arborescence
  de menus antérieure au flux simplifié introduit par `1d475f9`). Aucun dossier `docs/`.
- **Désynchronisation constatée** : le guide wizard renvoie à `3. OPTIMISATION DE STUFF`
  alors que le menu principal en compte quatre entrées et que l'optimisation ouvre désormais
  un parcours en trois questions (classe → éléments → niveau).
- **Mode hors-ligne d'abord** : la base locale `.data/dofus.sqlite3` suffit ; la resynchronisation
  Dofusdude n'est déclenchée que si le besoin l'exige.
- **Historique** : 10 commits, dernier en date `1d475f9` (flux simplifié de recommandation).

## Constraints

- **Technique** : Python 3.11+, package `dofus_stuff`, pytest comme seul outillage de vérification — pas de nouvelle dépendance pour la documentation.
- **Langue** : documentation intégralement en français ; le code, les chemins et les identifiants techniques restent inchangés.
- **Données** : lecture seule sur `.data/` — jamais de `db clear`, de drop SQLite ni de suppression sous `.data/`.
- **Réseau** : mode hors-ligne par défaut ; aucune resynchronisation Dofusdude sauf nécessité démontrée ; aucune publication ni déploiement distant.
- **Vérification** : les critères de « fait » doivent être prouvés par des tests pytest réellement exécutés — aucune validation manuelle ni résultat inventé.
- **Périmètre** : strictement documentaire, limité au besoin initial ; pas de nouveau milestone après livraison.

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Sauter la cartographie de codebase | Package petit et lisible ; la doc exige déjà de lire le code réel ; la carte serait un artefact intermédiaire redondant | — Pending |
| Public « Utilisateur + dev » | Le cœur est le parcours guidé du joueur ; les sections techniques restent identifiables sans ouvrir la doc de contribution | — Pending |
| Périmètre « Produit complet » | L'utilisateur doit aller de l'installation au stuff obtenu sans quitter la doc (les trous seraient les premiers points de blocage) | — Pending |
| Livrable `docs/` multi-fichiers | Granularité adaptée aux 8 thèmes, liens internes et sommaire vérifiables automatiquement, aucune dépendance ajoutée | — Pending |
| Vérification par tests pytest | Remplace la relecture manuelle par un contrôle reproductible — traite la cause de la désynchronisation constatée | — Pending |
| Mode YOLO, granularité Standard, exécution Parallèle | Besoin borné et sans action destructrice ; 5-8 phases couvrent les 8 thèmes ; seuls les fichiers pivots restent séquencés | — Pending |
| Recherche / Plan Check / Verifier activés | Le risque dominant est de documenter un produit imaginaire ; ces agents lisent la source de vérité avant et après | — Pending |
| Modèles « adaptatif » | Les rôles lourds (recherche, plan, vérification) doivent lire réellement le code ; les tâches légères restent économiques | — Pending |
| Sections PR : User Stories + Risques & Dépendances | Récits et critères d'acceptation = tests prévus ; risques/dépendances = désynchronisation et fichiers pivots partagés | — Pending |
| Pas de validation par parties prenantes dans les PR | Aucune validation humaine ne peut être automatisée ni inventée ; un contrôle automatique prouve le même critère | — Pending |
| L'ancrage documentaire dérive sa vérité du parseur à l'exécution, jamais d'une liste recopiée | Une liste recopiée se périme en même temps que la page : les sondes d'argv et `format_help()` restent vrais après tout renommage d'option | ✓ Appliqué en phase 2 (contrôle strict par nom exact ajouté après revue, commit `a650032`) |
| Une section par sous-commande plutôt que la table récapitulative unique de `CLAUDE.md` §2 (DOCS-06) | Les décisions D-16/D-17 gouvernent la phase ; la substance de DOCS-06 est tenue section par section ; une table unique serait un second référentiel à maintenir | ✓ Écart assumé, consigné dans `WINDOWS.md` (02-01, id 2) |
| Un écran de contrôle (batterie de mutations) doit être exécutable sur une implémentation correcte | Une batterie qui échoue sur une page correcte rend la phase inexécutable ; les constats sont donc accumulés puis assertés une seule fois, pour que chaque motif attribué reste atteignable | ✓ Appliqué en phase 2 (19/19 mutations, revue de plan itérée 3 fois) |
| La revue de code d'une phase de documentation se juge sur le harnais, pas sur la page | Le livrable était exact (37/37 valeurs par défaut vérifiées) ; les 5 avertissements portaient tous sur les tests, et deux d'entre eux (faux positif `--help`, garde absente sur `db sync`/`cache fill`) étaient de vrais défauts de sûreté ou d'usage | ✓ Corrigés et re-mesurés (commit `a650032`), suite 169 passed |

## Evolution

This document evolves at phase transitions and milestone boundaries.

**After each phase transition** (via `/gsd-transition`):
1. Requirements invalidated? → Move to Out of Scope with reason
2. Requirements validated? → Move to Validated with phase reference
3. New requirements emerged? → Add to Active
4. Decisions to log? → Add to Key Decisions
5. "What This Is" still accurate? → Update if drifted

**After each milestone** (via `/gsd:complete-milestone`):
1. Full review of all sections
2. Core Value check — still the right priority?
3. Audit Out of Scope — reasons still valid?
4. Update Context with current state

---
*Last updated: 2026-09-11 after Phase 2 (Référence CLI alignée sur le parseur)*
