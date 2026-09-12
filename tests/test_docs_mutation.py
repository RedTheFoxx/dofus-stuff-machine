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

Le **trou museliere** est traite au lieu d'etre note : l'ecran de sortie du produit (`GET /quit`) ne rend
aucun message et n'accepte pas `POST` (mesure de `06-RESEARCH.md` : 405, aucune ligne de statut). Une
derive qui pretendrait lui attribuer un message doit donc etre **refusee par la sonde** du module
d'ancrage (`message non produit par le code`) : c'est la mutation `ecran_muet_declare`, et c'est ce qui
ferme le trou par un controle plutot que par une phrase.

Limites declarees (`D-85`), pour qu'aucune morsure ne soit lue au-dela de ce qu'elle mesure :

- la morsure est cherchee par **appartenance de sous-chaine** : le motif attendu doit apparaitre dans les
  constats produits. Elle prouve donc que le controle rougit **avec ce motif**, jamais que ce motif est la
  seule cause du rouge, ni que le constat appartient bien a la famille visee ;
- les familles couvertes sont les **cinq familles declarees** dans `FAMILLES` : une derive hors de ces
  familles n'est pas demontree impossible, elle est couverte « autant que » par les gardes livrees ;
- la mutation d'un module d'ancrage (`ecran_muet_declare`) est prouvee en **rechargeant** le module depuis
  la copie ; la mutation d'un litteral du produit (`litteral_produit_renomme`) porte sur la copie de
  `dofus_stuff/`, jamais sur `dofus_stuff/**` du depot (`D-103`) ;
- la suite entiere n'est pas rejouee ici (aucun sous-processus) : ce module prouve la morsure **au niveau
  des fonctions de controle** ; le rejeu complet, ses compteurs et ses durees vivent dans le rapport ;
- le rendu Markdown hors GitHub, la prose des pages et l'exhaustivite des derives non declarees restent
  hors d'atteinte, comme les modules d'ancrage le declarent deja.
"""

import ast
import hashlib
import importlib.util
import re
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

# --- Familles de derive declarees ---
# Les cinq familles du plan. Chacune doit declarer au moins une mutation, sinon la batterie le dit
# (`MOTIF_COUVERTURE_MUTATION`) au lieu de laisser une famille muette.
FAMILLE_PAGE_LIVREE = "page_livree"
FAMILLE_INDEX_ET_PARCOURS = "index_et_parcours"
FAMILLE_MESSAGES = "messages_du_depannage"
FAMILLE_GLOSSAIRE = "glossaire"
FAMILLE_README = "readme"
FAMILLES_DECLAREES = (
    FAMILLE_PAGE_LIVREE,
    FAMILLE_INDEX_ET_PARCOURS,
    FAMILLE_MESSAGES,
    FAMILLE_GLOSSAIRE,
    FAMILLE_README,
)

# Les livrables de la phase qui doivent etre la cible d'au moins une mutation declaree : les quatre pages
# (les deux pages livrees, le sommaire qui les indexe, le README dont la commande de nettoyage est
# encadree) et le module d'ancrage des messages, dont la mutation `ecran_muet_declare` deplace une
# declaration de provenance.
LIVRABLES_DE_LA_PHASE = (
    "docs/depannage.md",
    "docs/glossaire.md",
    "docs/sommaire.md",
    "README.md",
    "tests/test_docs_depannage.py",
)

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

# --- Empreinte en lecture seule de la base du depot (`GARD-03`, `D-104`) ---
# La triple est **mesuree sur le disque** par l'executeur avant d'etre ecrite ici : rien n'est estime. La
# lecture passe par les octets (`read_bytes`) et `hashlib` : la base n'est **jamais** ouverte par SQLite,
# ce que la garde de cloture de ce module refuse par l'import et que la regle `D-104` interdit.
CHEMIN_BASE = ".data/dofus.sqlite3"
EMPREINTE_BASE = (
    24989696,
    1788730056843137500,
    "e3793d64cb7939ad1a51837b075b6b95e03d64c878fcb9cc07f86c00bb8fef7b",
)

# --- Motifs portes par ce module ---
# Regle posee au plan 03-03 et tenue ici : un motif est porte par une constante ASCII du module, jamais
# ecrit en clair dans une ligne d'assertion — pytest reproduit la ligne source de l'`assert`, une valeur en
# clair y serait trouvee meme si aucun constat n'avait ete produit.
MOTIF_GARDE = "garde de cloture du harnais"
MOTIF_MUTATION_SANS_OBJET = "mutation sans objet"
MOTIF_COPIE_ROUGE = "copie rouge avant mutation"
MOTIF_COUVERTURE_MUTATION = "livrable non couvert par une mutation"
MOTIF_EMPREINTE_BASE = "empreinte de la base du depot"
MOTIF_MOTIF_INTROUVABLE = "motif attendu introuvable dans le module d'ancrage"
MOTIF_FAMILLE_ABSENTE = "famille de derive absente de la table"
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

# Le motif de la ligne du tableau d'index dont la cible est le glossaire : la mutation retire **cette**
# ligne, jamais une ligne qui citerait la page par ailleurs.
MOTIF_LIGNE_INDEX_GLOSSAIRE = re.compile(r"^\|\s*\[[^\]]*\]\(glossaire\.md\)\s*\|")


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


def _mutation_index_retire(copie: Path) -> None:
    """La ligne du tableau d'index dont la cible est `glossaire.md` est retiree du sommaire."""
    _retirer_lignes(
        copie / DOSSIER_DOCS / SOMMAIRE,
        lambda ligne: bool(MOTIF_LIGNE_INDEX_GLOSSAIRE.match(ligne)),
    )


def _mutation_parcours_renomme(copie: Path) -> None:
    """L'entree numerotee du parcours qui reprend le libelle `Glossaire` est renommee.

    L'ancre est lue sur la page livree (mesure de l'ecriture) ; une page qui ne la porterait plus rendrait
    la mutation **sans objet**, et le refus serait nomme au lieu de laisser la copie verte.
    """
    _remplacer(
        copie / DOSSIER_DOCS / SOMMAIRE,
        "7. Glossaire\r\n",
        "7. Glossaire detaille\r\n",
    )


def _mutation_parcours_en_lien(copie: Path) -> None:
    """Une entree numerotee du parcours est convertie en lien Markdown.

    Cette forme est refusee par decision de plan (`D-05`, `D-95`) : tout lien du sommaire est lu comme une
    entree d'index par les gardes de structure, donc le parcours conseille est du texte simple.
    """
    _remplacer(
        copie / DOSSIER_DOCS / SOMMAIRE,
        "1. Installation\r\n",
        "1. [Installation](installation.md)\r\n",
    )


def _mutation_message_retire(copie: Path) -> None:
    """La ligne du message de saisie requise est retiree de la rubrique qui le cite."""
    _retirer_lignes(
        copie / DOSSIER_DOCS / "depannage.md",
        lambda ligne: ligne.startswith("| `SAISIE REQUISE`"),
    )


def _mutation_message_non_declare(copie: Path) -> None:
    """Une ligne de message non declare est inseree dans la rubrique de la base, donc **citee** par elle."""
    chemin = copie / DOSSIER_DOCS / "depannage.md"
    ancre = "## Saisie invalide\r\n"
    ligne = (
        "| `MESSAGE INEXISTANT DU PRODUIT` | interface web, ligne de statut | "
        "aucun geste : ce message n'est produit par aucune surface |\r\n"
    )
    texte = _lire(chemin)
    _exiger_mutation(
        texte.count(ancre) == 1,
        f"l'ancre {ancre!r} figure {texte.count(ancre)} fois dans {chemin.as_posix()}",
    )
    _ecrire(chemin, texte.replace(ancre, f"{ligne}\r\n{ancre}", 1))


def _mutation_litteral_produit(copie: Path) -> None:
    """Le litteral du message de base vide est renomme dans la **copie** de `dofus_stuff/sync.py`.

    La page ne bouge pas : c'est le **produit** qui derive, et le controle de provenance doit rougir
    (`source_literal`). `dofus_stuff/**` du depot reste intact (`D-103`) : seul le fichier de la copie est
    mute.
    """
    _remplacer(
        copie / "dofus_stuff" / "sync.py",
        "Base locale vide et --offline : impossible de synchroniser",
        "Base locale vide, synchronisation impossible",
    )


def _mutation_ecran_muet_declare(copie: Path) -> None:
    """Le message d'attente de la ligne de commande est declare **rendu** par l'interface web.

    L'ecran de sortie du produit (`GET /quit`) ne rend aucun message et n'accepte pas `POST` (mesure de
    `06-RESEARCH.md` : 405, aucune ligne de statut) : la declaration affirme donc un rendu qu'aucune sonde
    n'observe, et la sonde du module d'ancrage doit **refuser** (`message non produit par le code`). C'est
    la mecanisation du trou museliere : une declaration que le produit ne produit pas est un constat,
    jamais un vert muet.
    """
    _remplacer(
        copie / "tests" / "test_docs_depannage.py",
        '("Calcul en cours (CP-SAT)…", "calcul", "source_literal", SOURCE_CLI),',
        '("Calcul en cours (CP-SAT)…", "calcul", "web_render", None),',
    )


def _mutation_terme_retire(copie: Path) -> None:
    """La ligne du terme `bouclier` est retiree du tableau des termes : le contrat n'est plus tenu."""
    chemin = copie / DOSSIER_DOCS / "glossaire.md"
    _exiger_mutation(
        "| `bouclier` |" in _lire(chemin),
        f"la ligne du terme « bouclier » est absente de {chemin.as_posix()}",
    )
    _retirer_lignes(chemin, lambda ligne: ligne.startswith("| `bouclier` |"))


def _mutation_employeur_non_employeur(copie: Path) -> None:
    """L'employeur de `panoplie` pointe, page **et** declaration, vers un fichier qui ne l'emploie pas.

    La page est mutee d'abord (la cellule « Employe par » de la ligne du terme), puis la declaration du
    module d'ancrage dans la copie de `tests/` : le controle confronte la page a sa declaration **avant** de
    confronter la declaration au fichier, donc sans les deux mutations le constat serait celui d'une
    citation qui ne correspond plus, et non celui du chemin qui n'emploie pas le terme. Le fichier choisi
    (`dofus_stuff/sync.py`) existe reellement et n'emploie pas le terme (mesure).
    """
    _remplacer(
        copie / DOSSIER_DOCS / "glossaire.md",
        "`dofus_stuff/catalog.py`",
        "`dofus_stuff/sync.py`",
    )
    _remplacer(
        copie / "tests" / "test_docs_glossaire.py",
        '("panoplie", "dofus_stuff/catalog.py", "base-locale.md"),',
        '("panoplie", "dofus_stuff/sync.py", "base-locale.md"),',
    )


def _mutation_readme_renvoi_retire(copie: Path) -> None:
    """Les lignes du README qui portent le renvoi vers la page de la base locale sont retirees."""
    _retirer_lignes(copie / "README.md", lambda ligne: "docs/base-locale.md" in ligne)


def _mutation_readme_avertissement_retire(copie: Path) -> None:
    """Le mot d'avertissement du bloc de la commande de nettoyage est remplace par un mot neutre."""
    chemin = copie / "README.md"
    texte = _lire(chemin)
    _exiger_mutation(
        "détruit" in texte and "irréversible" in texte,
        f"le mot d'avertissement est absent de {chemin.as_posix()}",
    )
    _ecrire(chemin, texte.replace("détruit", "vidée").replace("irréversible", "réversible"))


def _mutation_readme_commande_disparue(copie: Path) -> None:
    """La ligne de la commande de nettoyage est retiree : l'information cesse d'etre documentee."""
    _retirer_lignes(copie / "README.md", lambda ligne: "python fetcher.py db clear" in ligne)


# --- La table unique des derives declarees ---
# Six champs, lus par les constantes d'indice ci-dessous : famille, fichier cible, module d'ancrage, fonction
# de constats a appeler, mutation, motifs attendus (les **noms** des constantes du module d'ancrage).
F_FAMILLE, F_CIBLE, F_MODULE, F_FONCTION, F_MUTATION, F_MOTIFS = range(6)

FAMILLES = (
    # (1) Page livree : la page disparait de la decouverte, puis la page est videe.
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
    # (2) Index et parcours : la ligne d'index disparait, le libelle du parcours derive, la forme en lien.
    (
        FAMILLE_INDEX_ET_PARCOURS,
        "docs/sommaire.md",
        "test_docs_completude.py",
        "problemes_couverture_index",
        _mutation_index_retire,
        ("MOTIF_COUVERTURE_INDEX",),
    ),
    (
        FAMILLE_INDEX_ET_PARCOURS,
        "docs/sommaire.md",
        "test_docs_glossaire.py",
        "problemes_parcours",
        _mutation_parcours_renomme,
        ("MOTIF_PARCOURS",),
    ),
    (
        FAMILLE_INDEX_ET_PARCOURS,
        "docs/sommaire.md",
        "test_docs_glossaire.py",
        "problemes_parcours",
        _mutation_parcours_en_lien,
        ("MOTIF_PARCOURS_LIEN",),
    ),
    # (3) Messages du depannage : ligne retiree, message non declare ajoute, litteral du produit renomme,
    #     et le trou museliere (une declaration de rendu que le produit ne produit pas).
    (
        FAMILLE_MESSAGES,
        "docs/depannage.md",
        "test_docs_depannage.py",
        "problemes_messages",
        _mutation_message_retire,
        ("MOTIF_MESSAGE_ABSENT",),
    ),
    (
        FAMILLE_MESSAGES,
        "docs/depannage.md",
        "test_docs_depannage.py",
        "problemes_messages",
        _mutation_message_non_declare,
        ("MOTIF_MESSAGE_INVENTE",),
    ),
    (
        FAMILLE_MESSAGES,
        "dofus_stuff/sync.py",
        "test_docs_depannage.py",
        "problemes_messages",
        _mutation_litteral_produit,
        ("MOTIF_MESSAGE_NON_PRODUIT",),
    ),
    (
        FAMILLE_MESSAGES,
        "tests/test_docs_depannage.py",
        "test_docs_depannage.py",
        "_produire",
        _mutation_ecran_muet_declare,
        ("MOTIF_MESSAGE_NON_PRODUIT",),
    ),
    # (4) Glossaire : terme retire, employeur qui n'emploie pas le terme.
    (
        FAMILLE_GLOSSAIRE,
        "docs/glossaire.md",
        "test_docs_glossaire.py",
        "problemes_glossaire",
        _mutation_terme_retire,
        ("MOTIF_TERME_ABSENT",),
    ),
    (
        FAMILLE_GLOSSAIRE,
        "docs/glossaire.md",
        "test_docs_glossaire.py",
        "problemes_glossaire",
        _mutation_employeur_non_employeur,
        ("MOTIF_EMPLOYEUR",),
    ),
    # (5) README : renvoi retire, avertissement retire, occurrence de la commande disparue. Les trois
    #     mutations portent le motif du controle **et** la famille de constat qu'elles prouvent.
    (
        FAMILLE_README,
        "README.md",
        "test_docs_completude.py",
        "problemes_readme",
        _mutation_readme_renvoi_retire,
        ("MOTIF_README", "FAMILLE_RENVOI"),
    ),
    (
        FAMILLE_README,
        "README.md",
        "test_docs_completude.py",
        "problemes_readme",
        _mutation_readme_avertissement_retire,
        ("MOTIF_README", "FAMILLE_AVERTISSEMENT"),
    ),
    (
        FAMILLE_README,
        "README.md",
        "test_docs_completude.py",
        "problemes_readme",
        _mutation_readme_commande_disparue,
        ("MOTIF_README", "FAMILLE_DISPARITION"),
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


def test_les_familles_declarent_leurs_mutations() -> None:
    """Les cinq familles sont declarees, chacune avec au moins une mutation complete (`D-97`).

    Une famille declaree sans mutation, ou une entree a qui manquerait son module d'ancrage, son fichier
    cible, sa mutation ou son motif attendu, est un constat portant `livrable non couvert par une mutation`
    — jamais un silence : c'est exactement ainsi qu'une famille muette passerait pour une famille prouvee.
    """
    constats: list[str] = []
    familles = {derive[F_FAMILLE] for derive in FAMILLES}

    for nom in FAMILLES_DECLAREES:
        if nom not in familles:
            constats.append(
                f"{MOTIF_FAMILLE_ABSENTE} : « {nom} » n'est declaree par aucune entree de FAMILLES ; "
                f"attendu que les cinq familles du plan y figurent (D-97)"
            )
    for nom in sorted(familles - set(FAMILLES_DECLAREES)):
        constats.append(
            f"{MOTIF_FAMILLE_ABSENTE} : « {nom} » figure dans FAMILLES sans etre une famille declaree du "
            f"plan ; attendu une famille de derive connue, jamais une famille inventee (D-85)"
        )
    for nom in FAMILLES_DECLAREES:
        if not [derive for derive in FAMILLES if derive[F_FAMILLE] == nom]:
            constats.append(
                f"{MOTIF_COUVERTURE_MUTATION} : la famille « {nom} » ne porte aucune mutation ; attendu au "
                f"moins une derive ecrite sur la copie et un motif attendu (D-97)"
            )
    for derive in FAMILLES:
        champs = (
            (F_CIBLE, "fichier cible"),
            (F_MODULE, "module d'ancrage"),
            (F_FONCTION, "fonction de constats"),
            (F_MOTIFS, "motifs attendus"),
        )
        manquants = [libelle for index, libelle in champs if not derive[index]]
        if not callable(derive[F_MUTATION]):
            manquants.append("mutation")
        if derive[F_MODULE] and derive[F_MODULE] not in MODULES_ANCRAGE:
            manquants.append("module d'ancrage hors des trois modules de la phase")
        if manquants:
            constats.append(
                f"{MOTIF_COUVERTURE_MUTATION} : l'entree de la famille « {derive[F_FAMILLE]} » sur "
                f"{derive[F_CIBLE]} ne porte pas {', '.join(manquants)} ; attendu chaque entree complete, "
                f"sans quoi la mutation ne mesurerait rien (D-97)"
            )

    assert not constats, (
        f"FAMILLES : {MOTIF_COUVERTURE_MUTATION} — constats : "
        + " ; ".join(constats)
        + " ; attendu les cinq familles de derive du plan, chacune portant au moins une mutation complete "
        "(fichier cible, module d'ancrage, fonction de constats, mutation, motifs attendus) (GARD-04, D-97)"
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


def test_la_base_du_depot_est_intacte() -> None:
    """La base du depot est lue en **octets** et garde sa taille, son `mtime_ns` et son SHA-256.

    Aucune ouverture par SQLite : l'import de `sqlite3` est refuse par la garde de cloture, donc la regle
    `D-104` et le controle sont coherents. Le constat nomme les **trois** valeurs attendues et les trois
    valeurs lues, jamais une seule : un SHA-256 seul laisserait passer une base reecrite a l'identique, et
    une taille seule ne verrait rien du contenu. L'empreinte de reference vient du disque (mesuree par
    l'executeur avant d'etre ecrite ici), jamais d'une estimation.
    """
    chemin = RACINE_DEPOT / CHEMIN_BASE
    if not chemin.is_file():
        raise AssertionError(
            f"{CHEMIN_BASE} : {MOTIF_EMPREINTE_BASE} — base absente ({chemin.as_posix()}) ; attendu la "
            f"base locale du depot, presente au debut de la phase et jamais approchee par la batterie "
            f"(GARD-03, D-104)"
        )

    octets = chemin.read_bytes()
    lues = (len(octets), chemin.stat().st_mtime_ns, hashlib.sha256(octets).hexdigest())
    attendues = EMPREINTE_BASE
    assert lues == attendues, (
        f"{CHEMIN_BASE} : {MOTIF_EMPREINTE_BASE} — valeurs lues (taille, mtime_ns, sha256) : "
        f"{lues[0]}, {lues[1]}, {lues[2]} ; valeurs attendues : {attendues[0]}, {attendues[1]}, "
        f"{attendues[2]} ; attendu une base du depot intacte, lue en octets et jamais ouverte par SQLite "
        f"(GARD-03, D-104)"
    )


def test_chaque_livrable_est_couvert_par_une_mutation() -> None:
    """Chaque livrable de la phase est la cible d'au moins une mutation declaree (critere 4).

    C'est la mecanisation de la formule du critere : « chaque page livree est prouvee durable par une
    mutation reelle ». La liste des cibles est **derivee** de `FAMILLES`, jamais ecrite une seconde fois —
    la table est la seule source du contrat — et un livrable sans mutation est un constat nomme
    (`MOTIF_COUVERTURE_MUTATION`), jamais un silence.
    """
    cibles = {derive[F_CIBLE] for derive in FAMILLES}
    manquants = sorted(set(LIVRABLES_DE_LA_PHASE) - cibles)
    assert not manquants, (
        f"{MOTIF_COUVERTURE_MUTATION} : {', '.join(manquants)} ; attendu une mutation declaree dans FAMILLES "
        f"pour chaque livrable de la phase, la preuve du critere 4 portant sur les derives reelles de ces "
        f"fichiers (GARD-04, D-97)"
    )

