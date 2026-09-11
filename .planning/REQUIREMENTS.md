# Requirements: dofus-stuff-machine — Documentation utilisateur

**Defined:** 2026-09-10
**Core Value:** Un utilisateur qui n'a jamais vu le projet peut installer l'outil, lancer le flux simplifié classe → éléments → niveau, lire son résultat et retrouver chaque commande/menu cité dans le code réel — sans lire le code et sans rencontrer de documentation périmée.

## v1 Requirements

Exigences de la livraison initiale. Chacune est mappée à exactement une phase du roadmap.

**Mode projet :** MVP vertical — chaque phase livre un document de bout en bout *et* ses contrôles automatisés.

**Provenance :** les identifiants sont granulaires pour permettre un mapping 1:1 avec les phases. La colonne « Dérivé de » relie chaque exigence aux hypothèses DOCS-01…DOCS-12 de `PROJECT.md`.

### Socle documentaire et accès

- [x] **SOMM-01** : Un lecteur trouve le sommaire de la documentation depuis le `README.md` racine — dérivé de DOCS-01, DOCS-02
- [x] **SOMM-02** : Chaque page livrée sous `docs/` est listée dans `docs/sommaire.md`, et réciproquement — dérivé de DOCS-01
- [x] **SOMM-03** : Chaque page `docs/` porte un unique titre H1 égal à son libellé d'index et une ligne de retour vers le sommaire — dérivé de DOCS-01

### Installation et démarrage

- [x] **INST-01** : Un lecteur peut installer l'outil (Python 3.11+, `pip install -e ".[dev]"`) puis vérifier son installation sans lire le code — dérivé de DOCS-03
- [x] **INST-02** : Un lecteur peut démarrer l'interface web et sait dans quel mode elle démarre (hors-ligne par défaut) et sur quelle adresse — dérivé de DOCS-03
- [x] **INST-03** : Un lecteur comprend que l'interface web se pilote au clavier (champ de saisie, F7/F8/ESC/PageUp/PageDown) avant de la lancer — dérivé de DOCS-03

### Flux simplifié (cœur de la valeur produit)

- [x] **SIMP-01** : Un lecteur peut ouvrir l'optimisation depuis le menu réel et dérouler les trois questions (classe → éléments → niveau), avec les entrées acceptées et les messages d'erreur réels — dérivé de DOCS-04
- [x] **SIMP-02** : Un lecteur peut lire son résultat : pagination, emplacement réel des informations de calcul, correspondance des libellés abrégés à l'écran — dérivé de DOCS-04
- [x] **SIMP-03** : Un lecteur peut sauvegarder un stuff dans son navigateur et l'exporter vers Dofusbook — dérivé de DOCS-04
- [x] **SIMP-04** : Un lecteur sait ce que l'outil suppose (répartition des points, paliers, heuristiques) et ce qu'il ne fait pas — dérivé de DOCS-04

### Flux avancé (wizard)

- [x] **WIZ-01** : Un lecteur peut parcourir les étapes du wizard, éditer les formats de caractéristiques et utiliser la syntaxe d'items interdits/forcés — dérivé de DOCS-05
- [ ] **WIZ-02** : Un lecteur connaît les commandes et les touches réellement actives du wizard — dérivé de DOCS-05
- [ ] **WIZ-03** : `GUIDE_WIZARD.md` ne contredit plus le code : contenu migré vers `docs/wizard-avance.md` comme source unique, fichier racine réduit à un aiguillage corrigé, `README.md` redirigé — dérivé de DOCS-10

### Référence CLI

- [x] **CLI-01** : Chaque sous-commande documentée de `fetcher.py` est réellement analysable par le parseur d'arguments du code — dérivé de DOCS-06
- [x] **CLI-02** : Chaque option globale et chaque option d'optimisation documentée est réellement analysable par le parseur — dérivé de DOCS-06
- [x] **CLI-03** : Chaque exemple de commande cité dans `docs/cli.md` est analysable et apparaît verbatim dans la page — dérivé de DOCS-06

### Base locale et hors-ligne

- [ ] **BASE-01** : Un lecteur comprend le fichier de base locale, les catégories d'objets stockées et la fenêtre de resynchronisation — dérivé de DOCS-07
- [ ] **BASE-02** : Un lecteur comprend les deux comportements hors-ligne (web hors-ligne par défaut ; CLI en ligne par défaut, donc option requise) et les champs affichés par l'état de la base — dérivé de DOCS-07
- [ ] **BASE-03** : Les commandes destructrices de la base sont signalées comme telles et jamais présentées comme une étape normale — dérivé de DOCS-07

### Aide et vocabulaire

- [ ] **AIDE-01** : Un lecteur trouve une rubrique de dépannage en cherchant par message d'erreur réel — dérivé de DOCS-08
- [ ] **AIDE-02** : Un lecteur trouve un glossaire du vocabulaire employé par l'outil et par la documentation — dérivé de DOCS-09

### Garde-fous automatiques

- [x] **GARD-01** : La suite pytest échoue si un lien interne de `docs/` ne se résout pas, si le sommaire diverge de l'ensemble des pages, ou si un renvoi obsolète réapparaît — dérivé de DOCS-11
- [x] **GARD-02** : La suite pytest échoue si un libellé de flux ou d'étape du wizard cité dans la documentation n'est plus produit par le code — dérivé de DOCS-12
- [ ] **GARD-03** : La complétude est un critère de sortie vérifié après livraison des pages, et un test de mutation prouve que le harnais détecte réellement une dérive — dérivé de DOCS-11, DOCS-12
- [ ] **GARD-04** : La vérification s'exécute avec `.venv/Scripts/python.exe -m pytest -q`, sans écrire sous `.data/`, sans exécuter `main()` et sans ouvrir de connexion réseau — dérivé de DOCS-11, DOCS-12

## v2 Requirements

Reportées à une livraison ultérieure. Suivies mais hors roadmap actuel.

### Contenu

- **DOC2-01** : Documentation d'architecture interne du produit
- **DOC2-02** : Guide de contribution (workflow de développement, conventions de code)
- **DOC2-03** : Captures d'écran et illustrations de l'interface terminal
- **DOC2-04** : Page dédiée « lire le résultat » et « sauvegardes / export » (aujourd'hui des sections du parcours simplifié)

### Outillage

- **OUT2-01** : Génération d'un site statique (MkDocs ou Sphinx) depuis `docs/`
- **OUT2-02** : Vérificateur de liens externes (le contrôle actuel ne couvre que les liens internes)
- **OUT2-03** : Intégration continue exécutant la suite de tests à chaque changement

### Internationalisation

- **I18N-01** : Traduction de la documentation vers une autre langue que le français

## Out of Scope

Explicitement exclu. Documenté pour empêcher la réintroduction par glissement.

| Feature | Reason |
|---------|--------|
| Modification de `dofus_stuff/**` pour aligner la doc | Le code est la source de vérité ; une doc qui oblige à changer le produit sort du besoin initial |
| Refonte de l'interface web ou du solveur | Le besoin est strictement documentaire |
| Documentation d'architecture interne et guide de contribution | Public visé = « Utilisateur + dev », pas « Développeur » |
| Site statique généré (MkDocs, Sphinx) | Dépendance et outillage supplémentaires sans nécessité démontrée |
| Vérificateur de liens tiers (`linkcheck`, `markdown-link-check`) | Le contrôle des liens internes est faisable avec la bibliothèque standard déjà présente |
| Traduction de la documentation | Le besoin est explicitement « en Français » |
| Publication ou déploiement distant (site, paquet, PR publiée) | Interdit par les règles du projet |
| Exécution de `db clear` / `db sync`, drop SQLite, suppression sous `.data/` | Interdit par les règles du projet ; les commandes destructrices sont documentées, jamais exécutées |
| Relance de l'outillage documentaire antérieur (`doc-agent.toml`, `.doc-agent/`) | Écrivain non contrôlé ciblant `docs/` ; il peut fabriquer commandes et écrans inexistants |
| Suppression de `.doc-agent/`, `doc-agent.toml` ou des fichiers GSD à la racine | Aucune suppression de données autorisée ; ces fichiers restent en place, non suivis |
| Documentation de l'outillage documentaire ou de son endpoint local | Hors sujet utilisateur ; `docs/` appartient exclusivement à ce milestone |
| Valeurs volatiles dans la prose (nombre d'objets, version de jeu, horodatages) | Se périme à chaque synchronisation ; la doc décrit les formats, les commandes produisent les chiffres |

## Traceability

Rempli lors de la création du roadmap (6 phases). Chaque exigence v1 est mappée à exactement une phase.

| Requirement | Phase | Status |
|-------------|-------|--------|
| SOMM-01 | Phase 1 | Complete |
| SOMM-02 | Phase 1 | Complete |
| SOMM-03 | Phase 1 | Complete |
| INST-01 | Phase 1 | Complete |
| INST-02 | Phase 1 | Complete |
| INST-03 | Phase 1 | Complete |
| SIMP-01 | Phase 3 | Complete |
| SIMP-02 | Phase 3 | Complete |
| SIMP-03 | Phase 3 | Complete |
| SIMP-04 | Phase 3 | Complete |
| WIZ-01 | Phase 4 | Complete |
| WIZ-02 | Phase 4 | Pending |
| WIZ-03 | Phase 4 | Pending |
| CLI-01 | Phase 2 | Complete |
| CLI-02 | Phase 2 | Complete |
| CLI-03 | Phase 2 | Complete |
| BASE-01 | Phase 5 | Pending |
| BASE-02 | Phase 5 | Pending |
| BASE-03 | Phase 5 | Pending |
| AIDE-01 | Phase 6 | Pending |
| AIDE-02 | Phase 6 | Pending |
| GARD-01 | Phase 1 | Complete |
| GARD-02 | Phase 1 | Complete |
| GARD-03 | Phase 6 | Pending |
| GARD-04 | Phase 6 | Pending |

**Coverage:**

- v1 requirements : 25 total
- Mapped to phases : 25 ✓
- Unmapped : 0 ✓

**Répartition par phase :**

| Phase | Exigences | Total |
|-------|-----------|-------|
| Phase 1 — Socle documentaire, installation et harnais vérifiable | SOMM-01, SOMM-02, SOMM-03, INST-01, INST-02, INST-03, GARD-01, GARD-02 | 8 |
| Phase 2 — Référence CLI alignée sur le parseur | CLI-01, CLI-02, CLI-03 | 3 |
| Phase 3 — Parcours simplifié documenté depuis le rendu réel | SIMP-01, SIMP-02, SIMP-03, SIMP-04 | 4 |
| Phase 4 — Wizard avancé et résorption de la dette `GUIDE_WIZARD` | WIZ-01, WIZ-02, WIZ-03 | 3 |
| Phase 5 — Base locale, hors-ligne et resynchronisation | BASE-01, BASE-02, BASE-03 | 3 |
| Phase 6 — Dépannage, glossaire, complétude et preuve finale | AIDE-01, AIDE-02, GARD-03, GARD-04 | 4 |

Aucune exigence n'est dupliquée entre deux phases : la propriété de chaque contrôle appartient à la
phase qui l'introduit (les phases suivantes l'étendent sans le réclamer).

---
*Requirements defined: 2026-09-10*
*Last updated: 2026-09-10 after roadmap creation (traceability filled, coverage 25/25)*
