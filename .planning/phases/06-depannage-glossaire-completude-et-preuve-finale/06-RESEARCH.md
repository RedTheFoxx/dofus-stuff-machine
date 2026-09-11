# Phase 6: Dépannage, glossaire, complétude et preuve finale - Research

**Researched:** 2026-09-12
**Domain:** Documentation utilisateur ancrée sur le code d'un produit Python local (deux surfaces CLI/web, harnais pytest d'ancrage documentaire), phase de clôture de jalon
**Confidence:** HIGH (toute la matière est interne au dépôt et a été mesurée cette session ; les rares points non mesurés sont listés en § *Claims non vérifiées*)

---

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions
[Copy verbatim from CONTEXT.md ## Decisions]

### Découpage et vagues
- **D-92:** Les 4 plans du ROADMAP sont conservés (06-01…06-04). **Les vagues sont séquentielles** : les
  quatre plans touchent `docs/` et/ou `tests/`, et 06-03/06-04 dépendent des pages livrées par 06-01 et
  06-02 (la complétude ne peut être prouvée qu'une fois les pages existantes). Aucun parallélisme n'est
  revendiqué.

### Dépannage indexé par le message réel
- **D-93:** `docs/depannage.md` est organisé **par message réellement produit**, pas par symptôme
  imaginé : chaque rubrique s'adosse à une chaîne **lue dans le code** au moment de la rédaction (D-19),
  et les cinq familles du critère 1 sont couvertes : base absente ou vide, saisie invalide, calcul long,
  clavier inactif, résultat paginé. Un message non produit par le code ne crée pas de rubrique (D-76).

### Glossaire
- **D-94:** `docs/glossaire.md` définit le vocabulaire du produit et de la documentation ; **chaque entrée
  citée est réellement présente** dans la page et **les entrées sont triées**. Le contrôle porte sur
  l'existence et l'ordre, pas sur la prose des définitions (limite déclarée, D-85).

### Complétude et ensemble exact des fichiers
- **D-95:** La **liste épinglée des 8 pages** devient une constante de test, et l'**ensemble exact des
  fichiers de `docs/`** est vérifié : **toute page en trop fait échouer la suite** (critère 3). Le
  `docs/sommaire.md` reçoit son **parcours conseillé final**, cohérent avec les pages livrées.
- **D-96:** Le contrôle de complétude vit dans `tests/`, **réutilise les fixtures partagées** (D-12) et
  suit le patron d'ancrage des phases 3 à 5 (constats citant page, valeur attendue, fichier producteur).

### Preuve du harnais
- **D-97:** Le critère 4 est prouvé par un **test de mutation** : une **copie de `docs/` sous `tmp_path`**
  reçoit une **dérive injectée**, et le harnais doit **échouer réellement** — complétude, ancrage de
  libellé et renvois obsolètes détectés. La copie doit être **verte avant mutation**, sinon la morsure ne
  prouve rien (leçon des phases 3 à 5). Chaque morsure exige un **motif nommé** dans la sortie d'échec.

### Vérification finale
- **D-98:** Le critère 5 est exécuté et **rapporté avec le compteur et la durée réellement obtenus** par
  `.venv/Scripts/python.exe -m pytest -q` — jamais une valeur attendue ou reconstituée. `.data/` est
  mesurée (empreinte) avant et après, **identique** ; aucune connexion réseau ; `main()` jamais exécuté.
  L'audit de périmètre `git status` est consigné : seuls `docs/`, `README.md`, `GUIDE_WIZARD.md` et
  `tests/` peuvent apparaître comme modifiés.
- **D-99:** Les fichiers de planification (`GUIDE_WIZARD.md`, `README.md`) ne sont touchés **que** si un
  contrôle prouve une incohérence ; sinon ils restent tels quels.

### Points hérités de la phase 5, à trancher ici
- **D-100:** L'occurrence de `db clear` dans `README.md:80` (bloc `bash`) est **explicitement transmise à
  cette phase** : elle doit être **tranchée** — soit couverte par un contrôle (le README ne présente
  alors plus une commande destructrice comme une étape), soit **conservée et déclarée** comme limite du
  périmètre, avec sa raison. Elle ne peut pas rester dans un entre-deux non écrit.
- **D-101:** La dérive préexistante de `.planning/WINDOWS.md` (`windows_ledger_table_drift`, ligne `id=5`,
  héritée de la phase 3) est **un défaut de registre connu, hors périmètre** : elle n'est **pas corrigée à
  la main** et reste déclarée. Elle n'a jamais été causée par une phase de ce run.

### Conventions et frontières
- **D-102:** Conventions des phases 1 à 5 applicables **telles quelles** : gabarit de page D-01/D-69
  (H1 = libellé d'index, `## Source de vérité`, ligne de retour en dernière ligne non vide, CRLF, UTF-8
  sans BOM), normalisation D-11, helpers partagés D-12, constats D-13, constantes publiques D-14,
  interpréteur épinglé D-15, une seule source par énoncé D-17, aucune sémantique inventée D-19, limites
  honnêtes D-85, français D-67.
- **D-103:** `dofus_stuff/**` est **lecture seule** (D-88) : la documentation se conforme au code.
- **D-104:** **Aucune action destructive sur les données** : pas de `db clear`, pas de `drop`, aucune
  suppression sous `.data/` ni sous `.doc-agent/` ; `.data/dofus.sqlite3` peut être **lue en octets**
  pour une empreinte, jamais ouverte par SQLite dans un contrôle d'intégrité. Aucune resynchronisation.
- **D-105:** Commits **locaux** uniquement, indexation **par chemin explicite** (jamais `git add .`, ni
  `doc-agent.toml`, ni `.doc-agent/`, ni `gsd-auto*.toml`, ni `.planning/state.json`) ; **aucune
  publication, aucun déploiement distant** ; **aucune dépendance ajoutée**.

### Claude's Discretion
- L'ordre des rubriques de dépannage, la formulation des entrées de glossaire, le nombre et la forme des
  morsures du critère 4, le découpage exact des contrôleurs entre 06-03 et 06-04, et le libellé du
  parcours conseillé final.

### Deferred Ideas (OUT OF SCOPE)
- Aucune : cette phase clôt le jalon. Les deux points transmis par la phase 5 (occurrence `db clear` du
  README, registre `.planning/WINDOWS.md`) sont traités ici ou déclarés (D-100, D-101).
</user_constraints>

---

## Summary

Cette phase est **entièrement interne au dépôt** : aucun paquet, aucune API, aucune documentation tierce.
La « recherche » consiste donc à **mesurer** deux choses que les plans ne peuvent pas deviner — les
**messages que le produit imprime réellement** (le critère 1 dit « le message réellement produit », et un
message plausible mais faux est le défaut que ce jalon a déjà payé deux fois) et **ce que le harnais
sait déjà détecter** (le critère 4 demande de prouver que les gardes mordent, or cinq gardes existent
déjà et trois familles de dérive sont déjà prouvées par un test de mutation de la phase 1).

Six résultats de mesure structurent la planification :

1. **Les cinq familles du critère 1 ne se ressemblent pas.** *Base absente ou vide* et *saisie invalide*
   portent des messages **littéraux**, mesurés sur les deux surfaces (ex. `Version jeu : (aucune)` /
   `VERSION JEU : (aucune)`, `SAISIE REQUISE`, `LIMITE INVALIDE`, `ID INVALIDE — ENTIER ATTENDU`).
   *Résultat paginé* porte un **motif de gabarit**, pas une chaîne : `PAGE {page}/{total}` composé dans
   `_screen` (`dofus_stuff/web/routes.py:145`), et la forme CLI `Page suivante disponible : ` (`cli.py:407`).
   *Calcul long* porte **un seul** message d'attente — `Calcul en cours (CP-SAT)…` (`cli.py:416`) — côté
   CLI, et rien côté web où l'attente est signifiée par la ligne de statut `ENTREE=CALCULER`
   (`routes.py:1008`, mesuré). **Aucun message ne dit qu'un calcul est long, ni ne donne de durée
   d'attente** : ce que le produit expose, c'est un **budget** (`--time-limit`, défaut `5.0`, `cli.py:106-110` ;
   rendu `DUREE=5s` dans le récapitulatif, `web/optimize_wizard.py:266`, mesuré).
   *Clavier inactif* — et c'est le résultat le plus important de cette recherche — **ne porte aucun
   message** : je n'ai trouvé aucune chaîne produite par le code pour cette famille (recherche
   `inactif|gelé|figé|bloqué|clavier` sur tout le dépôt : **0 occurrence hors `.claude/CLAUDE.md`**). Ce que
   le code porte, c'est un **mécanisme observable** : le champ est `autofocus` (`templates/screen.html:61`),
   `terminal.js:80-88` le refocalise au chargement et à chaque clic ailleurs, et `terminal.js:595` fait
   dépendre la soumission de `Entrée` de `document.activeElement === input` ; sur les écrans **sans champ**
   (`input_label=None`, ex. `VER-01`, `TST-01`, `DB-02`, `END-01`), **mesuré** : aucune saisie n'est
   possible. La rubrique « clavier inactif » devra donc s'adosser à `terminal.js` et au **symptôme rendu**
   (absence de champ, `F3`/`ESC` seuls actifs), jamais à un message — et le § *Feasibility* dit ce qu'un
   contrôle peut et ne peut pas en prouver.
2. **Le parcours conseillé du sommaire annonce déjà deux pages qui n'existent pas.** `docs/sommaire.md:12-13`
   liste `6. Dépannage` et `7. Glossaire` alors qu'aucun fichier ne les porte, et **aucune garde ne voit
   cette section** : elle est en texte simple, pas en liens (`grep "Parcours" tests/*.py` → **0
   occurrence**). Le parcours diverge aussi de l'index sur l'ordre (`wizard-avancé` est 3ᵉ au parcours et
   4ᵉ à l'index). Le « parcours conseillé final » de D-95 n'est donc pas une remise en forme : c'est la
   **première fois** que cette section devient vérifiable.
3. **L'ensemble exact des fichiers de `docs/` est déjà tenu, mais relativement à l'index.** Mesuré :
   supprimer `docs/cli.md` d'une copie fait **14 failed** (motifs `docs/sommaire.md : cible listee absente
   sur disque : cli.md` et `lien mort vers cli.md`) ; ajouter `docs/page-en-trop.md` fait échouer
   `test_sommaire_lists_every_document` **et** `test_h1_matches_sommaire_entry` en nommant la page. Les
   deux sens de la dérive sont donc déjà couverts **par rapport à l'index**, jamais par rapport à une
   **liste épinglée** : une 9ᵉ page listée à l'index **et** présente passerait. C'est précisément ce que
   la constante de D-95 ajoute, et il n'y a rien à dupliquer des gardes existantes
   (`tests/test_docs_structure.py:92-119` pour l'index, `:337-380` pour le H1).
4. **Le critère 4 est déjà prouvé pour trois familles de dérive, par un test de mutation de la phase 1.**
   `tests/test_docs_structure.py:533` (`test_mutation_detecte_les_trois_derives`) copie `docs/` sous
   `tmp_path`, exige la copie **verte avant mutation**, puis injecte (a) un lien mort, (b) une page non
   indexée, (c) un H1 divergent, et vérifie que le constat nomme la dérive. J'ai **rejoué** deux dérives
   supplémentaires cette session sur des copies réelles : la **page manquante** (rouge, motifs mesurés) et
   l'**ancrage de libellé** (H1 divergent → rouge ; libellé remplacé par un nom non produit par le code →
   rouge **si** le nom ne contient pas le libellé réel : `Fermer` mord, `Quitter tout` **passe**).
   Le delta honnête de la phase 6 est donc : (i) la **page manquante** (nouveau), (ii) un **oracle plus
   large** que trois fonctions (la phase 1 appelle les trois fonctions de garde ; les phases 3 à 5 ont
   rejoué la **suite entière** dans une copie, par script), (iii) la **limite mesurée** de l'ancrage de
   libellé, écrite plutôt que revendiquée.
5. **Le `db clear` du `README.md` n'est couvert par aucune garde, et deux gardes existantes sont proches
   sans l'atteindre.** `README.md:77-81` est un bloc ` ```bash ` contenant `db status`, `db sync` **et**
   `db clear` sans avertissement. Les gardes de commande destructrice portent toutes sur une page précise :
   `tests/test_docs_structure.py:275` (installation.md), `tests/test_docs_cli.py:928` (cli.md),
   `tests/test_docs_base_locale.py:1721` (base-locale.md). Le seul contrôle qui lit le `README.md` est
   `tests/test_docs_base_locale.py:1964`, et sa docstring déclare explicitement que **le bloc de commandes
   du README est hors de son mandat**. Trois faits mesurés à verser au tranchage de D-100 : le bloc est
   tagué `bash` et non `console` (or `lignes_exemple` ne lit que les blocs `console`, D-24) ; le README ne
   porte qu'**un** lien interne (`docs/sommaire.md`) ; et `db sync`, classée destructrice pour la règle des
   exemples (D-23), est dans le **même** bloc.
6. **La vérification finale est mesurable telle quelle, mais le périmètre `git status` du critère 5 est
   faux à la lettre.** Mesuré cette session : `219 passed in 4.31s` (et `219 passed in 4.13s` avec un
   greffon qui refuse `socket`, `create_connection`, `socketpair`, `urlopen` **et** `main()` des deux
   points d'entrée) ; empreinte `.data/dofus.sqlite3` **identique** avant et après tout le travail :
   `24989696:1788730056843137500:e3793d64cb7939ad1a51837b075b6b95e03d64c878fcb9cc07f86c00bb8fef7b`.
   Mais `git status --porcelain` porte **déjà**, avant toute action de cette phase, ` M .gitignore` et
   ` M .planning/config.json`, et la phase fera bouger `.planning/ROADMAP.md`, `.planning/STATE.md`,
   `.planning/REQUIREMENTS.md` (fichiers **suivis**) plus ses propres plans/résumés sous
   `.planning/phases/06-…/`. L'audit de périmètre doit donc être écrit sur le périmètre **livrable**
   (`docs/`, `README.md`, `GUIDE_WIZARD.md`, `tests/`) avec ces deux écarts nommés, sans quoi il serait
   écrit faux dès sa première exécution.

**Primary recommendation:** rédiger les deux pages **exclusivement** à partir de l'inventaire mesuré de ce
document (chaque message y est cité verbatim avec sa provenance `fichier:ligne`), traiter la rubrique
« clavier inactif » comme un **mécanisme** et non comme un message, faire de la liste épinglée une
constante de test **ajoutée** (jamais une réécriture des gardes d'index, qui tiennent déjà l'égalité
d'ensembles), et écrire la preuve du harnais en **deux temps** : un test pytest en processus (patron de
`test_mutation_detecte_les_trois_derives`, sans `subprocess` — la garde de clôture des quatre modules
d'ancrage l'interdit) **plus** une batterie rejouable qui exécute la **suite entière** dans la copie et
colle la sortie réelle, comme les plans 05-02/05-04 l'ont fait.

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| AIDE-01 | Un lecteur trouve une rubrique de dépannage en cherchant par message d'erreur réel | § *Mesured inventory* A : les cinq familles avec leurs **messages verbatim** et leur provenance `fichier:ligne`, sur les deux surfaces ; le § A.6 donne, pour chaque famille, comment un contrôle observe le message **sans `.data/`** et **sans `main()`** (capture de `_print_db_status` sur base `tmp_path`, `ast` sur `cli.py::main`, client de test Flask en processus). |
| AIDE-02 | Un lecteur trouve un glossaire du vocabulaire employé par l'outil et par la documentation | § *Mesured inventory* B : la table des termes candidats, chacun adossé à la ligne qui l'emploie (aide de parseur, constante publique, rendu d'écran, page livrée) ; la colonne « déjà défini où » distingue les termes **à définir** des termes **à renvoyer** (D-17). |
| GARD-03 | La complétude est un critère de sortie vérifié après livraison, et un test de mutation prouve que le harnais détecte réellement une dérive | § *Mesured inventory* C (inventaire réel de `docs/`, liste épinglée des 8, gardes d'index/H1 existantes) et D (les trois dérives **mesurées** : page manquante, libellé dérivé, renvoi obsolète) ; § *Feasibility verdict* : mécanisme recommandé par dérive et limites honnêtes. |
| GARD-04 | La vérification s'exécute avec `.venv/Scripts/python.exe -m pytest -q`, sans écrire sous `.data/`, sans exécuter `main()` et sans ouvrir de connexion réseau | § *Mesured inventory* E : compteur et durée **mesurés cette session** (`219 passed in 4.31s`), empreinte `.data/` avant/après, greffon de preuve « ni réseau ni `main()` » mesuré vert (`219 passed in 4.13s`), et périmètre `git status` réel (trois écarts nommés). |
</phase_requirements>

## Project Constraints (from CLAUDE.md)

Le fichier de projet est `.claude/CLAUDE.md` (`claude_md_path` de `.planning/config.json`) ; il contient
le bloc projet, la recherche de stack et les conventions. Directives actionnables, telles quelles :

- **Périmètre** : strictement documentaire, limité au besoin initial ; « pas de nouveau milestone après
  livraison » ; pas de modification de `dofus_stuff/**` pour « aligner » la doc (`.claude/CLAUDE.md:39-49`
  et table `What NOT to Use`).
- **Technique** : Python 3.11+, `pytest` comme **seul** outillage de vérification, **aucune nouvelle
  dépendance** (`.claude/CLAUDE.md:36`, et `.planning/config.json` → `workflow.nyquist_validation: true`,
  `security_enforcement: true`, `security_asvs_level: 1`).
- **Langue** : documentation intégralement en français (D-67).
- **Données** : lecture seule sur `.data/` ; jamais de `db clear`, de drop SQLite ni de suppression.
- **Réseau** : hors-ligne par défaut, aucune resynchronisation, aucune publication, aucun déploiement.
- **Vérification** : les critères de « fait » sont prouvés par des tests pytest **réellement exécutés** ;
  aucune validation manuelle, aucun résultat inventé.
- **Interpréteur** : `.venv/Scripts/python.exe` (l'interpréteur ambiant n'a pas `pytest`) — D-15.
- **Interdits explicites utiles ici** : ne pas créer `docs/index.md` en plus de `docs/sommaire.md` ; ne pas
  vérifier les liens **externes** dans les tests ; ne **pas** ancrer un chiffre de valeur de base
  (`18288`, `3.6.10.11`) ; ne pas ajouter `docs/` au `.gitignore` ; ne pas installer MkDocs/Sphinx.

**Écarts mesurés entre `.claude/CLAUDE.md` et l'état livré — à ne pas suivre à la lettre :**

| Prescription de `.claude/CLAUDE.md` | État réel mesuré | Conséquence pour cette phase |
|---|---|---|
| `docs/sommaire.md` : H1 `# Documentation dofus-stuff-machine`, « parcours conseillé en 3 étapes » (`.claude/CLAUDE.md:76`) | H1 réel : `# Sommaire de la documentation` (`docs/sommaire.md:1`) ; parcours à **7** entrées (`:7-13`) | Le gabarit à suivre est celui **livré** (D-102), pas la prescription du document de recherche ; le H1 du sommaire n'est d'ailleurs gardé par **aucun** contrôle (le sommaire est exclu de `problemes_h1`). |
| `README.md` porte **7** liens vers les pages de `docs/` (`.claude/CLAUDE.md:96-105`) | Le README porte **un seul** lien interne, `docs/sommaire.md` (`README.md:7`), et `test_readme_links_to_sommaire` exige **exactement 1** (`tests/test_docs_structure.py:180-205`) | Ne pas « corriger » le README pour y ajouter 7 liens : la règle livrée est D-10, et l'ajout ferait échouer une garde verte. |
| `test_docs_directory_has_sommaire` vérifie « `sommaire.md` + les 7 pages attendues, et **aucun `.md` non listé** » (`.claude/CLAUDE.md:123`) | Le test réel (`tests/test_docs_structure.py:120-131`) ne vérifie que l'existence du dossier et de `sommaire.md` ; « aucun `.md` non listé » est tenu par `problemes_index`, **relativement à l'index** | La liste épinglée de D-95 n'existe **pas** aujourd'hui : c'est bien un ajout, et le document de recherche surestime la garde existante. |

---

## Architectural Responsibility Map

Cette phase ne construit aucune capacité produit : elle **documente** des capacités existantes et
**garde** cette documentation. La carte ci-dessous dit donc *d'où vient chaque énoncé* et *qui doit le
prouver* — c'est ce que le planificateur doit vérifier avant d'écrire une tâche.

| Capacité | Tier primaire (responsable) | Tier secondaire | Raison |
|---|---|---|---|
| Le message imprimé par une commande CLI | **CLI / produit** — `dofus_stuff/cli.py`, `dofus_stuff/sync.py`, `dofus_stuff/catalog.py`, `dofus_stuff/api.py` | Documentation (`docs/depannage.md`) | La documentation **se conforme** au code (D-19/D-103) : le message n'est jamais réécrit, il est cité. |
| Le message affiché par un écran web | **API / rendu Flask** — `dofus_stuff/web/routes.py`, `web/optimize_wizard.py`, `web/templates/screen.html` | Documentation | Le libellé naît du rendu (`_screen` compose la ligne de statut, `routes.py:141-150`) ; la sidebar de certitude est le **corps rendu**, jamais la réponse entière (`data-stuff-payload` échappe les accents). |
| Le comportement du clavier | **Client (JS)** — `dofus_stuff/web/static/js/terminal.js` | Gabarit HTML (`screen.html:61` `autofocus`) | Le clavier est du JavaScript : aucun contrôle Python ne peut l'**exécuter** ; le contrôle lit le fichier et le rendu (limite A2, déjà écrite en phase 5). |
| La liste épinglée des pages et l'ensemble des fichiers | **Harnais** — `tests/` | — | La complétude est un invariant de test (D-95/D-96), pas une propriété du produit. |
| La preuve que le harnais mord | **Harnais** — `tests/` + une batterie rejouable | — | D-97 : la preuve porte sur la copie, jamais sur l'arbre livré. |
| L'intégrité de `.data/` | **Harnais (mesure)** | — | Empreinte `(taille, mtime_ns, sha256)` prise autour de la suite entière ; le fichier n'est jamais ouvert par SQLite dans un contrôle d'intégrité (D-104). |

**Conséquence pour le planificateur :** aucune tâche de cette phase ne doit créer de capacité produit, ni
toucher `dofus_stuff/**`. Chaque tâche se répartit entre « lire le code pour écrire une page » (tier
CLI/rendu) et « écrire une garde dans `tests/` » (tier harnais).

---

## Measured inventory

Tout ce qui suit a été **mesuré cette session** sur le dépôt, sans exécuter `main()`, sans ouvrir de
connexion réseau et sans écrire sous `.data/`. Les mesures de rendu passent par le **client de test Flask
en processus** sur des bases `tmp_path` ; les mesures CLI passent par la **fonction de production**
`_print_db_status` sur une base `tmp_path` et par une **lecture `ast`** des littéraux de `cli.py::main`.
Les scripts de mesure sont conservés dans `.gsd-tmp/mesure-06.py` et `.gsd-tmp/mesure-06-cli.py` (hors
périmètre livrable, non suivis par git) pour que le planificateur puisse les rejouer.

### A. Les cinq familles du critère 1 — messages réellement produits

**A.1 — Base absente ou vide**

| # | Message verbatim | Où il est produit | Observé comment |
|---|---|---|---|
| 1 | `Fichier : ` | `dofus_stuff/cli.py:216` | `_print_db_status` sur base `tmp_path` (sortie capturée) |
| 2 | `Version jeu : (aucune)` | `dofus_stuff/cli.py:217` | idem — mesuré sur un dossier vide : le fichier est **créé** (`dofus.sqlite3` présent après l'appel) |
| 3 | `Dernier check : (aucun)` | `dofus_stuff/cli.py:223` | idem |
| 4 | `Entrées : 0` | `dofus_stuff/cli.py:224` | idem ; **aucune** ligne `Par catégorie :` n'est imprimée sur base vide (le bloc est conditionnel, `cli.py:226-229`) |
| 5 | `Par catégorie :` | `dofus_stuff/cli.py:227` | idem sur base peuplée (`  - equipment : 1`) |
| 6 | `Erreur : aucune version en base` | `dofus_stuff/cli.py:372` (littéral lu par `ast`) | littéral de `main`, **jamais** exécuté |
| 7 | `Erreur : Base locale vide et --offline : impossible de synchroniser` | message levé par `dofus_stuff/sync.py:43`, composé avec le préfixe `Erreur : ` de `dofus_stuff/cli.py:433` | littéraux des deux fichiers lus par `ast` ; message déjà ancré par `tests/test_docs_base_locale.py:320` (`MESSAGE_BASE_VIDE`) |
| 8 | `Aucun résultat.` | `dofus_stuff/cli.py:383` | littéral de `main` lu par `ast` |
| 9 | `Aucun objet sur cette page.` | `dofus_stuff/cli.py:399` | idem |
| 10 | `ERREUR : AUCUNE VERSION EN BASE.` (corps) et `AUCUNE VERSION EN BASE` (statut) | `dofus_stuff/web/routes.py:647-648` | rendu mesuré de `GET /version` sur catalogue vide |
| 11 | `VERSION JEU : (aucune)` | `dofus_stuff/web/routes.py:756` | rendu mesuré de `GET /db/status` sur base vide |
| 12 | `DERNIER CHECK : (AUCUN)` | `dofus_stuff/web/routes.py:762` | idem |
| 13 | `ENTREES : 0` | `dofus_stuff/web/routes.py:764` | idem ; **aucun** `PAR CATEGORIE :` (conditionnel `:766-770`) |
| 14 | `3 CONTROLE(S) EN ECHEC`, `[ECHEC] catalogue non vide`, `[ECHEC] objet 44 : 'Équipement introuvable : #44'` | `dofus_stuff/web/routes.py:671-684` + `dofus_stuff/catalog.py:77` | rendu mesuré de `GET /self-test` sur catalogue vide |

*Ce que la mesure interdit de citer sous cette rubrique :* aucune date, aucune taille de fichier, aucun
chemin de poste. La sortie réelle contient `Fichier : C:\…\dofus.sqlite3` — c'est une valeur **volatile de
la machine**, déjà prohibée par D-73/D-75 et par `tests/test_docs_base_locale.py:263` (`MOTIF_VOLATILE`).
La page ne cite donc que les **libellés**, jamais la ligne entière.

**A.2 — Saisie invalide**

| # | Message verbatim | Où il est produit | Observé comment |
|---|---|---|---|
| 1 | `SAISIE REQUISE` | `dofus_stuff/web/routes.py:308`, `:377`, `:461`, `:527`, `:596` | rendu mesuré : `POST /search` avec `query=""` → statut `SAISIE REQUISE — ENTREE=VALIDER` |
| 2 | `LIMITE INVALIDE` | `routes.py:319` | rendu mesuré : `POST /search` avec `query="Cape|abc"` → statut `LIMITE INVALIDE — ENTREE=VALIDER` |
| 3 | `AUCUN RESULTAT.` (corps et statut) | `routes.py:325` et `routes.py:351` | rendu mesuré : `POST /search` avec `query="zzzz"` → statut `AUCUN RESULTAT. — ENTREE=VALIDER` |
| 4 | `ID INVALIDE — ENTIER ATTENDU` | `routes.py:382`, `:418`, `:466`, `:532`, `:601`, `:611` | rendu mesuré : `POST /list` et `POST /item` avec `ankama_id="x"` |
| 5 | `'ÉQUIPEMENT INTROUVABLE : #999999'` (le message de `catalog.get_equipment` **passé en majuscules**) | `dofus_stuff/catalog.py:77` puis `routes.py:428` (`str(exc).upper()`) | rendu mesuré : `POST /item` avec `ankama_id=999999` |
| 6 | `OPTION INVALIDE — SAISIR 1 A 5` / `… 1 A 4` / `… 1 A 3` | `routes.py:226`, `:262`, `:740` | rendu mesuré pour `1 A 4` (`POST /system`, `selection="9"`) et `1 A 3` (`POST /db`) |
| 7 | `Saisissez le nom ou le numéro de votre classe.` | `routes.py:966` (`raise ValueError`) → affiché par `routes.py:985` | rendu mesuré : `POST /optimize/quick/classe` avec `cmd="zzz"` |
| 8 | `Exemple : feu, terre air, ou multi.` | `routes.py:974` | littéral de la fonction (même mécanisme) |
| 9 | `Saisissez un niveau entre 1 et 200.` | `routes.py:979` | rendu mesuré : `POST /optimize/quick/niveau` avec `cmd="999"` → statut `Saisissez un niveau entre 1 et 200. — ENTREE=CALCULER` |
| 10 | `SAISIE INVALIDE` | `dofus_stuff/web/optimize_wizard.py:308` (`raise ValueError("Saisie invalide")`) → `routes.py:1131` (`str(exc).upper()`) | rendu mesuré : `POST /optimize/wizard/slots` avec `cmd="zzz"` → statut `SAISIE INVALIDE — PAGE 1/2 — ENTREE=SUIVANT` |
| 11 | `FILTRE INVALIDE` / `SLOT INVALIDE` / `OPTION INVALIDE` | `optimize_wizard.py:293`, `:307`, `:333` (majuscules au rendu par `routes.py:1131`) | littéraux du module (le rendu suit le même chemin que le n° 10) |
| 12 | `Saisie invalide — voir aide syntaxe`, `Saisie vide`, `Aucune caractéristique valide`, `jet invalide : …`, `Niveau invalide : …`, `Nombre invalide pour …` | `dofus_stuff/optimize/profile_input.py:261`, `:240`, `:285`, `:255`/`:340`/`:391`, `:278`/`:353`, `:367` | littéraux du module ; lus par la CLI comme par le web via `OptimizeInputError` (cli.py:414 et 429-431, routes.py:985) |
| 13 | `Erreur : <message>` (préfixe unique de la CLI) | `dofus_stuff/cli.py:414`, `:430`, `:433` | littéraux de `main` lus par `ast` |
| 14 | `fetcher.py: error: unrecognized arguments: --offline` | produit par **argparse**, pas par le dépôt | déjà cité par `docs/cli.md:31-33` et `docs/installation.md:121` ; la page de dépannage doit **y renvoyer**, pas le réécrire (D-17) |

**A.3 — Calcul long**

| # | Message verbatim | Où il est produit | Observé comment |
|---|---|---|---|
| 1 | `Calcul en cours (CP-SAT)…` | `dofus_stuff/cli.py:416` (`print(..., flush=True)`) | littéral de `main` lu par `ast` — **le seul message d'attente du produit** |
| 2 | `ENTREE=CALCULER` | `dofus_stuff/web/routes.py:1008` (`enter_hint="CALCULER"`) composé en `routes.py:148` | rendu mesuré : `GET /optimize/quick/niveau` → statut exactement `ENTREE=CALCULER` |
| 3 | `NIVEAU 200  JET=average  DUREE=5s` (forme `NIVEAU {level}  JET={jet_mode}  DUREE={time_limit_s:g}s`) | `dofus_stuff/web/optimize_wizard.py:266` | rendu mesuré : `GET /optimize/wizard/recap` |
| 4 | `GO = LANCER  RESET = REINITIALISER  1-8 = RETOUR ECRAN` | `optimize_wizard.py:269-272` (rendu `GO = LANCER`) | rendu mesuré du récapitulatif |
| 5 | `3. DUREE (S)       = {spec.time_limit_s:g}` | `optimize_wizard.py:204` | littéral + lecture du module |
| 6 | `CALCUL TERMINE` | `routes.py:925` (`flash` après `optimize_stuff`) | littéral du module ; le calcul est **synchrone**, l'utilisateur ne voit ce message qu'à la fin |
| 7 | `Timeout CP-SAT en secondes`, `Désactiver CP-SAT (greedy + local uniquement)`, défaut `5.0` | `dofus_stuff/cli.py:105-115` (`--time-limit`, `--no-cpsat`) | littéraux de `build_parser` lus par `ast` |

**Aucun message ne dit qu'un calcul est long, ni ne promet une durée bornée à l'utilisateur** : le code
expose un **budget** (`--time-limit`, 5 s par défaut) et un **état** (`Calcul en cours (CP-SAT)…`,
`ENTREE=CALCULER`). Toute rubrique qui écrirait « le calcul peut prendre plusieurs minutes » inventerait
une sémantique (D-19) ; elle doit dire ce que le produit dit, et renvoyer au réglage du budget.

**A.4 — Clavier inactif — AUCUN MESSAGE TROUVÉ (constat, pas un oubli)**

Recherche mesurée : `grep -rn "inactif|INACTIF|gelé|GELE|FIGE|figé|bloqu|BLOQU|CLAVIER|clavier|keyboard"`
sur tout le dépôt → **une seule occurrence de « clavier » dans un artefact non produit**
(`.claude/CLAUDE.md:82`, qui nomme la rubrique « clavier inactif (focus du champ) »), **zéro occurrence**
dans `dofus_stuff/**`. **Je n'ai pas trouvé de message produit par le code pour cette famille.** Ce que le
code porte est un mécanisme, mesuré sur trois fichiers :

| # | Fait mesuré | Provenance |
|---|---|---|
| 1 | Le champ de saisie porte `autofocus` ; il n'existe que si `input_label` n'est pas `None` | `dofus_stuff/web/templates/screen.html:51-63` (`autofocus` : `:61`) |
| 2 | Au chargement, le script appelle `input.focus()` ; un `mousedown` ailleurs que dans le champ est intercepté (`e.preventDefault()`) puis refocalise le champ | `dofus_stuff/web/static/js/terminal.js:80-88` |
| 3 | `Entrée` ne soumet le formulaire que si `document.activeElement === input` (sinon le gestionnaire rend la main et la touche n'a aucun effet de saisie) | `dofus_stuff/web/static/js/terminal.js:595-597` |
| 4 | Les écrans **sans champ** de saisie laissent le clavier sans effet autre que `F3`/`ESC`/`F7`/`F8`/`PageUp`/`PageDown` | rendu mesuré : `GET /version`, `GET /db/status`, `GET /quit` → **`AUCUN champ de saisie`** (pas de `id="main-input"`), barre `ESC=Retour` (et `ESC=Menu` pour `END-01`) ; `routes.py:655-670`, `:781-786`, `:266-283` passent `input_label=None` |
| 5 | La description déjà livrée du mécanisme | `docs/installation.md:55` (« Un clic ailleurs sur la page ramène automatiquement le curseur dans ce champ ») et `docs/installation.md:69` (barre construite dynamiquement) |

**Conséquence pour D-93 :** la rubrique « clavier inactif » s'adosse à ces **faits** (champ `autofocus`,
refocalisation, `Entrée` conditionné à la saisie, écrans sans champ), jamais à une chaîne imprimée. Et
**D-17 s'applique ici** : `docs/installation.md:55` et `:69` disent déjà le mécanisme → la rubrique doit
y **renvoyer** (lien) plutôt que le redéfinir.

**A.5 — Résultat paginé**

| # | Message verbatim | Où il est produit | Observé comment |
|---|---|---|---|
| 1 | `PAGE {page}/{total}` (motif de gabarit) | `dofus_stuff/web/routes.py:145` (`indicators.append(f"PAGE {page}/{total}")`) | rendu mesuré : `GET /list?page=1&size=1` → statut `PAGE 1/3 — ENTREE=VALIDER`, `GET /list?page=2&size=1` → `PAGE 2/3 — ENTREE=VALIDER` |
| 2 | `ENTREE=VALIDER` | `routes.py:147-148` (composé en `:150` par `" — ".join(indicators)`) | idem |
| 3 | `Page prec` / `Page suiv` (utilisation **paginée** d'un écran) | `routes.py:138-139` (`f7_label`/`f8_label` quand aucun `f7_url`/`f8_url` n'est fourni) | rendu mesuré : `GET /list?page=1&size=1` → couples `F7=Page prec`, `F8=Page suiv` |
| 4 | `Precedent` / `Suivant` (étape explicite de wizard) | `routes.py:138-139` (`f7_url`/`f8_url` fournis) | rendu mesuré : `GET /optimize/wizard/recap` → `F7=Precedent`, `F8=Page suiv` (fin de parcours) ; `GET /optimize/wizard/caracs` → `F7=Precedent`, `F8=Suivant` |
| 5 | `PAGE {page}/{total}   TAILLE {size}   TOTAL EQUIPEMENTS {total}` (ligne de corps) | `dofus_stuff/web/routes.py:477` | rendu mesuré : `PAGE 1/3   TAILLE 1   TOTAL EQUIPEMENTS 3` |
| 6 | `PAGE 1/1   TAILLE 1   TOTAL PANOPLIES 0` + `AUCUNE PANOPLIE SUR CETTE PAGE.` | `dofus_stuff/web/routes.py:543` et littéral de corps | rendu mesuré : `GET /sets?page=1&size=1` → statut `ENTREE=VALIDER` (pas de `PAGE n/n` au statut quand `total == 1`, `routes.py:144`) |
| 7 | `Page suivante disponible : ` | `dofus_stuff/cli.py:407` | littéral de `main` lu par `ast` (le lien `_links.next` vient de `catalog.py:164`) |
| 8 | `PAGE n/total` dans les écrans de sauvegardes | `dofus_stuff/web/static/js/terminal.js:370` et `:400` | lecture du fichier ; déjà cité par `docs/parcours-simplifie.md:176` |

**Piège mesuré du critère 1 :** `total == 1` **supprime** le motif du statut (`routes.py:144-145`) alors
que la ligne de corps le porte toujours (`routes.py:543`). Une rubrique qui exigerait `PAGE n/n` dans la
ligne de statut d'un écran non paginé serait **rouge sur un produit correct** (cette leçon est exactement
celle d'ECR-2, `.planning/WINDOWS.md` ligne `id=6`).

**A.6 — Comment un contrôle observe chaque famille sans toucher `.data/` ni exécuter `main()`**

Toutes les routes ci-dessous ont été **employées cette session** ; aucune n'ouvre `.data/`, aucune ne
lance de processus, aucune ne contacte le réseau.

| Famille | Route de mesure (sans `.data/`, sans `main()`) | Ce que ça prouve / limite |
|---|---|---|
| Base absente ou vide | **CLI** : instancier `Database(data_dir=tmp_path/"x")`, appeler `_print_db_status(db)` et capturer `stdout` par `contextlib.redirect_stdout` — patron déjà écrit dans `tests/test_docs_base_locale.py:1235` (`_sortie_db_status`). **Web** : `create_app(data_dir=tmp_path/…, offline=True, catalog=Catalog(version=None, items={}), load_catalog=False)` puis `client.get("/version")`, `client.get("/db/status")`, `client.get("/self-test")` (fixture `app` de `tests/conftest.py:83-111`, qui construit déjà sa base sous `tmp_path`). | La fonction de production est appelée, `main()` ne l'est jamais ; le fichier créé est sous `tmp_path`, jamais `.data/`. |
| Saisie invalide | **Web** : `client.post(...)` avec `follow_redirects=True` (les refus sont des `flash` + `redirect`) et lecture de la **ligne de statut** (helper `_statut`, `tests/test_docs_parcours.py:316-320`). **CLI** : littéraux de `main` lus par `ast` (les messages de `profile_input.py` sont, eux, atteignables par leurs fonctions publiques). | Le statut est la seule source des messages de refus ; poster un formulaire ne déclenche **aucun** calcul sur `/search` et `/list`. |
| Calcul long | **CLI** : littéral de `cli.py:416` lu par `ast` (jamais exécuté, le calcul serait lancé). **Web** : `client.get("/optimize/quick/niveau")` et `client.get("/optimize/wizard/recap")` (rendus, aucun `POST`). | Aucun calcul n'est lancé : `POST /optimize/quick/niveau` **est** le calcul, il n'est jamais posté par les contrôles. |
| Clavier inactif | **Lecture** de `terminal.js` (lignes citées en A.4) + **rendu** des écrans sans champ (`/version`, `/db/status`, `/quit`) : l'absence de `id="main-input"` est mesurable sur la réponse. | Aucun DOM, aucun navigateur : l'**exécution** JS n'est pas observable (limite A2, honnêtement déclarée depuis la phase 5). |
| Résultat paginé | **Web** : `client.get("/list?page=1&size=1")` sur une fixture à ≥ 2 équipements (la fixture `catalog` en porte **3** : `tests/conftest.py:20-54`), lecture du statut et de la barre `fkeys`. **CLI** : `catalog.list_equipment_page` est une fonction publique pure (`dofus_stuff/catalog.py:144`) ; `Page suivante disponible : ` est un littéral de `main` lu par `ast`. | La pagination est mesurée sur le rendu réel, sans serveur ni navigateur. |

### B. Le vocabulaire (critère 2)

Décision de lecture : le glossaire ne doit **pas** redéfinir ce qui est déjà défini ailleurs (D-17). La
colonne « déjà défini » dit donc, pour chaque terme, s'il faut **le définir** (aucune définition livrée)
ou **y renvoyer** (la définition existe déjà dans une page). Chaque ligne porte la provenance de
l'**emploi** du terme.

**Vocabulaire du produit**

| Terme | Emploi mesuré (file:line) | Déjà défini ailleurs ? → geste |
|---|---|---|
| `base locale` | `dofus_stuff/cli.py:33` (`"API Dofus — base locale Dofusdude"`), `:39` (aide de `--data-dir`), `:54`, `:182` (`"Gérer la base locale"`), `:189` (`"Vider la base locale"`) ; `README.md:9` | **Oui** : `docs/base-locale.md` (page entière, H1 `# Base locale`, `:1`) → renvoyer |
| `synchronisation` | `dofus_stuff/cli.py:44` (`"Ignorer la fenêtre 24h et forcer une vérif / sync version"`), `:187` (`"Forcer la synchronisation complète"`) ; `dofus_stuff/web/routes.py:713` (`"2. SYNCHRONISATION FORCEE (SYNC)"`), `:839` (`SYNCHRONISATION TERMINEE`) | **Oui** : `docs/base-locale.md:111-115` → renvoyer |
| `mode hors-ligne` | `dofus_stuff/cli.py:49` (aide de `--offline`) ; `docs/base-locale.md:47` ; `docs/installation.md:79` | **Oui** : `docs/base-locale.md:41-55` → renvoyer |
| `wizard` | `dofus_stuff/web/routes.py:1031` (`ECRAN WIZARD INCONNU`), `:1029` (route `/optimize/wizard/<step>`) ; `dofus_stuff/web/optimize_wizard.py:36` (`"slots": "SLOTS ET FILTRES"`) | **Oui** : `docs/wizard-avance.md` (page entière) → renvoyer |
| `stuff` | `dofus_stuff/cli.py:70` (`"Optimiser un stuff pour un niveau…"`) ; `dofus_stuff/web/routes.py:986` (`VOTRE STUFF EN 3 CHOIX`), `:1006` (`RECOMMANDATION DE STUFF`) ; `terminal.js:316` (`STUFF SAUVEGARDE`) | **Partiellement** : `docs/sommaire.md:20` (« Obtenir un stuff en 3 questions ») l'emploie sans le définir → **définir** (une ligne) |
| `catégorie` / `kind` | `dofus_stuff/database.py:18-26` (`ITEM_KINDS`) ; `cli.py:227` (`Par catégorie :`) ; `routes.py:767` (`PAR CATEGORIE :`) | **Oui** : `docs/base-locale.md:20-33` (les 7 catégories nommées) → renvoyer |
| `slot` / `emplacement` | `dofus_stuff/model/solver_spec.py:15` (`SLOT_GROUPS`), `:29` (`DEFAULT_SLOT_GROUPS`) ; `optimize_wizard.py:180` (`SLOTS (N=TOGGLE) :`) | **Partiellement** : `docs/wizard-avance.md:37` et `:49` expliquent « emplacements d'équipement » → renvoyer |
| `jet` | `dofus_stuff/cli.py:99-103` (`--jet`, `choices=("min","average","max")`, `"Mode de jets d'objets (défaut: average)"`) ; `optimize_wizard.py:266` (`JET=average`) | **Partiellement** : `docs/wizard-avance.md:124`, `docs/parcours-simplifie.md:107` → renvoyer |
| `exo` | `dofus_stuff/model/solver_spec.py:80` (`EXO_STATS = ("PA", "PM", "Portée")`) ; `docs/wizard-avance.md:132` (`FORMAT : BASE EXO CIBLE POIDS`) | **Oui** : `docs/parcours-simplifie.md:226-228` → renvoyer |
| `palier` | `docs/parcours-simplifie.md:196`, `:198-209` (paliers de coût de caractéristique et paliers PA/PM) | **Oui, en détail** : `docs/parcours-simplifie.md:198-209` → renvoyer, **ne pas redéfinir** |
| `heuristique` / `greedy` | `dofus_stuff/optimize/score.py:8` (`Literal["optimal_prouve","borne_solver","borne_heuristique"]`), `:58` ; `dofus_stuff/optimize/greedy.py` (module) ; `docs/cli.md:143` (`greedy et recherche locale`) | **Oui** : `docs/parcours-simplifie.md:238`, `:261` → renvoyer |
| `solveur` / `CP-SAT` | `dofus_stuff/cli.py:109`, `:114` (aides `--time-limit`, `--no-cpsat`) ; `docs/wizard-avance.md:38` (`OPTIONS SOLVEUR`) | **Partiellement** : `docs/parcours-simplifie.md:142`, `:242` → renvoyer |
| `poids` | `dofus_stuff/cli.py:136` (`"Poids STAT=valeur (ex: intelligence=2 vitalite=0.5)"`) ; `optimize_wizard.py:268` (`POIDS : `) | **Partiellement** : `docs/wizard-avance.md:128-133` → renvoyer |
| `cible` | `dofus_stuff/cli.py:130` (`"Cibles STAT=valeur (ex: intelligence=1200 pa=11)"`) ; `optimize_wizard.py:269` (`CIBLES : `) | **Partiellement** : `docs/wizard-avance.md:128-133` → renvoyer |
| `ID Ankama` | `dofus_stuff/cli.py:62` (`"ID Ankama de l'objet"`), `:143` (`"Ankama IDs interdits"`) ; `dofus_stuff/database.py:55` (`ankama_id INTEGER NOT NULL`) | **Oui** : `docs/cli.md:63`, `:67` → renvoyer |
| `panoplie` / `set` | `dofus_stuff/catalog.py:83` (`Panoplie introuvable : #`), `:246-293` (`format_set_summary`) ; `database.py:25` (`"sets"`) ; `routes.py:543` (`TOTAL PANOPLIES`) | **Oui** : `docs/base-locale.md:31` → renvoyer |
| `Dofus` / `trophée` / `familier` / `prysmaradite` / `bouclier` | `dofus_stuff/cli.py:119` (`"Ignorer Dofus/Trophées, familier et prysmaradite"`) ; `solver_spec.py:15-27` (clés de `SLOT_GROUPS`) | **Oui** : `docs/parcours-simplifie.md:144`, `:162`, `:164` ; `docs/cli.md:112` → renvoyer |
| `score` / `indice de recherche` | `dofus_stuff/optimize/score.py` (module) ; `terminal.js:241-247` (`Méthode`/`Score`) | **Oui** : `docs/parcours-simplifie.md:238`, `:264` → renvoyer |
| `sauvegarde locale` (`SAVE`, `SAVES`) | `terminal.js:279-319` (`SAVES_KEY`, `STUFF SAUVEGARDE`), `:459-471` (`PURGE OUI`) ; `routes.py:1282` (route `saves`) | **Oui** : `docs/parcours-simplifie.md:168-176` → renvoyer |
| `ligne de statut` / `barre de raccourcis` / `écran 100x24` | `dofus_stuff/web/screens.py:5-11` (`COLS`, `ROWS`, `BODY_LINES`, `FOOTER_START`) ; `screen.html:49` (`row status`) ; `routes.py:150` (composition du statut) | **Oui** : `docs/parcours-simplifie.md:27`, `:50`, `:140` ; `docs/installation.md:69` → renvoyer |

**Vocabulaire de la documentation** — mesuré : **trois** termes seulement sont employés par les pages
livrées et nulle part définis.

| Terme | Emploi mesuré | Déjà défini ? → geste |
|---|---|---|
| `sommaire` | `docs/sommaire.md:1` (`# Sommaire de la documentation`) ; lien de retour de **chaque** page (`[Retour au sommaire](sommaire.md)`, dernière ligne des 5 pages de contenu) | **Non** → définir (une ligne : point d'entrée unique, D-04) |
| `parcours conseillé` | `docs/sommaire.md:5` (`## Parcours conseillé`) | **Non** → définir, puis renvoyer à la section elle-même |
| `index` | `docs/sommaire.md:15` (`## Index`) | **Non** → définir (la table page → sujet) |
| `source de vérité` | `docs/base-locale.md:135`, `docs/cli.md:188`, `docs/installation.md:131`, `docs/parcours-simplifie.md:258`, `docs/wizard-avance.md:216` (`## Source de vérité`) | **Non**, mais c'est un **titre de section** du gabarit : le définir une fois suffit, la page de dépannage n'a pas à le redire |

**Termes à NE PAS mettre au glossaire** (mesuré : 0 occurrence dans `docs/` **et** dans `dofus_stuff/**`,
ce sont des termes de harnais/planification) : `page épinglée` (vocabulaire de D-95, `.planning/`
seulement), `renvoi` (`tests/test_docs_parcours.py:2314` `RENVOIS_SANS_LIEN`, `:2865` `ANCRES_RENVOI_D63`),
`ancrage` (`tests/test_docs_code_anchor.py:1`, titre de module). Les définir serait **inventer de la
sémantique produit** (D-19) et exposer des mots que le lecteur ne rencontrera jamais à l'écran.

**Liste de candidats d'un autre artefact, à traiter avec méfiance :** `.claude/CLAUDE.md:83` prescrit
« Stuff, slot, solveur, poids, cible, ID Ankama, jet, exo, panoplie, dofus, trophée, prysmaradite — trié
alphabétiquement ». C'est une **liste de recherche de la phase 1**, jamais confirmée par une garde, et elle
omet le vocabulaire **documentaire** que le critère 2 exige aussi (« le vocabulaire du produit **et de la
documentation** »). Elle sert de garde-fou de non-oubli, pas de contrat.

### C. L'ensemble exact des fichiers, la liste épinglée et le parcours (critère 3)

**C.1 — Inventaire livré, mesuré (`docs/` : 6 fichiers, tous `.md`)**

| Fichier | Octets | Lignes | CRLF | BOM | Dernière ligne non vide |
|---|---:|---:|---:|---|---|
| `base-locale.md` | 13 755 | 141 | 141 | non | `[Retour au sommaire](sommaire.md)` |
| `cli.md` | 9 381 | 195 | 195 | non | `[Retour au sommaire](sommaire.md)` |
| `installation.md` | 7 380 | 141 | 141 | non | `[Retour au sommaire](sommaire.md)` |
| `parcours-simplifie.md` | 20 174 | 269 | 269 | non | `[Retour au sommaire](sommaire.md)` |
| `sommaire.md` | 815 | 23 | 23 | non | `\| [Base locale](base-locale.md) \| La bas…` (une ligne d'index, **pas** un retour) |
| `wizard-avance.md` | 16 554 | 224 | 224 | non | `[Retour au sommaire](sommaire.md)` |

`git ls-files --eol docs/` rend `i/lf  w/crlf  attr/` pour les six : l'arbre de travail est **CRLF** et
l'index git **LF** (`core.autocrlf=true`, aucun `.gitattributes`) — l'assertion CRLF est donc vraie **par
construction sur ce poste** (limite AR-5, non résolue, à déclarer comme les phases 3 à 5 le font).

**C.2 — La liste épinglée des 8 pages.** `docs/` doit contenir **exactement** :

`sommaire.md`, `installation.md`, `parcours-simplifie.md`, `wizard-avance.md`, `cli.md`, `base-locale.md`,
`depannage.md`, `glossaire.md`.

Provenance : `.claude/CLAUDE.md:76-83` énumère exactement ces 8 fichiers dans sa table
« fichier → exigence → contenu prescrit », et `.claude/CLAUDE.md:93` écrit « Le sommaire liste les **7
autres pages** » — donc 7 pages de contenu **+** le sommaire. L'arithmétique mesurée concorde : 6
fichiers livrés aujourd'hui, **2** à livrer par cette phase (`depannage.md`, `glossaire.md`) → 8.
Cette liste est `[CITED]` d'un document de recherche et non d'un artefact de planification : le
planificateur la **figera** comme constante de D-95 (voir A1 de l'*Assumptions Log*).

**C.3 — Les gardes existantes qui portent déjà l'index et le H1 (à NE PAS dupliquer, D-96)**

| Garde | Fichier:ligne | Ce qu'elle tient déjà | Morsure mesurée cette session |
|---|---|---|---|
| `problemes_liens` | `tests/test_docs_structure.py:39-89` | Chaque cible de lien interne de `docs/` résout et reste sous la racine ; refuse `#`, chemins absolus, antislashs, `file://` | **Oui** : copie sans `docs/cli.md` → `lien mort vers cli.md` |
| `test_all_relative_links_resolve` | `tests/test_docs_structure.py:157` | Idem, sur toutes les pages | **Oui** |
| `problemes_index` | `tests/test_docs_structure.py:92-119` | **Égalité d'ensembles** entre les cibles du sommaire et les pages présentes (hors sommaire), dans les deux sens | **Oui** : page supprimée → `cible listee absente sur disque : cli.md` ; page ajoutée → `page non listee dans docs/sommaire.md` |
| `test_sommaire_lists_every_document` | `tests/test_docs_structure.py:134` | Appelle `problemes_index` | **Oui** |
| `problemes_h1` | `tests/test_docs_structure.py:337-380` | Un **unique** H1 par page, **égal** au libellé d'index après normalisation (D-11) | **Oui** : H1 muté → `H1 « Installation provisoire » different du libelle d'index « Installation »` |
| `test_h1_matches_sommaire_entry` | `tests/test_docs_structure.py:468` | Appelle `problemes_h1` | **Oui** |
| `problemes_retour_sommaire` | `tests/test_docs_structure.py:383-417` | Ligne de retour vers `sommaire.md` (le sommaire est **exclu** de la règle) | Patron existant |
| `problemes_encodage` | `tests/test_docs_structure.py:418-447` | UTF-8 strict, aucun jeton de brouillon, ≥ 300 caractères | Patron existant |
| `test_sommaire_index_labels_are_unique` | `tests/test_docs_structure.py:492` | Libellés d'index distincts, sommaire non auto-listé | Patron existant |
| `test_mutation_detecte_les_trois_derives` | `tests/test_docs_structure.py:533-603` | Copie `tmp_path`, **verte avant mutation**, puis trois dérives (lien mort, page non indexée, H1 divergent) | Patron existant — voir § D |

**Ce qui manque et que cette phase doit ajouter :** une constante de **liste épinglée** comparée à
l'ensemble des fichiers de `docs/` (l'égalité d'ensembles index↔disque n'interdit pas une page **listée et
présente** qui ne serait pas l'une des 8), un contrôle des **entrées du glossaire** (existence + ordre), un
contrôle **message → rubrique** de la page de dépannage, et la garde du **parcours conseillé** qui n'existe
pas.

**C.4 — Le parcours conseillé actuel, mesuré (`docs/sommaire.md:5-13`)**

Extrait verbatim de `docs/sommaire.md:5-13` (cité en bloc pour ne pas être confondu avec une section de ce document) :

> ## Parcours conseillé
>
> 1. Installation
> 2. Parcours simplifié
> 3. Wizard avancé
> 4. CLI
> 5. Base locale
> 6. Dépannage
> 7. Glossaire

Quatre faits à verser au plan :

1. Le parcours **annonce deux pages qui n'existent pas** (`6. Dépannage`, `7. Glossaire`) : il est donc
   **faux sur disque** aujourd'hui. Après livraison des deux pages, il devient vrai — ce qui fait du
   parcours un **effet du plan 06-02**, pas une réécriture gratuite.
2. **Aucune garde ne le lit** : `grep -rn "Parcours" tests/*.py` → **0 occurrence**. Le parcours est du
   texte simple (pas de liens) : ni `problemes_liens` ni `problemes_index` ne peuvent le voir.
3. Il **diverge de l'index sur l'ordre** : le parcours met `Wizard avancé` en 3ᵉ et `CLI` en 4ᵉ, l'index
   (`docs/sommaire.md:19-23`) met `CLI` en 3ᵉ et `Wizard avancé` en 4ᵉ. C'est de la *discretion* : le plan
   décide l'ordre de lecture, puis le rend **cohérent et vérifiable**.
4. Il **n'oublie aucune page livrée** (les 5 pages existantes y sont), et il est le **seul** endroit du
   sommaire qui mentionne `Dépannage`/`Glossaire` avant leur indexation — l'index, lui, n'a que 5 lignes
   (`docs/sommaire.md:19-23`, mesuré).

### D. Provabilité du harnais (critère 4) — mécanismes mesurés par famille de dérive

**D.1 — Le mécanisme établi (à recopier tel quel).** Les phases 3 à 5 ont rejoué leurs morsures avec
**le même patron**, conservé dans `.gsd-tmp/batterie-05-02-t1.sh`, `.gsd-tmp/verif-06.sh` et
`.gsd-tmp/verif-suite-05-02.sh` :

```
T="$(mktemp -d)"
cp -r docs tests dofus_stuff fetcher.py pyproject.toml GUIDE_WIZARD.md README.md "$T"/
avant="$(cd "$T" && "$PY" -m pytest tests/<module>.py -q 2>&1)"
#  -> refus si la copie est ROUGE avant mutation (« la morsure ne serait pas discriminante »)
<mutation, sur "$T" uniquement>
out="$(cd "$T" && "$PY" -m pytest -q 2>&1)"
#  -> succès si la sortie porte `[0-9]+ (failed|error)` ET le motif nommé cherché par `grep -qF`
```

Deux invariants sont non négociables (D-97, leçon des phases 3 à 5) : **la copie est verte avant
mutation**, et **le motif nommé est cherché dans la sortie d'échec** (`grep -F`). Le patron est déjà
**matérialisé en test** par `tests/test_docs_structure.py:533` (`test_mutation_detecte_les_trois_derives`),
qui copie `docs/` avec `shutil.copytree` et **appelle les trois fonctions de garde** sur la copie.

**D.2 — Les trois dérives du critère 4, mesurées cette session sur des copies réelles** (copie de
`docs tests dofus_stuff fetcher.py pyproject.toml GUIDE_WIZARD.md README.md`, sous
`mktemp -d` ; copie **verte** mesurée à `216 passed, 3 skipped` — les 3 `skip` sont les mesures
d'empreinte `.data/`, qui n'ont pas d'objet hors du dépôt, `MOTIF_BASE_ABSENTE`) :

| Dérive | Mutation réellement appliquée | Ce qui a mordu (mesuré) | Motif à chercher dans la sortie |
|---|---|---|---|
| **(i) page manquante** | `rm docs/cli.md` | **`14 failed, 202 passed, 3 skipped`** ; constats : `docs/sommaire.md : cible listee absente sur disque : cli.md ; attendu une page presente sous docs/ (SOMM-02, D-06)` (via `problemes_index`) **et** `docs/wizard-avance.md : lien mort vers cli.md` (via `problemes_liens`) | `cible listee absente sur disque` |
| **(ii-a) libellé dérivé — H1 ≠ libellé d'index** | `# Installation\r\n` → `# Installation provisoire\r\n` (remplacement sur **octets**, CRLF préservé) | `1 failed` ; `docs/installation.md : H1 « Installation provisoire » different du libelle d'index « Installation »` (`test_h1_matches_sommaire_entry`, `tests/test_docs_structure.py:468`) | `different du libelle d'index` |
| **(ii-b) libellé dérivé — nom cité non produit par le code** | `Quitter` → `Fermer` dans `docs/installation.md` | `1 failed` ; `installation.md : libellé « Quitter » absent de la section « ## Pilotage clavier » ; attendu ce libellé…, parce que dofus_stuff/web/routes.py le produit` (`test_libelles_cites_sont_produits_par_le_code`, `tests/test_docs_code_anchor.py:240`) | `absent de la section` |
| **(iii) renvoi obsolète** | cible d'un lien remplacée par une page absente (`sommaire.md` → `sommaire.mrd` dans la copie ; patron de `tests/test_docs_structure.py:554-560`) | `problemes_liens` produit `lien mort vers sommaire.mrd` ; le cas mesuré en (i) prouve le même détecteur sur une cible supprimée | `lien mort vers` |

**Limite mesurée de (ii-b) — à écrire dans le module, pas à masquer :** j'ai rejoué la dérive avec un nom
qui **contient** le libellé réel (`Quitter` → `Quitter tout`) : **`216 passed, 3 skipped`**, la suite
**reste verte**. La garde compare par **appartenance de sous-chaîne** (`test_docs_code_anchor.py:243`,
`assert libelle in corps`), elle ne détecte donc pas un libellé **sur-accentué** tant que le libellé réel y
reste contenu. La morsure du critère 4 doit utiliser un nom qui **ne contient pas** le libellé produit
(`Fermer`), et la limite doit être déclarée (D-85).

**D.3 — Ce que le nouveau test peut faire en processus, et ce qu'il ne peut pas.** Le patron
`test_mutation_detecte_les_trois_derives` est **sans `subprocess`** : il importe les fonctions de garde et
les appelle sur la copie. C'est la seule forme compatible avec la **garde de clôture** que les quatre
modules d'ancrage portent déjà — `RACINES_INTERDITES` refuse `subprocess` **et** `socket`, `urllib`,
`sqlite3` :

- `tests/test_docs_cli.py:227` : `INTERDITS_EXECUTION = ("subprocess", "socket", "sqlite3")`
- `tests/test_docs_parcours.py:268` : `RACINES_INTERDITES = (… "subprocess" …)`
- `tests/test_docs_wizard.py:313` : idem
- `tests/test_docs_base_locale.py:411-423` : idem, avec `APPEL_PRODUIT = "main"` (`:430`)

**Conséquence de plan, à trancher explicitement :** un test de mutation **en pytest** peut prouver que les
*gardes* mordent (appel des fonctions sur la copie), mais **pas** que `pytest` échoue : cela demanderait de
lancer `pytest` dans la copie, donc `subprocess`, donc un **écart à la garde de clôture** — à écrire,
justifié et nommé, ou à reporter sur une batterie rejouable. Les deux voies sont mesurées :

| Voie | Ce qu'elle prouve | Coût / limite |
|---|---|---|
| `tests/test_docs_mutation.py` **en processus** (recommandée) : `shutil.copytree(docs_dir, tmp_path/"docs")`, appeler `problemes_index`, `problemes_liens`, `problemes_h1` sur la copie, puis (pour le libellé cité) la fonction de comparaison du module d'ancrage concerné | Que **chaque garde** produit son constat nommé sur une copie portant la dérive, la copie étant verte avant | N'exécute pas `pytest` sur la copie : « le harnais échoue » est prouvé **au niveau des fonctions de garde**. Ne peut pas voir les gardes non paramétrables (`RACINE_DEPOT` figé dans `tests/test_docs_parcours.py:2937`) |
| Batterie rejouable (script, hors `tests/`) : `cp -r … mktemp -d` → pytest vert → mutation → `pytest -q` → `grep -F <motif>` | Que **`pytest` entier** échoue **avec le motif nommé** | N'est pas un test pytest ; c'est la **preuve de vérification** à coller dans le `SUMMARY.md`, comme `05-VERIFICATION.md § Behavioral Spot-Checks` l'a fait |

**Recommandation :** faire **les deux** — la voie 1 satisfait la lettre de D-97 (« un test de mutation »)
sans casser la convention de clôture ; la voie 2 fournit la sortie réelle (`N failed … motif`) que le
rapport de vérification exige. Si le plan retient un `subprocess` dans un module de `tests/`, il doit
l'**écrire** dans le module (constante de motif `MOTIF_GARDE`) et le **justifier** dans sa docstring, sans
quoi la garde de clôture du module neuf rougira — c'est le patron de toutes les phases précédentes.

**D.4 — Le piège CR mesuré.** `sed -i` sous Git-for-Windows **supprime les `\r`** : mesuré cette session
sur un fichier CRLF copié (`sed (GNU sed) 4.9`) — un fichier `a\r\nb\r\nc\r\n` devient `a\nb\nc\n` après un
`sed -i 's/…/…/'` qui ne touchait **pas** les fins de ligne. Conséquence : une mutation appliquée par
`sed -i` sur une page de `docs/` fait **aussi** rougir l'assertion CRLF (`MOTIF_CRLF = "fins de ligne"`,
`tests/test_docs_base_locale.py:282`, `:2157`), et la morsure devient **confondue** — deux causes, un seul
constat. **Route de mutation recommandée (celle qu'ont employée les plans 05-02/05-04) :** muter par
Python, en **octets**, avec des ancres CRLF explicites — c'est ce que j'ai fait pour les mesures (ii-a) et
(ii-b) ci-dessus :

```python
# Patron CR-preservant, mesure cette session (5 fois) : la mutation ne touche que la copie.
p = pathlib.Path(copie / "docs" / "installation.md")
s = p.read_bytes().decode("utf-8")
assert "<ancre>" in s, "ancre absente : la mutation ne mesurerait rien"
p.write_bytes(s.replace("<ancre>", "<derive>", 1).encode("utf-8"))
```

Pour un fichier **ajouté**, écrire explicitement du CRLF : `(copie/"docs"/"x.md").write_bytes(
b"# X\r\n\r\n...\r\n")` (patron de `tests/test_docs_structure.py:562-564`).

**D.5 — Le piège `__future__` + import injecté (mesuré, avec sa cause).** Une morsure qui insère un
`import` interdit **en tête** d'un module de test ne peut pas mordre si ce module porte
`from __future__ import annotations` en deuxième ligne : la source devient invalide et le module **meurt à
la collecte** (`SyntaxError: from __future__ imports must occur at the beginning of the file`) ; `ast.parse`
l'accepte mais `compile` — que la réécriture d'assertions de pytest utilise — la refuse. Mesure d'origine :
`.planning/phases/05-…/05-01-SUMMARY.md:179-184`. **Conséquence :** le module neuf de la phase 6 ne doit
pas porter `from __future__ import annotations` **si** l'une de ses morsures injecte un import en tête
(c'est le cas de `tests/test_docs_base_locale.py`, qui documente le refus en tête de fichier, `:36-42`) ;
et aucune mutation ne doit insérer d'import dans un module de test.

### E. La vérification finale (critère 5) — mesuré cette session

**E.1 — Commandes et résultats réels**

| Commande | Résultat mesuré | Remarque |
|---|---|---|
| `./.venv/Scripts/python.exe -m pytest -q` | **`219 passed in 4.31s`** (temps mural `0m4.741s`) | interpréteur de référence (D-15) ; **0 skipped** sur le dépôt |
| `PYTHONPATH=<greffon> … -m pytest -q -p no_net` | **`219 passed in 4.13s`** | greffon qui refuse `socket.socket`, `socket.create_connection`, `socket.socketpair`, `urllib.request.urlopen` **et** remplace `dofus_stuff.cli.main` / `dofus_stuff.web.__main__.main` par un piège qui lève |
| `python -c "<empreinte .data/dofus.sqlite3>"` avant / après **toutes** les mesures | **identique** : `24989696:1788730056843137500:e3793d64cb7939ad1a51837b075b6b95e03d64c878fcb9cc07f86c00bb8fef7b` | 3 fois : avant, après la suite, après le greffon + les 4 batteries de mutation |

Compteur par module (mesuré, `pytest -q <fichier>`) — **219** au total :

| Module | Tests | Module | Tests |
|---|---:|---|---:|
| `tests/test_docs_base_locale.py` | 14 | `tests/test_optimize.py` | 16 |
| `tests/test_docs_cli.py` | 11 | `tests/test_profile_input.py` | 9 |
| `tests/test_docs_code_anchor.py` | 8 | `tests/test_recommend.py` | 31 |
| `tests/test_docs_parcours.py` | 18 | `tests/test_screens.py` | 10 |
| `tests/test_docs_structure.py` | 14 | `tests/test_solver_spec.py` | 10 |
| `tests/test_docs_wizard.py` | 18 | `tests/test_web.py` | 60 |

Les **6** modules de documentation portent **83** tests ; la phase 6 en ajoute (2 pages + 2 contrôleurs +
la preuve de mutation), donc **le compteur final sera supérieur à 219** et ne peut pas être annoncé — D-98
exige de le **relever**, jamais de le prévoir.

**E.2 — Aucune connexion réseau, `main()` jamais exécuté.** Le greffon mesuré est reproductible en une
trentaine de lignes (voir E.1) et sa vertu est d'être **actif**, pas déclaratif : tout appel réseau ou tout
appel de `main()` **lève**. Limites à déclarer : (a) le piège porte sur les points d'entrée Python
(`socket`, `urllib.request`), pas sur les appels système directs d'une extension compilée ; (b) il est
posé **dans le processus de test**, ce n'est pas une sandbox OS ; (c) il ne prouve rien d'un `main()`
exécuté par un **autre** processus (aucun n'est lancé).

**E.3 — Périmètre `git status` : le critère est faux à la lettre, et voici le vrai.** Mesuré **avant**
toute action de cette phase :

```
 M .gitignore                 # ajout de « .gsd-auto/ » (outillage) — antérieur, hors livrable
 M .planning/config.json      # ajout de « "_auto_chain_active": false » (outillage) — antérieur
?? .doc-agent/  ?? .gsd-tmp/  ?? .gsd/  ?? .planning/state.json
?? doc-agent.toml  ?? gsd-auto-rules.toml  ?? gsd-auto.toml
```

Fichiers de `.planning/` **suivis par git** (`git ls-files .planning`) : `PROJECT.md`, `REQUIREMENTS.md`,
`ROADMAP.md`, `STATE.md`, `WINDOWS.md`, `config.json`, et **tout** `phases/**`. La phase 6 fera donc
apparaître comme modifiés, **en plus** de `docs/` et `tests/` :

- `.planning/ROADMAP.md`, `.planning/STATE.md`, `.planning/REQUIREMENTS.md` (clôture de phase et de jalon) ;
- `.planning/phases/06-…/*` (plans, résumés, vérification) ;
- et les deux fichiers **déjà** modifiés avant la phase (`.gitignore`, `.planning/config.json`).

**Formulation honnête de l'audit :** « le périmètre **livrable** ne montre que `docs/`, `tests/` (et
`README.md`/`GUIDE_WIZARD.md` **si et seulement si** un contrôle prouve une incohérence, D-99) ; les
artefacts de pilotage `.planning/**` et d'outillage (`.gitignore`, `.planning/config.json`,
`gsd-auto*.toml`, `.gsd-tmp/`, `.gsd/`, `.doc-agent/`, `doc-agent.toml`) apparaissent en plus et ne sont
pas des livrables ». Mesuré : `dofus_stuff/**` doit rester **absent** de `git status` (vérifiable par
`git status --porcelain -- dofus_stuff`, vide, comme en phase 5).

**E.4 — Empreinte `.data/` : la mesure est possible sans ouvrir SQLite.** Le contrôle lit les **octets**
(`Path.read_bytes()`), calcule `hashlib.sha256` et relève `st_size`/`st_mtime_ns` — jamais
`sqlite3.connect` sur `.data/dofus.sqlite3` (D-104). Patron existant **triple** :
`tests/test_docs_parcours.py:2557`, `tests/test_docs_wizard.py:2289`, `tests/test_docs_base_locale.py:2284`
(la même fonction recopiée **assumée**, jamais factorisée — Pitfall 10 de la recherche 05). Le `skip`
conditionnel porte `MOTIF_BASE_ABSENTE` (`tests/test_docs_base_locale.py:301`).

### F. Les deux points hérités de la phase 5

**F.1 — `db clear` dans `README.md` (D-100).** Bloc mesuré, verbatim (`README.md:77-81`) :

````
```bash
python fetcher.py db status
python fetcher.py db sync            # forcer une sync complète
python fetcher.py db clear           # vider la base
```
````

Faits mesurés, sans décision :

| Fait | Mesure |
|---|---|
| Contexte | `README.md:75` titre `#### Base locale`, sous la section `### Usage CLI` ; aucune phrase d'avertissement dans le bloc ni autour |
| Balise du bloc | ` ```bash ` — or `lignes_exemple` ne lit que les blocs tagués ` ```console ` (`tests/conftest.py:151` `BALISE_EXEMPLE = "console"`) : même si une garde lisait le README, la règle « jamais dans un exemple » ne l'atteindrait pas sans élargir la balise |
| Gardes qui couvrent `db clear` | Trois, chacune **liée à une page** : `tests/test_docs_structure.py:275-331` (installation.md), `tests/test_docs_cli.py:928-988` (cli.md, `PAGE = "cli.md"`), `tests/test_docs_base_locale.py:1721-1884` (base-locale.md) |
| Garde qui lit le README | **Une seule** : `test_renvois_du_readme_resolus` (`tests/test_docs_base_locale.py:1964-2032`) — elle vérifie que les **liens** résolvent, et sa docstring déclare que « le bloc de commandes du `README.md` est **hors du mandat** de cette phase (D-87) ». **Aucune garde ne voit donc le `db clear` du README.** |
| Ce que le README contredit | `docs/cli.md:174-178` et `docs/base-locale.md:129` déclarent la commande destructrice **et** l'écartent de tout parcours recommandé (D-80). Le README, lui, la présente en troisième ligne d'un bloc d'usage, sans marque |
| Coût des deux options de D-100 | **Option A — la couvrir par un contrôle :** il faut (1) une garde qui lit `README.md` et y cherche les jetons destructeurs `\bdb\s+clear\b` (motif existant `COMMANDE_DESTRUCTRICE`, `tests/test_docs_structure.py:20`) **hors de tout bloc de commandes**, ou (2) une modification du README (marquer la ligne comme destructrice, ou la retirer) — or D-99 n'autorise à toucher le README **que si un contrôle prouve l'incohérence**, ce qui serait alors le cas. Coût : un fichier de plus modifié au périmètre livrable (README.md), une garde de plus, et l'élargissement du motif prend le risque de mordre sur `docs/cli.md` (qui, lui, **doit** citer la commande **hors** exemple : la garde devrait donc être portée par le README seulement). **Option B — la déclarer comme limite de périmètre :** aucun fichier modifié, mais une **incohérence livrée** (une commande destructrice présentée comme une étape dans le point d'entrée du lecteur) et une phrase de limite à écrire, cohérente avec D-80 (« jamais dans aucun parcours recommandé ») — c'est-à-dire une **dérogation explicite** à une décision verrouillée. |
| Ce qui départage, factuellement | D-80/D-90 sont verrouillées et disent « aucune commande destructrice présentée comme une étape » ; le README est le **premier** fichier que lit un lecteur (`.claude/CLAUDE.md`, section Documentation utilisateur). Mais D-99 limite la modification du README à ce qu'un contrôle prouve, et D-87 (phase 5) a explicitement laissé le bloc du README hors mandat. **Je ne tranche pas** : le planificateur écrit l'option retenue, son coût et sa raison. |

**F.2 — La dérive de `.planning/WINDOWS.md` (D-101).** État réel mesuré du fichier :

| Élément | Valeur mesurée |
|---|---|
| Front matter | `schema_version: 1`, `open_count: 6`, `waived_count: 0`, `fixed_count: 0`, `total_count: 6`, `last_updated: 2026-09-11T13:37:27.213Z` (`:1-8`) |
| Table rendue | **6** lignes (`:18-23`), toutes `status: open` |
| Ligne `id=5` (celle de D-101) | `.planning/WINDOWS.md:22` — `phase 3`, `kind deviation`, fichier `.planning/ROADMAP.md`, ligne 1, description ECR-1 : la table « libellé tronqué → nom complet » n'a pas d'objet dans ce flux (aucune ligne rendue ne porte de points de suspension) ; décision enregistrée dans `.planning/ROADMAP.md` et `03-02-PLAN.md` |
| Ligne `id=6` | `:23` — même famille, ECR-2 : « Méthode / Score / Indice de recherche sur la dernière page » est faux sur la fixture déterministe |
| Le libellé `windows_ledger_table_drift` | **Introuvable dans `.planning/WINDOWS.md`** : c'est un verdict **d'outil**, consigné dans deux artefacts de phase — `04-03-SUMMARY.md:220` et `05-03-SUMMARY.md:238` — qui rapportent tous deux que `gsd-tools windows append` **refuse d'écrire** parce que la table rendue diverge, sur la ligne `id=5`, de l'entrée JSON (source de vérité) |
| Effet de la dérive | `windows status` rend `open_count: 6`. Le blocage de `/gsd-ship` dépend de `workflow.windows_enforce`, **absent** de `.planning/config.json` (mesuré) : la dérive est donc réelle mais **non bloquante** pour ce jalon |
| Correction attendue | **Aucune** : D-101 la déclare hors périmètre, non corrigée à la main. Ce que la phase doit faire, c'est **la nommer à l'identique** dans son rapport (jamais la présenter comme résolue, et surtout ne pas tenter un `windows fixed 5`, qui réécrirait le registre) |

---

## Standard Stack

Cette phase est **documentaire et interne** : elle n'ajoute **aucune** dépendance (contrainte de projet
`.claude/CLAUDE.md:36` et D-105). La « stack » est donc celle qui existe déjà et qu'il ne faut pas
changer.

### Core

| Élément | Version | Usage | Pourquoi celui-là |
|---|---|---|---|
| Markdown nu (CommonMark + GFM) | format, pas un paquet | Les 2 pages neuves | Les 6 pages livrées sont du Markdown nu : continuité de format, lisible sur disque et rendu par GitHub, aucun build |
| `pytest` (dans `.venv`) | **9.1.1** mesuré (`>=8.0` déclaré, `pyproject.toml:19`) | Tous les contrôles | Seul outillage de vérification autorisé ; déjà configuré (`pyproject.toml:37-44`) |
| Python | **3.14.7** pour `.venv/Scripts/python.exe` (mesuré) ; `requires-python = ">=3.11"` (`pyproject.toml:10`) | Écrire les contrôleurs | D-15 : l'interpréteur ambiant n'a pas `pytest` |
| stdlib `pathlib`, `re`, `unicodedata`, `hashlib`, `shutil`, `contextlib` | 3.11+ | Lecture de pages, ancrage, copie de `docs/`, capture de `stdout` | Aucun paquet tiers n'est nécessaire à des contrôles de documentation |

### Supporting

| Élément | Version | Usage | Quand l'utiliser |
|---|---|---|---|
| `flask.Flask.test_client` | `flask>=3.0` (`pyproject.toml:12`) | Rendu des écrans en processus (messages des familles 1, 2, 3, 5) | Fixture `client` de `tests/conftest.py:114-116` — jamais un serveur |
| `dofus_stuff.cli._print_db_status` | produit | Sortie CLI de l'état de la base, sur base `tmp_path` | Famille « base absente ou vide », patron `tests/test_docs_base_locale.py:1235` |
| `ast` | stdlib | Lire les littéraux de `cli.py::main` **sans l'exécuter** | Toute citation d'un message CLI que seule `main()` imprime |
| `shutil.copytree` | stdlib | Copie de `docs/` sous `tmp_path` pour la preuve de mutation | `tests/test_docs_structure.py:536` |

### Alternatives Considered

| Au lieu de | On pourrait | Arbitrage |
|---|---|---|
| Contrôleurs pytest maison | MkDocs/Sphinx/mdBook | **Non** : publication distante interdite, dépendance ajoutée, `.claude/CLAUDE.md` les exclut explicitement |
| Ancrage par comparaison normalisée (D-11) | Comparaison octet à octet d'un rendu | **Non** : fragile aux accents et aux espaces ; l'objet est la doc, pas le rendu |
| Mesure d'empreinte `.data/` par lecture d'octets | `sqlite3` en lecture seule (`?mode=ro`) | **Non** : D-104 interdit d'ouvrir la base dans un contrôle d'intégrité |
| `subprocess` pour faire échouer la suite dans la copie | Greffon qui refuse le réseau et `main()` | **Non** à ce stade : `subprocess` est refusé par la garde de clôture des quatre modules d'ancrage (§ D.3) ; la batterie rejouable hors `tests/` couvre le besoin |

**Installation :**

```bash
# Rien à installer. Aucune dépendance ajoutée (D-105).
./.venv/Scripts/python.exe -m pytest -q
```

**Version verification :** aucune version tierce n'est proposée par cette recherche — les seules versions
citées sont **mesurées** localement (`pytest 9.1.1`, Python 3.14.7 dans le `.venv`, `flask` importé avec
succès) et **déclarées** dans `pyproject.toml:12-20`. Aucune `pip index versions` n'est donc à lancer :
l'écosystème externe n'entre pas dans cette phase.

## Package Legitimacy Audit

**Aucun paquet externe n'est installé par cette phase.** Le gate de légitimité est donc **sans objet** :
aucun `npm install`, aucun `pip install`, aucune dépendance de test ajoutée (D-105, contrainte
`.claude/CLAUDE.md:36`). La porte est vérifiable par un contrôle négatif simple : `pyproject.toml` doit
rester **inchangé** (`git status --porcelain -- pyproject.toml` vide) et `uv.lock` aussi.

*Si un plan proposait d'ajouter un paquet — p. ex. un vérificateur de liens Markdown — il violerait une
contrainte de projet et devrait être refusé, pas audité.*

## Architecture Patterns

### System Architecture Diagram

```
                 ┌───────────────────────────── lecture seule, jamais d'écriture ─────────────────────────────┐
                 │                                                                                         │
  code produit   │  dofus_stuff/cli.py            dofus_stuff/web/routes.py          terminal.js              │
  (référence)    │   littéraux de main()           _screen() compose le statut        focus / touches          │
                 │   _print_db_status()            optimize_wizard.py (ValueError)                             │
                 └───────────┬──────────────────────────┬───────────────────────────────┬────────────────────┘
                             │ ast (littéraux)          │ client de test Flask          │ lecture du fichier
                             │ capture stdout (tmp)     │ (tmp_path, en processus)      │ + rendu des écrans
                             ▼                          ▼                               ▼
                 ┌─────────────────────────────────────────────────────────────────────────────────────┐
                 │  docs/depannage.md  ──  rubriques indexées par message réel   (06-01)               │
                 │  docs/glossaire.md  ──  entrées triées, chacune adossée à un emploi (06-02)        │
                 │  docs/sommaire.md   ──  index + parcours conseillé final      (06-02)               │
                 └───────────┬─────────────────────────────────────────────────────────────────────────┘
                             │ page → message/rubrique, page → terme
                             ▼
                 ┌─────────────────────────────────────────────────────────────────────────────────────┐
                 │  tests/  (harnais, 06-03 / 06-04)                                                   │
                 │   · contrôle message → rubrique            (nouveau, 06-01)                         │
                 │   · contrôle des entrées du glossaire + ordre (nouveau, 06-02)                      │
                 │   · liste épinglée des 8 + ensemble exact des fichiers (nouveau, 06-03)             │
                 │   · contrôle du parcours conseillé          (nouveau, 06-03)                        │
                 │   · preuve de mutation en processus         (nouveau, 06-04)  ── copie tmp_path ──┐ │
                 │   · empreinte .data/ (octets) autour de la suite            (06-04)              │ │
                 └─────────────────────────────────────────────────────────────────────────────────┼─┘
                                                                                                   │
       gardes existantes (NE PAS dupliquer) : problemes_liens / problemes_index / problemes_h1 ◄──┘
       tests/test_docs_structure.py · test_docs_code_anchor.py (libellés produits par le code)
```

Lecture du flux principal : *un message imprimé par le produit* → *est cité verbatim dans une rubrique de
`depannage.md`* → *est adossé à un contrôle qui le relit dans le code* → *une dérive injectée dans une
copie de `docs/` fait échouer le contrôle en nommant la dérive*.

### Recommended Project Structure

```
docs/                      # 8 fichiers épinglés, à l'identique des 6 livrés (CRLF, UTF-8 sans BOM)
├── sommaire.md            # index + parcours conseillé final (06-02)
├── installation.md        # livré
├── parcours-simplifie.md  # livré
├── wizard-avance.md       # livré
├── cli.md                 # livré
├── base-locale.md         # livré
├── depannage.md           # NOUVEAU (06-01) — rubriques indexées par message réel
└── glossaire.md           # NOUVEAU (06-02) — entrées triées
tests/
├── conftest.py            # fixtures partagées : à RÉUTILISER, jamais recopier (D-12)
├── test_docs_structure.py # gardes d'index, H1, retour, encodage + mutation de la phase 1
├── test_docs_code_anchor.py, test_docs_cli.py, test_docs_parcours.py, test_docs_wizard.py,
│   test_docs_base_locale.py  # ancrages par page (à ne pas affaiblir)
├── test_docs_depannage.py # NOUVEAU (06-01) — message → rubrique  [nom libre : voir § Wave 0]
├── test_docs_glossaire.py # NOUVEAU (06-02) — entrées + ordre    [nom libre]
└── test_docs_completude.py# NOUVEAU (06-03) — liste épinglée + ensemble exact + parcours
```

### Pattern 1: Une valeur citée est lue dans le code, jamais écrite de mémoire (D-19)

**Quand l'utiliser :** chaque message, chaque libellé, chaque terme des deux pages neuves.

```python
# Source : patron de tests/test_docs_base_locale.py:1235 (_sortie_db_status) et :531 (_litteraux_du_module)
# Le message CLI se mesure sur la FONCTION DE PRODUCTION, jamais sur main() :
buf = io.StringIO()
with redirect_stdout(buf):
    _print_db_status(db)            # db construite sur tmp_path, jamais .data/
sortie = buf.getvalue()
assert "Version jeu : (aucune)" in sortie   # mesuré cette session sur un dossier vide

# Le message que seule main() imprime se lit dans l'ARBRE, par ast, jamais par exécution :
arbre = ast.parse((RACINE_DEPOT / "dofus_stuff/cli.py").read_text(encoding="utf-8"))
litteraux = _litteraux_de_fonction(arbre, "main")
assert "Calcul en cours (CP-SAT)…" in litteraux
```

### Pattern 2: Les messages de refus du web se lisent dans la LIGNE DE STATUT, avec `follow_redirects`

**Quand l'utiliser :** toute rubrique « saisie invalide » de la page de dépannage.

```python
# Source : tests/test_docs_parcours.py:316-320 (_statut) et la composition de routes.py:141-150
reponse = client.post("/search", data={"query": ""}, follow_redirects=True)  # 302 -> SRC-01
assert statut(reponse).startswith("SAISIE REQUISE")     # mesuré : « SAISIE REQUISE — ENTREE=VALIDER »
# Le corps rendu, jamais la réponse entière : data-stuff-payload échappe les accents (leçon de la phase 3).
```

### Pattern 3: Constats accumulés, une seule assertion (convention des phases 2 à 5)

**Quand l'utiliser :** tout contrôle neuf de cette phase. Les motifs sont des **constantes de module**,
incluses dans le texte du constat, et **jamais** écrites en clair dans la ligne d'assertion — pytest
reproduit cette ligne dans sa sortie, et un motif littéral y ferait croire à une morsure (règle du plan
03-03, rappelée par `tests/test_docs_parcours.py:2851-2854`).

```python
MOTIF_PAGE_MANQUANTE = "page epinglee absente de docs"
constats: list[str] = []
for nom in PAGES_EPINGLEES:
    if not (docs_dir / nom).is_file():
        constats.append(f"{MOTIF_PAGE_MANQUANTE} : {nom} ... ; attendu ... (D-95)")
assert not constats, f"{PAGES_EPINGLEES_REF} : " + " ; ".join(constats) + " ; attendu ..."
```

### Pattern 4: Copie verte, mutation sur la copie, motif cherché dans la sortie

**Quand l'utiliser :** la preuve du critère 4 (06-04).

```python
# Source : tests/test_docs_structure.py:533-603 + § D.1 de cette recherche
copie = tmp_path / "docs"
shutil.copytree(docs_dir, copie)
sain = problemes_liens(docs_dir) + problemes_index(docs_dir) + problemes_h1(docs_dir, normalize)
assert sain == [], "docs/ livre deja en derive avant toute mutation (D-97)\n" + "\n".join(sain)
page = copie / "cli.md"                    # dérive (i) : page manquante
page.unlink()
constats = problemes_index(copie)
assert any(MOTIF_PAGE_MANQUANTE in c for c in constats), "\n".join(constats)
```

### Pattern 5: Muter par octets, jamais par `sed -i` (piège CR mesuré)

```python
# Source : § D.4 — sed (GNU sed) 4.9 sous Git-for-Windows retire les \r (mesure cette session).
p = copie / "docs" / "installation.md"
s = p.read_bytes().decode("utf-8")
p.write_bytes(s.replace("# Installation\r\n", "# Installation provisoire\r\n", 1).encode("utf-8"))
```

### Anti-Patterns to Avoid

- **Citer un message « plausible »** (une variante accentée, un mot changé) : c'est le défaut payé deux
  fois par ce jalon. Le message vient d'une lecture `fichier:ligne` faite **pendant** la rédaction.
- **Écrire une rubrique de dépannage par symptôme** : le critère 1 indexe par **message réel** (D-93) ;
  un symptôme sans message produit ne crée pas de rubrique (D-76).
- **Redéfinir dans le glossaire ce qu'une page définit déjà** : `palier`, `exo`, `heuristique`, `score`,
  `ligne de statut` sont **déjà** définis (`docs/parcours-simplifie.md:198-209`, `:226-228`, `:238`) —
  y renvoyer, sinon on crée une seconde source (D-17).
- **Dupliquer les gardes d'index/H1** dans le nouveau contrôleur de complétude : elles tiennent déjà
  l'égalité d'ensembles et le H1 (`tests/test_docs_structure.py:92-119`, `:337-380`).
- **Injecter une mutation par `sed -i`** sur une page CRLF, ou **en insérant un import** dans un module de
  test (§ D.4, § D.5).
- **Faire du `subprocess`** dans un module d'ancrage sans le déclarer : la garde de clôture le refuse.
- **Annoncer un compteur de tests** ou une durée : D-98 exige la valeur **relevée**.
- **Annoncer `git status` « seulement docs/, tests/ »** : mesuré faux (§ E.3).

## Don't Hand-Roll

| Problème | Ne pas construire | Utiliser à la place | Pourquoi |
|---|---|---|---|
| Résoudre un lien interne de `docs/` | Un nouveau résolveur dans le module neuf | `problemes_liens` (`tests/test_docs_structure.py:39-89`) | Il refuse déjà `#`, les chemins absolus, les antislashs, `file://` et la sortie de la racine |
| Comparer libellé d'index ↔ H1 | Une seconde comparaison d'égalité | `problemes_h1` (`tests/test_docs_structure.py:337-380`) | Normalisation D-11, unicité du H1, message qui cite la page et le libellé |
| Vérifier l'égalité index ↔ fichiers | Une seconde énumération de `docs/` | `problemes_index` (`tests/test_docs_structure.py:92-119`) | Le sens « page en trop » est **déjà** couvert |
| Normaliser un libellé (accents, casse, entités, CRLF) | `unicodedata` réécrit dans le module | Fixture `normalize` (`tests/conftest.py:119-136`) | D-12 : un helper recopié finit par diverger (leçon WR-04) |
| Extraire les blocs de code / les lignes d'exemple | Un troisième scanner | Fixtures `lignes_de_code`, `lignes_exemple` (`tests/conftest.py:231-246`) | Le scanner unique garde la balise (`BALISE_EXEMPLE = "console"`) |
| Ouvrir une page de `docs/` en UTF-8 strict | Un `read_text` local | `_lire_page` + fixtures `docs_dir`/`section`/`sections` | Gère le `UnicodeDecodeError` en constat (D-13) |
| Mesurer l'empreinte de `.data/` | Une quatrième copie « améliorée » | Le patron des trois copies existantes (`test_docs_parcours.py:2557`, `test_docs_wizard.py:2289`, `test_docs_base_locale.py:2284`) | La convention est de **recopier verbatim** (copie assumée), jamais de factoriser (Pitfall 10 de la recherche 05) |
| Rendre un écran web en test | Lancer un serveur ou un navigateur | Client de test Flask (`tests/conftest.py:114`) + le greffon de refus réseau (§ E.2) | Aucun réseau, aucun processus |

**Key insight :** dans ce dépôt, la duplication qui coûte est celle **non assumée** : trois copies de
`_empreinte` sont documentées et vérifiées, mais un helper de normalisation recopié divergerait
silencieusement. La règle est donc : *fixtures partagées pour tout ce qui vit dans `conftest.py`,
recopie verbatim documentée pour le reste*.

## Feasibility verdict : le critère 4 (la preuve de mutation)

**Verdict : FAISABLE, avec un périmètre honnête à écrire.** Le critère n'est pas à construire de zéro :
trois de ses cinq composantes sont **déjà prouvées** par des gardes existantes, mesurées cette session.

| Composante du critère 4 | Morsure prouvée ? | Mécanisme recommandé | Limite honnête à déclarer |
|---|---|---|---|
| **Complétude** (page manquante + ensemble exact) | **Partiellement** : page manquante → `problemes_index` + `problemes_liens` (**mesuré : 14 failed**) ; page en trop → `problemes_index` + `problemes_h1` (**mesuré**) | In-process : `shutil.copytree` de `docs/`, `page.unlink()` sur la copie, appel de `problemes_index`/`problemes_liens`, constat portant un motif dédié (nouveau : la **liste épinglée**, que seule une constante neuve porte) | La **liste épinglée** ne peut pas être prouvée par les gardes existantes (elles comparent l'index au disque, pas à une liste) : sa morsure doit être écrite dans le module neuf — injecter une 9ᵉ page **listée à l'index** dans la copie et exiger le constat de liste épinglée. Vérifier que ce constat est **distinct** de `problemes_index`, sinon la morsure ne prouve rien de neuf |
| **Ancrage de libellé** | **Oui** : H1 divergent → `problemes_h1` (**mesuré**) ; nom cité non produit (`Fermer`) → `test_libelles_cites_sont_produits_par_le_code` (**mesuré**) | In-process : mutation CR-préservante par octets sur la copie, puis appeler **la fonction de comparaison du module d'ancrage** concerné (import du module de test voisin, patron déjà employé entre modules de `tests/`) | **Limite mesurée** : la comparaison de libellé est une **appartenance de sous-chaîne** (`tests/test_docs_code_anchor.py:243`) — `Quitter tout` **passe** (mesuré : `216 passed`) ; la morsure doit donc utiliser un nom qui ne contient pas le libellé réel. Les gardes non paramétrables (racine figée, `tests/test_docs_parcours.py:2937`) ne peuvent pas être rejouées sur une copie : la preuve par le **rendu** les couvre autrement |
| **Renvois obsolètes** | **Oui, deux détecteurs** : `docs/**` → `problemes_liens` ; `GUIDE_WIZARD.md` → `MOTIF_LIEN_MORT` (`tests/test_docs_parcours.py:2879`, `:2931-2950`) ; `README.md` → `renvois_morts` (`tests/test_docs_base_locale.py:1935-1961`) | In-process, sur la copie : remplacer une cible de lien par `page-absente.md` et exiger le constat nommant la cible | Pour le README et `GUIDE_WIZARD.md`, les gardes résolvent depuis la **racine du dépôt** : la copie doit inclure ces fichiers à la racine de la copie (patron du § D.1) |

**Les deux limites structurelles du critère, mesurées :**

1. **Une preuve « en processus » ne fait pas échouer `pytest`** : elle fait lever l'appel de garde. La
   phrase du critère (« le harnais échoue réellement ») se lit alors à deux niveaux — la garde lève (test
   pytest) et la suite échoue (batterie rejouable). Les deux ont été employées par les phases 3 à 5 ;
   la batterie fournit la sortie brute à coller dans le `SUMMARY.md`.
2. **`subprocess` est interdit par la convention** (§ D.3) : exécuter `pytest` dans la copie depuis un
   module de `tests/` obligerait à un écart écrit et justifié. C'est possible, mais c'est un choix à
   **nommer dans le plan**, pas un détail d'implémentation.

---

## D-17 — Une seule source par énoncé : les doublons déjà présents

C'est le risque numéro un de cette phase : les deux pages neuves décrivent des sujets que **six pages
livrées traitent déjà**. Ce tableau est **mesuré** ; le planificateur doit décider, pour chaque ligne, si
la page neuve **renvoie** (lien) ou si elle est la **première** à dire la chose.

| Énoncé que la page neuve voudrait porter | Où il est déjà écrit (mesuré) | Geste attendu |
|---|---|---|
| `Base locale vide et --offline : impossible de synchroniser` (+ le préfixe `Erreur : `) | `docs/installation.md:112` et l'explication `:115` ; `docs/cli.md:35-41` pour `--offline incompatible avec db sync` | **Renvoi** — c'est déjà la rubrique « base absente » de `installation.md:99-117` |
| `fetcher.py: error: unrecognized arguments: --offline` (options globales après la sous-commande) | `docs/installation.md:119-125` ; `docs/cli.md:27-33` | **Renvoi** |
| Les trois messages de refus du parcours simplifié (`Saisissez le nom ou le numéro de votre classe.`, `Exemple : feu, terre air, ou multi.`, `Saisissez un niveau entre 1 et 200.`) | `docs/parcours-simplifie.md:46-48` (table des saisies et de leur refus), `:50`, `:92`, `:130` ; `docs/wizard-avance.md:94` (`SAISIE INVALIDE`) | **Renvoi** vers la page de la surface concernée ; la rubrique de dépannage **indexe** le message, elle ne réexplique pas la saisie |
| `SAISIE INVALIDE`, `OPTION INVALIDE`, `NUMERO INVALIDE`, `SAISIR LE NUMERO DE LA LIGNE`, `SYNTAXE : +ID \| -ID \| !ID \| CLEAR` | `docs/wizard-avance.md:94`, `:122`, `:137`, `:163` | **Renvoi** |
| `PAGE n/total`, `ENTREE=VALIDER`, `F7=Page prec`, `F8=Page suiv` | `docs/parcours-simplifie.md:140` et `:176` ; `docs/installation.md:62-63` ; `docs/wizard-avance.md:173`, `:181` | **Renvoi** — le mécanisme de pagination a **déjà** sa source |
| `ENTREE=CALCULER` | `docs/parcours-simplifie.md:130` | **Renvoi** |
| `GO = LANCER`, `RESET = REINITIALISER`, `1-8 = RETOUR ECRAN` | `docs/wizard-avance.md:189`, `:212` | **Renvoi** |
| `DUREE (S)` / budget de temps du calcul | `docs/wizard-avance.md:107`, `:124` | **Renvoi** |
| `db clear` / `cache clear` destructrices | `docs/cli.md:174-178`, `:192` ; `docs/base-locale.md:129` | **Renvoi** — et c'est **déjà** gardé (`tests/test_docs_cli.py:928`, `tests/test_docs_base_locale.py:1721`) |
| `PURGE OUI` destructrice (sauvegardes du navigateur) | `docs/base-locale.md:131` ; `docs/parcours-simplifie.md:174`, `:176` | **Renvoi** |
| `Version jeu : (aucune)`, `Dernier check : (aucun)`, `Entrées : 0` et leurs équivalents web | `docs/base-locale.md:77`, `:95`, `:105` | **Renvoi** |
| Le pilotage clavier (champ de saisie, refocalisation au clic, barre dynamique) | `docs/installation.md:53-71` | **Renvoi** — c'est le seul endroit qui décrit le clavier ; la rubrique « clavier inactif » y renvoie |
| Le sens de `palier`, `exo`, `heuristique`/`borne_heuristique`, `score`/`indice de recherche` | `docs/parcours-simplifie.md:198-209`, `:226-228`, `:238` | **Renvoi** depuis le glossaire |
| `stuff`, `slot`, `poids`, `cible`, `jet`, `ID Ankama`, `panoplie`, `prysmaradite` | voir § B (chaque terme a sa ligne) | Définir **seulement** ce qui n'est défini nulle part (`stuff`) ; renvoyer pour le reste |

**Messages que la page de dépannage sera la PREMIÈRE à citer** (0 occurrence dans `docs/`, mesuré) :
`SAISIE REQUISE`, `LIMITE INVALIDE`, `AUCUN RESULTAT.`, `ID INVALIDE — ENTIER ATTENDU`,
`OPTION INVALIDE — SAISIR 1 A N`, `AUCUNE VERSION EN BASE` / `ERREUR : AUCUNE VERSION EN BASE.`,
`Calcul en cours (CP-SAT)…`, `Page suivante disponible : `, `Aucun résultat.`, `Aucun objet sur cette
page.`, `ÉQUIPEMENT INTROUVABLE : #N`, `CALCUL TERMINE`, `SYNCHRONISATION TERMINEE`, `CLEAR ANNULE`,
`SYNC ANNULEE`. C'est là que la page apporte de la valeur — et là que le risque d'invention est maximal :
chaque ligne doit être adossée à sa provenance `fichier:ligne` **pendant** la rédaction.

## Common Pitfalls

### Pitfall 1: « Clavier inactif » n'a pas de message — une rubrique qui en invente un est fausse
**Ce qui se passe :** le rédacteur écrit « le message *CLAVIER INACTIF* » ou « *SAISIE IGNORÉE* » parce que
la famille est nommée dans le critère. Mesuré : **aucune** chaîne de ce genre n'existe dans le produit.
**Pourquoi :** le critère nomme cinq **familles** de symptômes, pas cinq messages ; quatre familles ont un
message, la cinquième un **mécanisme** (JS + `autofocus`).
**Comment l'éviter :** adosser la rubrique aux faits de A.4 (`terminal.js:80-88`, `:595`,
`screen.html:61`, écrans sans `input_label`) et le déclarer en limite.
**Signe précoce :** un contrôle qui chercherait le message dans le code ne trouverait rien et le test
deviendrait « vert par absence d'objet ».

### Pitfall 2: un message « à peu près juste » casse toute la valeur de la page
**Ce qui se passe :** la page cite `Erreur : Aucune version en base` (majuscule) alors que le code imprime
`Erreur : aucune version en base` (`cli.py:372`) ; ou la page cite `AUCUNE VERSION EN BASE.` sans le
`ERREUR : ` du corps (`routes.py:647`).
**Pourquoi :** les deux surfaces ne portent pas les mêmes chaînes (accent, casse), et la lecture de mémoire
lisse l'écart.
**Comment l'éviter :** chaque message est **recopié depuis une mesure** ; les tests comparent en
**normalisation D-11** seulement là où la phase 5 l'a fait (les messages de refus du wizard sont comparés
via `normalize`), et l'ancrage **strict** porte sur la comparaison au rendu/code.

### Pitfall 3: la pagination a deux formes, et une assertion mal placée est rouge sur un produit correct
**Ce qui se passe :** exiger `PAGE n/n` dans la ligne de **statut** d'un écran non paginé. Mesuré :
`routes.py:144-145` n'ajoute le motif que si `total > 1` ; la ligne de **corps** le porte toujours
(`routes.py:543`).
**Pourquoi :** c'est exactement le motif d'ECR-2 (`.planning/WINDOWS.md`, ligne `id=6`) — une assertion
positionnelle fausse.
**Comment l'éviter :** mesurer la pagination sur `GET /list?page=1&size=1` (fixture à 3 équipements,
`total = 3`), et dire dans la page que le motif apparaît **quand l'écran est paginé**.

### Pitfall 4: le parcours conseillé est du texte simple — aucune garde ne le voit
**Ce qui se passe :** le plan écrit un « parcours conseillé final » sans contrôle, et une dérive
ultérieure (page renommée) passe silencieusement. Mesuré : `grep "Parcours" tests/*.py` → 0 occurrence.
**Comment l'éviter :** rendre le parcours **vérifiable** — au minimum que chaque page livrée y figure et
qu'aucun nom de page inexistante n'y apparaisse (les entrées peuvent rester en texte si le contrôle
compare des libellés normalisés aux libellés d'index).

### Pitfall 5: la liste épinglée peut être « prouvée » par une garde qui ne la regarde pas
**Ce qui se passe :** le contrôle neuf appelle `problemes_index` et se déclare prouvé ; il l'est **déjà**
par la phase 1 et n'ajoute rien.
**Comment l'éviter :** la morsure doit injecter une dérive que **seule** la constante neuve voit — une page
**présente et listée à l'index** mais absente de la liste épinglée (ou l'inverse), et le constat doit porter
un motif **distinct** de ceux de `problemes_index`.

### Pitfall 6: `sed -i` détruit les CR de la copie et confond la morsure
Mesuré cette session (§ D.4). **Comment l'éviter :** muter par octets avec des ancres `\r\n`.

### Pitfall 7: injecter un import dans un module de test qui porte `from __future__ import annotations`
Mesuré en phase 5 (`.planning/phases/05-…/05-01-SUMMARY.md:179-184`) : le module meurt à la **collecte** et
la morsure rapporte « non détectée ». **Comment l'éviter :** le module de mutation ne porte **pas**
`from __future__ import annotations` s'il subit ce type de morsure, et aucune mutation n'insère d'import.

### Pitfall 8: `subprocess` dans un module d'ancrage → la garde de clôture rougit
`RACINES_INTERDITES` / `INTERDITS_EXECUTION` portent sur les **quatre** modules d'ancrage (§ D.3). Un
module neuf qui lancerait `pytest` dans la copie échouerait sur sa propre garde. **Comment l'éviter :**
choisir la voie in-process, ou écrire et justifier l'écart.

### Pitfall 9: le README présente une commande destructrice comme une étape, et rien ne le voit
Mesuré (§ F.1) : `README.md:80`, bloc `bash`, aucune garde. C'est le piège de fond de D-100 : la tentation
est de l'ignorer, la conséquence est une documentation qui contredit D-80.

### Pitfall 10: `test_mutation_detecte_les_trois_derives` dérive tout seul si les pages neuves changent
**Ce qui se passe :** ce test injecte une page dont le **nom est dérivé de l'arbre** (`_nom_page_injectee`,
`tests/test_docs_structure.py:507-522`) précisément pour qu'une page livrée par une phase ultérieure (le
glossaire !) ne le rende pas faussement rouge. **Conséquence :** il ne faut **pas** le « corriger » en
ajoutant `glossaire.md`/`depannage.md` à une liste de noms connus — il est déjà conçu pour.
**Signe précoce :** un plan qui propose de « mettre à jour » cette constante a mal lu le fichier.

### Pitfall 11: l'assertion CRLF n'est pas portable
`MOTIF_CRLF` (`tests/test_docs_base_locale.py:2157`) dépend de `core.autocrlf=true` (mesuré sur ce poste,
aucun `.gitattributes`). À déclarer comme limite (AR-5), pas à présenter comme un invariant universel.
NB : les gardes de structure ne vérifient **pas** le CRLF des pages neuves ; si le plan l'exige, il écrit
l'assertion et déclare la limite, comme la phase 5.

### Pitfall 12: annoncer un compteur, une durée ou un `git status` non mesurés
D-98 le dit : le rapport final cite ce qui a été **observé**. Mesuré aujourd'hui : `219 passed in 4.31s`,
empreinte `.data/` identique, et un périmètre `git status` qui **contient** `.planning/**` (§ E.3).

---

## Environment Availability

| Dépendance | Requise par | Disponible | Version / preuve | Repli si absente |
|---|---|---|---|---|
| `.venv/Scripts/python.exe` | tous les contrôles (D-15) | **Oui** | `Python 3.14.7`, exécuté cette session | Aucun : `.claude/CLAUDE.md` interdit d'en installer un autre ; l'interpréteur ambiant n'a pas `pytest` (mesuré en phase 1) |
| `pytest` | tous les contrôles | **Oui** | `9.1.1` (dans `.venv`), `219 passed` mesuré | Aucun |
| `flask` | fixtures web | **Oui** | import réussi, `flask>=3.0` (`pyproject.toml:12`) | Aucun : les fixtures `app`/`client` du `conftest` partagent la même dépendance |
| `ortools` | non requis par cette phase | présent (`pyproject.toml:17`) | jamais importé par les mesures de rendu de cette recherche | — |
| Git | audit de périmètre (06-04) | **Oui** | `git status --porcelain` mesuré ; `git ls-files --eol` mesuré | Aucun (le rapport est un livrable de la phase) |
| Éditeur / IDE | — | sans objet | — | — |
| Navigateur / DOM | exécution JS (`terminal.js`) | **Non — et non requis** | limite A2 assumée depuis la phase 5 | Lecture du fichier + rendu des écrans (A.4) |
| Réseau | interdiction (GARD-04) | **Non utilisé** | greffon qui refuse `socket`/`urlopen` mesuré vert | — |

**Aucune dépendance manquante** : cette phase n'a rien à installer (D-105).

## Validation Architecture

Le projet tourne en **validation Nyquist** (`workflow.nyquist_validation: true` dans
`.planning/config.json`) : chaque critère de succès doit devenir une **assertion automatisée**, et
`/gsd:plan-phase` refuse de créer `VALIDATION.md` si cette section manque.

### Test Framework

| Propriété | Valeur |
|---|---|
| Framework | `pytest` (seul outillage autorisé ; `pyproject.toml:19`, `:37-44`) |
| Interpréteur de référence | `.venv/Scripts/python.exe` (D-15) — **jamais** `python` nu |
| Commande rapide (un module) | `./.venv/Scripts/python.exe -m pytest tests/<module>.py -q` |
| Commande complète | `./.venv/Scripts/python.exe -m pytest -q` → mesuré **`219 passed in 4.31s`** |
| Commande réseau/`main()` interdits | suite + greffon qui refuse `socket.socket`, `socket.create_connection`, `socket.socketpair`, `urllib.request.urlopen`, et remplace `dofus_stuff.cli.main` / `dofus_stuff.web.__main__.main` → mesuré **`219 passed in 4.13s`** |
| Fixtures partagées à réutiliser (D-12) | `docs_dir`, `pages`, `section`, `sections`, `normalize`, `client`, `app`, `catalog`, `lignes_de_code`, `lignes_exemple` (`tests/conftest.py`) |
| Convention d'assertion | constats accumulés + **une** assertion finale (D-13) ; motifs en constantes de module, jamais dans la ligne d'assertion |
| Compteur attendu | **> 219** (3 modules neufs) ; la valeur exacte est **relevée** au moment de la vérification (D-98) |

### Sampling Rate (Nyquist)

| Niveau | Fréquence | Cible |
|---|---|---|
| Boucle par tâche (wave) | après chaque modification de page ou de test | `-m pytest tests/<module concerné>.py -q` — doit rester vert **avant** toute mutation |
| Après chaque plan | fin de chaque plan 06-01…06-04 | `-m pytest -q` complet (le compteur doit **croître**, jamais stagner) |
| Contre-mesure de non-régression | 06-04 | suite complète **dans une copie** (`mktemp -d`) avant mutation — mesuré **`216 passed, 3 skipped`** (les 3 `skip` sont les mesures d'empreinte `.data/`, absentes hors du dépôt) |
| Preuve de morsure | 06-04, par dérive | suite complète **dans la copie mutée** : la sortie doit porter `[0-9]+ (failed\|error)` **et** le motif nommé (`grep -F`) |
| Intégrité des données | 06-04, autour de la suite | empreinte `(taille, mtime_ns, sha256)` de `.data/dofus.sqlite3` — mesurée **identique** 3× cette session |

### Wave 0 Gaps (ce qui doit exister avant que les contrôleurs des vagues suivantes aient du sens)

| Manque | Pourquoi il est bloquant | Traitement recommandé |
|---|---|---|
| `docs/depannage.md` | Tout contrôle « message → rubrique » est vide sans elle | Plan 06-01, tâche de rédaction **puis** contrôle dans le même plan |
| `docs/glossaire.md` + son entrée d'index + le parcours final | Le contrôle d'entrées n'a pas d'objet ; le parcours reste faux sur disque | Plan 06-02 |
| **Nom des 3 modules de test neufs** | Convention à figer une fois : `tests/test_docs_depannage.py`, `tests/test_docs_glossaire.py`, `tests/test_docs_completude.py` (+ le module de mutation, p. ex. `tests/test_docs_mutation.py`) | Décision de planification (discretion) ; aucune collision mesurée avec l'existant |
| **Constante de liste épinglée** | Aucune garde existante ne la porte (§ C.3) | Plan 06-03 : constante de module + contrôle, motif distinct de `problemes_index` |
| **Contrôle du parcours conseillé** | 0 occurrence dans `tests/` (§ C.4) | Plan 06-03 |
| **Contrôle d'intégrité `.data/`** | Le patron existe (3 copies) mais n'appartient à aucun module neuf de cette phase | Plan 06-04 : recopie verbatim assumée + `skip` portant `MOTIF_BASE_ABSENTE` |
| Méthode de capture des sorties longues | Le test de mutation doit imprimer la sortie réelle en cas de non-morsure | Patron existant : `MOTIF_*` + message d'assertion qui cite la sortie ; la batterie rejouable fournit la sortie brute |

### Les 5 critères de succès → assertions automatisées

Les critères ci-dessous sont **recopiés du ROADMAP** (§ Phase 6) ; la colonne « preuve » dit **ce qui
existe déjà** (`existant`) ou **ce qui doit être écrit** (`nouveau`).

| Critère (verbatim du ROADMAP) | Assertion automatisée proposée | Preuve |
|---|---|---|
| 1. « `docs/depannage.md` permet de retrouver chaque rubrique par le message réellement produit (base absente ou vide, saisie invalide, calcul long, clavier inactif, résultat paginé) — contrôle message → rubrique. » | Table `MESSAGES` → `RUBRIQUE` : (a) chaque message mesuré de § A apparaît dans le corps de la page ; (b) chaque message apparaît dans la rubrique déclarée pour sa famille, et **toutes** les rubriques existent (H2) ; (c) chaque message cité est **adossé** au code : pour la famille « clavier inactif », l'assertion porte sur les faits de A.4 (constantes `terminal.js` lues par la page) et non sur un message ; (d) le nombre de rubriques de la page est ≥ 5 et chaque famille est représentée | `nouveau` (`tests/test_docs_depannage.py`) + réutilise `section`/`sections`/`normalize` (D-12) |
| 2. « `docs/glossaire.md` définit le vocabulaire du produit et de la documentation, chaque entrée citée étant réellement présente et triée. » | (a) les entrées sont extraites (liste/titres selon le format choisi) et leur nombre ≥ la liste de § B « à définir » ; (b) chaque entrée est **triée** (comparaison sur la forme normalisée D-11, locale `fr`) ; (c) chaque terme est **présent** dans le dépôt : au moins une occurrence mesurée (code produit ou page livrée) — l'assertion cite la provenance ; (d) aucune entrée du glossaire ne définit un terme absent des deux (`page épinglée`, `renvoi`, `ancrage` interdits) | `nouveau` (`tests/test_docs_glossaire.py`) + `normalize`, `pages` |
| 3. « Les 8 pages épinglées sont toutes livrées, l'ensemble des fichiers de `docs/` est exactement celui attendu (toute page en trop fait échouer la suite) et le sommaire propose un parcours conseillé final. » | (a) `{f.name for f in docs_dir.glob("*.md")} == set(PAGES_EPINGLEES)` — les deux sens ; (b) chaque page épinglée a un H1 égal à son libellé d'index ; (c) le parcours conseillé contient les 8 pages (ou les 7 de contenu, selon la décision) et **aucun** nom de page inexistante ; (d) le parcours et l'index ne se contredisent pas sur l'ordre si le plan le décide ainsi | `nouveau` (liste épinglée + parcours) ; H1/index **déjà** prouvés par `test_h1_matches_sommaire_entry` et `test_sommaire_lists_every_document` (`tests/test_docs_structure.py:468`, `:134`) |
| 4. « Un test de mutation (copie de `docs/` sous `tmp_path` avec dérive injectée) prouve que le harnais échoue réellement : complétude, ancrage de libellé et renvois obsolètes sont détectés. » | Test pytest en processus : copie `shutil.copytree` **verte avant mutation**, puis 3 dérives + 1 (liste épinglée), chacune exigeant son **motif nommé** ; **plus** une batterie rejouable qui exécute `pytest` dans la copie mutée et colle la sortie réelle | `existant` pour 3 des dérives (mesurées : 14 failed / 1 failed / 1 failed) ; `nouveau` pour la dérive « liste épinglée » ; la batterie est un artefact de vérification (patron `.gsd-tmp/verif-*.sh`) |
| 5. « La vérification finale s'exécute par `.venv/Scripts/python.exe -m pytest -q` (compteur et durée réels cités), `.data/` est inchangée (empreinte ou mtime), aucune connexion réseau n'est ouverte, `main()` n'est jamais exécuté, et `git status` ne montre que `docs/`, `README.md`, `GUIDE_WIZARD.md` et `tests/`. » | (a) exécuter la commande et **citer** `N passed in X.XXs` ; (b) empreinte/mtime de `.data/dofus.sqlite3` **avant/après** identique (nouveau contrôle, patron existant ×3) ; (c) suite complète sous greffon qui refuse `socket`/`urlopen` **et** piège `main()` → **vert** ; (d) `git status --porcelain` filtré : `dofus_stuff/` absent, et l'ensemble observé **expliqué** (livrables + `.planning/**` + outillage) — voir § E.3 | `existant` (a, c : mesurés) ; `nouveau` (b : contrôle d'empreinte dans un module de cette phase) ; `nouveau` (d : constat écrit dans le `SUMMARY`/`VERIFICATION`) |

### Critères prouvés par une garde existante plutôt que par un nouveau test

- **H1 = libellé d'index** de `depannage.md` et `glossaire.md`, **unicité du H1**, **égalité d'ensembles
  index ↔ disque** (sens « page en trop »), **ligne de retour au sommaire**, **encodage UTF-8**,
  **longueur minimale**, **absence de jeton de brouillon**, **résolution de tous les liens internes** : rien
  à écrire, tout est déjà porté par `tests/test_docs_structure.py`. Les pages neuves sont **contraintes**
  par ces gardes dès qu'elles entrent dans `docs/` — c'est pourquoi la rédaction doit respecter le gabarit
  **avant** de lancer la suite.
- **Ancrage des libellés cités** des pages neuves : partiellement déjà porté par
  `tests/test_docs_code_anchor.py:240` pour `installation.md` ; l'extension aux deux pages neuves est
  `nouveau` mais le **mécanisme** est existant.
- **Renvois du README et de `GUIDE_WIZARD.md`** : déjà portés (`tests/test_docs_base_locale.py:1964`,
  `tests/test_docs_parcours.py:2931`), donc tout lien ajouté depuis ces fichiers est automatiquement gardé.

### Seam de vérification (le seul « manuel », remplacé par un contrôle)

Le critère 4 dit « le harnais échoue **réellement** ». La tentation est de le « vérifier à la main » une
fois. Ce n'est pas nécessaire : la voie automatisée est **la batterie rejouable** (§ D.1) qui (i) copie
l'arbre, (ii) exige **vert avant mutation**, (iii) mute, (iv) exige `N failed` **et** le motif nommé. Elle
s'exécute en une commande et sa sortie est **collée** dans le rapport — c'est exactement le patron que
`05-VERIFICATION.md` a employé, et il donne un critère reproductible au lieu d'une déclaration.

## Security Domain

`security_enforcement: true`, `security_asvs_level: 1`, `security_block_on: high`
(`.planning/config.json`).

| Catégorie ASVS | Applicable ? | Contrôle standard | Contrôle de cette phase |
|---|---|---|---|
| V1 Architecture, design & threat modeling | **Oui** | La documentation ne doit pas créer de surface nouvelle | Aucune capacité produit ajoutée ; `dofus_stuff/**` en lecture seule (D-103) |
| V2 Authentication | Non | — | Le produit n'a pas d'authentification (outil local) |
| V3 Session management | Non | — | Les sauvegardes du wizard vivent en `localStorage` (documentées, `docs/parcours-simplifie.md:168-176`) |
| V4 Access control | Non | — | Sans objet |
| V5 Validation, sanitization & encoding | **Oui (documentaire)** | Ne pas publier de données locales, ne pas élargir les exemples | Les pages neuves **ne citent aucun** chemin absolu, date, ni taille de fichier (D-73/D-75, `MOTIF_VOLATILE` `tests/test_docs_base_locale.py:263`) ; aucun identifiant, aucun secret |
| V6 Cryptography | **Oui (interdit)** | Ne pas introduire de crypto | **Aucune** construction de chaîne « sécurisée » ; les seules empreintes sont des mesures de test (`hashlib.sha256` sur `.data/`) |
| V7 Error handling & logging | **Oui** | Les erreurs affichées ne fuient pas d'information sensible | C'est **le sujet** de la page de dépannage : elle documente les messages **réels**, dont aucun ne porte de donnée personnelle ; elle doit **ne pas** normaliser la fuite du chemin local (`Fichier : C:\…`) dans ses exemples — le produit l'affiche, la page n'a pas à le reproduire |
| V8 Data protection | **Oui** | `.data/` ne doit pas être modifiée | Empreinte avant/après identique (mesuré), lecture d'octets seulement, `sqlite3.connect` interdit sur `.data/` (D-104) |
| V9 Communications | **Oui** | Aucune connexion sortante | Greffon qui refuse `socket`/`urlopen` (mesuré vert) ; aucune resynchronisation |
| V10 Malicious code | **Oui** | Aucune commande destructrice présentée comme étape | Le point `db clear` du README est **le** sujet ouvert de D-100 (§ F.1) |
| V11 Business logic | **Oui** | Les exemples ne doivent pas être destructeurs | `tests/test_docs_cli.py:928`, `tests/test_docs_structure.py:275`, `tests/test_docs_base_locale.py:1721` couvrent `docs/` ; **le README échappe encore** |
| V12 Files & resources | **Oui** | Pas d'écriture hors livrables | Toute mutation est sous `tmp_path` ; `git status` explicité (§ E.3) |
| V13 API & web service | Non | — | Le serveur web est local `127.0.0.1` (déjà documenté) |
| V14 Configuration | **Oui** | Pas de configuration secrète | Aucune clé, aucun jeton, aucun fichier de config modifié (hors `.planning/config.json`, outillage, antérieur) |

**Menaces réelles de cette phase :** (a) **divulgation** d'un chemin local ou d'un nom d'utilisateur dans
une page livrée — mitigé par l'absence d'exemple « sortie complète » et par `MOTIF_VOLATILE` ;
(b) **recommandation destructive** (`db clear`) dans le README (D-100) ; (c) **écriture parasite** hors
périmètre (mutations qui viseraient `docs/` livré au lieu d'une copie) — mitigé par `mktemp -d`/`tmp_path`
et par l'audit `git status`. Aucune surface réseau, aucun secret, aucune donnée personnelle : le niveau
ASVS 1 est atteignable sans contrôle supplémentaire.

## Assumptions Log

| # | Affirmation | Statut | Évaluation |
|---|---|---|---|
| A1 | Les 8 pages épinglées sont exactement `sommaire.md`, `installation.md`, `parcours-simplifie.md`, `wizard-avance.md`, `cli.md`, `base-locale.md`, `depannage.md`, `glossaire.md` | `[CITED: .claude/CLAUDE.md:76-83, :93]` + arithmétique mesurée (6 + 2 = 8) | **Confiance élevée**, mais la source est un document de **recherche** de la phase 1 et non un artefact de planification ; le ROADMAP dit « les 8 pages épinglées » sans les énumérer. **Le planificateur fige la constante et la cite** — s'il existait un doute, la seule liste cohérente avec les fichiers livrés est celle-ci |
| A2 | Le `db clear` de `README.md:80` est bien le point hérité de D-100 (et non un `db clear` d'une page livrée, déjà gardé) | `[VERIFIED: README.md:77-81 + § F.1 mesures]` | Confirmé : aucune autre occurrence non gardée n'a été trouvée |
| A3 | « Clavier inactif » n'a **aucun** message produit | `[VERIFIED: recherche `grep` sur le dépôt + mesure des écrans]` | Confirmé par l'absence, qui est un constat **négatif** : la recherche a porté sur `inactif|gelé|figé|bloqu|clavier|keyboard` dans tout le dépôt. Si un message existait sous une forme inattendue, le rédacteur doit refaire la recherche **sur le mot-clé de la rubrique avant d'écrire** |
| A4 | L'assertion CRLF restera vraie pendant la phase | `[VERIFIED: `git ls-files --eol docs/` = `i/lf w/crlf` sur les 6 fichiers]` | Dépend de `core.autocrlf=true` sur ce poste ; limite AR-5 déjà assumée par les phases 3 à 5, à redéclarer |
| A5 | La batterie rejouable peut copier l'arbre avec `cp -r docs tests dofus_stuff fetcher.py pyproject.toml GUIDE_WIZARD.md README.md` | `[VERIFIED: patron `.gsd-tmp/batterie-05-02-t1.sh` + mesure à `216 passed, 3 skipped`]` | Aucun fichier caché requis ; `pyproject.toml` est nécessaire pour que `pytest` trouve `pythonpath = ["."]` |
| A6 | Le compteur final sera > 219 | `[ASSUMED]` | Conséquence arithmétique de 3 modules neufs, mais D-98 impose de **relever** la valeur : ne jamais l'écrire d'avance |
| A7 | `.planning/config.json` et `.gitignore` étaient **déjà** modifiés avant la phase | `[VERIFIED: `git status --porcelain` + `git diff --stat` mesurés]` | Les deux diffs sont de l'outillage (`.gsd-auto/`, `_auto_chain_active`), sans rapport avec les livrables |

**Toute affirmation `[ASSUMED]` ci-dessus doit être validée par un contrôle avant d'entrer dans une page
livrée.** Les affirmations `[VERIFIED]` de ce document sont adossées à une mesure ou à une lecture citée
cette session.

## Open Questions (RESOLVED)

1. **Le « clavier inactif » a-t-il un message ?**
   - Ce qui était ambigu : la famille est nommée dans le critère 1, au même titre que quatre familles qui
     portent des messages.
   - **Résolu :** non, aucun message (§ A.4). La rubrique s'adosse au mécanisme JS et au rendu des écrans
     sans champ, avec la limite A2 déclarée.
2. **Faut-il construire de zéro la preuve de mutation du critère 4 ?**
   - **Résolu :** non. Trois dérives sur quatre sont déjà détectées par des gardes existantes (**mesuré**) ;
     le delta est la **liste épinglée** et l'**oracle de sortie** (§ D.2, § Feasibility).
3. **La liste épinglée est-elle redondante avec `problemes_index` ?**
   - **Résolu :** non. `problemes_index` compare l'index au disque ; une page **listée et présente** qui ne
     serait pas l'une des 8 passerait. La constante neuve est donc nécessaire, et sa morsure doit porter un
     motif **distinct** (Pitfall 5).
4. **Le parcours conseillé est-il déjà gardé ?**
   - **Résolu :** non (`grep "Parcours" tests/*.py` → 0). Il est aujourd'hui **faux sur disque** (deux pages
     annoncées, inexistantes) : c'est un effet du plan 06-02, et il doit devenir vérifiable (§ C.4).
5. **Comment muter sans piéger l'assertion CRLF, `__future__` ou la garde de clôture ?**
   - **Résolu :** mutation par octets avec ancres `\r\n` (§ D.4) ; module de mutation sans
     `from __future__ import annotations` s'il subit une morsure d'import (§ D.5) ; voie in-process, ou écart
     `subprocess` écrit et justifié (§ D.3).
6. **Le critère 5 est-il vrai à la lettre ?**
   - **Résolu :** non pour la partie `git status` (§ E.3) : la phase fera bouger `.planning/**`, et deux
     fichiers d'outillage sont modifiés **avant** elle. L'audit doit être écrit sur le périmètre livrable,
     avec ces écarts nommés.
7. **Que faire du `db clear` du README (D-100) ?**
   - **Résolu au niveau des faits, pas au niveau du choix :** aucune garde ne le voit, le bloc est tagué
     `bash`, `db sync` y est aussi ; les deux options et leur coût sont mesurés (§ F.1). Le choix appartient
     au planificateur (D-100 l'exige explicitement, sinon « deux-entre non écrit »).

## Claims non vérifiées (à ne pas reprendre sans mesure)

| Affirmation | Pourquoi elle n'est pas vérifiée | Ce qu'il faudrait faire |
|---|---|---|
| « `PURGE OUI` n'est pas observable en processus » | C'est une **limite déclarée** héritée (docstring de `tests/test_docs_base_locale.py:26-29`, D-85). Je ne l'ai pas re-mesurée | Rien pour cette phase : ne pas présenter le contrôle JS comme complet |
| Le comportement d'un **navigateur réel** (DOM, focus après `preventDefault`) | Aucun navigateur piloté, aucun lancement de serveur (interdit) | Ne rien affirmer de plus que la lecture de `terminal.js` et le rendu HTML |
| Le rendu Markdown des pages neuves **hors GitHub** | Aucun moteur de rendu installé (interdit) | S'en tenir au Markdown nu et aux gardes existantes |
| La liste complète des messages **de toute l'application** | J'ai mesuré les **cinq familles du critère 1** et les refus/bilans qui les entourent, par `grep`, par lecture `ast` et par rendu. Je n'ai **pas** audité chaque littéral du dépôt (p. ex. messages d'`optimize/wizard_flow.py`, de `web/templates/*` hors `screen.html`) | Si un plan veut citer un message hors des familles du critère 1, la ligne du code doit être ouverte **avant** la rédaction |
| « Aucune occurrence de `clavier` dans `dofus_stuff/**` » | Recherche par motif concentrée sur `inactif\|gelé\|figé\|bloqu\|clavier\|keyboard` | Refaire la recherche avant d'écrire la rubrique si le libellé retenu change |
| Le contenu exact des `skip` dans la copie | Mesuré `3 skipped` ; je n'ai pas listé les trois noms | Sans conséquence : la convention `MOTIF_BASE_ABSENTE` est déjà documentée |
| L'état de `.planning/WINDOWS.md` « tel qu'un outil le voit » | J'ai lu le **fichier** (front matter + 6 lignes) et deux résumés ; je n'ai **pas** lancé `gsd-tools windows status` (l'outil, non le dépôt) | Si le rapport final cite la dérive, citer la ligne `id=5` et le message d'outil rapporté par les résumés, en disant d'où il vient |

## Sources

### Primary (HIGH confidence — mesuré ou lu cette session)
- `dofus_stuff/cli.py` (ligne 33 à 433) — aide du parseur, littéraux de `main()`, `_print_db_status`
- `dofus_stuff/sync.py` (11, 41-43, 59, 91-114) — fenêtre 24 h, messages de synchronisation
- `dofus_stuff/catalog.py` (77, 83, 90, 121-122, 144, 246-293) — messages d'`introuvable`, pagination
- `dofus_stuff/api.py` (13, 64-73) — base distante et échecs de tentative
- `dofus_stuff/web/routes.py` (138-150, 226-308, 319-351, 382-428, 461-543, 596-671, 709-713, 756-786, 839-889, 925-1031, 1131-1134) — statuts, corps, écrans
- `dofus_stuff/web/optimize_wizard.py` (36, 180-204, 266-272, 293-333) — récapitulatif, refus
- `dofus_stuff/optimize/profile_input.py` (240-391) — erreurs de saisie CLI/web
- `dofus_stuff/web/templates/screen.html` (49, 61) ; `dofus_stuff/web/static/js/terminal.js` (80-88, 370-400, 595)
- `tests/conftest.py`, `tests/test_docs_structure.py`, `tests/test_docs_code_anchor.py`, `tests/test_docs_cli.py`, `tests/test_docs_parcours.py`, `tests/test_docs_wizard.py`, `tests/test_docs_base_locale.py`
- `docs/*.md` (6 fichiers), `README.md`, `pyproject.toml`
- Mesures exécutées : suite complète (`219 passed in 4.31s`), suite sous greffon (`219 passed in 4.13s`), 4 batteries de mutation (14 failed / 1 failed / 1 failed / vert), empreinte `.data/` ×3 identique, `git status`/`git ls-files --eol`
- `.planning/phases/06-…/06-CONTEXT.md` (D-92…D-105), `.planning/ROADMAP.md` § Phase 6, `.planning/config.json`, `.planning/WINDOWS.md`, `.planning/phases/05-…/05-01-SUMMARY.md:179-184`, `05-04-PLAN.md:185`, `04-03-SUMMARY.md:220`, `05-03-SUMMARY.md:238`

### Secondary (MEDIUM confidence)
- `.claude/CLAUDE.md` — prescriptions projet, liste des 8 pages, interdits (document de recherche, partiellement **divergent** de l'état livré : voir le tableau de § *Project Constraints*)

### Tertiary (LOW confidence — usage de garde-fou uniquement)
- Aucune : cette phase n'emploie aucune source externe (pas de WebSearch, pas de registre de paquets, pas de documentation tierce)

## Metadata

**Confidence breakdown:**
- **Inventaire des messages (A)** : HIGH — chaque chaîne citée vient d'une lecture `fichier:ligne` ou d'un rendu mesuré cette session ; les littéraux de `main()` ont été lus par `ast` sans l'exécuter.
- **Vocabulaire (B)** : HIGH pour la provenance de chaque terme, MEDIUM pour le **périmètre** final du glossaire (le plan peut retenir plus ou moins d'entrées ; la règle « définir seulement ce qui n'est défini nulle part » est, elle, mesurée).
- **Complétude et gardes (C)** : HIGH — ensemble des fichiers, liste épinglée, gardes existantes et morsures mesurées.
- **Provabilité du harnais (D)** : HIGH pour les morsures mesurées (4 dérives, dont une **qui ne mord pas** — la limite est documentée) ; MEDIUM pour le **choix** entre test in-process et `subprocess` (décision de planification).
- **Vérification finale (E)** : HIGH — compteur, durée, greffon et empreinte mesurés ; le périmètre `git status` est **mesuré faux** tel qu'écrit dans le critère, et corrigé par l'analyse.
- **Points hérités (F)** : HIGH pour les faits (`db clear` non gardé, état du registre) ; le **choix** de D-100 reste ouvert.
- **Pitfalls** : HIGH — chacun adossé à une mesure de cette session ou à un artefact de phase antécédent cité.

**Research date:** 2026-09-12
**Valid until:** 2026-10-12 (la matière est interne et stable ; re-mesurer si `docs/`, `tests/` ou `dofus_stuff/**` changent — en particulier si une page est renommée ou si `.data/dofus.sqlite3` est modifiée par un autre chemin, ce qui invaliderait l'empreinte de référence).
