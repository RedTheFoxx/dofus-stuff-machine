# Phase 2 : Référence CLI alignée sur le parseur - Carte des patrons

**Cartographiée :** 2026-09-11
**Artefacts analysés :** 5 artefacts livrables (2 docs, 3 tests) + 1 fichier existant à ne pas toucher
**Analogues trouvés :** 5 / 5 artefacts livrables ont un analogue direct ; 6 besoins n'ont **aucun** analogue (§ « Aucun analogue trouvé »)
**Périmètre de recherche :** `docs/**`, `tests/**`, `README.md`, `dofus_stuff/cli.py`, `fetcher.py`, `pyproject.toml`, `.planning/phases/01-…/{01-REVIEW,01-REVIEW-FIX}.md`
**Interpréteur de référence :** `./.venv/Scripts/python.exe` — mesure de référence re-mesurée pendant cette cartographie : `158 passed in 1.67s` le 2026-09-11, **avant** tout ajout de cette phase.

> Cette phase n'écrit **aucun code produit**. Les « analogues » ci-dessous sont donc des **pages livrées** et des **helpers de test existants**, pas du code applicatif. Chaque extrait est une copie verbatim du dépôt, avec `fichier:ligne` ; l'exécuteur recopie la forme, pas la sémantique web de la phase 1.

**Vérification de traçabilité git (#3645) :** tous les analogues nommés ci-dessous sont **suivis par git** — mesuré par `git ls-files -- docs/sommaire.md docs/installation.md tests/conftest.py tests/test_docs_structure.py tests/test_docs_code_anchor.py dofus_stuff/cli.py fetcher.py` → les 7 chemins sont renvoyés. Aucun chemin de miroir gitignoré n'est cité.

---

## Artefacts de la phase

| Artefact | Action | Rôle | Patron applicable |
|----------|--------|------|-------------------|
| `docs/cli.md` | **créé** | page de référence (prose + tables + blocs `console`) | gabarit de `docs/installation.md` |
| `docs/sommaire.md` | **modifié** (+1 ligne) | entrée d'index « CLI » → `cli.md` | la ligne d'index existante (`:19`) |
| `tests/test_docs_cli.py` | **créé** | contrôles CLI-01 / CLI-02 / CLI-03 | `tests/test_docs_code_anchor.py` (ancrage sur parseur) + `tests/test_docs_structure.py` (inventaire/mutation) |
| `tests/conftest.py` | **modifié** | un seul scanner de blocs de code partagé (D-12) | fixture `normalize` (`:132-135`) |
| `tests/test_docs_code_anchor.py` | **modifié au minimum** | consommer le helper partagé par fixture | son propre test (`:158`) — signature seulement |
| `README.md` | **inchangé** (D-29) | lien unique vers le sommaire (D-10) | `test_readme_links_to_sommaire` (`tests/test_docs_structure.py:190-213`) |

---

## Classification des fichiers

| Fichier (créé / modifié) | Rôle | Flux de données | Analogue le plus proche | Qualité |
|--------------------------|------|-----------------|-------------------------|---------|
| `docs/cli.md` | page de documentation | contenu statique (prose + tables + blocs de code) | `docs/installation.md` | **exact** (même gabarit D-01, même index, même retour, même encodage) |
| `docs/sommaire.md` (ligne ajoutée) | entrée d'index | lien fichier→fichier | la ligne d'index `:19` de `docs/sommaire.md` | **exact** |
| `tests/conftest.py` (`_blocs_de_code`, `_lignes_de_code`, `_lignes_exemple` + fixtures) | helper de test partagé | transform (découpage Markdown → lignes) | fixture `normalize` (`tests/conftest.py:118-135`) | **role-match** (même mécanisme d'exposition par fixture ; le scanner lui-même n'a pas d'analogue) |
| `tests/test_docs_cli.py` | module de test | parse-validate (page → parseur, `shlex` + `parse_args`) | `tests/test_docs_code_anchor.py` | **exact** (même rôle : ancrer une page sur un parseur public) |
| `tests/test_docs_code_anchor.py` (1 signature) | module de test | parse-validate | son test `test_cli_examples_of_installation_page_parse` (`:158-189`) | **exact** (changement d'appel, comportement identique) |
| `tests/test_docs_structure.py` | **non modifié** | inventaire statique | — (activé indirectement en livrant la page + l'entrée) | **n/a** |

---

## Affectations de patrons

### 1. `docs/cli.md` — gabarit de page (page, contenu statique)

**Analogue : `docs/installation.md`** (page livrée en phase 1, verte avec les invariants de `tests/test_docs_structure.py`).

#### 1.1 H1 unique (ligne 1)

`docs/installation.md:1`

```markdown
# Installation
```

Forme : `# ` + libellé **court, sans ponctuation finale**, suivi d'une ligne vide. Contrainte mécanique (`problemes_h1`, `tests/test_docs_structure.py:337-381`) : **un seul** H1, et `normalize(H1) == normalize(libelle d'index)`. Mesure faite pour cette phase (§ 2) : libellé `CLI` + H1 `# CLI` → 0 problème.

#### 1.2 Phrase d'introduction (ligne 3)

`docs/installation.md:3`

```markdown
Cette page décrit l'installation de dofus-stuff-machine, du prérequis Python au premier lancement en ligne de commande.
```

Forme : une **seule phrase**, à la troisième personne, sans titre intermédiaire, qui dit ce que la page couvre **et son périmètre**. Pour `cli.md`, la même forme donne par exemple « Cette page décrit les commandes de `fetcher.py`, leurs options et des exemples analysables par le parseur réel. » (formulation discrétionnaire, D-16 ; seule la **forme** est copiée).

#### 1.3 Style des sections

`docs/installation.md:7`, `:13`, `:29`, `:39`, `:53`, `:73`, `:99`, `:131`

```markdown
## Prérequis
## Installation
## Vérification
## Premier lancement
## Pilotage clavier
## Lancement de l'interface web
## Erreurs fréquentes
## Source de vérité
```

Sous-sections (niveau 3) quand un § a plusieurs cas — `docs/installation.md:101`, `:119`, `:123`, `:127` :

```markdown
### Base locale vide et mode hors-ligne
### Option globale placée après la sous-commande
### Ordre correct des options
### Ne jamais omettre le mode hors-ligne
```

Forme : titres **accentués**, casse de phrase, **pas** de numérotation, pas de « ## 1. », sections courtes. Pour `cli.md`, D-16 impose **une section par sous-commande dans l'ordre du parseur** : `## version`, `## self-test`, `## search`, `## item`, `## list`, `## optimize`, `## db`, puis la section d'alias `cache` (D-20) — même forme de titre.

#### 1.4 Table d'options (analogue de D-18)

`docs/installation.md:83-93`

```markdown
Options d'entrée de la commande :

| Option | Rôle |
|--------|------|
| `--data-dir` | répertoire de la base locale |
| `--offline` | ne pas contacter l'API (actif par défaut) |
| `--no-offline` | contacter l'API au démarrage |
| `--online` | équivalent de `--no-offline` |
| `--timeout` | délai HTTP en secondes |
| `--host` | adresse d'écoute (valeur par défaut `127.0.0.1`) |
| `--port` | port d'écoute (valeur par défaut `5000`) |
```

Forme à copier : une phrase d'amorce (`Options … :`), puis un tableau `| Option | … |` dont la première colonne porte l'option **entre accents graves**, la valeur par défaut étant écrite **en prose dans la cellule**, avec des accents graves pour la valeur. C'est l'analogue direct des « tables groupées par thème » de D-18 (`optimize`) : seul le nombre de colonnes et de groupes change, pas la forme.

> **Différence à assumer (D-18 vs C8) :** les 4 groupes thématiques d'`optimize` et l'absence de table récapitulative unique (D-17) sont propres à cette phase — l'analogue ne fournit **pas** d'exemple de « tables par thème », seulement la forme d'une table d'options.

#### 1.5 Bloc « Source de vérité » (D-30, D-03) — **liste, pas tableau**

`docs/installation.md:131-139`

```markdown
## Source de vérité

- `pyproject.toml` : dépendances, extra `dev` et configuration de pytest.
- `fetcher.py` : point d'entrée de la ligne de commande.
- `dofus_stuff/cli.py` : parseur et commandes réellement disponibles.
- `dofus_stuff/sync.py` : synchronisation de la base locale et garde du mode hors-ligne.
- `dofus_stuff/web/__main__.py` : options et valeurs par défaut de l'interface web.
- `dofus_stuff/web/routes.py` : écrans et libellés affichés par l'interface web.
- `dofus_stuff/web/static/js/terminal.js` : gestion des touches du clavier.
```

Forme à copier : titre `## Source de vérité` **exact**, une ligne vide, puis une **liste à puces** dont chaque entrée est `- ` suivi d'un chemin entre accents graves, puis ` : ` et le rôle en une phrase (voir les 7 lignes ci-dessus). Jamais un tableau (le contrôle `test_sources_de_verite_exist` extrait les chemins **entre accents graves** sur toute la page — un tableau marcherait techniquement, mais la forme livrée est une liste et doit être reconduite pour que la phase 3/6 n'ait pas deux formes à connaître).

Contraintes mécaniques qui pèsent sur le texte exact de `cli.md` :

- `tests/test_docs_code_anchor.py:25` — `CHEMIN_CITE = re.compile(r"\`(?P<chemin>[\w./-]+\.(?:py|toml|js|md|json|sql))\`")` : **tout** chemin entre accents graves de **toute la page** doit exister, résolu depuis la racine du dépôt (`tests/test_docs_code_anchor.py:143-156`, fix WR-01).
- D-30 exige que le bloc nomme **`build_parser()`** (la fonction), pas seulement `dofus_stuff/cli.py`. **Aucun analogue** pour cette assertion (voir § « Aucun analogue trouvé », ligne 6) : `build_parser()` n'est pas un chemin, `CHEMIN_CITE` ne le voit pas, et le test de phase 1 n'assère que l'existence des chemins.
- Le point d'entrée à citer est `fetcher.py` (racine) : `fetcher.py:1-11` est un shim, `from dofus_stuff.cli import main` — c'est bien le « point d'entrée » que D-30 demande.

#### 1.6 Ligne de retour (dernière ligne du fichier)

`docs/installation.md:141`

```markdown
[Retour au sommaire](sommaire.md)
```

Mesures : c'est la **dernière** ligne du fichier ; le fichier se termine par un `\r\n` (contrôle octet par octet : `...](sommaire.md)\r\n`) ; la cible est **relative**, sans ancre, sans antislash (`problemes_retour_sommaire`, `tests/test_docs_structure.py:383-416` ; `problemes_liens`, `:39-90`).

#### 1.7 Encodage et fins de ligne (conventions mesurées)

| Propriété | Mesure (2026-09-11) |
|-----------|---------------------|
| Encodage | UTF-8 **strict**, **aucun BOM** : `docs/sommaire.md`, `docs/installation.md`, `README.md`, `tests/*.py` commencent respectivement par `# S`, `# I`, `# D`, `"""` (aucun `\xef\xbb\xbf`) |
| Fins de ligne | **intégralement CRLF** : 19/19, 141/141, 125/125, 135/135, 603/603, 298/298 lignes CRLF, 0 ligne LF nue |
| Lecture par le harnais | `Path.read_text(encoding="utf-8")` (mode texte) **normalise** CRLF → LF en mémoire : `splitlines()` et les comparaisons `in` sont donc indépendantes des fins de ligne. Mesuré : `read_text().split("\r\n")` renvoie **1** élément sur `docs/sommaire.md` |
| Écriture par le harnais | `Path.write_text(..., encoding="utf-8")` reconvertit `\n` → `\r\n` sur ce poste. Mesuré : un contenu écrit avec `"\n".join(...)` est relu sur disque en `b'# Sommaire de la documentation\r\n'` |
| Longueur minimale | `LONGUEUR_MINIMALE = 300` (`tests/test_docs_structure.py:315`) : `len(texte.strip()) >= 300`, sinon `problemes_encodage` (`:441-446`) |
| Jetons de brouillon interdits | `JETONS_BROUILLON = ("todo", "a completer", "lorem")` (`tests/test_docs_structure.py:312`), comparés **après normalisation** — donc `TODO`, `à compléter`, `Lorem` sont tous refusés |

Conclusion pour l'exécuteur : écrire `docs/cli.md` en UTF-8 **avec CRLF** (comme les pages livrées), sans BOM, et ne pas craindre les CRLF dans les assertions (le harnais lit en mode texte).

#### 1.8 Règles de rédaction des exemples (D-24/D-25, adossées aux mesures de `02-RESEARCH.md` § M4)

L'analogue de **fond** est `docs/installation.md` § Premier lancement (`:39-51`) et ses blocs de code ```` ```bash ```` — mais **la balise diffère** et c'est une décision de cette phase : `docs/cli.md` marque ses exemples par des blocs ```` ```console ```` (D-24 ; `02-RESEARCH.md` Pattern 1), `installation.md` garde ses ```` ```bash ```` (question ouverte 5 : ne pas la modifier). **Aucun analogue** pour cette balise (voir § « Aucun analogue trouvé », ligne 1).

Contraintes mesurées qui s'appliquent au texte des exemples (chacune est un cas où le contrôle deviendrait faux ou aveugle) :

| Règle | Mesure | Conséquence sur la page |
|-------|--------|------------------------|
| Une ligne = une commande complète commençant par `python fetcher.py ` | `docs/installation.md:41` : `python fetcher.py --offline db status` | pas de prompt `$ `, pas de sortie mélangée dans le bloc |
| Aucun commentaire en fin de ligne | `python fetcher.py --offline db status   # etat de la base` → `SystemExit(2)` (`arguments excédentaires`) | l'explication vit **hors** du bloc (`text` ou prose) |
| Aucune continuation `\` | `shlex` → `ValueError: No escaped character` | une commande longue se coupe en plusieurs exemples distincts |
| Aucun métacaractère de shell (`*`, `$`, `~`) | `shlex` ne les étend pas, `parse_args` les accepte : contrôle **aveugle** | ne pas en montrer |
| Chemin Windows portables ou guillemetés | `C:\Users\Red\.data` → `C:UsersRed.data` **accepté** par le parseur (faux vert) | écrire `.data`, `C:/Users/…` ou guillemeter |
| `--offline` jamais avec `db sync` / `cache fill` | `--offline db sync` → code **1**, `Erreur : --offline incompatible avec db sync` | les exemples de `db sync` sont écrits **sans** `--offline` (Pitfall 4 : ne pas reconduire la règle de `installation.md`) |
| Option globale **avant** la sous-commande | `db status --offline` → code **2**, `fetcher.py: error: unrecognized arguments: --offline` | au moins un exemple `--offline optimize …` (D-27) |
| Sondes de sous-commande à argv complet | `parse_args(["db"])` et `parse_args(["cache"])` → `SystemExit(2)` | chaque exemple `db`/`cache` porte sa sous-commande (`db status`) |

---

### 2. `docs/sommaire.md` — entrée d'index (index, lien fichier→fichier)

**Analogue : la seule ligne d'index existante**, `docs/sommaire.md:15-19`

```markdown
## Index

| Page | Sujet |
|------|-------|
| [Installation](installation.md) | Installer l'outil, vérifier, lancer CLI et web |
```

Forme à copier : la nouvelle ligne est **une ligne de tableau de plus**, ajoutée **à la suite** de la ligne existante (la dernière ligne du fichier, sans ligne vide après — le fichier se termine par `\r\n`) :

```markdown
| [CLI](cli.md) | Commandes, options et exemples de `fetcher.py` |
```

Libellé `<->` H1 — réconciliation demandée :

| Élément | Valeur | Contrainte mécanique |
|---------|--------|----------------------|
| libellé d'index | `CLI` | `pages_listees` (`tests/test_docs_structure.py:326-334`) extrait `(libelle, cible)` de toute entrée `[libellé](cible)` du sommaire |
| H1 de la page | `# CLI` | `problemes_h1` (`:337-381`) exige `len(H1) == 1` **et** `normalize(H1) == normalize(libelle)` |
| cible | `cli.md` | `problemes_index` (`:92-118`) compare `cible` au **chemin de la page relatif à `docs/`** ; `problemes_retour_sommaire` (`:383-416`) exige un lien de retour dont la cible résolue vaut `docs/sommaire.md` |

**Mesure de réconciliation (faite pendant cette cartographie, dans une copie jetable de `docs/` ; l'arbre livré est resté intact — `docs/` contient toujours exactement `installation.md` et `sommaire.md`) :**

- page `cli.md` (H1 `# CLI`, phrase d'intro, ≥300 caractères, `[Retour au sommaire](sommaire.md)`) **+** ligne `| [CLI](cli.md) | … |` :
  - `problemes_index` → `[]`
  - `problemes_h1` → `[]`
  - `problemes_retour_sommaire` → `[]`
  - `problemes_encodage` → `[]`
  - `problemes_liens` → `[]`
  - `test_sommaire_index_labels_are_unique` → OK
- page `cli.md` **sans** l'entrée d'index, deux problèmes nommés (verbatim mesuré) :

```text
cli.md : page non listee dans docs/sommaire.md ; attendu une ligne d'index pointant vers cli.md (SOMM-02, D-06)
docs/cli.md : page non listee dans docs/sommaire.md ; attendu une ligne d'index dont le libelle egale le H1 de C:/Users/Red/AppData/Local/Temp/tmp…/docs/cli.md (SOMM-03, D-06)
```

Conclusion : l'entrée `cli.md` **et** la page doivent être livrées dans la **même** unité de travail (D-28) ; le libellé `CLI` + H1 `# CLI` est la configuration qui donne **zéro** problème, exactement comme `02-RESEARCH.md` § Pitfall 15 le mesure.

**Détail à ne pas confondre :** `docs/sommaire.md:5-13` porte déjà un « Parcours conseillé » **en texte brut**, dont la ligne `:10` vaut `4. CLI`. Cette ligne n'est **pas un lien** : `pages_listees`/`LIEN_LIBELLE` ne la voient pas, et **aucun** invariant n'exige que son texte égale le H1 ou le libellé d'index. Choisir `CLI` comme H1/étiquette la rend cohérente avec ce parcours, mais ce n'est pas une contrainte mécanique.

**`README.md` : ne pas y toucher** (D-29) — `test_readme_links_to_sommaire` (`tests/test_docs_structure.py:190-213`) exige exactement **1** lien vers `docs/sommaire.md` et `README.md:7` le porte déjà. `.claude/CLAUDE.md:96-106` suggère des liens directs vers les pages `docs/` (dont `cli.md`) : c'est **superseded** par D-10/D-29, et un lien direct ajouté ne serait **pas** détecté par la suite (Pitfall 14) — donc à ne pas ajouter.

---

### 3. `tests/conftest.py` — helper partagé, un seul scanner de blocs (D-12)

**Analogue du mécanisme d'exposition : la fixture `normalize`**, `tests/conftest.py:118-135`

```python
def _normalize(text: str) -> str:
    """Normalise un libellé pour comparaison (D-11) : entités HTML, accents, casse, espaces."""
    text = html.unescape(text)
    text = unicodedata.normalize("NFKD", text)
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    return re.sub(r"\s+", " ", text).strip().lower()


@pytest.fixture(scope="session")
def docs_dir() -> Path:
    """Racine du dossier docs/ du dépôt, indépendante du répertoire courant."""
    return Path(__file__).resolve().parents[1] / "docs"


@pytest.fixture(scope="session")
def normalize():
    """Expose _normalize aux modules de test sans import inter-modules."""
    return _normalize
```

Forme à copier : implémentation privée `_xxx` en haut du module + **fixture `session`** qui l'expose, avec une docstring qui dit pourquoi (« sans import inter-modules »). `conftest.py` importe déjà `re`, `html`, `unicodedata`, `Path`, `pytest` — le scanner n'ajoute **aucun** import.

**Code à DÉPLACER verbatim** depuis `tests/test_docs_code_anchor.py:128-138` (il ne doit **pas** exister en deux exemplaires, leçon WR-04 : deux scanners divergeraient) :

```python
def _lignes_de_code(texte: str) -> list[str]:
    """Lignes situées entre les délimiteurs de blocs de code Markdown (trois accents graves)."""
    lignes: list[str] = []
    dans_bloc = False
    for ligne in texte.splitlines():
        if DELIMITEUR_CODE.match(ligne):
            dans_bloc = not dans_bloc
            continue
        if dans_bloc:
            lignes.append(ligne)
    return lignes
```

Sa dépendance à déplacer avec lui — `tests/test_docs_code_anchor.py:34`

```python
DELIMITEUR_CODE = re.compile(r"^\s*```")
```

Le scanner **étendu** (balise conservée) et `_lignes_exemple` : voir `02-RESEARCH.md` § Pattern 1 (bloc `BALISE_EXEMPLE = "console"`, `DELIMITEUR_BLOC`, `_blocs_de_code`, `_lignes_exemple`). **Aucun analogue** de cette extension n'existe dans le dépôt (voir § « Aucun analogue trouvé », ligne 1) : le seul scanner livré jette la balise.

**Preuve de non-régression obligatoire après le déplacement** (leçon CR-01/WR-05, `02-RESEARCH.md` § Pattern 1) : dans une copie jetable, retirer `--offline` d'une commande de `docs/installation.md` et vérifier que `test_cli_examples_of_installation_page_parse` (`tests/test_docs_code_anchor.py:158-189`) **échoue** en nommant le drapeau manquant. Un helper déplacé sans mutation n'est pas prouvé.

---

### 4. `tests/test_docs_code_anchor.py` — modification minimale (module de test, parse-validate)

**Analogue : son propre test**, `tests/test_docs_code_anchor.py:158-189` (appel à `_lignes_de_code` à la ligne `:161`) :

```python
def test_cli_examples_of_installation_page_parse(docs_dir: Path) -> None:
    """Chaque commande fetcher.py des blocs de code est analysable et porte --offline."""
    texte = (docs_dir / PAGE).read_text(encoding="utf-8")
    commandes = [ligne.strip() for ligne in _lignes_de_code(texte) if "fetcher.py" in ligne]
```

Changement attendu = **signature + un appel** (le comportement reste identique au caractère près) : recevoir la fixture `lignes_de_code` et écrire `lignes_de_code(texte)`. Ne rien changer d'autre dans ce module (Pitfall 5 de la question ouverte : `installation.md` garde ses ```` ```bash ````).

#### 4.1 Comparaison bidirectionnelle : l'anti-analogue (CR-01) et la forme **corrigée** à copier

**Anti-analogue — contrôle à sens unique nommé comme s'il était bidirectionnel** (`tests/test_docs_code_anchor.py:208-219`) :

```python
def test_documented_entry_options_parse() -> None:
    """Chaque option d'entrée web de la page est acceptée par le parseur réel (D-14)."""
    parser = build_parser()
    for argv in SONDES_WEB:
        try:
            parser.parse_args(argv)
        except SystemExit:
            raise AssertionError(
                f"{PAGE} : option « {argv[0]} » refusée par le parseur ; attendu une option "
                f"acceptée par {SOURCE_WEB}::build_parser().parse_args()"
            ) from None
```

Pourquoi c'est un anti-patron : la docstring dit « **de la page** » mais la fonction ne prend **pas** `docs_dir`, n'ouvre jamais la page et itère une liste codée en dur `SONDES_WEB` (`:38-48`). Une option **inventée par la page** ne fait donc rien rougir (preuve CR-01 : `157 passed` après ajout d'une ligne `| --serve | … |`).

**Forme corrigée (commit `3f221b3`) — c'est CETTE forme que les contrôles CLI doivent copier**, `tests/test_docs_code_anchor.py:259-280` :

```python
def test_options_citees_par_la_page_sont_acceptees_par_le_parseur(docs_dir: Path) -> None:
    """La page est la source des options citees : chacune est acceptee par le parseur web (D-14)."""
    texte = (docs_dir / PAGE).read_text(encoding="utf-8")
    citees = set(OPTION_CITEE.findall(_section(texte, TITRE_LANCEMENT_WEB)))
    assert citees, (
        f"{PAGE} : aucune option « --… » citee par la section « {TITRE_LANCEMENT_WEB} » ; "
        f"attendu la surface d'entree du parseur {SOURCE_WEB}::build_parser()"
    )

    parser = build_parser()
    inventees = sorted(option for option in citees if not _option_acceptee(parser, option))
    assert not inventees, (
        f"{PAGE} : option(s) citee(s) par la section « {TITRE_LANCEMENT_WEB} » mais refusee(s) "
        f"par le parseur : {', '.join(inventees)} ; attendu chaque option citee acceptee par "
        f"{SOURCE_WEB}::build_parser().parse_args()"
    )

    surface = _options_aide_web()
    assert citees == surface, (
        f"{PAGE} : surface citee par la section « {TITRE_LANCEMENT_WEB} » = {sorted(citees)} ; "
        f"attendu la surface de {SOURCE_WEB}::build_parser().format_help() = {sorted(surface)}"
    )
```

Les quatre traits à reconduire : (a) la **page est la source** (`docs_dir` en paramètre, texte lu, extraction par motif) ; (b) garde-fou « extraction non vide » (`assert citees`) ; (c) chacune des options extraites est **sondée** sur le parseur public et les refusées sont **nommées** ; (d) l'égalité d'ensembles **des deux surfaces** est assertée, avec les deux ensembles affichés dans le message.

**Transposition obligatoire pour la CLI (Pitfall 10) :** extraire les options d'`optimize` **des lignes de tableau de la section** (`^\|` contenant un jeton `` `--xxx` ``), **jamais** de tout le texte de la section (les exemples citent `--offline`, globale **refusée** par le sous-parseur `optimize` → faux échec), et normaliser les jetons des deux côtés (`--[a-z][a-z-]*`, **sans** `=valeur`) — sinon `` `--limit=10` `` et `--limit` se comparent mal (WR-04 transposé).

**Transposition inverse — non applicable ici :** `_option_acceptee` (`:107-121`) est la sonde tri-état (`[opt]`, `[opt,"1"]`, `[opt,"x"]`) : elle **déclare `--jet` inventée** (Pitfall 7, faux négatif mesuré). Elle reste utilisable pour la surface web (vert aujourd'hui) mais **ne doit pas** servir aux 30 options d'`optimize` : la liste épinglée `(option, valeur d'essai|None)` de `02-RESEARCH.md` § Pattern 2 est le patron retenu (aucun analogue).

---

### 5. `tests/test_docs_cli.py` — module de test (parse-validate)

**Analogue principal : `tests/test_docs_code_anchor.py`** (même rôle : ancrer une page sur un parseur public, sans exécuter le produit). En-tête du module (`:1-13`) à copier, seule partie dont le texte change (noms de fichiers/constantes) :

```python
"""Ancrage de la documentation utilisateur sur le code réel du produit (critère de succès 4).

Aucune introspection privée d'argparse (D-14), aucune exécution de commande, aucune base
ouverte : les contrôles passent par les parseurs publics et par la lecture des fichiers.
"""

from __future__ import annotations

import io
import re
import shlex
from contextlib import redirect_stderr
from pathlib import Path
```

Constantes de module à copier en forme (`:18-21`, adaptation des valeurs) :

```python
RACINE_DEPOT = Path(__file__).resolve().parents[1]
PAGE = "installation.md"
SOURCE_WEB = "dofus_stuff/web/__main__.py"
SOURCE_CLI = "dofus_stuff/cli.py"
```

→ pour ce module : `PAGE = "cli.md"`, `SOURCE_CLI` inchangé, et l'import `from dofus_stuff.cli import build_parser as build_cli_parser` (`:15`) **sans** l'import du parseur web (`:16`).

#### 5.1 Helpers de section — à réutiliser, jamais à recopier (D-12)

`tests/test_docs_code_anchor.py:79-104` — `_sections` **inclut l'entête de page** comme première section de titre `None` (fix WR-02) :

```python
def _sections(texte: str) -> list[tuple[str | None, str]]:
    """Couples (titre de niveau 2, corps) des sections, dans l'ordre du fichier.

    L'entete qui precede le premier titre de niveau 2 est la premiere section, de titre None :
    une regle portant sur « chaque section » couvre donc aussi l'entete de la page.
    """
    titres = list(TITRE_H2.finditer(texte))
    sections: list[tuple[str | None, str]] = [
        (None, texte[: titres[0].start()] if titres else texte)
    ]
    for index, trouve in enumerate(titres):
        fin = titres[index + 1].start() if index + 1 < len(titres) else len(texte)
        sections.append((trouve.group("titre"), texte[trouve.end() : fin]))
    return sections


def _section(texte: str, titre: str) -> str:
    """Corps d'une section de niveau 2, du titre jusqu'au titre de niveau 2 suivant."""
    attendu = titre.strip().lstrip("#").strip()
    for titre_trouve, corps in _sections(texte):
        if titre_trouve is not None and titre_trouve.strip() == attendu:
            return corps
    raise AssertionError(
        f"{PAGE} : section « {titre} » introuvable ; attendu un titre de niveau 2 "
        f"« ## {attendu} » dans la page ({PAGE})"
    )
```

Dépendance `TITRE_H2` (`:33`) : `TITRE_H2 = re.compile(r"^##\s+(?P<titre>.+?)\s*$", re.MULTILINE)`.

Ces deux fonctions sont nécessaires au nouveau module (périmètre « tables de la section `optimize` », section `cache`, section « Source de vérité ») : voir § 6 pour le déplacement, qui évite la **troisième** copie (WR-04).

`tests/test_docs_structure.py:223-231` porte de son côté un `_section` **de sémantique différente** (retourne `None` si absent, recherche par `find`) — il reste **local** et ne doit pas être confondu avec celui ci-dessus.

#### 5.2 Extraction verbatim des exemples et conversion des échecs (D-13, D-25)

Forme corrigée de l'ancrage des exemples — `tests/test_docs_code_anchor.py:158-189`, extrait à copier (mot pour mot, seules les constantes de page changent) :

```python
    parser = build_cli_parser()
    for commande in commandes:
        try:
            argv = shlex.split(commande)
        except ValueError:
            raise AssertionError(
                f"{PAGE} : commande « {commande} » non analysable ; attendu une commande "
                f"découpable par shlex (source : {SOURCE_CLI})"
            ) from None
        reste = argv[argv.index("fetcher.py") + 1 :]
        try:
            parser.parse_args(reste)
        except SystemExit:
            raise AssertionError(
                f"{PAGE} : commande « {commande} » refusée par le parseur réel ; "
                f"attendu une commande acceptée par {SOURCE_CLI}::build_parser().parse_args()"
            ) from None
```

Trois traits à reconduire : `shlex.split` enveloppé, `SystemExit` **converti** en `AssertionError` localisante (jamais laissé traverser), `from None` pour ne pas polluer le message.

**Deux écarts exigés pour `cli.md`** (mesures `02-RESEARCH.md` § Pattern 3) :

- remplacer `argv.index("fetcher.py")` par un test de préfixe plus robuste (`argv[:2] == ["python", "fetcher.py"]`), car `argv.index` casse si une valeur vaut `fetcher.py` ;
- ajouter l'assertion « verbatim » (`exemple in texte`) exigée par D-25, en sachant qu'elle est **tautologique** (la ligne est extraite de la page) : la garantie est de construction et le module doit l'écrire comme telle (limite D-26, cf. `02-RESEARCH.md` § Validation Architecture).

#### 5.3 Inventaire/mutation : ce que le nouveau module doit **imiter** et ce qu'il **ne doit pas** encoder

**Analogue : `tests/test_docs_structure.py:533-560`** (mutation sur copie jetable, jamais sur l'arbre livré) :

```python
def test_mutation_detecte_les_trois_derives(tmp_path: Path, docs_dir: Path, normalize) -> None:
    """Trois derives injectees dans une copie de docs/ sont detectees, l'arbre livre restant sain (critere 5)."""
    copie = tmp_path / "docs"
    shutil.copytree(docs_dir, copie)

    sain = (
        problemes_liens(docs_dir)
        + problemes_index(docs_dir)
        + problemes_h1(docs_dir, normalize)
    )
    assert sain == [], (
        "docs/ livre deja en derive avant toute mutation ; attendu un arbre sain garde "
        "par tests/test_docs_structure.py (critere 5, GARD-01)\n" + "\n".join(sain)
    )
```

**Analogue du nom dérivé (fix WR-05) — `tests/test_docs_structure.py:517-530`, à reconduire si un besoin de mutation apparaît** :

```python
def _nom_page_injectee(docs_dir: Path) -> str:
    """Nom de page absent de docs/ et du sommaire, pour que l'injection reste une derive (critere 5).

    Le nom est derive de l'arbre analyse et jamais code en dur : une page livree par une phase
    ulterieure (le glossaire, par exemple) ne peut donc pas rendre cette mutation faussement rouge.
    """
    connus = {page.name for page in _pages(docs_dir)}
    connus |= {Path(cible).name for _, cible in pages_listees(docs_dir)}
    nom = "page-injectee-mutation.md"
    rang = 1
    while nom in connus:
        rang += 1
        nom = f"page-injectee-mutation-{rang}.md"
    return nom
```

**Décision de périmètre (Pitfall 13, D-26) :** `tests/test_docs_cli.py` **n'encode aucune mutation** et **aucune assertion ne dépend d'un nom de page que cette phase ne livre pas**. Les dérives sont injectées à la main dans une copie jetable pendant l'exécution (le test de mutation formel reste en phase 6, GARD-03). Si un nom de page dérivé devient nécessaire, copier `_nom_page_injectee` **depuis `tests/test_docs_structure.py`** (ou l'exposer en fixture) — jamais un `glossaire.md`/`depannage.md` codé en dur.

#### 5.4 Propriété statique « aucune exécution, aucune base » (critère 5, C6)

Aucun analogue direct : `tests/test_docs_code_anchor.py` **déclare** la propriété dans sa docstring (`:3-4`) mais ne l'assert pas. Le nouveau module doit la rendre vérifiable sur **son propre texte source** (lecture de `Path(__file__)`, absence des jetons `Database`, `Catalog`, `main(`), en plus de la déclaration. Voir § « Aucun analogue trouvé », ligne 5.

---

### 6. Ce qui MIGRE dans `tests/conftest.py` vs ce qui reste local (D-12)

| Élément | Décision | Raison (analogue / finding) |
|---------|----------|-----------------------------|
| `_lignes_de_code` (`test_docs_code_anchor.py:128-138`) + `DELIMITEUR_CODE` (`:34`) | **MIGRE** vers `tests/conftest.py` (+ `_blocs_de_code`, `_lignes_exemple`, `BALISE_EXEMPLE`) et est exposé en fixtures | D-12 + Pattern 1 de la recherche : **un seul** scanner ; deux scanners divergeraient (WR-04). Preuve de non-régression exigée sur `test_cli_examples_of_installation_page_parse` |
| `_sections` / `_section` (`test_docs_code_anchor.py:79-104`) + `TITRE_H2` (`:33`) | **MIGRE** vers `tests/conftest.py`, exposé en fixtures ; `test_docs_code_anchor.py` supprime ses définitions locales et les consomme par fixture | Le nouveau module a besoin d'un périmètre par section (`optimize`, `cache`, « Source de vérité ») ; une **troisième** copie locale serait le piège WR-04 (« deux invariants du même fichier en désaccord »). Même mécanisme d'exposition que `normalize` (`conftest.py:132-135`) |
| `docs_dir`, `normalize` (`conftest.py:126-135`) | **réutilisés tels quels**, jamais recopiés | D-12 ; `normalize` a un test de comportement dédié (`test_docs_structure.py:495-514`) |
| `_normalize` (`conftest.py:118-124`) | **réutilisé via la fixture `normalize`** uniquement | D-11 ; ne jamais réimplémenter un `.lower()` local |
| `PAGE`, `SOURCE_WEB`, `SONDES_WEB`, `OPTIONS_WEB`, `LIBELLES_SOURCE`, `_option_acceptee`, `_options_aide_web`, `OPTION_LONGUE`, `JETON_AIDE`, `ADRESSE_ECOUTE`, `TITRE_LANCEMENT_WEB`, `TITRE_SOURCE`, `CHEMIN_CITE` | **restent locaux** à `tests/test_docs_code_anchor.py` | Spécifiques à la page d'installation / à la surface web ; aucun autre consommateur. `_option_acceptee` (tri-état) est en outre **impropre** à la surface `optimize` (Pitfall 7) |
| `pages_listees`, `problemes_index`, `problemes_h1`, `problemes_retour_sommaire`, `problemes_encodage`, `_pages`, `_lire_page`, `_section` (variante `:223-231`), `_nom_page_injectee` | **restent locaux** à `tests/test_docs_structure.py` | Déjà actifs et verts ; livrer la page + l'entrée les déclenche **sans** nouveau code (D-28). Ne rien réécrire, ne rien importer |
| `SONDES_SOUS_COMMANDES`, `SONDES_GLOBALES`, `SONDES_OPTIMIZE`, `JETON_DESTRUCTEUR`, `JETON_AVERTISSEMENT`, `_espace_de_noms`, `_accepte`, `_argv_de_exemple` | **nouveaux, locaux** à `tests/test_docs_cli.py` | D-12 : le `conftest` ne reçoit que le **partagé** ; ces listes sont propres à la surface CLI |

---

## Patrons partagés (cross-cutting)

### P-1. Message d'échec localisant (D-13, D-31) — la forme exigée des nouveaux messages

Forme canonique : `<page> : <ce qui est faux> ; attendu <valeur/état attendu> (source : <fichier de code ou décision>)`, sur une ou plusieurs f-strings concaténées, **sans saut de ligne dans le message**.

Trois messages livrés à copier :

1. Index / page manquante — `tests/test_docs_structure.py:113-117` :

```python
    for page in sorted(pages - cibles):
        problemes.append(
            f"{page} : page non listee dans docs/sommaire.md ; attendu une ligne d'index "
            f"pointant vers {page} (SOMM-02, D-06)"
        )
```

2. Longueur de page insuffisante — `tests/test_docs_structure.py:441-446` :

```python
        longueur = len(texte.strip())
        if longueur < LONGUEUR_MINIMALE:
            problemes.append(
                f"{nom} : page de {longueur} caracteres dans {page.as_posix()} ; attendu "
                f"au moins {LONGUEUR_MINIMALE} caracteres pour une page livree (GARD-01)"
            )
```

3. Option citée refusée par le parseur (forme **corrigée** CR-01) — `tests/test_docs_code_anchor.py:269-274` :

```python
    inventees = sorted(option for option in citees if not _option_acceptee(parser, option))
    assert not inventees, (
        f"{PAGE} : option(s) citee(s) par la section « {TITRE_LANCEMENT_WEB} » mais refusee(s) "
        f"par le parseur : {', '.join(inventees)} ; attendu chaque option citee acceptee par "
        f"{SOURCE_WEB}::build_parser().parse_args()"
    )
```

Application aux nouveaux messages (forme + contenu) : la page (`cli.md`), la valeur attendue, et le fichier de code (`dofus_stuff/cli.py::build_parser()`, ou `fetcher.py` pour le point d'entrée). Deux messages-types cohérents avec les trois ci-dessus :

```text
docs/cli.md : sous-commande « cache » absente de la page ; attendu chaque sous-commande documentée analysable par dofus_stuff/cli.py::build_parser()
docs/cli.md : exemple « python fetcher.py --offline list --page 2 » refusé par le parseur réel ; attendu une commande acceptée par dofus_stuff/cli.py::build_parser().parse_args()
```

### P-2. Normalisation avant comparaison de **libellés** (D-11) — et jamais sur une commande

- Utiliser la fixture `normalize` (`tests/conftest.py:132-135`) pour tout libellé, titre, phrase ou jeton d'avertissement (`destruct`) : accents, casse, entités HTML, espaces multiples, CRLF/LF sont unifiés (comportement testé, `tests/test_docs_structure.py:495-514`).
- **Ne pas** normaliser une **commande** : D-25 exige la présence verbatim et `parse_args` compare les jetons tels quels. La comparaison d'options se fait sur un jeton extrait de la même façon des deux côtés (`--[a-z][a-z-]*`), jamais sur des formes de nature différente (`` `--limit=10` `` vs `--limit`, WR-04).

### P-3. Lecture de page et mutation jetable

- Lecture : `(docs_dir / PAGE).read_text(encoding="utf-8")` — **encodage explicite partout** (fins de ligne CRLF sur ce poste, `read_text` les normalise en mémoire : mesuré).
- Mutation : `tmp_path` + `shutil.copytree(docs_dir, copie)` (`tests/test_docs_structure.py:533-536`), puis assertions sur la copie, puis assertions finales que **l'arbre livré** est intact (`:588-602` : `"(sommaire.md)" in texte_livre`, `texte_livre.startswith("# Installation")`, `not (docs_dir / page_injectee).exists()`). Jamais d'écriture sous `docs/`.
- Garde de page absente : tourner une page manquante en **problème nommé** plutôt qu'en `FileNotFoundError` (patron `_page` `tests/test_docs_structure.py:215-221` + `_sommaire_absent` `:31-37`) — c'est exactement ce que IN-03 reproche encore à `test_docs_code_anchor.py` (finding laissé ouvert, cf. § 7 / « Aucun analogue trouvé », ligne 6).

### P-4. Ancrage par surface **publique** du parseur (D-14)

- Vérification acceptée par l'exécuteur : `build_parser()` / `parse_args` / `format_usage` / `format_help` — mesuré pendant cette cartographie (interpréteur épinglé, aucun `main()` exécuté) :

```text
defauts globaux: {'timeout': 15, 'data_dir': WindowsPath('…/.data'), 'force_sync': False, 'offline': False, 'command': 'version'}
usage: {version,self-test,search,item,list,optimize,db,cache}
SystemExit 2 ['db'] / ['cache']      # db_command requis
OK ['db', 'clear'] / ['cache', 'clear'] / ['optimize', '--jet', 'average'] / ['optimize', '--demo']
optimize --jet sans valeur -> SystemExit 2
```

- Jamais d'attribut privé (`parser._subparsers`, etc.), jamais `format_help()` comme source de surface (Pitfall 5 : `--all` invisible partout), jamais `main()` (C6/D-22), jamais `subprocess` (utiliser `shlex`, la mesure ci-dessus le confirme sur 6 sondes).

### P-5. Prose en français, code inchangé

Prose, titres, docstrings et messages en français (accents conservés) ; chemins, identifiants, options, code et frontmatter **inchangés** (`.claude/CLAUDE.md:113-118`). Les modules existants alternent docstrings accentuées (`test_docs_code_anchor.py:129`) et non accentuées (`tests/test_docs_structure.py`) : suivre le module d'accueil.

---

## 7. Anti-patrons à NE PAS recopier (leçons de la revue de phase 1)

Chaque ligne : le finding, la forme interdite **telle qu'elle a existé**, le correctif **livré** (à copier), et ce que le nouveau code doit en faire.

| Finding | Anti-patron (forme fautive d'origine) | Correctif livré (à copier) | Ce que `tests/test_docs_cli.py` doit faire |
|---------|--------------------------------------|----------------------------|--------------------------------------------|
| **CR-01** | Un contrôle à sens unique **nommé** comme bidirectionnel : `test_documented_entry_options_parse` (`:208-219`) affirme « **de la page** » dans sa docstring mais itère `SONDES_WEB` sans jamais lire la page — une option inventée par la doc passait (muté → `157 passed`) | Le contrôle bidirectionnel de `:259-280` : extraction **depuis la page**, garde-fou « non vide », sonde `parse_args`, puis **égalité d'ensembles** des deux surfaces, chacune affichée dans le message | Nommer et docstringuer **exactement** ce qui est implémenté ; obtenir la « seconde direction » par la **liste épinglée** (présence des noms dans la page) et non par une prétention ; écrire la limite D-26 **dans le module** (aucune complétude parser → page revendiquée) |
| **WR-01** | Motif trop étroit **et** périmètre trop étroit : `CHEMIN_CITE` ne couvrait que les extensions `.py` et `.toml` (avant fix) et `test_sources_de_verite_exist` n'était appliqué qu'au seul bloc `## Source de vérité` → le chemin `.js` du bloc et la ligne `Sources :` de `docs/installation.md:71` échappaient au contrôle | `CHEMIN_CITE` élargi à six extensions (`:25`, citation verbatim au § 1.5) et appliqué à **`texte` entière** (`:143-156`), l'assertion « au moins un chemin dans le bloc » étant conservée comme garde-fou | Extraire les **options** depuis les **lignes de tableau** de la section (`^\|`), pas de tout le texte de section (`--offline` y est cité et refusé par `optimize`) ; chercher le jeton destructeur avec une alternance `db`/`cache` suivie de `clear` et d'espaces quelconques (`02-RESEARCH.md` § Pattern 4), jamais `\bdb\s+clear\b` seul |
| **WR-02** | Règle évaluée **par section** alors que l'entête échappe : la règle « `--debug` ⇒ `developpement` » ne couvrait que les corps de `## `, l'entête de page (`docs/installation.md:1-5`) n'était dans **aucune** section | `_sections` expose l'entête comme première section de titre `None` (`tests/test_docs_code_anchor.py:79-92`) et le message nomme le périmètre : `f"l'entête de {PAGE}, avant le premier titre de niveau 2"` (`:244-249`), assertion `:252-256` | La règle destructrice et la règle d'exemple s'appliquent **ligne à ligne sur le texte entier** (jamais par section) ; réserver les périmètres par section aux tables d'options, où le périmètre **est** la section |
| **WR-03** | Ancre reconnue seulement si la cible **commence** par `#` : `installation.md#prerequis` n'était pas diagnostiquée « ancre interdite » mais « lien mort », et `test_no_anchor_or_absolute_links` restait vert sur une ancre réelle | `if "#" in cible:` **n'importe où** dans la cible, suivie d'un `continue` pour ne pas doubler d'un faux « lien mort » — livré dans `problemes_liens` (`tests/test_docs_structure.py:53-58`) **et** dans `test_no_anchor_or_absolute_links` (`:167-171`), les liens externes restant testés en premier (`:51-52`, `:165-166`) | Prendre la même précaution pour `LINK`-like : tester la nature de la cible **avant** de la résoudre, et ne jamais produire deux diagnostics pour la même cible. `docs/cli.md` n'écrit **aucune** ancre (liens fichier→fichier, D-01/T-01-04) |
| **WR-04** | Comparer des choses de nature différente : `problemes_index` comparait des **noms de base** (`page.name`) à des **cibles brutes** du sommaire, alors que `_pages` est récursif → page imbriquée invisible, page imbriquée listée **impossible** à satisfaire (deux invariants du même fichier en désaccord) | Comparaison de chemins **relatifs à `docs/`** des deux côtés : `pages = {page.relative_to(docs_dir).as_posix() for page in _pages(docs_dir) if page.name != "sommaire.md"}` (`:101-105`) face à `cibles = set(LINK.findall(...))` (`:100`), et **même clé** pour le libellé d'index dans `problemes_h1` (`libelles.get(page.relative_to(docs_dir).as_posix())`, `:350`) | Comparer **des formes identiques** des deux côtés : un jeton d'option extrait par le même motif que celui employé pour la page (jamais `` `--limit=10` `` face à `--limit`) ; ne pas réimplémenter l'égalité d'ensembles du sommaire (les fonctions de `test_docs_structure.py` restent l'unique juge) |
| **WR-05** | Test de mutation **codant en dur un nom de page qu'une phase ultérieure livre légitimement** : la mutande injectait `glossaire.md` (phase 6) → le harnais serait devenu rouge sans dérive (`1 failed, 156 passed` en simulant la phase 6) | `_nom_page_injectee` (`tests/test_docs_structure.py:517-530`) dérive le nom de l'arbre analysé (pages présentes ∪ cibles du sommaire), avec suffixe incrémenté en cas de collision ; l'assertion sur l'arbre livré porte sur **le même nom dérivé** ; non-régression prouvée (phase 6 simulée → `158 passed`) | **Ne coder aucun nom de page en dur** (`cli.md` est livré, `glossaire.md`/`depannage.md` sont futurs) ; **n'encoder aucune mutation** dans le module (Pitfall 13) ; si un nom dérivé devient nécessaire, copier/partager `_nom_page_injectee` |
| **IN-03** (info, **laissé ouvert**) | `tests/test_docs_code_anchor.py` lève un `FileNotFoundError` brut dès que la page manque (`(docs_dir / PAGE).read_text(...)`, occurrences `:143`, `:160`, `:194`, `:234`, `:261`, `:285`) au lieu du message nommé de D-13 | Correctif **non livré** (hors `fix_scope`) ; la forme attendue existe dans `tests/test_docs_structure.py` : `_page` (`:215-221`) et `_sommaire_absent` (`:31-37`) transforment l'absence en problème lisible | Le **nouveau** module ne doit pas hériter de ce défaut : toute lecture de `docs/cli.md` passe par une garde qui produit un `AssertionError` nommant la page, la valeur attendue et `dofus_stuff/cli.py` (D-13) |

**Formes fausses explicitement écartées par la recherche (à ne pas écrire) :** dériver une surface de `format_help()` (Pitfall 5 / M3 : `--all` invisible, `==SUPPRESS==` littéral, `--data-dir` machine-dépendant) ; comparer `vars(db_ns) == vars(cache_ns)` sans retirer `command` (Pitfall 3 : toujours faux) ; sonder une sous-commande par un jeton nu `db`/`cache` (Pitfall 2 : `SystemExit(2)`) ; recopier les exemples de l'épilog du parseur (Pitfall 6 : sous-commande dupliquée, code 2) ; sonde tri-état sur une option à `choices` (Pitfall 7 : `--jet` faussement « inventée ») ; exiger `--offline` sur les exemples `db sync` (Pitfall 4) ; annoncer que `SUPPRESS` « masque » une sous-commande du `--help` (Pitfall 1).

---

## 8. Aucun analogue trouvé

| # | Besoin de la phase | Rôle | Flux | Raison de l'absence | Forme à écrire (source) |
|---|--------------------|------|------|---------------------|-------------------------|
| 1 | Balise de bloc `console` + `_blocs_de_code`/`_lignes_exemple` | helper partagé | transform | Le seul scanner livré (`test_docs_code_anchor.py:128-138`) **jette la balise** ; `docs/` n'utilise que ```` ```bash ```` et ```` ```text ```` (mesuré) : aucune page ne porte de bloc `console` | `02-RESEARCH.md` § Pattern 1 (code complet fourni) |
| 2 | Listes épinglées `(option, valeur d'essai\|None)` et `(sous-commande, argv)` | constance de test | parse-validate | Aucune liste épinglée n'existe : `SONDES_WEB` (`:38-48`) est une liste de sondes **web**, et la sonde tri-état (`:107-121`) est impropre aux `choices` | `02-RESEARCH.md` § Pattern 2 (sondes mesurées, 30/30) ; `.claude/CLAUDE.md:134-146` (noms et sondes prescrits) |
| 3 | Co-présence « `db clear` + avertissement destructeur sur la même ligne », jamais dans un exemple | contrôle | texte statique | **Analogue inverse** : `test_no_destructive_command_in_installation` (`tests/test_docs_structure.py:277-307`) **interdit** le jeton dans `installation.md` (`COMMANDE_DESTRUCTRICE = re.compile(r"\bdb\s+clear\b")`, `:20`). Rien dans le dépôt n'exige au contraire un avertissement | `02-RESEARCH.md` § Pattern 4, avec une alternance `db`/`cache` et `\s+` (et **non** la seule limite `\b` du motif existant) + § M6 pour la dérivation du classement « destructeur » |
| 4 | Preuve d'alias `cache` ≡ `db` par **espace de noms modulo `command`** | contrôle | parse-validate | Rien dans le dépôt ne compare deux espaces de noms ; mesure : `vars()` bruts diffèrent **toujours** (clé `command`) et l'égalité devient vraie modulo cette clé (5 sous-commandes, `clear --all` compris). Aucun `aliases=`/`set_defaults` dans `dofus_stuff/cli.py:179-195` | `02-RESEARCH.md` § Pattern 5 (`_espace_de_noms`) + § M1.3 |
| 5 | Assertion statique « ce module n'exécute ni `main()` ni aucune base » | contrôle | texte statique | Seule une **docstring** déclare la propriété (`test_docs_code_anchor.py:3-4`) ; aucune assertion ne la vérifie | `02-RESEARCH.md` § Validation Architecture (critère 5) : lecture de `Path(__file__)`, absence des jetons `Database`, `Catalog`, `main(` |
| 6 | « Le bloc Source de vérité **nomme `build_parser()`** » + garde de page absente | contrôle | texte statique | `test_sources_de_verite_exist` (`:141-156`) n'assert que l'**existence** des chemins cités (`CHEMIN_CITE`) ; `build_parser()` n'est pas un chemin et n'est vu par aucun motif. La garde d'absence nommée n'existe que dans `test_docs_structure.py` (IN-03 laissé ouvert) | D-30 (exigence) + `tests/test_docs_structure.py:215-221`/`:31-37` (forme de la garde nommée) |
| 7 | Contenu éditorial de `docs/cli.md` (synopsis par sous-commande, 4 groupes de tables d'`optimize`, phrase d'introduction, avertissement `db clear`) | page | contenu statique | Aucune page du dépôt ne documente la CLI : `installation.md` ne cite que 6 commandes en passant. Le texte exact relève de la rédaction (Claude's Discretion) | `02-RESEARCH.md` § Mesures M1/M2 (surface et défauts mesurés) ; D-16/D-18/D-19/D-20/D-22 pour la structure ; `docs/installation.md` pour la **forme** (§ 1) |

**Précisions honnêtes à porter dans le plan (issues de la recherche, pas de la présente cartographie) :**

- `db clear --all` est accepté par le parseur mais **jamais lu** par le code : l'omettre (D-19), la limite D-26 l'autorise explicitement.
- A2 : `db sync` / `cache fill` réécrivent la base sans la détruire ; recommander un avertissement `destruct` pour `db clear` **uniquement**, et pour `sync`/`fill` une mention « réécrit la base, nécessite le réseau, incompatible avec `--offline` » — à écrire explicitement dans le plan pour qu'un relecteur ne lise pas D-23 comme violée.
- « Hors parcours recommandé » n'est **pas** décidable mécaniquement : le contrôle s'en tient à (présence) + (co-présence même ligne) + (absence des blocs `console`) et **écrit cette limite dans le module** (D-26).

---

## Métadonnées

**Périmètre de recherche des analogues :** `docs/**` (2 fichiers), `tests/**` (3 fichiers livrés + `conftest.py`), `README.md`, `dofus_stuff/cli.py` (lu intégralement), `fetcher.py`, `pyproject.toml`, `.planning/phases/01-…/01-REVIEW.md`, `01-REVIEW-FIX.md`, `.claude/CLAUDE.md` § 4.3.
**Fichiers scannés :** 7 (tous git-suivis, vérifié par `git ls-files`).
**Vérifications exécutées pendant la cartographie** (interpréteur `.venv/Scripts/python.exe`, aucune écriture sous `docs/` ni `.data/`, `main()` jamais appelé) :

- `-m pytest -q` → `158 passed in 1.67s` (état **avant** cette phase) ;
- invariants de phase 1 appelés sur une **copie jetable** de `docs/` : avec `cli.md` + l'entrée `| [CLI](cli.md) | … |` → 0 problème sur `problemes_index`, `problemes_h1`, `problemes_retour_sommaire`, `problemes_encodage`, `problemes_liens` ; **sans** l'entrée → les 2 problèmes verbatim cités au § 2 ; arbre livré intact (`docs/` = `installation.md`, `sommaire.md`) ;
- sondes du parseur public : défauts globaux (`timeout=15`, `force_sync=False`, `offline=False`), `format_usage()` → `{version,self-test,search,item,list,optimize,db,cache}`, `db`/`cache` nus → `SystemExit 2`, `db clear` / `cache clear` / `optimize --jet average` / `optimize --demo` acceptés, `optimize --jet` sans valeur → `SystemExit 2` ;
- conventions de fichier : CRLF intégral et absence de BOM sur les 6 fichiers de référence ; `read_text` normalise les fins de ligne, `write_text` réécrit CRLF sur ce poste.

**Date d'extraction des patrons :** 2026-09-11.
**Validité :** tant que `dofus_stuff/cli.py` et les 3 modules de `tests/` de la phase 1 sont inchangés — toute modification de l'un d'eux invalide la mesure et la ligne citée.
