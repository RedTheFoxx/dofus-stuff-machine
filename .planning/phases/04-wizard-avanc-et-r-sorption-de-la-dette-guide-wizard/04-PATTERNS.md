# Phase 4: Wizard avancé et résorption de la dette `GUIDE_WIZARD` - Pattern Map

**Mapped:** 2026-09-11
**Files analyzed:** 8 (3 créés, 5 modifiés)
**Analogs found:** 6 / 8 (2 sans analogue réel : voir « No Analog Found »)
**Méthode :** tous les extraits ci-dessous sont **cités du fichier réel**, lus cette session avec
`Read`/`sed` sur C:/Users/Red/Documents/Projets/dofus-stuff-machine. Les numéros de ligne sont ceux
du dépôt à cette date (`git ls-files` vérifié pour chaque analogue : aucun chemin d'un miroir
gitignoré n'est cité).

## File Classification

| New/Modified File | Role | Data Flow | Closest Analog | Match Quality |
|-------------------|------|-----------|----------------|---------------|
| `docs/wizard-avance.md` (créé par cette phase) | page de documentation (`docs/`) | transform (texte rédigé depuis un rendu mesuré) | `docs/parcours-simplifie.md` | exact (même gabarit D-01, même méthode D-32/D-36) |
| `docs/wizard-avance.md` — variante de section | page de documentation | transform | `docs/cli.md` | role-match (page d'un autre thème, même gabarit, plus courte) |
| `tests/test_docs_wizard.py` (créé par cette phase) | test / module d'ancrage | request-response (client de test Flask **+** lecture disque) | `tests/test_docs_parcours.py` | exact |
| `tests/test_docs_wizard.py` — détecteur | fonction pure de test | transform (`texte` → `list[str]`) | `tests/test_docs_structure.py::problemes_*` | exact (même signature et même contrat de sortie) |
| `tests/fixtures/guide-wizard-obsolete.md` (créé par cette phase) | fixture de test (donnée) | file-I/O | *(aucun)* — voir « No Analog Found » | none |
| `GUIDE_WIZARD.md` (modifié) | aiguillage racine (config/navigation) | transform | `docs/sommaire.md` | role-match partiel (seule page racine/`docs` purement navigante du dépôt) |
| `docs/sommaire.md` (modifié) | index / config | transform (une ligne ajoutée) | lui-même (`test_docs_structure.py` le garde) | exact |
| `README.md` (modifié) | config (readme produit) | transform (une ligne supprimée) | lui-même (`test_readme_links_to_sommaire`) | exact |
| `docs/parcours-simplifie.md` (modifié) | page de documentation | transform (2 renvois en prose → liens) | lui-même, lien `](cli.md)` de la ligne 5 | exact |
| `tests/test_docs_parcours.py` (modifié) | test / module d'ancrage | request-response | lui-même (`PAGES_INEXISTANTES`) | exact |

**Chemins de code (source de vérité, non modifiés par cette phase, D-66)** : `dofus_stuff/web/optimize_wizard.py`,
`dofus_stuff/web/routes.py`, `dofus_stuff/model/solver_spec.py`, `dofus_stuff/web/screens.py`,
`dofus_stuff/web/templates/screen.html` — tous **git-tracked** (vérifié).

**Encodage/lignes de fin — mesuré, à respecter par tout fichier produit** :

| Fichier | Octets | CRLF | BOM |
|---------|--------|------|-----|
| `docs/sommaire.md` | 596 | 21/21 | non (`23 20 53` = `# S`) |
| `docs/parcours-simplifie.md` | 20015 | 269/269 | non |
| `docs/cli.md` | 9381 | 195/195 | non |
| `docs/installation.md` | 7380 | 141/141 | non |
| `GUIDE_WIZARD.md` | 13118 | 330/330 | non |
| `README.md` | 5292 | 125/125 | non |
| `tests/*.py` | — | CRLF | non |

→ La nouvelle page, l'aiguillage réduit, la ligne d'index et la fixture s'écrivent en **UTF-8 sans BOM,
fin de ligne CRLF**. `tests/test_docs_parcours.py:2533-2547` sanctionne déjà le BOM et les LF sur
`parcours-simplifie.md` (`if octets.startswith(BOM_UTF8)` puis `if fins != crlf`) ; c'est la
convention de tout `docs/`.

## Pattern Assignments

### `docs/wizard-avance.md` (page de documentation, transform)

**Analog principal :** `docs/parcours-simplifie.md` (269 lignes, phase 3) — la seule page du dépôt
construite exactement comme celle demandée : ancrage au rendu, tableaux d'entrées, bloc « Source de
vérité », ligne de retour.
**Analog secondaire :** `docs/cli.md` (195 lignes, phase 2) — même gabarit, page plus courte, utile
pour la concision du bloc source.

#### Gabarit : en-tête (parcours-simplifie.md, lignes 1-5)

```markdown
# Parcours simplifié

Cette page suit le parcours simplifié de l'interface web, question par question : la classe, les éléments, puis le niveau. Pour chacune, elle recopie l'écran tel qu'il s'affiche et dit ce que la saisie accepte.

Toutes les affirmations de cette page viennent du rendu réel de la vue web. La surface des commandes n'est pas recopiée ici : elle appartient à [la page CLI](cli.md). Les écrans du wizard avancé et le fonctionnement de la base locale seront décrits dans les pages qui leur seront consacrées. Le parcours en ligne de commande, lui, ne pose pas ces trois questions : la classe et les éléments n'existent que dans le parcours guidé de l'interface web.
```

Comparaison `docs/cli.md` lignes 1-5 (même forme : `H1` nu, phrase d'introduction, portée) :

```markdown
# CLI

Cette page décrit la ligne de commande de dofus-stuff-machine : les sous-commandes de `fetcher.py`, les options qu'elles acceptent, les valeurs par défaut relevées dans le parseur et un exemple analysable par commande.

Le point d'entrée est `fetcher.py`, à la racine du dépôt : les commandes de cette page s'écrivent depuis cette racine. Le parseur de la ligne de commande ne connaît que les options déclarées dans `dofus_stuff/cli.py` : cette page n'en présente donc aucune qui ne soit définie dans le produit.
```

**Contrainte de H1 (D-56 + `problemes_h1`, `tests/test_docs_structure.py:337-380`)** : le `H1` doit
être **unique** et **égal au libellé d'index du sommaire après normalisation** (D-11). Si la ligne
d'index s'écrit `| [Wizard avancé](wizard-avance.md) | … |`, alors `docs/wizard-avance.md` commence
**exactement** par `# Wizard avancé` (pas d'apostrophe, pas de précision entre parenthèses : le
message d'échec « H1 « Wizard avancé (avancé) » différent du libellé d'index » est explicitement
anticipé par la recherche, Pitfall 4).

#### Bloc « Source de vérité » — verbatim (parcours-simplifie.md, lignes 258-266)

```markdown
## Source de vérité

- `dofus_stuff/web/routes.py` : écrans et libellés des trois questions.
- `dofus_stuff/optimize/recommend.py` : liste des classes, paliers PA/PM et heuristiques de classe.
- `dofus_stuff/optimize/api.py` : lignes du résultat et emplacements affichés.
- `dofus_stuff/model/solver_spec.py` : capital de points par niveau.
- `dofus_stuff/optimize/score.py` : « indice de recherche ».
- `dofus_stuff/optimize/candidates.py` : sélection du catalogue.
- `dofus_stuff/web/static/js/terminal.js` : sauvegardes du navigateur.
- `dofus_stuff/web/dofusbook_export.py` : export Dofusbook.
```

Comparaison `docs/cli.md` lignes 188-194 (phrases plus longues, un chemin par ligne, même forme) :

```markdown
## Source de vérité

- `fetcher.py` : point d'entrée de la ligne de commande.
- `dofus_stuff/cli.py` : parseur et commandes réellement disponibles ; la fonction `build_parser()` y déclare la surface documentée ici.
- `dofus_stuff/database.py` : suppression effective des tables par `db clear`, la commande destructrice qui vide la base locale.
- `dofus_stuff/optimize/profile_input.py` : choix du mode interactif de l'optimisation.
```

**Ce que le contrôle exigera de ce bloc (D-03/D-56)** — `problemes` de
`tests/test_docs_parcours.py::test_source_de_verite_et_chemins_cites` (lignes 1187-1219) : chaque
chemin **entre accents graves** du fichier doit exister sur disque depuis la racine du dépôt, et le
contrôle échoue si le bloc n'en cite aucun :

```python
    manquants = [
        chemin
        for chemin in sorted(set(CHEMIN_CITE.findall(texte)))
        if not (RACINE_DEPOT / chemin).exists()
    ]
    for chemin in manquants:
        constats.append(
            f"le chemin « {chemin} » cite entre accents graves n'existe pas depuis la racine du "
            f"depot ; attendu un chemin reel, jamais un chemin invente"
        )
```

→ Pour `docs/wizard-avance.md`, les chemins candidats **vérifiés présents** sont
`dofus_stuff/web/optimize_wizard.py`, `dofus_stuff/web/routes.py`,
`dofus_stuff/model/solver_spec.py`, `dofus_stuff/web/screens.py`,
`dofus_stuff/web/templates/screen.html`. Ne citer **aucun** chemin inventé, et **aucune** constante
privée (D-14).

#### Ligne de retour — verbatim, dernière ligne non vide (3 pages sur 3)

```markdown
[Retour au sommaire](sommaire.md)
```

Mesuré : `docs/cli.md:195`, `docs/installation.md:141`, `docs/parcours-simplifie.md:269` — la
convention est unanime, et `problemes_retour_sommaire`
(`tests/test_docs_structure.py:383-415`) n'exige qu'**au moins un** lien dont la cible résolue est
`docs/sommaire.md`, mais `test_page_complete_et_sans_derive` de la phase 3 exige que ce soit la
**dernière ligne non vide**. Suivre la convention mesurée, pas le minimum.

#### Titres de niveau 2 et sous-sections de niveau 3

Le gabarit existant enchaîne `## Section` (niveau 2) et `### Sous-section` (niveau 3 :
« Entrées acceptées », « Erreurs et refus » sous chaque `## Question n/3`). Le helper partagé
`section` ne connaît que les `H2` : la page peut donc regrouper les 9 étapes en sous-sections sans
casser les contrôles, à condition que les titres de niveau 2 restent stables et que le test lise les
`H3` par un helper **local** (voir `_sous_section` plus bas) — jamais en le promouvant dans
`tests/conftest.py` (D-12 : le partagé ne se duplique pas, mais ne s'étend pas non plus sans raison).

---

### `tests/test_docs_wizard.py` (test d'ancrage, request-response + transform)

**Analog :** `tests/test_docs_parcours.py` (2734 lignes, 17 tests, phase 3) — **le** patron à copier.
Les huit extraits ci-dessous couvrent tout ce dont le nouveau module a besoin ; le plan peut dire
« suivre cette forme » sans re-dériver quoi que ce soit.

#### 1. En-tête et imports — verbatim (lignes 1-11 et 36-51)

````python
"""Ancrage de la page `docs/parcours-simplifie.md` sur le rendu reel du parcours simplifie.

Le contrat va du rendu vers la page : les trois ecrans du parcours simplifie sont rendus par le
client de test Flask, en processus, sur la fixture `app` de `tests/conftest.py` (D-32), puis les
libelles lus dans les lignes du corps et dans la ligne de statut sont compares a ceux que la page
cite. Chaque entree citee par la page est rejouee sur le rendu et classee par ce que l'outil fait
reellement : une entree acceptee redirige ou atteint l'appel d'optimisation, une entree refusee
re-rend le meme ecran avec le message attendu au debut de la ligne de statut. Aucun serveur n'est
lance, aucun socket n'est ouvert, le programme du produit n'est jamais execute et rien n'est ecrit
sous `.data/` : la fixture `app` construit sa propre base dans un dossier temporaire.
````

```python
from __future__ import annotations

import ast
import base64
import hashlib
import importlib
import re
from pathlib import Path
from unittest.mock import patch

import msgpack
import pytest

from dofus_stuff.model.solver_spec import capital_spent, total_capital_for_level
from dofus_stuff.optimize.recommend import CLASSES, ELEMENTS, recommendation_spec
from dofus_stuff.web.dofusbook_export import build_dofusbook_url

RACINE_DEPOT = Path(__file__).resolve().parents[1]
PAGE = "parcours-simplifie.md"
SOMMAIRE = "sommaire.md"
SOURCE_ROUTES = "dofus_stuff/web/routes.py"
SOURCE_RECOMMEND = "dofus_stuff/optimize/recommend.py"
SOURCE_API = "dofus_stuff/optimize/api.py"
SOURCE_JS = "dofus_stuff/web/static/js/terminal.js"
SOURCE_SCREENS = "dofus_stuff/web/screens.py"
SOURCE_DOFUSBOOK = "dofus_stuff/web/dofusbook_export.py"
SOURCE_SPEC = "dofus_stuff/model/solver_spec.py"
SOURCE_SCORE = "dofus_stuff/optimize/score.py"
SOURCE_CANDIDATES = "dofus_stuff/optimize/candidates.py"
```

→ Transposition pour la phase 4 : `PAGE = "wizard-avance.md"`, `RACINE_DEPOT` conservé,
et des `SOURCE_*` pour `dofus_stuff/web/optimize_wizard.py`, `dofus_stuff/web/routes.py`,
`dofus_stuff/model/solver_spec.py`. **Aucun import de `msgpack`, `base64` ou `hashlib`** n'est
justifié ici ; `ast` et `pytest` le sont (garde de clôture, `pytest.skip` de la mesure d'empreinte).
Les constantes publiques à importer pour ancrer les attentes (D-13/D-42) sont
`WIZARD_STEPS`, `STEP_TITLES`, `TYPE_FILTER_LABELS` (`dofus_stuff/web/optimize_wizard.py`) et
`TYPE_FILTER_KEYS` (`dofus_stuff/model/solver_spec.py`), vérifiées présentes cette session :

```python
WIZARD_STEPS: tuple[str, ...] = (
    "slots",
    "options",
    "caracs",
    "papmpo",
    "resistances",
    "damages",
    "misc",
    "items",
    "recap",
)

STEP_TITLES: dict[str, str] = {
    "slots": "SLOTS ET FILTRES",
    "options": "OPTIONS SOLVEUR",
    "caracs": "CARACTERISTIQUES",
    "papmpo": "PA / PM / PO",
    "resistances": "RESISTANCES",
    "damages": "DOMMAGES",
    "misc": "DIVERS",
    "items": "ITEMS INTERDITS / FORCES",
    "recap": "RECAPITULATIF",
}
```
*(`dofus_stuff/web/optimize_wizard.py:23-45`, verbatim)*

```python
TYPE_FILTER_LABELS: dict[str, str] = {
    "familier": "FAMILIER",
    "montilier": "MONTILIER",
    "dragodinde": "DRAGODINDE",
    "muldo": "MULDO",
    "volkorne": "VOLKORNE",
    "arme_distance": "ARMES DISTANCE",
    "arme_melee": "ARMES MELEE",
    "dofus": "DOFUS",
    "trophee": "TROPHEE",
    "prysmaradite": "PRYSMARADITE",
}
```
*(`dofus_stuff/web/optimize_wizard.py:111-121`, verbatim)*

```python
# Filtres de types d'équipement (True = autorisé).
TYPE_FILTER_KEYS: tuple[str, ...] = (
    "familier",
    "montilier",
    "dragodinde",
    "muldo",
    "volkorne",
    "arme_distance",
    "arme_melee",
    "dofus",
    "trophee",
    "prysmaradite",
)
```
*(`dofus_stuff/model/solver_spec.py:42-53`, verbatim)*

**Seconde source du couple `F6`/`F7` (D-53), mesurée** : `TYPE_FILTER_KEYS[5] == "arme_distance"` et
`TYPE_FILTER_KEYS[6] == "arme_melee"` → `F6` = `ARMES DISTANCE`, `F7` = `ARMES MELEE`. Le rendu le
confirme (page 2 de `/optimize/wizard/slots`).

#### 2. Marqueurs du rendu — verbatim (lignes 100-106)

```python
MARQUEUR_CORPS = 'id="body">'
MARQUEUR_STATUT = '<div class="row status'
LIGNE_CORPS = re.compile(r'<div class="row">(.*?)</div>', re.S)
LIBELLE_SAISIE = re.compile(r'<label class="input-label meta">(.*?)</label>', re.S)
TOUCHE_BARRE = re.compile(
    r'<span class="fkey-key meta">([^<]*)</span>'
    r'<span class="fkey-eq meta">=</span>'
    r'<span class="fkey-label">([^<]*)</span>'
)
```

Ces quatre marqueurs viennent de `dofus_stuff/web/templates/screen.html` et sont **les mêmes** pour
toutes les vues du produit, wizard compris : le nouveau module les recopie à l'identique (« identique »
au sens de la forme — c'est un patron local de lecture du rendu, pas un helper partagé de
`conftest.py` ; la phase 3 l'a posé ainsi, le plan peut décider de le reprendre tel quel).

#### 3. Lecteurs du rendu — verbatim (lignes 267-306)

```python
def _texte_page(docs_dir: Path) -> str:
    """Texte de la page, lu en UTF-8 explicite ; page absente = AssertionError localisante (D-13).

    Jamais de `FileNotFoundError` brut (lecon IN-03) : l'echec nomme la page, le chemin attendu et
    le fichier de code dont elle decrit la surface. Toute lecture de la page passe par ici.
    """
    chemin = docs_dir / PAGE
    if not chemin.is_file():
        raise AssertionError(
            f"{PAGE} : page introuvable ({chemin}) ; attendu la page du parcours simplifie "
            f"decrite par {SOURCE_ROUTES}, livree dans docs/"
        )
    return chemin.read_text(encoding="utf-8")


def _lignes_du_corps(reponse) -> list[str]:
    """Lignes visibles du corps de l'ecran, jamais la reponse entiere.

    La charge utile `data-stuff-payload` porte tout le resultat sur chaque page et `tojson` y
    echappe les accents : une assertion sur la reponse entiere serait fausse sur une page correcte.
    """
    texte = reponse.get_data(as_text=True)
    corps = texte.split(MARQUEUR_CORPS, 1)[1].split(MARQUEUR_STATUT, 1)[0]
    return [ligne.rstrip() for ligne in LIGNE_CORPS.findall(corps)]


def _statut(reponse) -> str:
    """Texte de la ligne de statut : la seule source des messages de refus."""
    texte = reponse.get_data(as_text=True)
    return texte.split(MARQUEUR_STATUT, 1)[1].split(">", 1)[1].split("</div>", 1)[0]


def _touches(reponse) -> list[tuple[str, str]]:
    """Couples touche <-> libelle de la barre de raccourcis, tels qu'ils sont rendus.

    Chaque touche est un `span` distinct : la chaine `ESC=Retour` n'existe nulle part dans le HTML
    rendu, c'est donc le couple extrait qui est exige, jamais la concatenation.
    """
    return TOUCHE_BARRE.findall(reponse.get_data(as_text=True))
```

**Règle héritée à ne pas réinventer (anti-pattern de la recherche)** : ne jamais asserter la
concaténation `ON=Retour` — elle n'existe pas dans le HTML ; exiger le **couple** extrait du `span`.

#### 4. Client de test par étape — verbatim (lignes 342-354)

```python
def _client_etape(app, etape: str):
    """Client de test neuf dont la session porte l'etat minimal de l'etape.

    L'etat est ecrit sous la cle lue par la vue (`session.get("recommendation_input")`,
    `dofus_stuff/web/routes.py:940`). Un client neuf est indispensable : un POST accepte reecrit
    l'etat de session et fausserait le verdict suivant. `client.session_transaction()` est l'API de
    test publique de Flask, deja employee par `tests/test_web.py`.
    """
    client = app.test_client()
    with client.session_transaction() as session:
        session["recommendation_input"] = dict(ETATS_ETAPE[etape])
    return client
```

**Mesure de la recherche, à exploiter par le plan** : les 9 écrans du wizard répondent **200 sur un
client neuf** (`load_wizard_spec` retombe sur `default_player_spec(level=200)`) → le module n'a
**pas besoin** de rejouer classe → éléments → niveau pour rendre un écran ; `_client_etape` n'est
nécessaire que pour prouver le **chemin d'arrivée** (`POST /optimize/quick/niveau cmd=AVANCE`).

#### 5. Constats accumulés en une seule assertion — verbatim (lignes 419-474, extrait)

```python
    # Les constats sont accumules et joints a *une seule* assertion : une assertion par constat
    # rendrait un motif inatteignable des que la premiere leverait avant les suivants.
    constats: list[str] = []
    for titre, question, reponse, couples_attendus in ecrans:
        normalise = normalize(question)
        if reponse.status_code != 200:
            constats.append(
                f"l'ecran « {titre} » repond {reponse.status_code} au lieu de 200 ; attendu le "
                f"rendu du corps par {SOURCE_ROUTES}"
            )
            continue
        lignes = [normalize(ligne) for ligne in _lignes_du_corps(reponse)]
        if normalise not in lignes:
            constats.append(
                f"{PAGE} : le libelle « {question} » n'est pas rendu dans les lignes du corps de "
                f"l'ecran « {titre} » ; attendu ce libelle, produit par {SOURCE_ROUTES}"
            )
        ...
    assert not constats, (
        f"{PAGE} : constats sur les trois questions du parcours simplifie : "
        + " ; ".join(constats)
        + f" ; attendu les trois questions et « {avance} » rendus par {SOURCE_ROUTES} et cites "
        f"par la section correspondante de la page"
    )
```

**Style de message de réussite/d'échec (D-13), à reproduire mot pour mot dans sa forme** :
`{page} : <ce qui est faux> ; attendu <valeur attendue>, <producteur : fichier de code ou ligne>`.
Le producteur est **toujours** nommé (`SOURCE_ROUTES`, `optimize_wizard.py:424`, …).

#### 6. Parcours multi-étapes rendu en une seule séquence — verbatim (lignes 398-410)

```python
def test_trois_questions_et_avance_rendus(docs_dir: Path, app, normalize, section) -> None:
    """Les trois questions et `AVANCE` sont rendues telles quelles et citees par la page (V1)."""
    texte = _texte_page(docs_dir)
    client = app.test_client()
    ecran_classe = client.get("/optimize/quick/classe")
    client.post("/optimize/quick/classe", data={"cmd": "Cra"})
    ecran_elements = client.get("/optimize/quick/elements")
    client.post("/optimize/quick/elements", data={"cmd": "terre"})
    ecran_niveau = client.get("/optimize/quick/niveau")
```

C'est **le** patron du flux multi-étapes du dépôt : un seul client, `POST` puis `GET` successifs,
et l'état de session porte la transition. Le chemin d'arrivée du wizard s'écrit de la même façon
(mesuré, 4 appels — c'est ce que le plan doit faire asserter) :

```python
c = app.test_client()
assert c.post("/", data={"selection": "4"}).headers["Location"] == "/optimize"
assert c.get("/optimize").headers["Location"] == "/optimize/quick/classe"
c.post("/optimize/quick/classe", data={"cmd": "Cra"})
c.post("/optimize/quick/elements", data={"cmd": "terre"})
assert c.post("/optimize/quick/niveau", data={"cmd": "AVANCE"}).headers["Location"] \
    == "/optimize/wizard/recap"        # <- atterrit sur recap, pas sur slots
```

`[VERIFIED: 04-RESEARCH.md § Chemin d'arrivée réel — mesuré pas à pas, et
`POST /` `selection=4` → `/optimize` confirmé par `dofus_stuff/web/routes.py:214-222` lu cette session]`

#### 7. Assertions **négatives** (propriétés absentes) — trois formes déjà éprouvées

**(a) Absence d'un littéral, démontrée par `ast` sur un module produit** — verbatim
(`tests/test_docs_parcours.py:962-1014`, extrait) :

```python
def test_parcours_cli_ne_pose_pas_les_trois_questions(docs_dir: Path, normalize) -> None:
    """La page dit ce que le parcours en ligne de commande ne contient pas (D-33).

    Demonstration indirecte : la sonde lit le TEXTE de `dofus_stuff/optimize/profile_input.py` et
    ses litteraux de chaine par `ast`, elle n'execute jamais la ligne de commande et n'appelle
    jamais son point d'entree. Une invite composee ailleurs, ou construite dynamiquement, lui
    echapperait : c'est une limite nommee, pas une couverture revendiquee.
    """
    ...
    else:
        arbre = ast.parse(chemin.read_text(encoding="utf-8"))
        litteraux = [
            noeud.value
            for noeud in ast.walk(arbre)
            if isinstance(noeud, ast.Constant) and isinstance(noeud.value, str)
        ]
    ...
    for litteral in litteraux:
        normalise = normalize(litteral)
        for motif in MOTS_PROFIL_INTERDITS:
            if re.search(motif, normalise):
                constats.append(
                    f"{SOURCE_PROFIL} : le litteral « {litteral} » contient une invite de classe ou "
                    f"d'element ; attendu l'absence de toute invite de ce genre, pour que la phrase "
                    f"« {MOTIF_PAGE_CLI} » de {PAGE} reste vraie"
                )
```

**(b) Garde statique sur le module de test lui-même** — verbatim
(`tests/test_docs_parcours.py:1840-1888`, extrait) : `test_aucun_post_db_sans_patch` parse
`Path(__file__)` et refuse toute `ast.Call` dont `data={"cmd": "DB"}`. C'est la forme à reprendre
pour la garde de clôture du nouveau module (jamais d'exécution du produit, jamais d'écriture) :

```python
    arbre = ast.parse(Path(__file__).read_text(encoding="utf-8"))
    ...
    for noeud in ast.walk(arbre):
        if not isinstance(noeud, ast.Call):
            continue
        for mot in noeud.keywords:
            if mot.arg != "data" or not isinstance(mot.value, ast.Dict):
                continue
```

**(c) Le contrôle lit ce que le lecteur voit, pas la réponse entière** — verbatim
(`tests/test_docs_parcours.py:476-490`) :

```python
def test_lignes_du_corps_ne_sont_pas_la_reponse_entiere(app) -> None:
    """Le controle lit ce que le lecteur voit, pas la reponse HTTP entiere (Pitfall 2)."""
    reponse = app.test_client().get("/optimize/quick/classe")
    lignes = _lignes_du_corps(reponse)
    entier = reponse.get_data(as_text=True)

    assert 1 <= len(lignes) <= 18, (
        f"{PAGE} : {len(lignes)} lignes de corps extraites de l'ecran de la question 1 ; attendu "
        f"entre 1 et 18 lignes visibles, comme rendu par {SOURCE_ROUTES}"
    )
    assert len("".join(lignes)) < len(entier), (
        f"{PAGE} : les lignes du corps extraites ({len(''.join(lignes))} caracteres) ne sont pas "
        f"un sous-ensemble strict de la reponse ({len(entier)} caracteres) ; attendu une extraction "
        f"qui laisse hors du controle la charge utile `data-stuff-payload` de {SOURCE_ROUTES}"
    )
```

#### 8. Garde de clôture du harnais — verbatim (lignes 245-263)

```python
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

et la mesure d'empreinte, verbatim (lignes 2456-2464) :

```python
def _empreinte(chemin: Path) -> tuple[int, int, str]:
    """Empreinte `(taille, mtime_ns, sha256)` d'un fichier, pour comparer deux instants (V15).

    Le SHA-256 porte le contenu et `mtime_ns` porte la modification a contenu identique : les trois
    composantes sont rendues pour qu'un ecart dise laquelle a bouge, et la mesure se demontre
    discriminante sur une copie dans un dossier temporaire, jamais sur le fichier du depot (T-17).
    """
    octets = chemin.read_bytes()
    return (len(octets), chemin.stat().st_mtime_ns, hashlib.sha256(octets).hexdigest())
```

`test_data_locale_non_modifiee_autour_des_rendus` (lignes 2557+) ouvre le sujet par `pytest.skip`
explicite si la base est absente (`MOTIF_BASE_ABSENTE`) — **jamais** un faux vert, **jamais** une
écriture : c'est la convention à conserver pour la mesure de non-régression de `.data/`.

#### 9. Sous-sections `H3` : helper **local**, jamais promu — verbatim (lignes 356-373)

```python
def _sous_section(corps: str, titre: str) -> str:
    """Corps d'une sous-section de niveau 3, du titre jusqu'au titre `###` suivant.

    Le helper partage `section` de `tests/conftest.py` ne connait que les titres de niveau 2 : les
    tables d'entrees vivant sous un titre de niveau 3, leur extraction reste locale a ce module et
    n'est promue nulle part (D-12).
    """
    lignes = corps.splitlines()
    debut: int | None = None
    for index, ligne in enumerate(lignes):
        if debut is not None and ligne.startswith("### "):
            return "\n".join(lignes[debut:index])
        if ligne.strip() == titre.strip():
            debut = index + 1
    if debut is None:
        raise AssertionError(
            f"{PAGE} : sous-section « {titre} » introuvable ; attendu ce titre de niveau 3, qui "
            f"porte les entrees mesurees du parcours simplifie, rendues par {SOURCE_ROUTES}"
        )
    return "\n".join(lignes[debut:])
```

#### 10. Le raccourci de solveur — `unittest.mock.patch`, importé en tête

`from unittest.mock import patch` (`tests/test_docs_parcours.py:44`) : la phase 3 patche l'étape de
calcul pour ne pas lancer le solveur. **Pitfall 6 de la recherche** : poster `GO` au récapitulatif
**exécute réellement le solveur** (`routes.py:1114-1116` → `_run_optimize_and_redirect`,
`routes.py:911-928`) et redirige vers `/optimize/result`. Le nouveau module ne poste `GO` que patché,
ou se contente de citer le libellé rendu `GO = LANCER` lu dans `body_recap`.

#### 11. Ce qui n'a **pas** d'analogue et doit être décidé par le plan

- Le wizard n'a **aucun** module de test d'ancrage existant : `tests/test_web.py` le couvre
  fonctionnellement (`test_saves_reachable_from_wizard_recap:96`, `test_optimize_wizard_go_mocked:489`,
  `test_wizard_exposes_step_nav_urls:611`, `test_optimize_wizard_...`), ce qui est une **source
  d'idiomes** complémentaire (post de `cmd` sur `/optimize/wizard/<step>`, `session_transaction`),
  mais pas un patron de contrôle documentaire.
- La lecture des 11 options et des listes de statistiques n'a **aucune constante publique** :
  `body_options` écrit onze lignes littérales (`optimize_wizard.py:198-215`) et `apply_options_input`
  porte une table locale (`:311-347`) → l'ancrage se fait **sur le rendu** (Pitfall 3), jamais sur
  une constante privée (D-14).

---

### L'idiome `PAGES_INEXISTANTES` — l'obstacle n° 1 que la phase 4 doit lever

**Fichier :** `tests/test_docs_parcours.py` (git-tracked). **Il n'existe nulle part ailleurs** :
vérifié par `grep -rn "INEXISTANT" tests/*.py` → une seule occurrence, dans ce module.
`tests/test_docs_structure.py` **ne porte aucune constante équivalente** — son seul moyen de refuser
un lien mort est `problemes_liens`, qui rougirait sur `](wizard-avance.md)` **seulement si la page
cible n'existait pas** ; comme cette phase la crée, `test_docs_structure.py` n'a rien à changer.

#### Constante et commentaire — verbatim (lignes 2229-2231)

```python
# Pages citees en prose par la section, sans lien : leurs pages n'existent pas encore (D-44).
PAGES_INEXISTANTES = ("wizard-avance.md", "base-locale.md")
```

Contexte immédiat, verbatim (ligne 2221) :

```python
RENVOIS_SANS_LIEN = ("réglages avancés", "base locale")
```

#### Site n° 1 — dans `test_limites_ancrees_sur_le_code` (`def` ligne 2261), verbatim (lignes 2392-2398)

```python
        # 6. Renvois en prose, sans lien : les pages cibles n'existent pas encore (D-44).
        for page_cible in PAGES_INEXISTANTES:
            if f"]({page_cible})" in texte:
                constats.append(
                    f"{PAGE} : la page lie « {page_cible} », qui n'existe pas encore ; attendu un "
                    f"renvoi en prose, sans lien — l'ajout du lien appartient a la phase qui cree "
                    f"cette page"
                )
```

#### Site n° 2 — dans `test_page_complete_et_sans_derive` (`def` ligne 2467), verbatim (lignes 2525-2531)

```python
    for page_cible in PAGES_INEXISTANTES:
        if f"]({page_cible})" in texte:
            constats.append(
                f"{PAGE} : {MOTIF_LIENS_INEXISTANTS} — la page lie « {page_cible} », qui n'existe pas "
                f"encore ; attendu un renvoi en prose, l'ajout du lien appartenant a la phase qui "
                f"cree cette page (D-44)"
            )
```

#### Ce qui doit changer — précisément

| Élément | État actuel | État requis par la phase 4 | Pourquoi |
|---------|-------------|----------------------------|----------|
| `PAGES_INEXISTANTES` | `("wizard-avance.md", "base-locale.md")` | `("base-locale.md",)` | `base-locale.md` appartient à la phase 5 (deferred) ; `wizard-avance.md` est créé **par cette phase** |
| Commentaire au-dessus | « leurs pages n'existent pas encore (D-44) » | doit dire **pourquoi** la constante a changé (dette D-44 levée par la phase 4 pour le wizard, la base locale restant en phase 5) | leçon écrite dans la recherche : « un commentaire faux est pire qu'un commentaire absent » |
| Portée du contrôle | `if f"]({page_cible})" in texte` sur le **texte entier** de la page, dans **deux** tests | inchangée : il ne reste que `base-locale.md` | le test ne lit pas seulement la section des limites — les deux sites portent sur `texte` |
| Assertion symétrique | absente | **à ajouter dans `tests/test_docs_wizard.py`** : le lien `](wizard-avance.md)` **existe** dans `docs/parcours-simplifie.md` (dette D-44 levée) | preuve que la levée de dette n'est pas seulement une suppression de contrôle |
| `RENVOIS_SANS_LIEN` | `("réglages avancés", "base locale")` | **inchangé** : les deux tournures doivent rester dans la section `## Ce que l'outil ne fait pas` | le lien D-63 s'ajoute **dans** le paragraphe de la ligne 256, il ne remplace pas les mots |

**Signes d'alerte mesurés (Pitfall 1)** : `pytest` vert **avant** l'édition de la page, rouge **après**
l'ajout du lien, avec un constat « la page lie « wizard-avance.md », qui n'existe pas encore ». La
correction de la constante doit être **dans le même commit** que l'ajout du lien.

#### Deux contraintes voisines du même fichier, à ne pas casser

- `test_limites_ancrees_sur_le_code` exige que la section `## Ce que l'outil ne fait pas` ne porte
  **aucun nombre de trois chiffres ou plus** sauf `COLS` (lu à `dofus_stuff/web/screens.py`, valeur
  `100`). Le lien ajouté à la ligne 256 ne doit donc introduire **aucun nombre**.
- La ligne 140 (`Ces libellés sont ceux du résultat : le wizard avancé, qui n'est pas décrit ici,
  affiche `Precedent` et `Suivant` à la place.`) reste **inchangée** (D-63/D-64) : le rendu donne
  `Page prec`/`Suivant` à `slots` et `Precedent`/`Page suiv` à `recap` (mesuré). C'est
  `docs/wizard-avance.md` qui porte la précision par étape, et un contrôle éventuel doit être
  **scopé aux étapes intermédiaires** (`options` … `items`), jamais aux 9.

---

### Le contrat du sommaire (`docs/sommaire.md`, `tests/test_docs_structure.py`, `tests/conftest.py`)

**Analog :** l'état actuel de `docs/sommaire.md` (21 lignes, verbatim intégral) :

```markdown
# Sommaire de la documentation

Cette page est le point d'entrée unique de la documentation utilisateur de dofus-stuff-machine.

## Parcours conseillé

1. Installation
2. Parcours simplifié
3. Wizard avancé
4. CLI
5. Base locale
6. Dépannage
7. Glossaire

## Index

| Page | Sujet |
|------|-------|
| [Installation](installation.md) | Installer l'outil, vérifier, lancer CLI et web |
| [Parcours simplifié](parcours-simplifie.md) | Obtenir un stuff en 3 questions, lire puis sauvegarder le résultat |
| [CLI](cli.md) | Commandes, options et exemples de fetcher.py |
```

→ La ligne à ajouter dans `## Index` (aucun autre changement), en respectant la casse et la forme
des trois lignes existantes :

```markdown
| [Wizard avancé](wizard-avance.md) | Les 9 étapes du wizard, ses filtres, ses formats et ses touches |
```

**« Parcours conseillé » reste sans lien markdown** (D-05/D-57) : le thème y est déjà en texte
numéroté, et `problemes_index` ne regarde que les cibles de liens. Ajouter le lien là-haut
satisférait l'égalité d'ensembles tout en perdant la valeur de signal (Pitfall 4).

#### Les 4 assertions qu'une nouvelle ligne d'index doit satisfaire — extraits verbatim

**(a) Exhaustivité bidirectionnelle (D-06)** — `problemes_index`, `tests/test_docs_structure.py:92-127` :

```python
def problemes_index(docs_dir: Path) -> list[str]:
    """Egalite d'ensembles entre les cibles du sommaire et les pages presentes (SOMM-02, D-06)."""
    ...
    cibles = set(LINK.findall(sommaire.read_text(encoding="utf-8")))
    pages = {
        page.relative_to(docs_dir).as_posix()
        for page in _pages(docs_dir)
        if page.name != "sommaire.md"
    }

    problemes: list[str] = []
    for cible in sorted(cibles - pages):
        problemes.append(
            f"docs/sommaire.md : cible listee absente sur disque : {cible} ; attendu une "
            f"page presente sous {docs_dir.name}/ (SOMM-02, D-06)"
        )
    for page in sorted(pages - cibles):
        problemes.append(
            f"{page} : page non listee dans docs/sommaire.md ; attendu une ligne d'index "
            f"pointant vers {page} (SOMM-02, D-06)"
        )
    return problemes
```

avec le motif de lecture des entrées, `tests/test_docs_structure.py:7` :

```python
LINK = re.compile(r"\[[^\]]*\]\((?P<target>[^)\s]+)\)")
```

→ Conséquence directe : **créer la page sans ajouter la ligne d'index fait rougir la suite**
(`wizard-avance.md : page non listee dans docs/sommaire.md`), et **ajouter la ligne sans créer la
page** aussi (`cible listee absente sur disque`). Les deux vont dans le même commit.

**(b) `H1` unique égal au libellé d'index** — `problemes_h1`, `tests/test_docs_structure.py:337-380`
(extrait) :

```python
def problemes_h1(docs_dir: Path, normalize) -> list[str]:
    """H1 unique de chaque page, egal a son libelle d'index (SOMM-03, D-11)."""
    ...
    libelles = {cible: libelle for libelle, cible in pages_listees(docs_dir)}
    ...
        titres = H1.findall(texte)
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

**(c) Ligne de retour** — `problemes_retour_sommaire`, `tests/test_docs_structure.py:383-415` :
au moins un lien dont la **cible résolue** est `docs/sommaire.md` ; convention mesurée : dernière
ligne non vide.

**(d) Encodage, brouillon, longueur** — `problemes_encodage`, `tests/test_docs_structure.py:418-451`
et les trois constantes voisines (`tests/test_docs_structure.py:300-316`) :

```python
# Jetons de brouillon interdits, compares sur le texte normalise (casse et accents ignores, D-11).
JETONS_BROUILLON = ("todo", "a completer", "lorem")

# Longueur minimale d'une page livree, en caracteres (GARD-01).
LONGUEUR_MINIMALE = 300
```

Unicité du libellé, vérifiée par `test_sommaire_index_labels_are_unique`
(`tests/test_docs_structure.py:480-512`) : deux entrées ne peuvent pas partager le même libellé
normalisé, et le sommaire ne peut pas s'auto-lister.

#### Signatures exactes des helpers disponibles (`tests/conftest.py`, verbatim)

| Helper / fixture | Signature réelle | Portée | Contrat |
|------------------|------------------|--------|---------|
| `app` | `app(catalog, tmp_path)` → Flask | function | `create_app(data_dir=tmp_path/"data", offline=True, catalog=…, load_catalog=False)` + `TESTING = True` |
| `client` | `client(app)` → test client | function | `app.test_client()` |
| `docs_dir` | `docs_dir()` → `Path` | **session** | `Path(__file__).resolve().parents[1] / "docs"` — indépendant du cwd |
| `normalize` | `normalize` → `_normalize(text: str) -> str` | session | expose **le helper**, pas une valeur |
| `section` | `section(texte, titre, page)` → `str` | session | **`page` obligatoire, sans défaut** (D-13) ; lève `AssertionError` si le titre manque |
| `sections` | `sections(texte)` → `list[tuple[str \| None, str]]` | session | l'en-tête avant le premier `##` est la première section, titre `None` |
| `lignes_de_code` | `lignes_de_code(texte)` → `list[str]` | session | toutes balises confondues |
| `lignes_exemple` | `lignes_exemple(texte)` → `list[str]` | session | blocs ```` ```console ```` seulement (D-24) |

Extraits des docstrings qui portent le contrat (verbatim) :

```python
def _normalize(text: str) -> str:
    """Normalise un libellé pour comparaison (D-11) : entités HTML, accents, casse, espaces."""
    text = html.unescape(text)
    text = unicodedata.normalize("NFKD", text)
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    return re.sub(r"\s+", " ", text).strip().lower()
```

```python
def _section(texte: str, titre: str, page: str) -> str:
    """Corps d'une section de niveau 2, du titre jusqu'au titre de niveau 2 suivant.

    `page` est obligatoire et sans valeur par defaut (D-13, D-31) : le helper partage ne peut
    plus lire la constante de page du module appelant, et un appel sans page leve `TypeError`
    des l'execution au lieu de perdre silencieusement le nom de la page dans le message.
    """
```

```python
@pytest.fixture(scope="session")
def lignes_exemple():
    """Expose _lignes_exemple aux modules de test, comme les autres helpers (D-12).

    La fixture rend le *helper*, jamais les lignes d'une page : chaque test appelle
    `lignes_exemple(texte_de_la_page)`. Rendre directement des lignes obligerait la fixture a
    connaitre la page de l'appelant, et iterer la fixture elle-meme leve
    `TypeError: 'function' object is not iterable` — contrat ecrit ici pour ne pas etre redecouvert.
    """
```

→ **D-12 : aucun de ces helpers n'est recopié dans `tests/test_docs_wizard.py`.** Ils y arrivent par
les paramètres de test (`def test_x(docs_dir, normalize, section, app)`). Le seul helper local
légitime est ce que le partagé ne sait pas faire : les `H3` (`_sous_section`) et les lectures de
marqueurs HTML du rendu (patron de la phase 3, section 2 ci-dessus).

---

### Précédent de **fonction pure** pour `renvois_obsoletes(texte, faits) -> list[str]`

**Analog :** `tests/test_docs_structure.py` — **le** précédent du dépôt : cinq fonctions **pures**,
qui prennent des entrées et **retournent une liste de constats**, appelées par des `test_*` minces
qui ne font qu'asserter `== []`. C'est exactement la forme demandée pour le détecteur.

```python
def problemes_liens(docs_dir: Path) -> list[str]:
    """Cibles de liens non resolues de docs/ ; chaque probleme cite la page, la cible et la racine (D-13)."""
```

```python
def problemes_index(docs_dir: Path) -> list[str]:
```

```python
def problemes_h1(docs_dir: Path, normalize) -> list[str]:
```

```python
def problemes_retour_sommaire(docs_dir: Path) -> list[str]:
```

```python
def problemes_encodage(docs_dir: Path, normalize) -> list[str]:
```

Signature réellement utilisée par le wrapper mince, verbatim
(`tests/test_docs_structure.py:143-146`) :

```python
def test_sommaire_lists_every_document(docs_dir: Path) -> None:
    """Le sommaire liste exactement les pages presentes sous docs/ (SOMM-02, D-06)."""
    problemes = problemes_index(docs_dir)
    assert problemes == [], "\n".join(problemes)
```

Trois traits à reprendre dans `renvois_obsoletes(texte, faits)` :

1. **Entrées explicites, aucun état global** : la fonction ne lit rien elle-même si le plan veut la
   lancer sur deux textes (fichier livré + copie figée, D-59). Le patron `problemes_*` lit le disque
   en interne ; le détecteur de la phase 4 doit accepter le **texte** en paramètre — c'est la variante
   demandée par la recherche, et c'est ce qui rend la preuve relançable.
2. **Sortie = `list[str]` de constats localisants** : chaque constat nomme la forme détectée, la
   valeur fautive et la valeur attendue **lue** ; jamais un booléen, jamais une exception.
3. **Dégradation douce de la lecture** : quand un fichier peut ne pas décoder, le module lit par un
   helper unique et **nomme** l'échec au lieu de laisser remonter `UnicodeDecodeError` — verbatim
   (`tests/test_docs_structure.py:318-323`) :

```python
def _lire_page(page: Path) -> str | None:
    """Texte de la page lu en UTF-8 strict, ou None si le decodage echoue (GARD-01, D-11)."""
    try:
        return page.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return None
```

#### Preuve à deux états : le précédent existe déjà (critère 5 de la phase 1)

`test_mutation_detecte_les_trois_derives` (`tests/test_docs_structure.py:533-603`) est le seul
précédent du dépôt d'un contrôle **observé sur un état dégradé sans toucher à l'arbre livré** :
copie jetable sous `tmp_path`, injection de dérives, assertion que **chaque** fonction `problemes_*`
les signale, puis relecture de l'arbre livré pour prouver qu'il n'a pas bougé — verbatim (extrait) :

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

```python
    # L'arbre livre n'a pas ete touche : la mutation ne vit que dans tmp_path (T-01-07).
    texte_livre = livree.read_text(encoding="utf-8")
```

→ **À transposer** : la copie figée du critère 5 (D-59b) remplit le rôle de la « copie jetable »,
mais elle est **permanente et versionnée** : elle doit donc être signalée par le détecteur à chaque
exécution, pas seulement dans un test de mutation. Le plan peut s'appuyer sur les deux : fixture
versionnée **et** (optionnellement) un test de morsure supplémentaire.

---

### `GUIDE_WIZARD.md` (aiguillage racine, transform) — contenu à retirer/migrer, verbatim

**Analog :** aucun aiguillage racine n'existe (voir « No Analog Found »). Le plus proche est
`docs/sommaire.md` (page purement navigante). Ce qui suit est le **texte réel à traiter**, cité tel
quel avec ses numéros de ligne (fichier de 330 lignes, CRLF, git-tracked).

```markdown
> **Entrée simplifiée :** le menu Optimisation demande désormais classe, éléments
> et niveau, puis lance le calcul. Exemple : `Iop` → `terre feu` → `150`.
> `multi` sélectionne tous les éléments. `AVANCE` ouvre les réglages ci-dessous ;
> `EDIT` sur les résultats reprend le profil calculé. Les objectifs PA/PM sont
> souples : un objectif manqué est signalé. Aucun budget kamas n'est supposé.

# Guide du Wizard d’optimisation de stuff
```
*(lignes 1-6, verbatim — la note de tête est exactement le type de bloc que la recherche signale
comme « note de tête + corps périmé », Pitfall 2 du research projet : elle doit disparaître avec le
reste, D-46)*

**Les trois formes obsolètes, verbatim, avec leurs lignes réelles** — matière de la future fixture
`tests/fixtures/guide-wizard-obsolete.md` (D-59b) :

````markdown
Tapez `3` puis **Entrée** pour ouvrir l’optimisation.

```
1. RECHERCHE D'OBJETS
2. LISTE DES EQUIPEMENTS
3. OPTIMISATION DE STUFF

4. SYSTEME
```
````
*(forme (a1), lignes 35-42 — l’arborescence est inversée : le code route `4 → optimize_entry`,
`3 → list_sets`, `5 → system_menu`, verbatim `dofus_stuff/web/routes.py:214-222`)*

```markdown
Vous arrivez **directement** dans le wizard (premier écran : slots et filtres).
```
*(forme (c), ligne 45 — l'arrivée passe par les 3 questions et atterrit sur `recap`)*

```markdown
Exemple : pour **interdire les armes à distance**, tapez `F7` (selon la liste affichée) jusqu’à voir `OFF`.
```
*(forme (b), ligne 157 — `F7` = `ARMES MELEE`)*

**Occurrences secondaires de la forme (a)**, lignes 50 et 328 (un détecteur qui ne chercherait que
`3. OPTIMISATION` les laisserait passer) :

```markdown
L’option **4. SYSTEME** regroupe le reste : détail d’un équipement par ID, version locale,
self-test et gestion de la base.
```
*(ligne 50 — `SYSTEME` est en `5`)*

```markdown
- Les données viennent de la **base locale** (menu `4. SYSTEME` → `4. GESTION DE LA BASE` / sync) : gardez-la à jour pour des objets récents.
```
*(ligne 328)*

**L'arborescence correcte, lue au code (D-47)** — verbatim, `dofus_stuff/web/routes.py:214-222` :

```python
@bp.post("/")
def menu_post() -> Any:
    choice = (request.form.get("selection") or "").strip()
    if choice == "4":
        return redirect(url_for("terminal.optimize_entry"))
    routes = {
        "1": "terminal.search",
        "2": "terminal.list_items",
        "3": "terminal.list_sets",
        "5": "terminal.system_menu",
    }
    if choice in routes:
        return redirect(url_for(routes[choice]))
    flash("OPTION INVALIDE — SAISIR 1 A 5", "error")
```

→ Les libellés **rendus** du menu (mesurés) : `1. RECHERCHE D'OBJETS`,
`2. LISTE DES EQUIPEMENTS`, `3. LISTE DES PANOPLIES`, `4. OPTIMISATION DE STUFF`, `5. SYSTEME`.
L'aiguillage corrigé cite ces libellés ; c'est ce qui permet au détecteur d'exiger l'**égalité** par
numéro au lieu d'une contenance floue (Open Question 1 de la recherche — recommandation retenue :
libellés rendus complets).

### `README.md` (config, transform) — les deux lignes concernées, verbatim

À **conserver tel quel** (ligne 7, lien unique vers le sommaire, D-10/D-29) :

```markdown
La documentation utilisateur commence par un sommaire unique : [Sommaire de la documentation](docs/sommaire.md).
```

À **supprimer sans remplacement** (ligne 63, D-62) :

```markdown
**Guide détaillé :** [GUIDE_WIZARD.md](GUIDE_WIZARD.md)
```

Le contrôle qui garde ce fichier, verbatim (`tests/test_docs_structure.py:190-204`) :

```python
def test_readme_links_to_sommaire(docs_dir: Path) -> None:
    """README.md porte un lien unique vers docs/sommaire.md et la cible existe (SOMM-01, D-10)."""
    racine = docs_dir.parent
    readme = racine / "README.md"
    ...
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

→ Supprimer la ligne 63 ne change pas ce compte (le lien vers le sommaire est ligne 7). **Ajouter**
un renvoi vers `GUIDE_WIZARD.md` ou `docs/wizard-avance.md` le ferait rougir si ce renvoi visait le
sommaire — D-62 va plus loin et interdit purement et simplement le remplacement. Aucun test
n'interdit aujourd'hui un lien mort dans `README.md` : c'est pourquoi la recherche recommande
(Pitfall 8, Open Question 5) que le nouveau module vérifie **explicitement**
`"](GUIDE_WIZARD.md)" not in readme`.

### `docs/sommaire.md` (index, transform)

Analog : lui-même. Voir « Le contrat du sommaire » ci-dessus pour la ligne à ajouter et les quatre
assertions à satisfaire. **Une seule ligne ajoutée**, dans `## Index`, aucun autre énoncé modifié.

### `docs/parcours-simplifie.md` (page de documentation, transform) — les 3 lignes concernées, verbatim

**(1) Renvoi n° 1 à convertir en lien (ligne 5, D-63)** — le lien `](cli.md)` de cette même phrase
est le patron exact à imiter :

```markdown
Toutes les affirmations de cette page viennent du rendu réel de la vue web. La surface des commandes n'est pas recopiée ici : elle appartient à [la page CLI](cli.md). Les écrans du wizard avancé et le fonctionnement de la base locale seront décrits dans les pages qui leur seront consacrées. Le parcours en ligne de commande, lui, ne pose pas ces trois questions : la classe et les éléments n'existent que dans le parcours guidé de l'interface web.
```

**(2) Renvoi n° 2 à convertir en lien (ligne 256, D-63)** — dans la section
`## Ce que l'outil ne fait pas`, sous le titre `### Ce que cette page ne décrit pas` :

```markdown
Les **réglages avancés** (les écrans du wizard) et le fonctionnement de la **base locale** ne sont pas décrits ici : chaque sujet appartient à la page qui lui sera consacrée, et cette page ne dit que ce que le parcours simplifié en montre. Le parcours en ligne de commande, lui, ne pose pas ces trois questions : sa surface est décrite dans la page CLI.
```

Contraintes mesurées sur cette phrase précise :
- les tournures `réglages avancés` **et** `base locale` doivent **rester** (`RENVOIS_SANS_LIEN`,
  normalisées) — le lien s'ajoute à la clause wizard, il ne remplace pas les mots ;
- **aucun nombre de trois chiffres ou plus** ne doit apparaître dans cette section sauf `COLS` (`100`) ;
- la clause « base locale » reste en prose (sa cible est la phase 5) : un lien vers `base-locale.md`
  serait mort et ferait rougir `problemes_liens`.

**(3) Ligne à NE PAS toucher (ligne 140, D-63/D-64)** :

```markdown
Ces libellés sont ceux du résultat : le wizard avancé, qui n'est pas décrit ici, affiche `Precedent` et `Suivant` à la place.
```

### `tests/test_docs_parcours.py` (test, request-response)

Analog : lui-même. Le geste exact est décrit dans « L'idiome `PAGES_INEXISTANTES` » ci-dessus :
**une constante** (`("base-locale.md",)`), **son commentaire** réécrit, et **une assertion symétrique
ajoutée dans le nouveau module**. Les deux sites d'appel (lignes 2392 et 2525) ne bougent pas : ils
itèrent sur la constante.

### `tests/fixtures/guide-wizard-obsolete.md` (fixture, file-I/O)

**Analog : aucun.** Le dossier `tests/fixtures/` **n'existe pas** (`ls tests` ne liste que des `.py`,
`git ls-files tests/fixtures` est vide) et aucun `.md` n'est aujourd'hui versionné sous `tests/`.
Le plus proche pourvoyeur de données figées est `tests/conftest.py::_sample_items()`, qui retourne un
dict littéral servant de catalogue gelé — même intention (données figées au service des tests), forme
différente (Python au lieu de Markdown) :

```python
def _sample_items() -> dict[tuple[str, int], dict]:
    return {
        ("equipment", 44): {
            "ankama_id": 44,
            "name": "Épée de Boisaille",
            "level": 7,
```

**Ce que le plan doit décider explicitement** (D-59/Claude's Discretion autorise les trois formes) :

| Option | Coût | Avantage | Risque |
|--------|------|----------|--------|
| `tests/fixtures/guide-wizard-obsolete.md` (recommandée par la recherche) | créer le dossier + `git add` **par chemin explicite** (D-66) | le détecteur est testé contre un texte réellement obsolète ; preuve lisible et relançable | nouveau dossier non versionné à ce jour |
| constante `str` dans le module de test | nul | rien à versionner | un texte multi-lignes dans un `.py` est moins lisible ; risque de dérive par rapport au fichier d'origine |
| donnée structurée (dict des 3 extraits) | faible | cible chaque forme séparément | ne reproduit pas les **associations** (ligne en forme de menu, phrase), donc teste moins bien le détecteur |

**Fait vérifié qui sécurise l'option fichier (D-59b)** : le .md sous `tests/` n'entre dans **aucun**
contrôle existant, parce que toutes les gardes de structure itèrent sur `docs_dir` :

```python
def _pages(docs_dir: Path) -> list[Path]:
    """Pages Markdown presentes sous docs/ ; liste vide si le dossier est absent (D-13)."""
    if not docs_dir.is_dir():
        return []
    return sorted(docs_dir.rglob("*.md"))
```
*(`tests/test_docs_structure.py:24-28`)*

et `pyproject.toml` déclare `testpaths = ["tests"]` — pytest ne collecte que `test_*.py`, jamais un
`.md`. **Conséquence à écrire dans la fixture** (recommandation de la recherche, Open Question 2) :
un commentaire en tête rappelant qu'il s'agit d'une **copie figée d'un état obsolète**, pas d'une
page de documentation.

---

## Shared Patterns

### Message d'échec localisant (D-13) — s'applique à **tout** le nouveau module

**Source :** `tests/test_docs_parcours.py` (`_texte_page`, `_sous_section`, chaque `constats.append`)
et `tests/conftest.py::_section`.

```python
    if not chemin.is_file():
        raise AssertionError(
            f"{PAGE} : page introuvable ({chemin}) ; attendu la page du parcours simplifie "
            f"decrite par {SOURCE_ROUTES}, livree dans docs/"
        )
```

Règle : `{page} : <constat> ; attendu <valeur> <producteur>`. Le producteur est un **fichier de
code** ou une **ligne** de code, jamais « le code » en général. À appliquer aux 3 créations de la
phase.

### Comparaison normalisée (D-11) — s'applique aux libellés cités

**Source :** `tests/conftest.py::_normalize` via la fixture `normalize`.
**Appliquer à :** toute comparaison libellé de page ↔ libellé rendu (titres d'étapes, filtres,
options, touches, messages de refus). L'analog l'utilise systématiquement
(`[normalize(ligne) for ligne in _lignes_du_corps(reponse)]`).

**Attention mesurée** : `_normalize` réduit les espaces multiples mais **ne supprime pas** l'espace
avant `]` — donc `[ON ]` (espace final produit par `_on_off`) ne se compare pas à `[ON]`. La page
décrit `ON`/`OFF` en prose et cite les **libellés** de slots/filtres, jamais la forme entre crochets
(Pitfall 5).

### Helpers partagés, jamais dupliqués (D-12) — s'applique aux 2 modules de test

**Source :** `tests/conftest.py` (`app`, `client`, `docs_dir`, `normalize`, `section`, `sections`,
`lignes_de_code`, `lignes_exemple`).
**Appliquer à :** `tests/test_docs_wizard.py` (usage par paramètres de test) et à la modification de
`tests/test_docs_parcours.py` (aucun helper nouveau). Un helper **local** n'est légitime que pour ce
que le partagé ne sait pas faire (`_sous_section` pour les H3, lecture des marqueurs HTML).

### Ancrage par API publique uniquement (D-14) — s'applique aux attentes du wizard

**Sources autorisées :** le **rendu** (client de test Flask, en processus) et les **constantes
publiques** `WIZARD_STEPS`, `STEP_TITLES`, `TYPE_FILTER_LABELS`, `TYPE_FILTER_KEYS`, `MAIN_CARACS`,
`EXO_STATS`, `RESISTANCE_STATS`, `DAMAGE_STATS`, `MISC_STATS`, `SLOT_GROUP_LABELS`.
**Interdit :** les variables locales (`keys` d'`apply_options_input`), les attributs privés,
l'introspection `argparse`/`inspect`. Les 11 options et les 9 étapes ne sont **pas** toutes des
constantes : l'ancrage se fait alors sur le **rendu** (Pitfall 3).

### Interdits d'exécution (D-15/D-61) — s'applique à la garde de clôture du module

**Source :** `tests/test_docs_parcours.py:245-263` (`RACINES_INTERDITES`, `MODULE_BASE_INTERDIT`,
`APPELS_SUPPRESSION`, `APPEL_PRODUIT`).
**Appliquer à :** `tests/test_docs_wizard.py`, qui ne doit appeler ni `main()`, ni `subprocess`, ni
`sqlite3`, ni `socket`, ni `webbrowser`, ni écrire sous `.data/`. `db clear` n'est **jamais** exécuté
et n'est jamais classé dans un parcours recommandé, ni par la page, ni par le détecteur.

### Solveur non lancé — s'applique à tout POST passant par le récapitulatif

**Source :** `from unittest.mock import patch` (`tests/test_docs_parcours.py:44`).
**Appliquer à :** tout contrôle qui poste `GO` ou une saisie vide sur `/optimize/wizard/recap`
(mesuré : `302 /optimize/result`, statut `CALCUL TERME`). `RESET`, `SAVES` et `1`–`8` sont sans
solveur. **Ne jamais** poster `GO` pour observer autre chose (Pitfall 6).

### Encodage CRLF sans BOM — s'applique aux fichiers texte produits

**Source :** `tests/test_docs_parcours.py:2506-2512` (« la derniere ligne non vide »), `:2533-2547`
(`BOM_UTF8`, `fins != crlf`) et la mesure de tout `docs/` (tableau en tête de ce document).
**Appliquer à :** `docs/wizard-avance.md`, `docs/sommaire.md`, `GUIDE_WIZARD.md`, `README.md`,
`docs/parcours-simplifie.md`, `tests/fixtures/guide-wizard-obsolete.md`.

### Commits locaux, `git add` par chemin explicite (D-66) — s'applique à la phase entière

`git add <chemin>` pour chaque fichier touché, **jamais** `git add .`. Aucun `db clear`, aucune
suppression sous `.data/` ni `.doc-agent/`, aucun push, aucun déploiement.

---

## No Analog Found

| Fichier | Rôle | Data Flow | Raison |
|---------|------|-----------|--------|
| `tests/fixtures/guide-wizard-obsolete.md` (créé par cette phase) | fixture de test (donnée) | file-I/O | **`tests/fixtures/` n'existe pas** : `ls tests` ne liste que des `.py` + `__pycache__/`, et `git ls-files tests/fixtures` est vide. Le dossier et le fichier sont à **créer** ; aucun `.md` n'est aujourd'hui versionné sous `tests/`. Le plan doit choisir explicitement entre fichier / constante / donnée structurée (D-59 le permet) — tableau d'arbitrage plus haut |
| `GUIDE_WIZARD.md` réduit à un aiguillage | aiguillage racine (config/navigation) | transform | **Aucun aiguillage racine n'existe dans le dépôt.** Le plus proche est `docs/sommaire.md` (21 lignes, uniquement de la navigation, sans énoncé de contenu) : à utiliser comme **modèle de ton et de concision**, pas comme modèle de structure. Aucun test ne couvre aujourd'hui un fichier de la racine autre que le lien unique de `README.md` → les deux liens de l'aiguillage doivent être vérifiés **explicitement** par `tests/test_docs_wizard.py` (Pitfall 8, D-46/D-48) |

**Analogs dont l'existence a été vérifiée sur disque et dans l'index git** (aucun chemin de miroir
gitignoré n'est cité dans ce document) : `docs/parcours-simplifie.md`, `docs/cli.md`,
`docs/installation.md`, `docs/sommaire.md`, `GUIDE_WIZARD.md`, `README.md`, `tests/conftest.py`,
`tests/test_docs_parcours.py`, `tests/test_docs_structure.py`, `tests/test_docs_cli.py`,
`tests/test_docs_code_anchor.py`, `dofus_stuff/web/optimize_wizard.py`,
`dofus_stuff/web/routes.py`, `dofus_stuff/model/solver_spec.py` — tous listés par
`git ls-files` (non vides).

## Metadata

**Analog search scope :** racine du dépôt (`README.md`, `GUIDE_WIZARD.md`, `pyproject.toml`),
`docs/**` (4 pages), `tests/**` (11 modules + `conftest.py`), `dofus_stuff/**` en **lecture seule**
pour confirmer les constantes publiques citées (`web/optimize_wizard.py`, `web/routes.py`,
`model/solver_spec.py`, `web/screens.py`, `web/templates/screen.html`).
**Files scanned :** 11 fichiers lus (intégraux ou par plages non recouvrantes) + 6 relevés ciblés.
**Pattern extraction date :** 2026-09-11.
**Baseline mesurée (recherche, même session) :** `186 passed in 3.65s`, `.data/dofus.sqlite3`
inchangée (24989696 octets, sha256 `e3793d64…fef7b`).

**Rappel de périmètre pour le planificateur :** cette phase **ne modifie aucun fichier de
`dofus_stuff/**`** (D-66) ; les seuls fichiers créés sont `docs/wizard-avance.md`,
`tests/test_docs_wizard.py` et (si l'option fichier est retenue)
`tests/fixtures/guide-wizard-obsolete.md`.



