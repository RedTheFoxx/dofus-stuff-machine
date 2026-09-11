# Phase 5: Base locale, hors-ligne et resynchronisation - Research

**Researched:** 2026-09-11
**Domain:** Documentation ancrée au code d'un produit Python local (SQLite `.data/dofus.sqlite3`, deux surfaces CLI/web, harnais pytest d'ancrage documentaire)
**Confidence:** HIGH (toute la matière est interne au dépôt et a été mesurée cette session)

---

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions
[Copy verbatim from CONTEXT.md ## Decisions]

### Périmètre et gabarit de `docs/base-locale.md`
- **D-68:** La page est la **source unique** du sujet « base locale » : le fichier, les catégories
  d'objets stockées, la fenêtre de re-check de 24 h, les deux défauts hors-ligne et les champs de
  l'état de la base. Aucun de ces énoncés n'est décrit deux fois ailleurs (D-17) ; les pages voisines
  y renvoient par lien.
- **D-69:** Gabarit de page hérité, sans exception (D-01) : `H1` unique `# Base locale` **égal au
  libellé d'index** après normalisation, introduction en français, sections courtes, bloc
  « Source de vérité » dont **chaque chemin entre accents graves existe sur disque**, dernière ligne
  non vide `[Retour au sommaire](sommaire.md)`. Fichier **CRLF, UTF-8 sans BOM** (D-67).
- **D-70:** `docs/sommaire.md` gagne **exactement une** ligne d'index
  `| [Base locale](base-locale.md) | … |` **à cette phase** — l'index croît au rythme des pages créées
  (D-05). L'ordre des lignes existantes et l'ordre du « Parcours conseillé » ne sont pas remaniés. La
  liste épinglée des 8 pages reste à la phase 6.

### Les deux défauts hors-ligne (critère 2)
- **D-71:** Les deux défauts sont énoncés **séparément et nommés par leur surface**, jamais fusionnés
  en une phrase générale : **le web est hors-ligne par défaut** et **la CLI est en ligne par défaut,
  donc `--offline` y est requis**. Chaque énoncé dit **où** il s'applique (lancement web / commande CLI).
- **D-72:** Les **orthographes exactes** des drapeaux et leurs textes d'aide sont **lus dans le code**
  au moment de la recherche et de la rédaction, jamais écrits de mémoire (D-19). La page ne cite un
  drapeau que si le code le porte.

### Fenêtre de re-check de 24 heures (critère 1)
- **D-73:** La fenêtre est documentée depuis le code (`dofus_stuff/sync.py`,
  `CHECK_INTERVAL_SECONDS = 24 * 60 * 60`), **constante nommée**, sans recopier aucune date, durée
  calculée ni horodatage (D-72 ci-dessus : aucune valeur volatile).

### Fichier et catégories stockées (critère 1)
- **D-74:** Le nom du fichier est documenté depuis `dofus_stuff/database.py` (`DB_NAME`), pas depuis
  la mémoire. Les **catégories d'objets réellement stockées** sont relevées dans le code (schéma,
  modules d'écriture) ; la page ne revendique aucune catégorie que le code ne stocke pas.

### Champs de l'état de la base (critères 2 et 5)
- **D-75:** Chaque **nom de champ ou de commande** cité par la page est **produit par le code** :
  lu dans une constante publique (D-14) ou au rendu, jamais recopié de mémoire. Les champs sont décrits
  **par leurs noms**, sans aucune **valeur volatile** (date, taille, compteur, version courante).
- **D-76:** Un champ dont le nom n'est produit ni par une constante publique ni par un rendu
  observable **n'est pas cité** : la page ne décrit que ce qu'un contrôle peut ancrer.

### Cas non évidents (critère 3)
- **D-77:** `db status` **crée le fichier s'il n'existe pas** : le comportement est décrit comme tel,
  et il est **prouvé sans toucher `.data/`** (répertoire temporaire, jamais la base réelle).
- **D-78:** `db sync` **refuse `--offline`** : le refus est décrit et **son message réel** est cité
  depuis le code (`dofus_stuff/cli.py`), jamais paraphrasé.
- **D-79:** L'écran web de synchronisation **contacte l'API même en mode hors-ligne** : c'est le seul
  endroit où le mode hors-ligne **ne s'applique pas**, et la page le dit explicitement.

### Commandes destructrices (critère 4)
- **D-80:** `db clear` et `PURGE OUI` sont **signalées comme destructrices sur la même ligne** que la
  commande, et n'apparaissent dans **aucun parcours recommandé**. La page ne présente jamais l'une
  d'elles comme une étape à suivre.
- **D-81:** **Aucun contrôle de la phase n'exécute une commande destructrice**, n'écrit sous `.data/`,
  n'exécute de synchronisation, ni n'ouvre de connexion réseau. La démonstration d'un comportement qui
  toucherait la base se fait **exclusivement** dans un répertoire temporaire (`tmp_path`), et
  l'intégrité de la base réelle est mesurée (empreinte) **avant et après la suite entière**.

### Contrôles d'ancrage (critère 5)
- **D-82:** Un module dédié `tests/test_docs_base_locale.py` porte l'ancrage de la page ; il **réutilise
  les fixtures partagées** de `tests/conftest.py` et ne les recopie pas (D-12).
- **D-83:** Chaque constat d'échec cite **la page, la valeur attendue et le fichier de code producteur**
  (D-13), de sorte qu'un échec dise quoi corriger sans lecture supplémentaire.
- **D-84:** Les morsures sont jouées **sur une copie verte en répertoire temporaire, avant mutation**,
  jamais sur l'arbre réel ni sur `.data/` ; chaque morsure rapportée provient d'une **sortie réellement
  obtenue**, jamais d'un résultat attendu.
- **D-85:** Le module **déclare ses limites honnêtes** : ce que la page ne revendique pas
  (couverture et précision des contrôles), sans revendiquer d'exhaustivité.

### Frontières et conventions
- **D-86:** Les renvois de la page se font **par lien uniquement là où la cible existe** (leçon D-44) :
  aucun lien mort, aucune cible citée en prose sans lien lorsqu'elle n'existe pas encore.
- **D-87:** La phase 5 porte en plus le contrôle de complétude demandé par le porteur du projet :
  **les renvois de `README.md` pointent vers des fichiers qui existent**. Le libellé « T6 » employé par
  le porteur n'a **aucune définition dans les artefacts de planification** (vérifié : aucune
  occurrence) : le critère est donc pris **à la lettre** (les renvois du README résolvent) et n'est pas
  étendu à une liste de pages que le README ne cite pas.
- **D-88:** `dofus_stuff/**` n'est **pas modifié** : le code est la référence et la page s'y conforme
  (D-19).
- **D-89:** **Aucune resynchronisation Dofusdude** n'est déclenchée par cette phase ; le travail se fait
  **hors-ligne d'abord** sur la base locale existante. Aucun `db clear`, aucun `drop`, aucune
  suppression sous `.data/` ni sous `.doc-agent/`.
- **D-90:** Conventions des phases 1 à 4 applicables **telles quelles** (D-01…D-67) : normalisation
  accents/casse/CRLF/balises (D-11), helpers partagés (D-12), constats (D-13), constantes publiques
  (D-14), interpréteur épinglé `./.venv/Scripts/python.exe` (D-15), une seule source par énoncé (D-17),
  aucune sémantique inventée (D-19), français (D-67).
- **D-91:** Commits **locaux** uniquement, indexation **par chemin explicite** (jamais `git add .`, ni
  `doc-agent.toml`, ni `.doc-agent/`, ni `gsd-auto*.toml`, ni `.planning/state.json`) ; **aucune
  publication, aucun déploiement distant** ; **aucune dépendance ajoutée**.

### Claude's Discretion
- L'ordre exact des sections à l'intérieur de la page, la formulation de l'introduction.
- Le nombre et la forme des contrôles d'ancrage, et le découpage des sections du module de test.
- Le point de savoir si les deux défauts hors-ligne ont leur propre section ou sont deux sous-blocs
  d'une même section.
- Les termes exacts employés pour signaler le caractère destructeur, tant que l'avertissement est
  **sur la même ligne** que la commande (D-80).

### Deferred Ideas (OUT OF SCOPE)
- Preuve de complétude des pages et liste épinglée des pages → phase 6.
- Dépannage par message d'erreur → phase 6.
- Glossaire → phase 6.
- Toute discussion sur une resynchronisation Dofusdude (hors périmètre : le travail est hors-ligne
  d'abord).
</user_constraints>

---

## Summary

Cette phase est **intégralement interne au dépôt** : aucune documentation tierce, aucun paquet, aucune
API. La « recherche » consiste donc à **mesurer** ce que le code produit réellement — nom du fichier,
schéma, catégories stockées, constante de la fenêtre de re-check, défauts et textes d'aide des deux
parseurs, refus, champs rendus par l'état de la base, commandes destructrices — puis à dire, pour
chaque énoncé, **comment un contrôle automatique peut le prouver sans toucher `.data/` ni ouvrir de
connexion réseau**. C'est la méthode des phases 2 à 4, prolongée : le client de test Flask en
processus et les parseurs publics remplacent l'exécution du produit.

Quatre résultats de mesure structurent la planification :

1. **Les deux « hors-ligne » ne font pas la même chose, et le disent différemment.** Côté CLI,
   `--offline` laisse **tourner la vérification de version** : la fenêtre est consultée, puis la
   synchronisation est refusée (`{"action": "skip", "reason": "offline"}`, mesuré) ou lève
   `Base locale vide et --offline : impossible de synchroniser` sur une base vide (mesuré). Côté web,
   `reload_catalog` calcule `skip_sync = bool(cfg["offline"]) and not force_sync` et
   `Catalog.load(skip_sync=True)` **n'appelle jamais `ensure_up_to_date`** : aucune vérification de
   version n'a lieu au démarrage. C'est le point exact où une phrase générale (« l'outil est
   hors-ligne par défaut ») serait vraie en apparence et fausse en pratique (D-71).
2. **Les cinq noms de champs de l'état de la base ne sont adossés à aucune constante publique.**
   Ils sont des littéraux internes à `_print_db_status` (`dofus_stuff/cli.py:214-229`) et à
   `db_status` (`dofus_stuff/web/routes.py:744-785`), et **les deux surfaces ne portent pas les mêmes
   chaînes** : la CLI rend `Entrées :` (accentué) et `Dernier check :`, le web rend `ENTREES :` (sans
   accent) et `DERNIER CHECK :`. La route d'ancrage est donc le **rendu** : client de test Flask pour
   l'écran `DB-02`, sortie capturée de `_print_db_status` (ou ses littéraux lus par `ast`) pour la CLI.
   Un seul champ de la base est produit par une constante publique : rien (voir § *Feasibility*).
3. **`db status` crée le fichier, et c'est mesuré sur les deux surfaces.** `main()` ouvre la base
   (`dofus_stuff/cli.py:338`) avant de brancher sur la sous-commande, et `Database.open()` fait
   `mkdir(parents=True, exist_ok=True)` puis `sqlite3.connect(self.path)`
   (`dofus_stuff/database.py:41-42`) : sur un répertoire inexistant, `_print_db_status` crée dossier et
   fichier (mesuré). L'écran web `/db/status` fait de même (`routes.py:747-748`, mesuré HTTP 200 sur un
   répertoire absent). **Aucune de ces deux mesures n'ouvre `.data/dofus.sqlite3`** : elles passent par
   un répertoire temporaire.
4. **La seule occurrence d'une commande destructrice présentée comme une étape est dans `README.md`.**
   `README.md:80` porte `python fetcher.py db clear           # vider la base` dans un bloc de
   commandes, sans avertissement. Partout ailleurs (`docs/cli.md:174-178`, `:192`), `db clear` est
   étiqueté destructeur et hors parcours. `PURGE OUI` est déjà décrit par `docs/parcours-simplifie.md`
   (`:174`, `:176`) — et, mesuré dans `dofus_stuff/web/static/js/terminal.js:459-466`, il détruit les
   **sauvegardes du navigateur** (`localStorage.removeItem(SAVES_KEY)`), **pas** la base SQLite.

**Primary recommendation:** rédiger `docs/base-locale.md` exclusivement à partir de l'**inventaire
mesuré** de ce document (chaque valeur y est citée verbatim avec sa provenance `fichier:ligne`),
ajouter **une** ligne d'index (D-70), puis écrire `tests/test_docs_base_locale.py` sur le patron de la
phase 4 — fixtures partagées, constats accumulés en une seule assertion, garde `ast` adaptée (le
module **peut** importer `dofus_stuff.database`, il **ne peut pas** appeler `main`, `subprocess`,
`socket`, supprimer un fichier ni poster une confirmation), et mesure d'empreinte de `.data/` autour
des rendus. **Deux modifications de fichiers existants sont obligatoires et doivent être nommées par
le plan** : `docs/sommaire.md` (la ligne d'index) et `tests/test_docs_parcours.py` — sans la réduction
de `PAGES_INEXISTANTES = ("base-locale.md",)` (`:2327`), la création de la page fait **rougir** la
suite (`tests/test_docs_parcours.py:2946-2952`).

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| BASE-01 | Un lecteur comprend le fichier de base locale, les catégories d'objets stockées et la fenêtre de resynchronisation — dérivé de DOCS-07 | Fichier et emplacement mesurés (`DB_NAME`/`DEFAULT_DATA_DIR`, § *1*) ; schéma réel lu dans le code et vérifié sur une copie **lecture seule** de la base (§ *2*) ; les 7 catégories sont la constante publique `ITEM_KINDS` **et** les kinds de `SYNC_SOURCES`, mesurés égaux (§ *3*) ; la fenêtre est `CHECK_INTERVAL_SECONDS = 24 * 60 * 60` avec les quatre sorties mesurées de `ensure_up_to_date` (§ *4*) |
| BASE-02 | Un lecteur comprend les deux comportements hors-ligne (web hors-ligne par défaut ; CLI en ligne par défaut, donc option requise) et les champs affichés par l'état de la base — dérivé de DOCS-07 | Défauts mesurés sur les deux parseurs (`parse_args([]).offline is True` côté web, `False` côté CLI) avec les textes d'aide verbatim (§ *5*) ; **différence de comportement hors-ligne entre les deux surfaces** mesurée (§ *6*) ; les cinq noms de champs lus au rendu des **deux** surfaces, avec leurs écarts d'accentuation (§ *7*) |
| BASE-03 | Les commandes destructrices de la base sont signalées comme telles et jamais présentées comme une étape normale — dérivé de DOCS-07 | `db clear` (aide, sous-commande, `DELETE`) et `PURGE OUI` (ligne de statut rendue, `localStorage`) relevés verbatim avec leur portée réelle (§ *10*) ; inventaire des occurrences dans la documentation livrée, dont l'unique exception `README.md:80` (§ *Destructive-command audit*) |
</phase_requirements>

## Project Constraints (from CLAUDE.md)

`./.claude/CLAUDE.md` est le fichier d'instructions projet (`claude_md_path` de `.planning/config.json`).
Directives actionnables pour cette phase, à respecter dans la rédaction **et** dans les tests :

| Directive (verbatim ou résumée) | Portée pour la phase 5 |
|---------------------------------|------------------------|
| Documentation **intégralement en français** ; « le code, les chemins et les identifiants techniques restent inchangés » | La page et les constats du module sont en français ; les identifiants cités (`ITEM_KINDS`, `CHECK_INTERVAL_SECONDS`, `db status`) sont recopiés tels quels |
| « **Technique** : Python 3.11+, package `dofus_stuff`, pytest comme seul outillage de vérification — pas de nouvelle dépendance pour la documentation » | Aucun ajout à `pyproject.toml` ; `re`, `pathlib`, `ast`, `hashlib` suffisent |
| « **Données** : lecture seule sur `.data/` — jamais de `db clear`, de drop SQLite ni de suppression sous `.data/` » | Aucun contrôle n'exécute `db clear`, aucun POST de confirmation n'est envoyé, `.data/` n'est lu que pour l'empreinte (jamais écrit) |
| « **Réseau** : mode hors-ligne par défaut ; aucune resynchronisation Dofusdude sauf nécessité démontrée » | Les seuls écrans rendus sont des `GET` sans synchronisation ; aucun appel à `ensure_up_to_date` avec `offline=False` |
| « **Vérification** : les critères de « fait » doivent être prouvés par des tests pytest réellement exécutés — aucune validation manuelle ni résultat inventé » | Chaque critère est une assertion ; les morsures sont des sorties de commande réellement obtenues (D-84) |
| « Ancrer un chiffre de base (`18288` objets, `3.6.10.11`) dans la doc » → *What NOT to Use* | Interdit : la page ne cite ni compteur, ni version de jeu, ni horodatage (D-73/D-75) |
| « Lire `.data/dofus.sqlite3` dans les tests de doc » → *What NOT to Use* | Interdit hors mesure d'empreinte (lecture d'octets, jamais d'ouverture SQLite du chemin réel) |
| `§4.3` prescrit un test nommé `test_db_status_fields_documented` ancré sur « `dofus_stuff.cli` » et « `dofus_stuff.sync.CHECK_INTERVAL_SECONDS` », reprenant « les libellés de sortie de `_print_db_status` (`Fichier :`, `Version jeu :`, `Dernier check :`, `Entrées :`, `Par catégorie :`) et la fenêtre **24 h** » | **Ce test n'existe pas** (vérifié : `grep -rn "test_db_status_fields_documented\|_print_db_status\|CHECK_INTERVAL_SECONDS\|ITEM_KINDS" tests/*.py` ne renvoie **rien**). L'attente écrite reste une bonne spécification : elle **légitime par son nom** la route d'ancrage `_print_db_status` pour les libellés CLI |
| `§2.3` prescrit un bloc « Documentation utilisateur » de `README.md` contenant sept puces, dont `- [Base locale et mode hors-ligne](docs/base-locale.md)` | **Non implémenté et supersédé** : `README.md:7` porte **un seul** lien vers `docs/sommaire.md` (contrôle `tests/test_docs_structure.py:190-210`, « exactement 1 cible `docs/sommaire.md` », D-10). La phase ne doit **pas** ajouter sept puces au README ; D-87 limite le travail README à la résolution de ses renvois |
| `§4.3` rattache `docs/base-locale.md` à `tests/test_docs_code_anchor.py` | **Supersédé** par le patron réel des phases 3 et 4 : chaque page a son **module dédié** (`test_docs_parcours.py`, `test_docs_wizard.py`). D-82 tranche : `tests/test_docs_base_locale.py` |
| `§10` : « Markdown ↔ … Windows (CRLF…) — Ne pas asserter sur les octets de fin de ligne » (confiance MEDIUM) | **En conflit avec l'état réel** : les phases 3 et 4 assertent les octets CRLF (`tests/test_docs_parcours.py:2635-2646`, `tests/test_docs_wizard.py:1834-1840`) et la convention est verrouillée (D-67, D-69, D-90). La phase 5 suit **la convention verrouillée et le patron réel**, et déclare la limite non portabilité (voir § *Pitfalls*, L-5 / AR-5) |

*Aucune de ces directives n'entre en conflit irréconciliable avec les décisions D-68…D-91 : les deux
écarts (README à sept puces, module d'ancrage unique) sont des prescriptions de la phase 1 déjà
tranchées autrement par les phases 1 à 4, et les signaler ici évite que le planificateur les
« restaure ».*

## Architectural Responsibility Map

Le « produit » de cette phase est une page Markdown, mais sa **source de vérité est double** — le code
qui produit les valeurs, et le rendu qui les rend observables. La carte ci-dessous attribue chaque
capacité à la couche propriétaire, pour éviter qu'un plan ne fasse décrire la prose par le code ou
l'inverse.

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|--------------|----------------|-----------|
| Vérité du nom de fichier, du schéma et des catégories stockées | **Produit — `dofus_stuff/database.py` + `dofus_stuff/api.py` (`SYNC_SOURCES`) + `dofus_stuff/sync.py` (`pull_all`)** | — | Le code est la source de vérité (D-19, D-88) ; il n'est pas modifié par cette phase |
| Vérité de la fenêtre de re-check | **Produit — `dofus_stuff/sync.py`** (`CHECK_INTERVAL_SECONDS`, `ensure_up_to_date`) | `dofus_stuff/catalog.py` (`Catalog.load` → `ensure_up_to_date`) | La constante est publique ; les décisions de branchement sont dans `ensure_up_to_date` |
| Vérité des défauts hors-ligne et de leurs textes d'aide | **Produit — les deux parseurs publics** : `dofus_stuff/cli.py::build_parser`, `dofus_stuff/web/__main__.py::build_parser` | `dofus_stuff/web/__init__.py::reload_catalog` (ce que « hors-ligne » change réellement côté web) | D-14 : sonde par l'API publique du parseur, jamais par introspection privée d'`argparse` |
| Vérité des champs de l'état de la base | **Produit — `dofus_stuff/cli.py::_print_db_status`** (surface CLI) et **`dofus_stuff/web/routes.py::db_status`** (surface web) | — | Aucun de ces noms n'est une constante publique : le rendu (ou la sortie capturée) est le seul ancrage (§ *Feasibility*) |
| Vérité des commandes destructrices | **Produit — `dofus_stuff/cli.py` (`db clear`), `dofus_stuff/web/routes.py` (écrans `DB-01`/`DB-04`, `SAV-01`), `dofus_stuff/web/static/js/terminal.js` (`PURGE OUI`)** | `dofus_stuff/database.py::Database.clear` (effet réel) | La page signale ; elle n'exécute jamais (D-80, D-81) |
| Description du sujet « base locale » | **`docs/base-locale.md`** (nouvelle page, source unique, D-68) | `docs/cli.md` (surface de commandes, propriétaire inchangé), `docs/installation.md` (premier contact et démarrage web) | Une seule source par énoncé (D-17) : la page décrit, les voisins renvoient par lien (D-86) |
| Navigation documentaire (index) | **`docs/sommaire.md`** (table d'index, une ligne, D-70) | — | Le sommaire croît par phase (D-05) ; l'exhaustivité bidirectionnelle reste le signal (D-06) |
| Résolution des renvois du `README.md` | **`README.md`** (lecture seule hors correction de renvoi) | `tests/test_docs_base_locale.py` (nouveau contrôle D-87) | D-87 : le critère est pris à la lettre — les renvois du README résolvent |
| Détection d'une dérive de la page | **Harnais pytest — `tests/test_docs_base_locale.py`** | fixtures partagées de `tests/conftest.py` (D-12) | Le test est le juge ; les morsures se jouent sur copie (D-84) |

---

## Measured inventory

**C'est la section que le planificateur recopie.** Chaque ligne porte une valeur **verbatim** telle que
le code la produit, et sa provenance `fichier:ligne`. Une valeur absente de cette section n'est pas
citable (D-76) ; une valeur volatile est nommée comme telle et **interdite à la citation** (D-73,
D-75). Toutes les lectures de cette session ont porté sur l'arbre réel, sans exécuter `main()`, sans
synchronisation et sans écrire sous `.data/` (méthode : § *Feasibility*).

### 1. Le fichier de base et son emplacement

| Élément | Valeur verbatim | Provenance |
|---------|-----------------|------------|
| Nom du fichier | `DB_NAME = "dofus.sqlite3"` | `dofus_stuff/database.py:12` |
| Répertoire par défaut | `DEFAULT_DATA_DIR = Path(__file__).resolve().parent.parent / ".data"` | `dofus_stuff/database.py:13` |
| Chemin résolu (mesuré) | `C:\Users\Red\Documents\Projets\dofus-stuff-machine\.data` — **égal** à `Path(tests/..)/.data` (mesuré `True`) | mesure de session (§ *Environment*) ; `dofus_stuff/database.py:13` |
| Chemin du fichier | `property def path(self) -> Path: return self.data_dir / DB_NAME` | `dofus_stuff/database.py:34-36` |
| Création du dossier et du fichier | `self.data_dir.mkdir(parents=True, exist_ok=True)` puis `self._conn = sqlite3.connect(self.path, check_same_thread=False)` | `dofus_stuff/database.py:41-42` |
| Défaut CLI `--data-dir` | `default=DEFAULT_DATA_DIR` — donc `.data/` à la racine du dépôt | `dofus_stuff/cli.py:38` |
| Aide CLI de `--data-dir` (⚠ volatile) | `help=f"Répertoire de la base locale (défaut : {DEFAULT_DATA_DIR})"` — l'aide **imprime le chemin absolu du poste** ; la page ne recopie **jamais** ce chemin | `dofus_stuff/cli.py:39` |
| Défaut web `--data-dir` | `default=Path(os.environ.get("DOFUS_DATA_DIR", DEFAULT_DATA_DIR))`, aide `"Répertoire de la base locale"` (**sans** chemin absolu, contrairement à la CLI) | `dofus_stuff/web/__main__.py:15-20` |
| Base non versionnée | `.gitignore` porte `.data/` | `.gitignore:6` |

Mesures de création (repertoire temporaire, `tmp_path`) :

```
AVANT : dossier False | fichier False
APRÈS Database(data_dir=tmp/"absent").open() : dossier True | fichier True
```

Deux points mesurés qui comptent pour la rédaction :

- **Le dossier parent est créé** (`parents=True`), pas seulement le fichier.
- Le fichier est un SQLite standard : ses 16 premiers octets mesurés sont `b'SQLite format 3\x00'`
  (base réelle, lecture seule). **La taille, la date et l'empreinte ne sont pas citables** (D-73/D-75) ;
  la lecture seule de la base n'a d'autre but que de vérifier ce que le schéma contient réellement
  (§ *3*).

### 2. Le schéma réellement créé

Le schéma est le texte que `Database.open()` exécute (`dofus_stuff/database.py:43-61`) :

| Objet | Définition verbatim (SQL) | Provenance |
|-------|---------------------------|------------|
| Table `meta` | `CREATE TABLE IF NOT EXISTS meta (key TEXT PRIMARY KEY, value TEXT NOT NULL)` | `dofus_stuff/database.py:44-50` |
| Table `items` | `CREATE TABLE IF NOT EXISTS items (kind TEXT NOT NULL, ankama_id INTEGER NOT NULL, payload TEXT NOT NULL, PRIMARY KEY (kind, ankama_id))` | `dofus_stuff/database.py:52-59` |
| Index | `CREATE INDEX IF NOT EXISTS idx_items_kind ON items (kind)` | `dofus_stuff/database.py:61` |
| Clé de version | `META_GAME_VERSION = "game_version"` | `dofus_stuff/database.py:15` |
| Clé de date de contrôle | `META_LAST_CHECKED_AT = "last_checked_at"` | `dofus_stuff/database.py:16` |

Vérifié **en lecture seule** (`sqlite3.connect("file:...?mode=ro", uri=True)`) sur `.data/dofus.sqlite3` :

```
table | items
table | meta
index | idx_items_kind            CREATE INDEX idx_items_kind ON items (kind)
index | sqlite_autoindex_items_1   (implicite : PRIMARY KEY (kind, ankama_id))
index | sqlite_autoindex_meta_1    (implicite : PRIMARY KEY key)
```

Le `payload` est le JSON de l'entrée : `json.dumps(entry, ensure_ascii=False)`
(`dofus_stuff/database.py:125`), relu par `json.loads` (`dofus_stuff/database.py:140`). **Les deux
noms de tables (`meta`, `items`) et les deux clés de `meta` sont citables** — ils sont produits par le
code ; les **lignes** de `meta` et les **compteurs** ne le sont pas.

### 3. Les catégories réellement stockées

Trois sources concordantes, mesurées **égales** :

| Source | Valeur | Provenance |
|--------|--------|------------|
| Constante publique des catégories | `ITEM_KINDS = ("equipment", "resources", "consumables", "quest", "cosmetics", "mounts", "sets")` | `dofus_stuff/database.py:18-26` (importée et imprimée cette session : 7 éléments) |
| Sources de synchronisation (chemin API, clé JSON, kind stocké) | `SYNC_SOURCES = (("/fr/items/equipment/all", "items", "equipment"), ("/fr/items/resources/all", "items", "resources"), ("/fr/items/consumables/all", "items", "consumables"), ("/fr/items/quest/all", "items", "quest"), ("/fr/items/cosmetics/all", "items", "cosmetics"), ("/fr/mounts/all", "mounts", "mounts"), ("/fr/sets/all", "sets", "sets"))` | `dofus_stuff/api.py:19-28` |
| Égalité mesurée | `tuple(kind for _, _, kind in SYNC_SOURCES) == ITEM_KINDS` → `True` | mesure de session |

**Le seul écrivain** est `pull_all` : `for list_path, collection_key, kind in SYNC_SOURCES:` …
`n = db.replace_kind(kind, typed_entries)` (`dofus_stuff/sync.py:93-104`). Aucun autre appel à
`replace_kind` n'existe dans `dofus_stuff/**` (vérifié : `grep -rn "replace_kind" dofus_stuff/` ne
renvoie que `database.py:117` (définition) et `sync.py:104` (appel)). Le catalogue en mémoire mappe
en plus des sous-types vers ces kinds (`SUBTYPE_TO_KIND`, `dofus_stuff/catalog.py:12-21`, avec
`"weapons": "equipment"`), mais **`weapons` n'est pas un kind stocké** : la page ne doit pas le
présenter comme une catégorie de la base.

Vérifié en lecture seule sur la base réelle : **7 kinds distincts**, exactement
`consumables`, `cosmetics`, `equipment`, `mounts`, `quest`, `resources`, `sets`.
Les **compteurs par catégorie et le total (18288 lignes) sont des valeurs volatiles : interdits à la
citation** (D-73/D-75, et `CLAUDE.md` § *What NOT to Use* nomme explicitement `18288` et `3.6.10.11`).

### 4. La fenêtre de re-check de 24 heures

| Élément | Valeur verbatim | Provenance |
|---------|-----------------|------------|
| Constante | `CHECK_INTERVAL_SECONDS = 24 * 60 * 60` (mesurée : `86400`) | `dofus_stuff/sync.py:11` |
| Décision | `needs_check = force or empty or last_checked is None or (now - last_checked) >= CHECK_INTERVAL_SECONDS` | `dofus_stuff/sync.py:32` |
| Sortie « pas de contrôle » | `return {"action": "skip", "reason": "within_24h", "game_version": local_version, "counts": db.counts_by_kind()}` | `dofus_stuff/sync.py:33-39` |
| Garde hors-ligne | `if offline:` → base vide : `raise RuntimeError("Base locale vide et --offline : impossible de synchroniser")` ; sinon `{"action": "skip", "reason": "offline", …}` | `dofus_stuff/sync.py:41-50` |
| Cas « version inchangée » | `db.touch_checked_at(now)` puis `print(f"Base à jour (version {remote_version}).")` | `dofus_stuff/sync.py:54-62` |
| Resynchronisation | `counts = pull_all(db, version=remote_version, timeout=timeout, quiet=quiet)` → `{"action": "sync", …}` | `dofus_stuff/sync.py:64-69` |
| Déclencheur (CLI et web) | `Catalog.load` appelle `ensure_up_to_date(db, force=force_sync, offline=offline, …)` **sauf** si `skip_sync` | `dofus_stuff/catalog.py:43-52` |
| Drapeau qui force le contrôle | `--force-sync` : `action="store_true"`, `help="Ignorer la fenêtre 24h et forcer une vérif / sync version"`, défaut `False` (mesuré) | `dofus_stuff/cli.py:41-45`, mesure `parse_args([...]).force_sync` |

**Quatre sorties mesurées** (base temporaire, aucune socket) :

| Situation mesurée | Retour réel |
|-------------------|-------------|
| Base remplie, `last_checked_at` = maintenant, sans `force`, **sans** `offline` | `{'action': 'skip', 'reason': 'within_24h', 'game_version': '9.9.9.9', 'counts': {'equipment': 1, 'resources': 1}}` |
| Base remplie, dernier check à −25 h, `offline=True` | `{'action': 'skip', 'reason': 'offline', …}` |
| Base remplie, `force=True` **et** `offline=True` | `{'action': 'skip', 'reason': 'offline', …}` — **`force` ne fait pas contacter l'API quand `offline` est vrai** |
| Base vide, `offline=True` (avec ou sans `force`) | `RuntimeError('Base locale vide et --offline : impossible de synchroniser')` |

Le cas « fenêtre non écoulée » est le seul où la vérification **ne peut pas** contacter l'API : le
retour `within_24h` précède `fetch_version` (`dofus_stuff/sync.py:33-39`). C'est ce qui rend la mesure
du point 1 ci-dessus possible **hors ligne** ; la page documente ce comportement sans jamais citer
l'âge (`il y a 0.0h`) ni l'horodatage.

### 5. Les deux défauts hors-ligne et leurs textes d'aide

**Surface web — hors-ligne par défaut (mesuré) :**

| Élément | Valeur verbatim | Provenance |
|---------|-----------------|------------|
| `--offline` web | `action=argparse.BooleanOptionalAction`, `default=True`, `help="Ne pas contacter l'API au démarrage (défaut : oui)"` | `dofus_stuff/web/__main__.py:21-26` |
| `--online` web | `action="store_true"`, `help="Autoriser le contact API (équivalent --no-offline)"` | `dofus_stuff/web/__main__.py:27-31` |
| Défaut mesuré | `parse_args([]).offline` → `True` ; `parse_args(["--no-offline"]).offline` → `False` ; `parse_args(["--online"])` → `offline=True`, `online=True` | mesure de session |
| Résolution dans `main` | `offline = False if args.online else args.offline` | `dofus_stuff/web/__main__.py:41` |
| Aide rendue (extrait verbatim) | `--offline, --no-offline` ⏎ `Ne pas contacter l'API au démarrage (défaut : oui)` puis `--online` ⏎ `Autoriser le contact API (équivalent --no-offline)` | mesure `format_help()` |
| Variable d'environnement | `resolved_offline = offline if offline is not None else _env_bool("DOFUS_OFFLINE", True)` | `dofus_stuff/web/__init__.py:48-50` |
| Variable d'environnement | `resolved_data_dir = Path(data_dir if data_dir is not None else os.environ.get("DOFUS_DATA_DIR", DEFAULT_DATA_DIR))` | `dofus_stuff/web/__init__.py:43-47` |

**Nuance mesurée au code (à ne pas confondre avec un défaut) :** `DOFUS_OFFLINE` n'est lu que par
`create_app` **quand `offline` ne lui est pas passé**. Le lancement documenté
(`python -m dofus_stuff.web`) passe toujours `offline=offline` (`web/__main__.py:44`), valeur dérivée
du drapeau dont le défaut est `True`. Autrement dit : **`DOFUS_OFFLINE=0` ne rend pas
`python -m dofus_stuff.web` « en ligne »** — c'est `--no-offline` ou `--online` qui le fait. Cette
nuance est une **lecture de code** (aucune exécution de `main()`, interdit) ; `README.md:110` écrit
`` `--offline` / `DOFUS_OFFLINE=1` | Pas d'API (défaut) ``, ce qui reste vrai pour le défaut mais ne
décrit pas ce mécanisme. La page n'a pas à trancher le README (D-87) ; si elle cite `DOFUS_OFFLINE`,
elle doit dire **qui** le lit.

**Surface CLI — en ligne par défaut (mesuré) :**

| Élément | Valeur verbatim | Provenance |
|---------|-----------------|------------|
| `--offline` CLI | `action="store_true"`, `help="Ne pas contacter l'API (échoue si la base locale est vide)"` — **aucun `default=`**, donc `False` | `dofus_stuff/cli.py:46-50` |
| Défaut mesuré | `build_parser().parse_args(["db", "status"]).offline` → `False` ; `parse_args(["--offline", "db", "status"]).offline` → `True` | mesure de session |
| Aide rendue (verbatim, deux lignes) | `--offline             Ne pas contacter l'API (échoue si la base locale est` ⏎ `                        vide)` | mesure `parse_args(["--help"])` |
| Emplacement | options globales : **avant** la sous-commande (`subparsers = parser.add_subparsers(...)` en `cli.py:52`) | `dofus_stuff/cli.py:34-50` |

**Le ROADMAP est confirmé, pas seulement « plausible » :** `--offline` est déclaré `store_true` sans
défaut (`cli.py:46-50`), donc `args.offline is False` quand le drapeau est absent (mesuré) ; la CLI
**est** en ligne par défaut et `--offline` **y est requis** pour ne pas contacter l'API. Les deux
défauts sont donc bien **opposés** selon la surface (D-71).

### 6. Ce que chaque surface fait réellement hors-ligne

C'est le cœur du risque de confusion de la phase (D-71, D-79). Les deux surfaces **ne font pas la
même chose** :

| Question | CLI (`--offline`) | Web (`--offline`, défaut) |
|----------|-------------------|---------------------------|
| La fenêtre 24 h est-elle consultée au démarrage ? | **Oui** : `Catalog.load(offline=True)` → `ensure_up_to_date(offline=True)` (`catalog.py:45-52`) ; les quatre branches de `sync.py:32-50` s'exécutent | **Non** : `reload_catalog` calcule `skip_sync = bool(cfg["offline"]) and not force_sync` (`web/__init__.py:110`) et `Catalog.load(skip_sync=True)` **n'appelle pas** `ensure_up_to_date` (`catalog.py:45` : `if not skip_sync:`) |
| Que se passe-t-il si la fenêtre est écoulée ? | `{"action": "skip", "reason": "offline"}` — **aucune** resynchronisation (mesuré) | Sans objet : aucune vérification n'a lieu |
| Que se passe-t-il si la base est vide ? | `RuntimeError(“Base locale vide et --offline : impossible de synchroniser”)` → `main` imprime `Erreur : <message>` et sort en **1** (`cli.py:430-433`) | **Aucune erreur** : `Catalog.load(skip_sync=True)` ouvre la base (et la crée), le catalogue est simplement vide ; l'interface démarre (documenté `docs/installation.md:81`) |
| L'API est-elle contactée ? | Non — sauf `db sync`, qui **refuse** `--offline` (§ *9*) | Non — **sauf** l'écran de synchronisation web, qui passe `offline=False` (§ *9*) |

La nuance mesurée qui doit apparaître dans la page : **« hors-ligne » veut dire « pas de
resynchronisation » dans les deux cas, mais côté CLI la fenêtre de 24 h est quand même lue, et une base
vide rend une erreur ; côté web, la vérification n'a pas lieu du tout et une base vide est un état
normal.** Une phrase générale qui fusionnerait les deux serait fausse sur au moins une surface.

### 7. Les champs de l'état de la base, nom par nom, par surface

**Aucun de ces noms n'est une constante publique.** Ils sont des littéraux : CLI dans
`_print_db_status` (`dofus_stuff/cli.py:214-229`), web dans `db_status`
(`dofus_stuff/web/routes.py:754-769`). Le rendu est donc le seul ancrage (D-75) ; la faisabilité est
traitée en § *Feasibility*.

**Surface CLI — `python fetcher.py db status` (sortie mesurée, base non vide) :**

```
Fichier : C:\Users\…\data\dofus.sqlite3
Version jeu : 9.9.9.9
Dernier check : il y a 0.0h
Entrées : 3
Par catégorie :
  - equipment : 2
  - resources : 1
```

| Nom produit | Forme verbatim dans le code | Provenance |
|-------------|-----------------------------|------------|
| `Fichier :` | `print(f"Fichier : {stats['path']}")` | `dofus_stuff/cli.py:216` |
| `Version jeu :` (+ état vide `(aucune)`) | `print(f"Version jeu : {stats['game_version'] or '(aucune)'}")` | `dofus_stuff/cli.py:217` |
| `Dernier check :` (deux formes) | `print(f"Dernier check : il y a {age_h:.1f}h")` / `print("Dernier check : (aucun)")` | `dofus_stuff/cli.py:221` et `:223` |
| `Entrées :` (**accentué**) | `print(f"Entrées : {stats['total_items']}")` | `dofus_stuff/cli.py:224` |
| `Par catégorie :` + `  - {kind} : {count}` | `print("Par catégorie :")` puis `print(f"  - {kind} : {count}")` | `dofus_stuff/cli.py:227-229` |

Mesure complémentaire : **sur une base vide, la CLI n'affiche ni `Par catégorie :` ni les lignes par
catégorie** (condition `if isinstance(by_kind, dict) and by_kind:`, `cli.py:226`) ; elle affiche
`Version jeu : (aucune)`, `Dernier check : (aucun)`, `Entrées : 0` (mesuré).

**Surface web — écran `DB-02` (`/db/status`) (corps rendu mesuré, base non vide) :**

```
FICHIER : C:\Users\…\data\dofus.sqlite3
VERSION JEU : 9.9.9.9
DERNIER CHECK : IL Y A 0.0H
ENTREES : 3
PAR CATEGORIE :
  - equipment : 2
  - resources : 1
```

| Nom produit | Forme verbatim dans le code | Provenance |
|-------------|-----------------------------|------------|
| `FICHIER :` | `f"FICHIER : {stats['path']}"` | `dofus_stuff/web/routes.py:755` |
| `VERSION JEU :` (+ état vide `(aucune)`) | `f"VERSION JEU : {stats['game_version'] or '(aucune)'}"` | `dofus_stuff/web/routes.py:756` |
| `DERNIER CHECK :` (deux formes) | `lines.append(f"DERNIER CHECK : IL Y A {age_h:.1f}H")` / `lines.append("DERNIER CHECK : (AUCUN)")` | `dofus_stuff/web/routes.py:761` et `:763` |
| `ENTREES :` (**sans accent**, contrairement à la CLI) | `lines.append(f"ENTREES : {stats['total_items']}")` | `dofus_stuff/web/routes.py:764` |
| `PAR CATEGORIE :` + `  - {kind} : {count}` | `lines.append("PAR CATEGORIE :")` puis `lines.append(f"  - {kind} : {count}")` | `dofus_stuff/web/routes.py:767-769` |
| Identifiant et titre d'écran | `pgm="DB-02"`, `title="** ETAT DE LA BASE **"` (rendu : `PGM: DB-02 … ** ETAT DE LA BASE **`) | `dofus_stuff/web/routes.py:774-775` |

Trois écarts mesurés entre les deux surfaces, à ne pas lisser dans la rédaction :

1. `Entrées :` (CLI, accentué) vs `ENTREES :` (web, sans accent) ;
2. `Dernier check : il y a …h` (CLI, minuscules) vs `DERNIER CHECK : IL Y A …H` (web, capitales) ;
3. `(aucun)` (CLI) vs `(AUCUN)` (web) pour la date de contrôle absente, et `(aucune)` pour les deux
   surfaces quand la version du jeu est absente.

**Nom non citable (D-76) :** aucun autre « champ » n'est produit. En particulier, `stats()` renvoie
une clé `"path"` (`dofus_stuff/database.py:154-161`) qui n'est **pas** un libellé destiné au lecteur ;
la page cite le libellé **rendu** (`Fichier :` / `FICHIER :`), jamais la clé de dictionnaire interne.
Même remarque pour `"total_items"` et `"by_kind"` : ce sont des clés, pas des noms de champs affichés.

### 8. Les sous-commandes `db` et leurs aides réelles

Aide lue en processus par l'API publique (`build_parser().parse_args([... , "--help"])`, patron de
`tests/test_docs_cli.py:268-277`) :

```
usage: <prog> db [-h] {status,stats,sync,fill,clear} ...

positional arguments:
  {status,stats,sync,fill,clear}
    status              Afficher l'état de la base
    stats               ==SUPPRESS==
    sync                Forcer la synchronisation complète
    fill                ==SUPPRESS==
    clear               Vider la base locale
```

| Sous-commande | Aide verbatim | Provenance |
|---------------|---------------|------------|
| `db` | `help="Gérer la base locale"` | `dofus_stuff/cli.py:182` |
| `cache` | `help=argparse.SUPPRESS` (rendu `==SUPPRESS==`) | `dofus_stuff/cli.py:182` |
| `status` | `help="Afficher l'état de la base"` | `dofus_stuff/cli.py:185` |
| `stats` | `help=argparse.SUPPRESS` — **alias de `status`** | `dofus_stuff/cli.py:186`, `:283-285` |
| `sync` | `help="Forcer la synchronisation complète"` | `dofus_stuff/cli.py:187` |
| `fill` | `help=argparse.SUPPRESS` — **alias de `sync`** | `dofus_stuff/cli.py:188`, `:283-285` |
| `clear` | `help="Vider la base locale"` ; option `--all` `action="store_true"`, `help=argparse.SUPPRESS` | `dofus_stuff/cli.py:189-194` |
| Alias | `aliases = {"stats": "status", "fill": "sync"}` | `dofus_stuff/cli.py:283-285` |
| Défaut mesuré | `parse_args(["cache", "fill"]).db_command` → `'fill'` ; `parse_args(["db", "clear", "--all"]).all` → `True` | mesure de session |

**Limite d'ancrage mesurée :** `db status --offline` **n'est pas accepté** — les options globales ne
vivent qu'au niveau racine du parseur ; le refus est déjà documenté et contrôlé
(`docs/cli.md:20-23`, `docs/installation.md:121`, `tests/test_docs_cli.py:193`). La nouvelle page ne
doit pas re-prouver ce point, elle peut y renvoyer par lien (`docs/cli.md`).

### 9. Les cas non évidents (critère 3)

**(a) `db status` crée le fichier s'il n'existe pas.** Chemin réel mesuré :

- `main()` branche sur `if args.command in {"db", "cache"}:` puis construit `db = Database(data_dir=…)`
  et appelle `db.open()` **avant** de choisir la sous-commande — `dofus_stuff/cli.py:335-341` ;
- `db.open()` crée le dossier puis le fichier — `dofus_stuff/database.py:41-42` ;
- `_print_db_status(db)` lit ensuite `db.stats()` — `dofus_stuff/cli.py:214-215`, `:341`.

Mesure (répertoire temporaire inexistant) : `_print_db_status` sur un `Database` non ouvert →
dossier `False` → `True`, fichier `False` → `True`, sortie
`Fichier : …\absent\dofus.sqlite3 | Version jeu : (aucune) | Dernier check : (aucun) | Entrées : 0`.
**Le même effet existe côté web** : `db_status` fait `db = Database(data_dir=data_dir); db.open()`
(`dofus_stuff/web/routes.py:746-748`) ; mesuré `GET /db/status` → **200** sur un répertoire absent,
fichier créé. (Même effet pour toute sous-commande `db`/`cache`, puisque `open()` précède le
branchement.)

**(b) `db sync` refuse `--offline`.** Message verbatim et code de retour :

| Élément | Valeur verbatim | Provenance |
|---------|-----------------|------------|
| Refus | `print("Erreur : --offline incompatible avec db sync", file=sys.stderr)` puis `return 1` | `dofus_stuff/cli.py:344-347` |
| Ce qui est lancé sans `--offline` | `ensure_up_to_date(db, force=True, offline=False, timeout=args.timeout, quiet=False)` | `dofus_stuff/cli.py:348-354` |

**(c) L'écran web de synchronisation contacte l'API même hors-ligne.** C'est le seul endroit où le mode
hors-ligne ne s'applique pas (D-79) :

| Élément | Valeur verbatim | Provenance |
|---------|-----------------|------------|
| Écran de confirmation `DB-03` (GET, **sans** appel API) | `"CETTE OPERATION CONTACTE L'API DOFUSDUDE"`, `"ET PEUT PRENDRE PLUSIEURS MINUTES."`, `"CONFIRMER ? (O=OUI / N=NON)"` ; `pgm="DB-03"`, `title="** SYNCHRONISATION **"` | `dofus_stuff/web/routes.py:788-804` |
| Confirmation exigée | `confirm not in {"O", "Y", "OUI", "YES"}` → `flash("SYNC ANNULEE", "info")` et redirection (mesuré : `POST /db/sync` avec `confirm=N` → **302 `/db`**) | `dofus_stuff/web/routes.py:807-812` |
| **Le contact API hors-ligne** | `ensure_up_to_date(db, force=True, offline=False, timeout=timeout, quiet=True)` — `offline=False` **en dur**, quel que soit `cfg["offline"]` | `dofus_stuff/web/routes.py:820-826` |
| Pourquoi | L'écran est **explicitement** une synchronisation forcée : la page de confirmation l'annonce (« CETTE OPERATION CONTACTE L'API DOFUSDUDE ») ; le mode hors-ligne règle le **démarrage** (`--offline` web : « Ne pas contacter l'API **au démarrage** »), pas ce bouton | `dofus_stuff/web/__main__.py:25`, `dofus_stuff/web/routes.py:794` |

Conséquence pour le harnais : **`GET /db/sync` est sûr** (rendu de confirmation, aucune socket) ;
**`POST /db/sync` avec une confirmation est interdit** — il déclenche `ensure_up_to_date(offline=False)`
et écrirait la base. `tests/test_web.py:378-388` ne l'autorise qu'en **patcheant**
`dofus_stuff.web.routes.ensure_up_to_date` ; le module de la phase 5, lui, ne le poste **jamais**.

### 10. Les commandes destructrices

`db clear` (CLI) :

| Élément | Valeur verbatim | Provenance |
|---------|-----------------|------------|
| Déclaration | `clear_parser = db_sub.add_parser("clear", help="Vider la base locale")` | `dofus_stuff/cli.py:189` |
| Effet réel | `cur = conn.execute("DELETE FROM items")` puis `conn.execute("DELETE FROM meta")` puis `conn.commit()` ; retourne `cur.rowcount` | `dofus_stuff/database.py:146-152` |
| Sortie | `print(f"Base vidée : {deleted} entrée(s) supprimée(s).")` | `dofus_stuff/cli.py:357-360` |
| Effet sur le fichier | **Le fichier n'est pas supprimé** (mesuré : après `clear()`, `fichier existe encore ? True`, `total = 0`, `game_version = None`) | mesure de session ; `dofus_stuff/database.py:146-152` |

`db clear` côté web — écran `DB-04` :

| Élément | Valeur verbatim | Provenance |
|---------|-----------------|------------|
| Entrée de menu `DB-01` | `"3. VIDER LA BASE (CLEAR)"` | `dofus_stuff/web/routes.py:714` |
| Avertissement rendu | `"ATTENTION : TOUTES LES ENTREES LOCALES SERONT SUPPRIMEES."` puis `"CONFIRMER ? (O=OUI / N=NON)"` | `dofus_stuff/web/routes.py:849-851` |
| Étiquette de statut | `status="OPERATION DESTRUCTIVE"`, `status_kind="error"` ; ligne de statut **rendue** : `OPERATION DESTRUCTIVE — ENTREE=VALIDER` | `dofus_stuff/web/routes.py:858-859` ; assemblage `routes.py:143-150` (mesuré) |
| Titre | `pgm="DB-04"`, `title="** VIDER LA BASE **"` | `dofus_stuff/web/routes.py:846-847` |

`PURGE OUI` — ce que c'est **réellement** (mesuré) :

| Élément | Valeur verbatim | Provenance |
|---------|-----------------|------------|
| Ligne de statut rendue par `SAV-01` | `status="N OUVRIR | DEL N | PURGE OUI"` ; rendu : `N OUVRIR | DEL N | PURGE OUI — ENTREE=VALIDER` | `dofus_stuff/web/routes.py:1293` ; assemblage `routes.py:143-150` |
| Effet réel | `if (upper === "PURGE OUI") { … localStorage.removeItem(SAVES_KEY); … setStatus("SAUVEGARDES PURGEES", "info"); }` | `dofus_stuff/web/static/js/terminal.js:459-466` |
| Confirmation en deux temps | `if (upper === "PURGE") { setStatus("CONFIRMER AVEC : PURGE OUI", "error"); }` | `dofus_stuff/web/static/js/terminal.js:469-470` |
| Ligne de statut paginée | `"PAGE " + page + "/" + total + " — N OUVRIR | DEL N | PURGE OUI | ESC"` | `dofus_stuff/web/static/js/terminal.js:370` |
| Refus | `setStatus("COMMANDE INVALIDE — N | DEL N | PURGE OUI", "error")` | `dofus_stuff/web/static/js/terminal.js:494` |

**Fait mesuré qui change la rédaction :** `PURGE OUI` détruit les **stuffs sauvegardés dans le
navigateur** (`localStorage.removeItem(SAVES_KEY)`), **pas** la base SQLite. Le critère 4 du ROADMAP
range `db clear` et `PURGE OUI` sous « commandes destructrices de la base » ; le code dit autre chose
pour la seconde. La page doit **signaler les deux comme destructrices** (D-80) et **dire ce que
chacune détruit**, sans reprendre la formulation « de la base » pour `PURGE OUI`.
Portée honnête du contrôle : `PURGE OUI` s'exécute dans le **navigateur** ; aucun test Python ne peut
l'exécuter. Ce qu'un contrôle peut prouver est la **présence** du libellé au rendu de `SAV-01`
(mesuré : `GET /saves` → 200, statut `N OUVRIR | DEL N | PURGE OUI — ENTREE=VALIDER`) et l'existence
du traitement dans `terminal.js` (lecture du fichier).

### 11. Les écrans web et leur arborescence réelle

| Étape | Libellé rendu (verbatim) | Provenance |
|-------|--------------------------|------------|
| Menu principal | `"5. SYSTEME"` | `dofus_stuff/web/routes.py:197` (écran `MNU-01`, `:189-200`) |
| Menu système | `"4. GESTION DE LA BASE"` | `dofus_stuff/web/routes.py:236` (écran `SYS-01`, `:230-248`) |
| Menu base | `"1. ETAT DE LA BASE (STATUS)"`, `"2. SYNCHRONISATION FORCEE (SYNC)"`, `"3. VIDER LA BASE (CLEAR)"`, `"SELECTIONNEZ UNE OPTION ET APPUYEZ SUR ENTREE :"` | `dofus_stuff/web/routes.py:712-716` (écran `DB-01`, `:709-727`) |
| État de la base | `** ETAT DE LA BASE **` (`DB-02`) | `dofus_stuff/web/routes.py:775` |
| Synchronisation | `** SYNCHRONISATION **` (`DB-03`) | `dofus_stuff/web/routes.py:792` |
| Vider la base | `** VIDER LA BASE **` (`DB-04`) | `dofus_stuff/web/routes.py:847` |
| Sauvegardes | `** STUFFS SAUVEGARDES **` (`SAV-01`) | `dofus_stuff/web/routes.py:1286` |

Ces libellés sont des candidats de citation pour situer l'écran ; la page doit les citer **au rendu**
(seul ancrage, aucune constante publique ne les porte).

### 12. Ce que la page ne peut PAS citer (D-76, D-73, D-75)

| Interdit | Pourquoi | Preuve |
|----------|----------|--------|
| Chemin absolu du poste affiché par l'aide CLI de `--data-dir` | Volatile : dépend de la machine (`f"… (défaut : {DEFAULT_DATA_DIR})"`) | `dofus_stuff/cli.py:39` ; `docs/cli.md:18` a déjà posé la règle |
| Compteurs (`18288` lignes, `equipment: 4356`, …) | Volatils : changent à chaque resynchronisation | mesure lecture seule de la base réelle |
| Version de jeu (`3.6.10.11`) et `last_checked_at` (`1788730056.8426304`) | Volatils | mesure lecture seule de `meta` |
| Âge du dernier contrôle (`il y a 0.0h`) et horloge de l'en-tête d'écran | Volatils (mesuré : `2026-09-11 21:54:13`) | rendu mesuré ; `dofus_stuff/web/routes.py:761`, `header_line` |
| Taille, `mtime`, SHA-256 de `.data/dofus.sqlite3` | Volatils ; servent de **mesure d'intégrité**, jamais de contenu documentaire | mesure d'empreinte (04-SECURITY L-2, § *Validation Architecture*) |
| Clés internes `"path"`, `"total_items"`, `"by_kind"` | Ce ne sont pas des noms de champs affichés (D-76) | `dofus_stuff/database.py:154-161` |
| `weapons` comme catégorie stockée | Sous-type mappé vers `equipment`, pas un kind | `dofus_stuff/catalog.py:12-21` |
| Le texte d'aide de `--force-sync` **recopié ligne à ligne avec la coupure du terminal** | L'aide est coupée à la largeur du terminal (mesuré : 80 colonnes) — c'est un artefact d'affichage, pas une constante | mesure `parse_args(["--help"])` (voir § *Pitfalls*, Pitfall 5) |

### 13. Synthèse : élément citable → valeur → provenance (table que le planificateur recopie)

| # | Élément (ce que la page peut affirmer) | Valeur / libellé verbatim | Provenance |
|---|----------------------------------------|---------------------------|------------|
| 1 | Nom du fichier de la base | `dofus.sqlite3` (`DB_NAME`) | `dofus_stuff/database.py:12` |
| 2 | Répertoire par défaut | `.data/` à la racine du dépôt (`DEFAULT_DATA_DIR`) | `dofus_stuff/database.py:13` |
| 3 | Tables | `meta`, `items` | `dofus_stuff/database.py:44-59` |
| 4 | Index | `idx_items_kind` sur `items (kind)` | `dofus_stuff/database.py:61` |
| 5 | Clés de `meta` | `game_version`, `last_checked_at` | `dofus_stuff/database.py:15-16` |
| 6 | Catégories stockées (7) | `equipment`, `resources`, `consumables`, `quest`, `cosmetics`, `mounts`, `sets` | `dofus_stuff/database.py:18-26` **et** `dofus_stuff/api.py:19-28` (mesurés égaux) |
| 7 | Fenêtre de re-check | `CHECK_INTERVAL_SECONDS = 24 * 60 * 60` | `dofus_stuff/sync.py:11` |
| 8 | Drapeau de forçage | `--force-sync`, aide `Ignorer la fenêtre 24h et forcer une vérif / sync version`, défaut faux | `dofus_stuff/cli.py:41-45` |
| 9 | Défaut web | `--offline` actif par défaut ; `--no-offline` / `--online` le désactivent | `dofus_stuff/web/__main__.py:21-31` |
| 10 | Défaut CLI | `--offline` **absent par défaut** (CLI en ligne) | `dofus_stuff/cli.py:46-50` + mesure `parse_args` |
| 11 | Aide `--offline` (web) | `Ne pas contacter l'API au démarrage (défaut : oui)` | `dofus_stuff/web/__main__.py:25` |
| 12 | Aide `--offline` (CLI) | `Ne pas contacter l'API (échoue si la base locale est vide)` | `dofus_stuff/cli.py:49` |
| 13 | Champs CLI | `Fichier :`, `Version jeu :`, `Dernier check :`, `Entrées :`, `Par catégorie :`, états `(aucune)` / `(aucun)`, ligne `  - {kind} : {count}` | `dofus_stuff/cli.py:216-229` |
| 14 | Champs web | `FICHIER :`, `VERSION JEU :`, `DERNIER CHECK :`, `ENTREES :`, `PAR CATEGORIE :`, états `(aucune)` / `(AUCUN)` | `dofus_stuff/web/routes.py:755-769` |
| 15 | Sous-commandes `db` | `status`, `stats`, `sync`, `fill`, `clear` (aides verbatim § *8*) | `dofus_stuff/cli.py:180-194` |
| 16 | Alias | `stats` → `status`, `fill` → `sync` ; `cache` = second nom de `db` | `dofus_stuff/cli.py:180-188`, `:283-285` |
| 17 | `db status` crée le fichier | `mkdir(parents=True, exist_ok=True)` + `sqlite3.connect(self.path)` | `dofus_stuff/database.py:41-42` ; `dofus_stuff/cli.py:338` |
| 18 | Refus de `db sync --offline` | `Erreur : --offline incompatible avec db sync` | `dofus_stuff/cli.py:346` |
| 19 | Base vide + `--offline` | `Base locale vide et --offline : impossible de synchroniser` | `dofus_stuff/sync.py:43` |
| 20 | Synchro web hors-ligne | `ensure_up_to_date(…, force=True, offline=False, …)` + corps `CETTE OPERATION CONTACTE L'API DOFUSDUDE` | `dofus_stuff/web/routes.py:820-826`, `:794` |
| 21 | `db clear` | aide `Vider la base locale` ; `DELETE FROM items` + `DELETE FROM meta` ; fichier **conservé** | `dofus_stuff/cli.py:189`, `dofus_stuff/database.py:149-150` |
| 22 | Écran destructeur | `OPERATION DESTRUCTIVE` (statut rendu `OPERATION DESTRUCTIVE — ENTREE=VALIDER`) | `dofus_stuff/web/routes.py:858`, `:147-150` |
| 23 | `PURGE OUI` | statut `N OUVRIR | DEL N | PURGE OUI` ; détruit les sauvegardes du navigateur | `dofus_stuff/web/routes.py:1293`, `dofus_stuff/web/static/js/terminal.js:459-466` |

---

## Standard Stack

### Core

| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| Python | `requires-python = ">=3.11"` (`pyproject.toml`) ; **interpréteur mesuré : `./.venv/Scripts/python.exe` → Python 3.14.7** | Rédiger la page et le module d'ancrage | Interpréteur de référence du dépôt (D-15) ; l'interpréteur ambiant n'a pas pytest |
| pytest | `>=8.0` déclaré ; **9.1.1 mesuré** (`./.venv/Scripts/python.exe -m pytest --version`) | Prouver les critères | Déjà configuré (`testpaths`, `pythonpath`), **205 passed in 3.59s** mesuré cette session |
| `flask.Flask.test_client` (Flask ≥ 3.0, déjà dépendance runtime) | via `tests/conftest.py::app` / `client` | Rendre les écrans `DB-01`/`DB-02`/`DB-03`/`DB-04`/`SAV-01` en processus | Aucun serveur, aucune socket, aucune écriture sous `.data/` ; c'est la méthode des phases 3 et 4 (D-32/D-36) |
| stdlib `re`, `pathlib`, `ast`, `hashlib`, `io`, `contextlib` | 3.11+ | Lire les fichiers, extraire des littéraux, capturer une sortie, mesurer une empreinte | Zéro dépendance nouvelle (contrainte CLAUDE.md) ; `ast` est le patron déjà employé en phase 3/4 |

### Supporting

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| `tests/conftest.py` (fixtures `app`, `client`, `docs_dir`, `normalize`, `section`, `sections`, `lignes_de_code`, `lignes_exemple`) | — | Helpers partagés | **Toujours** : D-12 interdit de dupliquer un helper dans un module de test |
| `dofus_stuff.database` (`DB_NAME`, `DEFAULT_DATA_DIR`, `ITEM_KINDS`, `META_GAME_VERSION`, `META_LAST_CHECKED_AT`, `Database`) | — | Lire les constantes publiques et construire une base **temporaire** | Quand la valeur est une constante publique (§ *1*, *2*, *3*) |
| `dofus_stuff.sync.CHECK_INTERVAL_SECONDS` | — | Lire la fenêtre | La page la nomme (D-73) |
| `dofus_stuff.cli.build_parser` / `dofus_stuff.web.__main__.build_parser` | — | Sonder les deux surfaces d'entrée par leur API publique | Pour les défauts et les textes d'aide (§ *5*) |
| `dofus_stuff.cli._print_db_status` | — | Produire la sortie réelle de l'état de la base côté CLI | Pour les cinq libellés CLI, faute de constante publique (§ *7*, § *Feasibility*) |

### Alternatives Considered

| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| Client de test Flask en processus | Lancer `python -m dofus_stuff.web` et interroger un port | Interdit : socket, serveur, hors-ligne ; D-15 interdit aussi d'exécuter `main()` |
| Lire la base **réelle** `.data/dofus.sqlite3` pour prouver les catégories | Base temporaire construite par la fixture `app` (`tmp_path/data`) | La lecture réelle a servi **une fois** en recherche (URI `?mode=ro`) pour confirmer les 7 kinds ; **aucun contrôle de la phase ne l'ouvre** (contrainte CLAUDE.md, D-81) |
| `DB_NAME`/`DEFAULT_DATA_DIR` importés depuis `dofus_stuff.database` | Recopier `"dofus.sqlite3"` / `".data"` dans la page et dans le module | Recopier perd l'ancrage : la page citerait une valeur qu'aucun contrôle ne relie au code (D-75) |
| Sonder les aides par `argparse` **privé** (`_actions`, `parser._subparsers`) | `build_parser().parse_args([... "--help"])` avec `redirect_stdout` | D-14 : l'introspection privée d'`argparse` est interdite ; le rendu de l'aide par `--help` est le chemin **public** déjà employé par `tests/test_docs_cli.py:268-277` |
| Exécuter `main()` pour lire `db status` | Appeler `_print_db_status(db)` sur une base temporaire, ou lire ses littéraux par `ast` | `main()` est **jamais** exécuté dans la suite (règle du dépôt, `tests/test_docs_cli.py:17`) ; les deux routes de remplacement sont mesurées en § *Feasibility* |

**Installation :** aucune. `pyproject.toml` ne change pas ; la phase n'ajoute ni dépendance runtime ni
extra `dev` (D-91).

## Package Legitimacy Audit

**Non applicable — cette phase n'installe aucun paquet externe.**

- Evidence : le chemin de vérification du projet est `pytest` + bibliothèque standard (contrainte
  CLAUDE.md « pas de nouvelle dépendance pour la documentation ») ; la phase ne modifie ni
  `pyproject.toml` ni `.venv` ; aucun `pip install` n'est exécuté.
- Les seuls outils utilisés sont **déjà présents et mesurés** : `.venv/Scripts/python.exe` (3.14.7),
  pytest 9.1.1, git 2.55.0.windows.4 (`core.autocrlf=true`).
- Aucun paquet découvert par recherche Web n'est recommandé : aucune recherche Web n'a été nécessaire,
  la matière est intégralement dans le dépôt.

**Packages removed due to [SLOP] verdict:** none — aucun paquet n'a été proposé.
**Packages flagged as suspicious [SUS]:** none.

## Architecture Patterns

### System Architecture Diagram

Deux flux traversent cette phase : le flux **produit** (ce que le lecteur vit, qui définit ce que la
page doit décrire) et le flux **de preuve** (ce que le harnais contrôle).

```
                 FLUX PRODUIT (source de vérité, jamais modifié par la phase)

  Lecteur CLI                          Lecteur web
    │ `fetcher.py [--offline] <cmd>`     │ `python -m dofus_stuff.web [--offline|--online]`
    ▼                                    ▼
  build_parser() (cli.py:33-196)       build_parser() (web/__main__.py:13-36)
    │ args.offline défaut False          │ args.offline défaut True
    ▼                                    │ offline = False if args.online else args.offline
  main()  ── commande db/cache ─┐        ▼
    │                           │      create_app(data_dir, offline)  (web/__init__.py:27-66)
    │                           │        │ web_config["offline"] = résolu
    │                           ▼        ▼
    │                  Database(data_dir)   reload_catalog(app)  (web/__init__.py:92-119)
    │                  db.open()              │ skip_sync = offline and not force_sync
    │                  → mkdir + connect      │
    │                  → CREATE TABLE meta/items│
    │                           │             ▼
    │                           │        Catalog.load(skip_sync=True)   (catalog.py:33-56)
    │                           │             │  if not skip_sync: ────┐
    ▼                           │             ▼                     │
  Catalog.load(offline=…)  ─────┤        items en mémoire           │
    │ if not skip_sync:         │             │                     │
    ▼                           │             ▼                     ▼
  ensure_up_to_date(db, offline=…, force=…)   écrans web       ensure_up_to_date
    │ needs_check = force or empty or          GET /db/status    (CLI uniquement)
    │   last_checked is None or (now-last)>=24h  GET /db/sync
    │                                                                │
    ├─ not needs_check → skip/within_24h  (AUCUN réseau)             │
    ├─ offline → vide : RuntimeError  /  sinon skip/offline          │
    └─ besoin de réseau ─────────────────────────────────────────► API Dofusdude
                                                      ▲
                                     POST /db/sync ───┘  (routes.py:820-826 : offline=False EN DUR)
                                     db sync (sans --offline) ──────┘  (cli.py:348-354)

                 FLUX DE PREUVE (phase 5, hors ligne, sans main())

  tests/test_docs_base_locale.py
    │ réutilise les fixtures de tests/conftest.py (app, client, docs_dir, normalize, …)
    ├─ lit les constantes publiques  : ITEM_KINDS, DB_NAME, CHECK_INTERVAL_SECONDS, META_*
    ├─ sonde les deux parseurs       : parse_args([...]) et parse_args([... "--help"])
    ├─ rend /db, /db/status, /db/sync, /db/clear, /saves via le client de test  (GET seulement)
    ├─ capture la sortie de _print_db_status sur une base tmp_path
    └─ lit docs/base-locale.md et compare chaque valeur citée
         │
         ├─ générateur de constats (page + valeur fautive + valeur attendue + fichier producteur)
         └─ une seule assertion agrégée (convention héritée des phases 3 et 4)
```

### Recommended Project Structure

```
docs/
├── base-locale.md          # NOUVELLE page, source unique du sujet (D-68)
├── sommaire.md             # MODIFIÉ : une seule ligne d'index (D-70)
├── installation.md         # voisine : premier contact + démarrage web (inchangée)
├── cli.md                  # voisine : surface de commandes (inchangée ; elle porte déjà db clear)
├── parcours-simplifie.md   # voisine : écran SAV-01 et PURGE OUI (inchangée ou un seul lien)
└── wizard-avance.md        # voisine (inchangée)

tests/
├── conftest.py             # fixtures partagées : réutilisées, jamais recopiées (D-12)
├── test_docs_base_locale.py  # NOUVEAU module d'ancrage (D-82)
├── test_docs_structure.py  # gardes d'index / H1 / retour / encodage : INCHANGÉES
├── test_docs_parcours.py   # À MODIFIER : PAGES_INEXISTANTES (« base-locale.md ») — sinon ROUGE
└── test_docs_wizard.py     # patron de la garde ast et de l'empreinte (inchangé)
```

### Pattern 1: Une valeur citée = une valeur lue (jamais écrite de mémoire)

**What:** chaque nom, drapeau ou libellé que la page affirme est comparé à ce que le code produit —
constante publique importée, aide rendue par `--help`, corps d'écran rendu, sortie capturée.
**When to use:** pour **chaque** valeur de la § *Measured inventory*.
**Example:**

```python
# Source : tests/conftest.py::app (fixture existante) + patron tests/test_docs_wizard.py
from dofus_stuff.database import DB_NAME, ITEM_KINDS   # constantes publiques (D-14)
from dofus_stuff.sync import CHECK_INTERVAL_SECONDS

# Le nom du fichier est produit par le code, pas recopié : le contrôle compare la page au code.
assert DB_NAME == "dofus.sqlite3"          # mesuré cette session
assert CHECK_INTERVAL_SECONDS == 24 * 60 * 60

# Les libellés CLI se lisent à la SORTIE RÉELLE de la fonction qui les produit :
import io
from contextlib import redirect_stdout
from dofus_stuff.cli import _print_db_status
from dofus_stuff.database import Database

db = Database(data_dir=tmp_path / "data")   # JAMAIS DEFAULT_DATA_DIR (D-81)
tampon = io.StringIO()
with redirect_stdout(tampon):
    _print_db_status(db)                    # crée le fichier temporaire, n'ouvre aucun réseau
lignes = tampon.getvalue().splitlines()
```

### Pattern 2: Les champs d'un écran se lisent au **corps rendu**, jamais dans la réponse entière

**What:** extraire le corps entre `id="body">` et `<div class="row status`, ligne par ligne, puis
comparer.
**When to look:** pour `DB-01`, `DB-02`, `DB-03`, `DB-04`, `SAV-01`.
**Example (repris verbatim du patron, `tests/test_docs_wizard.py:355-356`) :**

```python
# Source : tests/test_docs_wizard.py:91-94 et :353-356 (marqueurs déjà employés par la phase 4)
MARQUEUR_CORPS = 'id="body">'
MARQUEUR_STATUT = '<div class="row status'
LIGNE_CORPS = re.compile(r'<div class="row">(.*?)</div>', re.S)

def _lignes_du_corps(reponse) -> list[str]:
    texte = reponse.get_data(as_text=True)
    corps = texte.split(MARQUEUR_CORPS, 1)[1].split(MARQUEUR_STATUT, 1)[0]
    return [ligne.rstrip() for ligne in LIGNE_CORPS.findall(corps)]
```

Mesure de cette session sur un client de test, base `tmp_path` non vide :

```
GET /db/status  →  200
CORPS| FICHIER : …\data\dofus.sqlite3
CORPS| VERSION JEU : 9.9.9.9
CORPS| DERNIER CHECK : IL Y A 0.0H
CORPS| ENTREES : 3
CORPS| PAR CATEGORIE :
CORPS|   - equipment : 2
CORPS|   - resources : 1
```

### Pattern 3: Constats accumulés, une seule assertion (convention héritée)

**What:** collecter les écarts dans `constats: list[str]`, puis une assertion finale qui les joint ;
chaque constat nomme la page, la valeur fautive, la valeur attendue et le fichier producteur (D-13,
D-83).
**When to use:** partout ; c'est ce qui rend la sortie de `pytest` exploitable sans lecture du module.

### Pattern 4: Garde `ast` de clôture du module — **réécrite** pour cette phase

**What:** vérifier sur le texte du module, par `ast`, que le harnais ne peut pas (§ *Pitfalls*
Pitfall 1) : exécuter le produit, ouvrir une session, supprimer un fichier, **confirmer** une action
destructrice ou réseau.
**Difference from phase 4:** la phase 4 interdit l'import de `dofus_stuff.database`
(`MODULE_BASE_INTERDIT`, `tests/test_docs_wizard.py:326`). **Cette phase-ci en a besoin** : c'est la
source de `DB_NAME`, `ITEM_KINDS` et `Database`. La garde doit donc **déplacer le risque** : interdire
l'usage de `DEFAULT_DATA_DIR` comme `data_dir`, et interdire la **paire de confirmation**
`{"confirm": …}` (analogue à la paire `{"cmd": "GO"}` que la phase 4 refuse).
**Example:**

```python
# Source : adapté de tests/test_docs_wizard.py:311-330, :937-965 et de la paire "cmd"/"GO" (:968-980)
RACINES_INTERDITES = (              # conserve tel quel : base, processus, socket, reseau
    "sqlite3", "subprocess", "socket", "multiprocessing", "ctypes",
    "webbrowser", "urllib", "requests", "http", "ftplib", "smtplib",
)
APPELS_SUPPRESSION = ("remove", "unlink", "rmdir", "rmtree")
APPEL_PRODUIT = "main"              # jamais appele
CONFIRMATIONS_INTERDITES = ("O", "Y", "OUI", "YES")   # ce que routes.py:810 accepte
# dofus_stuff.database N'EST PLUS interdit : DB_NAME, ITEM_KINDS, Database sont la matiere de la page.
```

### Anti-Patterns to Avoid

- **Recopier un libellé « de mémoire » ou depuis un autre document** : la page citerait une seconde
  source d'un énoncé que le code produit (D-17, D-19). Tout vient de la § *Measured inventory*.
- **Ouvrir `.data/dofus.sqlite3` dans un contrôle** (même en lecture, même pour « vérifier » un nom) :
  interdit par CLAUDE.md et par D-81. La lecture réelle de cette session est une **mesure de
  recherche**, jamais un contrôle.
- **Uniformiser les deux surfaces** : `Entrées :` ≠ `ENTREES :`, `(aucun)` ≠ `(AUCUN)`. Lisser ces
  écarts rendrait la page fausse sur une surface.
- **Faire passer les deux « hors-ligne » pour un seul comportement** : mesuré, ils diffèrent (le web
  saute la vérification, la CLI la fait puis refuse).
- **Présenter `PURGE OUI` comme une commande qui vide la base** : mesuré, il vide `localStorage`.
- **Poster `/db/sync` ou `/db/clear` avec une confirmation** dans un contrôle : réseau et destruction,
  même sur une base temporaire (D-81). L'écran se lit en `GET`.
- **Recopier une aide `--help` avec ses coupures de ligne** : la largeur dépend du terminal (mesuré
  80 colonnes). Toute comparaison d'aide doit normaliser les espaces.

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Construire une base locale de test | Un `sqlite3.connect` à la main, un `mkdir` sous `.data/`, un dump SQL | La fixture `app` de `tests/conftest.py:84-111` construit `tmp_path/data` avec `Database` + `replace_kind` + `set_meta("game_version", …)` | La fixture isole déjà la base, pose les kinds `equipment` et `resources` et neutralise le catalogue ; c'est ce que les phases 3 et 4 utilisent |
| Rendre un écran web sans serveur | `subprocess`, `requests`, `app.run()` | `app.test_client()` (fixture `client`, `tests/conftest.py:115-116`) | En processus, sans socket, sans port ; c'est le patron D-32/D-36 |
| Lire une aide de parseur | Parser la source à la main, utiliser `argparse._actions` | `build_parser().parse_args([..., "--help"])` sous `redirect_stdout` (patron `tests/test_docs_cli.py:268-277`) ou `format_help()` | API publique, rendu réel ; D-14 interdit l'introspection privée d'`argparse` |
| Extraire une valeur littérale du code | Recopier la chaîne, ou exécuter la fonction pour la lire | Import de la constante publique ; sinon `ast` (patron `tests/test_docs_parcours.py:1124-1140`) | `ast` lit les littéraux d'une fonction **sans l'exécuter** : mesuré, `ast` retrouve `DELETE FROM items` / `DELETE FROM meta` dans `Database.clear` et les cinq libellés dans `_print_db_status` |
| Mesurer que `.data/` n'a pas bougé | Comparer les tailles à la main, mtime seul | L'empreinte `(taille, mtime_ns, sha256)` de la phase 3/4, **reprise verbatim** (`tests/test_docs_wizard.py:826-833`) | Trois composantes : un écart dit **laquelle** a bougé ; lecture seule, `skip` nommé si la base est absente |
| Normaliser accents/casse/espaces pour comparer | Réécrire un normaliseur | La fixture `normalize` (`tests/conftest.py:119-136`) | D-11/D-12 : un helper dupliqué finit par diverger |

**Key insight:** tout ce que cette phase doit prouver a **déjà** un outil dans le dépôt — fixtures,
patron de constats, garde `ast`, empreinte, normalisation. La valeur ajoutée de la phase n'est pas un
outillage nouveau, c'est la **matière mesurée** et la **réécriture de la garde `ast`** pour un module
qui, lui, doit légitimement lire `dofus_stuff.database`.

---

## Feasibility verdict: comment chaque valeur citée peut être ancrée (question G)

**Question posée :** comment le module peut-il prouver que chaque nom cité est produit par le code,
**sans toucher `.data/`** et **sans appel réseau** ? Verdict par mécanisme, avec ce qu'il prouve et ce
qu'il ne prouve pas.

| # | Mécanisme | Vue mesurée cette session | Ce qu'il **prouve** | Ce qu'il **ne prouve pas** |
|---|-----------|---------------------------|---------------------|----------------------------|
| 1 | **Import d'une constante publique** (`dofus_stuff.database.DB_NAME`, `ITEM_KINDS`, `META_GAME_VERSION`, `META_LAST_CHECKED_AT` ; `dofus_stuff.sync.CHECK_INTERVAL_SECONDS`) | `DB_NAME='dofus.sqlite3'`, `ITEM_KINDS=('equipment', …, 'sets')`, `CHECK_INTERVAL_SECONDS=86400` | Que la valeur citée **est** celle du code, **au moment du test** : un renommage ou une valeur différente fait rougir | Rien de la **page** : un import seul ne dit pas que la page cite la même valeur — il faut la comparaison page ↔ constante |
| 2 | **Aide d'un parseur rendue en processus** — CLI : `build_parser().parse_args([... , "--help"])` sous `redirect_stdout` (lève `SystemExit(0)`) ; web : `build_parser().format_help()` (ne lève rien) | `parse_args(["--help"]) → SystemExit 0` ; l'aide CLI contient `--force-sync`, `--offline` ; l'aide web contient `--offline, --no-offline` + `Ne pas contacter l'API au démarrage (défaut : oui)` | Que le drapeau **existe** (une sonde `parse_args` d'un argv complet échoue si l'option est renommée) et que le texte d'aide rendu **contient** la phrase citée | Que la **forme stricte** d'un jeton soit respectée : `argparse` accepte un préfixe non ambigu (limite **déjà mesurée** en phase 2, `tests/test_docs_cli.py:19-27`, WR-05) ; et non la sensibilité aux accents/casse si l'on compare avec `normalize` |
| 3 | **Défauts des parseurs** : `parse_args([])` (web) et `parse_args(["db","status"])` (CLI) | web `offline=True` ; CLI `offline=False` | Le **défaut** de chaque surface, chiffré : c'est la preuve directe du critère 2 | Que la page décrive ce défaut **là où il s'applique** : un contrôle doit exiger que la phrase web soit dans la section web et la phrase CLI dans la section CLI (ou dans son bloc) |
| 4 | **Rendu Flask en processus** (`client` de la fixture `app`) sur `tmp_path` | `GET /db/status` → 200 avec `FICHIER :`… ; `GET /db/clear` → 200 avec `ATTENTION : …` ; `GET /saves` → 200 avec `N OUVRIR \| DEL N \| PURGE OUI — ENTREE=VALIDER` | Que le libellé **est rendu** par le produit, exactement, y compris la composition de la ligne de statut (`routes.py:143-150`) | Rien du **JavaScript** : `PURGE OUI` s'exécute dans le navigateur (`terminal.js:459-466`) ; le rendu ne prouve que le libellé. Ne prouve pas non plus le clavier réel (aucun navigateur) |
| 5 | **Sortie capturée de `_print_db_status`** sur un `Database(tmp_path/…)` | `Fichier : …`, `Version jeu : (aucune)`, `Dernier check : (aucun)`, `Entrées : 0`, et sur base non vide `Par catégorie :` + `  - equipment : 2` | Que ces cinq libellés CLI **sont produits** par la fonction que `db status` appelle (`cli.py:341`), et l'effet de bord documenté : un répertoire inexistant devient dossier + fichier (mesuré) | Que `main()` les affiche tels quels (chemin `main` non parcouru) ; c'est un **écart déclaré**, couvert par le fait que `db status` appelle cette fonction en un seul point (`cli.py:340-342`) |
| 6 | **Littéraux lus par `ast`** (sans exécution) — `Database.clear`, `_print_db_status`, la chaîne de refus de `cli.py:346` | `ast` retrouve `['DELETE FROM items', 'DELETE FROM meta']` dans `clear` ; les littéraux des cinq libellés dans `_print_db_status` ; `'Erreur : --offline incompatible avec db sync'` à `cli.py:346` | Qu'une chaîne **est écrite dans le fichier producteur**, sans exécuter quoi que ce soit (utile pour `SET`/`DELETE`, ou si l'on refuse d'importer un nom privé) | Qu'elle soit **rendue** : `ast` lit un littéral, pas un affichage. Contrôle plus faible que 4 ou 5, à n'employer que là où l'exécution est interdite (`db clear`) |
| 7 | **Lit de la source** (`read_text`) pour `terminal.js`, `routes.py`, `cli.py` | `if (upper === "PURGE OUI") { … localStorage.removeItem(SAVES_KEY); … }` | Qu'un **fait présent dans le fichier** y est encore (ex. : `PURGE OUI` agit sur `localStorage`) | Rien de dynamique : ni exécution, ni compilation du JS |

**Verdict.** L'ancrage est **faisable sur les cinq critères**, avec **trois** mécanismes principaux :
constante publique (1) pour le fichier, les catégories et la fenêtre ; **aide + défauts des parseurs**
(2)(3) pour les deux défauts hors-ligne ; **rendu** (4)(5) pour les champs de l'état de la base et les
écrans, `lecture de source`/`ast` (6)(7) là où l'exécution est interdite ou impossible
(`PURGE OUI`, `DELETE`).

**Recommandation de mécanisme par valeur :**

| Valeur citée | Mécanisme recommandé | Raison |
|--------------|----------------------|--------|
| `dofus.sqlite3`, les 7 catégories, `CHECK_INTERVAL_SECONDS` | Import de constante publique + comparaison à la page | Le plus fort : la page et le code partagent la même source |
| `--offline` / `--force-sync` / `--online` (existence et texte d'aide) | Aide rendue (`--help` CLI, `format_help()` web) + sonde `parse_args` d'un argv complet | Le seul chemin **public** (D-14) ; la sonde attrape un renommage |
| Le **défaut** de chaque surface | `parse_args` sans le drapeau | Prouve le « par défaut » du critère 2 |
| Les 5 champs CLI | **Sortie capturée** de `_print_db_status` (mécanisme 5) ; repli `ast` (6) si le plan refuse un nom privé | CLAUDE.md §4.3 nomme ce point d'ancrage ; l'`ast` reste un contrôle plus faible |
| Les 5 champs web + les libellés d'écran | **Rendu** (4) | Seul ancrage observable ; aucune constante ne les porte |
| Le refus de `db sync --offline` | `ast` sur `cli.py` **et** comparaison du littéral à la phrase citée par la page | `main()` n'est pas exécuté ; le littéral est la source du message |
| `db clear` / `DELETE FROM items` / `DELETE FROM meta` | `ast` sur `database.py::clear` | **Interdit d'exécuter** (D-81) ; `ast` prouve l'effet écrit |
| `PURGE OUI` (libellé + effet) | Rendu (4) **et** lecture de `terminal.js` (7) | L'effet est du JavaScript : aucun contrôle Python ne l'exécute |
| Création du fichier par `db status` | Exécution **sur `tmp_path`** (mécanismes 4 et 5) | Mesure la création sans approcher `.data/` |

**La chose à ne JAMAIS faire par un contrôle (énoncé explicite) :** créer, ouvrir en écriture, ou vider
la **base réelle** `.data/dofus.sqlite3` — c'est-à-dire : ne pas appeler `db clear` (ni le POST
`/db/clear` avec confirmation), ne pas appeler `main()`, ne pas passer `DEFAULT_DATA_DIR` à `Database`,
ne pas poster `/db/sync` avec confirmation, ne pas ouvrir de socket. Les seules opérations admises sur
`.data/` sont la **lecture d'octets** pour l'empreinte et de la **comparer** à elle-même. Rappel de
confort : `Database()` sans argument lève `TypeError: Database.__init__() missing 1 required positional
argument: 'data_dir'` (mesuré) — l'accident « base réelle par omission » est donc impossible ;
l'accident possible est `Database(data_dir=DEFAULT_DATA_DIR)` ou `Catalog.load()` (qui retombe sur
`data_dir or DEFAULT_DATA_DIR`, `catalog.py:43`).

**Deux interprétations d'une chaîne à surveiller :** `PURGE OUI` est un **libellé d'écran** rendu par
`SAV-01` ; aucun contrôle ne peut prouver qu'un clic a eu lieu. La page dit donc ce que le code
**déclare** (le libellé et le traitement JS), et le module déclare cette limite (D-85).

---

## Common Pitfalls

### Pitfall 1: `PAGES_INEXISTANTES` fait rougir la suite dès que la page existe

**What goes wrong:** `tests/test_docs_parcours.py:2327` déclare
`PAGES_INEXISTANTES = ("base-locale.md",)` ; le contrôle `test_lien_wizard_avance_legitime`
(`:2882`) refuse qu'une réserve déclare inexistante une page **présente** et constate :
`la réserve declare « base-locale.md » inexistante alors que la page existe (…) ; attendu une reserve
reduite a ce qui n'existe pas`.
**Why it happens:** la dette D-44/D-63 a été laissée « visible par construction » (commentaire
`tests/test_docs_parcours.py:2322-2326`, docstring `:2886`, `:2890`) ; elle se paie à la phase qui crée
la page.
**How to avoid:** le plan doit **nommer** la modification de `tests/test_docs_parcours.py` dans le même
commit que la création de `docs/base-locale.md` (le patron établi par la phase 4 pour
`wizard-avance.md`), c'est-à-dire vider la réserve ou la remplacer par ce qui reste réellement
inexistant.
**Warning signs:** la suite passait 205 tests avant l'ajout de la page et rougit **sur un seul** test
qui ne parle pas de la base locale.

### Pitfall 2: La garde `ast` de la phase 4 interdit précisément l'import dont cette phase a besoin

**What goes wrong:** recopier `MODULE_BASE_INTERDIT = "dofus_stuff.database"`
(`tests/test_docs_wizard.py:326`) et son contrôle (`:949-955`) ferait **rougir** le nouveau module qui
doit lire `DB_NAME`, `ITEM_KINDS` et `Database`.
**Why it happens:** la garde a été écrite pour un module dont le sujet était le wizard, pas la base ;
son nom dit le **risque** (tirer la base locale), pas le module.
**How to avoid:** déplacer le risque : garder `RACINES_INTERDITES` (base/processus/socket/réseau) et
`APPELS_SUPPRESSION`/`APPEL_PRODUIT`, et ajouter les interdits **propres** à cette phase : aucune
confirmation (`"confirm"` → `"O" | "Y" | "OUI" | "YES"`), et `data_dir` jamais `DEFAULT_DATA_DIR`.
**Warning signs:** un constat qui dit « import de `dofus_stuff.database` » sur un module dont le sujet
**est** la base locale — signe d'une garde recopiée sans réécriture.

### Pitfall 3: `PAR CATEGORIE` / `Par catégorie :` n'apparaît que si des objets existent

**What goes wrong:** un contrôle qui exige la ligne `PAR CATEGORIE :` sur la fixture telle qu'elle est
rendue pour un écran vide échoue, ou pire : un contrôle qui l'exige sur une base vide **passe** grâce
à une recherche laxiste dans la page.
**Why it happens:** la ligne est conditionnelle des **deux** côtés :
`if isinstance(by_kind, dict) and by_kind:` (`cli.py:226`, `routes.py:766`).
**How to avoid:** rendre `/db/status` sur une base **non vide** (la fixture `app` pose `equipment` et
`resources`, `tests/conftest.py:91-99`) et prouver la condition : présence avec des objets, absence
sans.
**Warning signs:** une assertion qui ne distingue pas « champ présent » de « champ présent parce que la
base est peuplée ».

### Pitfall 4: Les deux surfaces ne portent pas les mêmes chaînes

**What goes wrong:** écrire une seule phrase « l'état de la base affiche `Entrées :` » et la faire
vérifier sur le rendu web : `ENTREES :` (sans accent) ne contient pas `Entrées :` ; inversement, une
page qui n'écrirait que la forme web rendrait la sortie CLI non documentée.
**Why it happens:** la CLI et le web ont deux littéraux distincts (`cli.py:224` vs `routes.py:764`),
et la normalisation D-11 (accents/casse ignorés) **masquerait** la différence si elle est appliquée.
**How to avoid:** citer **les deux** formes en nommant la surface (D-71 appliqué aux champs), et
comparer la forme **exacte** pour les libellés (réserver `normalize` aux libellés d'écran en capitales,
comme le font les phases 3/4 pour les libellés rendus).
**Warning signs:** un contrôle qui normalise avant de comparer `Entrées :` — il ne verrait pas un
`ENTREES :` fautif dans la section CLI.

### Pitfall 5: Une aide `--help` est coupée à la largeur du terminal

**What goes wrong:** exiger dans la page ou dans le contrôle la phrase d'aide `--force-sync` **en une
seule chaîne** échoue sur une page **correcte** : mesuré,
`"Ignorer la fenêtre 24h et forcer une vérif / sync version" in aide_cli.replace("\n", " ")` → **False**
(l'aide est coupée après `vérif / sync` puis reprend après 24 espaces), tandis que la même phrase est
trouvée après `re.sub(r"\s+", " ", …)` → **True**.
**Why it happens:** `argparse` formate selon `shutil.get_terminal_size()` (mesuré : 80 colonnes,
`COLUMNS` absent de l'environnement).
**How to avoid:** normaliser les espaces **avant** toute comparaison d'aide (`re.sub(r"\s+", " ", …)`),
et déclarer la tolérance qui en résulte (une aide citée avec des espaces fautifs passerait).
**Warning signs:** un contrôle d'aide qui rougit sur une phrase pourtant présente dans le code.

### Pitfall 6: `GET /db/sync` est sûr, `POST /db/sync` ne l'est pas

**What goes wrong:** cliquer « pour voir » sur l'écran de synchronisation — un `POST` avec une
confirmation déclenche `ensure_up_to_date(force=True, offline=False, …)` (`routes.py:820-826`), donc le
réseau **et** une écriture dans la base configurée.
**Why it happens:** l'écran est un formulaire ; la `GET` rend la confirmation, la `POST` agit.
**How to avoid:** ne rendre que des `GET` ; si le plan veut couvrir « la confirmation annule », poster
une valeur **non confirmante** (`"N"`) — mesuré : `POST /db/sync` avec `confirm=N` → `302 /db`, aucun
réseau (`routes.py:809-812` renvoie avant l'appel).
**Warning signs:** un `client.post("/db/sync", data={"confirm": "O"})` dans le nouveau module.

### Pitfall 7: `PURGE OUI` n'est pas `db clear`, et son effet n'est pas mesurable en Python

**What goes wrong:** écrire que `PURGE OUI` « vide la base locale » — faux : mesuré, il exécute
`localStorage.removeItem(SAVES_KEY)` (`terminal.js:459-466`), donc il efface des **sauvegardes de
navigateur**. Inversement : prétendre qu'un test « prouve » la purge.
**Why it happens:** le critère 4 du ROADMAP range les deux sous « commandes destructrices de la
base », et `docs/parcours-simplifie.md:174` décrit la commande sans la qualifier de destructrice.
**How to avoid:** signaler les deux (D-80) **et dire ce que chacune détruit** ; ancrer `PURGE OUI` sur
le rendu `SAV-01` + la lecture de `terminal.js` ; déclarer la limite (aucun navigateur).
**Warning signs:** une phrase de la page qui confond les deux cibles.

### Pitfall 8: Une commande destructrice est déjà présentée comme une étape — dans `README.md`

**What goes wrong:** le critique 4 dit « n'apparaissent dans aucun parcours » ; `README.md:80` porte
`python fetcher.py db clear           # vider la base` dans un bloc de commandes, sans avertissement,
alors que la même commande est proprement encadrée dans `docs/cli.md:174-178`.
**Why it happens:** le README est antérieur à la convention ; D-87 ne demande, pour le README, que la
résolution de ses renvois.
**How to avoid:** **délimiter le critère 4 explicitement au périmètre de la phase** (la page et son
module), comme D-87 l'a fait pour le README ; consigner l'observation pour la phase 6 (propriétaire de
la complétude).
**Warning signs:** une vérification de phase qui applique le critère 4 à `README.md` et déclare la
phase incomplète **pour un fichier que la phase n'a pas mandat de réécrire**.

### Pitfall 9: `tests/test_docs_structure.py` interdit `PURGE` dans `docs/installation.md`

**What goes wrong:** en « améliorant » `docs/installation.md` pour y parler des commandes
destructrices, on casse `test_no_destructive_command_in_installation` : `JETON_PURGE = "PURGE"` doit
être **absent** de cette page, et `\bdb\s+clear\b` aussi
(`tests/test_docs_structure.py:20-21`, `:283-301`).
**Why it happens:** la garde existe depuis la phase 1 (T-01-05) et ne concerne **que**
`installation.md`.
**How to avoid:** ne pas toucher au propos de `docs/installation.md` ; la nouvelle page est le bon
endroit pour ces mentions (et la garde ne la couvre pas).
**Warning signs:** un plan qui « ajoute un avertissement destructeur » dans la page d'installation.

### Pitfall 10: La mesure d'empreinte locale est vraie par construction, et deux modules la portent déjà

**What goes wrong:** revendiquer que le contrôle d'empreinte « prouve qu'aucun test n'écrit sous
`.data/` ». C'est **plus faible** : `tests/conftest.py` construit sa base sous `tmp_path/data`, donc le
test local compare le fichier du dépôt à lui-même pendant les rendus **de ce module** ; il ne peut pas
détecter une écriture faite par un autre module, et il **saute** (`pytest.skip(MOTIF_BASE_ABSENTE)`) sur
une copie sans base. C'est la limite **L-2** de `04-SECURITY.md:59-60`, écrite pour ne pas être relue
comme une preuve plus large.
**Why it happens:** deux modules (`tests/test_docs_parcours.py:2557+`, `tests/test_docs_wizard.py:2289+`)
portent **la même** mesure, chacun avec sa copie de `_empreinte` — convention assumée (04-PATTERNS:530,
« verbatim »), donc la phase 5 en ajoute une **troisième**.
**How to avoid:** reprendre l'`_empreinte` **verbatim**, garder le `skip` nommé, écrire la limite dans
la docstring, et laisser la preuve au périmètre de la suite entière (mesure avant/après `pytest -q`,
faite par la vérification de plan — mesurée cette session : identique).
**Warning signs:** une docstring qui revendique « rien n'écrit sous `.data/` » sans nommer la limite.

### Pitfall 11: Le contrôle CRLF dépend de `core.autocrlf` (limite AR-5, non résolue)

**What goes wrong:** sur un clone sans conversion, une page correcte rédigée en LF rougirait.
**Why it happens:** `git config core.autocrlf` mesuré `true` sur ce poste ; aucun `.gitattributes`
n'existe (vérifié) ; la convention CRLF est **verrouillée** (D-67, D-69).
**How to avoid:** suivre la convention et l'assertion du patron (comme les phases 3 et 4), et **ne pas**
présenter l'assertion comme portable. Mesure de cette session : **tous** les fichiers `docs/*.md`,
`tests/*.py`, `README.md`, `GUIDE_WIZARD.md` et `dofus_stuff/web/*.py` sont **100 % CRLF, sans BOM**
(0 fin de ligne LF seule, 0 BOM ; voir § *File conventions*).
**Warning signs:** un plan qui « simplifie » l'assertion de fin de ligne ou qui ajoute un
`.gitattributes` (hors périmètre).

---

## Runtime State Inventory

> **Non applicable au sens du gabarit** : cette phase n'est ni un renommage, ni une refactorisation,
> ni une migration. Le tableau ci-dessous est conservé et rempli **explicitement**, pour répondre à la
> question canonique — *après mise à jour de tous les fichiers du dépôt, quel système d'exécution porte
> encore l'ancien état ?* — qui, ici, se pose autrement : **quel état le harnais doit-il laisser
> intact ?**

| Catégorie | Éléments trouvés | Action requise |
|-----------|------------------|----------------|
| Données stockées | `.data/dofus.sqlite3` — **base réelle du dépôt**, présente, 18 288 lignes, 7 kinds (mesuré en lecture seule). `meta` porte `game_version` et `last_checked_at` | **Aucune** : aucune écriture, aucune suppression, aucun `drop`, aucun `db clear`. Empreinte mesurée avant/après la suite entière (§ *Validation Architecture*) |
| Configuration de service vivant | Aucun service externe ne stocke d'état du projet (l'API Dofusdude est en lecture ; aucune configuration distante) | Aucune |
| État enregistré dans l'OS | Tâches planifiées, services, `pm2`, `launchd`, `systemd` : **aucun** (vérifié : le dépôt n'en déclare aucun ; `pyproject.toml` n'expose que deux points d'entrée console) | Aucune |
| Secrets et variables d'environnement | Lues par le produit : `DOFUS_DATA_DIR`, `DOFUS_OFFLINE`, `DOFUS_TIMEOUT` (`web/__init__.py:43-54`), `DOFUS_SECRET_KEY` (`web/__init__.py:41`). **Aucune page ne doit citer `DOFUS_SECRET_KEY`** (aucune ne le fait : mesuré, 0 occurrence dans `docs/` et `README.md`) | Aucune : la page peut citer `DOFUS_DATA_DIR`/`DOFUS_OFFLINE` **seulement** si elle dit qui les lit (§ *5*) |
| Artefacts de build | `dofus_stuff_machine.egg-info/` (install éditable) ; `.pytest_cache/` ; `tests/__pycache__/` | Aucune : la phase n'installe rien et ne modifie pas `pyproject.toml` |
| État non versionné à ne pas toucher | `.doc-agent/`, `doc-agent.toml`, `gsd-auto*.toml`, `.gsd-tmp/` (mes sondes), `.planning/state.json` | **Aucune suppression, aucune indexation** (D-89, D-91) |

## D-17 — Une seule source par énoncé : les doublons déjà présents (question H)

Chaque ligne ci-dessous est un **énoncé que la phase 5 doit posséder** (D-68) mais qui **existe déjà**
ailleurs dans la documentation livrée. Le planificateur doit décider, pour chacune, entre : (a) laisser
le voisin tel quel et faire de la nouvelle page la source détaillée, (b) convertir le renvoi du voisin
en **lien** vers la nouvelle page (D-86 : seulement là où la cible existe — elle existera).

| # | Énoncé | Occurrence existante (verbatim, avec provenance) | Recommandation |
|---|--------|---------------------------------------------------|----------------|
| 1 | Le fichier et les 7 catégories | `README.md:13` : « Une copie complète de la DB (équipements, ressources, consommables, quêtes, cosmétiques, montures, panoplies) est stockée en SQLite dans `.data/dofus.sqlite3`. » | Laisser le README (D-87 : le README n'est pas réécrit au-delà de ses renvois). La page devient la source des catégories **avec leur nom de code** |
| 2 | La fenêtre de 24 h | `README.md:13` : « Au chargement, si le dernier check date de plus de 24h, la version API est re-testée et la base resynchronisée si elle a changé. » | Idem : la page est la source détaillée |
| 3 | La fenêtre de 24 h (mention courte) | `docs/cli.md:15` : `| ` + "`--force-sync`" + ` | ignorer la fenêtre 24 h et forcer une vérification / synchronisation de version | faux |` | Laisser : c'est la ligne d'option **de la page CLI**, dont le propriétaire est `docs/cli.md` (D-37) |
| 4 | Le renvoi explicite (le « signpost » déjà posé) | `docs/cli.md:26` : « Le détail de la fenêtre de 24 h et de la resynchronisation est traité avec la base locale. » | **À convertir en lien** vers `base-locale.md` par le plan (c'est la dette inverse de D-63 : la cible existe désormais) |
| 5 | Le refus `--offline` + `db sync` (message cité **deux fois**) | `docs/cli.md:26-29` et `docs/cli.md:168-171` : `Erreur : --offline incompatible avec db sync` | D-78 **exige** que la nouvelle page cite le message réel : c'est une duplication **prescrite par une décision verrouillée**, à consigner comme telle (le plan doit pouvoir la justifier) |
| 6 | `db clear` destructeur | `docs/cli.md:174-178` : « Les commandes destructrices `db clear` et `cache clear` vident **entièrement** la base locale : `DELETE FROM items` puis `DELETE FROM meta`, sans aucune confirmation (source : `dofus_stuff/database.py`). » + `:192` dans « Source de vérité » | `docs/cli.md` reste **propriétaire** de la surface de commandes : la nouvelle page **signale** sur la même ligne (D-80) et **renvoie par lien** à `cli.md` pour le détail |
| 7 | `PURGE OUI` et ses effets | `docs/parcours-simplifie.md:174` : « `N` ouvre la sauvegarde portant ce numéro, `DEL N` en supprime une, et `PURGE OUI` les retire toutes. » ; `:176` : « `PURGE OUI` annonce ensuite `SAUVEGARDES PURGEES` » | `docs/parcours-simplifie.md` reste propriétaire de l'écran `SAV-01` ; la nouvelle page **signale** le caractère destructeur (D-80) et **renvoie par lien** |
| 8 | Les champs de l'état de la base (prose) | `docs/installation.md:49` : « elle **crée** la base locale si elle est absente, puis affiche ses caractéristiques : fichier utilisé, version du jeu, date du dernier contrôle et nombre d'entrées. » | `docs/installation.md` décrit le **premier contact** ; la nouvelle page donne les **noms exacts des deux surfaces**. Ne rien réécrire dans `installation.md` (voir Pitfall 9 : la garde de cette page interdit `PURGE`) |
| 9 | `db status` crée le fichier | `docs/installation.md:49` **et** `:117` (« commencer par la commande hors-ligne `python fetcher.py --offline db status` du chemin minimal, qui crée la base locale si elle est absente ») | La nouvelle page porte le comportement (critère 3) ; `installation.md` garde sa formulation de remède, et son renvoi « hors de cette page » (`:51`, `:117`) peut devenir un **lien** |
| 10 | Le défaut hors-ligne du web | `docs/installation.md:79` : « L'interface démarre **en mode hors-ligne par défaut** : `--offline` est actif sans rien préciser. » + tableau `:86-90` | La nouvelle page énonce les **deux** défauts **côte à côte** (D-71) ; `installation.md` garde son tableau d'options d'entrée (propriété INST-02) |
| 11 | Le défaut « en ligne » de la CLI | `docs/cli.md:16` (défaut `faux` pour `--offline`) et `docs/installation.md:129` (« Sans `--offline`, la ligne de commande interroge l'API Dofusdude par défaut ») | La nouvelle page énonce la **paire** (c'est le risque de confusion central) ; les deux pages voisines gardent leurs énoncés par surface |
| 12 | Exemples de commandes `db` | `README.md:75-81` (bloc `db status` / `db sync` / `db clear`) et `docs/cli.md:152-171` | Le README garde son bloc (D-87) — voir le constat destructeur ci-dessous |

**Aucun autre énoncé du sujet n'apparaît ailleurs** : la page « base locale » n'existe pas encore
(vérifié : `grep -rn "base-locale" docs/ README.md` → seul `README.md` n'y fait **aucun** renvoi ;
`docs/sommaire.md:11` porte le libellé `5. Base locale` en **prose**, sans lien, dans le « Parcours
conseillé », et l'index (`:19-22`) ne la liste pas).

## Inventaire des commandes destructrices dans la documentation livrée (question H)

Recherche exhaustive (`grep -rni "drop|supprim|destruct|vider|clear|PURGE" docs/*.md README.md
GUIDE_WIZARD.md`) : **11 occurrences**, classées ci-dessous.

| # | Emplacement (verbatim court) | Présenté comme une étape à suivre ? | Constat |
|---|------------------------------|-------------------------------------|---------|
| 1 | `README.md:80` : `python fetcher.py db clear           # vider la base` | **OUI** — c'est la 3ᵉ ligne d'un bloc `bash` de trois commandes (`:77-81`), sans aucun avertissement | **La seule occurrence du dépôt où une commande destructrice est présentée comme une étape.** Le plan doit **délimiter le critère 4** (cf. Pitfall 8) et consigner ce fait ; le corriger supposerait de réécrire le README, ce que D-87 ne demande pas |
| 2 | `README.md:83` : « Les anciennes sous-commandes `cache stats\|fill\|clear` restent acceptées en alias. » | Non (mention d'alias) | Rien à faire |
| 3 | `docs/cli.md:164` : `| ` + "`clear`" + ` | Vider la base locale |` | Non (ligne de tableau, section `db`) | La page CLI la décrit ; la nouvelle page renvoie par lien |
| 4 | `docs/cli.md:174` : `### ` + "`db clear`" + `, commande destructrice` | Non — c'est un **titre** qui étiquette | Bon patron à imiter (avertissement **dans le titre**) |
| 5 | `docs/cli.md:176` : « Les commandes destructrices … vident **entièrement** la base locale : `DELETE FROM items` puis `DELETE FROM meta`, sans aucune confirmation » | Non — **explicitement** destructrice | `docs/cli.md` est propriétaire du détail |
| 6 | `docs/cli.md:178` : « Ces commandes ne sont l'étape d'aucun parcours de cette page et aucun bloc d'exemple n'en contient » | Non | À ne pas contredire |
| 7 | `docs/cli.md:192` : « suppression effective des tables par `db clear`, la commande destructrice qui vide la base locale » | Non (bloc « Source de vérité ») | Rien à faire |
| 8 | `docs/parcours-simplifie.md:174` : « `PURGE OUI` les retire toutes » | **Ambigu** — la phrase est une **description d'écran** dans un parcours (« Parcours simplifié »), pas une instruction, mais elle ne qualifie **pas** la commande de destructrice | La nouvelle page signale le caractère destructeur (D-80) ; `parcours-simplifie.md` reste propriétaire de la description de l'écran |
| 9 | `docs/parcours-simplifie.md:176` : « `PURGE OUI` annonce ensuite `SAUVEGARDES PURGEES` » | Non (description d'un retour d'écran) | Idem |
| 10 | `docs/wizard-avance.md:150` : `| ` + "`CLEAR`" + ` | ` + "`VIDER LISTES`" + ` |` | Non — c'est la commande de l'écran **`items`** du wizard (elle vide des listes de saisie, pas la base) | Ne pas confondre : `CLEAR` ≠ `db clear`. La page base locale ne doit pas laisser croire l'inverse |
| 11 | `docs/wizard-avance.md:214` : « Aucune commande destructrice n'appartient à ce parcours : l'exemple ne vide aucune liste, ne supprime rien et ne touche pas à la base locale. » | Non | Modèle de déclaration explicite, à imiter pour la page base locale |

**Aucun `drop`, aucun `DELETE` SQL et aucune suppression de fichier sous `.data/` n'est décrit comme
une étape où que ce soit dans les pages livrées** (les seules occurrences de `DELETE` sont dans
`docs/cli.md:176`, en tant que description de l'effet destructeur). La seule suppression décrite
comme action possible est `PURGE OUI` (`localStorage`, `docs/parcours-simplifie.md:174`) et
`DEL N` (une sauvegarde de navigateur).

## File conventions — preuve mesurée CRLF / UTF-8 sans BOM (question H)

Mesure de cette session (lecture binaire, `octets.count(b"\r\n")` vs nombre de fins de ligne,
`octets.startswith(b"\xef\xbb\xbf")`) :

| Fichier | Lignes | CRLF | LF seul | BOM |
|---------|--------|------|---------|-----|
| `docs/cli.md` | 195 | 195 | 0 | non |
| `docs/installation.md` | 141 | 141 | 0 | non |
| `docs/parcours-simplifie.md` | 269 | 269 | 0 | non |
| `docs/sommaire.md` | 22 | 22 | 0 | non |
| `docs/wizard-avance.md` | 224 | 224 | 0 | non |
| `README.md` | 123 | 123 | 0 | non |
| `GUIDE_WIZARD.md` | 18 | 18 | 0 | non |
| `tests/conftest.py` | 262 | 262 | 0 | non |
| `tests/test_docs_cli.py` | 1060 | 1060 | 0 | non |
| `tests/test_docs_code_anchor.py` | 255 | 255 | 0 | non |
| `tests/test_docs_parcours.py` | 2990 | 2990 | 0 | non |
| `tests/test_docs_structure.py` | 603 | 603 | 0 | non |
| `tests/test_docs_wizard.py` | 2721 | 2721 | 0 | non |
| `tests/fixtures/guide-wizard-obsolete.md` | 39 | 39 | 0 | non |
| `dofus_stuff/web/*.py` (5 modules) | 119-1384 | = lignes | 0 | non |

**Conclusion :** la convention est **uniforme** sur tout ce qui est produit dans ce dépôt — `100 %`
CRLF, **aucun** BOM, `0` fin de ligne LF seule. C'est la règle que `docs/base-locale.md` et
`tests/test_docs_base_locale.py` doivent suivre (D-67, D-69). L'assertion correspondante existe
**verbatim** dans deux modules et se recopie (`tests/test_docs_wizard.py:826-833` pour l'empreinte,
`:1832-1848` pour les octets de la page ; `tests/test_docs_parcours.py:2635-2646`). Limite :
`git config core.autocrlf` vaut `true` sur ce poste et **aucun `.gitattributes` n'existe** → l'assertion
n'est pas portable (Pitfall 11, AR-5 de la phase 3/4).

---

## Code Examples

Toutes les valeurs ci-dessous sont **mesurées** (import, rendu ou capture) dans cette session.

### Les trois constantes publiques qui fondent le critère 1

```python
# Source : dofus_stuff/database.py:12-26 et dofus_stuff/sync.py:11 (imports reels, mesures cette session)
DB_NAME = "dofus.sqlite3"
DEFAULT_DATA_DIR = Path(__file__).resolve().parent.parent / ".data"   # == <racine du depot>/.data
ITEM_KINDS = ("equipment", "resources", "consumables", "quest", "cosmetics", "mounts", "sets")
META_GAME_VERSION = "game_version"
META_LAST_CHECKED_AT = "last_checked_at"
CHECK_INTERVAL_SECONDS = 24 * 60 * 60        # 86400, mesure
```

### Les deux défauts, sondés par l'API publique des parseurs (D-14)

```python
# Source : dofus_stuff/cli.py:46-50 et dofus_stuff/web/__main__.py:21-31 (aide rendue mesuree)
from dofus_stuff.cli import build_parser as parseur_cli
from dofus_stuff.web.__main__ import build_parser as parseur_web

# CLI : en ligne par defaut -> --offline requis pour ne pas contacter l'API
assert parseur_cli().parse_args(["db", "status"]).offline is False      # mesure
assert parseur_cli().parse_args(["--offline", "db", "status"]).offline is True
assert parseur_cli().parse_args(["db", "status"]).force_sync is False

# Web : hors-ligne par defaut
assert parseur_web().parse_args([]).offline is True                     # mesure
assert parseur_web().parse_args(["--no-offline"]).offline is False
assert parseur_web().parse_args(["--online"]).online is True
```

### Lire une aide de parseur sans exécuter le produit

```python
# Source : tests/test_docs_cli.py:268-277 (patron existant, adapte aux deux parseurs)
import io
from contextlib import redirect_stderr, redirect_stdout

def aide(build, argv):
    tampon = io.StringIO()
    try:
        with redirect_stdout(tampon), redirect_stderr(tampon):
            build().parse_args(argv + ["--help"])   # leve SystemExit(0) : capturee, jamais subie
    except SystemExit:
        pass
    return tampon.getvalue()

aide_cli = aide(parseur_cli, [])                    # racine : --timeout, --data-dir, --force-sync, --offline
aide_web = parseur_web().format_help()              # web : --offline | --no-offline, --online, --data-dir, ...
```

Extraits **verbatim** des aides mesurées (espaces finaux rognés, retours de ligne réels) :

```
  --force-sync          Ignorer la fenêtre 24h et forcer une vérif / sync
                        version
  --offline             Ne pas contacter l'API (échoue si la base locale est
                        vide)
```
```
  --offline, --no-offline
                        Ne pas contacter l'API au démarrage (défaut : oui)
  --online              Autoriser le contact API (équivalent --no-offline)
```

### La sortie réelle de l'état de la base (critère 2) — deux surfaces, deux jeux de chaînes

```text
# CLI : _print_db_status sur une base non vide (mesure)
Fichier : <chemin absolu>
Version jeu : 9.9.9.9
Dernier check : il y a 0.0h
Entrées : 3
Par catégorie :
  - equipment : 2
  - resources : 1

# Web : GET /db/status, corps rendu (mesure)
FICHIER : <chemin absolu>
VERSION JEU : 9.9.9.9
DERNIER CHECK : IL Y A 0.0H
ENTREES : 3
PAR CATEGORIE :
  - equipment : 2
  - resources : 1
```

### Le refus de `db sync --offline` et la garde hors-ligne (D-78)

```python
# Source : dofus_stuff/cli.py:344-347 (litereaux lus par ast cette session)
if args.offline:
    print("Erreur : --offline incompatible avec db sync", file=sys.stderr)
    return 1
```
```python
# Source : dofus_stuff/sync.py:41-43 (leve sur base vide, mesure)
raise RuntimeError("Base locale vide et --offline : impossible de synchroniser")
```

### L'effet destructeur, lu sans l'exécuter (D-81)

```python
# Source : dofus_stuff/database.py:146-152 — littéraux extraits par ast, jamais exécutés
ast.parse(<source de dofus_stuff/database.py>)  →  FunctionDef "clear"  →  Constant(str) :
    ["Vide items + meta. Retourne le nombre d'items supprimés.", "DELETE FROM items", "DELETE FROM meta"]
```

```python
# Source : dofus_stuff/web/static/js/terminal.js:459-470 (mesure de lecture)
if (upper === "PURGE OUI") {
  try { localStorage.removeItem(SAVES_KEY); } catch (err) { /* ignore */ }
  renderSavesList();
  setStatus("SAUVEGARDES PURGEES", "info");
  return;
}
if (upper === "PURGE") {
  setStatus("CONFIRMER AVEC : PURGE OUI", "error");
  return;
}
```

### L'écran web destructeur et le seul contact API hors-ligne

```python
# Source : dofus_stuff/web/routes.py:843-859 (rendu mesure : "OPERATION DESTRUCTIVE — ENTREE=VALIDER")
status="OPERATION DESTRUCTIVE",
status_kind="error",
```
```python
# Source : dofus_stuff/web/routes.py:814-826 — offline=False EN DUR : le seul endroit ou le
# mode hors-ligne ne s'applique pas (D-79). Jamais poste par le harnais.
cfg = current_app.extensions["web_config"]
ensure_up_to_date(db, force=True, offline=False, timeout=timeout, quiet=True)
```

### La garde `ast` du nouveau module (à écrire — cf. Pattern 4 et Pitfall 2)

```python
# Adapte de tests/test_docs_wizard.py:311-330, :937-965, :968-980
RACINES_INTERDITES = ("sqlite3", "subprocess", "socket", "multiprocessing", "ctypes",
                      "webbrowser", "urllib", "requests", "http", "ftplib", "smtplib")
APPELS_SUPPRESSION = ("remove", "unlink", "rmdir", "rmtree")
APPEL_PRODUIT = "main"
CONFIRMATIONS_INTERDITES = ("O", "Y", "OUI", "YES")   # routes.py:810 accepte exactement ces valeurs
# dofus_stuff.database reste IMPORTable : c'est la source de DB_NAME / ITEM_KINDS / Database.
```

## State of the Art

Cette phase n'a **pas** de dimension écosystémique : aucun paquet, aucune version externe, aucune API.
Le tableau porte donc sur les **approches de vérification** dans ce dépôt.

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Vérifier une page par relecture manuelle | **Ancrer la page sur le rendu ou une constante publique**, un module par page | Phase 3 (`03-RESEARCH`), confirmé phase 4 | Un libellé faux fait rougir la suite au lieu de survivre ; c'est la méthode que la phase 5 reprend (D-82) |
| Un module d'ancrage unique (`test_docs_code_anchor.py`) pour toutes les pages | **Un module dédié par page**, helpers partagés dans `conftest.py` | Phases 3 et 4 | La prescription de `CLAUDE.md` §4.3 (base locale vérifiée par `test_docs_code_anchor.py`) est **supersédée** ; D-82 tranche pour `tests/test_docs_base_locale.py` |
| `PAGES_INEXISTANTES` comme dette visible | **Réduire la réserve au moment où la cible est créée**, dans le même commit | Phase 4 (pour `wizard-avance.md`) | C'est le geste obligatoire de la phase 5 (Pitfall 1) |
| Doc générée par LLM local (`.doc-agent`) | **Rédaction sourcée + contrôles pytest** | Phase 1 (décision de stack) | Aucun générateur n'est réactivé (son état est resté `running/PLAN`, non versionné) |
| « Ne pas asserter sur les octets de fin de ligne » (`CLAUDE.md` §10, MEDIUM) | **Assertion CRLF + BOM dans chaque module de page** | Phase 3, reconduit phase 4 | Convention verrouillée (D-67) avec une limite déclarée (AR-5, Pitfall 11) |

**Deprecated/outdated:**

- `docs/cli.md:26` — la phrase « Le détail de la fenêtre 24 h et de la resynchronisation est traité
  avec la base locale » : **vraie mais sans lien** ; elle devient un **renvoi par lien** dès que
  `base-locale.md` existe (D-86).
- `PAGES_INEXISTANTES = ("base-locale.md",)` — réservation devenue fausse à l'instant où la page est
  livrée (Pitfall 1).

## Assumptions Log

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|---------------|
| A1 | L'ancrage des **cinq libellés CLI** passe par l'appel à `_print_db_status` (nom privé) sur une base `tmp_path`, route que `CLAUDE.md` §4.3 nomme explicitement | § *7*, § *Feasibility* (mécanisme 5) | Si le planificateur refuse un nom privé au motif de D-14, le contrôle se replie sur les **littéraux `ast`** (mécanisme 6) — contrôle plus faible : il prouve que la chaîne est écrite dans le producteur, pas qu'elle est affichée |
| A2 | L'effet de `PURGE OUI` (purge des sauvegardes du navigateur) est établi par **lecture de `terminal.js`** ; aucun contrôle Python ne peut l'exécuter | § *10*, § *Feasibility* | Si le JavaScript change sans que le libellé change, la page devient fausse sur l'**effet** alors que le contrôle reste vert. La limite est déclarée (D-85) ; le plan peut ajouter un contrôle « le traitement `PURGE OUI` existe encore dans `terminal.js` » |
| A3 | Le critère 4 (« aucune commande destructrice dans un parcours ») est appliqué **au périmètre de la phase** (la nouvelle page et son module), `README.md:80` restant hors de la réécriture autorisée par D-87 | § *Destructive-command audit*, Pitfall 8 | Si la vérification de phase applique le critère **globalement**, elle trouvera une occurrence dans `README.md` et pourra déclarer la phase incomplète pour un fichier que la phase n'a pas mandat de réécrire. Le plan doit **écrire ce périmètre** pour que le critère soit vérifiable tel qu'il est livré |
| A4 | La phrase d'aide doit être comparée **après normalisation des espaces**, la largeur d'aide dépendant du terminal (mesuré 80 colonnes) | Pitfall 5 | Une comparaison non normalisée rougit sur une page correcte (mesuré) ; à l'inverse, la normalisation tolère une faute d'espacement — tolérance à **déclarer** dans la docstring du module |

## Open Questions (RESOLVED)

**Statut : les quatre questions sont RESOLVED par le jeu de plans de la phase 5 (`05-01` a `05-03`).**
Aucune n'est restee ouverte et aucune n'a ete renvoyee au porteur du projet : le lieu d'arbitrage de
chacune est nomme ci-dessous, et sa resolution est reportee **inline** sous chaque question. Cette
section ne tranche rien de neuf — elle **consigne** ce que les trois `PLAN.md` ont deja decide, et
chacune de ces resolutions s'adosse a une decision verrouillee de `05-CONTEXT.md` (D-63, D-68 a D-91),
qui restent telles quelles.

| # | Question | Resolution retenue et lieu d'arbitrage |
|---|----------|----------------------------------------|
| 1 | Ou placer la ligne d'index dans `docs/sommaire.md` ? | **Ajout en fin de table `## Index`**, aucune ligne existante remaniee (D-70). Arbitre par `05-01-PLAN.md` tache 1, controle `test_page_et_index_de_la_base_locale`. |
| 2 | Faut-il convertir les renvois en prose en liens ? | La reserve `PAGES_INEXISTANTES` est **videe** (obligatoire, D-44) **et** les deux renvois de `docs/parcours-simplifie.md` (lignes 5 et 256) deviennent des liens vers `base-locale.md` (D-63, D-86) ; le renvoi de `docs/cli.md:26` reste en prose (D-86 l'autorise sans l'imposer, aucun controle de la phase ne le porte). Arbitre par `05-01-PLAN.md` tache 1. |
| 3 | Citer le message de refus de `db sync` alors que `docs/cli.md` le cite deja deux fois ? | **Cite verbatim** depuis le code : D-78 est une decision verrouillee et prime sur D-17 ; le detail de la sous-commande reste chez `docs/cli.md`, atteint par un lien. Arbitre par `05-02-PLAN.md` tache 2, `test_le_refus_de_la_synchronisation`. |
| 4 | Ou vit le controle D-87 (renvois du `README.md`) ? | Dans le **module neuf** (`renvois_morts`, fonction pure), perimetre de la phase ; les gardes de la phase 1 restent inchangees. Arbitre par `05-03-PLAN.md` tache 1, `test_renvois_du_readme_resolus`. |

1. **Où placer la ligne d'index dans `docs/sommaire.md` ?**
   - What we know: D-70 impose **une seule** ligne et interdit de remanier l'ordre existant ; l'index
     porte aujourd'hui 4 lignes (`:19-22`) et le « Parcours conseillé » (`:7-13`) place « Base locale »
     en 5ᵉ position. Aucun contrôle ne vérifie **l'ordre** : `problemes_index` compare des **ensembles**
     (`tests/test_docs_structure.py:92-119`), `test_sommaire_index_labels_are_unique` l'unicité
     (`:468+`).
   - What's unclear: l'insertion en fin de tableau (après « Wizard avancé ») ou alignée sur le parcours.
   - Recommendation: **ajouter en fin de tableau** — c'est la lecture littérale de D-70 (« l'index
     croît au rythme des pages créées ») et cela ne touche aucune ligne existante.
   - **Résolution (décidée par le jeu de plans) :** recommandation **adoptée telle quelle** — la ligne
     d'index est ajoutée en fin de table `## Index`, aucune ligne existante n'est déplacée ni reformulée,
     et la liste « Parcours conseillé » garde son texte sans lien. Consommée par `05-01-PLAN.md` tâche 1 ;
     vérifiée par `test_page_et_index_de_la_base_locale` (et par `problemes_index`, qui compare des
     ensembles, `tests/test_docs_structure.py:92-119`).
2. **Faut-il convertir les renvois en prose de `docs/parcours-simplifie.md:256` (« le fonctionnement de
   la **base locale** ») et `docs/cli.md:26` en liens ?**
   - What we know: D-86 autorise le lien « là où la cible existe » ; la phase 4 a fait exactement cela
     pour `wizard-avance.md` (D-63) ; `tests/test_docs_parcours.py` exige que la phrase
     `RENVOIS_SANS_LIEN = ("réglages avancés", "base locale")` reste **présente** (elle admet un lien).
   - What's unclear: si le plan veut la dette **entièrement** levée ou minimalement (réserve réduite).
   - Recommendation: réduire `PAGES_INEXISTANTES` (**obligatoire**) et convertir les deux renvois en
     liens (**recommandé**, cohérent avec D-63/D-86) ; vérifier dans le même commit que
     `test_lien_wizard_avance_legitime` reste vert.
   - **Résolution (décidée par le jeu de plans) :** les deux branches sont **retenues** — la réserve
     `PAGES_INEXISTANTES` est **vidée** dans le même commit que la page (obligatoire, D-44) **et** les deux
     renvois en prose de `docs/parcours-simplifie.md` (~lignes 5 et 256) deviennent des liens vers
     `base-locale.md` (D-63, D-86) sans perdre les mots « base locale ». Le renvoi en prose de
     `docs/cli.md:26` reste en prose : D-86 autorise le lien *là où la cible existe* sans l'imposer, et
     aucun contrôle de la phase ne le porte. Consommée par `05-01-PLAN.md` tâche 1, contrôlée par
     `05-03-PLAN.md` tâche 1 (`test_renvoi_base_locale_legitime`).
3. **La nouvelle page doit-elle citer le message de refus de `db sync` alors que `docs/cli.md` le cite
   déjà deux fois ?**
   - What we know: D-78 l'exige (« son message réel est cité depuis le code, jamais paraphrasé ») ;
     D-17 pose une source unique par énoncé.
   - Recommendation: citer le message (décision verrouillée prioritaire), et **renvoyer par lien** à
     `docs/cli.md` pour le détail de la sous-commande.
   - **Résolution (décidée par le jeu de plans) :** la recommandation est **adoptée** — le message de refus
     est cité verbatim depuis le code (D-78, décision verrouillée prioritaire sur D-17) et le détail de la
     sous-commande reste chez `docs/cli.md`, atteint par un lien. Consommée par `05-02-PLAN.md` tâche 2,
     `test_le_refus_de_la_synchronisation` (littéral lu par `ast`, `main()` jamais exécuté).
4. **Le contrôle D-87 (renvois du `README.md`) doit-il vivre dans le nouveau module ou dans
   `tests/test_docs_structure.py` ?**
   - What we know: `tests/test_docs_structure.py:190-210` vérifie déjà **un** renvoi du README (le lien
     unique vers `docs/sommaire.md`) ; le critère D-87 dit « les renvois de `README.md` pointent vers
     des fichiers qui existent », ce qui est **plus général**.
   - Recommendation: un contrôle **dans le nouveau module** (périmètre de la phase, D-82) qui énumère
     **tous** les liens de `README.md` et exige que chacun résolve depuis la racine ; ne pas élargir
     les gardes de la phase 1 (elles restent inchangées).
   - **Résolution (décidée par le jeu de plans) :** la recommandation est **adoptée** — le contrôle vit dans
     le module neuf, sous la forme de la fonction pure `renvois_morts(texte, racine)` et du test
     `test_renvois_du_readme_resolus` ; les gardes de la phase 1 (`tests/test_docs_structure.py`) restent
     inchangées. Consommée par `05-03-PLAN.md` tâche 1 (morsure jouée sur une copie **en mémoire** du
     README, aucun fichier du dépôt n'est écrit).

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|-------------|-----------|---------|----------|
| `./.venv/Scripts/python.exe` | Exécution de référence (D-15) | ✓ | Python **3.14.7** (mesuré) | — |
| `pytest` dans `.venv` | Tout le harnais | ✓ | **9.1.1** (mesuré ; `>=8.0` déclaré) | — |
| `flask` (+ `test_client`) | Rendus `DB-01`…`DB-04`, `SAV-01` | ✓ | `>=3.0` déclaré, importé avec succès cette session | — |
| `git` | Commits locaux | ✓ | 2.55.0.windows.4 (mesuré), `core.autocrlf=true`, **aucun `.gitattributes`** | — |
| Base locale `.data/dofus.sqlite3` | **Aucun besoin pour les contrôles** : la fixture `app` construit sa base sous `tmp_path` | ✓ (présente, non ouverte par les contrôles) | 24 989 696 octets / `mtime_ns 1788730056843137500` / SHA-256 `e3793d64cb7939ad1a51837b075b6b95e03d64c878fcb9cc07f86c00bb8fef7b` | — |
| Réseau / navigateur / serveur web | — | ✗ (et interdit) | — | Aucun : les rendus passent par le client de test en processus ; `PURGE OUI` n'est **pas** exécutable ici (limite déclarée) |
| Compte externe, secret, service distant | — | ✗ (et hors périmètre) | — | Aucun |

**Missing dependencies with no fallback:** none — tout ce que la phase exige est installé et mesuré.
**Missing dependencies with fallback:** none.

*Écart à signaler au plan (pas un blocage) :* `requires-python = ">=3.11"` déclaré, interpréteur du
`.venv` en **3.14.7**. Rien dans cette phase n'utilise une construction au-delà de 3.11 (`ast`,
`pathlib`, `X | None` déjà employés) : aucun impact. Une seule dépendance est **non disponible par
nature** : un navigateur, donc l'exécution de `PURGE OUI` (limite A2).

---

## Validation Architecture

`workflow.nyquist_validation` vaut `true` dans `.planning/config.json` : cette section est **requise**.

### Test Framework

| Property | Value |
|----------|-------|
| Framework | pytest **9.1.1** (déclaré `>=8.0`), Python 3.14.7 (`./.venv/Scripts/python.exe`) |
| Config file | `pyproject.toml` → `[tool.pytest.ini_options]` (`testpaths = ["tests"]`, `pythonpath = ["."]`, `filterwarnings`) — **aucune configuration à ajouter** |
| Quick run command | `./.venv/Scripts/python.exe -m pytest -q tests/test_docs_base_locale.py` |
| Full suite command | `./.venv/Scripts/python.exe -m pytest -q` — **baseline mesurée cette session : `205 passed in 3.59s`** |
| Fixtures partagées | `tests/conftest.py` : `catalog`, `app`, `client`, `docs_dir`, `normalize`, `section`, `sections`, `lignes_de_code`, `lignes_exemple` (D-12 : **à réutiliser, jamais recopier**) |
| Preuve de non-régression de `.data/` | Empreinte `(taille, mtime_ns, sha256)` mesurée **avant et après la suite entière** — mesuré cette session : identique (`24989696` / `1788730056843137500` / `e3793d64cb7939ad1a51837b075b6b95e03d64c878fcb9cc07f86c00bb8fef7b`) |

### Phase Requirements → Test Map

| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|--------------|
| BASE-01 | Le nom du fichier cité par la page **est** `DB_NAME` (comparé à la constante importée) | unit (constante publique) | `… -m pytest -q tests/test_docs_base_locale.py -k fichier` | ❌ Wave 0 |
| BASE-01 | Les **7** catégories de `ITEM_KINDS` sont nommées par la page, et `ITEM_KINDS` **égale** les kinds de `SYNC_SOURCES` | unit (constantes + page) | `… -k categories` | ❌ Wave 0 |
| BASE-01 | La page cite la **constante** de la fenêtre (`CHECK_INTERVAL_SECONDS`) et aucune valeur volatile (aucun compteur, aucune date, aucune version) | unit (constante + page, motif négatif) | `… -k fenetre` | ❌ Wave 0 |
| BASE-02 | Défaut **web** hors-ligne (mesuré `True`) et défaut **CLI** en ligne (mesuré `False`), chacun énoncé **dans la section de sa surface**, avec la phrase d'aide réelle | unit (parseurs + page) | `… -k defauts_hors_ligne` | ❌ Wave 0 |
| BASE-02 | Les **5 champs CLI** cités sont produits par `_print_db_status` (sortie capturée sur `tmp_path`) | unit (capture stdout) | `… -k champs_cli` | ❌ Wave 0 |
| BASE-02 | Les **5 champs web** cités sont rendus par `GET /db/status` (corps rendu, `tmp_path`) et `PAR CATEGORIE` n'apparaît **que** sur une base peuplée | unit (rendu Flask) | `… -k champs_web` | ❌ Wave 0 |
| BASE-03 | `db status` **crée** le fichier : mesuré sur `tmp_path` par la CLI (fonction) **et** par `GET /db/status` | unit (effet de bord en tmp) | `… -k creation` | ❌ Wave 0 |
| BASE-03 | Le refus `Erreur : --offline incompatible avec db sync` est cité **verbatim** ; il est lu par `ast` dans `cli.py` (jamais par exécution de `main()`) | unit (ast) | `… -k refus_sync` | ❌ Wave 0 |
| BASE-03 | La page dit que l'écran **web** de synchronisation contacte l'API même hors-ligne, et le code le prouve (`offline=False` littéral dans l'appel de `routes.py`, lu par `ast`) | unit (ast + page) | `… -k synchro_web` | ❌ Wave 0 |
| BASE-03 | `db clear` et `PURGE OUI` sont signalés **destructeurs sur la même ligne** que la commande, et n'apparaissent dans **aucun** bloc d'exemple de la page (`lignes_exemple`) | unit (page, contrôle par ligne) | `… -k destructrices` | ❌ Wave 0 |
| BASE-03 | Aucun contrôle du module n'exécute une commande destructrice, aucun POST de confirmation, aucun `main()`, aucun réseau (**garde `ast`**) | unit (ast sur le module) | `… -k garde_cloture` | ❌ Wave 0 |
| BASE-03 | `.data/dofus.sqlite3` a la **même** empreinte autour des rendus du module (`skip` nommé si absente) | mesure (lecture d'octets) | `… -k data_locale` | ✅ patron existant (3ᵉ copie assumée) |
| BASE-03 (D-87) | **Chaque** renvoi de `README.md` résout depuis la racine du dépôt (le critère pris à la lettre) | unit (disque) | `… -k readme` | ❌ Wave 0 |
| Critère 5 | La page respecte le gabarit : H1 = libellé d'index, ligne de retour, UTF-8 strict, pas de jeton de brouillon, ≥ 300 caractères, lien présent dans l'index | unit (**gardes existantes**) | `… -m "" tests/test_docs_structure.py` | ✅ `tests/test_docs_structure.py:121-533` |
| Critère 5 | Les octets de `docs/base-locale.md` sont **CRLF sans BOM** | unit (lecture binaire) | `… -k crlf` | ❌ Wave 0 |
| Critère 5 | Les chemins entre accents graves du bloc « Source de vérité » **existent** sur disque | unit (disque) | `… -k source_de_verite` | ❌ Wave 0 |
| Critère 5 | La suite entière reste verte avec l'interpréteur épinglé | suite | `./.venv/Scripts/python.exe -m pytest -q` (`205 passed` avant la phase) | ✅ existant |
| Critère 4 | `PAGES_INEXISTANTES` ne déclare plus inexistante une page livrée | unit (**garde existante**, à ne pas casser) | `… tests/test_docs_parcours.py -k lien_wizard` | ✅ existant (rougit sans la modification exigée) |

*Ce qui est **déjà** couvert par une garde existante et ne doit **pas** être re-prouvé :* l'exhaustivité
bidirectionnelle de l'index et l'unicité du libellé (`tests/test_docs_structure.py:92-119`, `:468`), le
`H1` = libellé (`:337-380`), la ligne de retour (`:383-417`), l'encodage/longueur/jetons de brouillon
(`:418-447`), la résolution des liens internes (`:39-89`), la dérive injectée dans une copie de `docs/`
(`:533`), l'existence du **seul** renvoi du README vers le sommaire (`:190-210`), et le fait que
`cache <x>` et `db <x>` sont équivalents pour le parseur (`tests/test_docs_cli.py:676-694`).

*Ce que la phase **doit** ajouter malgré tout :* les sept contrôles de valeur de la table ci-dessus,
la garde `ast` **réécrite** (Pitfall 2), la mesure d'empreinte locale, et la modification
**obligatoire** de `tests/test_docs_parcours.py` (`PAGES_INEXISTANTES`).

### Sampling Rate

- **Per task commit :** `./.venv/Scripts/python.exe -m pytest -q tests/test_docs_base_locale.py`
  puis, dès qu'un fichier de `docs/` bouge :
  `… -m pytest -q tests/test_docs_structure.py tests/test_docs_parcours.py`.
- **Per wave merge :** `./.venv/Scripts/python.exe -m pytest -q` (suite entière, ~3,6 s mesurée).
- **Phase gate :** suite entière verte **et** empreinte de `.data/dofus.sqlite3` **identique** avant /
  après (`205 passed` puis le nouveau total), plus la sortie réelle des morsures collée dans le
  `SUMMARY.md` du module de test (D-84).

*Aucune validation manuelle :* l'interprète des critères est pytest. Le seul point non automatisable est
l'**exécution** de `PURGE OUI` (navigateur) — il n'est donc pas revendiqué comme vérifié ; la page
décrit et le module **déclare la limite** (D-85).

### Wave 0 Gaps

- [ ] `tests/test_docs_base_locale.py` — nouveau module d'ancrage (BASE-01, BASE-02, BASE-03, D-87)
- [ ] `docs/base-locale.md` — la page doit exister **avant** que les gardes de structure du sommaire
      (`problemes_index`, `problemes_h1`, `problemes_retour_sommaire`) ne passent
- [ ] `docs/sommaire.md` — **une** ligne d'index `| [Base locale](base-locale.md) | … |` (D-70)
- [ ] `tests/test_docs_parcours.py` — **modification obligatoire** : réduire
      `PAGES_INEXISTANTES` (`:2327`) et, si le plan retient la recommandation, convertir les renvois en
      prose en liens (`ANCRES_RENVOI_D63`, `RENVOIS_SANS_LIEN`) — sans quoi la suite est **rouge**
- [ ] `README.md` — **aucune modification attendue** : si un renvoi ne résout pas, c'est le plan qui
      décide, mais D-87 limite le travail du README à ses renvois
- [ ] Framework install : **aucun** — pytest 9.1.1 déjà présent dans `.venv`, `pyproject.toml` inchangé

## Security Domain

`workflow.security_enforcement` vaut `true` (ASVS niveau 1 déclaré). La phase ne livre ni endpoint, ni
authentification, ni donnée : l'analyse porte donc sur **ce que la phase peut casser** — la véracité
d'une page et l'intégrité de la base locale — et sur la **portée réelle** des contrôles.

### Applicable ASVS Categories

| ASVS Category | Applies | Standard Control |
|---------------|---------|-----------------|
| V2 Authentication | no | Aucune authentification livrée ; l'application de test est instanciée en processus |
| V3 Session Management | no | Aucune session créée ; les écrans lus sont des `GET` sans état |
| V4 Access Control | no | Aucun contrôle d'accès dans la phase |
| V5 Input Validation | **yes** | (1) Chaque valeur citée par la page est **validée contre le code** (constante, aide rendue, rendu, littéral `ast`) : c'est l'entrée de la phase ; (2) les liens de la documentation sont résolus en **rejetant** `#`, les chemins absolus, les antislashs et `file://` (garde existante `problemes_liens`, à ne pas contourner) |
| V6 Cryptography | no | Aucune cryptographie nouvelle ; seul usage : `hashlib.sha256` pour l'empreinte d'un fichier local (patron existant) |
| V8 Data Protection (en creux) | **yes** | Interdiction de citer des valeurs volatiles de la base locale (compteurs, version de jeu, horodatage, taille) : la page ne fige ni n'expose l'état d'un fichier local (D-73/D-75) |

### Known Threat Patterns for {docs + pytest harness + SQLite locale}

| Pattern | STRIDE | Standard Mitigation |
|---------|--------|---------------------|
| Commande destructrice présentée comme une étape normale (`db clear`, `PURGE OUI`, suppression sous `.data/`) | Tampering / DoS | La page signale **sur la même ligne** (D-80) et n'en fait l'étape d'aucun parcours ; le contrôle par bloc d'exemple le vérifie ; aucun `db clear` n'est exécuté (D-81) ; patron existant : `COMMANDE_DESTRUCTRICE` (`tests/test_docs_structure.py:20`) |
| Écriture involontaire sous `.data/` par un test | Tampering | Fixture `app` sur `tmp_path/data` ; **jamais** `DEFAULT_DATA_DIR` passé à `Database` ; empreinte avant/après la suite (limite **L-2** écrite : mesure locale vraie par construction, `skip` nommé si la base est absente) |
| Exécution du produit ou du solveur par le harnais (`main()`, `subprocess`, `eval`) | Elevation of Privilege | Garde `ast` sur le module (`APPEL_PRODUIT = "main"`, `RACINES_INTERDITES`), portée **déclarée** : elle contraint le **module committé**, pas un script hors dépôt (limite **L-1** de `04-SECURITY.md:57`) |
| **Confirmer** une action réseau ou destructive depuis un contrôle (`POST /db/sync`, `POST /db/clear`) | Tampering | Aucun POST de confirmation dans le module ; la garde `ast` refuse la paire `"confirm"` + une valeur de `{"O","Y","OUI","YES"}` (analogue à la paire `"cmd": "GO"` refusée en phase 4) ; le seul POST toléré est `confirm=N` (annulation, mesuré `302 /db`) |
| Fuite de secret dans la documentation | Information Disclosure | Aucun secret n'est écrit : `DOFUS_SECRET_KEY` n'apparaît dans **aucune** page (`docs/`, `README.md` : 0 occurrence, mesuré) ; la page ne cite que des libellés d'écran |
| Documentation qui ment (libellé faux, valeur volatile figée) | Spoofing | C'est la sécurité centrale de la phase : chaque valeur citée est adossée au code, et la § *12* liste explicitement ce qui est **interdit** de citer |
| Lien mort ou cible inexistante dans la nouvelle page | Information Disclosure / Tampering | `problemes_liens` (existant) + D-86 : un renvoi en prose ne devient un lien que là où la cible existe ; les renvois du README sont contrôlés (D-87) |
| Évasion de la racine du dépôt par un lien relatif (`../../…`, chemin absolu, `file://`) | Information Disclosure / Tampering | `problemes_liens` rejette ces formes (contrôle existant, à ne pas contourner) |

*Limites à déclarer dans le module (D-85), héritées et mesurées :* la garde `ast` ne contraint que le
module committé (L-1) ; la mesure d'empreinte locale est vraie par construction (L-2) ; la prose libre
de la page n'est pas vérifiée, seules les valeurs **citées** le sont ; l'exécution JavaScript de
`PURGE OUI` n'est pas observable (A2) ; l'assertion CRLF n'est pas portable hors
`core.autocrlf=true` (AR-5, Pitfall 11).

## Claims non vérifiées (liste explicite)

Aucune valeur citée ci-dessus n'est « plausible mais non mesurée ». Les points suivants sont, en
revanche, **explicitement non vérifiés** et ne doivent pas être présentés comme prouvés :

| # | Ce qui n'est PAS vérifié | Pourquoi | Ce qui est vérifié à la place |
|---|--------------------------|----------|-------------------------------|
| N1 | Que `python -m dofus_stuff.web` démarré par un humain se comporte exactement comme le client de test (serveur réel, navigateur) | Interdit : lancer un serveur et `main()` | Le **rendu** des cinq écrans par le client en processus, et la **lecture** de `web/__main__.py` |
| N2 | Que `DOFUS_OFFLINE=0` ne rend pas la commande web « en ligne » | Conclu par **lecture du code** (`web/__main__.py:41,44` + `web/__init__.py:48-50`) ; exécuter `main()` est interdit | Les lignes citées, verbatim |
| N3 | Le comportement réel de `PURGE OUI` dans un navigateur (localStorage vidé) | Aucun navigateur, aucun test JS | Le libellé au rendu de `SAV-01` **et** le traitement écrit dans `terminal.js:459-466` |
| N4 | Que `db clear` lancé par un humain ne supprime pas le fichier (seulement son contenu) | Interdit : exécuter une commande destructrice | `Database.clear` lu (deux `DELETE`, un `commit`, aucun `unlink`) **et** `clear()` exécuté **sur une base temporaire** en recherche (fichier encore présent, mesure) — ce second point est une **recherche**, jamais un contrôle de la phase |
| N5 | Le nombre de tests final de la phase | Il dépend des tests écrits | La baseline mesurée : `205 passed in 3.59s`, empreinte de `.data/` identique avant/après |
| N6 | Le contenu de `.doc-agent/` et son état de run | Hors périmètre ; non versionné ; **aucune suppression autorisée** | Il existe et n'est pas indexé (`git status` : `?? .doc-agent/`) |

---

## Sources

### Primary (HIGH confidence)

Tous les fichiers ci-dessous ont été **lus cette session** (les plages de lignes sont citées dans le
corps du document à côté de chaque valeur reprise) :

- `dofus_stuff/database.py` (162 lignes) — `DB_NAME:12`, `DEFAULT_DATA_DIR:13`, `META_GAME_VERSION:15`,
  `META_LAST_CHECKED_AT:16`, `ITEM_KINDS:18-26`, `path:34-36`, `open:38-62` (schéma `meta:44-50`,
  `items:52-59`, index `:61`), `game_version:88-89`, `last_checked_at:91-97`,
  `touch_checked_at:100-101`, `item_count:103-105`, `counts_by_kind:107-112`, `is_empty:114-115`,
  `replace_kind:117-133`, `iter_items:135-144`, `clear:146-152`, `stats:154-161`
- `dofus_stuff/sync.py` (115 lignes) — `CHECK_INTERVAL_SECONDS:11`, `ensure_up_to_date:14-69`
  (`needs_check:32`, `within_24h:33-39`, garde `offline:41-50`, cas « à jour » `:51-62`,
  `pull_all:64-69`), `pull_all:74-115` (boucle `SYNC_SOURCES:93`, `replace_kind:104`)
- `dofus_stuff/cli.py` (443 lignes) — options globales `:34-50` (`--force-sync:41-45`,
  `--offline:46-50`), sous-commandes `:52-57`, `db`/`cache` `:180-194`, `_print_db_status:214-229`,
  `_normalize_db_command:283-285`, `main` branche `db`/`cache` `:335-360` (création `:337-338`,
  `status:340-342`, refus `:344-347`, `clear:357-360`), `main:329-436`
- `dofus_stuff/web/__main__.py` (52 lignes, lu en entier) — `build_parser:13-36` (`--data-dir:15-20`,
  `--offline:21-26`, `--online:27-31`), `main:39-48`
- `dofus_stuff/web/__init__.py` (128 lignes) — `_env_bool:15-19`, `create_app:22-66`
  (`DOFUS_SECRET_KEY:41`, `resolved_data_dir:43-47`, `resolved_offline:48-50`,
  `resolved_timeout:51-54`, `web_config:60-65`), `reload_catalog:92-119` (`skip_sync:109-111`)
- `dofus_stuff/catalog.py` (295 lignes) — `SUBTYPE_TO_KIND:12-21`, `Catalog.load:33-56`
  (`Database(data_dir=data_dir or DEFAULT_DATA_DIR):43`, `if not skip_sync:45-52`),
  `search_items`, `list_equipment_page`, `format_item_summary`
- `dofus_stuff/api.py` (74 lignes, lu en entier) — `BASE_URL:14`, `DEFAULT_TIMEOUT:15`,
  `SYNC_TIMEOUT:16`, `MAX_RETRIES:17`, `SYNC_SOURCES:19-28`, `api_get:31-66`, `fetch_version:69-74`
- `dofus_stuff/web/routes.py` (1384 lignes, régions lues) — `_screen:89-186` (assemblage de la ligne de
  statut `:143-150`), `menu:189-227` (`5. SYSTEME:197`), `system_menu:230-248`
  (`4. GESTION DE LA BASE:236`), `self_test`, `db_menu:709-727`, `db_status:744-785`,
  `db_sync_confirm:788-804`, `db_sync_run:807-840`, `db_clear_confirm:843-860`, `db_clear_run:863-880`,
  `saves:1280-1295`
- `dofus_stuff/web/static/js/terminal.js` — `PURGE OUI:459-466`, `PURGE:469-470`, statuts paginés
  `:370`, `:494`
- `dofus_stuff/web/templates/screen.html:49` — la ligne de statut est rendue telle que `_screen`
  l'assemble
- `tests/conftest.py` (262 lignes, lu en entier) — `_sample_items:19-78`, `catalog:80-81`,
  `app:84-111`, `client:115-116`, `_normalize:119-124`, `docs_dir:128-130`, `normalize:133-136`,
  `TITRE_H2`/`DELIMITEUR_BLOC`/`BALISE_EXEMPLE`, `_blocs_de_code`, `_lignes_de_code`, `_lignes_exemple`,
  `_sections:194-205`, `_section:208-226`, fixtures `lignes_de_code`/`lignes_exemple`/`sections`/`section`
- `tests/test_docs_structure.py` (603 lignes) — `COMMANDE_DESTRUCTRICE:20`, `JETON_PURGE:21`,
  `problemes_liens:39-89`, `problemes_index:92-119`, `test_readme_links_to_sommaire:190-210`,
  `test_no_destructive_command_in_installation:277-301`, `LONGUEUR_MINIMALE:315`, `pages_listees:326`,
  `problemes_h1:337-380`, `problemes_retour_sommaire:383-417`, `problemes_encodage:418-447`,
  `test_sommaire_index_labels_are_unique:468`, `test_mutation_detecte_les_trois_derives:533-603`
- `tests/test_docs_cli.py` (1060 lignes, régions) — en-tête et limites `:1-30`,
  `SONDES_SOUS_COMMANDES:76-85`, `SONDES_GLOBALES:89-94`, `SOUS_COMMANDES_DB:134`,
  `_aide_capturee:268-277`, contrôle du défaut `:640-673`, `test_alias_cache_equivalent…:676-706`
- `tests/test_docs_wizard.py` (2721 lignes, régions) — `MARQUEUR_CORPS:91-94`, `RACINES_INTERDITES:311-323`,
  `MODULE_BASE_INTERDIT:326`, `APPELS_SUPPRESSION:329`, `APPEL_PRODUIT:330`, `_lignes_du_corps:353-356`,
  `_statut:373-375`, `_empreinte:826-833`, garde `ast` `:937-965` et paire `"cmd"/"GO"` `:968-980`,
  contrôle CRLF `:1832-1848`, empreinte locale `:2289-2323`
- `tests/test_docs_parcours.py` (2990 lignes, régions) — `PAGES_INEXISTANTES:2327` et son commentaire
  `:2322-2326`, `RENVOIS_SANS_LIEN:2318`, `LIENS_LEGITIMES_VERS_L_AIGUILLAGE:2334`, `_empreinte:2558-2566`,
  contrôle CRLF `:2635-2646`, `test_lien_wizard_avance_legitime:2882-2990`
- `tests/test_web.py` — `test_db_menu_and_status:361-370`, `test_db_sync_cancelled:372-376`,
  `test_db_sync_reload_after_sync:378-388` (patch de `ensure_up_to_date`), `test_db_clear:411-418`,
  `test_saves_screen:107-113` (`b"PURGE OUI" in rv.data`, `:112`)
- `docs/sommaire.md` (22 lignes, lu en entier), `docs/cli.md` (195), `docs/installation.md` (141),
  `docs/parcours-simplifie.md` (269), `docs/wizard-avance.md` (224), `README.md` (123),
  `GUIDE_WIZARD.md` (18)
- `pyproject.toml`, `.gitignore`, `.planning/config.json` (`nyquist_validation: true`,
  `security_enforcement: true`, `claude_md_path: "./.claude/CLAUDE.md"`), `.planning/ROADMAP.md`
  § Phase 5, `.planning/REQUIREMENTS.md` (BASE-01…03, `:47-49`, `:125-127`),
  `.planning/phases/05-…/05-CONTEXT.md`, `05-DISCUSSION-LOG.md`,
  `.planning/phases/04-…/04-RESEARCH.md`, `04-PATTERNS.md`, `04-SECURITY.md`, `.claude/CLAUDE.md`
- **Sonde SQLite en lecture seule** (URI `file:…?mode=ro`) sur `.data/dofus.sqlite3` : schéma, 7 kinds,
  clés de `meta`. **Aucune écriture, aucune suppression, la connexion est fermée.**

### Secondary (MEDIUM confidence)

- **Mesures d'exécution de cette session** — reproductibles par les commandes citées, mais ce ne sont
  pas des documents sources : aide des deux parseurs, défauts des parseurs, rendus `DB-01`…`DB-04` et
  `SAV-01`, sortie de `_print_db_status` (base vide et non vide), quatre retours de
  `ensure_up_to_date`, création du fichier sur `tmp_path`, littéraux `ast`,
  `205 passed in 3.59s`, empreinte de `.data/` avant/après, mesure CRLF/BOM de 20 fichiers.

### Tertiary (LOW confidence)

- Aucune. **Aucune recherche Web n'a été effectuée** : la phase est intégralement interne au dépôt, et
  la seule documentation technique nécessaire (`pytest`, `flask.test_client`, `ast`, `argparse`) est
  déjà couverte par les phases 1 à 4.

## Metadata

**Confidence breakdown:**

- Standard Stack : **HIGH** — aucun paquet nouveau ; versions réellement mesurées dans `.venv`
  (Python 3.14.7, pytest 9.1.1, git 2.55.0.windows.4).
- Architecture : **HIGH** — le nom du fichier, le schéma, les 7 catégories, la constante de 24 h, les
  deux défauts, les cinq champs par surface, le refus, la création du fichier et les commandes
  destructrices sont **mesurés** (import, rendu, capture, lecture seule), pas déduits.
- Pitfalls : **HIGH** pour les pitfalls 1, 2, 3, 4, 5, 6, 7, 9, 10, 11 (mesurés ou vérifiés au
  fichier) ; **MEDIUM** pour le pitfall 8 (il dépend du **périmètre** que le plan écrira pour le
  critère 4 — la mesure, elle, est certaine : `README.md:80` existe).
- Validation Architecture : **HIGH** — framework, fixtures et commandes existants ; baseline
  `205 passed in 3.59s` et empreinte de `.data/` mesurées cette session.
- Anchorability : **HIGH** sur les mécanismes (tous éprouvés ici) ; **MEDIUM** sur le choix entre
  `_print_db_status` appelée et ses littéraux `ast` (A1) et sur la portée du contrôle `PURGE OUI` (A2).

**Research date:** 2026-09-11
**Valid until:** 2026-10-11 (30 jours). La matière est dans le dépôt et ne dépend d'aucune source
externe ; seule une modification de `dofus_stuff/**` (interdite par D-88), de `tests/conftest.py`, ou
des pages voisines de `docs/` invaliderait les mesures. En particulier, toute modification de
`dofus_stuff/web/routes.py` (libellés des écrans), de `dofus_stuff/cli.py` (aides et libellés de
sortie) ou de `dofus_stuff/database.py` (constantes) rendrait caducs les § *1* à *11*.

