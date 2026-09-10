# Project Research Summary

**Project:** `dofus-stuff-machine` — documentation utilisateur en français
**Domain:** Documentation utilisateur (FR) d'un produit brownfield **déjà livré**, vérifiée par `pytest` — pas de nouveau runtime, pas de nouveau produit
**Researched:** 2026-09-10 (HEAD `19b5c96`, dernier commit fonctionnel `1d475f9`)
**Confidence:** **HIGH** sur les faits (chaque affirmation est ancrée dans un fichier du dépôt lu **ou** dans un rendu d'écran réel obtenu hors-ligne) ; **MEDIUM** sur l'ordonnancement des phases et les arbitrages éditoriaux (jugement d'ingénierie, pas fait observable) ; **LOW/n.a.** pour toute source externe — **aucun** fournisseur web n'était joignable (`search` tous drapeaux `false` dans `.planning/config.json`, `gsd_run query websearch` → `{"available": false, "reason": "BRAVE_API_KEY not set"}`), et **aucun résultat n'a été inventé ni mis en cache**.

---

## Executive Summary

Ce milestone n'est pas un projet de logiciel : c'est un **milestone documentaire sur un produit figé**. Le produit (package Python 3.11+, CLI `fetcher.py`, web Flask « terminal rétro », solveur ortools, base SQLite Dofusdude sous `.data/`) fonctionne ; ce qui manque est la documentation qui rend ses capacités utilisables, alors que deux documents existants (`README.md`, plutôt à jour ; `GUIDE_WIZARD.md`, franchement périmé) se contredisent depuis `1d475f9`. Les quatre recherches convergent donc sur une réponse unique : **Markdown nu dans `docs/` + la bibliothèque standard Python + le `pytest` déjà installé**. Zéro dépendance nouvelle, zéro générateur de site statique, zéro vérificateur de liens tiers : `pyproject.toml` déclare déjà `pytest>=8.0` dans l'extra `dev`, `testpaths` et `pythonpath` sont configurés, et le `.venv` du dépôt fournit pytest 9.1.1. La documentation doit être *rédigée à la main depuis le code réel*, puis **relue par des tests** — pas générée.

La solution retenue est un ensemble de **8 fichiers** à plat sous `docs/` (`sommaire.md` comme index unique + `installation.md`, `parcours-simplifie.md`, `wizard-avance.md`, `cli.md`, `base-locale.md`, `depannage.md`, `glossaire.md`), une section « Documentation utilisateur » dans `README.md`, `GUIDE_WIZARD.md` réduit à un aiguillage corrigé, et **deux modules de tests** qui matérialisent la règle de sens : *le code est la source de vérité, la doc est le reflet, le test est le juge*. `tests/test_docs_structure.py` vérifie les invariants internes à la doc (liens relatifs résolus, absence de liens absolus/ancres, sommaire exhaustif dans **les deux sens**, un seul H1 par page égal à son label d'index, UTF-8 strict sans placeholder, absence de renvois obsolètes) ; `tests/test_docs_code_anchor.py` vérifie l'ancrage au code (chaque commande/option citée est réellement analysée par `build_parser().parse_args`, chaque libellé d'écran cité est réellement **rendu** par le client de test Flask, chaque chemin `.py` d'un bloc « Source de vérité » existe). Le harnais **observe** : il n'exécute jamais `main()`, ne touche jamais `.data/`, n'ouvre aucune socket.

Le risque dominant est nommé et traité partout : **documenter un produit imaginaire**. Il est déjà matérialisé dans le dépôt — `GUIDE_WIZARD.md` contient 6 affirmations fausses et 5 trous structurels (le lecteur qui tape `3` atterrit sur les panoplies et non sur l'optimisation ; « vous arrivez directement dans le wizard » est faux depuis `1d475f9` ; `F7` y désigne les armes à distance alors que le code place `arme_distance` en `F6` ; le score est annoncé sur l'écran résultat alors qu'il est en **dernière page**) — et la cause racine est mesurée : **136 tests verts, aucun ne lit un fichier de documentation**, alors que `ab1eb38` a modifié le menu web sans toucher un seul fichier de doc. Les mitigations sont structurelles, pas déclaratives : ancrage bidirectionnel (la doc ne peut ni inventer ni oublier), comparaison **normalisée** des libellés (accents/casse/apostrophes/HTML ignorés, donc pas de test affaibli « parce qu'il est trop fragile »), séparation invariant auto-ajustant / complétude (la liste épinglée des 8 pages n'arrive qu'en **dernière** phase, pour ne pas laisser la suite rouge cinq phases et détruire sa valeur de signal), et un contrôle de renvois obsolètes qui doit être **vu rouge** sur l'état antérieur avant d'être vert.

---

## Key Findings

### Recommended Stack

Markdown nu (CommonMark + GFM) + stdlib Python + le `pytest` existant. `docs/` porte la doc, `tests/` la prouve. Le rendu GitHub est un consommateur à ne pas casser (liens relatifs, titres corrects) mais **pas un outil à installer**.

**Core technologies (ce qui porte la doc) :**
- **Markdown nu dans `docs/`** — continuité de format avec `README.md`/`GUIDE_WIZARD.md`, lisible tel quel (terminal/éditeur) **et** rendu par GitHub, aucun build, aucun artefact à resynchroniser
- **stdlib `pathlib` + `re` + `unicodedata` + `shlex`** — suffit à écrire tout le vérificateur : résoudre des liens relatifs, extraire les liens/blocs, normaliser les libellés accentués, découper un exemple CLI en `argv`
- **`pytest>=8.0` (déjà déclaré ; 9.1.1 dans `.venv`)** — seul outillage de vérification admis ; les tests de doc s'ajoutent sans toucher `pyproject.toml`
- **`flask.Flask.test_client` (déjà là)** — prouve les libellés **réellement rendus** via la fixture `client` de `tests/conftest.py`, avec catalogue synthétique et `tmp_path` (jamais `.data/`)
- **`git` local uniquement** — `commit_docs: true` ; aucun push, aucune PR publiée, aucune publication

**Interpréteur de référence obligatoire :** `.venv/Scripts/python.exe -m pytest -q`. L'interpréteur ambiant de l'hôte (Python 3.14.7) n'a **pas** pytest (`No module named pytest`). Toute citation de résultat doit inclure le **compteur et la durée réels** (état actuel : `136 passed in ~1.7s`).

**Interdits d'outillage (tranché) :** MkDocs/Material, Sphinx/autodoc, mdBook/Docusaurus/VitePress, `pytest-linkcheck`/`linkchecker`/`markdown-link-check`, `markdownlint`/`prettier`/hooks `pre-commit`, toute infrastructure i18n, toute inclusion de `docs/` dans le wheel (`package-data`), toute modification de `.gitignore` pour exclure `docs/`.

### Expected Features

Une « feature » ici n'est pas un écran du produit : c'est **un document, une section ou un parcours lecteur qui ferme un trou de parcours vérifiable**. Trois critères de recevabilité : elle existe si un lecteur peut faire X sans ouvrir le code ; chaque affirmation est ancrée sur un artefact ; elle est prouvable par un test, sinon elle n'est pas livrable.

**Must have (table stakes) — le lecteur les exige, sinon il ouvre le code :**
- `docs/sommaire.md` : index unique + parcours conseillé (installation → parcours simplifié → glossaire) — DOCS-01
- `README.md` : section « Documentation utilisateur » renvoyant au sommaire, et l'ancienne ligne 59 (`GUIDE_WIZARD.md`) redirigée vers `docs/wizard-avance.md` — DOCS-02
- `docs/installation.md` : prérequis, `pip install -e ".[dev]"`, premier lancement **CLI et web**, `pytest`, `http://127.0.0.1:5000`, **et** la section « l'interface terminal : ce qu'il faut savoir avant de taper » (champ de saisie, ligne de statut `ENTREE=…`, barre de touches, `F3`/`ESC`/`F7`/`F8`, `PAGE x/y`) — sans elle le lecteur ne peut pas *taper* — DOCS-03
- `docs/parcours-simplifie.md` : les 3 questions avec leurs libellés verbatim (`1/3 - Quelle est votre classe ?`, `2/3 - Quels éléments privilégier ?`, `3/3 - Quel est votre niveau ? (1 à 200)`, `AVANCE : personnaliser les réglages`), les entrées acceptées (nom **ou** numéro de classe, accents/casse tolérés, éléments `terre/feu/eau/air`, alias `1`–`4`, séparateurs espace/`,`/`+`, `multi`), les 3 messages d'erreur réels — DOCS-04
- `docs/parcours-simplifie.md` § « lire le résultat » : ordre réel du contenu, **carte de pagination** (`PAGE 1/6` observé sur le flux simplifié : page 1 = résumé + équipement ; pages intermédiaires = stats/panoplies ; **dernière page** = `Méthode`, `Score`, `Indice de recherche`), table de correspondance des slots (`amulet`, `ring_a`, `dofus_3`…) et des libellés **tronqués à 18 caractères** — DOCS-04
- `docs/parcours-simplifie.md` § « ce que l'outil suppose » : 5 points par niveau, ni exo ni parchemins, jets moyens, cibles PA/PM par paliers **40/100/150**, heuristiques de classe (distance/mêlée/portée/invocation) — DOCS-04
- `docs/wizard-avance.md` : les **9** étapes dans l'ordre de `WIZARD_STEPS` avec les titres de `STEP_TITLES`, les 11 slots (dont `BOUCLIER [OFF]` par défaut), les filtres `F1`–`F10` (⚠ `F6` = armes distance, `F7` = armes mêlée), les 11 options, la syntaxe items (`+ID` **interdit**, `-ID` **forcé** — contre-intuitif, à expliciter —, `!ID`, `CLEAR`), les 2 formats d'édition (`BASE POINTS CIBLE POIDS` / `BASE EXO CIBLE POIDS`, 4 nombres), le récap (`GO`/`RESET`/`SAVES`/`1-8`) — DOCS-05
- `docs/cli.md` : tableau « commande → rôle → exemple » couvrant **toutes** les sous-commandes (`version`, `self-test`, `search`, `item`, `list`, `optimize`, `db`, alias `cache`) et **toutes** les options globales (`--timeout`, `--data-dir`, `--force-sync`, `--offline`) + options `optimize` + avertissement explicite sur `db clear` — DOCS-06
- `docs/base-locale.md` : `.data/dofus.sqlite3`, catégories, mode hors-ligne, fenêtre de re-check **24 h**, `db status` décrit **par ses champs** (jamais par des valeurs), asymétrie CLI/web de la synchro, échec « base vide + `--offline` » — DOCS-07
- `docs/depannage.md` : 5 rubriques rédigées **à partir des messages réels** (base absente/vide, saisie invalide, calcul long, clavier inactif = focus hors champ, résultat paginé) — DOCS-08
- `docs/glossaire.md` : stuff, slot, solveur, poids, cible, ID Ankama, jet, exo, panoplie, dofus, trophée, prysmaradite, + « indice de recherche » — DOCS-09
- `GUIDE_WIZARD.md` corrigé là où il décrit l'ancienne arborescence — DOCS-10

**Should have (ce qui distingue une doc utile d'une doc « générée ») :**
- Bloc **« Source de vérité »** en tête de chaque page (chemins `.py` + symboles en backticks) — le lecteur sait sur quoi la page s'engage, et un fichier renommé casse un test
- Encadrés « ce que vous devez voir à l'écran » (copie verbatim du rendu) dans les parcours J2/J4/J5 — supprime la question « ai-je fait pareil ? »
- Table **libellé affiché → nom complet** (slots, stats tronquées, abréviations `B/P/C/W`, `E` pour exo) — sans elle, la page 2+ du résultat est illisible
- Section **« défauts différents selon l'entrée »** : wizard vierge = `DUREE 5s` / `TOP-K 30` ; wizard atteint par `AVANCE` avec classe+éléments = `DUREE 8s` / `TOP-K 40` et poids/cibles du profil recommandé — sinon la doc paraît fausse
- Section **« règles du profil recommandé »** (capital `5 × (niveau − 1)`, paliers PA/PM 40/100/150, `% Critique` 35, vitalité `niveau × 12`, heuristiques de classe) — déjà prouvée par `tests/test_recommend.py`
- **Transparence sur les limites** : « indice de recherche » ≠ qualité en combat, recherche sur une **sélection** du catalogue (optimalité globale non garantie), ni prix/kamas, ni simulation de sorts/rotations
- **« Consulter le catalogue » documenté** : syntaxe qui marche `terme|limite` (ex. `Cape|20`), casse significative avec contre-exemples réels (`Cape` vs `cape` vs `CAPE`), pagination, panneau `[ APERCU ]` (qui charge une image **distante**)
- **Table « message affiché → ce qu'il faut faire »**, y compris les cas non évidents : `db status` **crée** le fichier s'il n'existe pas ; `db sync` CLI **refuse** `--offline` ; l'écran web de synchro contacte l'API Dofusdude **même** en mode hors-ligne
- **Sauvegardes + export Dofusbook** documentés : `localStorage` (clé `dofus-stuff-machine.saves`), **20 max**, `SAVE [nom]` seulement depuis l'écran résultat, fiche → `DB`, message réel quand la sauvegarde est trop ancienne

**Defer (v2+ — hors besoin initial) :**
- Éclatement de `wizard-avance.md` en sous-pages si elle dépasse ~400 lignes (réévaluer un sous-dossier **dans** `docs/`, tests déjà récursifs)
- Page dédiée « rechercher et consulter le catalogue » si J5 devient un parcours principal
- Diagramme texte du flux menu → simplifié → avancé (utile, non nécessaire, non testable)
- Section « limites de l'outil » consolidée en page propre (aujourd'hui éparpillée)

**Anti-features (à ne PAS produire) :** documenter l'architecture interne / les heuristiques de `candidates.py`/`cpsat.py` / le format msgpack Dofusbook ; générer une référence d'API ; documenter la **ligne compacte** de l'optimiseur comme une commande (elle est testée mais **branchée sur aucune sous-commande** — vérifié) ; conseiller `db clear` « pour repartir de zéro » ; recopier des **valeurs volatiles** de la base (nombre d'objets, version de jeu, horodatage, `PAGE 1/872`) ; dupliquer la description du wizard dans deux fichiers ; ajouter des captures d'écran ; documenter `.doc-agent/`, la CI ou les migrations ; écrire en anglais ou prévoir `docs/en/` ; publier la doc ; recopier ligne à ligne `GUIDE_WIZARD.md` sans corriger (cela migrerait ses 6 erreurs).

### Architecture Approach

Une **couche documentaire adossée au produit**, à sens unique : le code est la source de vérité, la documentation est le reflet, le test est le juge. Aucun fichier de `dofus_stuff/**` n'est modifié ; le harnais observe (imports de symboles, `parse_args` sans exécution, rendu via client de test) et ne peut pas corriger.

**Major components :**
1. `docs/sommaire.md` — **l'index unique** : liste exhaustive des pages, un label par page (= son H1), parcours conseillé en 3 étapes ; ne décrit aucun écran (pas de contenu dupliqué)
2. `docs/installation.md`, `parcours-simplifie.md`, `wizard-avance.md`, `cli.md`, `base-locale.md`, `depannage.md`, `glossaire.md` — **un fichier = un thème = une exigence DOCS** : c'est ce découpage qui rend le message d'échec actionnable (« ajouter `AVANCE : personnaliser les réglages` dans `docs/parcours-simplifie.md` »)
3. `README.md` — point d'entrée produit (et `readme` du paquet) : reçoit une section « Documentation utilisateur », ne duplique rien, ne renvoie plus vers une page périmée
4. `GUIDE_WIZARD.md` — **aiguillage** : « ce guide a été déplacé », arborescence de menus **corrigée** en bloc de code, lien vers `docs/wizard-avance.md` ; n'est plus une seconde description concurrente
5. `tests/conftest.py` — **pivot édité une seule fois** : ajout de la fixture `docs_dir` (`Path(__file__).resolve().parents[1] / "docs"`), à côté des fixtures existantes `catalog`/`app`/`client`
6. `tests/test_docs_structure.py` — invariants **internes** à la doc ; n'importe **rien** du produit (reste évaluable même sans `ortools`)
7. `tests/test_docs_code_anchor.py` — invariants **doc ↔ code** ; **n'exécute jamais** `main()`, n'ouvre ni socket ni `.data/`

**Patterns structurants (à suivre tels quels) :**
- **Index unique + exhaustivité bidirectionnelle** : l'ensemble des cibles du sommaire **==** l'ensemble des `docs/**/*.md` (hors sommaire), test écrit **récursif** (`rglob`) dès maintenant
- **Séparer invariant auto-ajustant et complétude** : l'exhaustivité valide ce qui existe ; la liste épinglée `PAGES_REQUISES` (8 pages) est un **critère de sortie de la dernière phase**, jamais de la première — sinon la suite est rouge cinq phases « pour une bonne raison » et on cesse de la lire
- **Ancrage bidirectionnel** : (a) ce que la doc cite existe dans le code (sondes passées au vrai parseur, libellés extraits du vrai rendu) ; (b) ce que le code expose est cité dans la doc (aucune option oubliée)
- **Observer par rendu réel, pas par `grep`** : la troncature à 18 caractères, le padding à 100 colonnes, la pagination et l'échappement HTML sont invisibles à la lecture du code — c'est précisément là qu'un `grep` produit une doc plausible et fausse
- **Comparaison normalisée** : `unicodedata` NFD + suppression des diacritiques + `casefold` + apostrophes typographiques → ASCII + espaces écrasés. La doc **affiche verbatim** (accents, apostrophes françaises) ; le test **compare normalisé**
- **Bloc « Source de vérité » validé par existence de chemin** : tout jeton `` `…py` `` d'un bloc connu doit exister sur disque
- **Liens relatifs de fichier à fichier uniquement** : cible contenant `#` **rejetée** (réimplémenter l'algorithme de slug GitHub est une source de faux négatifs) ; pas de chemin absolu, pas d'URL vérifiée (les liens externes restent du texte)
- **Isolation des tests de doc** : `test_docs_structure.py` = lecture de fichiers uniquement ; les contrôles d'écran réutilisent la fixture `client` (catalogue synthétique, `tmp_path`, `skip_sync`) — la suite reste à ~2 s

**Fichiers pivots (à sérialiser malgré `parallelization: true`) :** `docs/sommaire.md` (chaque phase y ajoute une ligne, et l'omission est fatale), `tests/conftest.py` (une seule fois), les deux modules de tests de doc (une phase ajoute ses contrôles à la fin), `README.md` (phases 1 et 4), `GUIDE_WIZARD.md` (une seule phase propriétaire, la 4). Les phases peuvent paralléliser la **rédaction des pages** (un fichier `docs/` = un propriétaire) mais jamais leurs entrées d'index ni les modules de tests.

### Critical Pitfalls

1. **Documenter le produit d'avant** (le numéro de menu donné n'ouvre pas l'écran promis) — c'est **déjà cassé** : `GUIDE_WIZARD.md` cite `3. OPTIMISATION DE STUFF` alors que `3` ouvre les panoplies et que l'optimisation est `4` ; le menu réel compte **5** entrées, pas 4 ; « vous arrivez directement dans le wizard » est faux depuis `1d475f9`. **Parade :** dériver le menu et les titres du **rendu réel** (`client.get("/")`), et asserter la moitié **négative** (aucun document ne doit associer un numéro au mauvais libellé). Interdit : écrire `assert "5. SYSTEME" in doc` (constante recopiée).
2. **Le pansement en tête au lieu de corriger le corps** — `GUIDE_WIZARD.md` contient aujourd'hui deux vérités contradictoires (une note `1d475f9` en tête + le corps périmé 30 lignes plus bas) ; un test de **présence** passe donc sur une doc fausse. **Parade :** une seule source par énoncé ; la correction se fait **dans** la phrase fausse. C'est l'argument décisif de l'arbitrage n° 1 ci-dessous.
3. **Aucun test ne relie la doc au produit (cause racine)** — 136 tests verts, zéro test documentaire, et deux commits de dérive (`ab1eb38` → `1d475f9`) passés sans être détectés. **Parade :** chaque affirmation ancrable a **deux côtés dans le même test** (runtime + fichier sur disque) ; un test à un seul côté n'est pas un contrôle.
4. **Le test tautologique** (les deux côtés partagent la même source) — constante recopiée, liste de renvois obsolètes écrite à la main depuis la doc fautive, ou doc générée puis vérifiée contre son générateur. **Parade :** tout attendu provient d'un appel de code ; le contrôle des renvois obsolètes est **dérivé** (règle, pas liste) ; un **test de mutation** (dérive injectée dans une copie sous `tmp_path` → le contrôle doit échouer) prouve que le garde-fou mord.
5. **Vérifier en exécutant ce que la doc décrit — dont des commandes destructrices** — `python fetcher.py db clear` supprime **immédiatement**, sans confirmation côté CLI (la version web, elle, demande `O`), `db sync`/`--force-sync` déclenche une **vraie** resynchronisation, `PURGE OUI` efface jusqu'à 20 sauvegardes navigateur sans copie serveur. **Parade :** CLI vérifiée par `build_parser().parse_args` uniquement ; web vérifiée par le client de test sur base `tmp_path` ; dans `docs/`, aucune commande destructrice dans les parcours, et un avertissement explicite sur la même ligne là où elle est mentionnée. Noter que `git status` **ne peut pas** détecter une destruction (`.data/` est ignoré) : le contrôle d'intégrité de `.data/` passe par empreinte/mtime.
6. **Test documentaire non hermétique** (ouvre la vraie base ou le réseau) — construire l'app sans injecter de catalogue tombe sur `.data/dofus.sqlite3` et peut déclencher `ensure_up_to_date`. **Parade :** tests d'intégrité = lecture de fichiers ; tests d'écran = fixture `client` + patch réseau comme `tests/test_web.py` le fait déjà.
7. **Comparer des chaînes brutes au rendu HTML** → faux négatifs → quelqu'un « répare » en affaiblissant l'assertion → la dérive revient. Pièges observés : `D&#39;OBJETS` (autoescape) vs `D'OBJETS` ; padding à exactement 100 colonnes ; apostrophes typographiques `’` vs `'` ; casse différente (flux simplifié en casse de phrase, wizard tout en majuscules) ; console Windows qui n'affiche pas les accents. **Parade :** un **seul** helper de normalisation, documenté et testé lui-même.
8. **Le garde-fou jamais vu rouge, et la liste de pages épinglée trop tôt** — un test d'anti-dérive introduit après la correction sans avoir jamais échoué ne prouve rien ; une suite rouge cinq phases détruit sa valeur de signal. **Parade :** au moins un contrôle doit passer **rouge → vert** dans la phase qui corrige (phase 4) ; la complétude arrive en phase 6.
9. **Deux producteurs concurrents de `docs/`** — voir la section « Risques d'écrivains non contrôlés » ci-dessous.
10. **Vérification faite dans le mauvais interpréteur** — `python -m pytest -q` échoue (`No module named pytest`). **Parade :** la commande du milestone est littéralement `.venv/Scripts/python.exe -m pytest -q`, avec compteur et durée cités ; aucun résultat de test écrit sans exécution réelle. Et : « une action humaine indispensable qui ne peut pas être automatisée est un **blocage à signaler**, pas une validation à déclarer ».

---

## Implications for Roadmap

Structure suggérée : **7 phases**, chacune livrant une capacité de bout en bout **vérifiable** par `pytest` (mode MVP, tranches verticales). L'ordre est contraint par les dépendances de contenu identifiées par les recherches et par la sérialisation des six fichiers pivots.

### Phase 1: Socle documentaire et harnais (index, installation, preuve)
**Rationale:** l'index et la fixture sont les deux pivots dont tout dépend ; dès deux pages, les invariants de base (liens, exhaustivité auto-ajustante, UTF-8, H1 ↔ label) sont vérifiables et le harnais rend service au lieu d'attendre. C'est aussi la tranche verticale minimale : un lecteur installe, lance CLI et web, et trouve la doc depuis `README.md`.
**Delivers:** `docs/sommaire.md` + `docs/installation.md` (contenu réel, non-brouillon, incluant la section « interface terminal ») ; section « Documentation utilisateur » de `README.md` ; fixture `docs_dir` dans `tests/conftest.py` ; `tests/test_docs_structure.py` (P1 : arbre, exhaustivité, liens relatifs résolus, aucun lien ancre/absolu, H1 unique ↔ label, ligne `[← Sommaire]`, README → sommaire, UTF-8 sans placeholder) ; `tests/test_docs_code_anchor.py` (P1 : existence des chemins « Source de vérité », options de l'entrée web `--data-dir/--offline/--online/--timeout/--host/--port/--debug` documentées et analysables) + le helper de normalisation **et** son test.
**Addresses:** DOCS-01, DOCS-02, DOCS-03, DOCS-11 (socle).
**Avoids:** Pitfall 6 (fixture hermétique, créée une seule fois), Pitfall 7 (helper de normalisation posé avant toute comparaison), Pitfall 8 (liste épinglée **exclue** de cette phase), Pitfall 9 (décision écrite : `docs/` appartient à ce milestone, aucun générateur), Pitfall 10 (commande de test épinglée dans les critères de sortie).

### Phase 2: Surface CLI
**Rationale:** `installation.md` cite déjà des commandes ; fermer la boucle d'ancrage CLI avant que les pages d'usage ne s'appuient dessus évite d'ancrer la doc sur du vide.
**Delivers:** `docs/cli.md` (toutes sous-commandes, options globales, options `optimize`, mode interactif, exemples exécutables, avertissement `db clear`) + son entrée d'index + les contrôles P2 (`test_commandes_cli_documentees`, `test_options_globales_documentees`, `test_options_optimize_documentees`, `test_exemples_cli_analysables`).
**Uses:** `dofus_stuff.cli.build_parser` (ré-exporté « pour tests / scripts »), `shlex`, la bibliothèque standard.
**Addresses:** DOCS-06.
**Avoids:** Pitfall 3 (ancrage), Pitfall 4 (sondes statiques pour « la doc n'invente rien » + vérification que **chaque exemple documenté analyse** — pas d'attendu recopié), Pitfall 5 (jamais `main()`, `db clear` seulement **parsé**).

### Phase 3: Parcours simplifié (le cœur de la valeur produit)
**Rationale:** c'est la nouveauté `1d475f9` et la partie **totalement** non documentée ; `wizard-avance.md` en dépend (`AVANCE` et les retours ne se comprennent qu'après les 3 questions).
**Delivers:** `docs/parcours-simplifie.md` — les 3 questions verbatim, entrées acceptées, 3 messages d'erreur réels, `AVANCE` ; § « lire le résultat » (carte de pagination, où sont `Méthode`/`Score`/`Indice de recherche`, table libellé tronqué → nom complet) ; § « ce que l'outil suppose » (5 points/niveau, paliers 40/100/150, heuristiques de classe) ; § limites et § « ce que l'outil ne fait pas » ; entrée d'index + contrôles P3 (`test_menu_labels_documented`, `test_libelles_parcours_simplifie`).
**Addresses:** DOCS-04.
**Avoids:** Pitfall 1 (menu dérivé du rendu + assertions négatives sur les couples obsolètes), Pitfall 4 (chaque libellé est épinglé **sur l'écran où il est réellement rendu** — attention : `POST /optimize/quick/classe` répond l'écran **2/3**, le 1/3 s'obtient par `GET`), Pitfall 7 (comparaison normalisée), Anti-Pattern 2 (rédiger depuis le rendu, pas depuis un `grep` de `routes.py`).

### Phase 4: Wizard avancé + résorption de la dette `GUIDE_WIZARD`
**Rationale:** cette phase **réduit la dispersion**. Tant que `GUIDE_WIZARD.md` décrit encore le wizard en entier, deux sources concurrentes existent et toute correction peut être appliquée au mauvais endroit — c'est la cause directe du Pitfall 2. Elle est placée **avant** les autres pages de contenu pour cette raison.
**Delivers:** `docs/wizard-avance.md` (contenu **migré**, pas recopié : 9 étapes, slots/filtres, options, formats d'édition, syntaxe items, touches réelles, sauvegardes/export) ; `GUIDE_WIZARD.md` réduit à un aiguillage corrigé ; `README.md` ligne 59 redirigée ; contrôles de structure P2 (`test_aucun_renvoi_obsolete`, **vu rouge sur l'état antérieur puis vert**) et contrôles P3/P4 wizard (`test_etapes_wizard_documentees`, `test_commandes_wizard_documentees`, `test_touches_clavier_documentees`, `test_identifiants_ecrans_documentes`).
**Addresses:** DOCS-05, DOCS-10.
**Avoids:** Pitfall 2 (une seule source par énoncé), Pitfall 8 (démonstration rouge → vert exigée dans les critères de sortie), Pitfall 9 (interdiction de relancer le générateur ; liste des fichiers verrouillée en phase 6).

### Phase 5: Base locale, hors-ligne et resynchronisation
**Rationale:** c'est le point qui explique la majorité des « ça ne marche pas » hors connexion, et la phase qui parle des commandes destructrices — donc celle où la règle « on ne lance pas » doit être la plus visible.
**Delivers:** `docs/base-locale.md` (fichier, catégories, fenêtre 24 h, **deux défauts différents** — web hors-ligne par défaut, CLI **en ligne** par défaut donc `--offline` requis —, champs de `db status` et non valeurs, asymétrie CLI/web de la synchro, échec « base vide + `--offline` », `db status` qui **crée** le fichier, avertissements `db clear` / `PURGE OUI`) + entrée d'index + contrôles P4 (`test_db_status_fields_documented`, `test_base_locale_documentee`).
**Addresses:** DOCS-07.
**Avoids:** Pitfall 5 (aucune exécution, avertissement sur la même ligne), Anti-Pattern 5 (aucune valeur volatile), Anti-Pattern 7 (ne jamais modifier `dofus_stuff/**` pour aligner la doc), Pitfall 6 (aucun accès à `.data/`), et les « integration gotchas » : option globale **avant** la sous-commande (`--offline optimize …`, pas l'inverse), `--online`/`db sync` présentés comme actions explicites et ponctuelles, `--host 0.0.0.0` jamais recommandé (serveur de dev sans authentification), aucun secret dans `docs/` (le **nom** de la variable seulement).

### Phase 6: Dépannage, glossaire et complétude
**Rationale:** ces deux pages sont les filets du lecteur (il cherche par **message**, pas par concept) et le glossaire lève l'opacité du vocabulaire ; la liste épinglée des pages n'a de sens qu'ici, une fois les 8 pages livrées.
**Delivers:** `docs/depannage.md` (5 rubriques rédigées depuis les messages réels, cas non évidents inclus) ; `docs/glossaire.md` (trié, chaque entrée reliée à un libellé du produit) ; leurs entrées d'index ; contrôles P3 (`test_rubriques_depannage_presentes`, `test_glossaire_entrees_presentes`) ; **P4 `test_pages_requises_livrees`** (liste épinglée — critère de complétude, introduit **ici seulement**) ; le contrôle de l'ensemble des fichiers de `docs/` qui détecte une écriture parasite.
**Addresses:** DOCS-08, DOCS-09.
**Avoids:** Pitfall 8 (complétude trop tôt), Pitfall 9 (page supplémentaire = échec = détection d'un second écrivain), Pitfall 1 (les messages d'erreur cités sont ceux du code, pas des paraphrases).

### Phase 7: Clôture et preuve du harnais
**Rationale:** une suite verte ne prouve rien si les garde-fous n'ont jamais mordu ; la clôture est le moment de la preuve et de la consolidation.
**Delivers:** parcours conseillé final du sommaire ; **test de mutation** (copie de `docs/` dans `tmp_path`, dérive injectée — ex. `5. SYSTEME` → `4. SYSTEME` — et assertion que le contrôle échoue) ; suite complète verte exécutée en `.venv/Scripts/python.exe -m pytest -q` avec **compteur et durée réels** cités ; vérification que `.data/` est intacte par **empreinte/mtime** (et non par `git status`) ; vérification que seuls `docs/`, `README.md`, `GUIDE_WIZARD.md`, `tests/` apparaissent dans `git status --short` (donc aucune modification de `dofus_stuff/**`).
**Addresses:** DOCS-11, DOCS-12 (consolidés).
**Avoids:** Pitfall 4 (test tautologique), Pitfall 8 (garde-fou jamais rouge), Pitfall 10 (interpréteur), Pitfall 5 (contrôle d'intégrité de `.data/`).

### Phase Ordering Rationale

- **Phase 1 d'abord** : `sommaire.md` et la fixture `docs_dir` sont les pivots de tout le milestone, et les invariants P1 sont déjà vrais sur deux pages (aucune suite rouge « normale » à porter).
- **Phase 4 avant les autres pages de contenu** : elle supprime la **dispersion** (`GUIDE_WIZARD.md` complet ⇒ deux sources concurrentes). C'est le seul remède structurel à la cause du Pitfall 2.
- **La complétude en phase 6, jamais en phase 1** : sinon la suite est rouge cinq phases et perd sa valeur de signal (Pitfall 8).
- **`parcours-simplifie.md` (3) avant `wizard-avance.md` (4)** : `AVANCE` et le retour du récap ne se comprennent qu'à partir du flux simplifié ; inverser produit une page wizard qui commence par une redirection inexpliquée.
- **`cli.md` (2) avant `parcours-simplifie.md` (3)** : `installation.md` (phase 1) cite déjà des commandes ; la phase 2 ferme la boucle d'ancrage CLI avant que les pages d'usage ne s'appuient dessus.
- **`base-locale.md` (5) avant de multiplier les exemples CLI exécutables** : sinon le lecteur lance des commandes qui échouent hors-ligne avec « base vide + `--offline` ».
- **Les tests d'ancrage dépendent des pages, pas l'inverse** : écrire les pages avec les libellés corrects **puis** les tests qui les relisent — sinon les tests figent les erreurs existantes.
- **Séquençage imposé malgré `parallelization: true`** : les 6 fichiers pivots (`sommaire.md`, `conftest.py`, les 2 modules de tests, `README.md`, `GUIDE_WIZARD.md`) sont séquentiels. Le parallélisme ne porte que sur la rédaction de pages de propriétaires distincts ; l'ordonnanceur de cet hôte exécute les vagues séquentiellement (barrières préservées, aucune écriture concurrente).
- **Conflit à interdire explicitement** : réécrire `GUIDE_WIZARD.md` et rédiger `docs/wizard-avance.md` dans deux tâches parallèles sans arbitrer la source unique — c'est exactement le scénario qui a produit la désynchronisation actuelle.

### Research Flags

**Needs deeper investigation during planning** (pas de websearch : la source de vérité est le dépôt — il s'agit d'attention de *plan*, pas de recherche externe) :
- **Phase 4 :** la seule phase qui **réécrit un fichier existant** et qui est simultanément la cible d'un contrôle. Le plan doit trancher l'arbitrage n° 1, mapper les 12 défauts audités vers leur correction, et **conserver** ce qui est juste dans `GUIDE_WIZARD.md` (l'ordre des 9 étapes, la syntaxe `+ID`/`-ID`, la table des touches). Règle : « migrer, pas réinventer ».
- **Phase 2 :** décider explicitement entre **sondes statiques** et **introspection `argparse`** (arbitrage n° 3), et l'écrire dans le test lui-même.
- **Phase 5 :** décider du **propriétaire** des sections « lire le résultat » et « sauvegardes / export Dofusbook » (arbitrage n° 2) — c'est le point de divergence entre les deux recherches.

**Phases with standard patterns (skip `--research-phase`) :**
- **Phase 1 :** fixtures pytest, lecture de fichiers, regex de liens, normalisation Unicode — tout est standard et entièrement spécifié par les recherches.
- **Phase 3, 6, 7 :** rédaction sourcée + assertions de présence ; aucune incertitude technique.
- **Phase 5 :** comportement de `sync.py`/`database.py` déjà entièrement décrit (fenêtre 24 h, asymétrie CLI/web, effets de bord de `db status`).

---

## Décisions ouvertes à trancher par le roadmapper

Ces trois arbitrages sont **explicitement laissés ouverts** par les recherches. Ils doivent être résolus **dans le plan d'une phase** (et écrits dans le test concerné), pas rester implicites.

1. **`GUIDE_WIZARD.md` : migrer le contenu ou corriger sur place ?**
   - **Recommandation (MEDIUM, décision de goût) :** `docs/wizard-avance.md` devient la **source unique** (contenu migré depuis `GUIDE_WIZARD.md` **et corrigé** contre le code) ; `GUIDE_WIZARD.md` est réduit à un aiguillage d'une quinzaine de lignes (titre, « ce guide a été déplacé », arborescence de menus **corrigée** en bloc de code, lien vers `docs/wizard-avance.md`). Raisons : `GUIDE_WIZARD.md` ne peut pas être « corrigé par retouches » (6 affirmations fausses + 5 trous sur 330 lignes), et deux descriptions concurrentes sont la cause mesurée de la désynchronisation.
   - **Alternative acceptable :** garder `GUIDE_WIZARD.md` comme page complète corrigée et faire pointer `docs/sommaire.md` vers `../GUIDE_WIZARD.md`, sans créer `docs/wizard-avance.md`. **Conditions obligatoires :** ne jamais dupliquer le contenu, et **rediriger les tests d'ancrage wizard vers `GUIDE_WIZARD.md`** (DOCS-05 serait alors prouvé sur ce fichier, hors de `docs/`). À ne retenir que si la migration est jugée risquée.
   - **Décision requise en :** phase 4. **Interdit dans tous les cas :** committer un état où les deux fichiers décrivent le wizard en entier.

2. **Où vivent « lire le résultat » et « sauvegardes / export » ?**
   - **Recommandation :** ce sont des **sections** de `docs/parcours-simplifie.md` (`§ Lire le résultat`, `§ Sauvegarder et exporter`), **pas** un 8ᵉ fichier. Cela garde le test d'exhaustivité du sommaire trivial, évite un fichier pour ~60 lignes, et colle aux parcours lecteur J3/J6 (le lecteur lit son résultat **dans** le flux simplifié, puis le sauvegarde depuis ce même écran).
   - **Point de divergence à trancher :** `FEATURES.md` place explicitement ces sections dans `parcours-simplifie.md` ; `ARCHITECTURE.md` §1.3 attribue « sauvegardes, export Dofusbook » au propriétaire `wizard-avance.md`. **Une seule réponse est acceptable** (une source par énoncé). Recommandation : `parcours-simplifie.md` **possède** le contenu (parcours complet résultat → sauvegarde → export) ; `wizard-avance.md` s'y **réfère** par un lien, sans recopier. Si l'option « page dédiée » était choisie, il faudrait mettre à jour la liste épinglée du test d'exhaustivité **et** les deux modules.
   - **Décision requise en :** phase 3 (propriété) et rappel en phase 4.

3. **Sondes CLI statiques ou introspection `argparse` ?**
   - **Recommandation :** **sondes statiques** pour le sens « la doc n'invente rien » (robustes, lisibles, aucune API privée) **+** vérification bidirectionnelle sur les exemples réellement documentés (`shlex.split` → `build_parser().parse_args` doit réussir **et** l'exemple doit apparaître verbatim dans `docs/cli.md`). C'est ce qui est exécutable aujourd'hui sans dépendre de `parser._subparsers._group_actions[…]` (API privée, vérifiée mais fragile).
   - **Limite honnête à écrire dans le test :** l'ajout futur d'une option au parseur ne fera pas échouer le test tant que la sonde n'est pas ajoutée. L'alternative (introspection : détecte automatiquement les nouveautés au prix d'une API privée) reste ouverte — le roadmapper doit **choisir explicitement** et l'écrire, pas laisser la question ouverte.
   - **Décision requise en :** phase 2.

---

## Risques d'écrivains non contrôlés (à enregistrer ; ne rien supprimer)

Un outillage documentaire **antérieur et inactif** vise exactement la cible de ce milestone. **Aucune de ces ressources ne doit être supprimée, lancée, ni utilisée comme source.**

1. **`doc-agent.toml` (racine, non suivi par git) cible `output = "docs"`** — `language = "fr"`, `base_url = "http://localhost:11434/v1"` (Ollama local), `model = "qwen3.8:27b"`, `api_key_env = "ollama"`, `max_revision_cycles = 2`, `gsd_path` pointant vers le framework. Risque : une relance écrase des pages rédigées à la main, de façon non déterministe, et peut **fabriquer** des commandes ou des écrans inexistants — le risque dominant du milestone.
2. **`.doc-agent/state.json` est figé en `status: "running"` / `stage: "PLAN"`** (sur le commit `1d475f9`), avec `.doc-agent/lock` et `.doc-agent/runs/` ; **`.doc-agent/` n'est pas dans `.gitignore`** (le fichier ignore `.data/` et `.gsd-auto/`, mais pas `.doc-agent/`). `git status --porcelain` affiche `?? .doc-agent/` et `?? doc-agent.toml`. Risques : débris commités par un `git add .` / `git add -A` depuis la racine ; contrôle d'intégrité instable si le contenu de `docs/` change sans commit correspondant.

**Mitigations exigées :**
- `docs/` appartient **exclusivement** à ce milestone : ne pas lancer `doc-agent`, ne pas l'utiliser comme source, ne pas « compléter » ses sorties, ne pas documenter `doc-agent.toml` ni l'endpoint Ollama dans la doc utilisateur.
- **Ne jamais** utiliser `git add .` / `git add -A` depuis la racine ; toujours lister explicitement les chemins (`docs/`, `README.md`, `GUIDE_WIZARD.md`, `tests/`, `.planning/research/`).
- Le contrôle de l'ensemble des fichiers de `docs/` (phase 6) joue aussi le rôle de **détection d'écriture parasite** : toute page non listée fait échouer la suite.
- Si le bruit persiste : un **petit commit d'hygiène local** ajoutant `.doc-agent/` à `.gitignore` est acceptable (sans rapport avec le contenu de la doc). **Ne rien supprimer sous `.doc-agent/`.** Le `.gitignore` est actuellement modifié dans l'arbre de travail (ajout non commité de `.gsd-auto/`, plus `gsd-auto.toml` / `gsd-auto-rules.toml` non suivis) : **ne pas** inclure ces fichiers dans les commits de ce milestone.
- Signaux d'alerte : `updated_at` de `.doc-agent/state.json` qui augmente ; nombre de fichiers dans `docs/` qui change sans commit correspondant ; page dont le style tranche avec les autres.

**Contraintes de sûreté opérationnelles (rappel, valables à toutes les phases) :** hors-ligne d'abord (`.data/dofus.sqlite3` suffit) ; **jamais** `db clear`, jamais de drop SQLite, aucune suppression sous `.data/` ; aucune resynchronisation Dofusdude sauf nécessité démontrée ; aucune publication ni déploiement distant ; commits **locaux** uniquement ; aucune modification de `dofus_stuff/**` ; aucune validation humaine déclarée — un critère non automatisable est un **blocage à signaler**, jamais un « validé manuellement ».

---

## Confidence Assessment

| Area | Confidence | Notes |
|------|------------|-------|
| Stack | **HIGH** | Toutes les affirmations sont ancrées dans des fichiers lus (`pyproject.toml`, `.gitignore`, `tests/`) ou exécutés (`.venv` avec pytest 9.1.1). **Aucun** fournisseur web disponible : rien n'a été inventé, aucun digest externe n'a été mis en cache. Le choix « Markdown nu + stdlib + pytest » est surdéterminé par `PROJECT.md` (outillage = pytest seul ; site statique hors périmètre ; publication interdite). |
| Features | **HIGH** sur l'inventaire (lecture intégrale du code **et** rendu réel de chaque écran hors-ligne), **MEDIUM** sur les arbitrages de parcours lecteur et les priorités (jugement éditorial). Le layout de fichiers est repris de `STACK.md` : les recherches sont alignées, sauf sur le point « où vivent lire-le-résultat / sauvegardes » (arbitrage n° 2). |
| Architecture | **HIGH** sur les artefacts d'ancrage et les contrôles proposés (vérifiés par deux moyens indépendants : code + rendu), **MEDIUM** sur l'ordonnancement des phases, la séparation invariant auto-ajustant / complétude, et l'arbitrage sondes statiques vs introspection `argparse`. |
| Pitfalls | **HIGH** sur les pièges **observés dans ce dépôt** (chaque constat cite chemin + ligne, un commit, ou une exécution rejouable) ; **MEDIUM** sur « quel piège est le plus grave / quelle phase le traite ». Les pièges 1, 2, 3, 5 et 9 sont des **faits vérifiés**, pas des hypothèses. |

**Overall confidence:** **HIGH** pour l'exécution (le contenu à documenter et les contrôles sont déjà spécifiés au niveau de détail requis), **MEDIUM** pour l'ordonnancement et les trois arbitrages.

### Gaps to Address

- **Arbitrages 1 à 3 ci-dessus** : à trancher explicitement dans les plans des phases 2, 3 et 4, et à **écrire dans le test** concerné. Ne pas les laisser implicites.
- **Propriété de « sauvegardes / export » et « lire le résultat »** : `FEATURES.md` et `ARCHITECTURE.md` divergent (sections de `parcours-simplifie.md` vs `wizard-avance.md`). Une seule réponse acceptable ; la divergence doit être résolue avant d'écrire ces sections.
- **Coquille de l'écran de recherche** : `SRC-01` annonce `SYNTAXE OPTIONNELLE : terme|/limite` alors que le parseur attend `terme|<entier>` (le `/` provoque `LIMITE INVALIDE`). Le périmètre est documentaire et le code ne change pas : la doc doit donner la syntaxe **qui marche** (`Cape|20`) **et** signaler l'écart en note. Incertitude éditoriale assumée.
- **Ligne compacte de l'optimiseur** (`123 int,vit 200,50 100,0 classic jet=max`) : testée mais **branchée sur aucune sous-commande ni option**. Ne pas la documenter comme une commande ; si mention, l'annoncer explicitement comme « fonction interne, non exposée en CLI ».
- **Échec d'un `self-test`** : les libellés des contrôles sont stables mais techniques (`objet 44 nom`, `lecture mémoire stable`). Faut-il expliquer chaque échec dans `depannage.md` ? Incertitude éditoriale à trancher en rédigeant.
- **Limites honnêtes du harnais, à écrire dans la doc de vérification plutôt qu'à masquer :** (a) le comportement **JavaScript** n'est pas exécuté par `pytest` — on peut affirmer que les littéraux `F3`/`Escape`/`F7`/`F8`/`PageUp`/`PageDown`, `SAVES_KEY`, `MAX_SAVES = 20` existent dans `terminal.js` et dans les attributs `data-*` rendus, **pas** qu'un appui produit l'effet décrit ; (b) la **sortie réelle** de `db status`/`self-test`/`version` dépend de la base locale — donc aucun chiffre figé par un test ; (c) les contrôles prouvent l'**ancrage** (libellés, commandes, chemins), **pas la véracité de la prose** — d'où la règle « on n'écrit jamais une page sans avoir lu ou rendu l'artefact dans la même phase ».
- **Durées de calcul** : seules les valeurs **par défaut du code** sont citables (`DUREE` 5 s / 8 s, `TOP-K` 30 / 40, paliers 40/100/150). Ne jamais citer un temps mesuré (machine/base/solveur dépendants).
- **`README.md` est aussi le `readme` déclaré du paquet** (`pyproject.toml`) : sur PyPI, un lien relatif vers `docs/sommaire.md` ne résout pas. Garder une formulation explicite (« dans le dépôt : `docs/sommaire.md` ») et ne pas faire dépendre l'entrée de la doc du seul rendu README.
- **Deux défauts hors-ligne différents à ne pas confondre :** le **web** est hors-ligne par défaut (`--online` pour l'inverse) ; la **CLI** est **en ligne** par défaut (`--offline` requis). Les deux doivent être documentés explicitement, sinon la moitié des exemples « hors-ligne » sont faux.
- **Ambiguïté `DB`** : sur l'écran résultat, `DB` = **Dofusbook** ; dans `5. SYSTEME` → `4. GESTION DE LA BASE`, « base » = SQLite locale. La doc doit lever l'ambiguïté explicitement.

---

## Sources

Toutes les sources sont **locales** : fichiers du dépôt lus ou exécutés. Aucun fournisseur web n'était joignable (`gsd_run query websearch` → `{"available": false, "reason": "BRAVE_API_KEY not set"}` ; aucun outil `context7` exposé ; `.planning/config.json` : tous les drapeaux de recherche à `false`). **Aucun résultat inventé, aucun digest externe mis en cache.**

### Primary (HIGH confidence — contexte, contraintes et outillage)
- `.planning/PROJECT.md` — périmètre brownfield, exigences **DOCS-01…DOCS-12**, contraintes (pytest seul, français, lecture seule sur `.data/`, hors-ligne, aucune publication), out-of-scope (MkDocs/Sphinx, i18n, publication), décisions clés (livrable `docs/` multi-fichiers, vérification par pytest, pas de validation humaine)
- `.planning/config.json` — `commit_docs: true`, `parallelization: true`, **tous** les fournisseurs de recherche à `false`
- `pyproject.toml` — `requires-python = ">=3.11"`, dépendances runtime (`flask`, `msgpack`, `ortools`), extra `dev` = `pytest>=8.0`, `[tool.pytest.ini_options]` (`testpaths`, `pythonpath`), `readme = "README.md"`, `[project.scripts]` (`dofus-stuff`, `dofus-stuff-web`)
- `.gitignore` — ignore `.data/` et `.gsd-auto/` ; **n'ignore ni `docs/` ni `.doc-agent/`** (diff non commité : ajout de `.gsd-auto/`)

### Primary (HIGH confidence — sources de vérité du produit, documentées ou contrôlées par test)
- `dofus_stuff/cli.py` — `build_parser()` (toutes les sous-commandes/options réelles ; `__all__` le ré-exporte « pour tests / scripts »), `_print_db_status`, `db clear` **immédiat sans confirmation**, `db sync` refusé avec `--offline`, `--offline` = `store_true` (donc **en ligne** par défaut)
- `dofus_stuff/web/routes.py` — codes PGM (`MNU-01`, `SYS-01`, `ITM-01`, `ITM-02`, `LST-01`, `PAN-01/02`, `SAV-01`, `VER-01`, `TST-01`, `DB-01…04`, `SRC-01/02`, `END-01`, `OPT-SIMPLE`, `OPT-W1…9`, `OPT-WED`, `OPT-03`), menu réel (5 entrées), routage du menu (`3` → panoplies, `4` → optimisation), flux simplifié (3 étapes, messages de validation, `AVANCE`), statuts, écrans de base, écran résultat
- `dofus_stuff/web/optimize_wizard.py` — `WIZARD_STEPS` (9), `STEP_TITLES`, `SLOT_GROUP_LABELS`, `TYPE_FILTER_LABELS`, `apply_stat_edit` (4 nombres ; parchemins non saisissables), `apply_items_input` (`+ID` interdit / `-ID` forcé), `body_items`, `body_recap`
- `dofus_stuff/web/screens.py` — `COLS = 100`, `clip`/`wrap_line`/`paginate` (justifie l'observation **par rendu réel** plutôt que par lecture de source)
- `dofus_stuff/web/static/js/terminal.js` — clavier (`F3`, `Escape`, `F7`, `F8`, `PageUp`, `PageDown`, `Enter`), `SAVES_KEY = "dofus-stuff-machine.saves"`, `MAX_SAVES = 20`, reprise du focus, export Dofusbook, message « AUCUN SLOT SAUVEGARDE »
- `dofus_stuff/web/templates/screen.html` — `data-f3-url`, `data-esc-url`, `data-f7-url`, `data-f8-url`, `data-mode`, bloc `item-visual` (aperçu **distant**)
- `dofus_stuff/web/__main__.py`, `dofus_stuff/web/__init__.py` — options et variables d'entrée web (`DOFUS_DATA_DIR`, `DOFUS_OFFLINE` défaut **vrai**, `DOFUS_TIMEOUT`, `DOFUS_SECRET_KEY`), `--host` défaut `127.0.0.1`, `--port` 5000, `--online`/`--no-offline`, `--debug`
- `dofus_stuff/database.py` — `DB_NAME`, `DEFAULT_DATA_DIR` (racine du dépôt + `.data`), `ITEM_KINDS`, création du fichier par `db status`
- `dofus_stuff/sync.py` — `CHECK_INTERVAL_SECONDS = 24 * 60 * 60`, `ensure_up_to_date` (actions `skip`/`touch`/`sync`), échec « base vide + `--offline` »
- `dofus_stuff/api.py` — `BASE_URL`, `DEFAULT_TIMEOUT = 15`, `SYNC_TIMEOUT = 120`, `SYNC_SOURCES`
- `dofus_stuff/catalog.py` — `search_items` **sensible à la casse**, messages `Équipement introuvable : #…` / `Panoplie introuvable : #…`
- `dofus_stuff/optimize/recommend.py` — `CLASSES` (19), `ELEMENTS` (`terre/feu/eau/air` → Force/Intelligence/Chance/Agilité), règles du profil recommandé (capital `5 × (niveau − 1)`, paliers 40/100/150, `top_k = 40`, `time_limit_s = 8`, `exo = scroll = 0`, heuristiques de classe)
- `dofus_stuff/optimize/api.py` — `format_optimize_result` (ordre réel du résultat, diagnostics déplacés **en fin de sortie** en mode simplifié, libellé « Indice de recherche »)
- `dofus_stuff/optimize/profile_input.py` — mode interactif (`Niveau [demo] :`, `Jets (min|average|max) [average] :`, …) et **ligne compacte non branchée** sur une sous-commande
- `dofus_stuff/model/solver_spec.py` — `SLOT_GROUPS`, `DEFAULT_SLOT_GROUPS` (`BOUCLIER` **OFF** par défaut), `TYPE_FILTER_KEYS` (⚠ `F6` = armes distance, `F7` = armes mêlée), `MAIN_CARACS`, `EXO_STATS`, `StatGoal`
- `dofus_stuff/web/dofusbook_export.py` — URL externe Dofusbook (base64 + msgpack)
- `dofus_stuff/model/slots.py` — `dofus_1…dofus_6` (6 emplacements de dofus/trophées)

### Primary (HIGH confidence — documentation existante, cible des corrections)
- `README.md` (121 lignes) — plutôt à jour : 5 entrées de menu, flux simplifié en 3 choix, options globales, « indice de recherche », limitations du solveur ; **ligne 59** renvoie encore vers `GUIDE_WIZARD.md` ; `readme` déclaré du paquet
- `GUIDE_WIZARD.md` (330 lignes) — **périmé** : 6 affirmations fausses (menu `3`/`4`, arrivée « directe » dans le wizard, `4. SYSTEME`, `F7` = armes distance, « % de compatibilité », parchemins saisissables) et 5 trous structurels (11 slots, `BOUCLIER` OFF, défauts variables selon l'entrée, `DB` sur une fiche, pagination) ; **sa structure de plan est bonne** et doit être *migrée*, pas réinventée
- `docs/` — **n'existe pas** (état vérifié)

### Primary (HIGH confidence — tests existants, état de référence)
- `tests/conftest.py` — fixtures `catalog`, `app`, `client` (catalogue synthétique, `create_app(..., offline=True, load_catalog=False)` sur `tmp_path`) ; recevra la fixture `docs_dir`
- `tests/test_web.py` — le menu est épinglé **côté code** (seule protection actuelle du menu), `patch("…ensure_up_to_date")`, `skip_sync=True`, `db clear` exercé sur la base **temporaire**
- `tests/test_web.py`, `tests/test_screens.py`, `tests/test_recommend.py`, `tests/test_optimize.py`, `tests/test_profile_input.py`, `tests/test_solver_spec.py` — conventions de nommage (fonctions en anglais, docstrings françaises) et littéraux déjà « officiels »
- Exécutions reproductibles : `.venv/Scripts/python.exe -m pytest -q` → **136 passed** (~1,7–1,8 s) ; `python -m pytest -q` → `No module named pytest`

### Primary (HIGH confidence — historique git, cause de la dérive)
- `ab1eb38` — ajout de `3. LISTE DES PANOPLIES`, `OPTIMISATION` 3 → 4, `SYSTEME` 4 → 5 ; **tests mis à jour, aucun fichier de doc touché**
- `b3aa6f2` — F12 → ESC : code + tests + doc dans le **même** commit (contre-exemple : la synchronisation est possible)
- `692736b` — « Update GUIDE_WIZARD and README for menu changes » (correction manuelle d'un changement de menu)
- `1d475f9` — flux simplifié : `README.md` corrigé, `GUIDE_WIZARD.md` seulement **préfixé de 6 lignes** (0 ligne du corps modifiée)

### Primary (HIGH confidence — sondes exécutées, reproductibles)
- `build_parser().parse_args(…)` sur 13 sondes (dont `db clear`, `cache stats`, `cache fill`) — toutes parsent ; sous-commandes réelles = `cache, db, item, list, optimize, search, self-test, version` ; options globales = `--data-dir, --force-sync, --offline, --timeout`
- Rendu de 14+ écrans via `create_app(offline=True, catalog=…, load_catalog=False)` + client de test — codes PGM, libellés `1/3`/`2/3`/`3/3`, `AVANCE : personnaliser les réglages`, messages de validation, `WIZARD_STEPS` = 9, pagination `PAGE 1/6` du résultat
- Helper de normalisation (NFD + sans diacritiques + `casefold` + apostrophes/tirets) validé sur `RECOMMANDATION DE STUFF` et `1/3 - Quelle est votre classe ?`
- Lecture **seule** de `.data/dofus.sqlite3` (URI `?mode=ro`) pour connaître la **forme** des données uniquement — aucune valeur volatile portée dans la doc, aucune écriture, aucune synchronisation, aucune suppression

### Secondary (MEDIUM confidence — arbitrages d'ingénierie, pas des faits observables)
- Ordonnancement des 7 phases, séparation invariant auto-ajustant / complétude, choix « migrer `GUIDE_WIZARD.md` plutôt que le corriger sur place », arbitrage sondes statiques vs introspection `argparse`
- Priorisation des features documentaires et découpage éditorial des parcours lecteur (J1…J7)

### Tertiary (LOW confidence — n'a pas pu être obtenue)
- Sources web (`websearch`, `context7`) : **indisponibles sur cet hôte**, vérifié et non supposé. Aucune conclusion de ce document n'en dépend : pour une tâche brownfield dont la source de vérité est le code du dépôt, la documentation externe aurait de toute façon été une source plus faible.

---

*Research completed: 2026-09-10 (HEAD `19b5c96`)*
*Ready for roadmap: yes — sous réserve des trois arbitrages à trancher (voir « Décisions ouvertes à trancher par le roadmapper »)*

