# Phase 4: Wizard avancé et résorption de la dette `GUIDE_WIZARD` - Research

**Researched:** 2026-09-11
**Domain:** Documentation utilisateur adossée au rendu réel (Flask, en processus) + harnais pytest d'ancrage documentaire (Python 3.11+/pytest, zéro dépendance nouvelle)
**Confidence:** HIGH (toutes les valeurs citées sont lues dans le dépôt *cette session*, la plupart **mesurées par exécution du client de test Flask**)

<user_constraints>

## User Constraints (from CONTEXT.md)

### Locked Decisions

*(copie verbatim de `04-CONTEXT.md`, décisions D-46 à D-67 — non négociables pour le planificateur)*

**Périmètre de l'aiguillage `GUIDE_WIZARD.md`**

- **D-46:** `GUIDE_WIZARD.md` est réduit à un **aiguillage court** (~15 lignes) : `H1`, avis de
  déplacement, **arborescence de menus corrigée**, lien vers `docs/wizard-avance.md` **et** lien vers
  `docs/sommaire.md`. Tout le reste est supprimé : ni section « Lire le résultat », ni exemple guidé,
  ni table des touches rédupliquée.
- **D-47:** L'arborescence de l'aiguillage est **lue dans le code**, jamais écrite de mémoire :
  `4. OPTIMISATION` (et non `3`), `3. PANOPLIES`, `5. SYSTEME`, conformément à
  `dofus_stuff/web/routes.py` (`menu_post`, lignes ~217-222). L'affirmation « tapez `3` puis Entrée
  pour ouvrir l'optimisation » disparaît : c'est la première référence obsolète à résorber.
- **D-48:** L'aiguillage ne porte **aucun énoncé de contenu**. Deux **liens de navigation** ne sont pas
  deux descriptions : D-17 interdit de décrire le wizard deux fois, pas de le référencer deux fois.
  Les deux liens mènent au même ensemble documentaire, donc D-10/D-29 (lien unique du `README.md`
  vers le sommaire) restent intacts.
- **D-49:** Le contenu retiré est **migré, jamais perdu** : l'exemple guidé va dans
  `docs/wizard-avance.md` (D-55) ; « lire le résultat » et « sauvegarder et exporter » restent
  propriété de `docs/parcours-simplifie.md` (D-38, phase 3) — renvoi, pas recopie.

**Découpage de `docs/wizard-avance.md`**

- **D-50:** La page suit **`WIZARD_STEPS`** — les 9 étapes **dans l'ordre exact du code** —
  `slots`, `options`, `caracs`, `papmpo`, `resistances`, `damages`, `misc`, `items`, `recap` — avec
  les **titres réellement rendus** lus dans `STEP_TITLES` de `dofus_stuff/web/optimize_wizard.py`
  (`SLOTS ET FILTRES`, `OPTIONS SOLVEUR`, `CARACTERISTIQUES`, `PA / PM / PO`, `RESISTANCES`,
  `DOMMAGES`, `DIVERS`, `ITEMS INTERDITS / FORCES`, `RECAPITULATIF`).
- **D-51:** La page contient une section **« Arriver au wizard »** décrivant le **chemin réel** :
  menu `4` → `optimize_entry` → `optimize_quick` (les 3 questions) → `AVANCE`. C'est précisément
  l'affirmation fausse à résorber : `GUIDE_WIZARD.md` annonce une arrivée « **directement** dans le
  wizard », alors que `optimize_entry` (`routes.py` ~930-932) redirige vers le parcours des
  3 questions.
- **D-52:** Le **périmètre de rendu est le web seulement** — le client de test Flask, en processus,
  hors-ligne, sans serveur ni réseau (méthode **D-32/D-36** de la phase 3). Le wizard vit dans
  `dofus_stuff/web/optimize_wizard.py` ; **aucune correspondance `AVANCE`/`wizard` n'existe dans
  `dofus_stuff/cli.py` ni `fetcher.py`**. Aucune section « parcours CLI du wizard » n'est écrite :
  la surface de commandes appartient à `docs/cli.md` (**D-37**).
- **D-53:** Les filtres de type `F1`–`F10` sont adossés à **`TYPE_FILTER_KEYS`**
  (`dofus_stuff/model/solver_spec.py:43`) et **`TYPE_FILTER_LABELS`**
  (`dofus_stuff/web/optimize_wizard.py:111`). Vérifié au code : index 6 = `arme_distance` → `F6` =
  `ARMES DISTANCE`, index 7 = `arme_melee` → `F7` = `ARMES MELEE`. **C'est la troisième référence
  obsolète à résorber** : `GUIDE_WIZARD.md` présente `F7` comme les armes distance.
- **D-54:** La page documente les **formats d'édition des quatre nombres** (`B` / `P` / `C` / `W`) et
  la **syntaxe d'items** telle que le code l'applique (`+ID` interdit, `-ID` forcé, `!ID`, `CLEAR`),
  dont le message d'erreur est lu au code (`optimize_wizard.py` : `+ID | -ID | !ID | CLEAR`). Les
  **touches actives** réellement vues au rendu sont citées : `GO`, `RESET`, `SAVES`, et `1`–`8` au
  récapitulatif.
- **D-55:** L'**exemple guidé** de `GUIDE_WIZARD.md` (§ 8 « Premier stuff en 5 minutes », avec sa
  variante « cible PA ») est **migré** dans `docs/wizard-avance.md`, et **réancré au rendu réel** :
  chaque écran, libellé, titre, touche et format qu'il cite est confronté au rendu. Un passage
  contredit par le code est **corrigé**, jamais conservé au motif qu'il figurait dans le guide. Il
  passe par le chemin d'arrivée réel (D-51) et ne met jamais `db clear` dans un parcours recommandé.
  La variante « cible PA » ne survit que si le code la porte ; sinon elle est **retirée et signalée**
  (D-19).
- **D-56:** La page suit le **gabarit D-01** : `H1` unique, phrase d'introduction, sections courtes,
  bloc **« Source de vérité »** pointant vers des chemins qui **existent réellement** sur disque
  (D-03), et ligne de retour vers `docs/sommaire.md`. Les renvois vers « lire le résultat » /
  « sauvegarder et exporter » sont des **liens** vers `docs/parcours-simplifie.md`, **sans recopie**
  (D-38/D-43).
- **D-57:** `docs/sommaire.md` gagne **l'entrée d'index « Wizard avancé » à cette phase** (le
  sommaire croît par phase, **D-05**). La page y figure déjà dans « Parcours conseillé » (position 3)
  mais **pas dans la table d'index** — c'est le trou à combler. Le test d'exhaustivité
  bidirectionnelle (**D-06**) doit rester vert sans exception ; la liste épinglée des 8 pages reste en
  phase 6.

**Contrôle des renvois obsolètes (critère 5)**

- **D-58:** Le détecteur est **ciblé sur les trois formes obsolètes nommées par le ROADMAP** : (a) un
  menu associé au mauvais libellé, (b) `F7` présenté comme armes distance, (c) l'arrivée
  « directe » dans le wizard. Les attentes du détecteur sont **ancrées** — arborescence et filtres lus
  au code et au rendu réel, chemin d'arrivée lu au flux réellement rendu — jamais écrites de mémoire.
  Limite honnête consignée **dans le test lui-même** : une *autre* inversion, non couverte par ces
  trois formes, ne fera pas échouer la suite ; aucune exhaustivité n'est revendiquée (même arbitrage
  que la limite de **D-26**, phase 2).
- **D-59:** La preuve du critère 5 est **double**, pour être à la fois littérale et relançable :
  **(a)** *ordre TDD* — le détecteur est écrit et **lancé alors que `GUIDE_WIZARD.md` est encore
  obsolète** : le **rouge est réellement observé et consigné**, puis la correction est appliquée et le
  **vert** est réellement obtenu, dans la même phase ; **(b)** *copie figée* — le texte obsolète est
  conservé comme **fixture de test**, et le **même détecteur doit le signaler**, ce qui rend la preuve
  durable et protège le détecteur d'une régression. La fixture est un artefact de `tests/`, avec les
  helpers du `tests/conftest.py` **existant** (**D-12**) ; ce n'est pas une page de documentation.
- **D-60:** Le détecteur **ne doit pas signaler un renvoi légitime** — en particulier le lien vers
  `docs/wizard-avance.md` que cette phase ajoute (D-63) ni les liens vers `docs/parcours-simplifie.md`
  (D-56).
- **D-61:** Le détecteur ne classe jamais `db clear` dans un parcours recommandé, et aucun `db clear`
  n'est exécuté, à aucun moment (**D-22/D-23**, phase 2).

**Redirection `README.md` et dette de renvoi D-44**

- **D-62:** Dans `README.md`, la ligne `**Guide détaillé :** [GUIDE_WIZARD.md](GUIDE_WIZARD.md)`
  (~ligne 63) est **supprimée** — sans texte de remplacement. La section « Documentation utilisateur »
  garde son **lien unique** vers `docs/sommaire.md` (**D-10/D-29**). Aucun renvoi en prose vers
  `GUIDE_WIZARD.md` ni vers `docs/wizard-avance.md` n'est ajouté : rediriger la ligne ferait vivre
  **deux liens vers le sommaire dans le même fichier**, ce qui affaiblit le contrôle de structure et
  crée une seconde formulation du même renvoi (D-17). L'emplacement exact est **vérifié au fichier
  réel** avant édition (D-19).
- **D-63:** La **dette de renvoi D-44 est levée maintenant** : les deux renvois **en prose sans lien**
  de `docs/parcours-simplifie.md` (~lignes 5 et 256) deviennent de **vrais liens** vers
  `docs/wizard-avance.md`, **dans le même commit que la cible**. D-44 attribue explicitement le lien à
  la phase qui crée la page cible ; reporter laisserait la dette ouverte alors que sa condition de
  levée est précisément la création de la cible. **Aucun autre énoncé** de cette page n'est modifié.
- **D-64:** La ligne ~140 de `docs/parcours-simplifie.md` affirme que le wizard affiche `Precedent` /
  `Suivant` là où le résultat affiche `Page prec` / `Page suiv`. Cette affirmation **doit rester vraie
  après cette phase** : la page du wizard cite les libellés **effectivement rendus**, ou le contrôle
  les ancre ; en aucun cas elle ne les contredit.

**Conventions applicables (héritées, sans modification)**

- **D-65:** Les conventions des phases 1 à 3 s'appliquent telles quelles : comparaisons **après
  normalisation** accents/casse/CRLF/balises HTML (**D-11**), helpers dans le `tests/conftest.py`
  **existant** (**D-12**), message d'échec citant **la page, la valeur attendue et le fichier de
  code** (**D-13**), ancrage par **API publique** — client de test Flask et lectures de constantes
  publiques, jamais d'introspection privée (**D-14**) — et exécution de référence
  `.venv/Scripts/python.exe -m pytest -q`, **sans** exécuter `main()`, **sans** écrire sous `.data/`,
  **sans** connexion réseau (**D-15**).
- **D-66:** Aucune modification de `dofus_stuff/**` n'est faite **pour aligner la documentation** : le
  code est le référentiel, la page s'y conforme. Aucun `db clear`, aucune suppression sous `.data/` ni
  `.doc-agent/`. Commits **locaux** uniquement, `git add` **par chemin explicite** (jamais `git add .`).
  Aucune publication, aucun déploiement distant.
- **D-67:** La documentation est **en français**, comme les phases précédentes.

### Claude's Discretion

- Le libellé exact du `H1` de l'aiguillage `GUIDE_WIZARD.md` et le texte de l'avis de déplacement,
  tant que le fichier reste un aiguillage court et ne décrit plus le wizard.
- Le découpage interne des nouveaux tests (module `tests/test_docs_wizard.py` dédié ou extension d'un
  module existant) — seule contrainte : ne pas dupliquer les helpers de `tests/conftest.py` (D-12) et
  conserver le passage `.venv/Scripts/python.exe -m pytest -q` vert.
- La forme concrète de la **fixture** portant la copie figée du texte obsolète (chaîne dans le test,
  donnée structurée, ou fichier de fixture sous `tests/`), tant que le détecteur la signale et que la
  preuve reste relançable.
- Le regroupement des 9 étapes en sous-sections si la page y gagne en lisibilité, tant que **l'ordre
  du code** et les **titres réellement rendus** sont respectés et vérifiables.
- La formulation exacte de la limite honnête de D-58 dans le test.

### Deferred Ideas (OUT OF SCOPE)

- **`docs/base-locale.md` et son renvoi en prose** : `docs/parcours-simplifie.md` renvoie aussi à la
  base locale en prose sans lien. Sa cible est la **phase 5** ; le lien sera ajouté par la phase qui
  crée cette page, selon la règle D-44.
- **Liste épinglée des 8 pages du sommaire** : reste en **phase 6** (D-05/D-57). Cette phase ajoute
  seulement l'entrée d'index de sa propre page.
- **`docs/glossaire.md` et `docs/depannage.md`** : pages listées au sommaire mais non livrées ; elles
  relèvent des phases suivantes, pas de celle-ci.
- Aucune extension de périmètre : le périmètre de la phase est fixé par le ROADMAP et n'a pas été
  élargi pendant la discussion.

</user_constraints>

## Summary

Cette phase est *entièrement interne au dépôt* : aucune documentation tierce, aucun paquet externe,
aucune API à interroger. La « recherche » consiste donc à **mesurer le rendu réel du wizard** et à
extraire la matière exacte que `docs/wizard-avance.md` devra citer — pas à explorer un écosystème.
C'est le prolongement direct de la méthode de la phase 3 (D-32/D-36) : le client de test Flask rend
les écrans en processus, et les libellés sont lus dans ces rendus, jamais écrits de mémoire.

Trois résultats de mesure structurent la planification :

1. **Le wizard est entièrement rendu par `GET`, sans état de session préalable.** Les 9 étapes
   (`/optimize/wizard/slots` … `/optimize/wizard/recap`) répondent **200** sur un client neuf, car
   `load_wizard_spec` retombe sur `default_player_spec(level=200)`. Le contrôle n'a donc **pas**
   besoin de rejouer le parcours classe → éléments → niveau pour rendre les écrans : un seul POST
   `cmd=AVANCE` est nécessaire *seulement* si l'on veut prouver le chemin d'arrivée (D-51).
2. **Le chemin d'arrivée réel atterrit sur `recap`, pas sur `slots`.** Mesure : `POST
   /optimize/quick/niveau` avec `cmd=AVANCE` → `302 /optimize/wizard/recap`. L'affirmation obsolète
   « Vous arrivez **directement** dans le wizard (premier écran : slots et filtres) » est donc fausse
   **deux fois** : l'arrivée n'est pas directe (elle passe par les 3 questions) *et* le premier écran
   atteint est le **récapitulatif**.
3. **`+ID` n'est pas refusé par le code : `+ID` est la syntaxe qui AJOUTE un objet à la liste des
   interdits.** Le message `Syntaxe : +ID | -ID | !ID | CLEAR` (`optimize_wizard.py:424`) n'est levé
   que pour une saisie qui n'est ni `CLEAR`/`clear` ni `<[+-!]><chiffres>`. Le cadrage (« `+ID`
   interdit ») décrit donc **l'effet** de `+ID`, jamais un refus de syntaxe : la page et son test
   doivent écrire les quatre verbes tels que le code les applique — `+ID` = AJOUTER INTERDIT,
   `-ID` = AJOUTER FORCE, `!ID` = RETIRER (BAN OU FORCE), `CLEAR` = VIDER LISTES.

**Primary recommendation:** réutiliser *tel quel* le patron de `tests/test_docs_parcours.py` (client
de test Flask en processus + helpers de `tests/conftest.py` + constats accumulés en une seule
assertion + garde `ast`), rédiger `docs/wizard-avance.md` à partir des rendus mesurés consignés
ci-dessous (§ *Code Examples*), puis implémenter le détecteur de renvois obsolètes comme **une
fonction pure `renvois_obsoletes(texte, faits) -> list[str]`** appliquée à **deux entrées** :
`GUIDE_WIZARD.md` livré (attendu : liste vide) et une **copie figée** du texte obsolète conservée sous
`tests/` (attendu : un constat nommant chacune des trois formes). Le rouge du critère 5 s'obtient en
lançant le détecteur **avant** la réécriture du fichier ; ce run et sa sortie doivent être consignés
dans la tâche 04-04, puis la même commande est relancée verte après correction.

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| WIZ-01 | Un lecteur peut parcourir les étapes du wizard, éditer les formats de caractéristiques et utiliser la syntaxe d'items interdits/forcés | Inventaire mesuré des 9 étapes (titres, corps, pagination) — § *Label inventory* ; formats `B P C W` / `B E C W` mesurés avec leurs séparateurs acceptés et leurs messages d'erreur — § *Formats* ; syntaxe d'items mesurée ligne à ligne (`+ID` → INTERDITS, `-ID` → FORCES, `!ID` → retrait des deux, `CLEAR`/`clear` → listes vidées) avec l'unique message de refus — § *Syntaxe d'items* |
| WIZ-02 | Un lecteur connaît les commandes et les touches réellement actives du wizard | Relevé des couples `F7`/`F8`/`ESC` **par étape** (les libellés changent aux extrémités : `Page prec`/`Suivant` à `slots`, `Precedent`/`Page suiv` à `recap`), des commandes `GO`/`RESET`/`SAVES` et de la correspondance `1`–`8` → `WIZARD_STEPS[n-1]` — § *Touches et commandes* |
| WIZ-03 | `GUIDE_WIZARD.md` ne contredit plus le code : contenu migré vers `docs/wizard-avance.md`, fichier racine réduit à un aiguillage corrigé, `README.md` redirigé | Texte obsolète relevé verbatim avec ses numéros de ligne — § *Les trois formes obsolètes, verbatim* ; spécification du détecteur à double entrée (fichier livré + copie figée) et des valeurs attendues lues au rendu — § *Détecteur de renvois obsolètes* ; contraintes de structure et de liens à respecter — § *Contrats de structure* |

</phase_requirements>

## Project Constraints (from CLAUDE.md)

`./.claude/CLAUDE.md` est le fichier d'instructions projet (`claude_md_path` de `.planning/config.json`).
Directives actionnables pour cette phase, à respecter dans la rédaction **et** dans les tests :

| Directive | Portée pour la phase 4 |
|-----------|------------------------|
| Documentation **intégralement en français** ; code, chemins et identifiants techniques inchangés | Toute page et tout libellé cité restent en français tel que le code les rend |
| **Aucune nouvelle dépendance** pour la documentation (pytest + stdlib seulement) | Interdit d'ajouter un paquet ; le détecteur s'écrit avec `re`, `pathlib`, `unicodedata` déjà utilisés |
| Lecture seule sur `.data/` : jamais de `db clear`, de drop SQLite ni de suppression sous `.data/` | Aucun test de la phase n'écrit sous `.data/` ; `db clear` n'est jamais exécuté (D-22/D-23, D-61) |
| **Hors-ligne par défaut** ; aucune resynchronisation Dofusdude ; aucune publication ni déploiement | Les tests utilisent le client de test Flask sur la fixture `app` (`tmp_path`), donc aucune socket |
| Verification : les critères de « fait » sont **prouvés par des tests pytest réellement exécutés** — aucune validation manuelle, aucun résultat inventé | Le rouge-puis-vert du critère 5 doit être une sortie de commande réellement obtenue et collée |
| Périmètre **strictement documentaire**, limité au besoin initial ; pas de nouveau milestone après livraison | Aucune modification de `dofus_stuff/**` (D-66) |
| Le code est la source de vérité, la doc est le reflet, le test est le juge | Tout libellé affirmé est lu au rendu ou à une constante publique |
| Interdits d'introspection (D-14) : pas d'API privée d'`argparse`, pas d'attributs internes | Le détecteur lit le rendu HTTP et les constantes publiques (`WIZARD_STEPS`, `STEP_TITLES`, `TYPE_FILTER_KEYS`, `TYPE_FILTER_LABELS`) |
| `.claude/CLAUDE.md` porte une **copie du `STACK.md` de la phase 1**, qui prévoyait un test nommé `test_no_obsolete_menu_references` avec l'attente : `3. OPTIMISATION DE STUFF` **absent** de `README.md`, `GUIDE_WIZARD.md` et `docs/**` ; `4. OPTIMISATION DE STUFF` et `5. SYSTEME` **présents** ; motif `` Tapez\s+`?3`?\s+puis `` disparu | **Ce test n'existe pas** dans `tests/` (vérifié : `grep -rn "OPTIMISATION" tests/*.py` ne renvoie que `tests/test_web.py:17`, qui asserte le menu **rendu**). L'attente écrite reste une bonne spécification pour la forme (a) du détecteur de la phase 4 |

*Aucune de ces directives n'entre en conflit avec les décisions D-46…D-67.*

## Architectural Responsibility Map

Le « produit » de cette phase est la documentation, mais sa **source de vérité est le rendu web** : la
carte ci-dessous attribue donc chaque capacité à la couche qui en est propriétaire, pour éviter qu'un
plan ne fasse décrire la prose par le code ou l'inverse.

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|-------------|----------------|-----------|
| Vérité des libellés, titres, touches et formats du wizard | **Produit — `dofus_stuff/web/optimize_wizard.py`** (+ `routes.py`, `solver_spec.py`) | — | Le code est la source de vérité (D-66) ; il n'est pas modifié par cette phase |
| Preuve que le libellé cité existe | **Runtime de rendu — client de test Flask en processus** (`tests/conftest.py::app`) | Constantes publiques (`WIZARD_STEPS`, `STEP_TITLES`, `TYPE_FILTER_KEYS`, `TYPE_FILTER_LABELS`) | Méthode D-32/D-36 de la phase 3 : la surface publique est le seul ancrage autorisé (D-14) |
| Description du flux avancé | **`docs/wizard-avance.md`** (nouvelle page, source unique, D-17) | `docs/parcours-simplifie.md` pour « lire le résultat » / « sauvegarder » (D-38/D-56) | Une seule source par énoncé : la page décrit, les propriétaires restent propriétaires |
| Navigation documentaire (index) | **`docs/sommaire.md`** (table d'index) | — | Le sommaire croît par phase (D-05) ; l'exhaustivité bidirectionnelle reste le signal (D-06) |
| Aiguillage depuis la racine du dépôt | **`GUIDE_WIZARD.md`** réduit à ~15 lignes (D-46) | `README.md` (retrait du pointeur, D-62) | Un aiguillage ne porte aucun énoncé de contenu (D-48) |
| Détection des renvois obsolètes | **Harnais pytest — `tests/`** (module dédié + copie figée) | — | Le test est le juge ; la preuve doit être relançable (D-59) |
| Surface de commandes CLI | **`docs/cli.md`** (propriétaire, inchangé) | renvoi depuis la nouvelle page | D-37/D-52 : le wizard n'existe pas côté CLI, aucune section CLI n'est écrite |

## Standard Stack

### Core

| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| Python | `requires-python = ">=3.11"` (`pyproject.toml`) ; **interpréteur mesuré : `.venv/Scripts/python.exe` → Python 3.14.7** | Écrire les tests d'ancrage | Interpréteur de référence du dépôt (D-15) ; l'interpréteur ambiant n'a pas pytest |
| pytest | `>=8.0` déclaré ; **9.1.1 mesuré** (`.venv/Scripts/python.exe -m pytest --version`) | Prouver les critères | Déjà configuré (`testpaths`, `pythonpath`), 186 tests verts mesurés en 3,65 s |
| `flask.Flask.test_client` (Flask ≥ 3.0, déjà dépendance runtime) | via `tests/conftest.py::app` | Rendre les 9 écrans du wizard en processus | Méthode D-32/D-36 ; aucun serveur, aucun socket, aucune écriture sous `.data/` |
| stdlib `re`, `pathlib`, `unicodedata`, `html` | 3.11+ | Extraire les libellés rendus, normaliser les comparaisons, lire les fichiers | Déjà exposés par `tests/conftest.py` ; zéro dépendance nouvelle |

### Supporting

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| `tests/conftest.py` (fixtures `app`, `client`, `docs_dir`, `normalize`, `section`, `sections`, `lignes_de_code`, `lignes_exemple`) | — | Helpers partagés | **Toujours** : D-12 interdit de dupliquer un helper dans un module de test |
| `dofus_stuff.web.optimize_wizard` (constantes publiques `WIZARD_STEPS`, `STEP_TITLES`, `TYPE_FILTER_LABELS`) | — | Attendre des valeurs au lieu de les écrire | Quand le libellé n'est pas atteignable par le rendu, ou en seconde source |
| `dofus_stuff.model.solver_spec` (`TYPE_FILTER_KEYS`, `MAIN_CARACS`, `EXO_STATS`) | — | Idem | Idem |

### Alternatives Considered

| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| Client de test Flask en processus | Lancer réellement `python -m dofus_stuff.web` et interroger un port | Interdit : socket, serveur, hors-ligne ; D-15 interdit aussi d'exécuter `main()` |
| Client de test Flask | Lire le corps des fonctions `body_*` par `import` | Acceptable pour un message d'erreur, mais **plus faible** : ne prouve pas ce qui est *rendu* (pagination, barre F, ligne de statut). Le rendu reste la référence (D-36) |
| `ast` (extraction sur le source) | `inspect.getsource` / introspection | L'extraction `ast` est le patron **déjà employé** en phase 3 (`display_slots`, `_GROUP_SLOTS`) ; l'introspection privée reste interdite (D-14) |
| Détecteur par fonction pure sur un texte | Détecteur qui lit le fichier lui-même | La fonction pure est ce qui permet de la lancer **sur la copie figée** avec le même code (D-59) — c'est le cœur de la preuve durable |

**Installation :** aucune. `pyproject.toml` ne change pas ; la phase n'ajoute ni dépendance runtime ni extra `dev`.

## Package Legitimacy Audit

**Non applicable — cette phase n'installe aucun paquet externe.**

- Evidence : le chemin de vérification du projet est `pytest` + bibliothèque standard (contrainte
  CLAUDE.md « Aucune nouvelle dépendance pour la documentation »), et la phase ne modifie ni
  `pyproject.toml` ni `.venv` ; aucun `pip install` n'est exécuté.
- Les seuls outils utilisés sont **déjà présents et mesurés** : `.venv/Scripts/python.exe` (3.14.7),
  pytest 9.1.1, git 2.55.0.windows.4.
- Aucun paquet découvert par recherche Web n'est recommandé (aucune recherche Web n'a été nécessaire :
  la matière est intégralement dans le dépôt).

**Packages removed due to [SLOP] verdict:** none — aucun paquet n'a été proposé.
**Packages flagged as suspicious [SUS]:** none.

## Architecture Patterns

### System Architecture Diagram

Deux flux traversent cette phase : le flux **produit** (ce que le lecteur vit, qui définit ce que la
page doit décrire) et le flux **de preuve** (ce que le harnais contrôle).

```
                        FLUX PRODUIT (source de vérité, jamais modifié)
  Lecteur (navigateur)
    │  saisit 4 + Entrée
    ▼
  POST /            (routes.py:214 menu_post)  ──► 4  ──► 302 /optimize
    │                                                        │
    │                                        routes.py:930 optimize_entry
    │                                                        ▼
    │                                    302 /optimize/quick/classe
    │                                            │
    │   cmd=classe/elements/niveau               ▼
    └──────────────────────────►  /optimize/quick/<step>  (routes.py:936)
                                        │  cmd=AVANCE
                                        ▼
                            302 /optimize/wizard/recap
                                        │
                     /optimize/wizard/<step>  (routes.py:1029 optimize_wizard)
                                        │
       ┌────────────────┬───────────────┴────────────┬──────────────────┐
       ▼                ▼                            ▼                  ▼
  body_slots      body_options / body_stat_list   body_items        body_recap
  (OPT-W1)        (OPT-W2…W7)                     (OPT-W8)          (OPT-W9)
       │                │                            │                  │
       └────────────────┴──────────┬─────────────────┴──────────────────┘
                                   ▼
                     _screen() → screen.html → HTML rendu
                       (barre F7/F8/ESC, ligne de statut, PAGE n/t)

                        FLUX DE PREUVE (harnais pytest)
  tests/conftest.py::app (Flask, tmp_path, offline)  ──► GET/POST des écrans
        │                                                       │
        │                                                       ▼
        │                                        libellés, touches, statuts mesurés
        │                                                       │
        ▼                                                       ▼
  docs/wizard-avance.md  ──(comparaison normalisée D-11)──►  constats accumulés ──► 1 assertion

  détecteur (fonction pure)  ──► GUIDE_WIZARD.md livré        (attendu : [])
                             └─► copie figée sous tests/      (attendu : 3 formes nommées)

  garde de structure (existant)  ──► docs/sommaire.md ↔ docs/**/**.md, H1, ligne de retour, liens
```

### Recommended Project Structure

```
.planning/phases/04-wizard-avanc-et-r-sorption-de-la-dette-guide-wizard/
├── 04-CONTEXT.md          # décisions verrouillées (lu)
├── 04-RESEARCH.md         # ce fichier
└── 04-VALIDATION.md       # produit par l'orchestrateur depuis § Validation Architecture

docs/
├── sommaire.md            # + 1 ligne d'INDEX « Wizard avancé » → wizard-avance.md (D-57)
├── wizard-avance.md       # NOUVEAU — source unique du flux avancé (D-50…D-56)
└── parcours-simplifie.md  # 2 renvois en prose → liens (lignes 5 et 256, D-63) ; ligne 140 intacte

GUIDE_WIZARD.md            # réduit à un aiguillage ~15 lignes (D-46/D-47)
README.md                  # ligne 63 supprimée (D-62)

tests/
├── conftest.py            # helpers partagés — RÉUTILISÉS, jamais recopiés (D-12)
├── test_docs_structure.py # garde de structure du sommaire (inchangée, doit rester verte)
├── test_docs_parcours.py  # à MODIFIER : `PAGES_INEXISTANTES` (voir Pitfall 1)
└── test_docs_wizard.py    # NOUVEAU — ancrage du wizard + détecteur + copie figée
```

### Pattern 1: Recette exacte du rendu d'un écran de wizard (mesurée)

**What:** construire les faits (libellés, touches, statuts) en interrogeant l'application Flask en
processus via la fixture `app` de `tests/conftest.py`.
**When to use:** pour **tout** libellé, titre, touche ou format que la page cite.

```python
# Source : tests/conftest.py::app (fixture existante) + tests/test_docs_parcours.py (patron 03-01)
from dofus_stuff.web.optimize_wizard import WIZARD_STEPS

client = app.test_client()                      # D-32 : en processus, hors-ligne, sans socket
# 1) Les 9 ecrans sont rendus SANS etat de session prealable (mesure : 200 sur client neuf) :
for step in WIZARD_STEPS:
    reponse = client.get(f"/optimize/wizard/{step}")      # -> 200 pour les 9 etapes

# 2) Corps visible / ligne de statut / barre de touches : memes marqueurs que la phase 3.
MARQUEUR_CORPS = 'id="body">'
MARQUEUR_STATUT = '<div class="row status'

# 3) Le chemin d'arrivee reel se prouve en 4 appels (mesure) :
c = app.test_client()
assert c.post("/", data={"selection": "4"}).headers["Location"] == "/optimize"
assert c.get("/optimize").headers["Location"] == "/optimize/quick/classe"
c.post("/optimize/quick/classe", data={"cmd": "Cra"})
c.post("/optimize/quick/elements", data={"cmd": "terre"})
assert c.post("/optimize/quick/niveau", data={"cmd": "AVANCE"}).headers["Location"] \
    == "/optimize/wizard/recap"                 # <- atterrit sur recap, pas sur slots
```

### Pattern 2: Les attentes sont lues, jamais écrites (D-13/D-42)

**What:** chaque valeur attendue vient soit du rendu, soit d'une constante publique.
**When to use:** systématiquement, y compris dans le détecteur.

```python
# Source : dofus_stuff/web/optimize_wizard.py:35-45 (STEP_TITLES) et :111-121 (TYPE_FILTER_LABELS)
from dofus_stuff.web.optimize_wizard import STEP_TITLES, TYPE_FILTER_LABELS
from dofus_stuff.model.solver_spec import TYPE_FILTER_KEYS
# F6 / F7 : couples lus a l'index, jamais ecrits de memoire
assert TYPE_FILTER_KEYS[5] == "arme_distance"   # F6
assert TYPE_FILTER_KEYS[6] == "arme_melee"      # F7
assert TYPE_FILTER_LABELS[TYPE_FILTER_KEYS[6]] == "ARMES MELEE"
# Et le rendu le confirme (page 2 de l'ecran slots) :
#   F6. [ON ] ARMES DISTANCE
#   F7. [ON ] ARMES MELEE
```

### Pattern 3: Constats accumulés, une seule assertion (convention héritée)

**What:** collecter des `constats: list[str]` et terminer par **une** assertion qui les joint.
**When to use:** dans chaque test de la phase (leçon mesurée en phase 2 : une assertion par constat
rend des motifs inatteignables et fait échouer la batterie sur une implémentation correcte).

### Pattern 4: Détecteur à double entrée — la preuve du critère 5

**What:** une **fonction pure** appliquée à deux textes : le fichier livré (attendu vide) et une copie
figée du texte obsolète (attendu non vide).
**When to use:** c'est la forme du contrôle du critère 5 (D-58/D-59).

```python
# Source : forme proposee par cette recherche (a valider par le planificateur)
def renvois_obsoletes(texte: str, faits: dict[str, object]) -> list[str]:
    """Formes (a) menu mal apparie, (b) F7 presente comme armes distance, (c) arrivee directe."""
    ...  # voir § "Detecteur de renvois obsoletes" pour le detail des trois predicats

def test_guide_wizard_sans_renvoi_obsolete(docs_dir: Path, app) -> None:
    faits = _faits_mesures(app)                      # menu rendu + redirects + F6/F7 rendus
    texte = (RACINE_DEPOT / "GUIDE_WIZARD.md").read_text(encoding="utf-8")
    assert renvois_obsoletes(texte, faits) == [], ...

def test_detecteur_signale_la_copie_figee(app) -> None:
    faits = _faits_mesures(app)
    copie = (RACINE_DEPOT / "tests" / "fixtures" / "guide-wizard-obsolete.md").read_text(encoding="utf-8")
    constats = renvois_obsoletes(copie, faits)
    assert len(constats) >= 3, "le detecteur ne signale plus la copie figee : regression"
```

### Anti-Patterns to Avoid

- **Rejouer le parcours complet pour rendre un écran** : les 9 écrans sont rendus par un simple `GET`
  (mesuré). Rejouer classe → éléments → niveau à chaque test ajoute des POST inutiles et de l'état de
  session partagé — source de verdicts faux (leçon 03-01 : un client neuf par étape).
- **Écrire `+ID` comme « syntaxe refusée »** : c'est l'inverse du code (mesure). Une page qui écrit
  « `+ID` est interdit » au sens « refusé » serait fausse ; `+ID` **ajoute** à la liste des interdits.
- **Généraliser le détecteur à toute paire `numéro ↔ libellé` de la prose** : la discussion de phase a
  explicitement écarté cette option (faux positifs sur de la prose légitime) au profit d'un détecteur
  ciblé sur les trois formes (D-58).
- **Asserter la chaîne `ON=Retour`** (concaténation de la barre) : elle n'existe pas dans le HTML ;
  la phase 3 exige le **couple** extrait du `span` — même règle ici.
- **Faire entrer `docs/wizard-avance.md` dans la section « limites » de `parcours-simplifie.md`** : le
  contrôle des valeurs volatiles de cette section interdirait alors des ids d'objets et des nombres
  légitimes. Le renvoi D-63 est une phrase d'introduction/de clôture, pas une limite.
- **Citer des valeurs de catalogue** (nombre d'objets, version de jeu, horodatage) : interdiction de
  cadrage, la page décrit des formats et des libellés.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Rendre un écran du wizard en test | Un client HTTP maison, un serveur de test, un `requests` sur un port | La fixture `app` de `tests/conftest.py` + `app.test_client()` | Hors-ligne, en processus, déjà éprouvée (D-32) ; aucune socket, aucun port, aucun risque d'écriture sous `.data/` |
| Normaliser accents/casse/CRLF/HTML | Une seconde fonction de normalisation | La fixture `normalize` (`tests/conftest.py::_normalize`) | D-11/D-12 : un helper dupliqué finit par diverger (leçon WR-04) |
| Extraire une section de page | Un parseur Markdown | La fixture `section` (H2) et le helper local `_sous_section` (H3, déjà écrit en phase 3) | D-12 ; `section` exige la page pour que l'échec soit localisant (D-13) |
| Comparer deux chiffres à quatre chiffres / valeurs volatiles | Une liste noire de nombres | Les règles **scopées** déjà en place (section des limites) | La règle non scopée de 03-04 a été conservée à côté d'une règle scopée, précisément parce qu'un titre dérivé rend la règle scopée inopérante |
| Vérifier qu'une commande existe | Un `subprocess` sur le produit | Le parseur public (`build_parser().parse_args`) | D-15 interdit d'exécuter le produit ; le wizard n'a de toute façon aucune surface CLI (D-52) |
| Détecter les renvois obsolètes | Un vérificateur de liens ou un linter Markdown tiers | Une fonction pure du module de test, sur deux entrées | Contrainte « pytest seul outillage » ; la copie figée est ce qui rend la preuve relançable (D-59) |

**Key insight :** dans ce dépôt, chaque contrôle a déjà son propriétaire. La valeur de la phase 4 se
juge sur ce qu'elle **réutilise** (fixture `app`, `normalize`, `section`, patron de constats) et sur ce
qu'elle **n'invente pas** (libellés, chemins, commandes, arborescence de menus).

## Runtime State Inventory

Cette phase **retire du contenu** d'un fichier de la racine (`GUIDE_WIZARD.md`) et **retire un lien**
de `README.md` : c'est une opération de résorption de dette, pas un renommage de chaîne. L'inventaire
est fait quand même, parce que la question canonique (« après avoir mis à jour chaque fichier du
dépôt, quels systèmes gardent encore l'ancienne chaîne ? ») a une réponse non triviale ici.

| Category | Items Found | Action Required |
|----------|-------------|------------------|
| **Stored data** | **None — vérifié.** Aucune base ni datastore ne stocke `GUIDE_WIZARD` ou une arborescence de menus : `.data/dofus.sqlite3` contient un catalogue d'objets (mesure d'empreinte ci-dessous), et rien dans `dofus_stuff/**` ne référence le wizard par un nom de fichier de doc (aucun `read_text` de doc, aucun chemin `GUIDE_WIZARD` dans le paquet) | Aucune migration de données |
| **Live service config** | **None — vérifié.** Aucun service externe n'est configuré par ce dépôt (hors-ligne par défaut, aucune publication) | Aucune |
| **OS-registered state** | **None — vérifié.** Aucune tâche planifiée, aucun service, aucune entrée de registre : le produit se lance par `python -m dofus_stuff.web` ou `fetcher.py` | Aucune |
| **Secrets / env vars** | **None — vérifié.** Aucune variable d'environnement ni clé de secret ne porte ce nom (`DOFUS_DATA_DIR`, `DOFUS_OFFLINE`, `DOFUS_TIMEOUT`, `DOFUS_SECRET_KEY` sont les seules, lues dans `dofus_stuff/web/__init__.py`) | Aucune |
| **Build artifacts / installed packages** | **Aucun artefact ne porte la chaîne.** `pyproject.toml` déclare `readme = "README.md"` (jamais `GUIDE_WIZARD.md`) ; `dofus_stuff_machine.egg-info/` ne référence que le paquet | Aucune réinstallation |
| **Références hors dépôt suivi (à signaler, non modifiables)** | `./.claude/CLAUDE.md` contient une copie du `STACK.md` de la phase 1 qui cite `GUIDE_WIZARD.md` **et** l'attente `3. OPTIMISATION DE STUFF` absente / `4. OPTIMISATION DE STUFF` + `5. SYSTEME` présentes ; les artefacts GSD (`.gsd-auto/`, `.planning/`) et `.doc-agent/runs/**` citent aussi `GUIDE_WIZARD.md` | **Aucune action** : ce sont des artefacts de cadrage/outillage, non suivis ou non documentaires. Rien n'est supprimé (interdiction de supprimer sous `.doc-agent/`) ; le seul effet utile est que l'attente écrite dans CLAUDE.md **confirme** la forme (a) du détecteur |

**Mesure de non-régression à conserver dans la phase :** empreinte de `.data/dofus.sqlite3` avant et
après la suite entière.

```
AVANT suite : 24989696 octets, mtime_ns 1788730056843137500,
              sha256 e3793d64cb7939ad1a51837b075b6b95e03d64c878fcb9cc07f86c00bb8fef7b
APRES suite : 24989696 octets, mtime_ns 1788730056843137500,
              sha256 e3793d64cb7939ad1a51837b075b6b95e03d64c878fcb9cc07f86c00bb8fef7b
```
`[VERIFIED: exécution locale .venv/Scripts/python.exe -m pytest -q = 186 passed in 3.65s, mesure avant/après sur .data/dofus.sqlite3]`

## Common Pitfalls

### Pitfall 1: La phase 3 interdit explicitement le lien que la phase 4 doit ajouter

**What goes wrong:** `docs/parcours-simplifie.md` doit gagner deux liens vers `docs/wizard-avance.md`
(D-63), mais **deux tests existants** de `tests/test_docs_parcours.py` échouent dès que la chaîne
`](wizard-avance.md)` apparaît dans la page, parce qu'elle y est déclarée inexistante :

```python
# VERIFIED: tests/test_docs_parcours.py:2230-2231
# Pages citees en prose par la section, sans lien : leurs pages n'existent pas encore (D-44).
PAGES_INEXISTANTES = ("wizard-avance.md", "base-locale.md")
```
Le constat est levé dans **deux** tests (mesuré : `test_limites_ancrees_sur_le_code`, ligne 2392, et
`test_page_complete_et_sans_derive`, ligne 2525), sur le **texte entier** de la page
(`if f"]({page_cible})" in texte`), pas seulement sur la section des limites.

**Why it happens :** le contrôle de la phase 3 a été écrit pour l'état d'alors, où la cible n'existait
pas — c'était la bonne lecture de D-44. La condition de levée de D-44 est précisément la création de
la cible, donc **c'est à la phase 4 de faire évoluer ce contrôle**.

**How to avoid:** la phase 4 doit inclure une tâche explicite : réduire
`PAGES_INEXISTANTES` à `("base-locale.md",)` (la cible de la phase 5 reste inexistante) et **ajouter**
dans le nouveau module l'assertion symétrique — le lien vers `wizard-avance.md` **existe** dans
`docs/parcours-simplifie.md` (dette D-44 levée). Le commentaire au-dessus de la constante doit dire
pourquoi elle a changé (leçon : un commentaire faux est pire qu'un commentaire absent).

**Warning signs:** `pytest` vert avant l'édition de la page, rouge après l'ajout du lien, avec un
constat du type « la page lie « wizard-avance.md », qui n'existe pas encore ».

### Pitfall 2: `docs/parcours-simplifie.md` ligne 140 — l'affirmation n'est vraie qu'à moitié

**What goes wrong:** la ligne 140 affirme : « Ces libellés sont ceux du résultat : le wizard avancé,
qui n'est pas décrit ici, affiche `Precedent` et `Suivant` à la place. » **Mesure : faux aux deux
extrémités du wizard.**

```
étape       F7             F8               (mesuré sur le rendu)
slots       Page prec      Suivant          <- f7_url absent : pas d'etape precedente
options     Precedent      Suivant
caracs      Precedent      Suivant
papmpo      Precedent      Suivant
resistances Precedent      Suivant
damages     Precedent      Suivant
misc        Precedent      Suivant
items       Precedent      Suivant
recap       Precedent      Page suiv        <- f8_url absent : pas d'etape suivante
```
La règle est dans `_screen` (`routes.py:137-141`) :
```python
# VERIFIED: dofus_stuff/web/routes.py:137-141
    if total > 1 or f7_url or f8_url:
        f7_label = "Precedent" if f7_url else "Page prec"
        f8_label = "Suivant" if f8_url else "Page suiv"
        tail = [k for k in keys if k[0] in ("F3", "ESC")]
        keys = [("F7", f7_label), ("F8", f8_label)] + tail
```
et `_wizard_step_urls` (`routes.py:1018-1023`) rend `f7=url_for(...step=prev)` **ou `None`** et
`f8=url_for(...step=next)` **ou `None`**.

**Why it happens :** le libellé est dérivé de la **présence d'un voisin**, pas de l'appartenance au
wizard. Une phrase générale « le wizard affiche Precedent/Suivant » est donc une simplification qui
devient fausse sur le premier et le dernier écran.

**How to avoid :** D-63 interdit de modifier un autre énoncé de cette page, et D-64 exige que
l'affirmation « reste vraie ». La seule voie compatible : `docs/wizard-avance.md` **donne le libellé
réel par étape** (tableau ou paragraphe), donc l'ensemble documentaire ne contredit jamais la page du
parcours ; et si le plan veut *ancrer* la ligne 140 par un test, ce test doit être **scopé aux étapes
intermédiaires** (`options` … `items`), jamais aux 9 étapes. Recommandation : ne pas toucher la ligne
140, et porter la précision dans la page du wizard + dans le test du wizard (constat nommant l'étape
si le libellé dérive).

**Warning signs:** un test qui exige `("F7", "Precedent")` et `("F8", "Suivant")` sur les 9 étapes
serait **rouge sur une implémentation correcte** — c'est exactement le travers que la phase 2 a mesuré.

### Pitfall 3: « 11 options » et « 9 étapes » : où le nombre vient-il du code ?

**What goes wrong:** la page doit dire « les 11 options » ; le code ne porte **aucune constante** de
comptage. `body_options` (`optimize_wizard.py:198-215`) écrit onze lignes littérales `1.` … `11.`, et
`apply_options_input` (`optimize_wizard.py:311-347`) porte la table `keys = {1: ..., …, 11: ...}`.

**Why it happens :** la liste est en dur à deux endroits (affichage + validation), sans constante
partagée — contrairement à `WIZARD_STEPS`/`STEP_TITLES`.

**How to avoid:** ancrer le **rendu**, pas une constante privée (D-14). Le test lit la page 1 de
l'écran `options` et extrait les lignes `N. LIBELLE = valeur` rendues ; il exige que la page cite
**chacun** de ces couple `numéro + libellé` et que les numéros rendus soient exactement `1`…`11`.
Le nombre vient donc du rendu, jamais d'un `11` écrit dans le test.

**Warning signs:** un `assert "11 options" in page` — il ne prouve rien et passerait avec dix options.
Ne pas écrire non plus d'accès au dict `keys` (variable locale, pas une API).

### Pitfall 4: `docs/sommaire.md` — trois exigences, et une seule place correcte

**What goes wrong:** ajouter le lien dans « Parcours conseillé » (où le thème figure déjà en texte
numéroté) **satisfait** l'égalité d'ensembles de `problemes_index`, mais contredit la décision de la
phase 1 (parcours conseillé **sans lien markdown**, sinon le contrôle perd sa valeur de signal).

**Why it happens :** `problemes_index` compare l'ensemble des cibles de liens du sommaire à l'ensemble
des `.md` de `docs/`, sans imposer *où* le lien se trouve.

**How to avoid:** exiger la ligne de **table d'index** : `| [Wizard avancé](wizard-avance.md) | … |`.
Trois contrats, tous déjà appliqués par des tests existants et tous à respecter :
1. cible listée → `[Wizard avancé](wizard-avance.md)` dans la table `## Index` ;
2. `H1` de la page **égal au libellé d'index**, comparaison normalisée → `# Wizard avancé` ;
3. ligne de retour en dernière ligne non vide : `[Retour au sommaire](sommaire.md)`.
S'y ajoutent, via `problemes_encodage` : UTF-8 strict, aucun jeton `todo`/`a completer`/`lorem`, et
**au moins 300 caractères** (`LONGUEUR_MINIMALE = 300`, `tests/test_docs_structure.py:315`).

**Warning signs:** `problemes_index` vert mais H1 rouge (« H1 « Wizard avancé (avancé) » différent du
libellé d'index »), ou libellé d'index dupliqué (contrôle `test_sommaire_index_labels_are_unique`).

### Pitfall 5: Le libellé `[ON ]` / `[OFF]` et l'espace de `_on_off`

**What goes wrong:** `_on_off` rend `"ON "` (avec une espace finale) et `"OFF"` (sans), donc le corps
contient `[ON ]` et `[OFF]`. Une page qui écrit `[ON]` ne matche pas la chaîne rendue.

**Why it happens :** l'espace vient de l'alignement fixe `[ON ]`/`[OFF]`
(`optimize_wizard.py:163-165`).
**How to avoid:** la page décrit `ON` / `OFF` en prose et **cite les libellés de slots/filtres**
(`AMULETTE`, `ARMES MELEE`…), pas la forme entre crochets ; le test compare après normalisation (qui
réduit les espaces multiples mais **ne supprime pas** l'espace avant `]`).
**Warning signs:** une assertion sur la chaîne exacte `"[ON ]"` dans la page.

### Pitfall 6: Confondre « rendu du wizard » et « rendu du résultat »

**What goes wrong:** `GO` sur le récapitulatif **exécute le solveur** (`_run_optimize_and_redirect`,
`routes.py:911-928`) et redirige vers `/optimize/result`. Un test du wizard qui poste `GO` (ou une
saisie vide sur le récapitulatif) lance donc un calcul réel — mesure faite : `cmd='GO '` →
`302 /optimize/result`, statut `CALCUL TERME`.
**Why it happens :** `recap` traite `upper in {"", "go"}` comme un lancement (`routes.py:1119-1122`).
**How to avoid:** la phase 3 avait **patché** l'étape de calcul
(`unittest.mock.patch`) pour ne pas lancer le solveur. Le plan doit faire de même si un contrôle doit
observer le lancement, et **ne jamais** poster `GO` pour prouver autre chose ; `RESET`, `SAVES` et
`1`–`8` sont, eux, sans solveur (mesurés).
**Warning signs:** un module de tests de doc qui met 30 s au lieu de 1 s ; ou un test qui échoue parce
qu'aucun objet n'est retourné par un catalogue vide.

### Pitfall 7: Le détecteur signale un renvoi légitime (faux positif)

**What goes wrong:** après correction, `GUIDE_WIZARD.md` **et** `docs/wizard-avance.md` parlent de
menus, de `F7`, et de « wizard ». Un détecteur générique produit des constats sur des textes corrects
(D-60 l'interdit).
**Why it happens :** les formes obsolètes sont des **associations** (numéro ↔ mauvais libellé,
`F7` ↔ « distance », arrivée ↔ « directement »), pas des chaînes isolées.
**How to avoid:** trois précautions, à écrire dans le module :
(a) la forme (a) ne s'applique qu'aux lignes **en forme de menu** (`N. LIBELLE`) et aux phrases
instructives (« tapez `N` … optimisation ») ; (b) la forme (b) n'est évaluée que dans une **fenêtre
courte** autour du jeton `F7` ; (c) la forme (c) n'est cherchée qu'en **phrase affirmative** (une
négation — « vous n'arrivez pas directement » — ne doit pas être signalée).
**Warning signs:** le détecteur signale `GUIDE_WIZARD.md` **après** correction, ou signale le lien
`](wizard-avance.md)` ajouté par D-63.

### Pitfall 8: Le fichier livré `GUIDE_WIZARD.md` n'est vérifié par aucun test aujourd'hui

**What goes wrong:** `test_docs_structure.py` ne parcourt que `docs/**` ; le seul contrôle qui touche
la racine est `test_readme_links_to_sommaire`. Un aiguillage dont les deux liens sont morts passerait
donc la suite.
**Why it happens :** `problemes_liens(docs_dir)` calcule sa racine comme `docs_dir.parent` et
n'itère que sur `_pages(docs_dir)`.
**How to avoid:** le nouveau module doit vérifier explicitement (1) les deux liens de l'aiguillage
(`docs/wizard-avance.md`, `docs/sommaire.md`) résolvent depuis la racine, et (2) `README.md` ne
contient plus `](GUIDE_WIZARD.md)`.
**Warning signs:** aucun test rouge après avoir écrit un lien mort dans `GUIDE_WIZARD.md`.

## Code Examples

> **Statut de cette section :** les valeurs ci-dessous sont **relevées sur le rendu réel** (client de
> test Flask en processus, `create_app(data_dir=tmp_path, offline=True, load_catalog=False)`, client
> neuf, sans état de session) et/ou **lues** dans les sources indiquées. Elles constituent la matière
> première de `docs/wizard-avance.md` : le planificateur peut les reprendre telles quelles dans les
> tâches, et le test les relira au rendu plutôt que de les recopier.

### En-tête commun aux 9 écrans

```python
# VERIFIED: dofus_stuff/web/routes.py:1159-1160 et :1176-1177 ; dofus_stuff/web/screens.py:77-91
pgm=f"OPT-W{WIZARD_STEPS.index(step) + 1}"     # OPT-W1 … OPT-W9
title=f"** WIZARD — {STEP_TITLES[step]} **"
```
En-tête rendu (exemple mesuré, horodatage variable) :
`PGM: OPT-W8               ** WIZARD — ITEMS INTERDITS / FORCES **                2026-09-11 19:51:21`
Champ de saisie : libellé `CMD : [`, `name="cmd"`, `maxlength="40"`, `ENTREE=SUIVANT` sauf au
récapitulatif (`ENTREE=VALIDER`).

### Les 9 étapes, dans l'ordre de `WIZARD_STEPS`

| # | `step` | URL | `pgm` | Titre rendu (`STEP_TITLES`) | Barre F7/F8/ESC | Statut (client neuf) | Corps, page 1 |
|---|--------|-----|-------|------------------------------|-----------------|----------------------|----------------|
| 1 | `slots` | `/optimize/wizard/slots` | `OPT-W1` | `SLOTS ET FILTRES` | `Page prec` / `Suivant` / `Retour` | `PAGE 1/2 — ENTREE=SUIVANT` | `SLOTS (N=TOGGLE) :` + 11 slots + `FILTRES TYPES (F+N) :` + F1…F3 |
| 2 | `options` | `/optimize/wizard/options` | `OPT-W2` | `OPTIONS SOLVEUR` | `Precedent` / `Suivant` / `Retour` | `ENTREE=SUIVANT` | `OPTIONS (N=EDIT) :` + 11 options + `N=CHOISIR OPTION` |
| 3 | `caracs` | `/optimize/wizard/caracs` | `OPT-W3` | `CARACTERISTIQUES` | `Precedent` / `Suivant` / `Retour` | `ENTREE=SUIVANT` | `CARACTERISTIQUES (N=EDIT)  PAGE 1/1` + 6 lignes + `N=EDIT` |
| 4 | `papmpo` | `/optimize/wizard/papmpo` | `OPT-W4` | `PA / PM / PO` | `Precedent` / `Suivant` / `Retour` | `ENTREE=SUIVANT` | `PA / PM / PO (N=EDIT)  PAGE 1/1` + `PA`, `PM`, `Portée` + `N=EDIT` |
| 5 | `resistances` | `/optimize/wizard/resistances` | `OPT-W5` | `RESISTANCES` | `Precedent` / `Suivant` / `Retour` | `PAGE 1/2 — ENTREE=SUIVANT` | `RESISTANCES (N=EDIT)  PAGE 1/2` + 12 lignes + `N=EDIT` |
| 6 | `damages` | `/optimize/wizard/damages` | `OPT-W6` | `DOMMAGES` | `Precedent` / `Suivant` / `Retour` | `PAGE 1/2 — ENTREE=SUIVANT` | `DOMMAGES (N=EDIT)  PAGE 1/2` + 12 lignes + `N=EDIT` |
| 7 | `misc` | `/optimize/wizard/misc` | `OPT-W7` | `DIVERS` | `Precedent` / `Suivant` / `Retour` | `ENTREE=SUIVANT` | `DIVERS (N=EDIT)  PAGE 1/1` + 12 lignes + `N=EDIT` |
| 8 | `items` | `/optimize/wizard/items` | `OPT-W8` | `ITEMS INTERDITS / FORCES` | `Precedent` / `Suivant` / `Retour` | `ENTREE=SUIVANT` | voir § *Syntaxe d'items* |
| 9 | `recap` | `/optimize/wizard/recap` | `OPT-W9` | `RECAPITULATIF` | `Precedent` / `Page suiv` / `Retour` | `ENTREE=VALIDER` | voir § *Récapitulatif* |

`[VERIFIED: rendu mesuré par GET sur les 9 URL avec app.test_client(), cette session]`
`[VERIFIED: dofus_stuff/web/optimize_wizard.py:23-45 — WIZARD_STEPS = ("slots", "options", "caracs", "papmpo", "resistances", "damages", "misc", "items", "recap") ; STEP_TITLES = {"slots": "SLOTS ET FILTRES", "options": "OPTIONS SOLVEUR", "caracs": "CARACTERISTIQUES", "papmpo": "PA / PM / PO", "resistances": "RESISTANCES", "damages": "DOMMAGES", "misc": "DIVERS", "items": "ITEMS INTERDITS / FORCES", "recap": "RECAPITULATIF"}]`

**Points d'exactitude à ne pas rater dans la page :**
- Les étapes 3 à 7 sont **paginées automatiquement** quand le corps dépasse 18 lignes
  (`BODY_LINES = 18`, `screens.py:10`) : `?page=2` est nécessaire pour voir les dernières lignes
  (`resistances` page 2 : lignes 13 `% Résistance dista` et 14 `% Résistance mêlée` ; `damages` page 2 :
  13/14/15). Le libellé est **coupé à 18 caractères** par `_goal_line` (`name[:18]`), ce qui explique
  `% Résistance dista` — la page doit le dire ou citer le nom complet de la liste (`RESISTANCE_STATS`).
- Les 9 étapes sont atteignables **directement par GET** ; une étape inconnue
  (`/optimize/wizard/inconnu`) déclenche `flash("ECRAN WIZARD INCONNU")` et `302 /` (menu).

### Les 11 options de `OPTIONS SOLVEUR` (comptage vérifié)

```text
OPTIONS (N=EDIT) :

1. NIVEAU          = 200
2. JET             = average
3. DUREE (S)       = 5
4. SEED            = (aucun)
5. TOP-K           = 30
6. CP-SAT          = ON
7. STOP SI CIBLES  = OFF
8. AUTO POINTS     = OFF
9. ALLOW POWER     = OFF
10. ALLOW DOMMAGES = OFF
11. ALLOW DOM CRIT = OFF

N=CHOISIR OPTION
```
`[VERIFIED: rendu mesuré]` + `[VERIFIED: dofus_stuff/web/optimize_wizard.py:198-215 — body_options écrit littéralement les lignes « 1. NIVEAU          = {spec.level} » … « 11. ALLOW DOM CRIT = {_on_off(spec.allow_crit_damages_for_elemental).strip()} »]`

Comportement par numéro (`apply_options_input`, `optimize_wizard.py:311-347` ; mesuré) :
- `1`–`5` (`level`, `jet_mode`, `time_limit_s`, `seed`, `top_k`) → **sous-écran d'édition**
  (`pgm=OPT-WED`, titre `** WIZARD — EDITION **`, libellé `VAL : [`, `maxlength=20`) ;
- `6`–`11` (`use_cpsat`, `stop_when_satisfied`, `auto_distribute_points`, `allow_power_for_caracs`,
  `allow_damages_for_elemental`, `allow_crit_damages_for_elemental`) → **bascule immédiate**
  `ON`/`OFF`, sans sous-écran (mesuré : `6` → `CP-SAT = OFF`, statut `OPTION MISE A JOUR`) ;
- refus : hors liste → `OPTION INVALIDE` ; non numérique → `SAISIR UN NUMERO D'OPTION` — les deux
  ramènent sur `?page=1`. Le statut est mis en majuscules et coupé à `COLS` (`routes.py:1131`) :
  `OPTION INVALIDE` sans accent, `SAISIR UN NUMERO D'OPTION` (apostrophe échappée en HTML).

Valeurs acceptées par le sous-écran (mesurées, `apply_option_value`, `optimize_wizard.py:348-366`) :
`level` et `top_k` et `seed` via `int()` (**`1.5` refuse : message Python remonté tel quel
`INVALID LITERAL FOR INT() WITH BASE 10: '1.5'`**), `time_limit_s` via `float()`, `jet_mode` ∈
`min` | `average` | `max` (insensible à la casse ; sinon `JET = MIN|AVERAGE|MAX`), `seed` vide/`-`/
`none`/`aucun` → `(aucun)`, `top_k` **plancher à 1** (`0` et `-3` → `1`). `level` accepte `-5` :
le code **ne borne pas** le niveau du wizard — la page ne doit donc pas promettre une validation.

### Les 11 slots et les 10 filtres (page 1 et page 2 de `slots`)

```text
SLOTS (N=TOGGLE) :                      (page 1)
 1. [ON ] AMULETTE      2. [ON ] ANNEAUX      3. [ON ] CEINTURE
 4. [ON ] BOTTES        5. [ON ] COIFFE       6. [ON ] CAPE
 7. [ON ] ARME          8. [OFF] BOUCLIER     9. [ON ] DOFUS/TROPHEES
10. [ON ] FAMILIER/MONTURE   11. [ON ] PRYSMARADITE
FILTRES TYPES (F+N) :
F1. [ON ] FAMILIER     F2. [ON ] MONTILIER   F3. [ON ] DRAGODINDE

(page 2, ?page=2)                      (troncature attendue : le corps fait plus de 18 lignes)
F4. [ON ] MULDO        F5. [ON ] VOLKORNE   F6. [ON ] ARMES DISTANCE
F7. [ON ] ARMES MELEE  F8. [ON ] DOFUS       F9. [ON ] TROPHEE
F10. [ON ] PRYSMARADITE
N=TOGGLE SLOT  FN=TOGGLE FILTRE
```
`[VERIFIED: rendu mesuré (page 1 et page 2)]` ; `[VERIFIED: dofus_stuff/web/optimize_wizard.py:97-109 — SLOT_GROUP_LABELS ; :111-121 — TYPE_FILTER_LABELS ; dofus_stuff/model/solver_spec.py:43-53 — TYPE_FILTER_KEYS = ("familier", "montilier", "dragodinde", "muldo", "volkorne", "arme_distance", "arme_melee", "dofus", "trophee", "prysmaradite")]`
→ **`F6` = `ARMES DISTANCE` (index 5), `F7` = `ARMES MELEE` (index 6)** : confirmé au rendu *et* au
code. Les libellés de slots viennent de `SLOT_GROUP_LABELS`, les clés de `SLOT_GROUPS`
(`solver_spec.py:15`), dans l'ordre du dictionnaire (11 groupes).

Entrées acceptées / refusées (mesurées, `apply_slots_input`, `optimize_wizard.py:281-308`) :
un nombre `1`–`11` bascule le slot (statut `SLOT/FILTRE MIS A JOUR`) ; `F<n>` avec `1 ≤ n ≤ 10`
bascule le filtre ; **saisie vide = étape suivante** (`302 /optimize/wizard/options`) ; toute autre
saisie → `SAISIE INVALIDE` ; `F11` → `FILTRE INVALIDE` ; désactiver le dernier slot actif →
`AU MOINS UN SLOT REQUIS` (`ValueError("Au moins un slot requis")`, `optimize_wizard.py:305`).
La casse est ignorée (`text.casefold()`), donc `f7` fonctionne (mesuré).

### Les listes de statistiques : noms, ordre, format

| Étape | Source des noms (constante publique) | Contenu rendu (page 1) |
|-------|--------------------------------------|------------------------|
| `caracs` | `MAIN_CARACS` (`solver_spec.py:71-78`) | `1. Vitalité`, `2. Sagesse`, `3. Force`, `4. Intelligence`, `5. Chance`, `6. Agilité` |
| `papmpo` | `EXO_STATS` (`solver_spec.py:80`) | `1. PA`, `2. PM`, `3. Portée` — **le titre de l'écran dit `PA / PM / PO` mais la ligne rendue porte `Portée`** |
| `resistances` | `RESISTANCE_STATS` (`optimize_wizard.py:47-62`) | 14 lignes, 12 en page 1/2 (`% Résistance Neutr`, `Terre`, `Feu`, `Eau`, `Air`, `Résistance Neutre` … `Poussée`), 13–14 en page 2 |
| `damages` | `DAMAGE_STATS` (`optimize_wizard.py:64-80`) | 15 lignes, 12 en page 1/2 (`Dommage`, `Puissance`, `Dommage Critiques`, `Dommage Neutre/Terre/Feu/Eau/Air`, `Dommage Pièges`, `Puissance Pièges`, `Dommage Poussée`, `% Dommages aux sor`), 13–15 en page 2 |
| `misc` | `MISC_STATS` (`optimize_wizard.py:82-95`) | 12 lignes (`Initiative`, `Prospection`, `Invocation`, `Retrait PA`, `Esquive PA`, `Retrait PM`, `Esquive PM`, `% Critique`, `Soin`, `Tacle`, `Fuite`, `Pod`) |

Ligne rendue pour chaque statistique (`_goal_line`, `optimize_wizard.py:167-177`) :

```text
sans exo :  {nom[:18]:18s} B={base:g} P={points:g} C={target:g} W={weight:g}
avec exo :  {nom[:18]:18s} B={base:g} E={exo:g}    C={target:g} W={weight:g}
```
Mesuré : ` 4. Intelligence       B=0 P=0 C=0 W=0` et ` 1. PA                 B=0 E=0 C=0 W=0`.

**Format d'édition des quatre nombres** (`apply_stat_edit`, `optimize_wizard.py:368-397`) —
`[VERIFIED: dofus_stuff/web/optimize_wizard.py:375-397]` :

```python
    parts = raw.replace(",", " ").split()
    if with_exo:
        if len(parts) != 4:
            raise ValueError("Format : BASE EXO CIBLE POIDS")
        base, exo, target, weight = (float(p) for p in parts)
        points = 0.0
    else:
        if len(parts) != 4:
            raise ValueError("Format : BASE POINTS CIBLE POIDS")
        base, points, target, weight = (float(p) for p in parts)
```
- **Quatre valeurs exactement**, séparées par des **espaces ou des virgules** (mesuré : `300,0,0,1`
  est accepté) ; toute autre quantité → message `FORMAT : BASE POINTS CIBLE POIDS` (ou
  `FORMAT : BASE EXO CIBLE POIDS`) affiché dans la ligne de statut.
- Les valeurs sont des **flottants** ; une lettre → message Python brut remonté en majuscules
  (`COULD NOT CONVERT STRING TO FLOAT: 'A'`).
- Sous-écran d'édition (`pgm=OPT-WED`, `** WIZARD — EDITION CARAC **`, libellé `VAL : [`,
  `maxlength=40`), corps mesuré :
  ```text
  EDITION : INTELLIGENCE
  ACTUEL : B=0 P=0 C=0 W=0
  FORMAT : BASE POINTS CIBLE POIDS

  NOUVELLE VALEUR (ENTREE VIDE = ANNULER) :
  ```
  et pour `papmpo` : `ACTUEL : B=0 E=0 C=0 W=0` / `FORMAT : BASE EXO CIBLE POIDS`
  (`[VERIFIED: dofus_stuff/web/routes.py:1251-1260]`).
- **Entrée vide = annuler** (aucune écriture, retour à la liste) ; saisie valide → statut
  `CARAC ENREGISTREE` (et `VALEUR ENREGISTREE` pour une option).
- Édition d'une ligne : taper son **numéro** (statut `Saisir le numero de la ligne` si non numérique,
  `NUMERO INVALIDE` hors liste) ; l'écran de liste affiche `N=EDIT`.

### Syntaxe d'items (`ITEMS INTERDITS / FORCES`) — mesurée

Corps rendu (client neuf) :
```text
ITEMS — SYNTAXE :
  +ID   AJOUTER INTERDIT
  -ID   AJOUTER FORCE
  !ID   RETIRER (BAN OU FORCE)
  CLEAR VIDER LISTES

INTERDITS (0) : (aucun)
FORCES (0) : (aucun)
```
`[VERIFIED: dofus_stuff/web/optimize_wizard.py:240-260 — body_items, littéraux « ITEMS — SYNTAXE : », «   +ID   AJOUTER INTERDIT », «   -ID   AJOUTER FORCE », «   !ID   RETIRER (BAN OU FORCE) », «   CLEAR VIDER LISTES », « INTERDITS ({n}) : … » ou « (aucun) » ; rendu mesuré]`

Comportement mesuré (`apply_items_input`, `optimize_wizard.py:399-425`) :

| Saisie | Effet mesuré | Statut |
|--------|--------------|--------|
| `+12345` | `INTERDITS (1) : #12345` | `LISTE ITEMS MISE A JOUR` |
| `-12345` | `FORCES (1) : #12345` | `LISTE ITEMS MISE A JOUR` |
| `!12345` | retire des **deux** listes | `LISTE ITEMS MISE A JOUR` |
| `CLEAR` **ou `clear`** | vide les deux listes | `LISTE ITEMS MISE A JOUR` |
| `  -42  ` | espaces autour acceptés → `FORCES (1) : #42` | `LISTE ITEMS MISE A JOUR` |
| `abc`, `+abc`, `12345` | **refus** | `SYNTAXE : +ID | -ID | !ID | CLEAR` |
| *(vide)* | passe à `recap` (pas un refus) | `302 /optimize/wizard/recap` |

- Le message de refus est **exactement** `ValueError("Syntaxe : +ID | -ID | !ID | CLEAR")`
  (`optimize_wizard.py:424`), rendu en majuscules avec l'apostrophe échappée :
  `SYNTAXE : +ID | -ID | !ID | CLEAR`.
- **`+ID` n'est pas refusé** : c'est le verbe « AJOUTER INTERDIT ». Un identifiant **sans** préfixe
  (`12345`) est refusé.
- Un id ajouté à une liste est **retiré de l'autre** (`bans.discard` / `forced.discard`) : un objet ne
  peut pas être interdit et forcé en même temps (le guide actuel le dit déjà, à juste titre).
- Affichage tronqué au-delà de 8 entrées : `INTERDITS (10) : #1001, … #1008` puis ligne `… +2`
  (mesuré) ; l'ellipse est le caractère `…`.

### Récapitulatif, touches et commandes — mesurés

```text
NIVEAU 200  JET=average  DUREE=5s
SLOTS : amulet, rings, belt, boots, hat, cape, weapon, dofus, pet, prysma
POIDS : (aucun — defaut INT)
CIBLES : (aucune)
BAN=0 FORCE=0
STOP=False AUTO=False
POWER=False DMG=False CRIT=False

GO = LANCER  RESET = REINITIALISER  1-8 = RETOUR ECRAN
SAVES = STUFFS SAUVEGARDES
```
`[VERIFIED: dofus_stuff/web/optimize_wizard.py:262-279 — body_recap ; rendu mesuré]`

| Saisie au récapitulatif | Effet mesuré | Statut |
|-------------------------|--------------|--------|
| `GO` (ou vide) | lance le solveur, `302 /optimize/result` | `CALCUL TERME` |
| `RESET` / `reset` | remet le wizard à zéro, `302 /optimize/wizard/slots` | `WIZARD REINITIALISE` |
| `SAVES` / `saves` | `302 /saves` (écran `SAV-01`) | — |
| `1` … `8` | `302 /optimize/wizard/<WIZARD_STEPS[n-1]>` (mesuré : `1`→`slots`, `3`→`caracs`, `8`→`items`) | — |
| `9`, `0`, `-1`, `abc` | **refus** | `GO | RESET | SAVES | 1-8` |

- `GO` est le **seul** chemin de cette phase qui exécute le solveur (`routes.py:1114-1116` →
  `_run_optimize_and_redirect`, `routes.py:911-928`). Le libellé `SAVES = STUFFS SAUVEGARDES` figure
  aussi dans le corps du récapitulatif (`body_recap`), donc la page peut le citer depuis le rendu.
- La **barre de touches du récapitulatif** est `F7=Precedent`, `F8=Page suiv`, `ESC=Retour` : le
  libellé `Page suiv` apparaît **alors qu'il n'y a aucune pagination** (conséquence directe de
  `f8_url is None`, `routes.py:137-141`). Détail à ne pas contredire.

### Chemin d'arrivée réel — mesuré pas à pas

```text
POST /            data={"selection": "4"}   -> 302 /optimize
GET  /optimize                              -> 302 /optimize/quick/classe   (routes.py:930-932)
POST /optimize/quick/classe   cmd=Cra       -> 302 /optimize/quick/elements
POST /optimize/quick/elements cmd=terre     -> 302 /optimize/quick/niveau
POST /optimize/quick/niveau   cmd=AVANCE    -> 302 /optimize/wizard/recap    <- RECAP
```
Autres mesures utiles :
- `POST /` avec `selection=3` → `/sets`, `selection=5` → `/system`, `selection=1` → `/search` ;
  la barre de touches du menu principal n'affiche que `F3=Quitter` (cohérent avec
  `docs/installation.md:69`).
- `AVANCE` est reconnu **quelle que soit la casse** (`cmd.upper() == "AVANCE"`, `routes.py:948`) et
  fonctionne depuis les trois étapes ; **sans** classe + éléments enregistrés, il appelle
  `reset_wizard(session)` puis va quand même sur `recap` (mesuré : `POST /optimize/quick/classe`
  `cmd=AVANCE` → `302 /optimize/wizard/recap`).
- Le récapitulatif atteint par `AVANCE` **porte déjà la spec recommandée** (mesuré : `SLOTS : amulet,
  rings, belt, boots, hat, cape, weapon, shield, dofus, pet, prysma` et des `POIDS`/`CIBLES` non vides,
  parce que `recommendation_spec(classe, elements, niveau)` a été enregistrée). Le premier écran
  **slots** n'est donc pas l'écran d'arrivée : on y arrive par `RESET` ou par `1` depuis le
  récapitulatif.

### Détecteur de renvois obsolètes — les trois formes, verbatim, et où sont les attentes

**Texte obsolète actuel (verbatim, `GUIDE_WIZARD.md`, version en dépôt)** — les trois extraits sont
cités tels quels, en bloc indenté (le fichier source contient lui-même des délimiteurs de bloc) :

&nbsp;

    forme (a1) — arborescence inversée, GUIDE_WIZARD.md:35-42 :
        Tapez `3` puis **Entrée** pour ouvrir l’optimisation.

        1. RECHERCHE D'OBJETS
        2. LISTE DES EQUIPEMENTS
        3. OPTIMISATION DE STUFF

        4. SYSTEME

    forme (c) — arrivée « directe », GUIDE_WIZARD.md:45 :
        Vous arrivez **directement** dans le wizard (premier écran : slots et filtres).

    forme (b) — F7 présenté comme armes distance, GUIDE_WIZARD.md:157 :
        Exemple : pour **interdire les armes à distance**, tapez `F7` (selon la liste affichée) jusqu’à voir `OFF`.

    occurrences secondaires de la forme (a) — le numéro de SYSTEME, GUIDE_WIZARD.md:50 et :328 :
        L’option **4. SYSTEME** regroupe le reste : détail d’un équipement par ID, version locale, …
        - Les données viennent de la **base locale** (menu `4. SYSTEME` → `4. GESTION DE LA BASE` / sync) :

&nbsp;

*(numéros de ligne vérifiés par `grep -n` sur le fichier de 330 lignes. Les deux occurrences
secondaires comptent : `4` est le numéro de l'**optimisation**, `SYSTEME` est en `5` — un détecteur
de la forme (a) qui ne chercherait que `3. OPTIMISATION` laisserait passer deux renvois faux du même
document. Le prédicat (a1) les attrape tous les deux, puisqu'il compare le numéro au libellé rendu.)*

**Où les attentes doivent être LUES (jamais écrites de mémoire) :**

| Forme | Attente | Lecture |
|-------|---------|---------|
| (a) | Le menu réel compte **5 entrées** ; `4. OPTIMISATION…` ouvre l'optimisation ; `3.…PANOPLIES` ; `5. SYSTEME` | **Rendu** : `GET /` → corps `1. RECHERCHE D'OBJETS`, `2. LISTE DES EQUIPEMENTS`, `3. LISTE DES PANOPLIES`, `4. OPTIMISATION DE STUFF`, `5. SYSTEME` ; **routage** : `POST /` `selection=N` → `Location` (mesuré : `4 → /optimize`, `3 → /sets`, `5 → /system`) — donc le numéro « qui ouvre l'optimisation » est **mesuré**, pas supposé |
| (b) | `F6` = `ARMES DISTANCE`, `F7` = `ARMES MELEE` | **Rendu** : page 2 de `/optimize/wizard/slots` ; **seconde source** : `TYPE_FILTER_KEYS[5]`/`[6]` + `TYPE_FILTER_LABELS` |
| (c) | L'arrivée passe par les 3 questions ; le premier écran atteint est `recap` | **Rendu** : chaîne de redirections ci-dessus (`POST /` → `/optimize` → `/optimize/quick/classe` → … → `/optimize/wizard/recap`) |

**Forme concrète recommandée pour chaque prédicat** (fonction pure `renvois_obsoletes(texte, faits)`) :

1. **Forme (a) — menu mal apparié.** Deux sous-formes, toutes deux ciblées :
   - *(a1) ligne en forme de menu.* Pour chaque ligne du texte qui matche `^\s*(\d)\.\s+([A-ZÀ-ÿ' /-]{3,})$`
     (donc *pas* la prose), si le numéro est un numéro du menu réel et que le libellé de la ligne
     **n'est pas contenu** dans le libellé rendu de ce numéro → constat
     « menu `3` associé à `OPTIMISATION DE STUFF` ; le rendu associe `3` à `LISTE DES PANOPLIES` ».
     Règle de contenance (sous-chaîne, après normalisation D-11) et non d'égalité, parce que
     l'aiguillage corrigé écrit des **abréviations** : `OPTIMISATION` ⊂ `OPTIMISATION DE STUFF` et
     `PANOPLIES` ⊂ `LISTE DES PANOPLIES`. **Si le plan préfère l'égalité stricte, alors l'aiguillage
     doit citer les libellés rendus complets et D-47 doit être reformulé** — c'est un arbitrage à
     trancher explicitement (voir Open Question 1).
   - *(a2) phrase instructive.* Sur les phrases contenant `tapez`/`saisissez` **et** un jeton backtické
     numérique `` `N` ``, si la phrase contient aussi le mot `optimisation` et que `N` n'est pas le
     numéro mesuré qui ouvre l'optimisation (`4`) → constat. Cette sous-forme attrape « Tapez `3` puis
     Entrée pour ouvrir l'optimisation » sans toucher à un « tapez `3` » qui parlerait des panoplies.
2. **Forme (b) — `F7` présenté comme armes distance.** Pour chaque phrase contenant le jeton `F7`
   (casse ignorée, backticks ignorés), si la phrase contient un mot de distance (`distance`,
   `à distance`, `armes à distance`) **et** ne contient pas le libellé rendu de `F7` (`ARMES MELEE`)
   → constat. Fenêtre = **la phrase**, pas le fichier : c'est ce qui évite les faux positifs avec
   `% Résistance distance` ou `% Dommages distance`, qui vivent dans d'autres phrases.
3. **Forme (c) — arrivée « directe ».** Pour chaque phrase contenant `directement` **et** `wizard` :
   si aucun marqueur de négation (` pas `, `n'`, `jamais`, `ne … pas`) n'est présent dans la phrase →
   constat. Cette garde est indispensable : la page corrigée **peut** écrire « vous n'arrivez pas
   directement dans le wizard » pour corriger explicitement la croyance, et D-60 interdit alors un
   constat.

**Faux positifs à craindre (à écrire dans le test) :**
- La forme (a1) sur une **légende de tableau** ou une liste numérotée de procédure (`1.`, `2.`, `3.`)
  qui n'est pas une arborescence de menu → d'où le filtre « ligne en forme de menu » et la
  comparaison au libellé rendu **du même numéro**.
- La forme (b) sur `F7` cité pour dire « F7 = l'écran précédent » (navigation) dans une phrase qui
  parle aussi de distance résiduelle.
- La forme (c) sur une **négation**, sur « directement » employé pour autre chose (ex. « le résultat
  s'affiche directement »), ou sur `wizard` employé comme nom du fichier `GUIDE_WIZARD.md`.
- Le détecteur ne doit **jamais** considérer `](wizard-avance.md)` comme un renvoi obsolète (D-60).

**Copie figée (D-59b) — recommandation :** un fichier `tests/fixtures/guide-wizard-obsolete.md`
contenant les **trois extraits verbatim** ci-dessus (le reste du fichier n'est pas nécessaire : le
détecteur est en phrases/lignes). Avantages mesurés : (1) aucune structure de `docs/` n'est touchée —
`_pages(docs_dir)` ne parcourt que `docs/`, `problemes_index` ne lit que `docs/sommaire.md`, donc un
`.md` sous `tests/` n'entre dans **aucun** contrôle existant (vérifié) ; (2) la preuve reste
relançable et lisible ; (3) le détecteur est testé contre un texte **réellement obsolète**, pas contre
une chaîne fabriquée pour lui plaire.

**Limite honnête à consigner dans le test (D-58/D-26, formulation au choix) :** le détecteur couvre
**trois formes nommées** ; une *autre* inversion (par ex. un numéro d'étape du wizard mal associé, ou
un libellé de slot mal apparié dans un autre document) ne fera pas échouer la suite. Aucune
exhaustivité n'est revendiquée ; la complétude générale est portée par les contrôles de structure et
d'ancrage, pas par ce détecteur.

### Contrats de structure et de liens (ce qui existe déjà et doit rester vrai)

| Fichier | Contrôle existant | Effet pour cette phase |
|---------|-------------------|------------------------|
| `docs/sommaire.md` | `problemes_index` : les **cibles de liens** du sommaire == les `.md` de `docs/` (hors `sommaire.md`) | Ajouter **exactement une** cible `wizard-avance.md` (la page doit exister, sinon « cible listée absente sur disque ») |
| `docs/wizard-avance.md` | `problemes_h1` : un `H1` unique **égal au libellé d'index** (normalisé) | Libellé d'index et `H1` doivent coïncider (ex. `Wizard avancé`) |
| toutes les pages `docs/` | `problemes_retour_sommaire` : au moins un lien dont la cible résolue est `docs/sommaire.md` | Dernière ligne non vide : `[Retour au sommaire](sommaire.md)` (convention mesurée sur les 4 pages existantes) |
| toutes les pages `docs/` | `problemes_liens` : cibles relatives résolues, **sans `#`**, sans chemin absolu, sans `\`, sans `file://`, et sous la racine du dépôt | Les liens sortants de la nouvelle page (`parcours-simplifie.md`, `sommaire.md`) sont des liens de fichier à fichier |
| toutes les pages `docs/` | `problemes_encodage` : UTF-8 strict, pas de `todo`/`a completer`/`lorem`, ≥ `300` caractères | La page est longue, aucun jeton de brouillon |
| toutes les pages `docs/` | Encodage mesuré : **CRLF, UTF-8 sans BOM** sur les 4 pages existantes et sur `README.md`/`GUIDE_WIZARD.md` | Écrire la nouvelle page en **CRLF sans BOM** (le contrôle CRLF n'existe que pour `parcours-simplifie.md`, mais la convention est celle de tout `docs/`) |
| `README.md` | `test_readme_links_to_sommaire` : **exactement 1** cible `docs/sommaire.md` | Supprimer la ligne 63 ne change pas ce compte (le lien vers le sommaire est ligne 7) ; ajouter un second lien le ferait rougir |
| `docs/cli.md` | phase 2 : tableaux d'options, exemples analysables | **Inchangé** ; la nouvelle page ne recopie aucune commande (D-52) |

### Textes exacts à préserver ou modifier (relevés au fichier réel)

```text
# README.md:63 — a SUPPRIMER (D-62), sans texte de remplacement
**Guide détaillé :** [GUIDE_WIZARD.md](GUIDE_WIZARD.md)

# README.md:7 — le lien unique a CONSERVER tel quel (D-10/D-29)
La documentation utilisateur commence par un sommaire unique : [Sommaire de la documentation](docs/sommaire.md).

# docs/parcours-simplifie.md:5 — 1er renvoi en prose a convertir en lien (D-63)
Toutes les affirmations de cette page viennent du rendu réel de la vue web. La surface des commandes
n'est pas recopiée ici : elle appartient à [la page CLI](cli.md). Les écrans du wizard avancé et le
fonctionnement de la base locale seront décrits dans les pages qui leur seront consacrées. Le parcours
en ligne de commande, lui, ne pose pas ces trois questions : …

# docs/parcours-simplifie.md:140 — a NE PAS modifier (D-63/D-64), voir Pitfall 2
… Ces libellés sont ceux du résultat : le wizard avancé, qui n'est pas décrit ici, affiche
`Precedent` et `Suivant` à la place.

# docs/parcours-simplifie.md:256 — 2e renvoi en prose a convertir en lien (D-63)
Les **réglages avancés** (les écrans du wizard) et le fonctionnement de la **base locale** ne sont pas
décrits ici : chaque sujet appartient à la page qui lui sera consacrée, et cette page ne dit que ce que
le parcours simplifié en montre. …

# docs/installation.md:69 — coherence a PRESERVER (ligne 62-63 : F7/F8)
- La barre de raccourcis affichée en bas d'écran est construite dynamiquement : sur le menu principal
elle n'affiche que `F3` (« Quitter ») ; `F7` et `F8` n'y apparaissent que sur un écran paginé ou à une
étape du wizard. Les touches du tableau restent actives partout, même quand la barre ne les montre pas.
```

**Contraintes croisées supplémentaires, mesurées :**
- Le test de phase 3 `test_limites_ancrees_sur_le_code` exige que `docs/parcours-simplifie.md` contienne
  encore, dans la section `## Ce que l'outil ne fait pas`, les tournures **`réglages avancés`** et
  **`base locale`** (`RENVOIS_SANS_LIEN`). Convertir la ligne 256 en lien **doit conserver ces mots**.
- Ce même test interdit, dans cette section, tout nombre de trois chiffres ou plus sauf `COLS` (100).
  La phrase D-63 de la ligne 256 ne doit donc introduire **aucun** nombre.
- `test_page_complete_et_sans_derive` exige que la dernière ligne non vide de
  `docs/parcours-simplifie.md` reste exactement `[Retour au sommaire](sommaire.md)` et que les neuf
  titres de niveau 2 restent dans l'ordre : le lien D-63 s'ajoute **dans** un paragraphe existant.
- Le renvoi de la ligne 256 couvre **deux** cibles (`wizard` + `base locale`) qui sont deux pages
  différentes : une seule syntaxe de lien ne peut pas couvrir les deux. Voir Open Question 3.

### L'exemple guidé à migrer (§ 8 du guide) — vérifié contre le code

| Affirmation de `GUIDE_WIZARD.md` § 8 | Verdict mesuré |
|---------------------------------------|----------------|
| « Menu → `3` » | **FAUX** → `4`, puis les 3 questions, puis `AVANCE` (forme (a2) + (c)) |
| « **Slots** : laissez les défauts (Entrée vide / F8) » | Vrai en soi, mais l'arrivée réelle est `recap` : les écrans ne se suivent pas dans cet ordre depuis l'arrivée |
| « **Options** : `1` puis `123` » | Vrai (mesuré : `EDITION : LEVEL` puis `1. NIVEAU = 123`) |
| « Caractéristiques : trouvez **Intelligence** (souvent ligne `4`) » | Vrai (mesuré : `MAIN_CARACS[3]` = `Intelligence`, ligne ` 4.`) |
| « saisie : `300 0 0 1` » | Vrai (mesuré : `4. Intelligence B=300 P=0 C=0 W=1`) ; la justification « base 200 + parchemins 100 » est une décision du lecteur, pas une contrainte du code (`scroll` n'est pas éditable dans le wizard) |
| « **Variante cible PA** : `6 0 11 5` sur l'écran PA / PM / PO » | **VRAI, porté par le code** (mesuré : `1. PA B=6 E=0 C=11 W=5`, format `BASE EXO CIBLE POIDS`) — la variante **survit** à la vérification (D-55) |
| § 10 « Erreur rouge après saisie → relire le format (souvent 4 nombres, ou `+ID`) » | Ambigu après mesure : `+ID` **n'est pas** une erreur ; les erreurs réelles sont `SYNTAXE : +ID | -ID | !ID | CLEAR`, `FORMAT : BASE POINTS CIBLE POIDS`, `SAISIR LE NUMERO DE LA LIGNE`, `NUMERO INVALIDE` |
| § 7 « lire le résultat », « `SAVE` », « `SAVES` », « jusqu'à 20 entrées » | **Propriété de `docs/parcours-simplifie.md`** (D-38/D-49) : renvoi par lien, aucune recopie |

### Vérification du run de référence (mesure de la session)

```bash
./.venv/Scripts/python.exe -m pytest -q      # -> 186 passed in 3.65s
./.venv/Scripts/python.exe -c "…empreinte .data/dofus.sqlite3…"   # inchangée avant/après
```
`[VERIFIED: exécution réelle cette session, sortie citée ci-dessus]`

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Guide unique à la racine (`GUIDE_WIZARD.md`, 330 lignes) décrivant tout le flux avancé | Pages `docs/` à plat, une par thème, adossées au code et gardées par pytest | Phases 1→3 (ce milestone) | `GUIDE_WIZARD.md` devient un aiguillage : la source unique est `docs/wizard-avance.md` |
| Contrôle « à l'œil » des libellés | Ancrage mesuré au rendu (client de test Flask) + normalisation (D-11) | Phase 3 (D-32/D-36) | Un libellé qui dérive fait rougir la suite sans qu'un humain ait à relire |
| Détecteur générique de renvois obsolètes (idée initiale) | Détecteur **ciblé** sur trois formes + copie figée + limite honnête écrite dans le test | Discussion de phase 4 (D-58/D-59) | Le contrôle reste falsifiable et relançable sans produire de faux positifs sur de la prose légitime |

**Deprecated/outdated :**
- L'affirmation « tapez `3` puis Entrée pour ouvrir l'optimisation » : le menu réel route `4`.
- L'arborescence `3. OPTIMISATION DE STUFF` / `4. SYSTEME` : le rendu donne `3. LISTE DES PANOPLIES` /
  `4. OPTIMISATION DE STUFF` / `5. SYSTEME`.
- `F7` = armes distance : c'est `F6`.
- « Vous arrivez directement dans le wizard » : l'arrivée passe par les 3 questions et atterrit sur
  `recap`.
- `GUIDE_WIZARD.md` comme « Guide détaillé » du `README.md` : la ligne est supprimée (D-62).

## Assumptions Log

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|---------------|
| A1 | Le détecteur doit comparer les libellés de menu de l'aiguillage par **contenance** (sous-chaîne) et non par égalité, parce que D-47 prescrit des abréviations (`OPTIMISATION`, `PANOPLIES`) là où le rendu écrit `OPTIMISATION DE STUFF` et `LISTE DES PANOPLIES` | § *Détecteur*, forme (a1) | Une comparaison par égalité ferait rougir l'aiguillage **correct** ; une comparaison trop lâche laisserait passer une inversion d'un autre numéro. Arbitrage à confirmer au plan (Open Question 1) |
| A2 | La copie figée prend la forme d'un fichier `tests/fixtures/guide-wizard-obsolete.md` | § *Détecteur*, copie figée | Aucun contrôle existant ne parcourt `tests/`, donc le risque est faible ; si le plan préfère une constante dans le module, la preuve reste équivalente (D-59 laisse le choix) |
| A3 | La ligne 140 de `docs/parcours-simplifie.md` reste **inchangée** et c'est `docs/wizard-avance.md` qui porte la précision par étape | Pitfall 2 | Si le plan choisit de corriger la ligne 140, il contredit D-63 (« aucun autre énoncé n'est modifié ») et doit le signaler comme écart assumé (patron ÉCR-1…ÉCR-5 de la phase 3) |
| A4 | Le renvoi D-63 de la ligne 256 est attaché à la seule clause « wizard » (la clause « base locale » reste en prose, cible phase 5) | § *Textes exacts*, ligne 256 | Un lien vers `base-locale.md` serait un lien mort et ferait rougir `problemes_liens` |
| A5 | `docs/wizard-avance.md` cite les libellés de slots/filtres **sans** la forme entre crochets `[ON ]`/`[OFF]` | Pitfall 5 | Une assertion sur `[ON ]` (espace avant `]`) ferait rougir la page si elle écrit `[ON]` |
| A6 | La page ne documente **pas** le niveau `-5` / la durée négative comme des entrées valides (le code ne les borne pas, mais les présenter comme normales serait trompeur) | § *Les 11 options* | La page doit rester « telle que le code l'applique » (critère 2) sans transformer une absence de borne en mode d'emploi |

## Open Questions (RESOLVED)

**Statut : les six questions sont RESOLVED par le jeu de plans de la phase 4 (`04-01` a `04-04`).**
Aucune n'est restee ouverte et aucune n'a ete renvoyee au porteur du projet : le lieu d'arbitrage de
chacune est nomme ci-dessous, et sa resolution est reportee **inline** sous chaque question. Cette
section ne tranche rien de neuf — elle **consigne** ce que les quatre `PLAN.md` ont deja decide, et
chacune de ces resolutions s'adosse a une decision verrouillee de `04-CONTEXT.md` (D-46 a D-67), qui
restent telles quelles.

| # | Question | Resolution retenue et lieu d'arbitrage |
|---|----------|----------------------------------------|
| 1 | Egalite ou contenance pour les libelles de menu du detecteur ? | **Contenance par mot significatif** ; la recommandation d'egalite stricte est **ecartee** (D-47 prescrit les formes abregees, donc l'egalite stricte rendrait le vert du critere 5 inatteignable). Arbitre par `04-04-PLAN.md` tache 1, `_renvois_au_menu`. |
| 2 | Forme exacte de la copie figee ? | **Fichier** `tests/fixtures/guide-wizard-obsolete.md` (recommandation adoptee telle quelle), annonce en en-tete HTML comme piece de test et signale par le **meme** detecteur. Arbitre par `04-04-PLAN.md` tache 1. |
| 3 | Conversion du renvoi de la ligne 256, qui couvre deux cibles ? | Adoptee et **elargie** : les **deux** renvois en prose (~lignes 5 et 256) deviennent de vrais liens vers `wizard-avance.md` ; la clause « base locale » n'est pas liee, les mots exiges restent litteraux. Arbitre par `04-03-PLAN.md` tache 2. |
| 4 | Le controle de la ligne 140 doit-il exister, et a quel perimetre ? | Adoptee : ancrage **par etape** au rendu, assertion `Precedent`/`Suivant` **scope aux etapes 2 a 8**, et la ligne ~140 reste **inchangee** (D-64). Arbitre par `04-02-PLAN.md` tache 2, `test_touches_et_commandes_par_etape`. |
| 5 | `GUIDE_WIZARD.md` et `README.md` couverts par des controles de liens ? | Adoptee et **renforcee** : liens de l'aiguillage exiges et existants, `README.md` sans `GUIDE_WIZARD` avec un seul lien vers le sommaire, et toute cible de l'aiguillage **declaree** et **existante**. Arbitre par `04-03-PLAN.md` taches 1 et 2. |
| 6 | Le lancement `GO` doit-il etre prouve ? | Tranchee par la **seconde branche** de la recommandation : `GO` **n'est jamais poste**, seule sa citation au rendu est controlee ; la garde `ast` du harnais refuse tout appel portant `"cmd": "GO"`. Arbitre par `04-02-PLAN.md` tache 2 et `04-01-PLAN.md` tache 1. |

1. **Égalité ou contenance pour les libellés de menu du détecteur ?**
   - Ce qu'on sait : D-47 prescrit `4. OPTIMISATION`, `3. PANOPLIES`, `5. SYSTEME` ; le rendu donne
     `4. OPTIMISATION DE STUFF`, `3. LISTE DES PANOPLIES`, `5. SYSTEME`.
   - Ce qui n'est pas tranché : le plan peut écrire l'aiguillage avec les libellés **rendus exacts**
     (et alors le détecteur peut exiger l'égalité stricte, plus simple à raisonner) ou garder les
     abréviations de D-47 (et alors la contenance est nécessaire).
   - Recommandation : **citer les libellés rendus complets** dans l'aiguillage et exiger l'égalité
     stricte par numéro — c'est plus fort, plus simple, et satisfait D-47 sur le fond (les bons
     numéros), au prix d'une légère reformulation des libellés dans le fichier cible.
   - **Resolution (decidee par le jeu de plans) :** la **contenance par mot significatif** a ete
     retenue — la recommandation d'egalite stricte ci-dessus est **ecartee**, et le plan dit pourquoi.
     `04-04-PLAN.md` tache 1 (`_renvois_au_menu`) juge un jeton `N. LIBELLE` fautif si son numero
     n'existe pas parmi les libelles mesures au rendu de `GET /`, ou si le libelle lu ne partage
     **aucun** mot significatif (longueur >= 4, hors mots-outils `LISTE`, `DES`, `DE`, `LA`, `LE`,
     `LES`) avec le libelle reellement rendu de ce numero. La raison est consignee au plan et n'est pas
     contournable : D-47 **prescrit** les formes abrogees `4. OPTIMISATION` et `3. PANOPLIES` ; une
     egalite stricte declarerait fautif l'aiguillage corrige que la phase 3 exige et rendrait le
     **vert du critere 5 inatteignable**. La regle attrape malgre tout les trois inversions reelles du
     fichier (`3. OPTIMISATION DE STUFF`, `4. SYSTEME`, `4. GESTION DE LA BASE`). Limite de precision
     bornee et **ecrite** dans la docstring du detecteur : les jetons sont juges contre les libelles de
     **premier niveau** du rendu, si bien qu'un renvoi vers un sous-menu portant le meme numero serait
     rapporte forme (a) — dit plutot que passe sous silence (D-26).

2. **Quelle forme exacte pour la copie figée ?**
   - Ce qu'on sait : D-59 impose qu'elle soit un artefact de `tests/` et que le **même** détecteur la
     signale ; trois formes sont explicitement autorisées (chaîne, donnée structurée, fichier).
   - Ce qui n'est pas tranché : le fichier `tests/fixtures/guide-wizard-obsolete.md` (recommandé) vs
     une constante dans le module.
   - Recommandation : fichier de fixture, avec en en-tête un commentaire HTML rappelant qu'il s'agit
     d'un **copie figée d'un état obsolète** et non d'une page de documentation.
   - **Resolution (decidee par le jeu de plans) :** **fichier de fixture**, recommandation adoptee
     telle quelle. `04-04-PLAN.md` tache 1 cree `tests/fixtures/guide-wizard-obsolete.md` (UTF-8 sans
     BOM, fins de ligne CRLF comme les fichiers mesures du depot), ouvert par un commentaire HTML qui
     annonce qu'il s'agit d'un extrait fige pour test et **non** d'une page de documentation.
     `_lire_fixture()` le lit en UTF-8 explicite et leve une `AssertionError` localisante s'il manque —
     jamais un `skip` silencieux — et `test_copie_figee_signalee_par_le_detecteur` exige qu'il soit
     signale par le **meme** detecteur, avec au moins trois constats couvrant les trois formes
     nommees. La copie est **partielle et annoncee comme telle** : les extraits couverts par le wizard
     avance, pas les 330 lignes du guide.

3. **Comment convertir le renvoi de la ligne 256, qui couvre deux cibles ?**
   - Ce qu'on sait : la phrase nomme « les réglages avancés (les écrans du wizard) » **et** « la base
     locale » ; `base-locale.md` n'existe pas (phase 5) et un lien vers elle serait mort.
   - Ce qui n'est pas tranché : la tournure exacte qui lie le wizard sans lier la base locale.
   - Recommandation : lier la clause wizard (« les **réglages avancés** (les écrans du wizard) sont
     décrits dans [la page du wizard avancé](wizard-avance.md) »), conserver littéralement les mots
     `réglages avancés` et `base locale` (exigés par `RENVOIS_SANS_LIEN`) et n'introduire **aucun**
     nombre de trois chiffres dans la section des limites.
   - **Resolution (decidee par le jeu de plans) :** adoptee, et **elargie aux deux renvois**.
     `04-03-PLAN.md` tache 2 convertit les **deux** renvois en prose sans lien de
     `docs/parcours-simplifie.md` (~lignes 5 et 256) en **vrais liens markdown** vers
     `docs/wizard-avance.md`, dans le meme commit que la cible (D-63) : la question ne portait que sur
     la ligne 256, l'arbitrage porte sur les deux, parce que D-63 les nomme tous les deux. La clause
     « base locale » **n'est pas liee** — `base-locale.md` n'existe toujours pas et un lien vers elle
     serait mort. Les mots `reglages avances` et `base locale`, exiges par `RENVOIS_SANS_LIEN`,
     restent litteralement presents, aucun nombre de trois chiffres n'entre dans la section des
     limites, et l'affirmation de la ligne ~140 n'est pas touchee (D-64). L'hypothese **A4** est ainsi
     confirmee : le renvoi de la ligne 256 est attache a la seule clause « wizard ». Le controle vit
     dans `test_lien_wizard_avance_legitime` (constat `MOTIF_LIEN_D63`).

4. **Le contrôle de la ligne 140 doit-il exister, et à quel périmètre ?**
   - Ce qu'on sait : le rendu donne `Page prec`/`Suivant` à l'étape 1 et `Precedent`/`Page suiv` au
     récapitulatif ; `Precedent`/`Suivant` n'apparaissent qu'aux étapes 2 à 8 (mesuré).
   - Ce qui n'est pas tranché : la phase 4 ancre-t-elle l'affirmation de la page 3, ou se limite-t-elle
     à citer les libellés par étape dans `docs/wizard-avance.md` ?
   - Recommandation : ancrer **par étape** dans le test du wizard (source de vérité = rendu), et si un
     contrôle porte sur la ligne 140, le scoper explicitement aux étapes intermédiaires — jamais aux 9.
   - **Resolution (decidee par le jeu de plans) :** adoptee sur ses deux volets. `04-02-PLAN.md`
     tache 2 ecrit `test_touches_et_commandes_par_etape` : les couples touche/libelle sont ancres
     **par etape**, sur un client neuf, contre le rendu — l'etape 1 porte `Page prec`/`Suivant`, les
     etapes 2 a 8 `Precedent`/`Suivant`, l'etape 9 `Precedent`/`Page suiv`, et `ESC`/`Retour` sur les
     neuf. L'assertion `Precedent`/`Suivant` est **scope aux etapes 2 a 8** : un controle qui les
     exigerait sur les neuf contredirait le rendu des extremites. La ligne ~140 de
     `docs/parcours-simplifie.md` reste **inchangee**, donc vraie (D-64) — c'est `docs/wizard-avance.md`
     qui porte la precision par etape. L'hypothese **A3** est confirmee.

5. **`GUIDE_WIZARD.md` et `README.md` doivent-ils être couverts par des contrôles de liens ?**
   - Ce qu'on sait : aujourd'hui, aucun test ne lit `GUIDE_WIZARD.md` ; `test_docs_structure.py` ne
     parcourt que `docs/**`, et `test_readme_links_to_sommaire` ne vérifie que le lien du sommaire.
   - Recommandation : le nouveau module vérifie (a) les deux liens de l'aiguillage résolvent, (b)
     `README.md` ne contient plus `](GUIDE_WIZARD.md)`.
   - **Resolution (decidee par le jeu de plans) :** adoptee et **renforcee**. `04-03-PLAN.md` tache 1
     ecrit `test_aiguillage_et_readme` : sur `GUIDE_WIZARD.md`, un lien markdown dont la cible est
     `docs/wizard-avance.md` **et** un lien dont la cible est `docs/sommaire.md` sont exiges, et chaque
     cible doit exister depuis la racine du depot (constat `MOTIF_LIEN_AIGUILLAGE`) ; sur `README.md`,
     aucune occurrence de `GUIDE_WIZARD` ni de `wizard-avance`, et exactement **un** lien markdown vers
     `docs/sommaire.md` (constat `MOTIF_LIEN_PRODUIT`) — la recommandation (b) est donc satisfaite au
     sens large, la ligne « Guide detaille » etant supprimee sans texte de remplacement (D-62).
     `04-03-PLAN.md` tache 2 ajoute a cote `test_lien_wizard_avance_legitime` : toute cible de lien de
     l'aiguillage vers `docs/` doit etre **declaree** dans `LIENS_LEGITIMES_VERS_L_AIGUILLAGE` (constat
     `MOTIF_LIEN_NON_DECLARE`) **et** exister sur disque (constat `MOTIF_LIEN_MORT`).

6. **Le lancement `GO` doit-il être prouvé ?**
   - Ce qu'on sait : `GO` exécute réellement le solveur ; la phase 3 a patché l'étape de calcul pour
     ne pas le lancer.
   - Recommandation : ne prouver `GO` **que** par l'action et la redirection mesurées (POST → 302
     `/optimize/result`) avec le solveur patché, ou ne pas le prouver du tout et se contenter de citer
     le libellé rendu (`GO = LANCER`), qui vient du corps du récapitulatif. Ne jamais poster `GO` pour
     observer autre chose.
   - **Resolution (decidee par le jeu de plans) :** la **seconde branche** de la recommandation est
     retenue — `GO` **n'est jamais poste**. `04-02-PLAN.md` tache 2 l'ecrit comme une exigence : seule
     la citation des libelles du corps du recapitulatif est controlee (`GO = LANCER`,
     `RESET = REINITIALISER`, `1-8 = RETOUR ECRAN`, `SAVES = STUFFS SAUVEGARDES`, tous lus au rendu),
     et les commandes prouvees par l'action sont `RESET`, `SAVES` et les chiffres, jamais `GO`. La
     branche « POST puis redirection vers le resultat » n'est pas retenue : la garde `ast` de
     `04-01-PLAN.md` tache 1 (`test_garde_de_cloture_du_harnais`) refuse tout appel dont l'argument
     nomme `data` porte la paire `"cmd": "GO"`, et l'execution reelle du solveur reste couverte,
     patchee, par `tests/test_web.py`.

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|------------|-----------|---------|----------|
| `.venv/Scripts/python.exe` | Exécution de référence (D-15) | ✓ | Python **3.14.7** (mesuré) | — |
| `pytest` dans `.venv` | Tout le harnais | ✓ | **9.1.1** (mesuré ; `>=8.0` déclaré) | — |
| `flask` (+ `test_client`) | Rendu des 9 écrans | ✓ | `>=3.0` déclaré, importé avec succès cette session | — |
| `git` | Commits locaux | ✓ | 2.55.0.windows.4 (mesuré) | — |
| Base locale `.data/dofus.sqlite3` | **Aucun besoin** : la fixture `app` construit sa propre base sous `tmp_path` | ✓ (présente, non utilisée) | empreinte consignée | — |
| Réseau / navigateur / serveur web | — | ✗ (et interdit) | — | Aucun : le rendu passe par le client de test en processus |
| Compte externe, secret, service distant | — | ✗ (et hors périmètre) | — | Aucun |

**Missing dependencies with no fallback:** none — tout ce dont la phase a besoin est installé.
**Missing dependencies with fallback:** none.

*Écart à signaler au plan (pas un blocage) :* le dépôt déclare `requires-python = ">=3.11"` mais
l'interpréteur du `.venv` est **3.14.7**. La phase n'utilise aucune construction dépendante de la
version au-delà de ce que les phases 1 à 3 emploient déjà (typage `X | None`, `pathlib`,
`unicodedata`), donc aucun impact — mais un test qui s'appuierait sur une nouveauté 3.13+/3.14
sortirait du contrat « 3.11+ ».

## Validation Architecture

`workflow.nyquist_validation` vaut `true` dans `.planning/config.json` : cette section est requise.

### Test Framework

| Property | Value |
|----------|-------|
| Framework | pytest **9.1.1** (déclaré `>=8.0`), Python 3.14.7 (`.venv`) |
| Config file | `pyproject.toml` → `[tool.pytest.ini_options]` (`testpaths = ["tests"]`, `pythonpath = ["."]`, `filterwarnings`) — **aucune configuration à ajouter** |
| Quick run command | `./.venv/Scripts/python.exe -m pytest -q tests/test_docs_wizard.py` |
| Full suite command | `./.venv/Scripts/python.exe -m pytest -q` (baseline mesurée : **186 passed in 3.65s**) |
| Fixtures partagées | `tests/conftest.py` : `app`, `client`, `docs_dir`, `normalize`, `section`, `sections`, `lignes_de_code`, `lignes_exemple` (D-12 : **à réutiliser, jamais recopier**) |

### Phase Requirements → Test Map

| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|--------------|
| WIZ-01 | Les 9 titres/étapes de `STEP_TITLES` apparaissent dans la page, dans l'ordre de `WIZARD_STEPS`, et le nombre d'étapes est relu au code | unit (rendu + constantes) | `./.venv/Scripts/python.exe -m pytest -q tests/test_docs_wizard.py -k etapes` | ❌ Wave 0 |
| WIZ-01 | Les 11 slots et les 10 filtres `F1`…`F10` cités par la page existent au rendu ; `F6` = `ARMES DISTANCE`, `F7` = `ARMES MELEE` | unit (rendu page 1 + page 2) | `… -k filtres` | ❌ Wave 0 |
| WIZ-01 | Les 11 options du récapitulatif de l'écran `OPTIONS SOLVEUR` sont citées (numéro + libellé lus au rendu) | unit | `… -k options` | ❌ Wave 0 |
| WIZ-01 | Les formats `BASE POINTS CIBLE POIDS` / `BASE EXO CIBLE POIDS` sont décrits tels que le code les applique, avec les messages de refus réels | unit (rendu du sous-écran `OPT-WED` + POST de valeurs invalides) | `… -k formats` | ❌ Wave 0 |
| WIZ-01 | La syntaxe d'items (`+ID` → INTERDITS, `-ID` → FORCES, `!ID`, `CLEAR`) et l'unique message de refus sont cités | unit (POST par cas + rendu) | `… -k items` | ❌ Wave 0 |
| WIZ-02 | Les couples `F7`/`F8`/`ESC` **par étape** (extrémités incluses) et les commandes `GO`, `RESET`, `SAVES`, `1`–`8` sont cités | unit (rendu + POST `RESET`/`SAVES`/`1`/`8`, solveur jamais lancé) | `… -k touches` | ❌ Wave 0 |
| WIZ-02 | Le chemin d'arrivée réel (menu `4` → `/optimize` → `/optimize/quick/classe` → `AVANCE` → `/optimize/wizard/recap`) est décrit et mesuré | unit (chaîne de redirections) | `… -k arrivee` | ❌ Wave 0 |
| WIZ-03 | `GUIDE_WIZARD.md` livré ne contient aucun des trois renvois obsolètes (fonction pure, attentes lues au rendu) | unit (détecteur) | `… -k renvoi_obsolete` | ❌ Wave 0 |
| WIZ-03 | La **copie figée** sous `tests/` est signalée par le **même** détecteur (au moins trois constats nommés) | unit (détecteur) | `… -k copie_figee` | ❌ Wave 0 |
| WIZ-03 | Les deux liens de l'aiguillage résolvent et `README.md` ne contient plus `](GUIDE_WIZARD.md)` | unit (disque) | `… -k aiguillage` | ❌ Wave 0 |
| WIZ-03 | Le nouvel index du sommaire reste cohérent : `problemes_index`/`problemes_h1`/`problemes_retour_sommaire` verts | unit (garde existante) | `… -m docs_structure` / suite entière | ✅ `tests/test_docs_structure.py` |
| WIZ-03 | La dette D-44 est levée : `docs/parcours-simplifie.md` **lie** `wizard-avance.md`, ce que la phase 3 interdisait | unit (page + garde de structure) | `… tests/test_docs_parcours.py` | ✅ à **modifier** (voir Pitfall 1) |
| Critère 5 | Le détecteur est observé **rouge** sur l'état antérieur puis **vert** après correction, dans la même phase | preuve d'exécution (sortie collée) | `./.venv/Scripts/python.exe -m pytest -q tests/test_docs_wizard.py -k renvoi_obsolete` **avant** puis **après** la réécriture de `GUIDE_WIZARD.md` | ❌ Wave 0 |
| T-04-x | Aucune écriture sous `.data/` autour de la suite (empreinte taille/mtime_ns/sha256 inchangée) | mesure | commande d'empreinte de la phase 3, conservée | ✅ patron existant |
| T-04-x | Aucun `db clear` présenté comme étape normale, et aucune exécution | unit (absence de jeton dans les fichiers touchés) | `… -k destruct` | ❌ Wave 0 |

*Ouverture de périmètre (à signaler au plan) :* le ROADMAP annonce **4 plans** (04-01 à 04-04). Les
tests listés ci-dessus se répartissent naturellement sur les plans 04-02 (ancrage des écrans),
04-03 (aiguillage + `README`) et 04-04 (détecteur). Les plans doivent **nommer explicitement** la
modification de `tests/test_docs_parcours.py` (`PAGES_INEXISTANTES`) : sans elle, la suite est rouge
dès l'ajout du lien D-63.

### Sampling Rate

- **Per task commit :** `./.venv/Scripts/python.exe -m pytest -q tests/test_docs_wizard.py` (rapide)
  puis, dès qu'une page `docs/` bouge, `… tests/test_docs_structure.py tests/test_docs_parcours.py`.
- **Per wave merge :** `./.venv/Scripts/python.exe -m pytest -q` (suite entière, ~4 s mesurée).
- **Phase gate :** suite entière verte **et** la sortie rouge/verte du détecteur collée dans
  `04-VERIFICATION` (critère 5) ; l'empreinte de `.data/dofus.sqlite3` inchangée.

*Aucune validation manuelle :* l'interprète des critères est pytest. Le « rouge puis vert » n'est pas
une observation humaine — c'est **la sortie de la même commande, exécutée deux fois**, ce qui est la
manière automatisable de prouver les deux états.

### Wave 0 Gaps

- [ ] `tests/test_docs_wizard.py` — nouveau module : rendu des 9 étapes, libellés, touches, formats,
      items, chemin d'arrivée, détecteur (WIZ-01, WIZ-02, WIZ-03)
- [ ] `tests/fixtures/guide-wizard-obsolete.md` — copie figée des trois formes obsolètes (D-59b)
- [ ] `tests/test_docs_parcours.py` — **modification** : `PAGES_INEXISTANTES = ("base-locale.md",)`
      et commentaire mis à jour ; ajout du contrôle symétrique du lien `wizard-avance.md`
- [ ] `docs/wizard-avance.md` — la page cible doit exister **avant** que les contrôles de structure
      du sommaire et le test d'ancrage ne passent
- [ ] Framework install : **aucun** — pytest 9.1.1 déjà présent dans `.venv`

## Security Domain

`workflow.security_enforcement` vaut `true` (ASVS niveau 1 déclaré). La phase ne livre ni endpoint,
ni authentification, ni donnée : l'analyse porte donc sur **ce que la phase peut casser** dans le
harnais et dans la documentation.

### Applicable ASVS Categories

| ASVS Category | Applies | Standard Control |
|---------------|---------|-----------------|
| V2 Authentication | no | Aucune authentification livrée ; l'application de test est instanciée en processus |
| V3 Session Management | no | Les tests lisent `session_transaction()` de Flask (API de test), ils ne gèrent pas de session produit |
| V4 Access Control | no | Aucun contrôle d'accès dans la phase |
| V5 Input Validation | **yes** | Deux contrôles : (1) les liens de la documentation sont résolus en **rejetant** `#`, les chemins absolus, les antislashs, `file://` et toute cible hors de la racine du dépôt (`problemes_liens`) ; (2) le harnais n'exécute **jamais** de saisie produit : il la poste au client de test et lit la réponse |
| V6 Cryptography | no | Aucune cryptographie nouvelle ; le seul usage est `hashlib.sha256` pour l'empreinte d'un fichier local |
| V8 Data Protection (protection des données) | **yes**, en creux | Interdiction de citer des valeurs volatiles de la base locale (nombre d'objets, version de jeu, horodatage) : la doc ne fige ni n'expose l'état d'un fichier local |

### Known Threat Patterns for {docs + pytest harness}

| Pattern | STRIDE | Standard Mitigation |
|---------|--------|---------------------|
| Commande destructrice présentée comme une étape normale (`db clear`, `PURGE`, suppression sous `.data/`) | Tampering / DoS | Le détecteur et la page ne classent **jamais** `db clear` dans un parcours recommandé (D-61) ; aucun `db clear` n'est exécuté ; le patron existe déjà (`COMMANDE_DESTRUCTRICE`, `tests/test_docs_structure.py:20`) |
| Écriture involontaire sous `.data/` par un test | Tampering | La fixture `app` construit sa base sous `tmp_path` ; mesure d'empreinte avant/après la suite (taille, `mtime_ns`, `sha256`) |
| Évasion de la racine du dépôt par un lien relatif (`../../…`, chemin absolu, `file://`) | Information disclosure / Tampering | `problemes_liens` rejette ces formes (contrôle existant, à ne pas contourner) |
| Exécution de code ou de processus par le harnais (`subprocess`, `eval`, `import` du produit exécutable) | Elevation of privilege | Patron de la garde `ast` posée en 03-01 (`RACINES_INTERDITES`, `APPEL_PRODUIT = "main"`), à reprendre : le nouveau module ne doit appeler ni `main()`, ni `subprocess`, ni `sqlite3`, ni `socket` |
| Fuite de secret dans la documentation | Information disclosure | Aucun secret n'est écrit : la phase documente des libellés et des formats, jamais une clé (`DOFUS_SECRET_KEY` n'apparaît dans aucune page) |
| Défaut d'ancrage : une page qui affirme un libellé que le code ne rend plus | Spoofing (documentation qui ment) | Tout libellé affirmé est relu au rendu par un test (D-36/D-42) — c'est la sécurité de la phase, au sens de sa valeur centrale |

*Aucune menace résiduelle élevée :* la phase ne modifie pas `dofus_stuff/**`, n'ouvre aucun port,
n'ajoute aucune dépendance et n'exécute rien du produit.

## Sources

### Primary (HIGH confidence)

Tous les fichiers suivants ont été **lus cette session** (les plages de lignes sont citées dans le
corps du document là où la valeur est reprise) :

- `dofus_stuff/web/optimize_wizard.py` (450 lignes, lu en entier) — `WIZARD_STEPS:23`, `STEP_TITLES:35`,
  `RESISTANCE_STATS:47`, `DAMAGE_STATS:64`, `MISC_STATS:82`, `SLOT_GROUP_LABELS:97`,
  `TYPE_FILTER_LABELS:111`, `load_wizard_spec:125`, `body_slots:179`, `body_options:198`,
  `body_stat_list:218`, `body_items:240`, `body_recap:262`, `apply_slots_input:281`,
  `apply_options_input:311`, `apply_option_value:348`, `apply_stat_edit:368`, `apply_items_input:399`,
  `stat_names_for_step:439`
- `dofus_stuff/web/routes.py` (1384 lignes, régions lues : 60-260, 890-1300) — `_screen:89`
  (libellés F7/F8 : 137-141), `menu:189`, `menu_post:214`, `optimize_entry:930`, `optimize_quick:936`,
  `_wizard_fkeys:1014`, `_wizard_step_urls:1018`, `optimize_wizard:1029`, `_wizard_edit_screen:1192`,
  `saves:1282`, `_run_optimize_and_redirect:911`
- `dofus_stuff/model/solver_spec.py` — `SLOT_GROUPS:15`, `DEFAULT_SLOT_GROUPS:29`,
  `TYPE_FILTER_KEYS:43`, `MAIN_CARACS:71`, `EXO_STATS:80`, `default_player_spec:534`
- `dofus_stuff/web/screens.py` — `COLS:5`, `ROWS:6`, `BODY_LINES:10`, `clip:12`, `header_line:77`
- `dofus_stuff/web/templates/screen.html` (79 lignes, lu en entier) — marqueurs `id="body"`,
  `<div class="row status`, `fkey-key`/`fkey-label`, attributs `data-body-page`, `data-body-total`,
  `data-f7-url`, `data-f8-url`, `data-esc-url`
- `dofus_stuff/web/static/js/terminal.js` — `navigateF7:526`, `navigateF8:537`, gestion `F3`/`Escape`/
  `F7`/`F8`/`PageUp`/`PageDown` (563-595)
- `tests/conftest.py` (262 lignes, lu en entier) — `_normalize`, `docs_dir`, `normalize`, `section`,
  `sections`, `lignes_de_code`, `lignes_exemple`, fixtures `catalog`/`app`/`client`
- `tests/test_docs_structure.py` — `LINK:7`, `problemes_liens:39`, `problemes_index:92`,
  `pages_listees:326`, `problemes_h1:337`, `problemes_retour_sommaire:383`, `problemes_encodage:418`,
  `LONGUEUR_MINIMALE:315`, `test_readme_links_to_sommaire:190`,
  `test_mutation_detecte_les_trois_derives:533`
- `tests/test_docs_parcours.py` (2734 lignes, régions lues) — `SOMMAIRE`/`SOURCE_*`, `TITRE_*`,
  `ETATS_ETAPE:232`, `TOUCHES_WIZARD:212`, `PAGES_INEXISTANTES:2231`,
  `_client_etape`, `_lignes_du_corps`, `_statut`, `_touches`, `_couples_du_rendu`,
  `test_page_complete_et_sans_derive:2467`, `test_data_locale_non_modifiee_autour_des_rendus:2557`
- `tests/test_docs_code_anchor.py` — patron `LIBELLES_SOURCE:61` (libellé → fichier source → aiguilles)
- `docs/sommaire.md`, `docs/parcours-simplifie.md` (lignes 1-20, 125-160, 245-269 lues), `docs/installation.md`,
  `docs/cli.md`, `README.md`, `GUIDE_WIZARD.md` (330 lignes, lu en entier)
- `.planning/config.json` (`nyquist_validation: true`, `security_enforcement: true`,
  `git.allow_default_branch_commits: true`), `.planning/ROADMAP.md` § Phase 4, `.planning/REQUIREMENTS.md`,
  `.planning/STATE.md`, `.claude/CLAUDE.md`

### Secondary (MEDIUM confidence)

- Mesures d'exécution de cette session (rendu des écrans, redirections, messages de refus, comptages,
  suite complète) — reproductibles par les commandes citées, mais **non** des documents sources.

### Tertiary (LOW confidence)

- Aucune. Aucune recherche Web n'a été effectuée : la phase est intégralement interne au dépôt, et
  la seule documentation technique nécessaire (`pytest`, `flask.test_client`, stdlib) est déjà
  couverte par les phases 1 à 3.

## Metadata

**Confidence breakdown:**

- Standard Stack : **HIGH** — aucun paquet nouveau ; versions réellement mesurées dans `.venv`.
- Architecture : **HIGH** — le chemin d'arrivée, les 9 écrans, les libellés et les touches sont
  **mesurés au rendu** cette session, pas déduits.
- Pitfalls : **HIGH** pour les pitfalls 1, 2, 5, 6, 8 (mesurés ou vérifiés au fichier) ; **MEDIUM**
  pour les pitfalls 3, 4, 7 (ils dépendent de choix de conception du détecteur, pas d'une mesure).
- Validation Architecture : **HIGH** — framework, fixtures et commandes existants, baseline 186 tests
  verts mesurée.

**Research date:** 2026-09-11
**Valid until:** 2026-10-11 (30 jours). La matière est dans le dépôt et ne dépend d'aucune source
externe ; seule une modification de `dofus_stuff/**` (interdite par D-66) ou de `tests/` invaliderait
les mesures.
