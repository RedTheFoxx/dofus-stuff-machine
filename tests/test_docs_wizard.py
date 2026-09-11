"""Ancrage de la page `docs/wizard-avance.md` sur le rendu reel du wizard avance.

Le contrat va du rendu vers la page : les neuf ecrans du wizard avance sont rendus par le client de
test Flask, en processus, sur la fixture `app` de `tests/conftest.py` (D-32), puis les titres, les
libelles, les formats et les messages lus dans le corps, dans la ligne de statut et dans la ligne
d'en-tete sont compares a ceux que la page cite. Aucun serveur n'est lance, aucun socket n'est
ouvert, le programme du produit n'est jamais execute et rien n'est ecrit sous `.data/` : la fixture
`app` construit sa propre base dans un dossier temporaire.

Limite nommee : la garde `ast` de ce module est une demonstration statique et indirecte. Elle dit ce
que ce module importe et appelle, pas ce qu'un autre chemin ferait. En particulier, poster `GO` sur
le recapitulatif **execute le solveur** (`dofus_stuff/web/routes.py:1114-1116`) : la garde refuse
cette paire dans le module, et aucun controle de ce module ne poste `GO`.

Limite nommee : la prose libre de la page (les phrases d'explication) n'est pas verifiee par un
test. Les controles portent sur les libelles, les nombres et les messages **cites**, et ce module ne
revendique aucune exhaustivite de la redaction.
"""

from __future__ import annotations

import ast
import re
from pathlib import Path

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

# Contrat de titres de la page : chaque titre est ecrit au caractere pres, le helper `section` de
# `tests/conftest.py` ne normalisant pas un titre. Les titres des plans 04-02 a 04-04 sont poses des
# maintenant, a leur position finale, pour qu'une derive de titre soit vue au plus tot.
TITRES_SECTION_ATTENDUS = (
    "## Les 9 étapes du wizard",
    "## Slots et filtres",
    "## Les 11 options du solveur",
    "## Les quatre nombres d'une ligne",
    "## Interdire, forcer, retirer un objet",
    "## Source de vérité",
)

TITRE_ETAPES = TITRES_SECTION_ATTENDUS[0]
TITRE_SLOTS = TITRES_SECTION_ATTENDUS[1]
TITRE_SOURCE = TITRES_SECTION_ATTENDUS[5]

# Sous-titres de niveau 3 de la section des slots et des filtres.
SOUS_TITRE_EMPLACEMENTS = "### Les 11 emplacements"
SOUS_TITRE_FILTRES = "### Les 10 filtres de type"

# Marqueurs du gabarit reel (`dofus_stuff/web/templates/screen.html`) : le corps visible est encadre
# par `id="body"` et par la seule ligne de statut, qui porte les messages de refus ; la ligne
# d'en-tete porte le code de programme et le titre de l'ecran.
MARQUEUR_CORPS = 'id="body">'
MARQUEUR_STATUT = '<div class="row status'
MARQUEUR_ENTETE = '<div class="row header" id="header-row">'
LIGNE_CORPS = re.compile(r'<div class="row">(.*?)</div>', re.S)
LIBELLE_SAISIE = re.compile(r'<label class="input-label meta">(.*?)</label>', re.S)
TOUCHE_BARRE = re.compile(
    r'<span class="fkey-key meta">([^<]*)</span>'
    r'<span class="fkey-eq meta">=</span>'
    r'<span class="fkey-label">([^<]*)</span>'
)

# Lignes rendues des emplacements et des filtres (`optimize_wizard.py:189-215`) : le numero, l'etat
# entre crochets produit par `_on_off` (espace finale comprise) et le libelle. Le motif est applique
# ligne par ligne, une ligne rendue ne portant jamais deux entrees.
MOTIF_EMPLACEMENT_RENDU = re.compile(
    r"^\s*(?P<numero>\d{1,2})\.\s+\[\s*(?:ON|OFF)\s*\]\s*(?P<libelle>.+?)\s*$"
)
MOTIF_FILTRE_RENDU = re.compile(
    r"^F(?P<numero>\d{1,2})\.\s+\[\s*(?:ON|OFF)\s*\]\s*(?P<libelle>.+?)\s*$"
)

# Lignes de tableau de la page : `| 1 | `AMULETTE` |` et `| `F1` | `FAMILIER` |`.
MOTIF_LIGNE_EMPLACEMENT = re.compile(
    r"^\|\s*(?P<numero>\d{1,2})\s*\|\s*`(?P<libelle>[^`]+)`\s*\|\s*$"
)
MOTIF_LIGNE_FILTRE = re.compile(
    r"^\|\s*`F(?P<numero>\d{1,2})`\s*\|\s*`(?P<libelle>[^`]+)`\s*\|\s*$"
)

# Invites et rappel de l'ecran des slots et des filtres, lus au rendu et jamais ecrits de memoire.
MOTIF_INVITE_EMPLACEMENTS = re.compile(r"^SLOTS \(N=TOGGLE\) :$")
MOTIF_INVITE_FILTRES = re.compile(r"^FILTRES TYPES \(F\+N\) :$")
MOTIF_RAPPEL_TOUCHES = re.compile(r"^N=TOGGLE SLOT\s+FN=TOGGLE FILTRE$")

# Motif de morsure porte par une constante de module et jamais ecrit en clair dans la ligne
# d'assertion (regle posee au plan 03-03, tache 2) : pytest reproduit cette ligne dans sa sortie, et
# une valeur ecrite en clair y serait trouvee sans qu'aucun message n'ait ete produit.
MOTIF_ORDRE_ETAPES = "ordre de WIZARD_STEPS"

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


def _texte_page(docs_dir: Path) -> str:
    """Texte de la page, lu en UTF-8 explicite ; page absente = AssertionError localisante (D-13).

    Jamais de `FileNotFoundError` brut : l'echec nomme la page, le chemin attendu et le fichier de
    code dont elle decrit la surface. Toute lecture de la page passe par ici.
    """
    chemin = docs_dir / PAGE
    if not chemin.is_file():
        raise AssertionError(
            f"{PAGE} : page introuvable ({chemin}) ; attendu la page du wizard avance "
            f"decrite par {SOURCE_WIZARD}, livree dans docs/"
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


def _entete(reponse) -> str:
    """Texte de la ligne d'en-tete de la coquille, ou "" si le marqueur est absent du rendu.

    Le titre de l'etape n'est rendu nulle part ailleurs : la ligne de corps d'un ecran de
    statistiques porte le titre en majuscules pour sa pagination, mais l'ecran `recap` n'en porte
    aucun. L'en-tete est donc la seule source du titre rendu.
    """
    texte = reponse.get_data(as_text=True)
    if MARQUEUR_ENTETE not in texte:
        return ""
    return texte.split(MARQUEUR_ENTETE, 1)[1].split("</div>", 1)[0]


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


def _sous_section(corps: str, titre: str) -> str:
    """Corps d'une sous-section de niveau 3, du titre jusqu'au titre `###` suivant.

    Le helper partage `section` de `tests/conftest.py` ne connait que les titres de niveau 2 : les
    listes vivant sous un titre de niveau 3, leur extraction reste locale a ce module et n'est
    promue nulle part (D-12).
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
            f"porte la liste mesuree du wizard avance, rendue par {SOURCE_WIZARD}"
        )
    return "\n".join(lignes[debut:])


def _emplacements_du_rendu(lignes: list[str]) -> dict[int, str]:
    """Couples numero -> libelle des emplacements, lus dans les lignes rendues du corps."""
    couples: dict[int, str] = {}
    for ligne in lignes:
        trouve = MOTIF_EMPLACEMENT_RENDU.match(ligne)
        if trouve is not None:
            couples[int(trouve.group("numero"))] = trouve.group("libelle").strip()
    return couples


def _filtres_du_rendu(lignes: list[str]) -> dict[int, str]:
    """Couples numero -> libelle des filtres de type, lus dans les lignes rendues du corps."""
    couples: dict[int, str] = {}
    for ligne in lignes:
        trouve = MOTIF_FILTRE_RENDU.match(ligne)
        if trouve is not None:
            couples[int(trouve.group("numero"))] = trouve.group("libelle").strip()
    return couples


def _couples_de_table(sous_texte: str, motif: re.Pattern[str]) -> dict[int, str]:
    """Couples numero -> libelle cites par une table de la page, une ligne de tableau par couple."""
    couples: dict[int, str] = {}
    for ligne in sous_texte.splitlines():
        trouve = motif.match(ligne)
        if trouve is not None:
            couples[int(trouve.group("numero"))] = trouve.group("libelle").strip()
    return couples


def _imports_du_module(arbre: ast.AST) -> set[str]:
    """Modules importes par le module d'ancrage, imports imbattables compris dans les fonctions."""
    importes: set[str] = set()
    for noeud in ast.walk(arbre):
        if isinstance(noeud, ast.Import):
            importes.update(alias.name for alias in noeud.names)
        elif isinstance(noeud, ast.ImportFrom) and noeud.module is not None:
            importes.add(noeud.module)
    return importes


def _appels_du_module(arbre: ast.AST) -> set[str]:
    """Noms appeles par le module d'ancrage, sous forme `objet.attribut` ou `nom`."""
    appeles: set[str] = set()
    for noeud in ast.walk(arbre):
        if not isinstance(noeud, ast.Call):
            continue
        if isinstance(noeud.func, ast.Attribute):
            appeles.add(noeud.func.attr)
        else:
            appeles.add(getattr(noeud.func, "id", ""))
    return appeles


def test_garde_de_cloture_du_harnais() -> None:
    """Le module n'ouvre ni la base, ni un processus, ni une socket, et ne poste jamais `GO` (T-04-03).

    La propriete est verifiee sur le texte de ce module par `ast`, et jamais par une recherche de
    chaines : le module cite lui-meme les noms interdits dans ses messages, une recherche textuelle
    se detecterait elle-meme. Le controle porte sur le risque reel — ouvrir la base, lancer un
    processus, ouvrir une socket, joindre le reseau, supprimer un fichier, executer le produit — donc
    un import public pur ajoute plus tard passe sans revision, alors qu'un import qui tirerait la
    base rougit. Poster `GO` au recapitulatif execute le solveur : c'est la saisie interdite ici.
    """
    arbre = ast.parse(Path(__file__).read_text(encoding="utf-8"))
    importes = _imports_du_module(arbre)
    appeles = _appels_du_module(arbre)
    constats: list[str] = []

    racines = sorted(module for module in importes if module.split(".")[0] in RACINES_INTERDITES)
    if racines:
        constats.append(
            f"import(s) de base, de processus, de socket ou de reseau : {', '.join(racines)} ; "
            f"attendu aucun de ces imports dans le module d'ancrage decrit par {PAGE} "
            f"({SOURCE_ROUTES}, wizard avance)"
        )
    if MODULE_BASE_INTERDIT in importes or any(
        module.startswith(MODULE_BASE_INTERDIT + ".") for module in importes
    ):
        constats.append(
            f"import de « {MODULE_BASE_INTERDIT} » ; attendu aucun import de la base locale, la "
            f"fixture `app` construisant sa propre base temporaire ({SOURCE_WIZARD})"
        )
    if APPEL_PRODUIT in appeles:
        constats.append(
            f"appel a {APPEL_PRODUIT}() dans le module d'ancrage ; attendu un ancrage par le client "
            f"de test Flask de {SOURCE_ROUTES}, le produit n'etant jamais execute"
        )
    suppressions = sorted(set(APPELS_SUPPRESSION) & appeles)
    if suppressions:
        constats.append(
            f"appel(s) de suppression de fichier : {', '.join(suppressions)} ; attendu aucun appel "
            f"destructif dans le module d'ancrage decrit par {PAGE}"
        )

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

    assert not constats, (
        f"{PAGE} : constats sur la garde de cloture du harnais : "
        + " ; ".join(constats)
        + f" ; attendu un module d'ancrage qui rend les ecrans de {SOURCE_ROUTES} en processus, sans "
        f"ouvrir la base locale, sans joindre le reseau et sans jamais executer le solveur"
    )


def test_page_et_index_du_wizard(docs_dir: Path, app, normalize) -> None:
    """La page existe, son index est coherent, et les 9 titres rendus y sont cites (WIZ-01).

    Tranche verticale du plan : la page, sa ligne d'index, le harnais et le rendu sont traverses
    d'un bout a l'autre par ce seul controle. Les neuf ecrans repondent 200 sur un client neuf
    (`load_wizard_spec` retombe sur `default_player_spec(level=200)`), donc aucun etat de session
    n'est rejoue : un client neuf rend l'ecran, et la ligne d'en-tete porte le titre de l'etape.
    """
    texte = _texte_page(docs_dir)
    constats: list[str] = []

    # 1. La ligne d'index de la page, lue dans la table du sommaire : le libelle cite sert de
    #    reference au H1, il n'est jamais ecrit deux fois de memoire.
    sommaire = (docs_dir / SOMMAIRE).read_text(encoding="utf-8")
    entree = re.search(rf"\|\s*\[(?P<libelle>[^\]]+)\]\({re.escape(PAGE)}\)", sommaire)
    if entree is None:
        constats.append(
            f"{PAGE} : page non listee dans docs/sommaire.md ; attendu une ligne de la table "
            f"« ## Index » de {SOMMAIRE} pointant vers {PAGE} (D-05, D-57)"
        )
    libelle = entree.group("libelle") if entree is not None else ""

    # 2. Un seul titre de niveau 1, egal au libelle d'index apres normalisation (D-11, D-56).
    titres = [ligne for ligne in texte.splitlines() if ligne.startswith("# ")]
    if len(titres) != 1:
        constats.append(
            f"{PAGE} : la page porte {len(titres)} titre(s) de niveau 1 ({', '.join(titres)}) ; "
            f"attendu un seul titre de niveau 1, celui de la page (D-56)"
        )
    elif libelle:
        h1 = titres[0][len("# ") :].strip()
        if normalize(h1) != normalize(libelle):
            constats.append(
                f"{PAGE} : H1 « {h1} » different du libelle d'index « {libelle} » ; attendu le "
                f"libelle d'index de {SOMMAIRE} pour {PAGE} (D-11)"
            )

    # 3. Les neuf titres rendus, lus dans la ligne d'en-tete de chaque ecran, puis exiges de la page.
    client = app.test_client()
    for numero, etape in enumerate(WIZARD_STEPS, start=1):
        rendu = client.get(f"/optimize/wizard/{etape}")
        attendu = STEP_TITLES.get(etape, "")
        entete = _entete(rendu)
        if rendu.status_code != 200 or normalize(attendu) not in normalize(entete):
            constats.append(
                f"l'ecran « {etape} » (etape {numero}) repond {rendu.status_code} et son en-tete "
                f"vaut « {entete} » ; attendu le titre « {attendu} » rendu par la ligne d'en-tete "
                f"de /optimize/wizard/{etape}, construit par {SOURCE_ROUTES}"
            )
        if normalize(attendu) not in normalize(texte):
            constats.append(
                f"{PAGE} : le titre rendu de l'etape {numero} vaut « {attendu} » et n'est pas cite "
                f"par la page ; attendu ce titre, lu au rendu de /optimize/wizard/{etape} et produit "
                f"par {SOURCE_WIZARD} (STEP_TITLES)"
            )

    assert not constats, (
        f"{PAGE} : constats sur la page et son index : "
        + " ; ".join(constats)
        + f" ; attendu la page de {SOURCE_WIZARD} listee dans {SOMMAIRE}, ouverte par un H1 egal a "
        f"son libelle d'index et citant les {len(WIZARD_STEPS)} titres rendus par les ecrans"
    )


def test_etapes_dans_l_ordre_du_code(docs_dir: Path, app, normalize, section) -> None:
    """Les 9 titres rendus sont cites par la page dans l'ordre de `WIZARD_STEPS` (D-50).

    L'ordre attendu n'est jamais ecrit dans ce module : il est relu dans `WIZARD_STEPS` et les
    titres dans `STEP_TITLES` (`dofus_stuff/web/optimize_wizard.py:23-45`), puis confronte a la ligne
    d'en-tete que le rendu produit reellement pour chacun des neuf ecrans. La comparaison d'ordre se
    fait dans la seule section des etapes, jamais sur la page entiere : la page cite ailleurs des
    mots qui reprennent un titre d'etape, et une position globale mesurerait alors autre chose.
    """
    texte = _texte_page(docs_dir)
    corps = section(texte, TITRE_ETAPES, PAGE)
    corps_normalise = normalize(corps)
    constats: list[str] = []

    client = app.test_client()
    titres: list[tuple[int, str, str]] = []
    for numero, etape in enumerate(WIZARD_STEPS, start=1):
        rendu = client.get(f"/optimize/wizard/{etape}")
        attendu = STEP_TITLES.get(etape, "")
        entete = _entete(rendu)
        if rendu.status_code != 200 or normalize(attendu) not in normalize(entete):
            constats.append(
                f"l'ecran « {etape} » (etape {numero}) repond {rendu.status_code} et son en-tete "
                f"vaut « {entete} » ; attendu le titre « {attendu} » rendu par la ligne d'en-tete de "
                f"/optimize/wizard/{etape}, construit par {SOURCE_ROUTES}"
            )
        titres.append((numero, etape, attendu))

    numerotees = [
        ligne for ligne in corps.splitlines() if re.match(r"^\d+\.\s", ligne.strip())
    ]
    if len(numerotees) != len(WIZARD_STEPS):
        constats.append(
            f"{PAGE} : la section « {TITRE_ETAPES} » porte {len(numerotees)} ligne(s) numerotee(s) "
            f"pour {len(WIZARD_STEPS)} etape(s) listee(s) par {SOURCE_WIZARD} (WIZARD_STEPS) ; "
            f"attendu {MOTIF_ORDRE_ETAPES}"
        )

    position = -1
    for numero, etape, attendu in titres:
        index = corps_normalise.find(normalize(attendu))
        if index < 0:
            constats.append(
                f"{PAGE} : le titre rendu de l'etape {numero} (« {attendu} ») de "
                f"/optimize/wizard/{etape} n'est pas cite par la section « {TITRE_ETAPES} » ; attendu "
                f"ce titre, lu au rendu et produit par {SOURCE_WIZARD} (STEP_TITLES), dans "
                f"l'{MOTIF_ORDRE_ETAPES}"
            )
            continue
        if index < position:
            constats.append(
                f"{PAGE} : le titre « {attendu} » de l'etape {numero} ({etape}) apparait avant le "
                f"titre de l'etape precedente ; attendu l'{MOTIF_ORDRE_ETAPES} — les "
                f"{len(WIZARD_STEPS)} titres cites dans l'ordre du code ({SOURCE_WIZARD}, "
                f"WIZARD_STEPS) et rendus par {SOURCE_ROUTES}"
            )
            continue
        position = index

    assert not constats, (
        f"{PAGE} : constats sur l'ordre des etapes : "
        + " ; ".join(constats)
        + f" ; attendu les {len(WIZARD_STEPS)} titres rendus cites dans l'{MOTIF_ORDRE_ETAPES}, "
        f"relu dans {SOURCE_WIZARD} et confronte au rendu de {SOURCE_ROUTES}"
    )


def test_slots_et_filtres_ancres_au_rendu(docs_dir: Path, app, normalize, section) -> None:
    """Les emplacements et les filtres cites par la page sont ceux du rendu, numerotes (D-53).

    L'ecran `slots` est rendu sur ses **deux** pages : son corps compte plus de 18 lignes
    (`BODY_LINES`, `dofus_stuff/web/screens.py:10`), les onze emplacements tiennent en page 1 mais
    les derniers filtres ne sont lisibles qu'en page 2. Les couples `(numero, libelle)` et
    `(F<n>, libelle)` sont extraits du corps rendu, puis exiges de la page a l'identique. Le couple
    `F6`/`F7` est en plus adosse a ses deux sources publiques — `TYPE_FILTER_KEYS[5]`/`[6]`
    (`dofus_stuff/model/solver_spec.py:42-53`) apparies a `TYPE_FILTER_LABELS`
    (`dofus_stuff/web/optimize_wizard.py:111-121`) — pour que la permutation des deux libelles ne
    puisse pas passer.
    """
    texte = _texte_page(docs_dir)
    corps_page = section(texte, TITRE_SLOTS, PAGE)
    constats: list[str] = []

    client = app.test_client()
    ecran = client.get("/optimize/wizard/slots")
    ecran_page2 = client.get("/optimize/wizard/slots?page=2")
    lignes = _lignes_du_corps(ecran) + _lignes_du_corps(ecran_page2)
    rendus_slots = _emplacements_du_rendu(lignes)
    rendus_filtres = _filtres_du_rendu(lignes)

    if ecran.status_code != 200 or ecran_page2.status_code != 200:
        constats.append(
            f"l'ecran /optimize/wizard/slots repond {ecran.status_code} en page 1 et "
            f"{ecran_page2.status_code} en page 2 ; attendu 200 sur les deux, cet ecran etant rendu "
            f"par {SOURCE_ROUTES}"
        )
    if len(rendus_slots) != len(SLOT_GROUPS):
        constats.append(
            f"le rendu de /optimize/wizard/slots porte {len(rendus_slots)} emplacement(s) numerote(s) "
            f"pour {len(SLOT_GROUPS)} groupe(s) de {SOURCE_SPEC} (SLOT_GROUPS) ; attendu autant "
            f"d'emplacements rendus que de groupes, le corps etant lu sur ses deux pages"
        )
    if len(rendus_filtres) != len(TYPE_FILTER_KEYS):
        constats.append(
            f"le rendu de /optimize/wizard/slots porte {len(rendus_filtres)} filtre(s) numerote(s) "
            f"pour {len(TYPE_FILTER_KEYS)} touche(s) de {SOURCE_SPEC} (TYPE_FILTER_KEYS) ; attendu "
            f"autant de filtres rendus que de touches, le corps etant lu sur ses deux pages"
        )

    # 1. Les invites et le rappel de touches, lus au rendu puis exiges de la page.
    for motif, invite in (
        (MOTIF_INVITE_EMPLACEMENTS, "SLOTS (N=TOGGLE) :"),
        (MOTIF_INVITE_FILTRES, "FILTRES TYPES (F+N) :"),
        (MOTIF_RAPPEL_TOUCHES, "N=TOGGLE SLOT  FN=TOGGLE FILTRE"),
    ):
        ligne_rendue = next((ligne.strip() for ligne in lignes if motif.match(ligne.strip())), "")
        if not ligne_rendue:
            constats.append(
                f"la ligne « {invite} » est absente du rendu de /optimize/wizard/slots ; attendu "
                f"cet intitule, ecrit par {SOURCE_WIZARD} (body_slots)"
            )
            continue
        if normalize(ligne_rendue) not in normalize(texte):
            constats.append(
                f"{PAGE} : l'intitule rendu « {ligne_rendue} » n'est pas cite par la page ; attendu "
                f"cet intitule, lu au rendu et ecrit par {SOURCE_WIZARD} (body_slots)"
            )

    # 2. Les onze emplacements, numero par numero.
    cites_slots = _couples_de_table(_sous_section(corps_page, SOUS_TITRE_EMPLACEMENTS), MOTIF_LIGNE_EMPLACEMENT)
    for numero in sorted(set(rendus_slots) | set(cites_slots)):
        rendu = rendus_slots.get(numero, "")
        cite = cites_slots.get(numero, "")
        if normalize(rendu) != normalize(cite):
            constats.append(
                f"{PAGE} : emplacement {numero} — la section cite « {cite} » et le rendu associe le "
                f"numero {numero} a « {rendu} » ; attendu le libelle rendu par {SOURCE_WIZARD} "
                f"(SLOT_GROUP_LABELS), sur l'ordre de {SOURCE_SPEC} (SLOT_GROUPS)"
            )

    # 3. Les dix filtres, touche par touche.
    cites_filtres = _couples_de_table(_sous_section(corps_page, SOUS_TITRE_FILTRES), MOTIF_LIGNE_FILTRE)
    for numero in sorted(set(rendus_filtres) | set(cites_filtres)):
        rendu = rendus_filtres.get(numero, "")
        cite = cites_filtres.get(numero, "")
        if normalize(rendu) != normalize(cite):
            constats.append(
                f"{PAGE} : filtre F{numero} — la section cite « {cite} » et le rendu associe F{numero} "
                f"a « {rendu} » ; attendu le couple (F{numero}, libelle) rendu par {SOURCE_WIZARD} "
                f"(TYPE_FILTER_LABELS)"
            )

    # 4. Seconde source du couple F6/F7, lue au code et jamais ecrite de memoire.
    for index in (5, 6):
        cle = TYPE_FILTER_KEYS[index]
        numero = index + 1
        attendu = TYPE_FILTER_LABELS.get(cle, cle.upper())
        cite = cites_filtres.get(numero, "")
        if normalize(cite) != normalize(attendu):
            constats.append(
                f"{PAGE} : F{numero} — {SOURCE_SPEC} donne TYPE_FILTER_KEYS[{index}] = « {cle} » et "
                f"{SOURCE_WIZARD} associe cette cle a « {attendu} » dans TYPE_FILTER_LABELS, alors "
                f"que la section cite « {cite} » ; attendu le couple lu au rendu et au code"
            )

    # 5. Les refus mesures, exiges de la page : le message rendu est la seule source.
    refus = (
        (("abc",), "SAISIE INVALIDE"),
        (("F11",), "FILTRE INVALIDE"),
    )
    for saisies, message_attendu in refus:
        client_refus = app.test_client()
        statut = ""
        for saisie in saisies:
            reponse = client_refus.post(
                "/optimize/wizard/slots", data={"cmd": saisie}, follow_redirects=True
            )
            statut = _statut(reponse)
        if normalize(message_attendu) not in normalize(statut):
            constats.append(
                f"la saisie « {saisies[-1]} » rend « {statut} » ; attendu le message "
                f"« {message_attendu} » dans la ligne de statut, ecrit par {SOURCE_ROUTES} "
                f"(apply_slots_input)"
            )
        if normalize(message_attendu) not in normalize(texte):
            constats.append(
                f"{PAGE} : le message de refus rendu « {message_attendu} » n'est pas cite par la "
                f"page ; attendu ce message, lu au rendu et ecrit par {SOURCE_WIZARD} "
                f"(apply_slots_input)"
            )

    # 6. Le dernier emplacement actif ne peut pas etre desactive : les onze numeros sont bascules,
    #    puis le dernier emplacement encore actif est bascule a son tour.
    client_dernier = app.test_client()
    statut = ""
    for numero in range(1, len(rendus_slots) + 1):
        reponse = client_dernier.post(
            "/optimize/wizard/slots", data={"cmd": str(numero)}, follow_redirects=True
        )
        statut = _statut(reponse)
    reponse = client_dernier.post("/optimize/wizard/slots", data={"cmd": "8"}, follow_redirects=True)
    statut = _statut(reponse)
    if normalize("AU MOINS UN SLOT REQUIS") not in normalize(statut):
        constats.append(
            f"desactiver le dernier emplacement actif rend « {statut} » (apres {len(rendus_slots)} "
            f"bascule(s) et une derniere) ; attendu le message « AU MOINS UN SLOT REQUIS », ecrit par "
            f"{SOURCE_WIZARD} (apply_slots_input)"
        )
    if normalize("AU MOINS UN SLOT REQUIS") not in normalize(texte):
        constats.append(
            f"{PAGE} : le message rendu « AU MOINS UN SLOT REQUIS » n'est pas cite par la page ; "
            f"attendu ce message, lu au rendu et ecrit par {SOURCE_WIZARD} (apply_slots_input)"
        )

    assert not constats, (
        f"{PAGE} : constats sur les slots et les filtres : "
        + " ; ".join(constats)
        + f" ; attendu les {len(SLOT_GROUPS)} emplacements et les {len(TYPE_FILTER_KEYS)} filtres "
        f"cites avec le numero et le libelle rendus par {SOURCE_WIZARD} et {SOURCE_SPEC}"
    )
