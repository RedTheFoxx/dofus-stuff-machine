"""Preuve de morsure du harnais documentaire : une copie mutee, et le controle doit rougir.

Cette batterie est la mecanisation du **critere 4** du ROADMAP et de `GARD-04` (`D-97`, `D-98`) : elle
n'ajoute aucun controle documentaire, elle **prouve que les controles livres mordent**. La mesure se fait
integralement sur une **copie** construite sous `tmp_path` : le depot n'est jamais modifie, et ce module
n'ecrit rien hors du dossier temporaire de pytest.

Le contrat, dans l'ordre ou la preuve se deroule pour chaque derive declaree :

- la copie est construite a neuf (famille par famille), puis la racine lue par les modules d'ancrage est
  **redirigee** vers cette copie : sans cette redirection, un controle lirait le depot reel et la mutation
  porterait sur une copie que personne ne lit ;
- la copie est **verte avant la mutation** : le controle de la famille est appele sur la copie intacte et
  doit ne rien produire. Une morsure sur une copie deja rouge ne prouve rien, et c'est pourquoi cette
  precondition est elle-meme un test (`test_la_copie_est_verte_avant_toute_mutation`) ;
- la derive est ensuite ecrite dans la copie, jamais dans le depot ;
- le controle est rappele sur la copie mutee, et **le motif attendu** doit apparaitre dans ses constats.
  Les motifs ne sont pas recopies d'un module a l'autre : ils sont **lus** dans le module d'ancrage
  (`D-14`, `D-17`), par le nom de leur constante. Un motif introuvable est un constat, jamais un silence.

La tache 1 declare la famille `page_livree` ; les quatre autres familles du plan sont ajoutees par la
tache 2, chacune avec ses mutations. Une derive hors de ces familles n'est pas demontree impossible : elle
est couverte « autant que » par les gardes livrees, et c'est ecrit ici plutot que de laisser croire a une
exhaustivite.

Aucune reimplementation : les fonctions appelees sont celles des modules d'ancrage livres par les plans
06-01, 06-02 et 06-03 (`problemes_pages_epinglees`, `problemes_couverture_index`, `problemes_readme`,
`problemes_messages`, `problemes_glossaire`, `problemes_parcours`, et la sonde `_produire`). Une
reimplementation ne prouverait que la reimplementation.

Aucun sous-processus n'est lance : l'interdiction est celle du harnais (la garde de cloture de chaque
module d'ancrage refuse `subprocess`, et ce module reprend cette garde), et le rejeu de la suite entiere
est une **commande d'executeur** rejouee dans `06-04-SUMMARY.md`, jamais une assertion d'un test. La
morsure est donc cherchee **en processus** : la copie vit dans `tmp_path`, et la fonction de constats est
appelee sur elle.

Consequence de forme, heritee du patron des phases 3 a 5 : `APPELS_SUPPRESSION` refuse tout **appel** nomme
`remove`, `unlink`, `rmdir` ou `rmtree` — y compris dans ce module, qui s'auto-analyse. Une page est donc
rendue **absente** par `Path.rename` (elle sort de la decouverte `docs/*.md`), jamais par un appel de
suppression : une suppression litterale ferait rougir la garde de ce module sur une livraison conforme, ce
qui serait un defaut du module et non de la livraison.

Limites declarees (`D-85`), pour qu'aucune morsure ne soit lue au-dela de ce qu'elle mesure :

- la morsure est cherchee par **appartenance de sous-chaine** : le motif attendu doit apparaitre dans les
  constats produits. Elle prouve donc que le controle rougit **avec ce motif**, jamais que ce motif est la
  seule cause du rouge, ni que le constat appartient bien a la famille visee ;
- la suite entiere n'est pas rejouee ici (aucun sous-processus) : ce module prouve la morsure **au niveau
  des fonctions de controle** ; le rejeu complet, ses compteurs et ses durees vivent dans le rapport ;
- le rendu Markdown hors GitHub, la prose des pages et l'exhaustivite des derives non declarees restent
  hors d'atteinte, comme les modules d'ancrage le declarent deja.
"""

import ast
import importlib.util
import shutil
import sys
from pathlib import Path

import pytest

# --- Chemins (constantes de lecture, jamais ecrites hors de la copie) ---

RACINE_DEPOT = Path(__file__).resolve().parents[1]
DOSSIER_DOCS = "docs"
SOMMAIRE = "sommaire.md"

# Les trois modules d'ancrage dont ce module prouve les controles : jamais un quatrieme, jamais une
# reimplementation.
MODULES_ANCRAGE = (
    "test_docs_depannage.py",
    "test_docs_glossaire.py",
    "test_docs_completude.py",
)

# Les deux fichiers de documentation de la racine du depot. Ils sont copies **a la racine de la copie** :
# les controles qui les lisent resolvent depuis la racine, exactement comme dans le depot.
FICHIERS_HORS_DOCS = ("README.md", "GUIDE_WIZARD.md")

# Ce que la copie doit porter pour que les controles aient un objet : les trois dossiers lus par les
# modules d'ancrage (`dofus_stuff/` pour les littoraux du produit et les chemins de source, `tests/` pour
# les fixtures partagees et les lecteurs de page) et les fichiers de racine.
DOSSIERS_COPIES = ("docs", "tests", "dofus_stuff")
FICHIERS_COPIES = FICHIERS_HORS_DOCS + ("pyproject.toml",)

# Le dossier ou une page rendue absente est **deplacee** (jamais supprimee) : hors de `docs/`, donc hors de
# la decouverte `docs/*.md` et hors de la garde de suppression du module.
DOSSIER_RETIRES = "retires"

FAMILLE_PAGE_LIVREE = "page_livree"
# Les contrats de la phase qui se prouvent **sur la copie** : `(module d'ancrage, fonction de constats)`.
# La precondition (`test_la_copie_est_verte_avant_toute_mutation`) exige que **chacun** ne produise rien sur
# la copie intacte — c'est le meme patron que les plans 06-01 a 06-03, ou la copie est mesuree verte avant
# la mutation. Les sondes (dont le retour n'est pas une liste de constats) sont nommees a part.
CONTROLES_DE_LA_COPIE = (
    ("test_docs_completude.py", "problemes_pages_epinglees"),
    ("test_docs_completude.py", "problemes_couverture_index"),
    ("test_docs_completude.py", "problemes_readme"),
    ("test_docs_depannage.py", "problemes_messages"),
    ("test_docs_depannage.py", "problemes_rubriques"),
    ("test_docs_depannage.py", "problemes_page"),
    ("test_docs_depannage.py", "problemes_renvois"),
    ("test_docs_depannage.py", "problemes_budget"),
    ("test_docs_depannage.py", "problemes_clavier"),
    ("test_docs_depannage.py", "_produire"),
    ("test_docs_glossaire.py", "problemes_glossaire"),
    ("test_docs_glossaire.py", "problemes_page_glossaire"),
    ("test_docs_glossaire.py", "problemes_parcours"),
)

# Sondes : leur retour n'est pas une liste de constats, et elles signalent leur refus en levant. Une sonde
# qui rend sans lever est verte.
SONDES_DE_LA_COPIE = ("_produire",)

# --- Motifs portes par ce module ---
# Regle posee au plan 03-03 et tenue ici : un motif est porte par une constante ASCII du module, jamais
# ecrit en clair dans une ligne d'assertion — pytest reproduit la ligne source de l'`assert`, une valeur en
# clair y serait trouvee meme si aucun constat n'avait ete produit.
MOTIF_GARDE = "garde de cloture du harnais"
MOTIF_MUTATION_SANS_OBJET = "mutation sans objet"
MOTIF_COPIE_ROUGE = "copie rouge avant mutation"
MOTIF_MOTIF_INTROUVABLE = "motif attendu introuvable dans le module d'ancrage"
MOTIF_CONTROLE_INTROUVABLE = "controle introuvable dans la table des invocations"

# --- Garde de cloture du harnais (patron des phases 3 a 5, auto-analyse) ---
# Racines dont un import signalerait un risque reel : ouvrir la base, lancer un processus, ouvrir une
# socket, joindre le reseau. Ce module n'a besoin d'aucune des quatre : il copie des fichiers dans
# `tmp_path`, lit des octets et appelle des fonctions de constats.
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

# Noms d'appel dont la presence signalerait une suppression de fichier, l'execution du produit ou le
# lancement du solveur. Quatre noms de suppression : une page rendue absente par ce module l'est donc par
# `Path.rename`, jamais par un de ces appels.
APPELS_SUPPRESSION = ("remove", "unlink", "rmdir", "rmtree")
APPEL_PRODUIT = "main"
APPELS_CALCUL_PRODUIT = ("optimize_stuff", "_run_optimize_and_redirect")

# Les deux seuls points d'entree de l'interface qui visent la base locale ou le reseau : ce module ne les
# poste jamais, et aucun litteral de ces chemins neufs n'est ecrit ailleurs que dans cette constante.
CHEMINS_DESTRUCTIFS = ("/db/clear", "/db/sync")


# --- Lecture et ecriture de la copie ---


def _lire(chemin: Path) -> str:
    """Texte d'un fichier de la copie, lu en UTF-8 avec `newline=""` : les CRLF sont **preserves**.

    La lecture sans traduction des fins de ligne est la condition de la mesure : une mutation ecrite avec
    des LF ferait rougir les assertions de fins de ligne des modules d'ancrage, et la morsure serait
    confondue — deux causes, un seul motif (`06-RESEARCH.md` § D.4, `MOTIF_CRLF`).
    """
    with chemin.open("r", encoding="utf-8", newline="") as flux:
        return flux.read()


def _ecrire(chemin: Path, texte: str) -> None:
    """Ecrit le texte tel quel dans la copie, sans traduction de fins de ligne (voir `_lire`)."""
    with chemin.open("w", encoding="utf-8", newline="") as flux:
        flux.write(texte)


def _exiger_mutation(condition: bool, message: str) -> None:
    """Refuse une mutation **sans objet** : une ancre disparue laisserait la copie verte, et la morsure
    serait alors absente sans que rien ne le dise.

    C'est la garde de mesure du module : elle rend `MOTIF_MUTATION_SANS_OBJET` au lieu de laisser passer une
    mutation qui ne mesurerait plus rien (`06-RESEARCH.md` § D.4, « ancre absente : la mutation ne
    mesurerait rien »).
    """
    if not condition:
        raise AssertionError(f"{MOTIF_MUTATION_SANS_OBJET} : {message}")


def _remplacer(chemin: Path, ancre: str, derive: str) -> None:
    """Remplace une ancre **unique** d'un fichier de la copie ; refuse une ancre absente ou multiple."""
    texte = _lire(chemin)
    occurrences = texte.count(ancre)
    _exiger_mutation(
        occurrences == 1,
        f"l'ancre {ancre!r} figure {occurrences} fois dans {chemin.as_posix()} ; attendu exactement une",
    )
    _ecrire(chemin, texte.replace(ancre, derive, 1))


def _retirer_lignes(chemin: Path, predicat) -> None:
    """Retire les lignes qu'un predicat designe, et refuse une selection vide (voir `_exiger_mutation`)."""
    texte = _lire(chemin)
    lignes = texte.splitlines(keepends=True)
    restantes = [ligne for ligne in lignes if not predicat(ligne)]
    _exiger_mutation(
        len(restantes) < len(lignes),
        f"aucune ligne de {chemin.as_posix()} ne repond au predicat de la mutation",
    )
    _ecrire(chemin, "".join(restantes))


# --- Copie du depot, chargement des modules d'ancrage et redirection de leur racine ---

_COMPTEUR = 0


def _suivant(prefixe: str) -> str:
    """Nom **unique** par appel : un module recharge ne peut pas ecraser un module encore mesure, et
    chaque sonde ecrit dans son propre dossier sous `tmp_path`."""
    global _COMPTEUR
    _COMPTEUR += 1
    return f"{prefixe}{_COMPTEUR}"


def _charger_module(racine: Path, nom_fichier: str):
    """Charge un module de test **par chemin**, sous un nom unique prefixe `ancrage_`, et le retourne.

    Le chargement par chemin est ce qui permet d'exercer la **copie** : charge depuis la copie, le module y
    lit sa racine par sa propre constante (`Path(__file__).resolve().parents[1]`). Le nom est unique pour
    qu'un rechargement apres mutation ne se confonde pas avec la version precedente, et le module est
    inscrit dans `sys.modules` **avant** execution (les dataclasses et les fixtures le supposent).

    Aucune adaptation n'a ete necessaire sur les trois modules d'ancrage : leurs fonctions de constats
    lisent la racine depuis leur constante de module, jamais depuis une valeur capturee a l'import — c'est
    l'exigence de forme nommee par le plan, et si un module avait capture la racine, le constat se serait
    fait **dans ce module** (fichier de test, changement autorise et attendu).
    """
    chemin = racine / "tests" / nom_fichier
    nom = _suivant(f"ancrage_{Path(nom_fichier).stem}_")
    specification = importlib.util.spec_from_file_location(nom, chemin)
    module = importlib.util.module_from_spec(specification)
    sys.modules[nom] = module
    specification.loader.exec_module(module)
    return module


def _rediriger(module, copie: Path) -> None:
    """Pointe la racine lue par un module d'ancrage vers la copie (`D-97`).

    C'est la piece qui rend la mutation visible : les fonctions de constats lisent la racine de leur module
    (`RACINE_DEPOT`). Sans cette redirection, un controle lirait le depot reel, la mutation porterait sur une
    copie que personne ne lit, et la morsure serait un faux vert.
    """
    module.RACINE_DEPOT = copie


def _charger_modules(racine: Path) -> dict:
    """Les trois modules d'ancrage charges depuis `racine`, la racine qu'ils lisent redirigee vers elle."""
    modules = {}
    for nom_fichier in MODULES_ANCRAGE:
        module = _charger_module(racine, nom_fichier)
        _rediriger(module, racine)
        modules[nom_fichier] = module
    return modules


def _copie_du_depot(destination: Path) -> Path:
    """Copie de travail du depot sous `tmp_path` : `docs/`, `tests/`, `dofus_stuff/` et les fichiers lus.

    `dofus_stuff/` est copie parce que les controles de provenance y lisent des litteraux du produit et y
    resolvent les chemins cites par les blocs « Source de verite » ; `tests/` parce que les fixtures
    partagees et les lecteurs de page y vivent. `.data/` n'est **jamais** copie, et aucune base du depot
    n'est approchee par la batterie (la copie n'en construit aucune : les sondes du produit construisent les
    leurs sous `tmp_path`, `D-104`).
    """
    destination.mkdir(parents=True, exist_ok=True)
    for dossier in DOSSIERS_COPIES:
        shutil.copytree(
            RACINE_DEPOT / dossier,
            destination / dossier,
            ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
        )
    for nom in FICHIERS_COPIES:
        shutil.copy2(RACINE_DEPOT / nom, destination / nom)
    return destination


# --- Les mutations declarees : ecrites sur la **copie**, jamais sur le depot ---
# Chaque mutation est une fonction pure de la copie : elle lit et reecrit un fichier de la copie en
# preservant ses fins de ligne, et refuse (MOTIF_MUTATION_SANS_OBJET) si son ancre a disparu. Aucune n'est
# ecrite par un outil externe (`sed -i` retire les CR de ce poste, § D.4) : la mutation en Python garde les
# octets du reste du fichier.


def _mutation_page_renommee(copie: Path) -> None:
    """`docs/cli.md` sort de la decouverte par **renommage**, hors de `docs/` : jamais par suppression.

    Le renommage est la seule mise en absence compatible avec la garde de cloture de ce module
    (`APPELS_SUPPRESSION`) : la page n'est plus un fichier de `docs/`, donc la liste epinglee la declare
    absente, et la garde du harnais reste verte sur une livraison conforme.
    """
    source = copie / DOSSIER_DOCS / "cli.md"
    _exiger_mutation(source.is_file(), f"{source.as_posix()} est absent de la copie")
    retires = copie.parent / DOSSIER_RETIRES
    retires.mkdir(parents=True, exist_ok=True)
    source.rename(retires / "cli.md")


def _mutation_page_videe(copie: Path) -> None:
    """`docs/glossaire.md` est reduite a son titre : le seuil de lignes non vides n'est plus tenu."""
    chemin = copie / DOSSIER_DOCS / "glossaire.md"
    _exiger_mutation("# Glossaire\r\n" in _lire(chemin), f"{chemin.as_posix()} ne porte pas son titre")
    _ecrire(chemin, "# Glossaire\r\n")


# --- La table unique des derives declarees ---
# Six champs, lus par les constantes d'indice ci-dessous : famille, fichier cible, module d'ancrage, fonction
# de constats a appeler, mutation, motifs attendus (les **noms** des constantes du module d'ancrage).
F_FAMILLE, F_CIBLE, F_MODULE, F_FONCTION, F_MUTATION, F_MOTIFS = range(6)

FAMILLES = (
    (
        FAMILLE_PAGE_LIVREE,
        "docs/cli.md",
        "test_docs_completude.py",
        "problemes_pages_epinglees",
        _mutation_page_renommee,
        ("MOTIF_PAGE_ABSENTE",),
    ),
    (
        FAMILLE_PAGE_LIVREE,
        "docs/glossaire.md",
        "test_docs_completude.py",
        "problemes_pages_epinglees",
        _mutation_page_videe,
        ("MOTIF_PAGE_VIDE",),
    ),
)


# --- Invocations des controles sur la copie ---


def _controles(client, tmp_path: Path, sections, normalize, produites, rendus) -> dict:
    """Table unique des invocations : nom de la fonction de constats -> son appel sur la copie.

    Elle ne reimplemente rien : elle **fournit les arguments** des fonctions des modules d'ancrage, dont la
    racine est redirigee vers la copie (`_rediriger`). Les sondes du produit (`_produire`, `rendus`) sont
    celles du depot : le produit est le meme, la copie ne porte que des fichiers. Chaque sonde ecrit dans
    son propre dossier sous `tmp_path` (`_suivant`), donc deux mesures ne se heurtent pas.
    """

    def docs(copie: Path) -> Path:
        return copie / DOSSIER_DOCS

    return {
        "problemes_pages_epinglees": lambda module, copie: module.problemes_pages_epinglees(copie),
        "problemes_couverture_index": lambda module, copie: module.problemes_couverture_index(docs(copie)),
        "problemes_readme": lambda module, copie: module.problemes_readme(
            _lire(copie / "README.md"), module.INVOCATION_DESTRUCTIVE
        ),
        "problemes_messages": lambda module, copie: module.problemes_messages(
            docs(copie), produites, sections
        ),
        "problemes_rubriques": lambda module, copie: module.problemes_rubriques(docs(copie), sections),
        "problemes_page": lambda module, copie: module.problemes_page(docs(copie), sections, normalize),
        "problemes_renvois": lambda module, copie: module.problemes_renvois(docs(copie), sections),
        "problemes_budget": lambda module, copie: module.problemes_budget(
            docs(copie), sections, normalize
        ),
        "problemes_clavier": lambda module, copie: module.problemes_clavier(docs(copie), rendus, sections),
        "problemes_glossaire": lambda module, copie: module.problemes_glossaire(docs(copie), normalize),
        "problemes_page_glossaire": lambda module, copie: module.problemes_page_glossaire(docs(copie)),
        "problemes_parcours": lambda module, copie: module.problemes_parcours(
            _lire(docs(copie) / SOMMAIRE), normalize
        ),
        "_produire": lambda module, copie: module._produire(client, tmp_path / _suivant("sonde-")),
    }


def _sondes_du_produit(client, tmp_path: Path) -> tuple:
    """Sondes du produit, prises une fois : chaines produites et rendus des ecrans sans champ de saisie.

    Elles ne dependent pas de la copie — le produit est celui du depot, la copie ne porte que des fichiers —
    et les prendre une fois evite de rejouer le parcours de sondage du plan 06-01 a chaque famille.
    """
    depannage = _charger_module(RACINE_DEPOT, "test_docs_depannage.py")
    produites = depannage._produire(client, tmp_path / _suivant("sonde-"))
    rendus = depannage._rendus_sans_champ(client)
    return produites, rendus


def _mesure(derive, modules: dict, copie: Path, controles: dict) -> tuple:
    """Constats rendus par le controle de la famille, et texte de son refus s'il a refuse.

    Une sonde (`SONDES_DE_LA_COPIE`) signale son refus en levant : le refus est rendu comme un texte ou le
    motif attendu est cherche exactement comme dans un constat. Une declaration muette doit donc faire
    rougir le controle, jamais passer pour un vert.
    """
    nom_module, nom_fonction = derive[F_MODULE], derive[F_FONCTION]
    module = modules.get(nom_module)
    _exiger_mutation(module is not None, f"{MOTIF_CONTROLE_INTROUVABLE} : {nom_module} n'est pas charge")
    invocation = controles.get(nom_fonction)
    _exiger_mutation(
        invocation is not None,
        f"{MOTIF_CONTROLE_INTROUVABLE} : {nom_fonction} n'est pas dans la table des invocations",
    )
    try:
        rendus = invocation(module, copie)
    except AssertionError as refus:
        return [], str(refus)
    if nom_fonction in SONDES_DE_LA_COPIE:
        return [], ""
    return [str(constat) for constat in rendus or []], ""


def _appliquer(copie: Path, derive) -> None:
    """Applique la mutation de la derive sur la **copie** (jamais sur le depot)."""
    derive[F_MUTATION](copie)


def _motifs_attendus(derive, module) -> list:
    """Motifs attendus, **lus** dans le module d'ancrage par le nom de leur constante (`D-14`, `D-17`).

    Un motif recopie d'un module a l'autre serait une seconde source de verite : il resterait vert apres un
    renommage du constat dans le module d'ancrage. Un nom de constante introuvable est un constat
    (`MOTIF_MOTIF_INTROUVABLE`), jamais un motif vide.
    """
    attendus = []
    for nom in derive[F_MOTIFS]:
        _exiger_mutation(
            hasattr(module, nom),
            f"{MOTIF_MOTIF_INTROUVABLE} : {derive[F_MODULE]} ne porte pas la constante {nom}",
        )
        attendus.append(getattr(module, nom))
    return attendus


# --- Garde de cloture du harnais (auto-analysee par `ast`) ---


def _imports_du_module(arbre: ast.AST) -> set:
    """Modules importes par le module controle, imports imbriques compris dans les fonctions."""
    importes = set()
    for noeud in ast.walk(arbre):
        if isinstance(noeud, ast.Import):
            importes.update(alias.name for alias in noeud.names)
        elif isinstance(noeud, ast.ImportFrom) and noeud.module is not None:
            importes.add(noeud.module)
    return importes


def _appels_du_module(arbre: ast.AST) -> set:
    """Noms appeles par le module controle, sous forme `nom` ou `attribut` terminal."""
    appeles = set()
    for noeud in ast.walk(arbre):
        if not isinstance(noeud, ast.Call):
            continue
        if isinstance(noeud.func, ast.Attribute):
            appeles.add(noeud.func.attr)
        else:
            appeles.add(getattr(noeud.func, "id", ""))
    return appeles


def _litteraux_de_chemin_destructif(arbre: ast.AST) -> list:
    """Litteraux des deux chemins destructifs, **hors** de la constante qui les declare.

    Les deux chemins de `CHEMINS_DESTRUCTIFS` sont eux-memes des litteraux de ce module : ils sont
    identifies par l'affectation de la constante et exclus de la recherche, sans quoi la garde s'accuserait
    elle-meme. Tout **autre** litteral qui commence par l'un de ces deux chemins est un constat — que
    l'appel soit ecrit en clair ou que le chemin soit range dans une table de routes.
    """
    declares = set()
    for noeud in ast.walk(arbre):
        if not isinstance(noeud, ast.Assign):
            continue
        cibles = [cible for cible in noeud.targets if isinstance(cible, ast.Name)]
        if not any(cible.id == "CHEMINS_DESTRUCTIFS" for cible in cibles):
            continue
        declares.update(id(enfant) for enfant in ast.walk(noeud.value))
    fautifs = []
    for noeud in ast.walk(arbre):
        if not isinstance(noeud, ast.Constant) or not isinstance(noeud.value, str):
            continue
        if id(noeud) in declares:
            continue
        if noeud.value.startswith(CHEMINS_DESTRUCTIFS):
            fautifs.append((noeud.lineno, noeud.value))
    return fautifs


def test_garde_de_cloture_du_harnais() -> None:
    """Le module ne joint ni base, ni processus, ni socket, ni reseau, et ne supprime aucun fichier.

    La propriete est verifiee sur le texte de ce module par `ast`, jamais par une recherche de chaines : le
    module cite lui-meme les noms interdits dans ses messages et dans ses constantes, une recherche
    textuelle se detecterait elle-meme. Le controle porte sur le risque **reel** de ce module — copier des
    fichiers sous `tmp_path` et appeler des fonctions de constats : ouvrir une base, construire une base
    hors de `tmp_path`, lancer un processus, ouvrir une socket, joindre le reseau, supprimer un fichier,
    executer le produit, lancer le solveur, poster vers un chemin destructif.

    Limite nommee : c'est une demonstration **statique et indirecte**. Elle dit ce que ce module importe et
    appelle, pas ce qu'un autre chemin ferait ; la preuve que le depot n'a pas bouge est l'audit de
    perimetre et la comparaison d'empreinte de la tache 3 de ce plan, pas cette garde.
    """
    arbre = ast.parse(Path(__file__).read_text(encoding="utf-8"))
    importes = _imports_du_module(arbre)
    appeles = _appels_du_module(arbre)
    constats: list[str] = []

    racines = sorted(module for module in importes if module.split(".")[0] in RACINES_INTERDITES)
    if racines:
        constats.append(
            f"import(s) de base, de processus, de socket ou de reseau : {', '.join(racines)} ; attendu "
            f"aucun de ces imports dans la batterie de mutation, qui ne copie que des fichiers (GARD-04, "
            f"D-103)"
        )
    if APPEL_PRODUIT in appeles:
        constats.append(
            f"appel a {APPEL_PRODUIT}() dans la batterie de mutation ; attendu une batterie qui copie des "
            f"fichiers et appelle des fonctions de constats, le produit n'etant jamais execute (D-103)"
        )
    calculs = sorted(set(APPELS_CALCUL_PRODUIT) & appeles)
    if calculs:
        constats.append(
            f"appel(s) de calcul du produit : {', '.join(calculs)} ; attendu aucun lancement de solveur, "
            f"la batterie ne cedant jamais la main a un calcul (D-103)"
        )
    suppressions = sorted(set(APPELS_SUPPRESSION) & appeles)
    if suppressions:
        constats.append(
            f"appel(s) de suppression de fichier : {', '.join(suppressions)} ; attendu aucun appel "
            f"destructif : une page est rendue absente par un renommage, jamais supprimee (D-104)"
        )
    for ligne, chemin in _litteraux_de_chemin_destructif(arbre):
        constats.append(
            f"chemin destructif « {chemin} » porte ligne {ligne} ; attendu aucun litteral de ces deux "
            f"chemins hors de la constante qui les declare, ces deux points d'entree vidant la base locale "
            f"ou joignant le reseau (D-104)"
        )

    assert not constats, (
        f"test_docs_mutation.py : {MOTIF_GARDE} — constats : "
        + " ; ".join(constats)
        + " ; attendu une batterie qui copie le depot sous `tmp_path`, appelle les fonctions de constats des "
        "modules d'ancrage, ne joint ni base, ni processus, ni socket, ni reseau, et ne supprime rien "
        "(GARD-04, D-103, D-104)"
    )


# --- Les tests de la preuve ---


def test_la_copie_est_verte_avant_toute_mutation(tmp_path: Path, client, sections, normalize) -> None:
    """La copie **intacte** ne produit aucun constat sur les treize contrats de la phase (`D-97`).

    C'est la precondition de toute la batterie, et elle est elle-meme un test : une morsure sur une copie
    deja rouge ne prouverait rien, puisque le controle serait rouge avant comme apres la mutation. Tous les
    contrats de `CONTROLES_DE_LA_COPIE` sont appeles sur la **meme** copie intacte, la racine des modules
    d'ancrage etant redirigee vers elle. La copie porte `docs/`, `tests/`, `dofus_stuff/`, `README.md`,
    `GUIDE_WIZARD.md` et `pyproject.toml`, et rien d'autre du depot : aucune base, aucun dossier de donnees.
    """
    produites, rendus = _sondes_du_produit(client, tmp_path)
    controles = _controles(client, tmp_path, sections, normalize, produites, rendus)
    copie = _copie_du_depot(tmp_path / "copie-verte")
    modules = _charger_modules(copie)
    constats: list[str] = []

    for nom_module, nom_fonction in CONTROLES_DE_LA_COPIE:
        module = modules[nom_module]
        invocation = controles[nom_fonction]
        try:
            rendus_controle = invocation(module, copie)
        except AssertionError as refus:
            constats.append(f"{nom_module} :: {nom_fonction} — refus sur la copie intacte : {refus}")
            continue
        if nom_fonction in SONDES_DE_LA_COPIE:
            continue
        for constat in rendus_controle or []:
            constats.append(f"{nom_module} :: {nom_fonction} — {constat}")

    assert not constats, (
        f"copie de {copie.as_posix()} : {MOTIF_COPIE_ROUGE} — constats sur la copie intacte :\n"
        + "\n".join(constats)
        + " ; attendu une copie verte avant toute mutation, sans quoi aucune morsure ne serait "
        "discriminante (D-97, lecon des phases 3 a 5)"
    )


def test_chaque_derive_declenche_son_motif(tmp_path: Path, client, sections, normalize) -> None:
    """Chaque derive declaree est ecrite sur une copie fraiche et verte, et **son motif** est observe.

    Une copie par mutation : la morsure part toujours d'une copie **fraiche** dont le controle est mesure
    vert avant la mutation, sans quoi un constat deja present ferait passer une mutation inerte pour une
    morsure. Les motifs attendus sont lus dans le module d'ancrage (par le nom de leur constante), et un
    motif absent fait **echouer** la batterie en nommant la famille, le fichier cible, les motifs attendus et
    les constats **reellement** produits (`D-13`, `D-85`).

    Aucun `skip`, aucun `xfail` : une famille dont la morsure n'est pas observee est un defaut, jamais un
    avertissement discret. C'est l'objet meme de ce module.
    """
    produites, rendus = _sondes_du_produit(client, tmp_path)
    controles = _controles(client, tmp_path, sections, normalize, produites, rendus)
    manquantes: list[str] = []

    for derive in FAMILLES:
        famille = derive[F_FAMILLE]
        copie = _copie_du_depot(tmp_path / _suivant(f"copie-{famille}-"))
        modules = _charger_modules(copie)
        avant, refus_avant = _mesure(derive, modules, copie, controles)
        if avant or refus_avant:
            manquantes.append(
                f"{famille} ({derive[F_CIBLE]}) : {MOTIF_COPIE_ROUGE} — la copie fraiche n'est pas verte "
                f"avant mutation : " + " ; ".join(avant + [refus_avant]).strip(" ;")
            )
            continue

        _appliquer(copie, derive)
        modules = _charger_modules(copie)
        constats, refus = _mesure(derive, modules, copie, controles)
        attendus = _motifs_attendus(derive, modules[derive[F_MODULE]])
        absents = [
            motif
            for motif in attendus
            if not any(motif in constat for constat in constats) and motif not in refus
        ]
        if absents:
            manquantes.append(
                f"{famille} ({derive[F_CIBLE]}) : motif(s) attendu(s) absent(s) : {', '.join(absents)} ; "
                f"motifs lus dans {derive[F_MODULE]} ; constats reellement produits : "
                + (" ; ".join(constats) or refus or "aucun")
            )

    assert not manquantes, (
        "FAMILLES : morsure(s) non observee(s) sur une copie pourtant mesuree verte avant mutation :\n"
        + "\n".join(manquantes)
        + " ; attendu que chaque derive declaree fasse rougir le controle de son module d'ancrage avec son "
        "motif, la morsure etant cherchee par appartenance de sous-chaine dans les constats (GARD-04, D-97, "
        "D-98)"
    )

