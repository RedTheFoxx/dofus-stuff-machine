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

from dofus_stuff.web.optimize_wizard import STEP_TITLES, WIZARD_STEPS

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
