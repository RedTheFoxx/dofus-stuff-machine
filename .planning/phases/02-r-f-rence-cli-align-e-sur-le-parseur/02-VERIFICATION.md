---
phase: 02-r-f-rence-cli-align-e-sur-le-parseur
verified: 2026-09-11T12:54:34Z
status: passed
score: 19/19 must-haves verified (19/19 verifiees, 0 present-behavior-unverified)
covered_files:
  - .planning/REQUIREMENTS.md
  - .planning/ROADMAP.md
  - .planning/phases/02-r-f-rence-cli-align-e-sur-le-parseur/02-01-PLAN.md
  - .planning/phases/02-r-f-rence-cli-align-e-sur-le-parseur/02-01-SUMMARY.md
  - .planning/phases/02-r-f-rence-cli-align-e-sur-le-parseur/02-02-PLAN.md
  - .planning/phases/02-r-f-rence-cli-align-e-sur-le-parseur/02-02-SUMMARY.md
  - .planning/phases/02-r-f-rence-cli-align-e-sur-le-parseur/02-03-PLAN.md
  - .planning/phases/02-r-f-rence-cli-align-e-sur-le-parseur/02-03-SUMMARY.md
  - docs/cli.md
  - docs/sommaire.md
  - tests/conftest.py
  - tests/test_docs_cli.py
  - tests/test_docs_code_anchor.py
covered_digest: "v1:sha256:fe1d3603187d13774e152b9fb096d264d3ecfa6badc5772255f5202201b671c3"
behavior_unverified: 0
overrides_applied: 0
decision_coverage:
  honored: 16
  total: 16
  not_honored: []
prohibitions:
  test_tier: 8
  test_tier_enforced: 8
  judgment_tier: 4
  judgment_tier_flagged: 4
  flag: "unverified-prohibition — human review recommended (jugements LLM, non autoritaires ; aucun ne bloque, aucun n'est silencieux)"
deferred:
  - truth: "docs/sommaire.md « Parcours conseillé » nomme cinq pages non encore livrées (Parcours simplifié, Wizard avancé, Base locale, Dépannage, Glossaire)"
    addressed_in: "Phase 6"
    evidence: "ROADMAP.md Phase 6, critère de succès 3 : « Les 8 pages épinglées sont toutes livrées … et le sommaire propose un parcours conseillé final » ; D-05 (le sommaire croît par phase) et D-28 (seule l'entrée cli.md est ajoutée maintenant)"
gaps: []
---

# Phase 2: Référence CLI alignée sur le parseur — Verification Report

**Phase Goal :** Un lecteur dispose d'une référence `docs/cli.md` où chaque sous-commande, chaque option et chaque exemple est réellement analysable par `fetcher.py`.
**Verified :** 2026-09-11T12:54:34Z
**Status :** passed
**Re-verification :** Non — vérification initiale (aucun `*-VERIFICATION.md` antérieur dans le dossier de phase ; Step 0 sans objet)

**Interpréteur de référence :** `.venv/Scripts/python.exe` (pytest 9.1.1). L'interpréteur ambiant de l'hôte n'a pas pytest — toutes les commandes citées ci-dessous utilisent le venv épinglé.

## Goal Achievement

### Observable Truths

Les 5 critères de succès du ROADMAP (1-5, contrat opposable) sont fusionnés avec les `must_haves.truths` des trois plans et dédupliqués quand un point du plan reformule un critère du ROADMAP.

| # | Truth | Status | Evidence |
|---|-------|--------|----------|
| 1 | ROADMAP SC1 — chaque sous-commande documentée (`version`, `self-test`, `search`, `item`, `list`, `optimize`, `db`, alias `cache`) est analysée sans erreur par `build_parser().parse_args` | ✓ VERIFIED | Sonde indépendante des 8 exemples marqués : 8/8 `OK` (aucun `SystemExit`). `SONDES_SOUS_COMMANDES` sonde des argv **complets** (`["db","status"]`, `["cache","status"]`) — un jeton nu sort en code 2 (`db_command` requis), piège évité. Codes source : `dofus_stuff/cli.py:143-179`, defaults mesurés. |
| 2 | ROADMAP SC2 — chaque option globale documentée (`--timeout`, `--data-dir`, `--force-sync`, `--offline`) et chaque option d'`optimize` documentée est réellement acceptée par le parseur | ✓ VERIFIED | Mesure indépendante sur l'extraction des **37** lignes de tableau de la page : les 30 options d'`optimize` sont acceptées avec valeur d'essai (`--jet average` inclus, `choices` oblige) et leurs défauts mesurés par différence d'espaces de noms concordent (15 / `.data` / False / False, `--top-k` 30, `--time-limit` 5.0, `--base-*`/`--scroll-*` 0.0, `--level`/`--max`/`--target`/`--weight`/`--ban`/`--force`/`--seed` `None`, `--limit` 10, `--page` 1, `--size` 5). Chaque ligne de tableau de `## Options globales` est sondée contre le parseur racine (option inventée rejetée : mes mutations M7 et B1). |
| 3 | ROADMAP SC3 — chaque exemple de commande apparaît verbatim dans `docs/cli.md` et son découpage `shlex` est analysable | ✓ VERIFIED | Les 8 exemples sont extraits des blocs ` ```console ` (`BALISE_EXEMPLE`) ; `shlex.split` puis `parse_args` réussissent 8/8. La moitié « verbatim » est une **garantie de construction** (la ligne est extraite de la page) : limite écrite noir sur blanc dans le module (D-26) et dans la section Advisories ci-dessous — je ne la présente pas comme une preuve indépendante. Aucune commande citée en prose n'est un exemple (D-24) ; le seul fragment prose non analysable est la forme **fautive** `db status --offline`, citée précisément pour enseigner le refus (code 2, message réel). |
| 4 | ROADMAP SC4a — au moins un exemple place l'option globale avant la sous-commande | ✓ VERIFIED | `python fetcher.py --offline optimize --demo` est le **seul** exemple marqué portant la paire `--offline` puis `optimize` (comptage indépendant : 1 sur 8 exemples) — témoin unique, donc assertion observable. |
| 5 | ROADMAP SC4b — `db clear` n'apparaît qu'avec son avertissement destructif, jamais dans un parcours recommandé | ✓ VERIFIED | 3 lignes seulement citent `db`/`cache clear` (`l174` titre « commande destructrice », `l176` paragraphe destructeur, `l192` bloc Source de vérité « la commande destructrice qui vide la base ») et les 3 portent le jeton `destruct*` : 3/3. Aucune des 8 lignes d'exemple ne cite `clear`/`sync`/`fill`. Aucun bloc marqué n'en contient. |
| 6 | ROADMAP SC5 — la suite reste verte avec l'interpréteur épinglé, sans exécuter `main()`, sans écrire sous `.data/` | ✓ VERIFIED | `.venv/Scripts/python.exe -m pytest -q` → **169 passed in 2.56s** (relancée en fin de vérification ; le compteur d'avant-phase, 158, provient des exécutants et **n'a pas été re-mesuré** par moi). `git status --porcelain -- docs tests dofus_stuff README.md` → **vide**. `.data/dofus.sqlite3` mtime **`2026-09-06 23:27:36 +0200`** avant, pendant et après la phase et après mes propres exécutions. |
| 7 | 02-01 : `docs/sommaire.md` porte l'entrée d'index `CLI`, atteint `docs/cli.md` par un lien relatif résolu, et le H1 de la page égale le libellé d'index après normalisation | ✓ VERIFIED | `docs/sommaire.md` : `| [CLI](cli.md) | Commandes, options et exemples de fetcher.py |` ; `docs/cli.md:1` = `# CLI` ; dernière ligne = `[Retour au sommaire](sommaire.md)`. Invariants de phase 1 (`test_sommaire_links_resolve`, `test_h1_matches_sommaire_entry`, `test_pages_have_back_link`) verts. |
| 8 | 02-01 : une section par sous-commande dans l'ordre réel du parseur, chacune avec synopsis et au moins un exemple marqué | ✓ VERIFIED | Ordre lu sur la page : `## version`, `## self-test`, `## search`, `## item`, `## list`, `## optimize`, `## db`, `## cache` — identique à l'ordre d'enregistrement du parseur (`dofus_stuff/cli.py:46-52`, `143-179`). Le test de couverture exige explicitement cette suite de titres (une occurrence fortuite ne suffit plus). |
| 9 | 02-01 : les 4 options globales sont documentées avec leur défaut **mesuré**, jamais la valeur absolue propre au poste | ✓ VERIFIED | Page : `15`, « le dossier `.data/` à la racine du dépôt », `faux`, `faux` ; parseur : `DEFAULT_TIMEOUT=15`, `DEFAULT_DATA_DIR` = chemin **absolu** se terminant par `.data` (donc jamais recopié), `force_sync=False`, `offline=False`. |
| 10 | 02-01 : les 30 options d'`optimize` sont documentées en tables groupées par thème avec leur défaut mesuré, sans sémantique inventée pour les 11 options sans `help` | ✓ VERIFIED | Comptage indépendant : **30** lignes d'option dans `## optimize`, réparties en 4 groupes (`Profil et objectifs` 7, `Contraintes de sélection` 6, `Caractéristiques de base et scrolls` 12, `RNG et performances` 5). Le parseur n'a aucun `help` pour exactement 11 d'entre elles (`--base-vit/str/cha/agi/wis`, six `--scroll-*`) ; la page écrit pour chacune « aucune description dans l'aide du parseur » et l'explique en prose — aucune sémantique ajoutée. |
| 11 | 02-01 : `db sync` et `cache fill` sont décrits comme réécrivant la base et exigeant le réseau, avec l'incompatibilité mesurée (code 1, message littéral) | ✓ VERIFIED | Source : `dofus_stuff/cli.py:363-366` — `print("Erreur : --offline incompatible avec db sync", file=sys.stderr)` puis `return 1` ; la page cite ce message dans un bloc `text` et le code de retour 1. Le paragraphe dit explicitement que la règle « toutes les commandes portent `--offline` » de la page d'installation ne s'applique pas ici. |
| 12 | 02-01 : le bloc « Source de vérité » nomme `build_parser()` et `fetcher.py`, et chaque chemin entre accents graves de la page existe sur disque | ✓ VERIFIED | Bloc présent avec `fetcher.py`, `dofus_stuff/cli.py`, `dofus_stuff/database.py`, `dofus_stuff/optimize/profile_input.py` ; les 4 chemins existent (`[ -e ]` → OK pour les 4). Mutation B4 (jeton `build_parser()` retiré) et B5 (chemin `dofus_stuff/absent.py` ajouté) rougissent toutes deux. |
| 13 | 02-02 : `cache <sous-commande>` et `db <sous-commande>` produisent le même espace de noms modulo la clé `command`, et la section `## cache` déclare l'alias sans reproduire les trois descriptions de `## db` | ✓ VERIFIED | Mesure indépendante des **5** sous-commandes (`status`, `stats`, `sync`, `fill`, `clear`) : espaces de noms égaux hors `command` pour les 5 (`True` ×5), `command` valant bien `db`/`cache`. La section `## cache` déclare « `cache` est le second nom de `db` … équivaut à `db <sous-commande>` » et les trois descriptions (`Afficher l'état de la base`, `Forcer la synchronisation complète`, `Vider la base locale`) n'apparaissent qu'une fois, dans `## db`. |
| 14 | 02-02 : le scanner de blocs et les helpers de section existent en un seul exemplaire dans `tests/conftest.py`, exposés par fixtures ; `tests/test_docs_code_anchor.py` ne les définit plus localement et reste vert (prouvé par mutation) | ✓ VERIFIED | `grep -nE "^def (_blocs_de_code\|_lignes_de_code\|_section\|_sections\|_normalize)" tests/test_docs_code_anchor.py` → **aucune ligne** ; le module consomme les fixtures `lignes_de_code`, `sections`, `section`, `normalize`. Mutation 02-02/1 reproduite : `--offline` retiré de `docs/installation.md` → `test_cli_examples_of_installation_page_parse` rouge (copie jetable : 8 passed avant, 1 failed après). **Réserve honnête :** un `_section` au contrat divergent subsiste dans `tests/test_docs_structure.py` (fichier **non modifié** par cette phase, fork pré-existant de phase 1, relevé Info IN-04) — voir Advisories. |
| 15 | 02-02 : une page `docs/cli.md` absente produit une assertion localisante nommant la page et le fichier de code, jamais un `FileNotFoundError` brut | ✓ VERIFIED | `docs/cli.md` supprimé dans une copie jetable → `AssertionError: cli.md : page introuvable (<chemin>) ; attendu la page de reference de dofus_stuff/cli.py livree dans docs/` — nomme la page, le chemin et le fichier de code. |
| 16 | 02-03 : chaque sous-commande documentée possède au moins un exemple marqué, et l'ensemble atteint est exactement les huit noms épinglés | ✓ VERIFIED | 8 blocs `console`, 8 lignes d'exemple, une par sous-commande (`version`, `self-test`, `search`, `item`, `list`, `optimize`, `db`, `cache`) ; mutations M1 (exemple `cache` supprimé) et M6 (balise `console` retirée d'un exemple) rougissent avec le constat « sans exemple ». |
| 17 | 02-03 : aucun `SystemExit` ni `ValueError` ne traverse — chaque échec devient une `AssertionError` citant la page, l'exemple fautif, la cause et `dofus_stuff/cli.py` | ✓ VERIFIED | Toutes mes 19 exécutions mutées ont produit des `AssertionError` nommant `cli.md` (jamais de trace `SystemExit`/`ValueError` en échec) ; mutation B2 (guillemet non fermé) est convertie en « non découpable par shlex.split ». |
| 18 | 02-03 : la limite D-26 est écrite dans le module (complétude inverse non revendiquée, « verbatim » = garantie de construction, « hors parcours recommandé » non décidable mécaniquement) | ✓ VERIFIED | Bloc de commentaires `tests/test_docs_cli.py` (« Limite honnete (D-26), ecrite ici et pas seulement dans le plan … ») + tableau « Assertions declarees non falsifiables » de `02-03-SUMMARY.md`. |
| 19 | 02-03 : chaque assertion de la phase porte une preuve de morsure (mutation étiquetée exécutée dans une copie jetable) consignée mutation par mutation dans `02-03-SUMMARY.md` | ✓ VERIFIED | Tables « Mutation Battery » de `02-03-SUMMARY.md` (9 lignes : mutation, motif, verdict, compteur, constat attribué) et `02-02-SUMMARY.md` (10). **Contre-preuve indépendante :** batterie personnelle de **19 exécutions** sur une copie jetable (16 classes distinctes) — 19/19 détectées avec le motif attribué, plus un contrôle non muté vert (11 passed) et un contrôle de non-discrimination des motifs. Les 19 mutations exactes des exécutants n'ont pas été rejouées une par une (non indépendamment confirmé) ; la propriété qu'elles portent est reproduite par ma propre batterie. |

**Score :** 19/19 truths verified (0 present-behavior-unverified, 0 override, 0 gap).

Aucune truth de cette phase n'est *behavior-dependent* au sens de l'agent (aucune transition d'état, aucune invariante d'annulation/nettoyage/ordonnancement) : la phase livre une page Markdown et un harnais qui *analyse* (jamais n'exécute de commande). `behavior_unverified: 0`.

### Required Artifacts

| Artifact | Expected | Status | Details |
|----------|----------|--------|---------|
| `docs/cli.md` | Référence CLI : sections par sous-commande dans l'ordre du parseur, options globales, 30 options d'`optimize` groupées, alias `cache`, avertissement destructeur, bloc Source de vérité, ligne de retour (`contains: "# CLI"`, `min_lines: 90`) | ✓ VERIFIED | 195 lignes / 9 381 octets ; H1 `# CLI` ; 8 sections de sous-commande dans l'ordre ; 4 tables d'`optimize` + table des options globales + table des cinq verbes ; `## Source de vérité` ; ligne de retour. Commité en vague 1 (`8c96674`, `d778063`, `dcb65bc`) et **jamais modifié ensuite** (`git log -- docs/cli.md` s'arrête à `dcb65bc` ; `git status --porcelain -- docs` vide → le harnais n'a pas plié la page pour faire passer les tests). |
| `docs/sommaire.md` | Ligne d'index `CLI` pointant vers `cli.md`, livrée dans la même unité de travail (`contains: "[CLI](cli.md)"`, `min_lines: 20`) | ✓ VERIFIED | 22 lignes ; tableau `Index` avec `[CLI](cli.md)` ; entrée ajoutée en vague 1. |
| `tests/test_docs_cli.py` | Module d'ancrage CLI (`contains: SONDES_SOUS_COMMANDES`, `min_lines: 120` / `def test_commande_destructrice_avertie_et_jamais_dans_un_exemple(`, `min_lines: 240`) | ✓ VERIFIED | 1 060 lignes, 11 tests, 0 test désactivé, 0 marqueur de dette. Contient les deux jetons exigés et les trois batteries (sous-commandes/options/défauts, alias, exemples/defaults) . |
| `tests/conftest.py` | Scanner de blocs unique + helpers de section exposés par fixtures (`contains: "def _blocs_de_code("`, `min_lines: 165` / `BALISE_EXEMPLE`, `min_lines: 175`) | ✓ VERIFIED | 262 lignes ; `_blocs_de_code`, `_lignes_de_code`, `_lignes_exemple`, `_sections`, `_section(texte, titre, page)`, fixtures `lignes_de_code`, `lignes_exemple`, `sections`, `section`, `docs_dir`, `normalize`. |
| `tests/test_docs_code_anchor.py` | Module de la page d'installation consommant les fixtures, sans définition locale (`contains: "def test_cli_examples_of_installation_page_parse("`, `min_lines: 240`) | ✓ VERIFIED | 255 lignes ; aucune définition locale des helpers partagés ; 8 tests verts. |

Aucun artefact manquant, aucun stub : aucune ligne de la page n'est un remplissage (`problemes_encodage` vert), et les 11 options sans `help` sont décrites par leur nom et leur défaut — c'est la forme prescrite par D-19, pas un placeholder.

### Key Link Verification

| From | To | Via | Status | Details |
|------|----|-----|--------|---------|
| `docs/sommaire.md` | `docs/cli.md` | ligne d'index, cible relative égale au chemin relatif à `docs/` | ✓ WIRED | `[CLI](cli.md)` ; `test_sommaire_links_resolve` + `test_all_relative_links_resolve` verts. |
| `docs/cli.md` | `docs/sommaire.md` | dernière ligne, lien relatif sans ancre | ✓ WIRED | `[Retour au sommaire](sommaire.md)` ; `test_pages_have_back_link` vert. |
| `docs/cli.md` | `dofus_stuff/cli.py` | bloc Source de vérité nommant `build_parser()`, défauts relevés par `parse_args` | ✓ WIRED | Mutation B4 (jeton retiré) → rouge ; **37/37** défauts recoupés indépendamment par moi contre le parseur (33 lignes de sous-commandes/`optimize` + 4 options globales sondées séparément sur le parseur racine) ; 0 ancre, 0 chemin absolu, 0 `../` dans la page. |
| `docs/cli.md` | `dofus_stuff/database.py` | bloc Source de vérité pour la suppression effective par `db clear` | ✓ WIRED | Chemin existant ; page : « `DELETE FROM items` puis `DELETE FROM meta`, sans aucune confirmation » et « Aucun fichier n'est supprimé du disque » — conforme à `Database.clear` (revue §Vérifications point 4, recoupée en lecture source). |
| `tests/test_docs_cli.py` | `dofus_stuff/cli.py` | `build_parser().parse_args` sur chaque sonde épinglée | ✓ WIRED | Import unique `from dofus_stuff.cli import build_parser` ; mutation B7 (renommage de `self-test` **dans la copie du parseur**) → rouge avec le motif `self-test`, ce qui prouve que le test interroge bien le parseur vivant. |
| `tests/test_docs_cli.py` | `docs/cli.md` | lecture UTF-8 explicite, présence des jetons, extraction des lignes de tableau et des exemples marqués | ✓ WIRED | `_texte_page` (UTF-8 strict + assertion localisante) ; mutations M2/M3/M4/M5/M7/B1/B2/B3/B5/B6 rouges. |
| `tests/test_docs_code_anchor.py` | `tests/conftest.py` | fixtures `lignes_de_code`, `sections`, `section` | ✓ WIRED | Aucune définition locale ; mutation 02-02/1 (`--offline` retiré de la page d'installation) → `test_cli_examples_of_installation_page_parse` rouge : le scanner partagé sert toujours la page d'installation. |
| `tests/conftest.py` | `docs/installation.md` | le scanner partagé continue de servir la page d'installation, comportement inchangé | ✓ WIRED | Idem ci-dessus ; les 8 tests du module d'ancrage de la page d'installation sont verts. |

### Data-Flow Trace (Level 4)

| Artifact | Data Variable | Source | Produces Real Data | Status |
|----------|---------------|--------|--------------------|--------|
| `docs/cli.md` (noms de sous-commandes, options, défauts) | jetons épinglés du harnais | `build_parser().parse_args` sur le parseur public (`dofus_stuff/cli.py`) | Oui — 8 sous-commandes, 4 options globales, 30 options d'`optimize`, 37 défauts lus par différence d'espaces de noms | ✓ FLOWING |
| `docs/cli.md` (exemples) | `lignes_exemple` (blocs ` ```console `) | texte de la page, puis `shlex.split` → `build_parser().parse_args` | Oui — 8/8 analysés sans exécution | ✓ FLOWING |
| `docs/cli.md` (avertissement destructeur) | `JETON_DESTRUCTEUR` / `JETON_AVERTISSEMENT` | regex sur le texte entier de la page (jamais par section) | Oui — 3 lignes citantes, 3 avec avertissement ; aucune dans un bloc marqué | ✓ FLOWING |
| `docs/sommaire.md` (entrée d'index) | libellé d'index | H1 réel de la page, comparés après normalisation (D-11) | Oui — `CLI` == `# CLI` | ✓ FLOWING |

Aucune valeur affichée ne se termine dans un littéral statique ou un mock : les seules valeurs numériques de la page (défauts, codes de retour) sont comparées à celles rendues par le parseur ou au code de `main()`.

### Behavioral Spot-Checks

| Behavior | Command | Result | Status |
|----------|---------|--------|--------|
| Les 8 exemples marqués sont analysables par le parseur réel | `.venv/Scripts/python.exe` — `shlex.split` + `parse_args` sur chaque ligne des blocs `console` | 8/8 `OK` | ✓ PASS |
| La suite complète est verte avec l'interpréteur épinglé | `.venv/Scripts/python.exe -m pytest -q` | `169 passed in 2.56s` | ✓ PASS |
| Les exemples de la page d'installation restent analysables via le scanner partagé | `.venv/Scripts/python.exe -m pytest tests/test_docs_code_anchor.py -q` | `8 passed` | ✓ PASS |
| Égalité `cache`/`db` prouvée par le parseur public | `parse_args(["db",sc])` vs `["cache",sc]` pour les 5 verbes | Égaux hors `command` : 5/5 `True` | ✓ PASS |
| `db status --offline` est refusé (forme fautive enseignée) | `parse_args(["db","status","--offline"])` | `SystemExit(2)` | ✓ PASS |
| `stats`/`fill` apparaissent en `==SUPPRESS==` dans l'aide | `parse_args(["db","--help"])` / `(["cache","--help"])` (sorties capturées) | 2 occurrences chacune | ✓ PASS |
| `.data/` n'est pas écrite | `stat -c %y .data/dofus.sqlite3` avant/après | `2026-09-06 23:27:36 +0200` inchangé | ✓ PASS |

### Probe Execution

N/A — aucun probe n'est déclaré ni conventionnel : il n'existe pas de dossier `scripts/` et aucun `probe-*.sh` sur le disque (`find . -name "probe-*.sh"` → aucun résultat ; la phase est documentaire, pas une migration ni un outillage scripté).

### Mutation / Bite Checks (contre-preuve indépendante du harnais)

Le harnais n'est pas cru sur parole : j'ai copié `docs/`, `tests/`, `dofus_stuff/`, `fetcher.py`, `README.md` sous `%TEMP%/verify02` (hors du dépôt, **jamais** sous `.data/`), vérifié l'identité octet du parseur copié (`md5 ee183ea9…` identique) et joué **19 exécutions de mutation** (16 classes distinctes) :

| Contrôle | Mutation | Verdict | Motif attribué présent |
|----------|----------|---------|------------------------|
| Contrôle | copie **non mutée** | vert (`11 passed`) | — (0 occurrence des motifs attendus) |
| M1 | seul exemple de `cache` supprimé | DETECTEE | `sans exemple`, `cache` |
| M2 | défaut `--top-k` `30` → `31` dans la page | DETECTEE | `--top-k`, `30` |
| M3 | `--offline` déplacé après `db status` | DETECTEE | `cli.md` |
| M4 | mot « destruct* » retiré de la ligne `db clear` | DETECTEE | `destruct` |
| M5 | une description de `db` dupliquée dans `## cache` | DETECTEE | `duplique` |
| M6 | balise `console` retirée d'un exemple | DETECTEE | `sans exemple`, `search` |
| M7 | option globale inventée `--fictif` ajoutée à la table | DETECTEE | `--fictif` |
| M8 | commentaire de fin de ligne ajouté à un exemple | DETECTEE | `item` |
| B1 | `--page` → `--pages` dans un exemple | DETECTEE | `--pages` |
| B2 | guillemet non fermé dans un exemple | DETECTEE | `shlex` |
| B3 | toutes les lignes de tableau d'options supprimées | DETECTEE | `lignes de tableau`, `trois colonnes` |
| B4 | jeton `build_parser()` retiré du bloc Source de vérité | DETECTEE | `build_parser` |
| B5 | chemin `dofus_stuff/absent.py` ajouté au bloc Source de vérité | DETECTEE | `absent` |
| B6 | titre `## Source de vérité` renommé | DETECTEE | `Source de vérité` |
| B7 | `self-test` renommé **dans la copie du parseur** | DETECTEE | `self-test` |
| B8 | description de `db` dupliquée dans `cache` (rappel) | DETECTEE | `duplique` |
| B9 | `from dofus_stuff.database import Database` injecté dans le module d'ancrage | DETECTEE | `hors du parseur public` |
| 02-02/1 | `--offline` retiré de `docs/installation.md` | DETECTEE | `test_cli_examples_of_installation_page_parse` |
| garde | `docs/cli.md` supprimé | DETECTEE | `cli.md : page introuvable … ; attendu la page de reference de dofus_stuff/cli.py` |

Après la dernière mutation, la copie a été restaurée et vérifiée octet à octet contre le dépôt (`md5` identiques pour `cli.md`, `cli.py`, `test_docs_cli.py`) ; le dépôt lui-même n'a jamais été muté (`git status --porcelain -- docs tests dofus_stuff README.md` vide).

### Requirements Coverage

| Requirement | Source Plan | Description | Status | Evidence |
|-------------|-------------|-------------|--------|----------|
| **CLI-01** | 02-01 (`requirements: [CLI-01, CLI-02, CLI-03]`), 02-02 (`[CLI-01, CLI-02]`) | Chaque sous-commande documentée de `fetcher.py` est réellement analysable par le parseur d'arguments du code | ✓ SATISFIED | Truths 1, 8, 16 : 8/8 exemples et 8/8 sondes d'argv complets acceptés par `build_parser().parse_args` ; la page cite les 8 noms via des sections de niveau 2 dans l'ordre du parseur. Plan 02-01, 02-02 `[x]` dans `REQUIREMENTS.md:41`. |
| **CLI-02** | 02-01, 02-02 | Chaque option globale et chaque option d'optimisation documentée est réellement analysable par le parseur | ✓ SATISFIED | Truths 2, 9, 10, 13 : 4 options globales acceptées devant leur sous-commande, 30 options d'`optimize` acceptées avec valeur d'essai, toute option citée par une ligne de tableau sondée (option inventée = rouge, mutations M7/B1), alias `cache` prouvé équivalent sur les 5 verbes. `REQUIREMENTS.md:42` `[x]`. |
| **CLI-03** | 02-01, 02-03 (`[CLI-03]`) | Chaque exemple de commande cité dans `docs/cli.md` est analysable et apparaît verbatim dans la page | ✓ SATISFIED | Truths 3, 4, 5, 16, 17 : 8 exemples extraits des blocs `console`, `shlex` + `parse_args` 8/8, témoin unique `--offline optimize`, garde destructrice verte et mordante (M4/M6/M8). La composante « verbatim » est satisfaite par construction (limite déclarée D-26, cf. Advisories). `REQUIREMENTS.md:43` `[x]`. |

**Exigences orphelines :** aucune. `grep -E "Phase 2" .planning/REQUIREMENTS.md` ne renvoie que `CLI-01, CLI-02, CLI-03` (ligne 146), et les trois sont réclamées par au moins un plan (`requirements:` des trois plans). Aucun identifiant `DOCS-*` n'est réclamé par cette phase : `DOCS-06` reste une **hypothèse de provenance** dans `PROJECT.md` (« Les commandes et options CLI documentées existent réellement dans le parsing d'arguments »), ce qui est exactement le contrat de CLI-01…03 et ne comporte aucune exigence de table récapitulative.

### Decision Coverage

`gsd_run query check.decision-coverage-verify` → `{ total: 16, honored: 16, not_honored: [] }` — « All trackable CONTEXT.md decisions are honored by shipped artifacts. » Les décisions D-11…D-31 (dont D-16 sections par sous-commande, D-17 pas de table récapitulative, D-18/D-19 tables thématiques et aucune sémantique inventée, D-20/D-21 alias prouvé par le parseur, D-22/D-23 avertissement destructeur, D-24/D-25 exemples marqués et double contrôle, D-26 limite honnête, D-28 entrée d'index, D-30 gabarit, D-31 conventions de test) sont retrouvées dans les artefacts livrés. Aucune décision non honorée.

### Test Quality Audit

| Test File | Linked Req | Active | Skipped | Circular | Assertion Level | Verdict |
|-----------|-----------|--------|---------|----------|-----------------|---------|
| `tests/test_docs_cli.py` | CLI-01, CLI-02, CLI-03 | 11 | 0 | non | Valeur / comportemental (défauts comparés à la valeur rendue par le parseur ; exclusions et ordre d'options vérifiés par sonde) | ✓ OK |
| `tests/conftest.py` (helpers partagés) | CLI-01…03 | n/a (fixtures) | 0 | non | n/a | ✓ OK |
| `tests/test_docs_code_anchor.py` | CLI-01 (page d'installation) | 8 | 0 | non | Valeur | ✓ OK |
| `tests/test_docs_structure.py` | SOMM-01…03, INST-03 (hérités) | 14 | 0 | non | Valeur | ✓ OK |

- **Tests désactivés sur une exigence :** 0 (`grep -E "pytest\.mark\.skip|pytest\.skip|xfail|\.todo"` sur les 4 modules → aucune occurrence).
- **Motifs circulaires :** 0. Aucun module de test n'écrit de fichier ni de valeur attendue ; les valeurs attendues sont mesurées *depuis le parseur public* (oracle externe au harnais), et la page est verrouillée par `git log` depuis la vague 1 — elle n'a pas été alignée sur les tests.
- **Assertions insuffisantes :** 0. La seule faiblesse déclarée (l'assertion « verbatim » tautologique, IN-01) est classée en Advisories : elle ne porte pas l'exigence à elle seule (le volet `shlex` + `parse_args` est, lui, falsifiable et falsifié par M3/B1/B2).
- **Quantité :** non prescrite par les exigences.

### Anti-Patterns Found

| File | Line | Pattern | Severity | Impact |
|------|------|---------|----------|--------|
| `tests/test_docs_cli.py` | 828-833 environ | Assertion « verbatim » tautologique (`ligne in texte` avec `ligne` extraite de `texte`) — déclarée D-26 | ℹ️ Info | Branche morte, ne protège rien ; ne porte pas CLI-03 seule. Relevé IN-01 de `02-REVIEW.md`, non bloquant. |
| `tests/test_docs_cli.py` | 991-1055 | Garde `ast` plus étroite que son énoncé (imports + appel `main` seulement ; ni `open`, ni `connect`, ni `os.system`, ni constante `.data`) | ℹ️ Info | La propriété est vraie aujourd'hui (mesurée : `.data` inchangée, aucun import d'exécution) mais le contrôle ne la couvrirait pas d'une régression future. IN-02, non bloquant. |
| `tests/test_docs_structure.py` | 223 | `_section` privé concurrent de la fixture partagée `section` (contrat divergent) — fichier **non modifié** par la phase | ℹ️ Info | Fork pré-existant (phase 1) ; IN-04. N'affaiblit aucun contrôle de la phase 2. |
| `tests/test_docs_cli.py` | 164-166 | `OPTIONS_GLOBALES_A_VALEUR` recopie à la main l'arité des options globales | ℹ️ Info | Risque de faux rouge si une future option globale à valeur apparaît dans un exemple. IN-05, non bloquant. |
| `docs/cli.md` | 26-30 et 168-172 | Même affirmation et même bloc `text` (`Erreur : --offline incompatible avec db sync`) écrits deux fois | ℹ️ Info | Redondance exacte et correcte aujourd'hui ; « une seule source par énoncé » (D-17) visait la table récapitulative, pas cette reprise. IN-07, non bloquant. |
| `docs/sommaire.md` | 5-13 | « Parcours conseillé » nomme cinq pages non encore livrées (liste **sans liens**) | ℹ️ Info (deferred) | Voir section Deferred : couvert par le critère 3 de la phase 6 (D-05/D-28). IN-06, non bloquant. |

**Marqueurs de dette (`TBD`/`FIXME`/`XXX`) dans les fichiers modifiés par la phase :** **aucun** (`grep -nE "TBD|FIXME|XXX|TODO|HACK|PLACEHOLDER"` sur `docs/cli.md`, `docs/sommaire.md`, `tests/conftest.py`, `tests/test_docs_cli.py`, `tests/test_docs_code_anchor.py` → aucune ligne). Aucun `TODO`/`FIXME` non plus dans les 4 modules de test liés aux exigences. Pas de gate « debt marker » déclenché.

### Prohibitions (must-NOT)

**Test-tier (8/8 avec une mise en œuvre câblée — aucun `flagged` en fail-closed) :**

| Prohibition (plan) | Mise en œuvre | Verdict |
|--------------------|---------------|---------|
| 02-01 : aucun exemple marqué ne cite une commande destructrice ou réécrivant la base, ni commentaire/continuation/métacaractère | `_lignes_exemple` + `shlex.split` + `parse_args` | APPLIQUÉE — mutations M6/M8/B2 rouges |
| 02-01 : aucune ancre, aucun chemin absolu, aucun sous-dossier sous `docs/`, aucune modification de `dofus_stuff/**` ni de `README.md` | `test_no_anchor_or_absolute_links`, `test_all_relative_links_resolve`, `test_documents_are_utf8_and_not_drafts` + `git status` | APPLIQUÉE — 0 ancre / 0 absolu / 0 `../` dans `cli.md` ; phase 2 n'a touché que `docs/cli.md`, `docs/sommaire.md`, 3 fichiers de `tests/` |
| 02-02 : aucun `SystemExit` ni `ValueError` laissé traverser | `_accepte`, `_jetons`, `_espace_de_noms_brut` convertissent en `AssertionError` | APPLIQUÉE — 19/19 sorties de mutation portent une `AssertionError` localisante |
| 02-02 : aucune exécution de commande, aucun `main()`, aucune base, aucun réseau, aucune écriture sous `.data/` | garde `ast` (`INTERDITS_EXECUTION`, `IMPORT_PRODUIT_AUTORISE`) | APPLIQUÉE (périmètre d'import/appel ; réserve IN-02 sur l'étroitesse) |
| 02-02 : aucune mutation appliquée à l'arbre livré | copies jetables uniquement | APPLIQUÉE — `git status` vide, `docs/cli.md` figé depuis la vague 1 |
| 02-03 : aucune commande documentée n'est exécutée | garde `ast` + aucun `subprocess`/`socket`/`sqlite3` importé | APPLIQUÉE — mutation B9 rouge |
| 02-03 : aucune exécution de `main()`, aucune écriture `.data/`, aucun réseau | idem + `.data` mtime inchangé | APPLIQUÉE |
| 02-03 : aucune règle destructive/ni d'exemple évaluée par section ; motif du jeton destructeur couvrant `db clear` et `cache clear` avec espaces quelconques | regex sur le texte entier, ligne à ligne (3 lignes citantes détectées) | APPLIQUÉE — M4 verte avant/rouge après |

**Judgment-tier (4 — jugements LLM, non autoritaires ; `unverified-prohibition — human review recommended`, aucun n'est bloquant et aucun n'est silencieux) :**

| Prohibition (plan) | Verdict LLM | Élément examiné |
|--------------------|-------------|-----------------|
| 02-01 : aucune table récapitulative unique de toute la surface CLI en fin de page (D-17) | respectée | Lecture intégrale de `docs/cli.md` : toutes les tables sont **locales** (options globales, options propres d'une section, cinq verbes de `db`) ; aucune table ne couvre l'ensemble des sous-commandes/options, aucune en fin de page. |
| 02-01 : aucun lien direct de `README.md` vers `docs/cli.md`, et `README.md` non modifié | respectée | `git log -- README.md` s'arrête à `a8f080b` (phase 1) ; phase 2 ne modifie pas `README.md` (`git show --name-only` des 12 commits) ; `grep -c "cli.md" README.md` → 0. |
| 02-01 : aucune sémantique inventée pour les 11 options d'`optimize` sans `help` | respectée | Les 11 options sont exactement celles que le parseur déclare sans `help` (compté : `--base-vit/str/cha/agi/wis` + 6 `--scroll-*`, `--base-int` ayant un `help`) ; la page écrit pour chacune « aucune description dans l'aide du parseur » et n'ajoute aucun sens. |
| 02-03 : aucune mutation encodée en dur dans le module, aucun nom de page non livré cité par une assertion | respectée | `grep` des noms de pages dans `tests/test_docs_cli.py` : seul `cli.md` (la page livrée) est cité comme page ; les seules constantes de mutation sont des messages d'attente, aucune copie jetable n'est scriptée dans le module (le test de mutation formel est planifié en phase 6, GARD-03). |

### Deferred Items

| # | Item | Addressed In | Evidence |
|---|------|-------------|----------|
| 1 | « Parcours conseillé » de `docs/sommaire.md` nomme cinq pages pas encore livrées | Phase 6 | ROADMAP Phase 6, critère de succès 3 : « Les 8 pages épinglées sont toutes livrées … et le sommaire **propose un parcours conseillé final** » ; D-05 (le sommaire croît par phase) et D-28 (seule l'entrée `cli.md` est ajoutée maintenant). La liste ne contient **aucun lien** : aucun lien mort n'est créé. |

Aucun autre candidat-gap n'a été trouvé ; cet item est le seul filtré comme différé.

### Advisories (constats non bloquants, laissés visibles)

| # | Finding | Catégorie | Pourquoi advisory / ce qui le résoudrait |
|---|---------|-----------|------------------------------------------|
| A1 | **Écart assumé avec `.claude/CLAUDE.md` §2 (DOCS-06)** : l'instruction de projet prescrit pour `cli.md` « un tableau commande → rôle → exemple » unique ; la page livre une section par sous-commande (D-16) et pas de table récapitulative (D-17) | Other | Les critères de succès du ROADMAP, `PROJECT.md` DOCS-06 et CLI-01…03 n'exigent aucune table récapitulative ; les décisions D-16/D-17 ont été verrouillées en discussion puis honorées (decision coverage 16/16). Le conflit est **déjà consigné** dans `.planning/WINDOWS.md` (entrée 2, `open`) mais reste visible dans un fichier généré lu par les phases suivantes : résolution = amender `§2` de `.claude/CLAUDE.md` (hors périmètre de la phase 2) ou waive l'entrée. |
| A2 | **Entrée `open` de phase 1 dans `.planning/WINDOWS.md` (id 1)** : squelette `docs/installation.md` livré par 01-02 depuis longtemps | Other | Pré-existant, hors périmètre de la phase 2 (fichier non modifié par elle) ; `/gsd-ship` bloque sur `open_count > 0` **seulement si** `workflow.windows_enforce` est activé — la clé est absente de `.planning/config.json`. À traiter par `windows fixed 1` ou une waiver, au niveau milestone. |
| A3 | **`02-VALIDATION.md` en-tête `status: draft`, `nyquist_compliant: false`, sign-off `pending`** | Other | Aucun `must_have` ni critère de succès ne porte ces champs ; la propriété de Nyquist de la phase (chaque assertion a une mutation planifiée + résultat consigné) est portée par les tables « Mutation Battery » des SUMMARY et **reproduite** par ma batterie. Résolution = porte de phase (`validate-phase`), pas cette vérification. |
| A4 | **`docs/cli.md` — mention « hors parcours recommandé »** : la moitié de SC4b « jamais dans un parcours recommandé » n'est pas décidable mécaniquement | Other | La page ne comporte **aucune** section de parcours recommandé, et la commande n'apparaît que sous un titre qui la classe destructive : l'approche par co-présence + absence de tout bloc marqué prouve le critère tel qu'il s'applique à cette page. Écrit dans le module (D-26) et dans `02-VALIDATION.md`. |
| A5 | **Complétude `parseur → page` non revendiquée (D-26)** : une sous-commande/option ajoutée plus tard sans être documentée ne fera pas rougir la suite ; `SONDES_OPTIMIZE` reflète à la main l'arité du parseur (IN-05) | Other | Choix explicite D-26, écrit dans le module et dans les plans ; le sens exigé (page → parseur) est couvert dans les deux sens pour les 8 sous-commandes et les 34 options citées. Résolution = contrôle d'énumération `parseur → page` en phase 6 (GARD-03/GARD-04) si le projet le veut. |
| A6 | **Garde `ast` plus étroite que son énoncé (IN-02)**, assertion « verbatim » tautologique (IN-01), `_section` forké dans `test_docs_structure.py` (IN-04), duplication du paragraphe `--offline`/`db sync` (IN-07) | Other | Constats **Info** de `02-REVIEW.md`, tous vérifiés sans effet sur un `must_have` : la propriété visée est vraie aujourd'hui et mesurée (`.data` inchangée, aucune écriture du module, 8 exemples analysés). Ce sont des durcissements de harnais, pas des écarts de livrable. |

### Human Verification Required

**Aucune vérification humaine n'est requise** — et je ne demande pas de contrôle manuel qui ferait doublon avec un contrôle automatisé. Raisons, explicites :

1. **Les deux « manual-only verifications » déclarées par `02-VALIDATION.md` ont été réduites à des contrôles déterministes qui prouvent le même critère** : (a) « `db clear` hors parcours recommandé » → la page ne contient aucun parcours recommandé et les 3 lignes citantes portent toutes `destruct*` sur la même ligne (compté : 3/3) ; (b) « classer quelles sous-commandes sont destructrices » → `dofus_stuff/database.py::Database.clear` supprime `items` et `meta` sans confirmation, `db sync`/`cache fill` re-tirent de l'API sans donnée utilisateur : la classification par la page correspond au code, vérifiée en lecture source (prise de position du vérificateur, pas une action humaine).
2. **Aucune truth n'est comportementale** (ni transition d'état, ni invariante d'annulation/nettoyage/ordonnancement) et **aucune truth n'est `verification: backstop`** (`grep backstop` dans les trois plans → aucune occurrence) : il n'y a donc ni `behavior_unverified` ni `insufficient_spec` à router.
3. **Ce que je ne revendique pas.** La lisibilité/qualité rédactionnelle en français de `docs/cli.md` n'est pas mesurée par un contrôle automatique et ne pourrait l'être ; elle **n'est pas un `must_have`** (aucun critère de succès du ROADMAP, aucune exigence CLI-01…03 ni aucune décision D-16…D-31 ne porte sur la qualité de la prose). Je ne demande pas de humain pour ce point parce qu'aucun critère d'acceptation n'en dépend ; je le signale ici pour que personne ne lise ce rapport comme une validation rédactionnelle. Proxy automatisé essayé en premier : présence d'un H1 unique et d'une phrase d'introduction conforme au gabarit, absence de jeton de brouillon (`test_documents_are_utf8_and_not_drafts`), respect du gabarit de la page d'installation — insuffisant pour juger du style, suffisant pour les invariants documentaires exigés.

### Gaps Summary

Aucun gap. Les 19 must-haves (5 critères de succès du ROADMAP fusionnés avec les truths des trois plans) sont vérifiés, les 5 artefacts exigés existent et sont substantiels, les 8 key links sont câblés, la donnée circule réellement depuis le parseur public, les 3 exigences CLI-01/02/03 sont satisfaites sans orpheline, la couverture des décisions est de 16/16, aucun marqueur de dette n'existe, et le harnais **mord** : ma batterie indépendante de 19 exécutions de mutation est détectée 19/19 sur une copie jetable, avec le motif attribué, tandis que la copie non mutée (et le dépôt) restent verts — `169 passed in 2.56s`.

Ce qui reste ouvert est explicitement listé comme Advisory (A1…A6) ou différé en phase 6 (parcours conseillé du sommaire) : aucun de ces points n'est un must-have violé. Les 4 prohibitions de tier « judgment » sont jugées ci-dessus avec leur élément examiné, signalées comme non autoritaires, et laissées visibles pour une revue humaine éventuelle (`unverified-prohibition — human review recommended`) — jamais absorbées silencieusement dans le verdict.

---

_Verified: 2026-09-11T12:54:34Z_
_Verifier: Claude (gsd-verifier)_
