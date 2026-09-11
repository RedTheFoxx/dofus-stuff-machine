---
phase: 02-r-f-rence-cli-align-e-sur-le-parseur
reviewed: 2026-09-11T12:40:33Z
depth: standard
files_reviewed: 5
files_reviewed_list:
  - docs/cli.md
  - docs/sommaire.md
  - tests/conftest.py
  - tests/test_docs_code_anchor.py
  - tests/test_docs_cli.py
findings:
  critical: 0
  warning: 5
  info: 7
  total: 12
status: issues_found
fixes_applied: 5/5 warnings (commit a650032)
---

# Phase 2: Code Review Report

**Reviewed:** 2026-09-11T12:40:33Z
**Depth:** standard (per-file + cross-file, avec sondes exécutées dans des copies jetables)
**Files Reviewed:** 5
**Status:** issues_found

## Summary

Revue adversariale de la phase 2 (documentation CLI + harnais d'ancrage). Le **livrable est exact** :
toutes les affirmations de `docs/cli.md` que j'ai pu sonder mécaniquement sont vraies (37 valeurs par
défaut sur 37, message et code de retour de `db status --offline`, littéral `==SUPPRESS==` de
`stats`/`fill`, table d'alias, incompatibilité `--offline` / `db sync`, nature destructrice de
`db clear` lue dans `dofus_stuff/database.py`), la suite est verte (**168 passed**, conforme au
SUMMARY de 02-03), et aucune des garanties de sûreté ne fuit : aucun test n'exécute `main()`, aucune
base n'est ouverte, `.data/dofus.sqlite3` garde son horodatage après la suite complète.

Les défauts trouvés sont donc **des trous du harnais, pas des erreurs du produit** : ce sont
exactement les endroits où la page pourrait dériver plus tard sans qu'aucun test ne rougisse. J'ai
mesuré chacun d'eux en exécutant la suite sur des copies jetables (`/tmp`), jamais sur l'arbre livré.

Les cinq constats de niveau Warning :

1. **Aucune valeur par défaut documentée n'est vérifiée** : cinq colonnes « Défaut » falsifiées
   simultanément laissent la suite au vert (WR-01). Le chaînage « défauts relevés dans le parseur »
   revendiqué par la page (ligne 3) et par D-16 n'a aucune assertion derrière lui.
2. La garde de la commande destructrice ne couvre que `clear` : un exemple marqué
   `python fetcher.py --offline db sync` (réseau + réécriture de la base, D-23 / T-02-15) passe.
3. `python fetcher.py --help` — exemple légitime pour une page de référence — est déclaré « refusé
   par le parseur » (`SystemExit(0)` pris pour un refus).
4. « Décrite une seule fois » n'est vérifié que par l'**absence** dans `## cache` : la table des cinq
   verbes de `## db` peut disparaître sans qu'aucun test ne rougisse ; et le constat « la
   sous-commande est citée » est un test de sous-chaîne satisfait par le mot `items`.
5. La tolérance d'`argparse` aux préfixes rend invisible un **renommage d'option côté parseur** (le
   scénario « documentation périmée » que le projet doit empêcher), alors que la vérification stricte
   est disponible par API publique — la justification écrite dans le module est factuellement fausse.

Aucun **Critical** : je n'ai trouvé aucune affirmation fausse dans `docs/cli.md`, aucune écriture sous
`.data/`, aucun accès réseau, aucune exécution de commande, aucun secret, aucune injection. Les
défauts ci-dessus sont des risques de dérive future, pas des comportements incorrects livrés.

## Narrative Findings (AI reviewer)

### Critical Issues

Aucun constat de sévérité Critical. Ce n'est pas un oubli : j'ai cherché les cinq classes de défauts
critiques et je les ai écartées par mesure — (a) exactitude des affirmations de la page : 37/37
défauts et 4 faits de parseur vérifiés (voir « Vérifications passées »), aucune contradiction
trouvée ; (b) destruction/vidage : `db clear` n'est ni exécuté ni proposé en exemple marqué, garde
vérifiée mordante (elle rougit bien sur son motif) ; (c) accès à `.data/` : horodatage inchangé après
la suite complète (168 tests) ; (d) réseau : aucun exemple marqué n'utilise `db sync` / `cache fill`,
et aucun test n'ouvre de socket ; (e) secrets/injection/desérialisation : surface inexistante dans
ces cinq fichiers (documentation Markdown et tests de lecture d'`argv`).

### Warnings

#### WR-01 : Les valeurs par défaut documentées ne sont vérifiées par aucune assertion

**File:** `tests/test_docs_cli.py:92-138` (liste épinglée `SONDES_OPTIMIZE`), `:289-305`
(`_option_optimize_acceptee`), `:327-395` (les deux tests d'options) ; page concernée
`docs/cli.md:11-16`, `:51-58`, `:76-83`, `:100-148`

**Issue :** toute la vérification des options s'arrête à « le jeton est accepté par
`parse_args` ». La troisième colonne des tableaux (« Défaut ») n'est lue par **aucun** test : la
chaîne `default` n'apparaît nulle part dans `tests/test_docs_cli.py`, `tests/conftest.py`,
`tests/test_docs_anchor*.py` ni `tests/test_docs_structure.py`. Or c'est la promesse centrale de la
page (`docs/cli.md:3` : « les valeurs par défaut relevées dans le parseur ») et de D-16/D-18. Un
relecteur qui change `30` en `300` dans la page ne reçoit aucun signal.

**Scénario d'échec (mesuré) :** copie jetable de `docs/` + `tests/` ; cinq cellules falsifiées
(`--top-k` `30`→`300`, `--time-limit` `5.0`→`99.0`, `--timeout` `15`→`7`, `--limit` `10`→`99`,
`--jet` `average`→`max`) ; `pytest tests/test_docs_cli.py -q` → **`1 failed, 9 passed`**, soit
exactement le résultat de la copie non mutée (l'unique échec est le contrôle de chemins de 02-02,
rouge par construction dans une copie sans l'arbre produit — voir « Vérifications passées », point
9). Les cinq falsifications passent donc inaperçues.

**Fix :** lire la colonne « Défaut » et la comparer au parseur, avec le patron déjà présent dans le
dépôt (`tests/test_docs_code_anchor.py::test_adresse_par_defaut_documentee`, qui dérive l'adresse
attendue de `build_parser().parse_args([])`). Par exemple :

```python
attendu = build_cli_parser().parse_args(["optimize"])   # + ["search","x"], ["list"], ["version"]
namespace = vars(attendu)
assert str(namespace["top_k"]) == "30", ...   # lu dans la cellule de docs/cli.md
```

Traiter séparément les cas non littéraux de la page : `faux` (→ `False`), `aucun`/`aucune`
(→ `None`), `0` (→ `0.0`), et `--data-dir` (cellule « le dossier `.data/` à la racine du dépôt »,
comparaison par nom de dossier `.data` du chemin résolu).

#### WR-02 : La garde de la commande destructrice ne couvre pas `db sync` / `cache fill`

**File:** `tests/test_docs_cli.py:168-171` (`JETON_DESTRUCTEUR`), `:624-677`
(`test_commande_destructrice_avertie_et_jamais_dans_un_exemple`) ; page concernée `docs/cli.md:168`

**Issue :** D-23 classe comme destructrices `db clear` **et** `db sync` / `cache fill` (« qui
réécrivent la base »), et exige que chacune apparaisse avec son avertissement et hors de tout
parcours conseillé. Le motif de la garde est `(?:db|cache)\s+clear` : il ne peut rien dire de
`db sync` / `cache fill`. Le plan 02-03 en fait un constat humain (T-02-15 : « aucun exemple marqué
ne contient `db sync` ni `cache fill` ») qui est un **fait sur la page livrée**, pas un test : rien
n'empêche un exemple marqué d'inviter le lecteur à recopier une commande qui contacte l'API Dofusdude
et réécrit la base locale.

**Scénario d'échec (mesuré) :** copie jetable ; ajout d'un bloc
```` ```console / `python fetcher.py --offline db sync` / ``` ```` dans `docs/cli.md` ;
`pytest tests/test_docs_cli.py -q` → **`1 failed, 9 passed`** (baseline inchangée). L'exemple est
analysable par le parseur, atteint une sous-commande épinglée (`db`) et ne déclenche aucune règle.

**Fix :** séparer les deux règles, sans casser la page actuelle :

```python
# (c) jamais un exemple marque : la liste vient d'un fait du parseur (D-23), pas d'un seul mot-cle
JETONS_RESEAU = re.compile(r"(?<![\w-])(?:db|cache)\s+(?:clear|sync|fill)(?![\w-])")
```

et l'utiliser pour le seul constat « l'exemple … cite la commande » (`:655-665`). Garder
`JETON_DESTRUCTEUR` (`clear` seul) pour la co-présence de l'avertissement de la règle (b) : étendre
ce dernier motif à `sync`/`fill` rendrait la page actuelle faussement rouge, la ligne 168 ne
contenant pas le jeton « destruct ».

#### WR-03 : `python fetcher.py --help` est déclaré « refusé par le parseur »

**File:** `tests/test_docs_cli.py:498-505` (`_exemple_accepte`), appelé depuis `:527-575` ;
même défaut dans `:203-212` (`_accepte`)

**Issue :** `_exemple_accepte` traduit **tout** `SystemExit` en refus, y compris le
`SystemExit(0)` qu'`argparse` lève après avoir imprimé l'aide. `python fetcher.py --help` (et
`python fetcher.py optimize --help`) est une ligne de référence parfaitement légitime pour une page
qui documente une ligne de commande ; elle serait rejetée avec un message trompeur (« exemple …
refusé par `build_parser().parse_args()` ; règles de rédaction mesurées : … »), et l'aide complète
(28 lignes) polluerait la sortie pytest, seul `stderr` étant capturé.

**Scénario d'échec (mesuré) :** `parse_args(["--help"])` → `exit code 0` + 28 lignes sur **stdout** ;
ajout d'un bloc `console` contenant `python fetcher.py --help` dans une copie jetable →
`FAILED tests/test_docs_cli.py::test_exemples_marques_sont_analysables` avec le constat « exemple
« python fetcher.py --help » refuse par le parseur » — **faux positif sur une page correcte**.

**Fix :** distinguer le succès par le code de sortie et capturer aussi la sortie standard :

```python
try:
    with redirect_stderr(io.StringIO()), redirect_stdout(io.StringIO()):
        build_cli_parser().parse_args(_jetons(ligne)[2:])
except SystemExit as sortie:
    return sortie.code in (0, None)
return True
```

Appliquer la même correction à `_accepte` (`:213`) pour que `--help` ne soit jamais compté comme
option inventée (les tableaux excluent déjà `--help` via `- {JETON_AIDE}`, mais la liste épinglée et
les exemples ne passent pas par là).

#### WR-04 : « décrite une seule fois » ne vérifie que l'absence, et « la sous-commande est citée » est un test de sous-chaîne

**File:** `tests/test_docs_cli.py:308-324` (`test_sous_commandes_documentees_et_acceptees`),
`:416-431` (contrôle anti-duplication) ; page concernée `docs/cli.md:150-186`

**Issue :** deux constats portent une règle plus large que ce qu'ils mesurent.

- (a) Le contrôle anti-duplication n'exige que l'**absence** des trois descriptions de `db` dans
  `## cache` (`:425-431`). Rien n'exige leur **présence** dans `## db`, alors que le message du
  constat promet « ces trois descriptions une seule fois, dans la section « ## db » (D-20) ». La
  propriété réellement prouvée est « non dupliquée », pas « décrite une fois » : zéro occurrence la
  satisfait.
- (b) `if nom not in texte` (`:313`) est une recherche de sous-chaîne sur toute la page.
  `item` est satisfait par le mot **`items`** de la phrase ``DELETE FROM items`` (`docs/cli.md:176`,
  trois occurrences de « item » dont celle-là) ; `version` par la prose « synchronisation de
  version » (`docs/cli.md:15`). Pire : toute page satisfaisant
  `test_chaque_sous_commande_a_un_exemple` (`:577-620`) contient nécessairement le jeton du nom de
  chaque sous-commande, donc ce constat ne peut plus être le premier à rougir — il est redondant et
  jamais porteur d'information. Enfin D-16 (une section par sous-commande, **dans l'ordre du
  parseur**) n'est vérifié nulle part.

**Scénario d'échec (mesuré) :** copie jetable ; suppression de la table entière des cinq verbes de
`## db` (`docs/cli.md:158-164`, en-tête + 5 lignes) ; `pytest tests/test_docs_cli.py -q` →
**`1 failed, 9 passed`** (baseline inchangée). La page ne décrit plus aucun verbe de `db` et la
suite reste verte.

**Fix :**
(a) après le contrôle d'absence, exiger la présence :
`for description in DESCRIPTIONS_DB: assert normalize(description) in normalize(section(texte, "## db", PAGE))` ;
(b) remplacer le test de sous-chaîne par l'existence de la section et l'ordre de D-16 :

```python
titres = [_sections(texte)]  # ou section(texte, f"## {nom}", PAGE) pour chacun des 8 noms
assert ordre_reel == [nom for nom, _ in SONDES_SOUS_COMMANDES]
```

Les huit titres existent aujourd'hui (`## version`, `## self-test`, `## search`, `## item`,
`## list`, `## optimize`, `## db`, `## cache`) et dans l'ordre du parseur : ce contrôle passerait sur
la page livrée et rougirait sur un renommage ou une suppression de section.

#### WR-05 : La tolérance d'`argparse` au préfixe rend invisible un renommage d'option dans le parseur

**File:** `tests/test_docs_cli.py:17-21` (limite écrite dans le module), `:270-305`
(`_option_globale_acceptee`, `_option_optimize_acceptee`)

**Issue :** la sonde accepte un jeton de la page dès qu'il est un **préfixe non ambigu** d'une option
réelle. La justification écrite dans le module — « exiger la forme stricte demanderait
l'introspection privee d'`argparse` interdite par D-14 » — est **fausse** : l'ensemble exact des
jetons déclarés s'obtient par API publique, `build_parser().format_help()` (déjà utilisé par
`tests/test_docs_code_anchor.py::_options_aide_web`) et, pour un sous-parseur,
`parse_args(["optimize", "--help"])` avec `stdout` capturé. Conséquence : si `dofus_stuff/cli.py`
renomme une option, la page garde l'ancien jeton et **toute la suite reste verte** — précisément la
« documentation périmée » que la valeur centrale du projet interdit.

**Scénario d'échec (mesuré) :** parseur muté en mémoire (`--force-sync`→`--force-synchronisation`,
`--top-k`→`--top-k-slot`) : `parse_args(["--force-sync","version"])` et
`parse_args(["optimize","--top-k","30"])` sont **encore acceptés** (préfixes non ambigus). Mesuré
aussi que la liste stricte est accessible publiquement : l'aide capturée du parseur racine et de
`optimize` rend exactement les jetons déclarés (`--top-k` présent, `--classic` absent), soit 35
jetons en début de ligne dont les 4 options globales et les 30 options d'`optimize`.

**Fix :** ajouter un contrôle d'appartenance stricte à côté de la sonde d'analyse, sans
introspection privée :

```python
options_reelles = set(OPTION_LONGUE.findall(build_cli_parser().format_help()))
options_reelles |= set(OPTION_LONGUE.findall(aide_capturee(["optimize", "--help"])))
inventees = sorted(citees - options_reelles)
```

et corriger le paragraphe « Limite de lecture mesuree » du module : la sonde par `parse_args` reste
le contrôle « les exemples sont analysables », mais elle ne prouve pas la forme stricte.

### Info

#### IN-01 : L'assertion « verbatim » est tautologique (déclaré, mais inerte)

**File:** `tests/test_docs_cli.py:543-548`

**Issue :** la ligne est extraite du texte auquel elle est comparée : `if ligne not in texte` ne peut
jamais être vrai. Le module et le SUMMARY de 02-03 le déclarent (D-26 : garantie de construction),
donc ce n'est pas un défaut caché — mais la branche est morte et ne protège rien.
**Fix (optionnel) :** lui donner un sens falsifiable, par exemple exiger l'unicité
(`texte.count(ligne) == 1`), ce qui détecterait un bloc dupliqué ou une ligne « ossifiée ».

#### IN-02 : La garde « aucun test n'exécute rien » est plus étroite que son énoncé

**File:** `tests/test_docs_cli.py:679-706`, docstring du module `:23-25`

**Issue :** la garde `ast` n'inspecte que les **imports** et les appels nommés `main`. Un accès
direct à la base locale ou un effet de bord passe : `Path(".data/dofus.sqlite3").read_bytes()`,
`open(...)`, `write_text`, `os.system`, ou un import indirect
(`importlib.import_module("sqlite3")`). La docstring du module annonce « rien n'est ecrit sous
`.data/` (D-15) … `test_sans_execution_ni_base_locale` verifie cette propriete » : la propriété est
vraie aujourd'hui (mesurée), mais le contrôle ne la couvre pas.
**Fix :** étendre les listes gelées aux appels et aux constantes : `open`, `connect`, `write_text`,
`write_bytes`, `system`, `popen`, `run`, et tout `ast.Constant` non-docstring contenant `.data` ou
`dofus.sqlite3`.

#### IN-03 : La docstring de `tests/conftest.py` ne décrit plus son contenu

**File:** `tests/conftest.py:1`

**Issue :** `"""Fixtures pytest pour l'interface web."""` alors que le module héberge désormais tout
le harnais documentaire partagé (scanner de blocs, `_sections`, `_section`, `_normalize`, `docs_dir`,
fixtures `lignes_de_code` / `lignes_exemple` / `sections` / `section`), conformément à D-12.
**Fix :** description d'une ligne couvrant les deux usages (fixtures web + helpers documentaires
partagés).

#### IN-04 : Deux implémentations concurrentes de « corps d'une section H2 »

**File:** `tests/conftest.py:213` (`_section(texte, titre, page)`, lève `AssertionError`) vs
`tests/test_docs_structure.py:223` (`_section(texte, titre) -> str | None`, construit sur
`texte.find`)

**Issue :** D-12 (« une seule implémentation, pas de fork ») est vrai pour le scanner de blocs, pas
pour l'extraction de section : deux helpers homonymes aux contrats divergents coexistent — l'un
exige un titre de niveau 2 exact et échoue en nommant la page, l'autre accepte n'importe quelle
occurrence de la chaîne et rend `None`. Un correctif appliqué à l'un ne l'est pas à l'autre.
**Pré-existant** (phase 1, fichier non modifié par cette phase), mais la mise en commun de
`_section` en phase 2 rend le fork visible.
**Fix :** faire consommer la fixture partagée par `test_docs_structure.py`
(`section(texte, "## Pilotage clavier", "installation.md")`) et supprimer sa copie privée.

#### IN-05 : `OPTIONS_GLOBALES_A_VALEUR` recopie à la main l'arité du parseur

**File:** `tests/test_docs_cli.py:164-166`, utilisé par `_sous_commande_atteinte` (`:508-525`)

**Issue :** la projection du nom de sous-commande sait quelles options globales consomment le jeton
suivant grâce à une liste écrite en dur. Si une future option globale à valeur (`--api-url`, …)
apparaît dans un exemple marqué, son **valeur** est lue comme nom de sous-commande et le constat
« sous-commande atteinte sans être documentée » se déclenche sur une page correcte — une rougeur
fausse, du même genre que celle reprochée en WR-03.
**Fix :** dériver le saut par sondage (`parse_args` du préfixe avec et sans le jeton suivant), ou
consigner explicitement ce miroir comme point de maintenance dans la section des limites honnêtes du
module.

#### IN-06 : Le « Parcours conseillé » du sommaire nomme cinq pages inexistantes

**File:** `docs/sommaire.md:5-13`

**Issue :** les étapes 2, 3, 5, 6 et 7 (`Parcours simplifié`, `Wizard avancé`, `Base locale`,
`Dépannage`, `Glossaire`) ne correspondent à aucun fichier sous `docs/` (seuls `installation.md` et
`cli.md` existent). Aucun test ne peut le voir : le test d'égalité bidirectionnelle ne compare que
les **liens** Markdown, et cette liste numérotée n'en contient pas. Un lecteur qui suit le parcours
cherche un fichier absent. Hérité de la phase 1 (D-05 : la liste croît par phase), toujours visible.
**Fix :** annoter les étapes non encore livrées (« à venir ») ou les transformer en liens au fur et à
mesure des phases ; dans les deux cas le harnais reste vert.

#### IN-07 : La même affirmation et le même bloc `text` apparaissent deux fois dans `cli.md`

**File:** `docs/cli.md:26-30` et `docs/cli.md:168-172` (incompatibilité `--offline` / `db sync`,
même message `Erreur : --offline incompatible avec db sync`)

**Issue :** D-17 pose « une seule source par énoncé » ; ici l'énoncé est écrit deux fois dans la page.
Une évolution du message (`dofus_stuff/cli.py`) ou une correction de formulation appliquée à un seul
endroit laisse l'autre périmé — et aucune assertion ne compare ces blocs au message réellement
produit (le message est correct aujourd'hui, vérifié en source : `print("Erreur : --offline
incompatible avec db sync", …)` à `dofus_stuff/cli.py`).
**Fix :** garder le paragraphe là où vit la commande (`## db`) et faire pointer la section « Options
globales » vers lui, ou l'inverse ; éventuellement asserter la présence du message littéral une
seule fois dans la page.

---

## Vérifications passées (contrôlées, sans constat)

Ces points ont été vérifiés réellement (exécution, sondes du parseur public, lecture source) et sont
**corrects** — la revue les consigne pour que le dossier montre ce qui a été couvert.

1. **Suite verte, conforme au SUMMARY.** `./.venv/Scripts/python.exe -m pytest -q` →
   **168 passed** (identique à la mesure de `02-03-SUMMARY.md`) ; les trois modules documentaires
   seuls → **32 passed**.
2. **Toutes les valeurs par défaut documentées sont exactes (37/37).** Sondage de
   `build_parser().parse_args(...)` pour chacun : `--timeout` 15, `--force-sync`/`--offline` faux,
   `--data-dir` = chemin **absolu** se terminant par `.data` (l'affirmation de la page sur le chemin
   absolu est vraie), `--limit` 10, `--page` 1, `--size` 5, `--level`/`--max`/`--target`/`--weight`/
   `--ban`/`--force`/`--seed` = `None`, six `--base-*` et six `--scroll-*` = `0.0` (page : `0`),
   `--jet` `average`, `--top-k` 30, `--time-limit` 5.0, `--no-cpsat`/`--classic-only`/`--demo`/
   `--auto-points`/`--stop-when-satisfied`/`--allow-*` = faux.
3. **Faits de parseur affirmés par la page, mesurés.** `db status --offline` → code de retour
   **2** et ligne d'erreur exacte `fetcher.py: error: unrecognized arguments: --offline` ;
   `stats` et `fill` apparaissent bien sous la forme littérale **`==SUPPRESS==`** dans
   `fetcher.py db --help`, à côté des trois descriptions reprises mot pour mot par la page
   (« Afficher l'état de la base », « Forcer la synchronisation complète », « Vider la base locale ») ;
   dans l'aide du parseur **racine**, c'est l'entrée `cache` qui porte `==SUPPRESS==` — la page
   documentant `cache` comme second nom de `db` dans `## cache`, le lecteur n'est pas induit en
   erreur ; `--offline` + `db sync` → `main()` imprime littéralement
   `Erreur : --offline incompatible avec db sync` et retourne 1, même pour `cache fill` (le message
   est bien le littéral du source, donc l'affirmation « une telle commande sort avec … le message
   suivant » est vraie pour les deux alias).
4. **`db clear` décrit conformément au code.** `dofus_stuff/database.py::Database.clear` exécute
   `DELETE FROM items` puis `DELETE FROM meta`, sans confirmation, et ne supprime aucun fichier du
   disque : la page (`docs/cli.md:176-178`) est exacte, y compris la phrase « Aucun fichier n'est
   supprimé du disque ».
5. **Aucune exécution, aucune base, aucun réseau.** Le module n'importe du produit que
   `dofus_stuff.cli` (contrôle `ast` du module + lecture) ; `main()` n'est jamais appelé ; la seule
   construction de `Database` de `tests/conftest.py` vit dans la fixture `app`, que les modules
   documentaires ne demandent pas (aucune fixture `autouse` dans le fichier) ; aucune écriture dans
   les modules de test (aucun `tmp_path`) ; `.data/dofus.sqlite3` garde son horodatage
   `2026-09-06 23:27:36 +0200` avant **et** après la suite complète.
6. **La garde destructrice mord sur sa cible.** Insertion de `python fetcher.py --offline db clear`
   dans un bloc `console` (copie jetable) → le module rougit avec **les deux** constats attendus
   (« sans l'avertissement attendu » et « commande a recopier »), et les trois constats joints à une
   seule assertion fonctionnent comme documenté.
7. **Encodage et fins de ligne.** Les cinq fichiers sont UTF-8 strict **sans BOM**, **100 % CRLF**
   (0 ligne LF isolée) et terminés par un saut de ligne ; toutes les lectures passent par
   `encoding="utf-8"` explicite ; `_lignes_exemple` ne normalise aucune fin de ligne (le
   `splitlines()` + `strip()` ne peut pas faire passer une prétention « octet à octet » pour vraie,
   la comparaison « verbatim » étant elle-même déclarée comme garantie de construction).
8. **Projection des exemples conforme à D-24.** `_lignes_exemple` filtre les blocs sur la **balise
   d'ouverture** conservée par `_blocs_de_code` (un seul scanner, D-12) ; sur la page livrée, les
   commandes citées en prose (`db status --offline`, `--offline db sync`) vivent dans des blocs
   `text` ou dans la prose, jamais dans un bloc `console` — la distinction « exemple à recopier /
   commande citée » tient.
9. **Méthode de la batterie de mutations de 02-03 recoupée.** La copie jetable **non mutée** donne
   exactement `1 failed, 9 passed` (l'unique échec est le contrôle de chemins de 02-02, rouge par
   construction dans une copie sans l'arbre produit — le SUMMARY l'annonce), et la mutation « blocs
   d'exemple renommés » doit bien faire 4 échecs : ce sont les quatre tests qui dépendent des blocs
   marqués (exemples analysables, couverture par sous-commande, ordre global/sous-commande, plus le
   contrôle de chemins) — mon comptage indépendant confirme le chiffre annoncé. La discrimination des
   motifs est donc crédible ; les angles morts sont ceux que la batterie ne mute jamais (WR-01,
   WR-02, WR-04, WR-05).
10. **Cohérence sommaire / page.** `docs/sommaire.md` liste `cli.md`, l'entrée d'index `CLI` égale le
    H1 `# CLI` de la page, les liens résolvent et la ligne de retour vers le sommaire est présente
    (invariants de la phase 1, verts).

---

_Reviewed: 2026-09-11T12:40:33Z_
_Reviewer: Claude (gsd-code-reviewer)_
_Depth: standard_
