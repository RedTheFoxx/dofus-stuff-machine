# Phase 5: Base locale, hors-ligne et resynchronisation - Pattern Map

**Mapped:** 2026-09-11
**Files analyzed:** 4 (2 créés, 2 modifiés) — aucun fichier de `dofus_stuff/**` (D-88)
**Analogs found:** 4 / 4
**Méthode :** tous les extraits ci-dessous sont **cités du fichier réel**, lus cette session avec
`Read` / `awk` sur `C:/Users/Red/Documents/Projets/dofus-stuff-machine`. Les numéros de ligne sont ceux
du dépôt à cette date. Chaque analogue a été vérifié **git-tracked** (`git ls-files -- <chemin>` non
vide) : **aucun chemin d'un miroir gitignoré n'est cité**.
**Mesures de cette session (interpréteur épinglé `./.venv/Scripts/python.exe`) :** suite complète
**`205 passed in 3.58s`** ; `.data/dofus.sqlite3` empreinte **identique avant et après**
(`24989696` / `mtime_ns 1788730056843137500` /
sha256 `e3793d64cb7939ad1a51837b075b6b95e03d64c878fcb9cc07f86c00bb8fef7b`) ; `tests/test_docs_wizard.py`
seul : **`18 passed in 0.60s`**.

## File Classification

| New/Modified File | Role | Data Flow | Closest Analog | Match Quality |
|-------------------|------|-----------|----------------|---------------|
| `docs/base-locale.md` (créé par cette phase) | page de documentation (`docs/`) | transform (texte rédigé depuis des **constantes publiques** et un **rendu mesuré**) | `docs/wizard-avance.md` | exact (même gabarit D-01/D-69, même méthode) |
| `docs/base-locale.md` — variante « page qui cite des commandes » | page de documentation | transform | `docs/cli.md` (blocs ```` ```console ```` d'exemples + ```` ```text ```` de citation) et `docs/installation.md` (page du **premier contact**, dont plusieurs énoncés de cette phase sont déjà les siens) | role-match |
| `tests/test_docs_base_locale.py` (créé par cette phase) | test / module d'ancrage | request-response (client de test Flask **+** capture de `_print_db_status`) **et** transform (constats) | `tests/test_docs_wizard.py` | exact |
| `tests/test_docs_base_locale.py` — fonction pure de constats | fonction pure de test | transform (`texte` → `list[str]`) | `tests/test_docs_wizard.py::renvois_obsoletes` (`:674`) et `tests/test_docs_structure.py::problemes_*` (`:39-119`, `:337-447`) | exact (même contrat : entrées explicites, sortie `list[str]`) |
| `docs/sommaire.md` (modifié : **une** ligne d'index, D-70) | index / configuration | transform | lui-même (`tests/test_docs_structure.py` le garde) | exact |
| `tests/test_docs_parcours.py` (modifié : la réserve `PAGES_INEXISTANTES`, D-63) | test / module d'ancrage | transform (une constante + son commentaire) | lui-même, patron posé en phase 4 | exact |

**Sources de code (source de vérité, non modifiées par cette phase, D-88)** — toutes **git-tracked**,
vérifiées une à une cette session :

| Fichier | Ce que la page y ancre | Lignes utiles (mesurées) |
|---------|------------------------|--------------------------|
| `dofus_stuff/database.py` | `DB_NAME`, `DEFAULT_DATA_DIR`, `META_*`, `ITEM_KINDS`, schéma, `clear()`, `stats()` | `:12`, `:13`, `:15`, `:16`, `:18-26`, `:35-36`, `:38-62`, `:69-73`, `:146-152`, `:154-161` |
| `dofus_stuff/sync.py` | `CHECK_INTERVAL_SECONDS`, `ensure_up_to_date`, garde `offline` | `:11`, `:14-69` (garde `:41-50`), `:74-115` (`replace_kind` `:104`) |
| `dofus_stuff/api.py` | `SYNC_SOURCES` (les 7 kinds réellement stockés) | `:19-28` |
| `dofus_stuff/cli.py` | options globales, sous-commandes `db`, `_print_db_status`, refus `db sync --offline`, branche `clear` | `:32-57` (`:42-45`, `:47-50`, `:52`), `:179-194`, `:214-229`, `:329-360` (`:335-341`, `:344-347`, `:357-360`) |
| `dofus_stuff/web/__main__.py` | le défaut hors-ligne du web et son aide | `:13-36` (`:22-26`, `:28-31`), `:39-48` (`:41`) |
| `dofus_stuff/web/routes.py` | écrans `DB-01`…`DB-04`, `SAV-01`, `offline=False` en dur | `:143-150`, `:197`/`:236`, `:709-727`, `:744-785`, `:788-804`, `:807-840` (`:820-826`), `:843-860`, `:1280-1295` |
| `dofus_stuff/web/static/js/terminal.js` | ce que `PURGE OUI` détruit réellement | `:370`, `:459-466`, `:469-470`, `:494` |

**Encodage et fins de ligne — mesurés cette session, fichier par fichier** (lecture binaire ;
`CRLF` = `octets.count(b"\r\n")`, `fins` = `octets.count(b"\n")`, BOM = premiers octets `ef bb bf`) :

| Fichier | Octets | fins | CRLF | BOM |
|---------|--------|------|------|-----|
| `docs/cli.md` | 9381 | 195 | 195 | non |
| `docs/installation.md` | 7380 | 141 | 141 | non |
| `docs/parcours-simplifie.md` | 20138 | 269 | 269 | non |
| `docs/sommaire.md` | 703 | 22 | 22 | non |
| `docs/wizard-avance.md` | 16554 | 224 | 224 | non |
| `README.md` | 5231 | 123 | 123 | non |
| `GUIDE_WIZARD.md` | 561 | 18 | 18 | non |
| `tests/conftest.py` | 9617 | 262 | 262 | non |
| `tests/test_docs_cli.py` | 54013 | 1060 | 1060 | non |
| `tests/test_docs_code_anchor.py` | 11678 | 255 | 255 | non |
| `tests/test_docs_parcours.py` | 157418 | 2990 | 2990 | non |
| `tests/test_docs_structure.py` | 26214 | 603 | 603 | non |
| `tests/test_docs_wizard.py` | 141111 | 2721 | 2721 | non |
| `tests/test_optimize.py` | 13011 | 392 | 392 | non |
| `tests/test_profile_input.py` | 2912 | 87 | 87 | non |
| `tests/test_recommend.py` | 5142 | 107 | 107 | non |
| `tests/test_screens.py` | 2299 | 85 | 85 | non |
| `tests/test_solver_spec.py` | 4679 | 152 | 152 | non |
| `tests/test_web.py` | 25456 | 758 | 758 | non |
| `tests/fixtures/guide-wizard-obsolete.md` | 1596 | 39 | 39 | non |

→ Convention **uniforme** : `100 % CRLF`, **aucun BOM**, `0` fin de ligne LF seule. Les deux fichiers
produits par cette phase (`docs/base-locale.md` et `tests/test_docs_base_locale.py`) s'écrivent donc en
**UTF-8 sans BOM, fins de ligne CRLF** (D-67, D-69, D-90). L'assertion correspondante existe verbatim
dans deux modules et se recopie : `tests/test_docs_wizard.py:1833-1840` (page) et, pour l'empreinte,
`tests/test_docs_wizard.py:826-833`. **Limite (AR-5, Pitfall 11 de la recherche) :** cette assertion
n'est pas portable hors d'un poste dont `git config core.autocrlf` vaut `true` (mesuré `true` ici ;
aucun `.gitattributes` n'existe) — elle est à écrire comme les phases 3 et 4 l'ont écrite, **sans la
présenter comme portable**.

## Pattern Assignments

### `docs/base-locale.md` (page de documentation, transform)

**Analog principal :** `docs/wizard-avance.md` (224 lignes, CRLF, git-tracked) — la page livrée par la
phase 4, écrite exactement sous le gabarit que D-69 impose ici : `H1` nu, introduction en français,
sections de niveau 2, bloc « Source de vérité » dont **chaque chemin entre accents graves existe**, et
la ligne de retour en dernière ligne non vide.
**Analogs secondaires :** `docs/cli.md` (195 lignes) pour la forme des **blocs de commandes** (page
propriétaire de la surface CLI), `docs/installation.md` (141 lignes) pour les énoncés déjà écrits
ailleurs (premier contact, défaut hors-ligne du web), `docs/parcours-simplifie.md` (269 lignes) pour la
section « Ce que cette page ne décrit pas » (le patron de renvoi par lien).

#### 1. En-tête et introduction — verbatim (`docs/wizard-avance.md:1-3`)

```markdown
# Wizard avancé

Cette page décrit le parcours avancé de l'interface web, écran par écran, tel que l'outil le rend. Tous les titres, libellés, formats et touches cités ici sont lus sur le rendu réel : ils sont recopiés tels que le produit les affiche, jamais de mémoire. La surface des commandes n'est pas recopiée ici : elle appartient à [la page CLI](cli.md), et le wizard avancé n'existe que dans l'interface web, il n'a aucune commande en ligne de commande.
```

Structure mesurée : ligne 1 = `H1` **nu** (aucun gras, aucun suffixe) ; ligne 2 = ligne vide ; ligne 3 =
**un seul** paragraphe qui (a) dit d'où viennent les énoncés, (b) dit ce que la page ne recopie **pas**,
(c) renvoie à la page voisine **par lien**, jamais en prose (`[la page CLI](cli.md)`).

Comparaison `docs/cli.md:1-5` (même forme, introduction plus courte, portée du parseur) :

```markdown
# CLI

Cette page décrit la ligne de commande de dofus-stuff-machine : les sous-commandes de `fetcher.py`, les options qu'elles acceptent, les valeurs par défaut relevées dans le parseur et un exemple analysable par commande.

Le point d'entrée est `fetcher.py`, à la racine du dépôt : les commandes de cette page s'écrivent depuis cette racine. Le parseur de la ligne de commande ne connaît que les options déclarées dans `dofus_stuff/cli.py` : cette page n'en présente donc aucune qui ne soit définie dans le produit.
```

→ Pour `docs/base-locale.md` : `H1` = `# Base locale` (**exactement**, cf. § 3 ci-dessous), puis une
introduction qui dit que les énoncés viennent des **constantes publiques** (`DB_NAME`, `ITEM_KINDS`,
`CHECK_INTERVAL_SECONDS`) et du **rendu** des deux surfaces, et que la surface des commandes reste
propriété de `docs/cli.md` (D-68/D-86) — renvoi **par lien** `[la page CLI](cli.md)`, cible existante.

#### 2. Ordre et niveaux de titres — mesurés (`docs/wizard-avance.md`)

| Niveau | Ligne | Titre |
|--------|-------|-------|
| `H2` | 5 | `## Arriver au wizard` |
| `H2` | 33 | `## Les 9 étapes du wizard` |
| `H2` | 49 | `## Slots et filtres` |
| — `H3` | 53 / 69 / 86 / 92 | `### Les 11 emplacements` / `### Les 10 filtres de type` / `### Ce que la saisie accepte` / `### Erreurs et refus` |
| `H2` | 99 | `## Les 11 options du solveur` |
| `H2` | 126 | `## Les quatre nombres d'une ligne` |
| `H2` | 141 | `## Interdire, forcer, retirer un objet` |
| `H2` | 167 | `## Touches et commandes` |
| — `H3` | 187 | `### Les commandes du récapitulatif` |
| `H2` | 200 | `## Exemple guidé` |
| `H2` | 216 | `## Source de vérité` |
| (texte) | 224 | `[Retour au sommaire](sommaire.md)` |

Le gabarit est **`H2` pour les sections, `H3` pour les sous-blocs**, et le **dernier `H2` est toujours
`## Source de vérité`**. `docs/cli.md` porte le même dernier titre (`:188`), suivi de la ligne de retour
`:195` ; `docs/installation.md` : `## Source de vérité` `:131`, retour `:141` ; `docs/parcours-simplifie.md` :
`:258` et `:269`. **Les quatre pages de `docs/` finissent donc par `## Source de vérité` puis la ligne de
retour** : c'est la forme à suivre, jamais une invention locale.

**Fait mesuré à ne pas recopier de `wizard-avance.md` :** cette page **ne porte aucun bloc de code**
(vérifié : `grep -n '^```' docs/*.md` ne renvoie **rien** pour `docs/wizard-avance.md`), et son module
d'ancrage **interdit** le bloc ```` ```console ```` (`BALISE_COMMANDE = "```console"`,
`tests/test_docs_wizard.py:212`, contrôlé à `:1822-1826`). `docs/base-locale.md`, elle, **cite des
commandes** (`db status`, `db sync`, `db clear`, `PURGE OUI`) : le choix du balisage est structurant et
doit être **arrêté par le plan**, car il décide de ce qu'un contrôle peut lire :

| Balisage | Ce qu'il vaut pour le harnais | Exemples mesurés |
|----------|-------------------------------|------------------|
| ```` ```console ```` | **Exemple exécutable** : `tests/conftest.py:151` (`BALISE_EXEMPLE = "console"`) et `:181-195` (`_lignes_exemple`) ne rendent que ces lignes ; c'est ce que `docs/cli.md` emploie pour ses exemples (`:36`, `:44`, `:57`, `:69`, `:82`, `:146`, `:154`, `:184`) | `docs/cli.md` |
| ```` ```text ```` | **Citation, jamais un exemple** : `_lignes_exemple` l'ignore ; `docs/cli.md` l'emploie là où la commande n'est **pas** à recopier (`:170-172`, section `db clear`, commande destructrice) et `docs/installation.md` l'emploie pour le message d'erreur (`:111-113`) | `docs/cli.md:170-172` |
| ```` ```bash ```` | Bloc de commandes d'installation, employé par `docs/installation.md` (`:17`, `:23`, `:31`, `:41`, `:75`, `:105`) et `README.md` (`:21`, `:27`, `:46`, `:77`, `:96`, `:117`) | `docs/installation.md` |
| aucun bloc | La page cite les commandes en ligne (`PROSE`) ; les contrôleurs `lignes_de_code`/`lignes_exemple` rendent alors une liste **vide** pour cette page | `docs/wizard-avance.md` |

**Conséquence mesurable pour D-80 :** `db clear` et `PURGE OUI` doivent être signalés destructeurs **sur
la même ligne** et **n'apparaître dans aucun bloc d'exemple**. Le patron déjà livré est
`docs/cli.md:174-178` : un titre qui étiquette la commande comme destructrice
(`` ### `db clear`, commande destructrice ``) et une phrase explicite, dans un bloc ```` ```text ````
(`:170-172`) — **jamais** un ```` ```console ````.

#### 3. La ligne d'index et l'égalité `H1` ↔ libellé — mesurés

**État actuel de `docs/sommaire.md` (22 lignes, verbatim, lignes 15-22) :**

```markdown
## Index

| Page | Sujet |
|------|-------|
| [Installation](installation.md) | Installer l'outil, vérifier, lancer CLI et web |
| [Parcours simplifié](parcours-simplifie.md) | Obtenir un stuff en 3 questions, lire puis sauvegarder le résultat |
| [CLI](cli.md) | Commandes, options et exemples de fetcher.py |
| [Wizard avancé](wizard-avance.md) | Les 9 étapes du wizard, ses filtres, ses formats et ses touches |
```

La table d'index porte **4 lignes** (lignes 19-22) ; son en-tête est `| Page | Sujet |` (ligne 17) et son
séparateur `|------|-------|` (ligne 18). Le « Parcours conseillé » (lignes 5-13) liste déjà le thème en
**prose**, sans lien :

```markdown
5. Base locale
```
*(`docs/sommaire.md:11` — mesuré : `problemes_index` ne lit que les **cibles de liens**, cette ligne
n'entre donc dans aucun ensemble)*

→ La ligne à ajouter est **unique**, **en fin de table** (après la ligne 22), sur le patron exact des
quatre existantes :

```markdown
| [Base locale](base-locale.md) | <sujet, forme identique aux quatre autres lignes> |
```

**Les quatre gardes qu'une ligne d'index doit satisfaire (déjà écrites, **inchangées** — le plan ne les
re-prouve pas) :**

**(a) Exhaustivité bidirectionnelle** — `problemes_index`, `tests/test_docs_structure.py:92-119`, avec
`LINK = re.compile(r"\[[^\]]*\]\((?P<target>[^)\s]+)\)")` (`:7`) :

```python
    cibles = set(LINK.findall(sommaire.read_text(encoding="utf-8")))
    pages = {
        page.relative_to(docs_dir).as_posix()
        for page in _pages(docs_dir)
        if page.name != "sommaire.md"
    }
```
*(`:100-105`)* — créer la page **sans** la ligne fait rougir (`page non listee dans docs/sommaire.md`,
`:113-116`) et ajouter la ligne **sans** la page aussi (`cible listee absente sur disque`, `:108-112`).
**Les deux vont dans le même commit.**

**(b) `H1` unique égal au libellé d'index** — `problemes_h1`, `tests/test_docs_structure.py:337-380`
(extrait `:371-380`) :

```python
        if len(titres) != 1:
            problemes.append(
                f"{nom} : {len(titres)} titre(s) H1 dans {page.as_posix()} ; attendu un "
                f"unique H1 egal au libelle d'index « {libelle} » de docs/sommaire.md "
                f"(SOMM-03, D-11)"
            )
            continue
        if libelle is not None and normalize(titres[0]) != normalize(libelle):
            problemes.append(
                f"{nom} : H1 « {titres[0]} » different du libelle d'index « {libelle} » ; "
                f"attendu le libelle d'index de docs/sommaire.md pour {page.as_posix()} "
                f"(SOMM-03, D-11)"
            )
```

avec `H1 = re.compile(r"^#\s+(?P<title>.+?)\s*$", re.MULTILINE)` (`:8`) et
`LIEN_LIBELLE = re.compile(r"\[(?P<libelle>[^\]]*)\]\((?P<cible>[^)\s]+)\)")` (`:309`), lus par
`pages_listees` (`:326-334`). **Conséquence pour cette phase :** D-70 fixe le libellé `Base locale`,
donc la page commence **exactement** par `# Base locale` — ni `# Base locale et hors-ligne`, ni
`# Base locale (SQLite)`, ni `# Base Locale`. L'égalité est **normalisée** (D-11 : accents, casse,
espaces), donc `# BASE LOCALE` passerait : la forme à écrire reste celle du libellé, comme les quatre
lignes existantes. L'unicité du libellé est contrôlée par
`test_sommaire_index_labels_are_unique` (`tests/test_docs_structure.py:468-492`) : `Base locale` n'est
porté par aucune entrée d'index (la ligne 11 est de la prose, hors `pages_listees`).

**(c) Ligne de retour vers le sommaire** — `problemes_retour_sommaire`, `tests/test_docs_structure.py:383-417`
(exige **au moins un** lien dont la cible résolue est `docs/sommaire.md`) ; la convention mesurée sur les
4 pages est **la dernière ligne non vide** (cf. § 2) — c'est aussi ce que la phase 4 exige de sa propre
page (`tests/test_docs_wizard.py:1814-1820`).

**(d) Encodage, brouillon, longueur** — `problemes_encodage`, `tests/test_docs_structure.py:418-447`,
avec les constantes `:312-315` :

```python
JETONS_BROUILLON = ("todo", "a completer", "lorem")

# Longueur minimale d'une page livree, en caracteres (GARD-01).
LONGUEUR_MINIMALE = 300
```

→ `docs/base-locale.md` doit faire **≥ 300 caractères** après `strip()` (`:440-447`), ne porter aucun
jeton de brouillon, et se décoder en UTF-8 strict (`_lire_page`, `:318-323`).

#### 4. Gardes de liens — `problemes_liens`, `tests/test_docs_structure.py:39-89`

Pour **chaque** lien de la page (extraits `:47-88`) : les cibles externes (`http://`, `https://`,
`mailto:` — `LIENS_EXTERNES`, `:10`) sont **ignorées** (`continue`, `:48-49`) ; une cible portant `#`,
un chemin absolu, un antislash ou `file://` est **refusée** ; une cible qui sort de la racine du dépôt
est refusée ; une cible qui ne résout pas est refusée (`lien mort vers {cible}`). Les cibles de la
nouvelle page sont donc, au choix : `sommaire.md`, `cli.md`, `installation.md`, `parcours-simplifie.md`,
`wizard-avance.md` — **toutes existantes** (vérifié) — et **aucun chemin absolu, aucune ancre, aucun
antislash**. La page n'a besoin d'aucun lien externe ; la phase 4 interdit `](http` sur la sienne
(`FRAGMENT_LIEN_EXTERNE`, `tests/test_docs_wizard.py:210`), et il est cohérent de reprendre cette règle
pour la page 5 (patron, non obligation générale : `test_docs_structure.py` les tolère).

#### 5. Bloc « Source de vérité » — verbatim (`docs/wizard-avance.md:216-222`)

```markdown
## Source de vérité

- `dofus_stuff/web/optimize_wizard.py` : liste ordonnée des étapes (`WIZARD_STEPS`), titres rendus (`STEP_TITLES`), libellés d'emplacements (`SLOT_GROUP_LABELS`), libellés de filtres (`TYPE_FILTER_LABELS`), lignes des onze options, des listes de statistiques et des items, et formats d'édition.
- `dofus_stuff/web/routes.py` : route `/optimize/wizard/<etape>`, ligne d'en-tête, lignes de statut, sous-écrans d'édition et barre de touches.
- `dofus_stuff/model/solver_spec.py` : ordre des emplacements (`SLOT_GROUPS`) et touches des filtres de type (`TYPE_FILTER_KEYS`).
- `dofus_stuff/web/screens.py` : mise en page de l'écran et pagination du corps.
- `dofus_stuff/web/templates/screen.html` : gabarit HTML réellement rendu, dont la ligne de statut.
```

Comparaison `docs/cli.md:188-194` (phrases plus longues, un chemin par ligne, même forme) :

```markdown
## Source de vérité

- `fetcher.py` : point d'entrée de la ligne de commande.
- `dofus_stuff/cli.py` : parseur et commandes réellement disponibles ; la fonction `build_parser()` y déclare la surface documentée ici.
- `dofus_stuff/database.py` : suppression effective des tables par `db clear`, la commande destructrice qui vide la base locale.
- `dofus_stuff/optimize/profile_input.py` : choix du mode interactif de l'optimisation.
```

**Ce que le contrôle exigera de ce bloc** — patron `tests/test_docs_wizard.py:1843-1870` : le corps de la
section est extrait par la fixture `section(texte, TITRE_SOURCE, PAGE)` (helper partagé
`tests/conftest.py:214-228`, `page` **obligatoire**), puis **chaque chemin entre accents graves du
document entier** est confronté au disque :

```python
    chemins = sorted(set(CHEMIN_CITE.findall(texte)))
    if not chemins:
        constats.append(
            f"{PAGE} : la page ne cite aucun chemin de code ; attendu au moins un chemin, la page "
            f"ancrant ses libelles sur le code de ce depot"
        )
    for cite in chemins:
        if not (RACINE_DEPOT / cite).exists():
            constats.append(
                f"{PAGE} : la page cite « {cite} » et ce chemin n'existe pas ; attendu un chemin "
                f"existant, un chemin disparu signalant une page desalignee"
            )
```
*(`tests/test_docs_wizard.py:1851-1868`, avec
`CHEMIN_CITE = re.compile(r"`(?P<chemin>[\w./-]+\.(?:py|toml|js|md|json|sql))`")` `:207`)*

→ Chemins **vérifiés présents** cette session, candidats pour le bloc de `docs/base-locale.md` :
`dofus_stuff/database.py`, `dofus_stuff/sync.py`, `dofus_stuff/api.py`, `dofus_stuff/cli.py`,
`dofus_stuff/web/__main__.py`, `dofus_stuff/web/routes.py`,
`dofus_stuff/web/static/js/terminal.js`. **Ne citer aucun chemin inventé** (le contrôle ci-dessus le
refuse), et **aucun nom privé** de fonction comme source d'ancrage public (D-14).

---

### `tests/test_docs_base_locale.py` (test d'ancrage, request-response + transform)

**Analog :** `tests/test_docs_wizard.py` (2721 lignes, **18 tests**, `18 passed in 0.60s` mesuré cette
session, git-tracked) — le patron le plus proche, écrit par la phase 4 pour une page dont la vérité est
**le rendu**. Les onze éléments ci-dessous couvrent tout ce dont le nouveau module a besoin ; le plan
peut dire « suivre cette forme » sans re-dériver quoi que ce soit. Pour chaque élément : **réutilisable
tel quel**, **à adapter**, ou **à ne pas copier**.

#### 1. En-tête du module : contrat + limites nommées — verbatim (`:1-19`, extrait)

```python
"""Ancrage de la page `docs/wizard-avance.md` sur le rendu reel du wizard avance.

Le contrat va du rendu vers la page : les neuf ecrans du wizard avance sont rendus par le client de
test Flask, en processus, sur la fixture `app` de `tests/conftest.py` (D-32), puis les titres, les
libelles, les formats et les messages lus dans le corps, dans la ligne de statut et dans la ligne
d'en-tete sont compares a ceux que la page cite. Aucun serveur n'est lance, aucun socket n'est
ouvert, le programme du produit n'est jamais execute et rien n'est ecrit sous `.data/` : la fixture
`app` construit sa propre base dans un dossier temporaire.

Limite nommee : la garde `ast` de ce module est une demonstration statique et indirecte. ...

Limite nommee : la prose libre de la page (les phrases d'explication) n'est pas verifiee par un
test. Les controles portent sur les libelles, les nombres et les messages **cites**, et ce module ne
revendique aucune exhaustivite de la redaction.
"""
```

**Réutilisable (forme).** Les trois paragraphes du patron — contrat, puis **« Limite nommee : … »** —
sont exactement ce que D-85 exige : les limites sont écrites **dans le module** et pas seulement dans
un message d'échec. Les limites à écrire pour la phase 5 sont déjà inventoriées : la garde `ast` ne
contraint que le module committé (L-1 de `04-SECURITY.md`) ; l'empreinte locale est vraie par
construction (L-2) ; **la prose libre n'est pas vérifiée, seules les valeurs citées le sont** ;
**l'exécution JavaScript de `PURGE OUI` n'est pas observable** (aucun navigateur : `PURGE OUI` ne peut
être prouvé qu'au **rendu** de `SAV-01` **et** par la lecture de
`dofus_stuff/web/static/js/terminal.js`) ; l'assertion CRLF n'est pas portable (AR-5).

#### 2. Imports et constantes de chemin — verbatim (`:26-53`)

```python
from __future__ import annotations

import ast
import hashlib
import html
import re
import unicodedata
from pathlib import Path

import pytest

from dofus_stuff.model.solver_spec import SLOT_GROUPS, TYPE_FILTER_KEYS
from dofus_stuff.web.optimize_wizard import (
    STEP_TITLES,
    TYPE_FILTER_LABELS,
    WIZARD_STEPS,
)

RACINE_DEPOT = Path(__file__).resolve().parents[1]
PAGE = "wizard-avance.md"
SOMMAIRE = "sommaire.md"
GUIDE_WIZARD = "GUIDE_WIZARD.md"
README = "README.md"
SOURCE_ROUTES = "dofus_stuff/web/routes.py"
SOURCE_WIZARD = "dofus_stuff/web/optimize_wizard.py"
SOURCE_SPEC = "dofus_stuff/model/solver_spec.py"
SOURCE_SCREENS = "dofus_stuff/web/screens.py"
SOURCE_TEMPLATE = "dofus_stuff/web/templates/screen.html"
```

**À adapter.** Le nouveau module **importe en plus** (et c'est l'objet de la réécriture de la garde
`ast`, cf. § 6) :

```python
from dofus_stuff.database import DB_NAME, ITEM_KINDS, Database, META_GAME_VERSION, META_LAST_CHECKED_AT
from dofus_stuff.sync import CHECK_INTERVAL_SECONDS
from dofus_stuff.cli import build_parser as parseur_cli, _print_db_status
from dofus_stuff.web.__main__ import build_parser as parseur_web
```

Constantes de chemin par analogie (les fichiers sont tous cités dans la § *Sources de code* ci-dessus) :
`SOURCE_DATABASE = "dofus_stuff/database.py"`, `SOURCE_SYNC = "dofus_stuff/sync.py"`,
`SOURCE_CLI = "dofus_stuff/cli.py"`, `SOURCE_WEB_MAIN = "dofus_stuff/web/__main__.py"`,
`SOURCE_ROUTES = "dofus_stuff/web/routes.py"`, `SOURCE_TERMINAL_JS = "dofus_stuff/web/static/js/terminal.js"`.

**Mesures faites cette session (à citer comme attendus, jamais recopiées de mémoire)** : `DB_NAME` vaut
`'dofus.sqlite3'` (`database.py:12`) ; `ITEM_KINDS` a **7** éléments et **égale** `tuple(kind for _,
_, kind in SYNC_SOURCES)` (mesuré `True` ; `database.py:18-26` / `api.py:19-28`) ; `CHECK_INTERVAL_SECONDS`
vaut `86400` (`sync.py:11`) ; `Database()` sans argument lève
`TypeError: Database.__init__() missing 1 required positional argument: 'data_dir'` — l'accident « base
réelle par omission » est **impossible**, seul `Database(data_dir=DEFAULT_DATA_DIR)` serait fautif.

#### 3. Marqueurs du rendu et lecteurs — verbatim (`:91-94`, `:333-375`)

```python
MARQUEUR_CORPS = 'id="body">'
MARQUEUR_STATUT = '<div class="row status'
MARQUEUR_ENTETE = '<div class="row header" id="header-row">'
LIGNE_CORPS = re.compile(r'<div class="row">(.*?)</div>', re.S)
```

```python
def _texte_page(docs_dir: Path) -> str:
    """Texte de la page, lu en UTF-8 explicite ; page absente = AssertionError localisante (D-13)."""
    chemin = docs_dir / PAGE
    if not chemin.is_file():
        raise AssertionError(
            f"{PAGE} : page introuvable ({chemin}) ; attendu la page du wizard avance "
            f"decrite par {SOURCE_WIZARD}, livree dans docs/"
        )
    return chemin.read_text(encoding="utf-8")


def _lignes_du_corps(reponse) -> list[str]:
    """Lignes visibles du corps de l'ecran, jamais la reponse entiere."""
    texte = reponse.get_data(as_text=True)
    corps = texte.split(MARQUEUR_CORPS, 1)[1].split(MARQUEUR_STATUT, 1)[0]
    return [ligne.rstrip() for ligne in LIGNE_CORPS.findall(corps)]


def _statut(reponse) -> str:
    """Texte de la ligne de statut : la seule source des messages de refus."""
    texte = reponse.get_data(as_text=True)
    return texte.split(MARQUEUR_STATUT, 1)[1].split(">", 1)[1].split("</div>", 1)[0]
```

**Réutilisable tel quel** (les trois marqueurs viennent de
`dofus_stuff/web/templates/screen.html` et valent pour **tous** les écrans, `DB-01`…`DB-04` et `SAV-01`
compris — vérifié cette session). **Ne jamais** asserter sur la réponse entière : `_lignes_du_corps`
extrait le corps entre `id="body">` et la ligne de statut.

**Mesures faites cette session** (base `tmp_path` peuplée par l'équivalent de la fixture `app` ;
`GET` seulement, aucun POST, aucun `main()`) :

```
/db         200  STATUT| ENTREE=VALIDER
   CORPS| 1. ETAT DE LA BASE (STATUS)
   CORPS| 2. SYNCHRONISATION FORCEE (SYNC)
   CORPS| 3. VIDER LA BASE (CLEAR)
   CORPS| SELECTIONNEZ UNE OPTION ET APPUYEZ SUR ENTREE :
/db/status  200  STATUT| &nbsp;
   CORPS| FICHIER : …\data\dofus.sqlite3
   CORPS| VERSION JEU : 9.9.9.9
   CORPS| DERNIER CHECK : (AUCUN)
   CORPS| ENTREES : 3
   CORPS| PAR CATEGORIE :
   CORPS| - equipment : 2
   CORPS| - resources : 1
/db/sync    200  STATUT| ENTREE=VALIDER
   CORPS| CETTE OPERATION CONTACTE L&#39;API DOFUSDUDE
   CORPS| ET PEUT PRENDRE PLUSIEURS MINUTES.
   CORPS| CONFIRMER ? (O=OUI / N=NON)
/db/clear   200  STATUT| OPERATION DESTRUCTIVE — ENTREE=VALIDER
   CORPS| ATTENTION : TOUTES LES ENTREES LOCALES SERONT SUPPRIMEES.
   CORPS| CONFIRMER ? (O=OUI / N=NON)
/saves      200  STATUT| N OUVRIR | DEL N | PURGE OUI — ENTREE=VALIDER
   CORPS| CHARGEMENT DES SAUVEGARDES LOCALES…
```

**Deux faits mesurés qui décident de la rédaction du contrôle :**

1. **L'apostrophe est rendue `&#39;`** (`CETTE OPERATION CONTACTE L&#39;API DOFUSDUDE`). Toute
   comparaison de libellé passé par le HTML doit passer par la fixture `normalize`
   (`tests/conftest.py:119-124`, qui fait `html.unescape` puis NFKD/casse/espaces — D-11) ; c'est
   exactement ce que fait le patron (`[normalize(ligne) for ligne in _lignes_du_corps(reponse)]`).
   **Ne pas** normaliser les libellés CLI, dont l'écart d'accent est le fait à préserver (Pitfall 4).
2. **Les lignes vides d'une ligne `CORPS|` seule et le `STATUT| &nbsp;` de `/db/status`** sont normaux :
   `1 <= len(lignes)` et l'écran d'état n'a **aucun** message de statut. Le patron interdit d'asserter
   sur la longueur exacte (`tests/test_docs_parcours.py:541-556` est le modèle de cette précaution :
   « les lignes du corps ne sont pas la réponse entière »).

#### 4. L'ancrage des cinq libellés CLI — hors du patron wizard

**Analog partiel :** `tests/test_docs_wizard.py` ne l'a pas (sa page n'a pas de surface CLI), mais le
mécanisme est **mesuré cette session** et la recherche le recommande (mécanisme 5) :

```python
import io
from contextlib import redirect_stdout

db = Database(data_dir=tmp_path / "absent")   # JAMAIS DEFAULT_DATA_DIR (D-81)
tampon = io.StringIO()
with redirect_stdout(tampon):
    _print_db_status(db)
db.close()                                     # <- obligatoire, cf. avertissement ci-dessous
```

Sortie réelle mesurée (répertoire **inexistant** avant l'appel) :

```
Fichier : C:\Users\…\absent\dofus.sqlite3
Version jeu : (aucune)
Dernier check : (aucun)
Entrées : 0
```
et, sur une base peuplée, `Par catégorie :` puis `  - equipment : 2` / `  - resources : 1`
(`dofus_stuff/cli.py:214-229` en est la source exacte ; condition `if isinstance(by_kind, dict) and by_kind`
ligne `:226`).

**Avertissement mesuré (gagne du temps au plan) :** `_print_db_status` appelle `db.stats()` →
`_require_conn()` → `open()` (`dofus_stuff/database.py:69-73`) : l'appel **crée le dossier et le
fichier** (mesuré : dossier `True`, fichier `True`) et **laisse la connexion ouverte**. Sans `db.close()`,
le nettoyage du dossier temporaire échoue sur Windows (`PermissionError: [WinError 32] … dofus.sqlite3`
— mesuré cette session). Le contrôle doit fermer la base qu'il a créée.

**Ce que ce mécanisme prouve / ne prouve pas** : il prouve que ces cinq libellés **sont produits** par la
fonction que `db status` appelle (`cli.py:340-342`), et que le fichier est créé ; il **ne** prouve pas que
`main()` les affiche tels quels (le chemin `main` n'est jamais parcouru, D-15) — écart à déclarer comme
limite. **Repli** si le plan refuse un nom privé : `ast` sur les littéraux de `_print_db_status`
(contrôle plus faible, cf. `04-PATTERNS` § 7(a)).

#### 5. Fonction pure + constats, et une seule assertion — verbatim (`:674-702`, `:2414-2448`, extraits)

```python
def renvois_obsoletes(texte: str, faits: dict) -> list[str]:
    """Constats de renvois obsoletes d'un texte, juges contre les faits du jeu courant (D-58, WIZ-03).

    **Fonction pure** : elle ne lit aucun fichier, n'ouvre aucune connexion et ne cite aucune
    constante de projet — les attentes lui arrivent par `faits` (mesurees au rendu, D-58) et chaque
    constat les nomme avec le **fichier de code qui les produit** (D-13, repris par D-65).
    ...
    **Limite honnete (D-58/D-26) :** ce detecteur ne revendique **aucune exhaustivite**. ...
    """
    lignes = [ligne.strip() for ligne in texte.splitlines()]
    constats: list[str] = []
    constats += _renvois_au_menu(lignes, faits)
    constats += _renvois_de_filtre(lignes, faits)
    constats += _renvois_a_l_arrivee(lignes, faits)
    return constats
```

et son enveloppe mince, qui ne fait qu'asserter (`:2414-2448`) :

```python
def test_aiguillage_sans_renvoi_obsolete(docs_dir: Path, app, normalize) -> None:
    """..."""
    chemin = RACINE_DEPOT / GUIDE_WIZARD
    ...
    texte = chemin.read_text(encoding="utf-8")
    faits = _faits_du_rendu(app, normalize)
    constats = renvois_obsoletes(texte, faits)

    assert not constats, (
        f"{GUIDE_WIZARD} : renvois obsoletes signales sur la page controlee : "
        + " ; ".join(constats)
        + f" ; attendu un aiguillage sans renvoi vers un menu, un filtre ou une arrivee disparus, "
        ...
    )
```

**Réutilisable (forme), c'est le contrat de D-83 :**
1. `constats: list[str]` accumulés dans **tout** le test, puis **une seule** assertion qui les joint
   (`assert not constats, f"{PAGE} : … " + " ; ".join(constats) + " ; attendu …"`).
2. Chaque constat nomme **la page**, **la valeur fautive**, **la valeur attendue** et **le fichier de
   code producteur** — jamais « le code » en général. Le patron emploie aussi
   `raise AssertionError(f"{PAGE} : page introuvable ({chemin}) ; attendu … ({SOURCE_X})")` pour une
   lecture impossible : **jamais** de `FileNotFoundError` brut (leçon IN-03, `:333-346`).
3. Une **fonction pure** (`texte` en entrée, `list[str]` en sortie) quand la matière doit être jugée sur
   deux textes : c'est ce qui rend une **morsure** mesurable sans écrire de fichier.

**À ne pas copier :** `_faits_du_rendu` (`:477-570`), `_renvois_au_menu` / `_renvois_de_filtre` /
`_renvois_a_l_arrivee` (`:573-672`), les motifs de page (`MOTIF_EMPLACEMENT_RENDU`, `MOTIF_LIGNE_*`,
`:102-181`) : ce sont les faits **du wizard**, sans emploi pour la base locale.

#### 6. La garde `ast` de clôture — **RÉÉCRITE, jamais recopiée** (obstacle n° 2)

**Ce que le patron fait, verbatim** (`tests/test_docs_wizard.py:311-330`) :

```python
# Racines dont un import signalerait un risque reel : ouvrir la base, lancer un processus, ouvrir une
# socket, joindre le reseau. Le controle porte sur le risque, jamais sur une liste blanche de modules
# produit a tenir a jour.
RACINES_INTERDITES = (
    "sqlite3",
    "subprocess",
    "socket",
    "multiprocessing",
    "ctypes",
    "webbrowser",
    "urllib",
    "requests",
    "http",
    "ftplib",
    "smtplib",
)

# Nom produit dont l'import signalerait que le module d'ancrage tire la base locale.
MODULE_BASE_INTERDIT = "dofus_stuff.database"

# Noms d'appel dont la presence signalerait une action destructive ou l'execution du produit.
APPELS_SUPPRESSION = ("remove", "unlink", "rmdir", "rmtree")
APPEL_PRODUIT = "main"
```
*(lignes `:311-323`, `:325-326`, `:328-330`)*

**Le contrôle qui doit disparaître, verbatim** (`tests/test_docs_wizard.py:949-955`) :

```python
    if MODULE_BASE_INTERDIT in importes or any(
        module.startswith(MODULE_BASE_INTERDIT + ".") for module in importes
    ):
        constats.append(
            f"import de « {MODULE_BASE_INTERDIT} » ; attendu aucun import de la base locale, la "
            f"fixture `app` construisant sa propre base temporaire ({SOURCE_WIZARD})"
        )
```

**Pourquoi c'est un obstacle, mesuré :** la source de `DB_NAME`, `ITEM_KINDS` et `Database` **est**
`dofus_stuff.database` : recopier la garde telle quelle ferait rougir le module **sur ses imports
légitimes** (Pitfall 2 de la recherche). La règle du patron est cependant à conserver : *« Le contrôle
porte sur le risque réel, jamais sur une liste blanche de modules produit à tenir à jour »* (`:308-310`).
Le risque est donc **déplacé**, pas supprimé :

| Élément du patron | Décision pour la phase 5 | Justification (mesurée) |
|-------------------|--------------------------|--------------------------|
| `RACINES_INTERDITES` (`:311-323`) | **réutiliser tel quel** | `sqlite3`/`socket`/`subprocess`/… restent interdits : la base se construit par `Database`, jamais par un `sqlite3.connect` écrit à la main, et rien n'ouvre de socket. Attention : `sqlite3` interdit **l'import direct** dans le module de test — c'est `dofus_stuff.database` qui l'utilise, pas le harnais |
| `APPELS_SUPPRESSION` (`:329`) | **réutiliser tel quel** | aucun `remove`/`unlink`/`rmdir`/`rmtree` dans le module : la base temporaire est nettoyée par pytest, jamais par un appel de suppression (D-81/D-89) |
| `APPEL_PRODUIT = "main"` (`:330`) | **réutiliser tel quel** | `main()` n'est jamais exécuté (D-15, `tests/test_docs_cli.py:17`) ; le refus de `db sync --offline` se prouve par le **littéral** lu dans `cli.py` (cf. § 7) |
| `MODULE_BASE_INTERDIT` (`:325-326`) et son contrôle (`:949-955`) | **SUPPRIMER** | le module de la phase 5 **doit** importer `dofus_stuff.database` (constantes publiques + `Database`) |
| (nouveau) `DEFAULT_DATA_DIR` interdit comme `data_dir` | **ajouter** | c'est le **vrai** risque de cette phase : `Database(data_dir=DEFAULT_DATA_DIR)` ouvrirait la base du dépôt. Le contrôle lit l'arbre `ast` et refuse tout appel `Database(...)` ou `create_app(...)` dont `data_dir` (positionnel **ou** nommé) n'est pas une expression issue de `tmp_path` — patron de lecture des arguments nommés déjà écrit : `:968-983` |
| (nouveau) paire de confirmation interdite | **ajouter, en adaptant `:968-983`** | le patron refuse `data={"cmd": "GO"}` ; l'analogue est `data={"confirm": "O" \| "Y" \| "OUI" \| "YES"}` — les quatre valeurs exactement acceptées par le produit (`dofus_stuff/web/routes.py:810`), mesuré. `POST /db/sync` avec confirmation déclenche `ensure_up_to_date(force=True, offline=False, …)` (`routes.py:820-826`) : réseau **et** écriture. `POST /db/sync` avec `confirm=N` est sans danger (mesuré : 302 vers `/db`, `routes.py:809-812`) mais **le module de la phase 5 ne poste jamais** (`tests/test_web.py:378-388` le fait, lui, en patchant `ensure_up_to_date`) |

**Verbatim du contrôle de paire à adapter** (`tests/test_docs_wizard.py:968-988`) :

```python
    for noeud in ast.walk(arbre):
        if not isinstance(noeud, ast.Call):
            continue
        for mot in noeud.keywords:
            if mot.arg != "data" or not isinstance(mot.value, ast.Dict):
                continue
            paires: dict[str, str] = {}
            for cle, valeur in zip(mot.value.keys, mot.value.values):
                if (
                    isinstance(cle, ast.Constant)
                    and isinstance(cle.value, str)
                    and isinstance(valeur, ast.Constant)
                    and isinstance(valeur.value, str)
                ):
                    paires[cle.value] = valeur.value
            if paires.get("cmd", "").strip().casefold() == "go":
                constats.append(
                    f"saisie `cmd` = « GO » postee ligne {noeud.lineno} ; attendu aucune saisie "
                    f"`GO` : elle lance le solveur par `_run_optimize_and_redirect` "
                    f"({SOURCE_ROUTES}:1114-1116) et redirige vers le resultat"
                )
```

**Helpers à réutiliser tels quels** — `_imports_du_module` (`:903-911`) et `_appels_du_module`
(`:914-925`) `ast.walk` l'arbre entier (imports imbriqués dans les fonctions compris) :

```python
def _imports_du_module(arbre: ast.AST) -> set[str]:
    """Modules importes par le module d'ancrage, imports imbattables compris dans les fonctions."""
    importes: set[str] = set()
    for noeud in ast.walk(arbre):
        if isinstance(noeud, ast.Import):
            importes.update(alias.name for alias in noeud.names)
        elif isinstance(noeud, ast.ImportFrom) and noeud.module is not None:
            importes.add(noeud.module)
    return importes
```

La garde s'auto-analyse : `ast.parse(Path(__file__).read_text(encoding="utf-8"))` (`:937`) — **jamais**
une recherche de chaînes, le module citant lui-même les noms interdits dans ses messages (`:930-932`).

#### 7. Morsures : témoin vert d'abord, mutation ensuite, **jamais sur l'arbre réel** — verbatim (`:2666-2720`, extrait)

```python
def test_arborescence_abregee_signalee_par_le_controle(docs_dir: Path, app, normalize) -> None:
    """La morsure du controle d'arborescence est prouvee par mutation (CR-01, arbitrage D-59b).

    Le temoin est mesure d'abord : le texte **livre** est conforme. Chaque mutation s'applique ensuite
    a une **copie en memoire** du fichier — le fichier du depot n'est jamais ecrit — et doit produire
    au moins un constat. ...

    Limite honnete : ce controle prouve la morsure sur les deux formes nommees ; il ne revendique
    aucune exhaustivite sur les facons d'ecrire une arborescence fautive.
    """
    ...
    texte = chemin.read_text(encoding="utf-8")
    menus = _faits_du_rendu(app, normalize)["menus"]

    temoin = _constats_arborescence(texte, menus, normalize)
    if temoin:
        raise AssertionError(
            f"{GUIDE_WIZARD} : le texte livre est deja signale par le controle d'arborescence : "
            + " ; ".join(temoin)
            + " ; attendu un texte conforme avant toute mutation, sans quoi la morsure mesuree "
            "porterait sur le fichier livre et non sur la mutation"
        )

    constats: list[str] = []
    for rendue, abregee in MUTATIONS_ARBORESCENCE:
        if rendue not in texte:
            constats.append(...)
            continue
        mute = _constats_arborescence(texte.replace(rendue, abregee), menus, normalize)
        if not mute:
            constats.append(
                f"{MOTIF_ARBORESCENCE} : la copie mutee portant « {abregee} » au lieu de "
                f"« {rendue} » n'est signalee par aucun constat ; attendu au moins un constat, sans "
                f"quoi les formes abreges que le detecteur tolere (D-47) passeraient une seconde fois "
                f"sous une phrase annoncant « l'arborescence reelle » (CR-01 de 04-REVIEW.md)"
            )
```

**Réutilisable (forme), c'est le contrat de D-84 :** (1) le **témoin** est mesuré **avant** la mutation et
son échec est un `raise` (« attendu un texte conforme avant toute mutation ») ; (2) la mutation vit sur
une **copie en mémoire** (`texte.replace(...)`, `str` pur) — **aucun fichier de documentation n'est
écrit**, `.data/` n'est pas approché ; (3) chaque morsure attend **au moins un constat** et le rapport
**cite la sortie réellement obtenue**.

**Deux différences mesurées avec la phase 4, à trancher par le plan :**
- Le patron mute **en mémoire** une chaîne ; `tests/test_docs_structure.py::test_mutation_detecte_les_trois_derives`
  (`:533-603`) mute une **copie disque sous `tmp_path`** (`shutil.copytree`, `:536`). Les deux formes
  existent dans le dépôt : pour la phase 5, la **copie `tmp_path`** est la seule qui permet de vérifier
  un constat qui lit un fichier **par chemin** (cas de `docs/base-locale.md` : la page est lue depuis
  `docs_dir`), l'autre restant valable pour une fonction pure `texte → constats`.
- Le nom du motif de morsure est porté par une **constante de module**, jamais écrit en clair dans la
  ligne d'assertion (`:214-217`, `:2459-2470`) : pytest reproduit la ligne source, une valeur en clair y
  serait trouvée **sans qu'aucun message n'ait été produit**. Règle posée au plan 03-03, tâche 2.

#### 8. Limites honnêtes — où elles s'écrivent (relevé exhaustif du patron)

| Emplacement | Ligne(s) | Forme |
|-------------|----------|-------|
| Docstring de module | `:10-13` | `Limite nommee : la garde `ast` de ce module est une demonstration statique et indirecte…` |
| Docstring de module | `:15-17` | `Limite nommee : la prose libre de la page … n'est pas verifiee par un test` |
| Constante de message | `:244-250` | `LIMITE_HONNETE = ("le detecteur couvre trois formes nommees … et ne revendique aucune exhaustivite : …")` — réutilisée **dans les messages d'assertion** des contrôles concernés (`:2378`, `:2446`) |
| Docstrings de test | `:685-693`, `:1880`, `:2177`, `:2286-2292`, `:2336-2340`, `:2393-2395`, `:2502-2504`, `:2636-2637`, `:2675-2676` | `**Limite honnete (D-58/D-26) :** …` / `**Limite de precision de la forme (a) :** …` |

**À reprendre telle quelle** : pour chaque contrôle de la phase 5, la phrase `Limite honnete :` **dans la
docstring du test**, et une **constante** quand la même limite doit apparaître dans plusieurs messages
(le patron le fait pour `LIMITE_HONNETE`). Les limites de la phase 5 sont **déjà listées** par la
recherche (§ *Security Domain*, dernières lignes) et par la § 1 ci-dessus.

#### 9. Octets de la page et empreinte de `.data/` — verbatim

**Contrôle CRLF/BOM du patron** (`tests/test_docs_wizard.py:1832-1840`, dans
`test_page_sans_derive_ni_chemin_invente`) :

```python
    fins = octets.count(b"\n")
    retours = octets.count(b"\r\n")
    if octets.startswith(BOM_UTF8):
        constats.append(f"{PAGE} : la page commence par un BOM ; attendu un fichier UTF-8 sans BOM")
    if retours != fins:
        constats.append(
            f"{PAGE} : la page porte {fins} fin(s) de ligne pour {retours} retour(s) chariot ; attendu "
            f"des fins de ligne CRLF sur toutes les lignes, comme les autres pages de docs/"
        )
```
avec `BOM_UTF8 = b"\xef\xbb\xbf"` (`:208`) et `octets = chemin.read_bytes()` / `texte = octets.decode("utf-8")`
(`:1785-1787`) : **on lit les octets**, jamais un texte ré-encodé. Le même contrôle existe dans
`tests/test_docs_parcours.py:2636-2648`.

**Empreinte** (`tests/test_docs_wizard.py:826-833`, **identiquement** dans
`tests/test_docs_parcours.py:2558-2566`) :

```python
def _empreinte(chemin: Path) -> tuple[int, int, str]:
    """Empreinte `(taille, mtime_ns, sha256)` d'un fichier, pour comparer deux instants (T-04-08).

    Les trois composantes sont rendues pour qu'un ecart dise laquelle a bouge : le SHA-256 porte le
    contenu, `mtime_ns` porte la modification a contenu identique. Le fichier est lu, jamais ecrit.
    """
    octets = chemin.read_bytes()
    return (len(octets), chemin.stat().st_mtime_ns, hashlib.sha256(octets).hexdigest())
```

et son `skip` nommé (`tests/test_docs_wizard.py:2293-2296`) :

```python
    chemin = docs_dir.parent.joinpath(*BASE_LOCALE)
    if not chemin.exists():
        pytest.skip(MOTIF_BASE_ABSENTE)
```
(`BASE_LOCALE = (".data", "dofus.sqlite3")` `:193`, `MOTIF_BASE_ABSENTE = "base locale absente : la
mesure d'empreinte n'a pas d'objet"` `:194`)

**À reprendre tel quel** — c'est la **3ᵉ copie assumée** de la même mesure (04-PATTERNS:530, « verbatim »),
avec sa limite écrite dans la docstring (`tests/test_docs_wizard.py:2286-2292`) : la mesure **locale** est
vraie par construction (la fixture construit sa base sous `tmp_path`, donc comparer la base du dépôt à
elle-même ne peut pas détecter l'écriture d'un **autre** module) ; le contrôle qui a ce pouvoir est la
mesure avant/après autour de la **suite entière**, faite par la vérification de plan. **Le `skip` reste
nominatif** : jamais un faux vert.

**Contrôle négatif déjà éprouvé, à reprendre pour `PURGE OUI`** — `tests/test_web.py:107-113` :

```python
def test_saves_screen(client):
    rv = client.get("/saves")
    assert rv.status_code == 200
    assert b"SAV-01" in rv.data or b"STUFFS SAUVEGARDES" in rv.data
    assert b'data-mode="saves"' in rv.data
    assert b"PURGE OUI" in rv.data
```
→ ce qui est prouvable est la **présence du libellé au rendu** ; l'**effet** est du JavaScript
(`terminal.js:459-466` : `localStorage.removeItem(SAVES_KEY)`), constatable seulement par **lecture de
la source** — jamais par une exécution.

#### 10. Le contrôle des renvois du `README.md` (D-87) — l'analog existe déjà à moitié

**Ce que le dépôt possède déjà** (`tests/test_docs_structure.py:190-212`) : **un seul** contrôle de
racine, sur le lien unique du README vers le sommaire (`:199-212`) :

```python
    cibles = [
        cible
        for cible in LINK.findall(readme.read_text(encoding="utf-8"))
        if cible == "docs/sommaire.md"
    ]
    assert len(cibles) == 1, (
        f"README.md : {len(cibles)} lien(s) vers docs/sommaire.md dans "
        f"{readme.as_posix()} ; attendu exactement 1 cible docs/sommaire.md (D-10)"
    )
```

**L'analog de la lecture généralisée** (`tests/test_docs_wizard.py:2593-2614`, section 5 de
`test_aiguillage_et_readme`, avec `MOTIF_LIEN_MARKDOWN` `:2475` et `CIBLE_SOMMAIRE` `:2459`) :

```python
    texte_readme = chemin_readme.read_text(encoding="utf-8")
    ...
    cibles_readme = [trouve.group("cible") for trouve in MOTIF_LIEN_MARKDOWN.finditer(texte_readme)]
    vers_sommaire = [cible for cible in cibles_readme if cible == CIBLE_SOMMAIRE]
    if len(vers_sommaire) != 1:
        constats.append(...)
```

**Mesure de l'inventaire réel de `README.md` cette session** (6 liens au total) :

| Libellé | Cible | Résout depuis la racine ? |
|---------|-------|---------------------------|
| `Sommaire de la documentation` (`README.md:7`) | `docs/sommaire.md` | **oui** |
| `Dofusdude` (`:11`) | `https://api.dofusdu.de/` | externe |
| `documentation` (`:11`) | `https://docs.dofusdu.de` | externe |
| `guide des caractéristiques` (`:72`) | `https://dofusbuilds.com/guides/characteristic-points` | externe |
| `Dofusdude` (`:123`) | `https://dofusdu.de/` | externe |
| `doduapi` (`:123`) | `https://github.com/dofusdude/doduapi` | externe |

→ Le contrôle D-87 doit donc **ignorer** les cibles externes (`http://`, `https://`, `mailto:`) et
vérifier que **chaque cible interne résout** depuis `RACINE_DEPOT`. **État initial mesuré : il n'y en a
qu'une, et elle résout** — le contrôle est donc **vert dès son écriture**, ce qui est le résultat
attendu (D-87 limite le travail du README à ses renvois, il n'y a **rien** à corriger dans le README).
**Limite à nommer :** le contrôle énumère les liens **Markdown** ; un chemin cité en prose n'est pas vu
(sauf s'il est entre accents graves et passe par `CHEMIN_CITE`, comme dans le patron `:1851-1868`).

**Point de périmètre à écrire dans le plan (Pitfall 8) :** `README.md:80` porte
`python fetcher.py db clear           # vider la base` **sans avertissement** — c'est la **seule**
occurrence du dépôt où une commande destructrice est présentée comme une étape, et elle est **hors du
mandat de réécriture** de cette phase (D-87). Le critère 4 doit donc être **délimité explicitement au
périmètre de la phase** (la nouvelle page et son module), comme la recherche le recommande ; le fait est
à consigner pour la phase 6 (propriétaire de la complétude).

#### 11. Récapitulatif : réutiliser / adapter / ne pas copier

| Élément du patron `tests/test_docs_wizard.py` | Lignes | Décision |
|-----------------------------------------------|--------|----------|
| Docstring de module : contrat + « Limite nommee » | `:1-19` | **réutiliser la forme** (contenu propre à la phase 5) |
| `from __future__ import annotations`, `ast`, `hashlib`, `re`, `pytest`, `Path` | `:26-35` | **réutiliser tels quels** |
| `RACINE_DEPOT = Path(__file__).resolve().parents[1]` + `PAGE` + `SOURCE_*` | `:44-53` | **réutiliser la forme** |
| Contrat de titres (`TITRE_*`, `TITRES_SECTION_ATTENDUS`, `section`) | `:55-83` | **réutiliser** si le plan veut figer l'ordre et le nombre des sections ; **à adapter** aux titres réellement écrits |
| Marqueurs de rendu (`MARQUEUR_CORPS`, `MARQUEUR_STATUT`, `LIGNE_CORPS`) | `:91-94` | **réutiliser tels quels** |
| Marqueurs JS/spécifiques au wizard (`MOTIF_EMPLACEMENT_RENDU`, `MOTIF_OPTION_RENDUE`, `TOUCHE_BARRE`, …) | `:95-181` | **NE PAS copier** |
| `COMMANDE_DESTRUCTRICE = re.compile(r"\bdb\s+clear\b")` | `:186` | **réutiliser tel quel** (même motif que `tests/test_docs_structure.py:20`) |
| `BASE_LOCALE`, `MOTIF_BASE_ABSENTE`, `MOTIF_EMPREINTE_CHANGEE` | `:193-195` | **réutiliser tels quels** |
| `CHEMIN_CITE`, `BOM_UTF8`, `FRAGMENT_H1`, `FRAGMENT_LIEN_EXTERNE`, `LIGNE_RETOUR` | `:207-211` | **réutiliser tels quels** |
| `BALISE_COMMANDE = "```console"` + son contrôle | `:212`, `:1822-1826` | **NE PAS copier tel quel** : la page 5 cite des commandes. Si le plan retient des blocs ```` ```text ````, la garde devient « aucun `db clear` dans un bloc d'exemple » via `lignes_exemple` |
| Constantes de motif de morsure (`MOTIF_*`) + la règle « jamais en clair dans l'assertion » | `:214-223`, `:2459-2471` | **réutiliser la règle**, créer ses propres constantes |
| Constantes de contenu du wizard (`MARQUEURS_DE_CONTENU`, `TEMOINS_LEGITIMES`) | `:244-306`, `:2482-2488` | **NE PAS copier** |
| `RACINES_INTERDITES`, `APPELS_SUPPRESSION`, `APPEL_PRODUIT` | `:311-323`, `:329-330` | **réutiliser tels quels** |
| `MODULE_BASE_INTERDIT` + son contrôle | `:325-326`, `:949-955` | **SUPPRIMER** (cf. § 6) |
| `_imports_du_module`, `_appels_du_module` | `:903-925` | **réutiliser tels quels** |
| `test_garde_de_cloture_du_harnais` | `:927-995` | **adapter** : garder les quatre constats, remplacer celui de `MODULE_BASE_INTERDIT` par les deux interdits de la phase (`data_dir` = défaut, paire `confirm`) |
| Contrôle de paire `data={"cmd": "GO"}` | `:968-988` | **adapter** à `data={"confirm": …}` |
| `_texte_page` | `:333-346` | **réutiliser tel quel** |
| `_lignes_du_corps`, `_entete`, `_statut` | `:348-375` | **réutiliser tels quels** (`_entete` utile pour le code d'écran `DB-02`/`SAV-01`) |
| `_sous_section` (lecture des `H3`) | `:387-407` | **réutiliser** si la page porte des sous-sections |
| `_empreinte` | `:826-833` | **réutiliser verbatim** (3ᵉ copie assumée) |
| Fonctions pures + constats + une seule assertion | `:674-702`, `:2414-2448` | **réutiliser la forme** |
| Morsure : témoin vert puis mutation d'une copie | `:2666-2720` | **réutiliser la forme** |
| `_faits_du_rendu` et détecteurs wizard | `:477-672` | **NE PAS copier** |
| Contrôle CRLF/BOM par octets | `:1833-1840` | **réutiliser tel quel** |
| Mesure d'empreinte de `.data/` + `pytest.skip` nommé | `:2283-2325` | **réutiliser la forme** |
| État « ROUGE jusqu'au plan suivant » | `:18-19`, `:2414-2425` | **NE PAS copier** : la phase 5 n'a aucun rouge attendu (tout est vert dès que la page et la réserve sont livrées ensemble) |

---

### `docs/sommaire.md` (index, transform)

**Analog :** lui-même (`docs/sommaire.md:15-22`) + les quatre gardes du § 3 ci-dessus. **Une seule ligne
ajoutée**, en fin de table d'index, **aucun autre énoncé modifié** (D-70) : ni la ligne 11
(`5. Base locale`) du « Parcours conseillé », ni l'ordre des lignes existantes, ni le tableau d'options.
Forme à copier, mesurée (`:22`) :

```markdown
| [Wizard avancé](wizard-avance.md) | Les 9 étapes du wizard, ses filtres, ses formats et ses touches |
```

→ `| [Base locale](base-locale.md) | <sujet de la page, une proposition comme les quatre autres> |`
**Le libellé `Base locale` est verrouillé par D-70** : il décide du `H1` de la page (égalité normalisée,
`tests/test_docs_structure.py:371-380`).

**Deux régressions à éviter (mesurées) :** créer la page sans la ligne fait rougir
`test_sommaire_lists_every_document` (`tests/test_docs_structure.py:134-137`, message `page non listee
dans docs/sommaire.md`) ; ajouter la ligne sans la page fait rougir le même contrôle sur
`cible listee absente sur disque`. **Les deux, dans le même commit.**

### `tests/test_docs_parcours.py` (test, transform) — la modification **obligatoire**

**Analog :** lui-même. La réserve et son commentaire, verbatim (`tests/test_docs_parcours.py:2323-2327`) :

```python
# Pages citees en prose par la section, sans lien : leurs pages n'existent pas encore (D-44). La
# reserve est reduite a ce qui est **reellement** inexistant (D-63) : `wizard-avance.md` est livree par
# la phase 4, donc son lien est desormais legitime, et `test_lien_wizard_avance_legitime` refuse qu'une
# page existante reste declaree inexistante.
PAGES_INEXISTANTES = ("base-locale.md",)
```

**Les trois lectures de cette constante (toutes itèrent dessus ; aucune ne l'exige non vide) :**

| # | Emplacement | Effet quand `base-locale.md` existe |
|---|-------------|--------------------------------------|
| 1 | `test_limites_ancrees_sur_le_code`, boucle `:2494-2500` (`if f"]({page_cible})" in texte`) | **ne rougit pas** : il ne rougit que si `docs/parcours-simplifie.md` **lie** `base-locale.md` ; le détail reste en prose |
| 2 | `test_page_complete_et_sans_derive`, boucle `:2627-2633` (même condition, `MOTIF_LIENS_INEXISTANTS` `:2537`) | **ne rougit pas** (même raison) |
| 3 | **`test_lien_wizard_avance_legitime`**, boucle `:2935-2943` — le seul contrôle qui **regarde le disque** | **ROUGE** dès que `docs/base-locale.md` existe |

Verbatim du seul contrôle qui mord (`tests/test_docs_parcours.py:2934-2943`) :

```python
    # 2. La reserve ne peut pas declarer inexistante une page qui existe.
    for page_cible in PAGES_INEXISTANTES:
        chemin_cible = docs_dir / page_cible
        if chemin_cible.is_file():
            constats.append(
                f"{MOTIF_PAGES_INEXISTANTES} : la reserve declare « {page_cible} » inexistante alors "
                f"que la page existe ({chemin_cible.as_posix()}) ; attendu une reserve reduite a ce qui "
                f"n'existe pas, l'entree devenue une vraie cible etant retiree dans le meme commit que "
                f"le lien (D-63)"
            )
```
avec `MOTIF_PAGES_INEXISTANTES = "page declaree inexistante alors qu'elle existe"` (`:2852`).

**Changement requis, précisément (patron posé par la phase 4 pour `wizard-avance.md`) :**

| Élément | État actuel | État requis | Pourquoi |
|---------|-------------|-------------|----------|
| `PAGES_INEXISTANTES` (`:2327`) | `("base-locale.md",)` | **`()`** — la réserve est **vidée** : plus aucune page de `docs/` n'est en dette | D-63 : la réserve ne contient que ce qui est **réellement** inexistant ; après cette phase, **plus aucune** page n'est en dette |
| Commentaire (`:2323-2326`) | dit que `base-locale.md` reste à la phase 5 | **réécrit** : la dette D-44 est entièrement levée (wizard en phase 4, base locale en phase 5) ; si la constante devient `()`, le commentaire doit dire **pourquoi** elle reste, et non disparaît | « un commentaire faux est pire qu'un commentaire absent » (leçon de la phase 4) |
| Les deux boucles `:2494` et `:2627` | itèrent sur la constante | **inchangées** : sur un tuple vide elles ne produisent rien | Les sites d'appel n'ont pas à bouger |
| `RENVOIS_SANS_LIEN = ("réglages avancés", "base locale")` (`:2314`) | présent, contrôlé **en présence** (`:2501-2506` et `:2971-2977`) | **inchangé** | Les deux tournures doivent **rester** dans la page : le contrôle ne teste que leur **présence normalisée**, jamais l'absence de lien. Un lien `[la base locale](base-locale.md)` **conserve les mots** et satisfait donc les deux |
| `LIENS_LEGITIMES_VERS_L_AIGUILLAGE` (`:2333`) | `("docs/wizard-avance.md", "docs/sommaire.md")` | **inchangé** (GUIDE_WIZARD.md n'est pas modifié par cette phase) | Aucune cible de l'aiguillage ne change |
| Un contrôle **symétrique** | absent pour la base locale | **à ajouter dans `tests/test_docs_base_locale.py`** : le renvoi `](base-locale.md)` **existe** là où la dette l'exigeait (patron `:2912-2932`, `ANCRES_RENVOI_D63` `:2863-2866`) | preuve que la levée de dette n'est pas une simple suppression de contrôle |

**Signe d'alerte mesuré à écrire dans le plan (Pitfall 1) :** `205 passed` **avant** la création de
`docs/base-locale.md`, et **rouge sur un seul test** (`test_lien_wizard_avance_legitime`, qui ne parle
pas de la base locale) **après** — d'où l'obligation de livrer la page et la réduction **dans le même
commit**. Si le plan choisit de convertir le renvoi en prose de `docs/parcours-simplifie.md:256` en lien
(recommandation de la recherche, Open Question 2), **aucun** contrôle ne s'y oppose : `RENVOIS_SANS_LIEN`
reste satisfait (les mots sont conservés) et `problemes_liens`
(`tests/test_docs_structure.py:39-89`) résoudra la cible dès que la page existe.

---

## Shared Patterns

### Constat localisant (D-13/D-83) — s'applique à **tout** le nouveau module

**Source :** `tests/test_docs_wizard.py:333-346`, `:2414-2448`, chaque `constats.append` ;
`tests/conftest.py:214-228` (`_section`, `page` **obligatoire**, sans défaut).

```python
    chemin = docs_dir / PAGE
    if not chemin.is_file():
        raise AssertionError(
            f"{PAGE} : page introuvable ({chemin}) ; attendu la page du wizard avance "
            f"decrite par {SOURCE_WIZARD}, livree dans docs/"
        )
```

Règle : `{page} : <constat> ; attendu <valeur attendue>, <producteur : fichier ou ligne de code>`.
Le producteur est **toujours** nommé. Une lecture impossible lève un `AssertionError` localisant, jamais
un `FileNotFoundError` brut.

### Comparaison normalisée (D-11) — s'applique aux libellés **rendus**

**Source :** `tests/conftest.py:119-124` (`_normalize`), exposé par la fixture `normalize` (`:133-136`).

```python
def _normalize(text: str) -> str:
    """Normalise un libellé pour comparaison (D-11) : entités HTML, accents, casse, espaces."""
    text = html.unescape(text)
    text = unicodedata.normalize("NFKD", text)
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    return re.sub(r"\s+", " ", text).strip().lower()
```

**À appliquer** aux libellés lus dans un **rendu** (l'apostrophe y arrive en `&#39;`, mesuré).
**À NE PAS appliquer** aux cinq libellés de l'état de la base comparés **surface par surface** : c'est
justement `Entrées :` (CLI, `dofus_stuff/cli.py:224`) contre `ENTREES :` (web,
`dofus_stuff/web/routes.py:764`), `Dernier check : il y a …h` contre `DERNIER CHECK : IL Y A …H`, et
`(aucun)` contre `(AUCUN)` (`cli.py:221-223` / `routes.py:761-763`) — la normalisation **masquerait** ces
écarts et la page deviendrait fausse sur une surface (Pitfall 4).

### Helpers partagés, jamais dupliqués (D-12) — s'applique aux deux fichiers de test

**Source :** `tests/conftest.py` — signatures réelles relevées cette session :

| Fixture / helper | Signature | Portée | Ce qu'elle fournit |
|------------------|-----------|--------|--------------------|
| `catalog` | `catalog()` → `Catalog` | function | `Catalog(version="9.9.9.9", items=_sample_items())` (`:78-80`) ; `_sample_items` (`:18-75`) pose 3 équipements, 1 ressource, 1 panoplie |
| `app` | `app(catalog, tmp_path)` → Flask | function | `data_dir = tmp_path/"data"` ; `Database(data_dir).open()`, `set_meta("game_version","9.9.9.9")`, `replace_kind("equipment", …)`, `replace_kind("resources", …)`, `db.close()` (`:84-100`) ; puis `create_app(data_dir=data_dir, offline=True, catalog=catalog, load_catalog=False)` (`:102-107`), `TESTING = True`, `extensions["web_config"]["data_dir"] = data_dir` (`:108-109`) ; `yield` puis `catalog.close()` (`:110-111`) |
| `client` | `client(app)` → test client | function | `app.test_client()` (`:114-116`) — en processus, aucun port, aucun socket |
| `docs_dir` | `docs_dir()` → `Path` | **session** | `Path(__file__).resolve().parents[1] / "docs"` (`:127-130`), indépendant du répertoire courant |
| `normalize` | `normalize` → `_normalize(text)` | **session** | expose **le helper**, pas une valeur (`:133-136`) |
| `section` | `section(texte, titre, page)` → `str` | **session** | corps d'une section `H2` ; `page` **obligatoire** (D-13) ; lève `AssertionError` si le titre manque (`:214-228`) |
| `sections` | `sections(texte)` → `list[tuple[str \| None, str]]` | **session** | l'en-tête avant le premier `##` est la première section, titre `None` (`:198-211`) |
| `lignes_de_code` | `lignes_de_code(texte)` → `list[str]` | **session** | lignes de **tous** les blocs, toutes balises (`:176-178`) |
| `lignes_exemple` | `lignes_exemple(texte)` → `list[str]` | **session** | lignes des **seuls** blocs ```` ```console ````, bords rognés, lignes vides écartées (`:181-195`, `BALISE_EXEMPLE = "console"` `:151`) |

**Règle `tmp_path` (D-81) :** la fixture `app` construit sa base sous `tmp_path/data`
(`tests/conftest.py:85-86`) ; **aucun** contrôle ne passe `DEFAULT_DATA_DIR` à `Database`. Attention
mesurée : `create_app` **ne suffit pas** à rediriger la base — la fixture réécrit explicitement
`app.extensions["web_config"]["data_dir"]` (`:109`), et les écrans `db` lisent
`current_app.config["DATA_DIR"]` (`dofus_stuff/web/routes.py:746`). Un contrôle qui construit son propre
`Database` doit garder une **référence à `tmp_path`**, jamais au répertoire du dépôt.

### Ancrage par API publique uniquement (D-14) — s'applique à toutes les attentes

**Autorisé :** constantes publiques (`DB_NAME`, `DEFAULT_DATA_DIR`, `META_GAME_VERSION`,
`META_LAST_CHECKED_AT`, `ITEM_KINDS`, `CHECK_INTERVAL_SECONDS`), **rendu** des écrans par le client de
test, **aide et défauts des parseurs publics** `build_parser()`, **sortie capturée** de
`_print_db_status`.
**Interdit :** l'introspection privée d'`argparse` (`_actions`, `parser._subparsers`), les variables
locales, `inspect`. Les **cinq libellés de l'état de la base** ne sont **aucune** constante publique
(littéraux `dofus_stuff/cli.py:216-229` et `dofus_stuff/web/routes.py:755-769`) : leur ancrage est le
**rendu** (web) et la **sortie capturée** (CLI), avec repli `ast` là où l'exécution est interdite (D-76).

### Interdits d'exécution et de données (D-15/D-81/D-89) — s'applique à la garde de clôture ET aux tests

Aucun `main()`, aucun `subprocess`, aucun `sqlite3` importé par le harnais, aucune socket, aucun
`webbrowser`, aucune suppression de fichier ; aucun `db clear` (ni le `POST /db/clear` de confirmation),
aucun `POST /db/sync` avec confirmation, aucune écriture sous `.data/`, aucune synchronisation, **aucune
modification de `dofus_stuff/**`** (D-88). Les seules opérations admises sur `.data/` sont la **lecture
d'octets** pour l'empreinte et sa comparaison à elle-même.

### L'idiome `PAGES_INEXISTANTES`, à réduire dans le même commit que sa cible (D-63)

**Source :** `tests/test_docs_parcours.py:2323-2327` et `:2934-2943`. Voir le détail au § « la
modification obligatoire » ci-dessus. Cette phase **vide** la réserve : c'est le dernier usager de la
dette D-44.

### Commits locaux, indexation par chemin explicite (D-91) — s'applique à la phase entière

`git add <chemin>` pour chaque fichier touché, **jamais** `git add .`, jamais `doc-agent.toml`,
`.doc-agent/`, `gsd-auto*.toml` ni `.planning/state.json`. Aucun push, aucun déploiement, aucune
dépendance ajoutée (`pyproject.toml` inchangé).

---

## Guard-vs-existing coverage — ce qui est **déjà** prouvé, et ce que la phase doit ajouter

**Déjà couvert par une garde existante : NE PAS re-prouver, et ne jamais contourner** (D-90) :

| Besoin de la phase | Garde qui le porte déjà | Lignes mesurées |
|--------------------|-------------------------|-----------------|
| Résolution des liens internes de la nouvelle page | `problemes_liens` (`tests/test_docs_structure.py`) + `test_all_relative_links_resolve` | `:39-89`, wrapper `:151-154` |
| Rejet des ancres, chemins absolus, antislashs, `file://`, cibles hors racine | `problemes_liens` (mêmes lignes) + `test_no_anchor_or_absolute_links` | `:47-89`, wrapper `:157-187` |
| Exhaustivité **bidirectionnelle** de l'index | `problemes_index` + `test_sommaire_lists_every_document` | `:92-119`, wrapper `:134-137` |
| Unicité du libellé d'index et non-auto-listing du sommaire | `test_sommaire_index_labels_are_unique` | `:468-492` |
| `H1` **unique** égal au libellé d'index (normalisé) | `problemes_h1` + `test_h1_matches_sommaire_entry` | `:337-380`, wrapper `:450-453` |
| Ligne de retour vers le sommaire | `problemes_retour_sommaire` + `test_pages_have_back_link` | `:383-417`, wrapper `:456-459` |
| Décodage UTF-8 strict, absence de jeton de brouillon, longueur ≥ 300 | `problemes_encodage` + `test_documents_are_utf8_and_not_drafts`, constantes `JETONS_BROUILLON`/`LONGUEUR_MINIMALE` | `:418-447`, wrapper `:462-465`, constantes `:312-315` |
| Le **seul** renvoi du `README.md` vers le sommaire (exactement 1) | `test_readme_links_to_sommaire` | `:190-213` |
| `db clear` et `PURGE` **absents de `docs/installation.md`** (garde de portée **locale** à cette page) | `test_no_destructive_command_in_installation`, avec `COMMANDE_DESTRUCTRICE` et `JETON_PURGE` | `:277-305`, constantes `:20-21` |
| Dérive injectée dans une **copie** de `docs/` détectée par les trois `problemes_*`, arbre livré intact | `test_mutation_detecte_les_trois_derives` (+ `_nom_page_injectee`) | `:533-603`, `:517-530` |
| Normalisation D-11 (accents, casse, entités HTML, espaces, CRLF→LF) | `test_normalisation_insensible_aux_accents_et_casse` | `:495-514` |
| Le parseur traite `cache <x>` et `db <x>` de façon équivalente | `tests/test_docs_cli.py` | `:676-706` |
| Les écrans `db` fonctionnent (menu, annulation de sync, clear, `SAV-01`) — **couverture fonctionnelle, pas documentaire** | `tests/test_web.py` | `:361-370`, `:372-376`, `:378-388`, `:411-418`, `:107-113` |

**Ce que la phase 5 doit ajouter malgré tout** (et que rien ci-dessus ne couvre) :
les **sept contrôles de valeur** de la table `Phase Requirements → Test Map` de `05-RESEARCH.md`
(fichier + catégories, fenêtre 24 h, deux défauts hors-ligne, champs CLI, champs web, création du fichier
par `db status`, refus de `db sync --offline`, contact API de l'écran web, commandes destructrices sur la
même ligne), **la garde `ast` réécrite** (§ 6), **la mesure d'empreinte locale** (§ 9), **le contrôle des
renvois du `README.md`** (§ 10) et **la réduction de `PAGES_INEXISTANTES`** (modification obligatoire
d'un fichier existant).

**Deux gardes de portée à écrire dans le plan, sous peine de faux rouge ou de faux vert :**
1. `test_no_destructive_command_in_installation` (`tests/test_docs_structure.py:277-305`) ne couvre
   **que** `docs/installation.md` : « améliorer » cette page pour y parler des commandes destructrices
   casserait la suite (« jeton `PURGE` trouvé »). La nouvelle page est le bon endroit, et la garde ne la
   couvre pas (Pitfall 9).
2. Le critère 4 (« aucun parcours ne présente une commande destructrice ») doit être **délimité au
   périmètre de la phase** : `README.md:80` porte bien `db clear` sans avertissement, et D-87 ne mandate
   pas sa réécriture (Pitfall 8, A3 de la recherche).

## No Analog Found

| Fichier | Rôle | Data Flow | Raison |
|---------|------|-----------|--------|
| *(aucun)* | — | — | Les 4 fichiers de la phase ont un analogue **exact** ou de rôle équivalent, mesuré cette session. Le seul élément **sans précédent** est un *contrôle*, pas un fichier : la vérification que **chaque renvoi interne du `README.md` résout** (§ 10). Le plus proche existant est `test_readme_links_to_sommaire` (`tests/test_docs_structure.py:190-213`, **un seul** lien) et la lecture généralisée `MOTIF_LIEN_MARKDOWN` de `tests/test_docs_wizard.py:2475`, `:2606-2614` : il y a donc bien un analog de **forme**, mais aucune garde de racine généralisée n'existe — c'est ce que le plan doit écrire, à placer dans `tests/test_docs_base_locale.py` (Open Question 4 de la recherche) |

**Chemins dont l'existence et le suivi git ont été vérifiés** (aucun chemin de miroir gitignoré n'est
cité dans ce document) : `docs/base-locale.md` (**absent — à créer**), `docs/sommaire.md`,
`docs/cli.md`, `docs/installation.md`, `docs/parcours-simplifie.md`, `docs/wizard-avance.md`,
`README.md`, `GUIDE_WIZARD.md`, `tests/conftest.py`, `tests/test_docs_wizard.py`,
`tests/test_docs_structure.py`, `tests/test_docs_parcours.py`, `tests/test_docs_cli.py`,
`tests/test_docs_code_anchor.py`, `tests/test_web.py`,
`tests/fixtures/guide-wizard-obsolete.md`, `dofus_stuff/database.py`, `dofus_stuff/sync.py`,
`dofus_stuff/api.py`, `dofus_stuff/cli.py`, `dofus_stuff/web/__main__.py`,
`dofus_stuff/web/routes.py`, `dofus_stuff/web/static/js/terminal.js`,
`dofus_stuff/web/templates/screen.html`, `dofus_stuff/catalog.py` — tous listés par `git ls-files`
(non vides), sauf `docs/base-locale.md` qui n'existe pas encore.

## Metadata

**Analog search scope :** `docs/**` (5 pages), la racine (`README.md`, `GUIDE_WIZARD.md`),
`tests/**` (13 modules + `conftest.py` + `fixtures/`), et `dofus_stuff/**` en **lecture seule** pour
confirmer les valeurs que la page doit citer (`database.py`, `sync.py`, `api.py`, `cli.py`,
`web/__main__.py`, `web/routes.py`, `web/static/js/terminal.js`, `web/templates/screen.html`).
**Files scanned :** 9 fichiers lus intégralement ou par plages non recouvrantes
(`docs/sommaire.md`, `docs/wizard-avance.md`, `docs/cli.md`, `docs/installation.md`,
`docs/parcours-simplifie.md`, `tests/conftest.py`, `tests/test_docs_wizard.py`,
`tests/test_docs_structure.py`, `tests/test_docs_parcours.py`) + une douzaine de relevés ciblés
(`grep -n` / `awk` par plages) sur le code produit et `tests/test_web.py`.
**Mesures de cette session, reproductibles :**
`./.venv/Scripts/python.exe -m pytest -q` → **`205 passed in 3.58s`** ;
`… -m pytest -q tests/test_docs_wizard.py` → **`18 passed in 0.60s`** ;
imports des constantes publiques (`DB_NAME='dofus.sqlite3'`, `CHECK_INTERVAL_SECONDS=86400`,
`ITEM_KINDS` 7 éléments, égalité avec les kinds de `SYNC_SOURCES` → `True`) ;
défauts des parseurs (CLI `offline=False`, web `offline=True`) ;
`Database()` → `TypeError: … missing 1 required positional argument: 'data_dir'` ;
`_print_db_status` sur un répertoire **inexistant** (dossier et fichier créés, sortie capturée) ;
**cinq `GET`** (`/db`, `/db/status`, `/db/sync`, `/db/clear`, `/saves`) sur une base `tmp_path` peuplée ;
encodage/lignes/BOM de 20 fichiers ; empreinte de `.data/dofus.sqlite3` **avant et après la suite
entière** — identique (`24989696` / `1788730056843137500` /
`e3793d64cb7939ad1a51837b075b6b95e03d64c878fcb9cc07f86c00bb8fef7b`).
**Ce qui n'a PAS été fait, et n'est pas revendiqué :** aucune exécution de `main()`, aucun
`POST /db/sync` ni `POST /db/clear` (même avec une confirmation non validante), aucune synchronisation,
aucun appel réseau, aucune ouverture SQLite du chemin `.data/dofus.sqlite3` (seule la **lecture d'octets**
pour l'empreinte), aucune écriture sous `.data/`, aucun `db clear`, aucune suppression.
**Pattern extraction date :** 2026-09-11.





