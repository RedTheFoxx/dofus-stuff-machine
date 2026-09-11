# Roadmap: dofus-stuff-machine

## Overview

Ce milestone est documentaire : le produit `dofus-stuff-machine` (Python 3.11+, CLI
`fetcher.py`, interface web Flask « terminal rétro », solveur ortools, base SQLite locale
`.data/dofus.sqlite3`) est **figé** ; le livrable est la documentation utilisateur en
français qui le rend utilisable sans lire le code. Le parcours traverse six phases : poser
le socle vérifiable (sommaire, installation, harnais pytest), fermer l'ancrage CLI,
documenter le flux simplifié puis le wizard avancé (en y résorbant la dette
`GUIDE_WIZARD.md`), expliquer la base locale et le mode hors-ligne, et terminer par les
filets du lecteur (dépannage, glossaire) puis la preuve que les garde-fous échouent
réellement quand une cible dérive.

Le code est la source de vérité, la documentation en est le reflet, `pytest` est le juge.
La vérification de tout le milestone s'exécute par `.venv/Scripts/python.exe -m pytest -q`,
sans exécuter `main()`, sans écrire sous `.data/` et sans ouvrir de connexion réseau.

Aucune phase ne livre d'interface : l'annotation `**UI hint**: no` est explicite sur chaque
phase, parce que la prose documentaire contient des mots (« interface », « page ») que les
outils interpréteraient sinon comme un chantier frontend.

## Phases

**Phase Numbering:**

- Integer phases (1, 2, 3): Planned milestone work
- Decimal phases (2.1, 2.2): Urgent insertions (marked with INSERTED)

Decimal phases appear between their surrounding integers in numeric order.

- [x] **Phase 1: Socle documentaire, installation et harnais vérifiable** - Le lecteur trouve la doc depuis le `README.md`, installe l'outil, lance CLI et web ; les invariants documentaires et l'ancrage au code sont vérifiés dès les deux premières pages (completed 2026-09-11)
- [ ] **Phase 2: Référence CLI alignée sur le parseur** - `docs/cli.md` documente des commandes, options et exemples réellement analysables par `fetcher.py`
- [ ] **Phase 3: Parcours simplifié documenté depuis le rendu réel** - Le flux classe → éléments → niveau, la lecture du résultat, la sauvegarde/export et les hypothèses de l'outil sont décrits tels qu'ils s'affichent
- [ ] **Phase 4: Wizard avancé et résorption de la dette `GUIDE_WIZARD`** - `docs/wizard-avance.md` devient la source unique du flux avancé, et `GUIDE_WIZARD.md` ne contredit plus le produit
- [ ] **Phase 5: Base locale, hors-ligne et resynchronisation** - Le fichier SQLite, la fenêtre de re-check 24 h, les deux défauts hors-ligne et les commandes destructrices sont expliqués sans être exécutés
- [ ] **Phase 6: Dépannage, glossaire, complétude et preuve finale** - Le lecteur cherche par message d'erreur ou par terme, la complétude est vérifiée, et la suite prouve que les garde-fous mordent

## Phase Details

### Phase 1: Socle documentaire, installation et harnais vérifiable

**Goal**: Un lecteur découvre la documentation depuis le `README.md` racine, installe l'outil et l'utilise en CLI comme en web ; les invariants documentaires et l'ancrage au code sont vérifiés par pytest dès les deux premières pages.
**Mode:** mvp
**Depends on**: Nothing (first phase)
**Requirements**: SOMM-01, SOMM-02, SOMM-03, INST-01, INST-02, INST-03, GARD-01, GARD-02
**Success Criteria** (what must be TRUE):

  1. `README.md` porte une section « Documentation utilisateur » dont la cible `docs/sommaire.md` existe sur disque (le lien est résolu par un test).
  2. `docs/sommaire.md` liste exactement les pages `docs/**/*.md` présentes, et chaque page porte un unique H1 égal à son libellé d'index, plus une ligne de retour vers le sommaire (contrôle bidirectionnel).
  3. `docs/installation.md` mène de Python 3.11+ au premier lancement CLI **et** web (`pip install -e ".[dev]"`, `.venv/Scripts/python.exe -m pytest -q`, `python -m dofus_stuff.web`, adresse par défaut) et décrit le pilotage clavier (`F7`, `F8`, `ESC`, `PageUp`, `PageDown`, champ de saisie) avant de lancer l'interface.
  4. Chaque option d'entrée web citée par la documentation est acceptée par le parseur réel, et chaque chemin `.py` d'un bloc « Source de vérité » existe sur disque (contrôles d'ancrage).
  5. Une dérive injectée dans une copie de travail de `docs/` (lien interne mort, page non listée, H1 divergent) fait échouer la suite, qui reste verte sur l'état livré — exécutée par `.venv/Scripts/python.exe -m pytest -q`, sans exécuter `main()`, sans écrire sous `.data/` et sans ouvrir de connexion réseau.

**Plans**: 4/4 plans executed
**UI hint**: no

Plans:

- [x] 01-01-PLAN.md
- [x] 01-02-PLAN.md
- [x] 01-03-PLAN.md
- [x] 01-04-PLAN.md

**Wave 1**

- [x] 01-01: Poser `docs/sommaire.md` (index unique, parcours conseillé) et la section « Documentation utilisateur » de `README.md`

**Wave 2** *(blocked on Wave 1 completion)*

- [x] 01-02: Rédiger `docs/installation.md` depuis le code réel (prérequis, installation, vérification, lancement CLI et web, pilotage clavier)

**Wave 3** *(blocked on Wave 2 completion)*

- [x] 01-03: Ajouter la fixture `docs_dir`, le helper de normalisation (testé) et `tests/test_docs_structure.py` (arbres, exhaustivité bidirectionnelle, liens relatifs, H1 ↔ libellé, UTF-8)

**Wave 4** *(blocked on Wave 3 completion)*

- [x] 01-04: Ajouter `tests/test_docs_code_anchor.py` (chemins « Source de vérité », options d'entrée web) et vérifier la suite complète

### Phase 2: Référence CLI alignée sur le parseur

**Goal**: Un lecteur dispose d'une référence `docs/cli.md` où chaque sous-commande, chaque option et chaque exemple est réellement analysable par `fetcher.py`.
**Mode:** mvp
**Depends on**: Phase 1
**Requirements**: CLI-01, CLI-02, CLI-03
**Success Criteria** (what must be TRUE):

  1. Chaque sous-commande documentée (`version`, `self-test`, `search`, `item`, `list`, `optimize`, `db` et l'alias `cache`) est analysée sans erreur par le parseur d'arguments réel (`build_parser().parse_args`).
  2. Chaque option globale documentée (`--timeout`, `--data-dir`, `--force-sync`, `--offline`) et chaque option d'`optimize` documentée est réellement acceptée par le parseur.
  3. Chaque exemple de commande de la page apparaît verbatim dans `docs/cli.md` et son découpage en arguments (`shlex`) est analysable par le parseur.
  4. L'ordre réel est illustré : au moins un exemple hors-ligne place l'option globale avant la sous-commande (`--offline optimize …`), et `db clear` n'apparaît qu'accompagné de son avertissement destructif, jamais dans un parcours recommandé.
  5. La suite reste verte avec l'interpréteur épinglé, sans exécuter `main()` ni écrire sous `.data/`.

**Plans**: 3 plans
**UI hint**: no

Plans:
**Wave 1**

- [ ] 02-01: Rédiger `docs/cli.md` (sous-commandes, options globales, options d'`optimize`, mode interactif, avertissement destructif) et son entrée d'index

**Wave 2** *(blocked on Wave 1 completion)*

- [ ] 02-02: Ajouter les contrôles d'ancrage des sous-commandes et des options documentées

**Wave 3** *(blocked on Wave 2 completion)*

- [ ] 02-03: Ajouter le contrôle bidirectionnel des exemples (présence verbatim + analyse par le parseur) et la garde « commande destructrice jamais dans un parcours »

### Phase 3: Parcours simplifié documenté depuis le rendu réel

**Goal**: Un lecteur peut dérouler le flux simplifié classe → éléments → niveau, lire son résultat et comprendre ce que l'outil suppose.
**Mode:** mvp
**Depends on**: Phase 2
**Requirements**: SIMP-01, SIMP-02, SIMP-03, SIMP-04
**Success Criteria** (what must be TRUE):

  1. Les trois questions et le libellé `AVANCE : personnaliser les réglages` sont cités tels qu'ils sont rendus, avec les entrées acceptées (nom ou numéro de classe, éléments et alias, séparateurs) et les messages d'erreur réels.
  2. Le lecteur sait lire son résultat : carte de pagination, emplacement réel de `Méthode`, `Score` et `Indice de recherche` (dernière page), et table de correspondance libellé tronqué → nom complet de slot.
  3. La sauvegarde navigateur (20 sauvegardes maximum) et l'export Dofusbook sont décrits et rattachés à l'écran qui les expose.
  4. Les hypothèses de l'outil (points par niveau, paliers PA/PM 40/100/150, heuristiques de classe, ni exo ni parchemins) et ses limites (« indice de recherche » ≠ qualité en combat, recherche sur une sélection du catalogue) sont explicites.
  5. Le contrôle détecte un numéro de menu associé au mauvais libellé (assertion négative dérivée du rendu réel) et la suite reste verte.

**Plans**: 4 plans
**UI hint**: no

Plans:

- [ ] 03-01: Rédiger `docs/parcours-simplifie.md` — les trois questions, entrées acceptées, messages d'erreur réels, `AVANCE` — et son entrée d'index
- [ ] 03-02: Ajouter la section « lire le résultat » (pagination, emplacement des diagnostics, table libellé tronqué → slot)
- [ ] 03-03: Ajouter les sections « sauvegarder et exporter », « ce que l'outil suppose » et « ce que l'outil ne fait pas »
- [ ] 03-04: Ajouter les contrôles de rendu (libellés d'étapes, menu réel, assertions négatives sur les couples numéro/libellé obsolètes)

### Phase 4: Wizard avancé et résorption de la dette `GUIDE_WIZARD`

**Goal**: Le flux avancé est décrit dans une source unique alignée sur le code, et `GUIDE_WIZARD.md` ne contredit plus le produit.
**Mode:** mvp
**Depends on**: Phase 3
**Requirements**: WIZ-01, WIZ-02, WIZ-03
**Success Criteria** (what must be TRUE):

  1. `docs/wizard-avance.md` décrit les 9 étapes dans l'ordre du code avec leurs titres réellement rendus, les slots et filtres (`F1`–`F10`, `F6` = armes distance, `F7` = armes mêlée) et les 11 options — chaque libellé retrouvé dans le rendu.
  2. Les formats d'édition de caractéristiques (4 nombres) et la syntaxe d'items (`+ID` interdit, `-ID` forcé, `!ID`, `CLEAR`) sont documentés tels que le code les applique.
  3. Les touches et commandes réellement actives (dont `GO`, `RESET`, `SAVES` et `1`–`8` au récapitulatif) sont citées et retrouvées dans le rendu.
  4. `GUIDE_WIZARD.md` ne décrit plus le wizard en entier : il aiguille vers `docs/wizard-avance.md` avec une arborescence de menus corrigée, et `README.md` ne renvoie plus vers lui pour l'usage produit.
  5. Le contrôle des renvois obsolètes est observé **rouge** sur l'état antérieur (menu `3`/`4` inversés, `F7` présenté comme armes distance, arrivée « directe » dans le wizard) **puis vert** après correction, dans la même phase.

**Plans**: 4 plans
**UI hint**: no

Plans:

- [ ] 04-01: Trancher la source unique et rédiger `docs/wizard-avance.md` (9 étapes, slots, filtres, options, formats d'édition, syntaxe d'items) et son entrée d'index
- [ ] 04-02: Ajouter les contrôles wizard depuis le rendu réel (étapes, commandes, touches, identifiants d'écrans)
- [ ] 04-03: Réduire `GUIDE_WIZARD.md` à un aiguillage corrigé et rediriger `README.md`
- [ ] 04-04: Ajouter le contrôle des renvois obsolètes, observé rouge sur l'état antérieur puis vert après correction

### Phase 5: Base locale, hors-ligne et resynchronisation

**Goal**: Un lecteur comprend la base SQLite locale, la fenêtre de resynchronisation et les deux comportements hors-ligne, et ne lance jamais une commande destructrice par inadvertance.
**Mode:** mvp
**Depends on**: Phase 4
**Requirements**: BASE-01, BASE-02, BASE-03
**Success Criteria** (what must be TRUE):

  1. `docs/base-locale.md` décrit le fichier `.data/dofus.sqlite3`, les catégories d'objets stockées et la fenêtre de re-check de 24 heures.
  2. Les deux défauts hors-ligne sont distingués explicitement (web hors-ligne par défaut, CLI en ligne par défaut donc `--offline` requis) et les champs affichés par l'état de la base sont décrits par leurs noms, sans aucune valeur volatile.
  3. Les cas non évidents sont couverts : `db status` crée le fichier s'il n'existe pas, `db sync` refuse `--offline`, l'écran web de synchronisation contacte l'API même en mode hors-ligne.
  4. Les commandes destructrices (`db clear`, `PURGE OUI`) sont signalées comme telles sur la même ligne et n'apparaissent dans aucun parcours ; les contrôles de la phase n'écrivent pas sous `.data/`, n'exécutent aucune synchronisation et n'ouvrent aucune connexion réseau.
  5. Chaque nom de champ ou de commande cité par la page est produit par le code, et la suite reste verte avec l'interpréteur épinglé.

**Plans**: 3 plans
**UI hint**: no

Plans:

- [ ] 05-01: Rédiger `docs/base-locale.md` (fichier, catégories, fenêtre 24 h, deux défauts hors-ligne, champs de l'état de la base) et son entrée d'index
- [ ] 05-02: Couvrir les cas non évidents (création du fichier par `db status`, `db sync` refusé avec `--offline`, synchro web qui contacte l'API) et les avertissements destructifs sur la même ligne
- [ ] 05-03: Ajouter les contrôles d'ancrage de la page base locale (noms de champs produits par le code, aucun accès `.data/`, aucun réseau)

### Phase 6: Dépannage, glossaire, complétude et preuve finale

**Goal**: Le lecteur trouve une réponse en cherchant par message d'erreur ou par terme, et la documentation livrée est prouvée complète, non destructive et gardée par des contrôles qui échouent réellement quand une cible dérive.
**Mode:** mvp
**Depends on**: Phase 5
**Requirements**: AIDE-01, AIDE-02, GARD-03, GARD-04
**Success Criteria** (what must be TRUE):

  1. `docs/depannage.md` permet de retrouver chaque rubrique par le message réellement produit (base absente ou vide, saisie invalide, calcul long, clavier inactif, résultat paginé) — contrôle message → rubrique.
  2. `docs/glossaire.md` définit le vocabulaire du produit et de la documentation, chaque entrée citée étant réellement présente et triée.
  3. Les 8 pages épinglées sont toutes livrées, l'ensemble des fichiers de `docs/` est exactement celui attendu (toute page en trop fait échouer la suite) et le sommaire propose un parcours conseillé final.
  4. Un test de mutation (copie de `docs/` sous `tmp_path` avec dérive injectée) prouve que le harnais échoue réellement : complétude, ancrage de libellé et renvois obsolètes sont détectés.
  5. La vérification finale s'exécute par `.venv/Scripts/python.exe -m pytest -q` (compteur et durée réels cités), `.data/` est inchangée (empreinte ou mtime), aucune connexion réseau n'est ouverte, `main()` n'est jamais exécuté, et `git status` ne montre que `docs/`, `README.md`, `GUIDE_WIZARD.md` et `tests/`.

**Plans**: 4 plans
**UI hint**: no

Plans:

- [ ] 06-01: Rédiger `docs/depannage.md` indexé par message d'erreur réel, avec son entrée d'index et son contrôle message → rubrique
- [ ] 06-02: Rédiger `docs/glossaire.md`, son entrée d'index, son contrôle d'entrées, et le parcours conseillé final du sommaire
- [ ] 06-03: Ajouter le contrôle de complétude (liste épinglée des 8 pages et ensemble exact des fichiers de `docs/`)
- [ ] 06-04: Ajouter la preuve du harnais (test de mutation), le contrôle d'intégrité de `.data/`, l'audit de périmètre `git status` et l'exécution finale verte avec compteur et durée réels

## Progress

**Execution Order:**
Phases execute in numeric order: 1 → 2 → 3 → 4 → 5 → 6

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Socle documentaire, installation et harnais vérifiable | 4/4 | Complete    | 2026-09-11 |
| 2. Référence CLI alignée sur le parseur | 0/3 | Not started | - |
| 3. Parcours simplifié documenté depuis le rendu réel | 0/4 | Not started | - |
| 4. Wizard avancé et résorption de la dette GUIDE_WIZARD | 0/4 | Not started | - |
| 5. Base locale, hors-ligne et resynchronisation | 0/3 | Not started | - |
| 6. Dépannage, glossaire, complétude et preuve finale | 0/4 | Not started | - |
