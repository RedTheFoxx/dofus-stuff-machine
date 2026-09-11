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

Etat attendu pendant la phase : `test_aiguillage_sans_renvoi_obsolete` est **ROUGE** tant que
l'aiguillage livre `GUIDE_WIZARD.md` n'a pas ete corrige (plan 04-03, vague 4). C'est la preuve du
critere 5 dans son etat rouge (D-59a) — le detecteur est ecrit **et lance alors que le fichier est
encore obsolete** — et jamais une regression : le plan 04-04 ne corrige pas ce fichier, et la copie
figee `tests/fixtures/guide-wizard-obsolete.md` rend ce rouge relancable apres la correction.
"""

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

# Contrat de titres de la page : chaque titre est ecrit au caractere pres, le helper `section` de
# `tests/conftest.py` ne normalisant pas un titre. La constante compte les sections de ce plan et
# reste en accord exact avec la page a la fin de chaque tache : le plan 04-02 la complete, tache par
# tache, avec les sections qu'il cree — jamais un titre epingle sans sa section, sinon la morsure du
# controle de forme serait indiscernable d'une derive. Les titres sont nommes un a un, puis rassembles
# dans l'ordre du document : l'insertion d'une section ne peut donc pas decaler silencieusement la
# constante d'une autre.
TITRE_ARRIVEE = "## Arriver au wizard"
TITRE_ETAPES = "## Les 9 étapes du wizard"
TITRE_SLOTS = "## Slots et filtres"
TITRE_OPTIONS = "## Les 11 options du solveur"
TITRE_NOMBRES = "## Les quatre nombres d'une ligne"
TITRE_ITEMS = "## Interdire, forcer, retirer un objet"
TITRE_TOUCHES = "## Touches et commandes"
TITRE_EXEMPLE = "## Exemple guidé"
TITRE_SOURCE = "## Source de vérité"

TITRES_SECTION_ATTENDUS = (
    TITRE_ARRIVEE,
    TITRE_ETAPES,
    TITRE_SLOTS,
    TITRE_OPTIONS,
    TITRE_NOMBRES,
    TITRE_ITEMS,
    TITRE_TOUCHES,
    TITRE_EXEMPLE,
    TITRE_SOURCE,
)

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

# Lignes rendues des onze options du solveur (`optimize_wizard.py`) : numero, libelle, valeur.
MOTIF_OPTION_RENDUE = re.compile(
    r"^(?P<numero>\d{1,2})\.\s+(?P<libelle>.+?)\s*=\s*(?P<valeur>.*)$"
)

# Lignes rendues des listes d'objets : les quatre lignes de syntaxe et les deux listes, avec leur
# compte d'entrees et leur contenu.
MOTIF_SYNTAXE_RENDUE = re.compile(r"^\s*(?P<prefixe>\+ID|-ID|!ID|CLEAR)\s+(?P<verbe>.+?)\s*$")
MOTIF_LISTE_RENDUE = re.compile(
    r"^(?P<nom>INTERDITS|FORCES)\s*\((?P<compte>\d+)\)\s*:\s*(?P<contenu>.*)$"
)

# Invites et rappels des ecrans des options et des items, lus au rendu et jamais ecrits de memoire.
MOTIF_INVITE_OPTIONS = re.compile(r"^OPTIONS \(N=EDIT\) :$")
MOTIF_RAPPEL_OPTIONS = re.compile(r"^N=CHOISIR OPTION$")

# Ligne de tableau de la page citant une option : meme forme que celle d'un emplacement, un numero
# puis un libelle backtique.
MOTIF_LIGNE_OPTION = MOTIF_LIGNE_EMPLACEMENT

# Ligne de tableau de la page citant un ecran et sa forme d'edition, ou une saisie d'items et son
# verbe : la cle n'est pas un numero, elle est donc lue comme texte backtique.
MOTIF_LIGNE_FORMAT = re.compile(
    r"^\|\s*`(?P<cle>[^`]+)`\s*\|\s*`(?P<libelle>[^`]+)`\s*\|\s*$"
)
MOTIF_LIGNE_SYNTAXE_ITEMS = MOTIF_LIGNE_FORMAT

# Ligne de tableau de la page associant une etape a l'identifiant de son ecran :
# `| 1. `slots` | `OPT-W1` |`, tel que la ligne d'en-tete le rend (`dofus_stuff/web/routes.py`).
MOTIF_LIGNE_IDENTIFIANT = re.compile(
    r"^\|\s*(?P<numero>\d{1,2})\.\s*`(?P<etape>[a-z]+)`\s*"
    r"\|\s*`(?P<identifiant>OPT-W[A-Z0-9]+)`\s*\|\s*$"
)

# Lignes du parcours d'arrivee, lues au rendu et jamais ecrites de memoire : la ligne du menu
# principal qui ouvre l'optimisation, la ligne `AVANCE` proposee par les trois questions, et les
# trois questions elles-memes (`1/3`, `2/3`, `3/3`).
MOTIF_LIGNE_MENU = re.compile(r"^\s*(?P<numero>\d)\.\s+(?P<libelle>OPTIMISATION.*?)\s*$")
MOTIF_LIGNE_AVANCE = re.compile(r"^(?P<mot>AVANCE)\s*:\s*(?P<libelle>.+?)\s*$")
MOTIF_LIGNE_QUESTION = re.compile(r"^(?P<rang>[1-3])/3\s*-\s*(?P<question>.+?)\s*$")

# Ligne de tableau de la page associant une etape a ses trois couples touche/libelle :
# `| 1. `SLOTS ET FILTRES` (`slots`) | `Page prec` | `Suivant` | `Retour` |`, tel que la barre de
# raccourcis le rend (`dofus_stuff/web/routes.py:137-141`).
MOTIF_LIGNE_TOUCHES = re.compile(
    r"^\|\s*(?P<numero>\d{1,2})\.\s*`(?P<titre>[^`]+)`\s*\(`(?P<etape>[a-z]+)`\)\s*"
    r"\|\s*`(?P<f7>[^`]+)`\s*\|\s*`(?P<f8>[^`]+)`\s*\|\s*`(?P<esc>[^`]+)`\s*\|\s*$"
)

# Commandes annoncees par le corps du recapitulatif (`GO = LANCER`, `RESET = REINITIALISER`,
# `1-8 = RETOUR ECRAN`, `SAVES = STUFFS SAUVEGARDES`) et la forme sous laquelle la page les cite.
# Les couples d'une meme ligne rendue sont separes par au moins deux espaces
# (`dofus_stuff/web/optimize_wizard.py`, `body_recap`) : la decoupe suit ce separateur mesure, jamais
# une position fixe.
MOTIF_COMMANDE_RENDUE = re.compile(r"^(?P<cle>\S+)\s=\s(?P<verbe>.+)$")
MOTIF_COMMANDE_CITEE = re.compile(r"`(?P<cle>[A-Z0-9-]+) = (?P<verbe>[^`]+)`")
SEPARATEUR_COMMANDES = re.compile(r"\s{2,}")

# Jeton d'une commande destructrice, interdit dans un parcours recommande (D-22/D-23, D-61) : l'exemple
# guide migre n'en contient aucun. Le motif est celui deja employe par la garde de la page
# d'installation (`tests/test_docs_structure.py`), repris ici pour la seule section de l'exemple.
COMMANDE_DESTRUCTRICE = re.compile(r"\bdb\s+clear\b")

# Base locale du depot : lue pour y prendre une empreinte, jamais modifiee (T-04-08). La mesure locale
# de ce module est nommee pour ce qu'elle mesure : `tests/conftest.py` construit sa propre base sous
# `tmp_path/data`, aucun test de la suite n'ouvre ce chemin, donc cette re-mesure ne peut pas detecter
# une ecriture faite par un autre module. Le controle qui possede ce pouvoir est la mesure avant/apres
# autour de la suite entiere, executee par la verification du plan.
BASE_LOCALE = (".data", "dofus.sqlite3")
MOTIF_BASE_ABSENTE = "base locale absente : la mesure d'empreinte n'a pas d'objet"
MOTIF_EMPREINTE_CHANGEE = "empreinte de la base locale changee"

# Etat vide cite par la page, lu a cote de la phrase qui le porte.
MOTIF_ETAT_VIDE_CITE = re.compile(r"l'état vide `(?P<etat>\([^`]+\))`")

# Champ de saisie de la coquille, lu **dans la balise du champ** : une recherche libre de
# `maxlength="..."` trouverait d'abord une autre balise du document.
MOTIF_CHAMP_SAISIE = re.compile(r'<input class="field"(?P<attributs>[^>]*)>', re.S)
MOTIF_ATTRIBUT_CHAMP = re.compile(r'(?P<nom>[a-z-]+)="(?P<valeur>[^"]*)"')

# Chemin de code cite entre accents graves, et forme du document entier, reprises du patron de la
# phase 3 : une page qui cite un chemin doit citer un chemin qui existe.
CHEMIN_CITE = re.compile(r"`(?P<chemin>[\w./-]+\.(?:py|toml|js|md|json|sql))`")
BOM_UTF8 = b"\xef\xbb\xbf"
FRAGMENT_H1 = "# "
FRAGMENT_LIEN_EXTERNE = "](http"
LIGNE_RETOUR = "[Retour au sommaire](sommaire.md)"
BALISE_COMMANDE = "```console"

# Motif de morsure porte par une constante de module et jamais ecrit en clair dans la ligne
# d'assertion (regle posee au plan 03-03, tache 2) : pytest reproduit cette ligne dans sa sortie, et
# une valeur ecrite en clair y serait trouvee sans qu'aucun message n'ait ete produit.
MOTIF_ORDRE_ETAPES = "ordre de WIZARD_STEPS"
MOTIF_ARRIVEE = "arrivee du wizard"
MOTIF_IDENTIFIANT_ECRAN = "identifiant d'ecran"
MOTIF_EXEMPLE = "exemple guide"
MOTIF_TOUCHE = "couple touche/libelle"
MOTIF_COMMANDE_RECAP = "commande du recapitulatif"
MOTIF_COMMANDE_NUMERIQUE = "commande numerique"

# ---------------------------------------------------------------------------------------------
# Detecteur de renvois obsoletes (D-58, WIZ-03) — critere 5 de la phase 4.
#
# Trois formes nommees, et rien d'autre : (a) un renvoi au menu principal qui ne correspond pas au
# menu rendu, (b) un renvoi de filtre inverse (`F7` presente comme les armes a distance), (c) une
# arrivee « directe » dans le wizard. Chaque constat porte son motif en tete ; les tests de morsure
# cherchent la chaine du motif, jamais une phrase ecrite en clair dans la ligne d'assertion (meme
# regle que les motifs ci-dessus).
MOTIF_RENVOI_MENU = "renvoi obsolete (a)"
MOTIF_RENVOI_FILTRE = "renvoi obsolete (b)"
MOTIF_RENVOI_ARRIVEE = "renvoi obsolete (c)"
MOTIFS_RENVOI = (MOTIF_RENVOI_MENU, MOTIF_RENVOI_FILTRE, MOTIF_RENVOI_ARRIVEE)

# Copie figee des extraits obsoletes (D-59b) : un artefact de `tests/`, jamais une page de `docs/`.
FIXTURE_OBSOLETE = ("tests", "fixtures", "guide-wizard-obsolete.md")

# Limite honnete (D-58/D-26), ecrite dans le module **et** dans les messages : ce que le controle ne
# couvre pas est nomme, jamais passe sous silence. L'enonce produit est « le detecteur ne signale
# rien sur l'aiguillage corrige », jamais « plus aucun renvoi obsolete n'existe ».
LIMITE_HONNETE = (
    "le detecteur couvre trois formes nommees (un renvoi au menu principal, un renvoi de filtre "
    "inverse, une arrivee directe dans le wizard) et ne revendique aucune exhaustivite : une autre "
    "inversion, hors de ces trois formes, ne fera pas echouer la suite ; l'enonce produit est « le "
    "detecteur ne signale rien sur l'aiguillage corrige », jamais « plus aucun renvoi obsolete "
    "n'existe » (D-58, arbitrage D-26)"
)

# Jeton de menu `N. LIBELLE`, cherche **n'importe ou** dans la ligne : les trois occurrences reelles
# du fichier sont en tete de ligne (l'arbre), en gras (`**4. SYSTEME**`) et entre accents graves, donc
# une prise limitee au debut de ligne en manquerait deux sur trois.
MOTIF_JETON_MENU = re.compile(r"(?P<numero>\d)\.\s+(?P<libelle>[A-Z]['A-Z /-]{2,})")
MOTIF_LIGNE_MENU_RENDU = re.compile(r"^\s*(?P<numero>\d)\.\s+(?P<libelle>.+?)\s*$")
MOTIF_INVITATION = re.compile(r"(?i)\b(tapez|saisissez)\b")
MOTIF_NUMERO_CITE = re.compile(r"`(?P<numero>\d)`")
RACINE_OPTIMISATION = re.compile(r"(?i)optimisation")
MOTIF_TOUCHE_FILTRE = re.compile(r"F(?P<numero>[67])")
MOTIF_NEGATION = re.compile(r"\bpas\b|\bjamais\b|\bne\b|n['\u2019]")

# Mots-outils ecartes de la comparaison d'appartenance : aucun ne designe un menu.
MOTS_OUTILS = frozenset({"LISTE", "DES", "DE", "LA", "LE", "LES"})

# Signes d'arme a distance et d'arrivee, compares sur une ligne sans accents et en minuscules.
RACINES_DISTANCE = ("distance", "melee")
RACINES_ARRIVEE = ("arriv", "atterriss")
MARQUES_IMMEDIATETE = ("direct", "sans passer", "sans etape")

# Temoins legitimes du controle anti-faux-positif (D-60) : le texte corrige type que le plan 04-03
# ecrira, une phrase de filtre qui nomme sa touche **et** son libelle rendu, une phrase negative sur
# l'arrivee, et un renvoi en prose ordinaire. Un detecteur qui crie au loup sur ces quatre textes
# serait pire que pas de detecteur.
TEMOIN_AIGUILLAGE_CORRIGE = (
    "# Guide du Wizard (deplace)\n"
    "\n"
    "Le contenu de ce guide vit desormais dans `docs/wizard-avance.md`.\n"
    "\n"
    "```\n"
    "1. RECHERCHE D'OBJETS\n"
    "2. LISTE DES EQUIPEMENTS\n"
    "3. PANOPLIES\n"
    "\n"
    "4. OPTIMISATION\n"
    "5. SYSTEME\n"
    "```\n"
    "\n"
    "Tapez `4` puis Entrée pour ouvrir l'optimisation.\n"
)
TEMOIN_PHRASE_FILTRE_CORRIGEE = (
    "La touche `F7` retire les armes de mêlée du calcul ; le libellé rendu est ARMES MELEE.\n"
)
TEMOIN_PHRASE_NEGATIVE = (
    "Le parcours ne vous amène pas directement dans le wizard : il passe par les trois questions.\n"
)
TEMOIN_RENVOI_EN_PROSE = (
    "Pour revenir au menu principal, appuyez sur `ESC` ; le wizard avancé est décrit dans la page "
    "`docs/wizard-avance.md`.\n"
)
TEMOINS_LEGITIMES = (
    ("aiguillage corrige", TEMOIN_AIGUILLAGE_CORRIGE),
    ("phrase de filtre corrigee", TEMOIN_PHRASE_FILTRE_CORRIGEE),
    ("phrase negative sur l'arrivee", TEMOIN_PHRASE_NEGATIVE),
    ("renvoi en prose ordinaire", TEMOIN_RENVOI_EN_PROSE),
)

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


def _sans_accents(texte: str) -> str:
    """Texte prive de ses accents, casse conservee (les comparaisons passent en minuscules).

    `renvois_obsoletes` doit rester **pure** : elle ne peut donc pas recevoir la fixture `normalize`
    de `tests/conftest.py` et porte sa propre reduction, comme ce module le fait deja pour ses
    comparaisons internes (D-11).
    """
    decompose = unicodedata.normalize("NFKD", texte)
    return "".join(caractere for caractere in decompose if not unicodedata.combining(caractere))


def _mots_significatifs(libelle: str) -> set[str]:
    """Mots significatifs d'un libelle de menu : accents et casse reduits, mots-outils ecartes.

    C'est la regle d'**appartenance** retenue par `04-RESEARCH.md`, et non l'egalite stricte : D-47
    exige des formes abreges dans l'aiguillage corrige (`4. OPTIMISATION`, `3. PANOPLIES`), sous
    peine de declarer fautif le texte corrige et de rendre inatteignable le vert du critere 5.
    """
    mots = re.findall(r"[A-Za-z]+", _sans_accents(libelle))
    return {mot.upper() for mot in mots if len(mot) >= 4 and mot.upper() not in MOTS_OUTILS}


def _libelle_rendu(ligne: str) -> str:
    """Libelle d'une ligne rendue, entites HTML resolues et espaces reduits.

    La premiere ligne du menu est rendue `1. RECHERCHE D&#39;OBJETS` : sans cette reduction, le
    libelle mesure porterait une entite et la comparaison avec le libelle cite serait fausse.
    """
    return re.sub(r"\s+", " ", html.unescape(ligne)).strip()


def _lire_fixture() -> str:
    """Copie figee des extraits obsoletes, lue en UTF-8 explicite (D-59b).

    Fixture absente = `AssertionError` localisante (D-13), jamais un `skip` silencieux : sans cette
    piece, le rouge du critere 5 ne serait plus relancable apres la correction de `GUIDE_WIZARD.md`
    et le detecteur resterait sans morsure.
    """
    chemin = RACINE_DEPOT.joinpath(*FIXTURE_OBSOLETE)
    if not chemin.is_file():
        raise AssertionError(
            f"{'/'.join(FIXTURE_OBSOLETE)} : copie figee introuvable ({chemin}) ; attendu la copie "
            f"figee et partielle des extraits obsoletes de {GUIDE_WIZARD}, qui rend relancable le "
            f"rouge du critere 5 (D-59b)"
        )
    return chemin.read_text(encoding="utf-8")


def _faits_du_rendu(app, normalize) -> dict:
    """Les attentes du detecteur, **mesurees au rendu** — jamais recopiees (D-58, T-04-12).

    Trois groupes de faits, chacun accompagne du **fichier de code qui produit ses attentes** (D-13,
    repris par D-65) :

    - `menus` et `menu_optimisation` : les libelles du menu principal lus au rendu de `GET /`, et le
      numero qui ouvre reellement l'optimisation, decouvert en postant chaque numero de menu sur un
      client **neuf** et en suivant sa redirection — jamais suppose, jamais ecrit de memoire ;
    - `filtres` : les libelles de touches lus sur les **deux** pages de `/optimize/wizard/slots`,
      corroborees par `TYPE_FILTER_KEYS[5]`/`[6]` et `TYPE_FILTER_LABELS` de `{SOURCE_SPEC}` (D-53) —
      une divergence entre les deux sources est une erreur de harnais, jamais un constat de
      documentation ;
    - `arrivee` : le dernier segment de la chaine d'arrivee, postee pas a pas sur un seul client.

    Les sources (`source_menu`, `source_filtres`, `source_arrivee`) sont les chemins de code, pris
    dans les constantes du module : c'est ce qui permet a chaque constat de nommer sa valeur attendue
    **et** son producteur sans que `renvois_obsoletes` n'ait a lire un fichier ni a citer une
    constante de projet.
    """
    menus: dict[int, str] = {}
    for ligne in _lignes_du_corps(app.test_client().get("/")):
        trouve = MOTIF_LIGNE_MENU_RENDU.match(ligne)
        if trouve is not None:
            menus[int(trouve.group("numero"))] = _libelle_rendu(trouve.group("libelle"))
    if not menus:
        raise AssertionError(
            f"le rendu de GET / ne porte aucun libelle de menu numerote ; attendu les entrees du "
            f"menu principal, construites par {SOURCE_ROUTES} (menu)"
        )

    # Le numero qui ouvre l'optimisation est mesure, jamais suppose : on poste chaque numero sur un
    # client neuf et l'on suit la redirection jusqu'aux trois questions.
    menu_optimisation = 0
    for numero in sorted(menus):
        reponse = app.test_client().post("/", data={"selection": str(numero)})
        cible = reponse.headers.get("Location", "")
        if cible != "/optimize":
            continue
        suite = app.test_client().get(cible)
        if suite.headers.get("Location", "").startswith("/optimize/quick/"):
            menu_optimisation = numero
    if not menu_optimisation:
        raise AssertionError(
            f"aucun numero du menu rendu par GET / ne mene a l'optimisation ; attendu le numero dont "
            f"la redirection de POST / atteint /optimize puis les trois questions, construit par "
            f"{SOURCE_ROUTES} (menu_post)"
        )

    filtres_client = app.test_client()
    lignes_slots = _lignes_du_corps(filtres_client.get("/optimize/wizard/slots"))
    lignes_slots += _lignes_du_corps(filtres_client.get("/optimize/wizard/slots?page=2"))
    rendus = _filtres_du_rendu(lignes_slots)
    filtres: dict[int, str] = {}
    for touche, indice in ((6, 5), (7, 6)):
        libelle = rendus.get(touche, "")
        corrobore = TYPE_FILTER_LABELS.get(TYPE_FILTER_KEYS[indice], "")
        if not libelle or normalize(libelle) != normalize(corrobore):
            raise AssertionError(
                f"le rendu de /optimize/wizard/slots porte F{touche} = « {libelle} » ; attendu "
                f"« {corrobore} », lu dans TYPE_FILTER_LABELS[TYPE_FILTER_KEYS[{indice}]] de "
                f"{SOURCE_SPEC}"
            )
        filtres[touche] = libelle

    parcours = app.test_client()
    arrivee = ""
    for methode, adresse, donnees in (
        ("POST", "/", {"selection": str(menu_optimisation)}),
        ("GET", "/optimize", None),
        ("POST", "/optimize/quick/classe", {"cmd": "Cra"}),
        ("POST", "/optimize/quick/elements", {"cmd": "terre"}),
        ("POST", "/optimize/quick/niveau", {"cmd": "avance"}),
    ):
        reponse = (
            parcours.get(adresse) if methode == "GET" else parcours.post(adresse, data=donnees)
        )
        cible = reponse.headers.get("Location", "")
        arrivee = cible.rstrip("/").rsplit("/", 1)[-1] if cible else ""
    if not arrivee:
        raise AssertionError(
            f"la chaine d'arrivee mesuree n'atteint aucun ecran ; attendu le dernier segment de la "
            f"redirection des trois questions, construit par {SOURCE_ROUTES}"
        )

    return {
        "menus": menus,
        "menu_optimisation": menu_optimisation,
        "filtres": filtres,
        "arrivee": arrivee,
        "source_menu": SOURCE_ROUTES,
        "source_filtres": f"{SOURCE_ROUTES} et {SOURCE_SPEC}",
        "source_arrivee": SOURCE_ROUTES,
    }


def _renvois_au_menu(lignes: list[str], faits: dict) -> list[str]:
    """Forme (a) : un renvoi au menu principal qui ne correspond pas au menu rendu (D-58).

    Deux prises, parce que les trois occurrences reelles du fichier n'ont pas la meme forme :

    - une **invitation** (« tapez »/« saisissez ») qui cite un numero entre accents graves en parlant
      d'optimisation : le numero est compare a celui que `faits["menu_optimisation"]` a mesure ;
    - un **jeton de menu** `N. LIBELLE`, cherche n'importe ou dans la ligne : il est juge contre le
      libelle **rendu** de son numero, par appartenance de mots significatifs.
    """
    constats: list[str] = []
    menus: dict[int, str] = faits["menus"]
    attendu = faits["menu_optimisation"]
    source = faits["source_menu"]
    for ligne in lignes:
        if MOTIF_INVITATION.search(ligne) and RACINE_OPTIMISATION.search(ligne):
            for numero in MOTIF_NUMERO_CITE.findall(ligne):
                if int(numero) != attendu:
                    constats.append(
                        f"{MOTIF_RENVOI_MENU} : la ligne « {ligne} » invite a taper `{numero}` pour "
                        f"ouvrir l'optimisation ; le numero mesure qui ouvre l'optimisation est "
                        f"`{attendu}` (menu {attendu} = « {menus.get(attendu, '')} »), verifie par la "
                        f"redirection de POST / construite par {source}"
                    )
        for trouve in MOTIF_JETON_MENU.finditer(ligne):
            numero = int(trouve.group("numero"))
            libelle = trouve.group("libelle").strip()
            if numero not in menus:
                constats.append(
                    f"{MOTIF_RENVOI_MENU} : le jeton de menu « {numero}. {libelle} » porte un numero "
                    f"absent du menu rendu ({sorted(menus)}) ; attendu un numero du menu principal, "
                    f"rendu par GET / et construit par {source}"
                )
                continue
            if not _mots_significatifs(libelle) & _mots_significatifs(menus[numero]):
                constats.append(
                    f"{MOTIF_RENVOI_MENU} : le jeton de menu « {numero}. {libelle} » ne designe pas le "
                    f"menu {numero} ; le rendu de GET / associe {numero} au libelle "
                    f"« {menus[numero]} », construit par {source}"
                )
    return constats


def _renvois_de_filtre(lignes: list[str], faits: dict) -> list[str]:
    """Forme (b) : une ligne qui renvoie a une arme a distance par la touche du filtre inverse.

    La fenetre est **la ligne**, jamais le fichier : c'est ce qui evite de signaler un
    `% Résistance distance` ou un `F7` de navigation qui vivent dans d'autres lignes. Un renvoi est
    fautif quand la ligne porte `F6`/`F7` et un mot de distance, mais pas le libelle rendu de la
    touche citee.
    """
    constats: list[str] = []
    filtres: dict[int, str] = faits["filtres"]
    source = faits["source_filtres"]
    for ligne in lignes:
        normalisee = _sans_accents(ligne).lower()
        if not any(racine in normalisee for racine in RACINES_DISTANCE):
            continue
        for trouve in MOTIF_TOUCHE_FILTRE.finditer(ligne):
            touche = int(trouve.group("numero"))
            libelle = filtres.get(touche, "")
            if not libelle:
                continue
            if _sans_accents(libelle).lower() not in normalisee:
                constats.append(
                    f"{MOTIF_RENVOI_FILTRE} : la ligne « {ligne} » renvoie a une arme de distance par "
                    f"la touche F{touche} ; le libelle rendu de F{touche} est « {libelle} », lu sur "
                    f"/optimize/wizard/slots et produit par {source}"
                )
    return constats


def _renvois_a_l_arrivee(lignes: list[str], faits: dict) -> list[str]:
    """Forme (c) : une phrase affirmative qui affirme une arrivee directe dans le wizard.

    La garde de negation est indispensable (D-60) : la page corrigee **peut** ecrire « vous n'arrivez
    pas directement dans le wizard » pour corriger explicitement la croyance, et ce renvoi est
    legitime.
    """
    constats: list[str] = []
    arrivee = faits["arrivee"]
    source = faits["source_arrivee"]
    for ligne in lignes:
        normalisee = _sans_accents(ligne).lower()
        if not any(racine in normalisee for racine in RACINES_ARRIVEE):
            continue
        if "wizard" not in normalisee and "assistant" not in normalisee:
            continue
        if not any(marque in normalisee for marque in MARQUES_IMMEDIATETE):
            continue
        if MOTIF_NEGATION.search(normalisee):
            continue
        if arrivee == "recap":
            constats.append(
                f"{MOTIF_RENVOI_ARRIVEE} : la ligne « {ligne} » affirme une arrivee directe dans le "
                f"wizard ; la chaine d'arrivee mesuree atteint « {arrivee} » apres les trois "
                f"questions, construit par {source}"
            )
    return constats


def renvois_obsoletes(texte: str, faits: dict) -> list[str]:
    """Constats de renvois obsoletes d'un texte, juges contre les faits du jeu courant (D-58, WIZ-03).

    **Fonction pure** : elle ne lit aucun fichier, n'ouvre aucune connexion et ne cite aucune
    constante de projet — les attentes lui arrivent par `faits` (mesurees au rendu, D-58) et chaque
    constat les nomme avec le **fichier de code qui les produit** (D-13, repris par D-65).

    Trois formes nommees, et aucune autre : (a) un renvoi au menu principal qui ne correspond pas au
    menu rendu, (b) un renvoi de filtre inverse (`F7` presente comme les armes a distance), (c) une
    arrivee « directe » dans le wizard.

    **Limite honnete (D-58/D-26) :** ce detecteur ne revendique **aucune exhaustivite**. Une autre
    inversion, hors de ces trois formes, ne fera pas echouer la suite. L'enonce produit est « le
    detecteur ne signale rien sur l'aiguillage corrige », jamais « plus aucun renvoi obsolete
    n'existe ».

    **Limite de precision de la forme (a) :** les jetons `N. LIBELLE` sont juges contre les libelles
    de **premier niveau** mesures au rendu de `GET /`. Un renvoi vers un **sous-menu** portant le
    meme numero est donc hors de la surface comparee et serait rapporte comme forme (a) : la portee
    de la forme (a) est les renvois au menu principal, et cette precision est nommee plutot que
    passee sous silence (meme arbitrage que D-26).
    """
    lignes = [ligne.strip() for ligne in texte.splitlines()]
    constats: list[str] = []
    constats += _renvois_au_menu(lignes, faits)
    constats += _renvois_de_filtre(lignes, faits)
    constats += _renvois_a_l_arrivee(lignes, faits)
    return constats


def _couples_de_table(sous_texte: str, motif: re.Pattern[str]) -> dict[int, str]:
    """Couples numero -> libelle cites par une table de la page, une ligne de tableau par couple."""
    couples: dict[int, str] = {}
    for ligne in sous_texte.splitlines():
        trouve = motif.match(ligne)
        if trouve is not None:
            couples[int(trouve.group("numero"))] = trouve.group("libelle").strip()
    return couples


def _couples_texte(sous_texte: str, motif: re.Pattern[str]) -> dict[str, str]:
    """Couples cle -> libelle cites par une table dont la cle n'est pas un numero de ligne."""
    couples: dict[str, str] = {}
    for ligne in sous_texte.splitlines():
        trouve = motif.match(ligne)
        if trouve is not None:
            couples[trouve.group("cle").strip()] = trouve.group("libelle").strip()
    return couples


def _identifiants_cites(corps: str) -> dict[str, str]:
    """Couples etape -> identifiant d'ecran cites par la table de la section d'arrivee.

    La cle est le mot-cle de l'etape (`slots`, `options`, ...) : la comparaison se fait donc sur le
    nom que `WIZARD_STEPS` emploie, jamais sur le numero de la ligne de tableau.
    """
    cites: dict[str, str] = {}
    for ligne in corps.splitlines():
        trouve = MOTIF_LIGNE_IDENTIFIANT.match(ligne)
        if trouve is not None:
            cites[trouve.group("etape")] = trouve.group("identifiant")
    return cites


def _couples_de_commandes(lignes: list[str]) -> dict[str, str]:
    """Couples cle -> verbe annonces par le corps du recapitulatif, lus au rendu.

    Une meme ligne rendue porte plusieurs couples separes par au moins deux espaces
    (`GO = LANCER  RESET = REINITIALISER  1-8 = RETOUR ECRAN`) : la decoupe suit ce separateur
    mesure, jamais une position fixe. Les autres lignes du corps (`BAN=0 FORCE=0`, `JET=average`)
    ne portent pas la forme `CLE = VERBE` et ne produisent donc aucun couple.
    """
    couples: dict[str, str] = {}
    for ligne in lignes:
        for morceau in SEPARATEUR_COMMANDES.split(ligne.strip()):
            trouve = MOTIF_COMMANDE_RENDUE.match(morceau)
            if trouve is not None:
                couples[trouve.group("cle")] = trouve.group("verbe").strip()
    return couples


def _touches_citees(corps: str) -> dict[int, dict[str, str]]:
    """Couples touche -> libelle cites par la table des touches, indexes par numero d'etape.

    La table de la page porte une ligne par etape ; chaque ligne cite les trois couples de cette
    etape. Une ligne qui ne porte pas exactement cette forme n'entre pas dans le dictionnaire, donc
    une ligne manquante ou deformee ne peut pas passer pour une citation.
    """
    citees: dict[int, dict[str, str]] = {}
    for ligne in corps.splitlines():
        trouve = MOTIF_LIGNE_TOUCHES.match(ligne)
        if trouve is not None:
            citees[int(trouve.group("numero"))] = {
                "F7": trouve.group("f7").strip(),
                "F8": trouve.group("f8").strip(),
                "ESC": trouve.group("esc").strip(),
            }
    return citees


def _empreinte(chemin: Path) -> tuple[int, int, str]:
    """Empreinte `(taille, mtime_ns, sha256)` d'un fichier, pour comparer deux instants (T-04-08).

    Les trois composantes sont rendues pour qu'un ecart dise laquelle a bouge : le SHA-256 porte le
    contenu, `mtime_ns` porte la modification a contenu identique. Le fichier est lu, jamais ecrit.
    """
    octets = chemin.read_bytes()
    return (len(octets), chemin.stat().st_mtime_ns, hashlib.sha256(octets).hexdigest())


def _options_du_rendu(lignes: list[str]) -> dict[int, str]:
    """Couples numero -> libelle des options, lus dans les lignes rendues du corps.

    Le compte des options vient du rendu, jamais d'une table locale : la liste des onze options
    n'expose aucune constante publique (`dofus_stuff/web/optimize_wizard.py`), le rendu est donc le
    seul ancrage autorise.
    """
    couples: dict[int, str] = {}
    for ligne in lignes:
        trouve = MOTIF_OPTION_RENDUE.match(ligne.strip())
        if trouve is not None:
            couples[int(trouve.group("numero"))] = trouve.group("libelle").strip()
    return couples


def _syntaxe_du_rendu(lignes: list[str]) -> dict[str, str]:
    """Couples prefixe -> verbe des quatre lignes de syntaxe, lus dans le corps rendu."""
    couples: dict[str, str] = {}
    for ligne in lignes:
        trouve = MOTIF_SYNTAXE_RENDUE.match(ligne)
        if trouve is not None:
            couples[trouve.group("prefixe")] = trouve.group("verbe").strip()
    return couples


def _listes_du_rendu(lignes: list[str]) -> dict[str, str]:
    """Contenu rendu des deux listes d'objets, par nom de liste."""
    listes: dict[str, str] = {}
    for ligne in lignes:
        trouve = MOTIF_LISTE_RENDUE.match(ligne.strip())
        if trouve is not None:
            listes[trouve.group("nom")] = trouve.group("contenu").strip()
    return listes


def _forme_d_edition(lignes: list[str]) -> str:
    """Ligne `FORMAT : ...` du sous-ecran d'edition, ou "" si l'ecran n'en porte pas."""
    return next((ligne.strip() for ligne in lignes if ligne.strip().startswith("FORMAT : ")), "")


def _message_de_statut(statut: str) -> str:
    """Premier segment de la ligne de statut : le message, avant les indicateurs de l'ecran.

    La coquille joint le message et les indicateurs par ` — ` (`dofus_stuff/web/routes.py`) : le
    message seul est ce qui se compare au libelle ecrit par le code, sans la pagination ni l'invite
    d'entree.
    """
    return statut.split(" — ", 1)[0].strip()


def _libelle_saisie(reponse) -> str:
    """Texte interieur du libelle du champ de saisie, tel qu'il est rendu."""
    trouve = LIBELLE_SAISIE.search(reponse.get_data(as_text=True))
    return "" if trouve is None else trouve.group(1)


def _champ_saisie(reponse) -> dict[str, str]:
    """Attributs de la balise du champ de saisie, lus dans cette balise et nulle part ailleurs."""
    trouve = MOTIF_CHAMP_SAISIE.search(reponse.get_data(as_text=True))
    if trouve is None:
        return {}
    return {
        attribut.group("nom"): attribut.group("valeur")
        for attribut in MOTIF_ATTRIBUT_CHAMP.finditer(trouve.group("attributs"))
    }


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


def test_options_solveur_ancres_au_rendu(docs_dir: Path, app, normalize, section) -> None:
    """Les options citees par la page sont celles du rendu, et leurs refus ceux du code (D-19).

    Le compte des options est lu **au rendu**, jamais dans une table locale : la liste des options
    n'expose aucune constante publique (`dofus_stuff/web/optimize_wizard.py`). Le sous-ecran
    d'edition est reconnu a ce que le rendu porte vraiment — code de programme de l'en-tete, libelle
    de saisie, longueur maximale **lue dans la balise du champ** — et les deux comportements de
    numeros sont mesures : ouvrir une option d'edition passe par ce sous-ecran, basculer une option a
    valeur immediate rend un autre message. Aucune saisie `GO` : elle lancerait le solveur.
    """
    texte = _texte_page(docs_dir)
    texte_normalise = normalize(texte)
    corps_page = section(texte, TITRE_OPTIONS, PAGE)
    constats: list[str] = []

    client = app.test_client()
    ecran = client.get("/optimize/wizard/options")
    if ecran.status_code != 200:
        constats.append(
            f"/optimize/wizard/options repond {ecran.status_code} ; attendu 200, cet ecran etant "
            f"rendu par {SOURCE_ROUTES}"
        )
    lignes = _lignes_du_corps(ecran)
    rendues = _options_du_rendu(lignes)
    if not rendues:
        constats.append(
            f"aucune option numerotee n'est lisible dans le corps rendu de "
            f"/optimize/wizard/options ; attendu les options numerotees rendues par {SOURCE_WIZARD}"
        )
    else:
        numeros = sorted(rendues)
        if numeros != list(range(1, len(numeros) + 1)):
            constats.append(
                f"le rendu de /optimize/wizard/options porte les numeros {numeros} ; attendu des "
                f"options numerotees de 1 a {len(numeros)} sans trou, telles que {SOURCE_WIZARD} "
                f"les ecrit"
            )

    cites = _couples_de_table(corps_page, MOTIF_LIGNE_OPTION)
    if len(cites) != len(rendues):
        constats.append(
            f"{PAGE} : la section « {TITRE_OPTIONS} » cite {len(cites)} option(s) pour "
            f"{len(rendues)} rendue(s) par /optimize/wizard/options ; attendu autant d'options "
            f"citees que rendues, le compte etant lu au rendu ({SOURCE_WIZARD})"
        )
    for numero in sorted(set(rendues) | set(cites)):
        rendu = rendues.get(numero, "")
        cite = cites.get(numero, "")
        if normalize(rendu) != normalize(cite):
            constats.append(
                f"{PAGE} : option {numero} — la section cite « {cite} » et le rendu associe le "
                f"numero {numero} a « {rendu} » ; attendu le libelle rendu par {SOURCE_WIZARD}"
            )

    for motif, invite in (
        (MOTIF_INVITE_OPTIONS, "OPTIONS (N=EDIT) :"),
        (MOTIF_RAPPEL_OPTIONS, "N=CHOISIR OPTION"),
    ):
        ligne_rendue = next((ligne.strip() for ligne in lignes if motif.match(ligne.strip())), "")
        if not ligne_rendue:
            constats.append(
                f"la ligne « {invite} » est absente du rendu de /optimize/wizard/options ; attendu "
                f"cet intitule, ecrit par {SOURCE_WIZARD}"
            )
        elif normalize(invite) not in texte_normalise:
            constats.append(
                f"{PAGE} : l'intitule rendu « {invite} » n'est pas cite par la page ; attendu cet "
                f"intitule, lu au rendu et ecrit par {SOURCE_WIZARD}"
            )

    # Le sous-ecran d'edition, atteint par le rendu : ouvrir la premiere option d'edition.
    sous_ecran = app.test_client()
    sous_ecran.post("/optimize/wizard/options", data={"cmd": "1"}, follow_redirects=True)
    ecran_sous = sous_ecran.get("/optimize/wizard/options")
    lignes_sous = _lignes_du_corps(ecran_sous)
    entete_sous = _entete(ecran_sous)
    if normalize("OPT-WED") not in normalize(entete_sous):
        constats.append(
            f"l'en-tete du sous-ecran d'edition ouvert par la saisie « 1 » vaut « {entete_sous} » ; "
            f"attendu le code de programme « OPT-WED » rendu par {SOURCE_ROUTES}"
        )
    if normalize("OPT-WED") not in texte_normalise:
        constats.append(
            f"{PAGE} : le sous-ecran d'edition est annonce par « OPT-WED » et ce code n'est pas "
            f"cite par la page ; attendu le code rendu par {SOURCE_ROUTES}"
        )
    libelle = _libelle_saisie(ecran_sous)
    if normalize("VAL") not in normalize(libelle):
        constats.append(
            f"le libelle du champ de saisie du sous-ecran vaut « {libelle} » ; attendu un libelle "
            f"portant « VAL », ecrit par {SOURCE_ROUTES}"
        )
    if "VAL" not in texte:
        constats.append(
            f"{PAGE} : le libelle de saisie rendu « {libelle} » n'est pas cite par la page ; attendu "
            f"le libelle du champ, ecrit par {SOURCE_ROUTES}"
        )
    champ = _champ_saisie(ecran_sous)
    longueur = champ.get("maxlength", "")
    if longueur != "20":
        constats.append(
            f"la balise du champ du sous-ecran porte maxlength=« {longueur} » ; attendu la longueur "
            f"maximale rendue par {SOURCE_ROUTES}, lue dans la balise du champ"
        )
    if "maxlength=20" not in texte:
        constats.append(
            f"{PAGE} : le champ du sous-ecran est limite a maxlength={longueur} et cette limite "
            f"n'est pas citee par la page ; attendu la limite rendue par {SOURCE_ROUTES}"
        )

    reponse = sous_ecran.post("/optimize/wizard/options", data={"value": "300"}, follow_redirects=True)
    statut = _statut(reponse)
    if normalize("VALEUR ENREGISTREE") not in normalize(statut):
        constats.append(
            f"enregistrer une valeur dans le sous-ecran d'edition rend « {statut} » ; attendu le "
            f"message « VALEUR ENREGISTREE », ecrit par {SOURCE_ROUTES}"
        )
    if normalize("VALEUR ENREGISTREE") not in texte_normalise:
        constats.append(
            f"{PAGE} : le message rendu « VALEUR ENREGISTREE » n'est pas cite par la page ; attendu "
            f"ce message, ecrit par {SOURCE_ROUTES}"
        )

    for numero in (6, 11):
        bascule = app.test_client()
        reponse = bascule.post(
            "/optimize/wizard/options", data={"cmd": str(numero)}, follow_redirects=True
        )
        statut = _statut(reponse)
        if normalize("OPTION MISE A JOUR") not in normalize(statut):
            constats.append(
                f"la saisie « {numero} » sur /optimize/wizard/options rend « {statut} » ; attendu le "
                f"message « OPTION MISE A JOUR » d'une bascule immediate, ecrit par {SOURCE_WIZARD}"
            )
    if normalize("OPTION MISE A JOUR") not in texte_normalise:
        constats.append(
            f"{PAGE} : le message rendu « OPTION MISE A JOUR » n'est pas cite par la page ; attendu "
            f"ce message, lu au rendu et ecrit par {SOURCE_WIZARD}"
        )

    for saisie, message in (("12", "OPTION INVALIDE"), ("abc", "SAISIR UN NUMERO D'OPTION")):
        refus = app.test_client()
        reponse = refus.post("/optimize/wizard/options", data={"cmd": saisie}, follow_redirects=True)
        statut = _statut(reponse)
        if normalize(message) not in normalize(statut):
            constats.append(
                f"la saisie « {saisie} » rend « {statut} » ; attendu le message « {message} » dans la "
                f"ligne de statut, ecrit par {SOURCE_WIZARD}"
            )
        if normalize(message) not in texte_normalise:
            constats.append(
                f"{PAGE} : le message de refus rendu « {message} » n'est pas cite par la page ; "
                f"attendu ce message, lu au rendu et ecrit par {SOURCE_WIZARD}"
            )

    assert not constats, (
        f"{PAGE} : constats sur les options du solveur : "
        + " ; ".join(constats)
        + f" ; attendu les options rendues par {SOURCE_WIZARD} citees par la section "
        f"« {TITRE_OPTIONS} », avec le sous-ecran d'edition et les refus rendus par {SOURCE_ROUTES}"
    )


def test_formats_d_edition_et_refus_reels(docs_dir: Path, app, normalize, section) -> None:
    """La page cite chaque forme d'edition avec son ecran, et le refus de format est celui du rendu.

    Deux ecrans d'edition seulement portent une forme differente : les caracteristiques et les
    objectifs de PA / PM / PO. Le controle atteint **les deux** sous-ecrans par le rendu, lit leur
    ligne de forme et l'associe a l'ecran qui la porte, puis verifie que les deux formes marquees ne
    sont pas la meme : deux formes echangees ne peuvent donc pas passer. Le refus de format est
    mesure, pas deduit : une saisie qui ne porte pas quatre nombres rend le message de la forme de
    l'ecran, et ce message est celui de la forme affichee juste au-dessus.
    """
    texte = _texte_page(docs_dir)
    texte_normalise = normalize(texte)
    corps_page = section(texte, TITRE_NOMBRES, PAGE)
    constats: list[str] = []

    formes_citees = _couples_texte(corps_page, MOTIF_LIGNE_FORMAT)
    if not formes_citees:
        constats.append(
            f"{PAGE} : la section « {TITRE_NOMBRES} » ne cite aucune forme d'edition ; attendu une "
            f"ligne de tableau par forme, avec l'ecran qui la porte ({SOURCE_WIZARD})"
        )

    mesures: dict[str, tuple[object, str]] = {}
    for etape in ("caracs", "papmpo"):
        client = app.test_client()
        client.post(f"/optimize/wizard/{etape}", data={"cmd": "1"}, follow_redirects=True)
        ecran = client.get(f"/optimize/wizard/{etape}")
        if ecran.status_code != 200:
            constats.append(
                f"/optimize/wizard/{etape} repond {ecran.status_code} apres la saisie « 1 » ; attendu "
                f"200, cet ecran etant rendu par {SOURCE_ROUTES}"
            )
        forme = _forme_d_edition(_lignes_du_corps(ecran))
        mesures[etape] = (client, forme)
        titre = STEP_TITLES.get(etape, "")
        if not forme:
            constats.append(
                f"le sous-ecran d'edition de /optimize/wizard/{etape} ne porte aucune ligne de forme ; "
                f"attendu la forme rendue par {SOURCE_WIZARD}, lue apres la saisie « 1 »"
            )
            continue
        if normalize(forme) not in texte_normalise:
            constats.append(
                f"{PAGE} : la forme rendue par le sous-ecran de {etape} vaut « {forme} » et n'est pas "
                f"citee par la page ; attendu cette forme, lue au rendu ({SOURCE_WIZARD})"
            )
        cite = formes_citees.get(titre, "")
        if normalize(cite) != normalize(forme):
            constats.append(
                f"{PAGE} : l'ecran « {titre} » — la section cite « {cite} » et le sous-ecran atteint "
                f"par {etape} rend « {forme} » ; attendu chaque forme avec l'ecran qui la porte, "
                f"jamais deux formes echangees ({SOURCE_WIZARD})"
            )

    formes = {normalize(forme) for _, forme in mesures.values() if forme}
    if len(formes) != len(mesures):
        constats.append(
            f"{PAGE} : les {len(mesures)} sous-ecrans mesures rendent {len(formes)} forme(s) "
            f"distincte(s) ({', '.join(sorted(formes))}) ; attendu une forme par ecran, les deux "
            f"formes n'etant jamais fusionnees ({SOURCE_WIZARD})"
        )

    for etape, (client, forme) in mesures.items():
        reponse = client.post(
            f"/optimize/wizard/{etape}", data={"value": "1 2 3"}, follow_redirects=True
        )
        message = _message_de_statut(_statut(reponse))
        if normalize(forme) not in normalize(message):
            constats.append(
                f"{PAGE} : sur {etape}, une saisie de trois valeurs rend « {message} » et la forme du "
                f"sous-ecran vaut « {forme} » ; attendu le message de refus du format, identique a la "
                f"forme affichee juste au-dessus ({SOURCE_ROUTES})"
            )

    lignes_liste = _lignes_du_corps(app.test_client().get("/optimize/wizard/caracs"))
    if not any(ligne.strip().startswith("N=EDIT") for ligne in lignes_liste):
        constats.append(
            "la ligne « N=EDIT » est absente du rendu de /optimize/wizard/caracs ; attendu cet "
            f"intitule, ecrit par {SOURCE_WIZARD}"
        )
    if "N=EDIT" not in texte:
        constats.append(
            f"{PAGE} : l'intitule rendu « N=EDIT » n'est pas cite par la page ; attendu cet intitule, "
            f"ecrit par {SOURCE_WIZARD}"
        )

    for saisie, message in (("abc", "SAISIR LE NUMERO DE LA LIGNE"), ("99", "NUMERO INVALIDE")):
        refus = app.test_client()
        reponse = refus.post("/optimize/wizard/caracs", data={"cmd": saisie}, follow_redirects=True)
        statut = _statut(reponse)
        if normalize(message) not in normalize(statut):
            constats.append(
                f"la saisie « {saisie} » sur /optimize/wizard/caracs rend « {statut} » ; attendu le "
                f"message « {message} » dans la ligne de statut, ecrit par {SOURCE_WIZARD}"
            )
        if normalize(message) not in texte_normalise:
            constats.append(
                f"{PAGE} : le message rendu « {message} » n'est pas cite par la page ; attendu ce "
                f"message, lu au rendu et ecrit par {SOURCE_WIZARD}"
            )

    for separateur in (" ", ","):
        valeur = separateur.join(("1", "2", "3", "4"))
        valide = app.test_client()
        valide.post("/optimize/wizard/caracs", data={"cmd": "4"}, follow_redirects=True)
        reponse = valide.post(
            "/optimize/wizard/caracs", data={"value": valeur}, follow_redirects=True
        )
        statut = _statut(reponse)
        if normalize("CARAC ENREGISTREE") not in normalize(statut):
            constats.append(
                f"enregistrer la valeur « {valeur} » rend « {statut} » ; attendu le message "
                f"« CARAC ENREGISTREE » d'une saisie de quatre nombres, ecrit par {SOURCE_ROUTES}"
            )
    if normalize("CARAC ENREGISTREE") not in texte_normalise:
        constats.append(
            f"{PAGE} : le message rendu « CARAC ENREGISTREE » n'est pas cite par la page ; attendu ce "
            f"message, lu au rendu et ecrit par {SOURCE_WIZARD}"
        )

    assert not constats, (
        f"{PAGE} : constats sur les formes d'edition : "
        + " ; ".join(constats)
        + f" ; attendu chaque forme d'edition citee avec son ecran par la section "
        f"« {TITRE_NOMBRES} », les deux formes jamais fusionnees, et les messages d'edition rendus par "
        f"{SOURCE_ROUTES}"
    )


def test_syntaxe_d_items_et_etat_vide(docs_dir: Path, app, normalize, section) -> None:
    """La syntaxe des items citee par la page est celle du rendu, et l'etat vide est celui du code.

    Les quatre lignes de syntaxe sont appariees **prefixe par prefixe** : la page les cite sous forme
    de tableau, la comparaison porte donc sur le couple et jamais sur une ligne entiere — c'est ce qui
    rend une permutation de verbes visible. Le seul refus est mesure : une saisie sans prefixe est
    refusee, alors que `+ID` ne l'est pas. L'etat vide est lu au rendu puis confronte a la phrase qui
    le cite, sur un client neuf comme apres vidage, et la troncature annoncee est mesuree sur une
    liste de plus de huit entrees.
    """
    texte = _texte_page(docs_dir)
    texte_normalise = normalize(texte)
    corps_page = section(texte, TITRE_ITEMS, PAGE)
    constats: list[str] = []

    client = app.test_client()
    ecran = client.get("/optimize/wizard/items")
    if ecran.status_code != 200:
        constats.append(
            f"/optimize/wizard/items repond {ecran.status_code} ; attendu 200, cet ecran etant rendu "
            f"par {SOURCE_ROUTES}"
        )
    lignes = _lignes_du_corps(ecran)
    rendues = _syntaxe_du_rendu(lignes)
    attendues = ("+ID", "-ID", "!ID", "CLEAR")
    if sorted(rendues) != sorted(attendues):
        constats.append(
            f"le rendu de /optimize/wizard/items porte les saisies {sorted(rendues)} ; attendu les "
            f"quatre saisies {sorted(attendues)} ecrites par {SOURCE_WIZARD}"
        )

    cites = _couples_texte(corps_page, MOTIF_LIGNE_SYNTAXE_ITEMS)
    if len(cites) != len(rendues):
        constats.append(
            f"{PAGE} : la section « {TITRE_ITEMS} » cite {len(cites)} saisie(s) pour {len(rendues)} "
            f"ligne(s) de syntaxe rendue(s) ; attendu autant de saisies citees que de lignes rendues "
            f"({SOURCE_WIZARD})"
        )
    for prefixe in sorted(set(rendues) | set(cites)):
        verbe_rendu = rendues.get(prefixe, "")
        verbe_cite = cites.get(prefixe, "")
        if normalize(verbe_rendu) != normalize(verbe_cite):
            constats.append(
                f"{PAGE} : la saisie « {prefixe} » — la page annonce « {verbe_cite} » et l'ecran rend "
                f"« {verbe_rendu} » ; attendu le verbe rendu par {SOURCE_WIZARD}"
            )

    trouve = MOTIF_ETAT_VIDE_CITE.search(corps_page)
    etat_cite = trouve.group("etat") if trouve is not None else ""
    if not etat_cite:
        constats.append(
            f"{PAGE} : la section « {TITRE_ITEMS} » ne cite aucun etat vide ; attendu l'etat rendu par "
            f"{SOURCE_WIZARD} pour une liste sans entree"
        )
    etats_neuf = _listes_du_rendu(lignes)
    for nom in ("INTERDITS", "FORCES"):
        if nom not in etats_neuf:
            constats.append(
                f"la liste {nom} n'est pas lisible dans le rendu de /optimize/wizard/items ; attendu "
                f"les deux listes rendues par {SOURCE_WIZARD}"
            )
            continue
        if normalize(etats_neuf[nom]) != normalize(etat_cite):
            constats.append(
                f"{PAGE} : la section cite l'etat vide « {etat_cite} » et le rendu rend "
                f"« {etats_neuf[nom]} » pour la liste {nom} sur un client neuf ; attendu l'etat vide "
                f"ecrit par {SOURCE_WIZARD}"
            )
    vide_interdits = etats_neuf.get("INTERDITS", "")
    vide_forces = etats_neuf.get("FORCES", "")

    ajout = app.test_client()
    reponse = ajout.post("/optimize/wizard/items", data={"cmd": "+12345"}, follow_redirects=True)
    etats = _listes_du_rendu(_lignes_du_corps(reponse))
    if "#12345" not in etats.get("INTERDITS", ""):
        constats.append(
            f"la saisie « +12345 » rend la liste INTERDITS « {etats.get('INTERDITS', '')} » ; attendu "
            f"l'objet ajoute aux interdits, comme l'annonce {SOURCE_WIZARD}"
        )
    if normalize(etats.get("FORCES", "")) != normalize(vide_forces):
        constats.append(
            f"la saisie « +12345 » rend la liste FORCES « {etats.get('FORCES', '')} » ; attendu une "
            f"liste de forces vide « {vide_forces} », l'objet n'etant jamais dans les deux listes "
            f"({SOURCE_WIZARD})"
        )

    deplace = app.test_client()
    deplace.post("/optimize/wizard/items", data={"cmd": "-12345"}, follow_redirects=True)
    reponse = deplace.post("/optimize/wizard/items", data={"cmd": "+12345"}, follow_redirects=True)
    etats = _listes_du_rendu(_lignes_du_corps(reponse))
    if "#12345" not in etats.get("INTERDITS", "") or normalize(
        etats.get("FORCES", "")
    ) != normalize(vide_forces):
        constats.append(
            f"apres « -12345 » puis « +12345 », le rendu porte INTERDITS "
            f"« {etats.get('INTERDITS', '')} » et FORCES « {etats.get('FORCES', '')} » ; attendu "
            f"l'objet deplace d'une liste a l'autre, un objet n'etant jamais interdit et force en "
            f"meme temps ({SOURCE_WIZARD})"
        )

    retrait = app.test_client()
    retrait.post("/optimize/wizard/items", data={"cmd": "+12345"}, follow_redirects=True)
    reponse = retrait.post("/optimize/wizard/items", data={"cmd": "!12345"}, follow_redirects=True)
    etats = _listes_du_rendu(_lignes_du_corps(reponse))
    if normalize(etats.get("INTERDITS", "")) != normalize(vide_interdits):
        constats.append(
            f"apres « !12345 », le rendu porte INTERDITS « {etats.get('INTERDITS', '')} » ; attendu "
            f"une liste d'interdits vide « {vide_interdits} », l'objet etant retire des deux listes "
            f"({SOURCE_WIZARD})"
        )

    for saisie in ("CLEAR", "clear"):
        vidage = app.test_client()
        vidage.post("/optimize/wizard/items", data={"cmd": "+12345"}, follow_redirects=True)
        vidage.post("/optimize/wizard/items", data={"cmd": "-12345"}, follow_redirects=True)
        reponse = vidage.post("/optimize/wizard/items", data={"cmd": saisie}, follow_redirects=True)
        etats = _listes_du_rendu(_lignes_du_corps(reponse))
        for nom, reference in (("INTERDITS", vide_interdits), ("FORCES", vide_forces)):
            if normalize(etats.get(nom, "")) != normalize(reference):
                constats.append(
                    f"apres « {saisie} », le rendu porte {nom} « {etats.get(nom, '')} » ; attendu une "
                    f"liste vide « {reference} », la saisie vidant les deux listes ({SOURCE_WIZARD})"
                )

    espace = app.test_client()
    reponse = espace.post("/optimize/wizard/items", data={"cmd": "  +12345  "}, follow_redirects=True)
    etats = _listes_du_rendu(_lignes_du_corps(reponse))
    if "#12345" not in etats.get("INTERDITS", ""):
        constats.append(
            f"la saisie «   +12345   » rend INTERDITS « {etats.get('INTERDITS', '')} » ; attendu "
            f"l'objet ajoute comme pour une saisie sans espaces, les espaces etant ignores "
            f"({SOURCE_ROUTES})"
        )

    ajoutes = [f"+{identifiant}" for identifiant in range(20001, 20011)]
    troncature = app.test_client()
    for saisie in ajoutes:
        reponse = troncature.post(
            "/optimize/wizard/items", data={"cmd": saisie}, follow_redirects=True
        )
    lignes_tronquees = _lignes_du_corps(reponse)
    etats = _listes_du_rendu(lignes_tronquees)
    affichees = [entree for entree in etats.get("INTERDITS", "").split(",") if entree.strip()]
    ellipses = [ligne.strip() for ligne in lignes_tronquees if "…" in ligne]
    if not ellipses:
        constats.append(
            f"apres {len(ajoutes)} ajouts, aucune ligne d'ellipse n'est rendue pour INTERDITS "
            f"(contenu affiche « {etats.get('INTERDITS', '')} ») ; attendu la troncature de "
            f"l'affichage au-dela de huit entrees, ecrite par {SOURCE_WIZARD}"
        )
    elif len(affichees) >= len(ajoutes):
        constats.append(
            f"apres {len(ajoutes)} ajouts, le rendu affiche {len(affichees)} entree(s) d'INTERDITS et "
            f"la ligne d'ellipse « {ellipses[0]} » ; attendu une liste affichee plus courte que la "
            f"liste complete, la suite etant resumees par l'ellipse ({SOURCE_WIZARD})"
        )
    else:
        cache = re.search(r"\+(\d+)", ellipses[0])
        if cache is None or len(affichees) + int(cache.group(1)) != len(ajoutes):
            constats.append(
                f"apres {len(ajoutes)} ajouts, le rendu affiche {len(affichees)} entree(s) et la ligne "
                f"« {ellipses[0]} » ; attendu le nombre d'entrees cachees annonce, la somme devant "
                f"donner les {len(ajoutes)} saisies ajoutees ({SOURCE_WIZARD})"
            )

    refus = app.test_client()
    reponse = refus.post("/optimize/wizard/items", data={"cmd": "12345"}, follow_redirects=True)
    message = _message_de_statut(_statut(reponse))
    if not message:
        constats.append(
            "la saisie « 12345 » sur /optimize/wizard/items ne rend aucun message dans la ligne de "
            f"statut ; attendu le message de syntaxe ecrit par {SOURCE_WIZARD}"
        )
    elif normalize(message) not in texte_normalise:
        constats.append(
            f"{PAGE} : le refus rendu « {message} » n'est pas cite par la page ; attendu le message de "
            f"syntaxe ecrit par {SOURCE_WIZARD}"
        )
    plus = app.test_client()
    reponse = plus.post("/optimize/wizard/items", data={"cmd": "+12345"}, follow_redirects=True)
    if message and normalize(message) in normalize(_statut(reponse)):
        constats.append(
            f"la saisie « +12345 » rend « {_statut(reponse)} » ; attendu un ajout et non le refus "
            f"« {message} », la saisie prefixee etant un verbe d'ajout et non une saisie interdite "
            f"({SOURCE_WIZARD})"
        )

    assert not constats, (
        f"{PAGE} : constats sur la syntaxe des items : "
        + " ; ".join(constats)
        + f" ; attendu les quatre saisies rendues par {SOURCE_WIZARD} citees avec leur verbe par la "
        f"section « {TITRE_ITEMS} », avec le seul refus et l'etat vide rendus par {SOURCE_ROUTES}"
    )


def test_page_sans_derive_ni_chemin_invente(
    docs_dir: Path, normalize, sections, section
) -> None:
    """La page tient sa forme de bout en bout : titres, H1, retour au sommaire, encodage, chemins.

    Le controle des chemins est le plus utile : tout chemin de code cite entre accents graves doit
    exister sur le disque. Une page qui nomme un fichier disparu (renommage, deplacement) fait donc
    rougir la suite, ce qu'aucune relecture ne garantit. Les titres sont exiges dans l'ordre et leur
    nombre est fixe : une section ajoutee sans controle se voit ici, et non au prochain plan.
    """
    chemin = docs_dir / PAGE
    if not chemin.is_file():
        raise AssertionError(
            f"{PAGE} : page introuvable ({chemin}) ; attendu la page du wizard avance, decrite par "
            f"{SOURCE_WIZARD}"
        )
    octets = chemin.read_bytes()
    texte = octets.decode("utf-8")
    constats: list[str] = []

    titres = [titre for titre, _ in sections(texte) if titre is not None]
    if len(titres) != len(TITRES_SECTION_ATTENDUS):
        constats.append(
            f"{PAGE} : la page porte {len(titres)} section(s) de niveau 2 ({', '.join(titres)}) ; "
            f"attendu exactement {len(TITRES_SECTION_ATTENDUS)} sections, dans cet ordre : "
            f"{', '.join(TITRES_SECTION_ATTENDUS)}"
        )
    for index, attendu in enumerate(TITRES_SECTION_ATTENDUS):
        trouve = titres[index] if index < len(titres) else ""
        if normalize(attendu.lstrip("#").strip()) != normalize(trouve):
            constats.append(
                f"{PAGE} : section {index + 1} attendue « {attendu.lstrip('#').strip()} », section "
                f"trouvee « {trouve} » ; attendu les {len(TITRES_SECTION_ATTENDUS)} sections de la "
                f"page, dans l'ordre du document"
            )

    h1 = [ligne for ligne in texte.splitlines() if ligne.startswith(FRAGMENT_H1)]
    if len(h1) != 1:
        constats.append(
            f"{PAGE} : la page porte {len(h1)} titre(s) de niveau 1 ({', '.join(h1)}) ; attendu un "
            f"seul titre de niveau 1 (D-56)"
        )

    remplies = [ligne.strip() for ligne in texte.splitlines() if ligne.strip()]
    derniere = remplies[-1] if remplies else ""
    if derniere != LIGNE_RETOUR:
        constats.append(
            f"{PAGE} : la derniere ligne non vide vaut « {derniere} » ; attendu « {LIGNE_RETOUR} » "
            f"comme derniere ligne de la page"
        )

    if BALISE_COMMANDE in texte:
        constats.append(
            f"{PAGE} : la page porte un bloc de commandes ; attendu aucun bloc de commandes, le "
            f"wizard avance n'exposant aucune commande en ligne de commande ({SOURCE_ROUTES})"
        )
    if FRAGMENT_LIEN_EXTERNE in texte:
        constats.append(
            f"{PAGE} : la page porte un lien externe ; attendu des liens internes seulement, la page "
            f"decrit le produit de ce depot"
        )

    fins = octets.count(b"\n")
    retours = octets.count(b"\r\n")
    if octets.startswith(BOM_UTF8):
        constats.append(f"{PAGE} : la page commence par un BOM ; attendu un fichier UTF-8 sans BOM")
    if retours != fins:
        constats.append(
            f"{PAGE} : la page porte {fins} fin(s) de ligne pour {retours} retour(s) chariot ; attendu "
            f"des fins de ligne CRLF sur toutes les lignes, comme les autres pages de docs/"
        )

    corps_source = section(texte, TITRE_SOURCE, PAGE)
    for source in (SOURCE_ROUTES, SOURCE_WIZARD, SOURCE_SPEC):
        if source not in corps_source:
            constats.append(
                f"{PAGE} : la section « {TITRE_SOURCE} » ne cite pas « {source} » ; attendu le bloc "
                f"« Source de verite », qui nomme les fichiers dont la page decrit la surface"
            )

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

    assert not constats, (
        f"{PAGE} : constats sur la forme de la page : "
        + " ; ".join(constats)
        + f" ; attendu {len(TITRES_SECTION_ATTENDUS)} sections, un H1, la ligne de retour au sommaire, "
        f"des fins de ligne CRLF, aucun lien externe et des chemins de code existants"
    )


def test_ecrans_et_arrivee_du_wizard(docs_dir: Path, app, normalize, section) -> None:
    """Les identifiants d'ecrans et le chemin d'arrivee sont lus au rendu, puis exiges (D-51, WIZ-02).

    Le chemin d'arrivee est rejoue pas a pas sur **un seul** client : le menu poste `selection=4`,
    `/optimize` redirige vers les trois questions, et `AVANCE` ouvre le wizard. La ou l'on atterrit
    est mesure, jamais suppose : l'ecran d'arrivee est le recapitulatif, et la page le dit — c'est
    l'affirmation fausse que cette phase resorbe.

    Limite nommee (sonde d'aretes WIZ-02, ligne `unclassified`, qui reste `unresolved`) : ce controle
    porte sur les neuf couples identifiant/titre lus dans la ligne d'en-tete et sur la chaine
    d'arrivee. Il ne revendique aucune exhaustivite de la surface des touches, des messages ou des
    commandes du wizard : ce qu'il prouve est nomme, rien de plus.
    """
    texte = _texte_page(docs_dir)
    corps = section(texte, TITRE_ARRIVEE, PAGE)
    constats: list[str] = []

    # 1. Les neuf ecrans : identifiant et titre rendus dans la ligne d'en-tete, cites par la page.
    client = app.test_client()
    cites = _identifiants_cites(corps)
    for numero, etape in enumerate(WIZARD_STEPS, start=1):
        identifiant = f"OPT-W{numero}"
        rendu = client.get(f"/optimize/wizard/{etape}")
        entete = _entete(rendu)
        titre = STEP_TITLES.get(etape, "")
        if rendu.status_code != 200 or identifiant not in entete:
            constats.append(
                f"l'ecran « {etape} » (etape {numero}) repond {rendu.status_code} et sa ligne "
                f"d'en-tete vaut « {entete} » ; attendu l'{MOTIF_IDENTIFIANT_ECRAN} "
                f"« {identifiant} » dans la ligne d'en-tete rendue par {SOURCE_ROUTES}"
            )
        if normalize(titre) not in normalize(entete):
            constats.append(
                f"l'ecran « {etape} » repond {rendu.status_code} et sa ligne d'en-tete vaut "
                f"« {entete} » ; attendu le titre « {titre} » rendu par {SOURCE_WIZARD} (STEP_TITLES)"
            )
        if cites.get(etape, "") != identifiant:
            constats.append(
                f"{PAGE} : la section « {TITRE_ARRIVEE} » associe l'etape {numero} ({etape}) a "
                f"« {cites.get(etape, '')} » ; attendu l'{MOTIF_IDENTIFIANT_ECRAN} "
                f"« {identifiant} », lu dans la ligne d'en-tete rendue par {SOURCE_ROUTES}"
            )
        if normalize(titre) not in normalize(texte):
            constats.append(
                f"{PAGE} : le titre rendu de l'etape {numero} vaut « {titre} » et n'est pas cite "
                f"par la page ; attendu ce titre, lu au rendu de /optimize/wizard/{etape} et produit "
                f"par {SOURCE_WIZARD} (STEP_TITLES)"
            )

    # 2. Un ecran qui n'existe pas : le message du code, rendu sur l'ecran suivant (le menu).
    inconnu = app.test_client()
    reponse = inconnu.get("/optimize/wizard/inconnu")
    cible = reponse.headers.get("Location", "")
    if reponse.status_code != 302 or cible != "/":
        constats.append(
            f"l'ecran inconnu « inconnu » repond {reponse.status_code} vers « {cible} » ; attendu une "
            f"redirection vers le menu principal, posee par {SOURCE_ROUTES}"
        )
    message = "ECRAN WIZARD INCONNU"
    if message not in _statut(inconnu.get("/")):
        constats.append(
            f"{PAGE} : le message « {message} » n'est pas rendu sur l'ecran suivant ; attendu le refus "
            f"de {SOURCE_ROUTES} pour une etape hors de WIZARD_STEPS"
        )
    if normalize(message) not in normalize(texte):
        constats.append(
            f"{PAGE} : le message rendu « {message} » n'est pas cite par la page ; attendu ce message, "
            f"lu au rendu et produit par {SOURCE_ROUTES}"
        )

    # 3. La chaine d'arrivee, rejouee pas a pas sur un seul client.
    parcours = app.test_client()
    for methode, adresse, donnees, attendue in (
        ("POST", "/", {"selection": "4"}, "/optimize"),
        ("GET", "/optimize", None, "/optimize/quick/classe"),
        ("POST", "/optimize/quick/classe", {"cmd": "Cra"}, "/optimize/quick/elements"),
        ("POST", "/optimize/quick/elements", {"cmd": "terre"}, "/optimize/quick/niveau"),
        ("POST", "/optimize/quick/niveau", {"cmd": "avance"}, "/optimize/wizard/recap"),
    ):
        reponse = parcours.get(adresse) if methode == "GET" else parcours.post(adresse, data=donnees)
        cible = reponse.headers.get("Location", "")
        if reponse.status_code != 302 or cible != attendue:
            constats.append(
                f"{methode} {adresse} repond {reponse.status_code} vers « {cible} » ; attendu "
                f"l'{MOTIF_ARRIVEE} vers « {attendue} », construit par {SOURCE_ROUTES}"
            )
    titre_recap = STEP_TITLES.get("recap", "")
    arrivee = parcours.get("/optimize/wizard/recap")
    if arrivee.status_code != 200 or normalize(titre_recap) not in normalize(_entete(arrivee)):
        constats.append(
            f"l'ecran d'arrivee « /optimize/wizard/recap » repond {arrivee.status_code} et sa ligne "
            f"d'en-tete vaut « {_entete(arrivee)} » ; attendu le titre « {titre_recap} » — c'est lui "
            f"que l'{MOTIF_ARRIVEE} atteint, pas les emplacements ({SOURCE_ROUTES})"
        )

    # 4. Les quatre reperes du chemin, cites par la page depuis le rendu.
    entree_menu = next(
        (
            ligne.strip()
            for ligne in _lignes_du_corps(app.test_client().get("/"))
            if MOTIF_LIGNE_MENU.match(ligne)
        ),
        "",
    )
    if not entree_menu or normalize(entree_menu) not in normalize(corps):
        constats.append(
            f"{PAGE} : la section « {TITRE_ARRIVEE} » ne cite pas « {entree_menu} » ; attendu la ligne "
            f"du menu principal qui ouvre le parcours, lue au rendu de GET / et construite par "
            f"{SOURCE_ROUTES} ({MOTIF_ARRIVEE})"
        )

    questions_client = app.test_client()
    vues = [questions_client.get("/optimize/quick/classe")]
    questions_client.post("/optimize/quick/classe", data={"cmd": "Cra"})
    vues.append(questions_client.get("/optimize/quick/elements"))
    questions_client.post("/optimize/quick/elements", data={"cmd": "terre"})
    vues.append(questions_client.get("/optimize/quick/niveau"))

    questions: list[str] = []
    ligne_avance = ""
    for vue in vues:
        for ligne in _lignes_du_corps(vue):
            texte_ligne = ligne.strip()
            if MOTIF_LIGNE_QUESTION.match(texte_ligne) is not None:
                questions.append(texte_ligne)
            if MOTIF_LIGNE_AVANCE.match(texte_ligne) is not None:
                ligne_avance = texte_ligne
    if len(questions) != 3:
        constats.append(
            f"les trois questions du parcours repondent {len(questions)} ligne(s) de la forme "
            f"« N/3 - ... » ; attendu les trois questions posees par {SOURCE_ROUTES} avant le wizard "
            f"({MOTIF_ARRIVEE})"
        )
    for question in questions:
        if normalize(question) not in normalize(corps):
            constats.append(
                f"{PAGE} : la section « {TITRE_ARRIVEE} » ne cite pas la question « {question} » ; "
                f"attendu cette question, lue au rendu de /optimize/quick/<etape> par {SOURCE_ROUTES} "
                f"({MOTIF_ARRIVEE})"
            )
    if not ligne_avance or normalize(ligne_avance) not in normalize(corps):
        constats.append(
            f"{PAGE} : la section « {TITRE_ARRIVEE} » ne cite pas « {ligne_avance} » ; attendu la "
            f"ligne qui ouvre le wizard, lue au rendu des trois questions et construite par "
            f"{SOURCE_ROUTES} ({MOTIF_ARRIVEE})"
        )

    assert not constats, (
        f"{PAGE} : constats sur les ecrans et le chemin d'arrivee : "
        + " ; ".join(constats)
        + f" ; attendu les identifiants d'ecrans et l'{MOTIF_ARRIVEE} lus au rendu de {SOURCE_ROUTES}, "
        f"cites par la section « {TITRE_ARRIVEE} »"
    )


def test_exemple_guide_ancre_au_rendu(docs_dir: Path, app, normalize, section) -> None:
    """L'exemple guide migre est rejoue sur le rendu, edition par edition (D-55, WIZ-02).

    Les trois editions de l'exemple partent chacune d'un **client neuf** : un `POST` accepte reecrit
    l'etat de session, donc rejouer deux editions sur le meme client mesurerait autre chose. La ligne
    rendue apres chaque edition doit etre citee par la section de l'exemple : c'est cet ancrage qui
    fait rougir la suite si le code cesse de porter une ligne que l'exemple promet — la variante
    « cible PA » survit parce que le code la porte, jamais parce que l'ancien guide l'ecrivait.

    Aucune saisie `GO` n'est postee : elle lancerait le solveur (`{SOURCE_ROUTES}`). Seules sa
    citation, lue dans le corps du recapitulatif, et l'action des trois editions sont controlees.
    """
    texte = _texte_page(docs_dir)
    corps = section(texte, TITRE_EXEMPLE, PAGE)
    constats: list[str] = []

    # 1. Les trois editions de l'exemple : navigation depuis le recapitulatif, numero de ligne, valeur.
    for etape, chiffre, numero_ligne, valeur in (
        ("options", "2", "1", "123"),
        ("caracs", "3", "4", "300 0 0 1"),
        ("papmpo", "4", "1", "6 0 11 5"),
    ):
        adresse = f"/optimize/wizard/{etape}"
        client = app.test_client()
        client.get("/optimize/wizard/recap")
        saut = client.post("/optimize/wizard/recap", data={"cmd": chiffre})
        cible = saut.headers.get("Location", "")
        if saut.status_code != 302 or cible != adresse:
            constats.append(
                f"{PAGE} : {MOTIF_EXEMPLE} — le chiffre « {chiffre} » du recapitulatif repond "
                f"{saut.status_code} vers « {cible} » ; attendu l'ecran « {adresse} », lu dans le "
                f"rendu du recapitulatif ({SOURCE_ROUTES})"
            )
        ouverture = client.post(adresse, data={"cmd": numero_ligne})
        cible = ouverture.headers.get("Location", "")
        if ouverture.status_code != 302 or cible != adresse:
            constats.append(
                f"{PAGE} : {MOTIF_EXEMPLE} — le numero de ligne « {numero_ligne} » repond "
                f"{ouverture.status_code} vers « {cible} » ; attendu l'ouverture du sous-ecran "
                f"d'edition de « {adresse} » ({SOURCE_ROUTES})"
            )
        client.get(adresse)
        client.post(adresse, data={"value": valeur})
        rendues = [
            ligne.strip()
            for ligne in _lignes_du_corps(client.get(adresse))
            if ligne.strip().startswith(f"{numero_ligne}.")
        ]
        if not rendues:
            constats.append(
                f"{PAGE} : {MOTIF_EXEMPLE} — aucune ligne rendue ne commence par « {numero_ligne}. » "
                f"apres l'edition « {valeur} » sur « {adresse} » ; attendu la ligne editee, rendue "
                f"par {SOURCE_WIZARD}"
            )
        for ligne in rendues:
            if normalize(ligne) not in normalize(corps):
                constats.append(
                    f"{PAGE} : la section « {TITRE_EXEMPLE} » ne cite pas la ligne rendue « {ligne} » ; "
                    f"attendu cette ligne, lue apres l'edition « {valeur} » sur « {adresse} » "
                    f"({SOURCE_WIZARD})"
                )

    # 2. Le chemin d'arrivee, l'ecran d'arrivee et le libelle de lancement, cites depuis le rendu.
    ligne_avance = ""
    for ligne in _lignes_du_corps(app.test_client().get("/optimize/quick/classe")):
        if MOTIF_LIGNE_AVANCE.match(ligne.strip()) is not None:
            ligne_avance = ligne.strip()
    if not ligne_avance or normalize(ligne_avance) not in normalize(corps):
        constats.append(
            f"{PAGE} : la section « {TITRE_EXEMPLE} » ne cite pas « {ligne_avance} » ; attendu la "
            f"ligne qui ouvre le wizard, lue au rendu des trois questions ({SOURCE_ROUTES})"
        )

    recap = app.test_client().get("/optimize/wizard/recap")
    titre_recap = STEP_TITLES.get("recap", "")
    if recap.status_code != 200 or normalize(titre_recap) not in normalize(_entete(recap)):
        constats.append(
            f"l'ecran d'arrivee « /optimize/wizard/recap » repond {recap.status_code} ; attendu le "
            f"titre « {titre_recap} » — c'est l'ecran que l'exemple annonce ({SOURCE_ROUTES})"
        )
    if normalize(titre_recap) not in normalize(corps):
        constats.append(
            f"{PAGE} : la section « {TITRE_EXEMPLE} » ne cite pas l'ecran d'arrivee « {titre_recap} » ; "
            f"attendu cet ecran, rendu par {SOURCE_ROUTES} et produit par {SOURCE_WIZARD} (STEP_TITLES)"
        )

    commandes = _couples_de_commandes(_lignes_du_corps(recap))
    if "GO" not in commandes:
        constats.append(
            f"{PAGE} : {MOTIF_EXEMPLE} — le corps du recapitulatif n'annonce pas la commande « GO » ; "
            f"attendu le libelle de lancement rendu par {SOURCE_WIZARD} (body_recap)"
        )
    else:
        lancement = f"GO = {commandes['GO']}"
        if normalize(lancement) not in normalize(corps):
            constats.append(
                f"{PAGE} : la section « {TITRE_EXEMPLE} » ne cite pas « {lancement} » ; attendu le "
                f"libelle de lancement, lu dans le corps du recapitulatif ({SOURCE_WIZARD})"
            )

    # 3. Le refus de format de la ligne editee : c'est le message du code, pas un texte de memoire.
    edition = app.test_client()
    edition.get("/optimize/wizard/caracs")
    edition.post("/optimize/wizard/caracs", data={"cmd": "4"})
    forme = _forme_d_edition(_lignes_du_corps(edition.get("/optimize/wizard/caracs")))
    edition.post("/optimize/wizard/caracs", data={"value": "1 2 3"})
    refus = _message_de_statut(_statut(edition.get("/optimize/wizard/caracs")))
    if not forme or refus != forme:
        constats.append(
            f"{PAGE} : {MOTIF_EXEMPLE} — le refus d'une saisie de trois nombres vaut « {refus} » ; "
            f"attendu « {forme} », la forme de l'ecran edite, affichee juste au-dessus du refus par "
            f"{SOURCE_ROUTES}"
        )
    if normalize(forme) not in normalize(texte):
        constats.append(
            f"{PAGE} : {MOTIF_EXEMPLE} — la forme « {forme} » rendue par le sous-ecran n'est citee "
            f"nulle part dans la page ; attendu la forme de la ligne editee, lue au rendu "
            f"({SOURCE_ROUTES})"
        )

    # 4. Aucune commande destructrice dans un parcours recommande (D-22/D-23, D-61).
    if COMMANDE_DESTRUCTRICE.search(corps):
        constats.append(
            f"{PAGE} : la section « {TITRE_EXEMPLE} » porte une commande destructrice ; attendu un "
            f"parcours recommande sans aucune commande de destruction de donnees ({MOTIF_EXEMPLE})"
        )

    assert not constats, (
        f"{PAGE} : constats sur l'exemple guide : "
        + " ; ".join(constats)
        + f" ; attendu les trois editions de l'{MOTIF_EXEMPLE} rejouees sur le rendu de {SOURCE_WIZARD}, "
        f"leurs lignes rendues citees par la section « {TITRE_EXEMPLE} », et le libelle de lancement lu "
        f"dans le corps du recapitulatif"
    )


def test_touches_et_commandes_par_etape(docs_dir: Path, app, normalize, section) -> None:
    """Les couples touche/libelle et les commandes du recapitulatif sont lus au rendu (D-64, WIZ-02).

    Les couples sont exiges **par etape**, extremites comprises : l'etape 1 rend `Page prec` et
    `Suivant`, les etapes 2 a 8 rendent `Precedent` et `Suivant`, l'etape 9 rend `Precedent` et
    `Page suiv`, et `ESC` porte `Retour` sur les neuf. Aucune assertion de ce module n'exige
    `Precedent`/`Suivant` sur les neuf etapes : une telle assertion contredirait le rendu des
    extremites et l'affirmation de `docs/parcours-simplifie.md:140` (D-64, Pitfall 2).

    Les commandes du recapitulatif sont prouvees par l'**action** — `RESET`, `SAVES` et les chiffres
    `1` a `8` sont postes et leurs redirections comparees a `WIZARD_STEPS[n - 1]` lu au code — et par
    le **rendu** : les quatre libelles du corps sont exiges dans la page. `GO` est le seul qui n'est
    jamais poste, car il execute le solveur (`{SOURCE_ROUTES}`) : seule sa citation est controlee.

    Limite nommee (sonde d'aretes WIZ-02, ligne `unclassified`, qui reste `unresolved`) : ce controle
    porte sur les couples `F7`/`F8`/`ESC` des neuf etapes et sur les quatre commandes du corps du
    recapitulatif. Aucune exhaustivite de la surface des touches n'est revendiquee : une touche rendue
    hors de ces couples resterait hors du controle.
    """
    texte = _texte_page(docs_dir)
    corps = section(texte, TITRE_TOUCHES, PAGE)
    constats: list[str] = []

    # 1. Les couples touche/libelle, etape par etape, lus dans la barre que le rendu produit.
    citees = _touches_citees(corps)
    if sorted(citees) != list(range(1, len(WIZARD_STEPS) + 1)):
        constats.append(
            f"{PAGE} : la table des touches couvre les etapes {sorted(citees)} ; attendu les "
            f"{len(WIZARD_STEPS)} etapes numerotees 1 a {len(WIZARD_STEPS)}, une ligne par etape "
            f"({MOTIF_TOUCHE})"
        )
    for numero, etape in enumerate(WIZARD_STEPS, start=1):
        rendues = dict(_touches(app.test_client().get(f"/optimize/wizard/{etape}")))
        citee = citees.get(numero, {})
        for touche in ("F7", "F8", "ESC"):
            attendu = rendues.get(touche, "")
            cite = citee.get(touche, "")
            if attendu != cite:
                constats.append(
                    f"{PAGE} : {MOTIF_TOUCHE} de l'etape {numero} ({etape}) — la touche « {touche} » "
                    f"est citee « {cite} » ; attendu « {attendu} », lu dans la barre de raccourcis "
                    f"rendue par /optimize/wizard/{etape} ({SOURCE_ROUTES})"
                )

    # 2. Les quatre libelles annonces par le corps du recapitulatif, exiges dans la section.
    recap = app.test_client().get("/optimize/wizard/recap")
    annoncees = _couples_de_commandes(_lignes_du_corps(recap))
    citees_commandes = {
        trouve.group("cle").strip(): trouve.group("verbe").strip()
        for trouve in MOTIF_COMMANDE_CITEE.finditer(corps)
    }
    if not annoncees:
        constats.append(
            f"{PAGE} : {MOTIF_COMMANDE_RECAP} — le corps du recapitulatif n'annonce aucune commande "
            f"sous la forme `CLE = VERBE` ; attendu les libelles de {SOURCE_WIZARD} (body_recap)"
        )
    if annoncees != citees_commandes:
        constats.append(
            f"{PAGE} : {MOTIF_COMMANDE_RECAP} — la section « {TITRE_TOUCHES} » cite "
            f"{citees_commandes} ; attendu {annoncees}, les libelles lus dans le corps du "
            f"recapitulatif ({SOURCE_WIZARD})"
        )

    # 3. Les commandes agissantes : RESET, SAVES et les chiffres, postes puis compares a leur cible.
    for commande, attendue, motif in (
        ("RESET", "/optimize/wizard/slots", MOTIF_COMMANDE_RECAP),
        ("saves", "/saves", MOTIF_COMMANDE_RECAP),
    ):
        client = app.test_client()
        client.get("/optimize/wizard/recap")
        reponse = client.post("/optimize/wizard/recap", data={"cmd": commande})
        cible = reponse.headers.get("Location", "")
        if reponse.status_code != 302 or cible != attendue:
            constats.append(
                f"{PAGE} : {motif} — la saisie « {commande} » du recapitulatif repond "
                f"{reponse.status_code} vers « {cible} » ; attendu « {attendue} », la redirection "
                f"posee par {SOURCE_ROUTES}"
            )

    for chiffre in range(1, len(WIZARD_STEPS)):
        attendue = f"/optimize/wizard/{WIZARD_STEPS[chiffre - 1]}"
        client = app.test_client()
        client.get("/optimize/wizard/recap")
        reponse = client.post("/optimize/wizard/recap", data={"cmd": str(chiffre)})
        cible = reponse.headers.get("Location", "")
        if reponse.status_code != 302 or cible != attendue:
            constats.append(
                f"{PAGE} : {MOTIF_COMMANDE_NUMERIQUE} — le chiffre « {chiffre} » du recapitulatif "
                f"repond {reponse.status_code} vers « {cible} » ; attendu « {attendue} », soit "
                f"WIZARD_STEPS[n - 1] lu dans {SOURCE_WIZARD}"
            )

    # 4. Une saisie hors liste : la liste rendue dans la ligne de statut, exigee dans la page.
    refus = app.test_client()
    refus.get("/optimize/wizard/recap")
    reponse = refus.post("/optimize/wizard/recap", data={"cmd": "9"})
    cible = reponse.headers.get("Location", "")
    if reponse.status_code != 302 or not cible.startswith("/optimize/wizard/recap"):
        constats.append(
            f"{PAGE} : {MOTIF_COMMANDE_RECAP} — la saisie « 9 » du recapitulatif repond "
            f"{reponse.status_code} vers « {cible} » ; attendu un retour sur le recapitulatif, "
            f"la saisie etant refusee ({SOURCE_ROUTES})"
        )
    liste = _message_de_statut(_statut(refus.get("/optimize/wizard/recap")))
    if normalize(liste) not in normalize(corps):
        constats.append(
            f"{PAGE} : {MOTIF_COMMANDE_RECAP} — la section « {TITRE_TOUCHES} » ne cite pas le refus "
            f"rendu « {liste} » ; attendu la liste que {SOURCE_ROUTES} affiche pour une saisie hors "
            f"des commandes du recapitulatif"
        )

    assert not constats, (
        f"{PAGE} : constats sur les touches et les commandes : "
        + " ; ".join(constats)
        + f" ; attendu les {MOTIF_TOUCHE} par etape lus au rendu de {SOURCE_ROUTES}, les "
        f"{MOTIF_COMMANDE_RECAP} du corps du recapitulatif citees, et l'action de {MOTIF_COMMANDE_NUMERIQUE} "
        f"comparee a WIZARD_STEPS"
    )


def test_data_locale_non_modifiee_autour_des_rendus(docs_dir: Path, app) -> None:
    """La base locale du depot est intacte autour des rendus reels de ce module (T-04-08).

    Limite nommee, ecrite ici pour ne pas etre lue comme une preuve plus large qu'elle ne l'est :
    `tests/conftest.py` construit sa propre base sous `tmp_path/data` et aucun test de la suite
    n'ouvre `.data/dofus.sqlite3`, donc cette re-mesure locale ne peut pas detecter une ecriture faite
    par un **autre** module ; elle prouve que **ce module** n'y touche pas pendant qu'il rend les
    ecrans du wizard. Le controle qui possede ce pouvoir est la mesure avant/apres autour de la suite
    entiere, executee par la verification du plan. Le fichier est lu, jamais ecrit, et un `skip`
    explicite remplace un faux vert quand la base est absente.
    """
    chemin = docs_dir.parent.joinpath(*BASE_LOCALE)
    if not chemin.exists():
        pytest.skip(MOTIF_BASE_ABSENTE)

    avant = _empreinte(chemin)
    constats: list[str] = []

    client = app.test_client()
    for numero, etape in enumerate(WIZARD_STEPS, start=1):
        rendu = client.get(f"/optimize/wizard/{etape}")
        if rendu.status_code != 200:
            constats.append(
                f"l'ecran « {etape} » (etape {numero}) repond {rendu.status_code} ; attendu 200, sans "
                f"quoi la seconde empreinte serait prise sans qu'aucun rendu n'ait eu lieu "
                f"({SOURCE_ROUTES})"
            )

    apres = _empreinte(chemin)
    if avant != apres:
        constats.append(
            f"la base locale a change pendant les rendus du wizard : avant {avant}, apres {apres} ; "
            f"attendu une empreinte identique (taille, mtime_ns, sha256) — le harnais n'ecrit rien "
            f"sous .data/ ({MOTIF_EMPREINTE_CHANGEE})"
        )

    assert not constats, (
        f"{PAGE} : constats sur l'empreinte de la base locale : "
        + " ; ".join(constats)
        + f" ; attendu des rendus de {SOURCE_ROUTES} qui ne touchent ni ne modifient "
        f".data/dofus.sqlite3"
    )


def test_copie_figee_signalee_par_le_detecteur(docs_dir: Path, app, normalize) -> None:
    """La copie figee du texte obsolete reste signalee par le **meme** detecteur (D-59b, WIZ-03).

    C'est la seconde moitie de la preuve du critere 5 : le plan 04-03 corrigera l'aiguillage livre et
    obtiendra le vert, mais le detecteur garde sa morsure parce qu'il est juge ici sur une copie figee
    conservee sous `tests/`. Les trois formes nommees doivent y etre presentes, dont le libelle
    **rendu** du menu d'optimisation et le libelle **rendu** de `F7` : un test qui se contenterait de
    « la liste n'est pas vide » ne prouverait pas que les trois formes sont couvertes.

    Limite honnete, ecrite ici comme dans le module : le detecteur couvre trois formes nommees et ne
    revendique aucune exhaustivite (D-58). C'est la **presence de chaque forme** qui est exigee,
    jamais un compte de constats.
    """
    faits = _faits_du_rendu(app, normalize)
    constats = renvois_obsoletes(_lire_fixture(), faits)
    chemin = "/".join(FIXTURE_OBSOLETE)
    libelle_optimisation = faits["menus"][faits["menu_optimisation"]]
    libelle_f7 = faits["filtres"][7]
    manques: list[str] = []

    if len(constats) < 3:
        manques.append(
            f"la copie figee ne rend que {len(constats)} constat(s) ; attendu au moins trois, "
            f"couvrant les trois formes nommees ({chemin})"
        )
    for motif in MOTIFS_RENVOI:
        if not any(motif in constat for constat in constats):
            manques.append(
                f"{motif} : aucun constat de cette forme sur la copie figee ({chemin}) ; attendu "
                f"chaque forme nommee presente au moins une fois — c'est cette copie qui rend le "
                f"rouge du critere 5 relancable (D-59b)"
            )
    if not any(
        MOTIF_RENVOI_MENU in constat and libelle_optimisation in constat for constat in constats
    ):
        manques.append(
            f"{MOTIF_RENVOI_MENU} : aucun constat ne nomme le libelle rendu du menu d'optimisation "
            f"« {libelle_optimisation} » ({chemin}) ; attendu ce libelle, lu au rendu de GET / et "
            f"construit par {SOURCE_ROUTES}"
        )
    if not any(MOTIF_RENVOI_FILTRE in constat and libelle_f7 in constat for constat in constats):
        manques.append(
            f"{MOTIF_RENVOI_FILTRE} : aucun constat ne nomme le libelle rendu de F7 "
            f"« {libelle_f7} » ({chemin}) ; attendu ce libelle, lu sur /optimize/wizard/slots et "
            f"produit par {SOURCE_ROUTES} et {SOURCE_SPEC}"
        )

    assert not manques, (
        f"{chemin} : la copie figee des extraits obsoletes n'est pas signalee comme attendu : "
        + " ; ".join(manques)
        + f" ; constats rendus : {' | '.join(constats)} ; attendu la copie figee signalee par les "
        f"trois formes nommees (D-59b) — {LIMITE_HONNETE}"
    )


def test_renvois_legitimes_non_signales(docs_dir: Path, app, normalize) -> None:
    """Aucun renvoi legitime n'est signale : la garde anti-faux-positif de D-60 (WIZ-03).

    Quatre textes temoins, ecrits en constantes du module : le texte corrige type que le plan 04-03
    ecrira (arbre de menu **aux formes que D-47 exige** — `4. OPTIMISATION`, `3. PANOPLIES`,
    `5. SYSTEME` —, invitation correcte a taper le numero du menu d'optimisation **mesure**, et les
    deux liens de navigation), une phrase qui porte `F7` **et** son libelle rendu, une phrase negative
    sur l'arrivee, et un renvoi en prose ordinaire. Le premier temoin est aussi la preuve que la forme
    (a) accepte les abreviations de D-47 : sans cette tolerance, l'aiguillage corrige serait declare
    fautif et le vert du critere 5 deviendrait inatteignable.

    Limite honnete : ce controle porte sur quatre textes temoins, pas sur tous les textes corrects
    possibles (D-58). Un detecteur qui crie au loup serait pire que pas de detecteur, mais quatre
    temoins ne prouvent pas l'absence de tout faux positif ailleurs.
    """
    faits = _faits_du_rendu(app, normalize)
    fautifs: list[str] = []
    for nom, temoin in TEMOINS_LEGITIMES:
        trouves = renvois_obsoletes(temoin, faits)
        if trouves:
            fautifs.append(f"temoin legitime « {nom} » signale a tort : " + " | ".join(trouves))

    assert not fautifs, (
        f"le detecteur signale un renvoi legitime, ce que D-60 interdit : "
        + " ; ".join(fautifs)
        + f" ; attendu zero constat sur les quatre temoins legitimes — le texte corrige type ecrit "
        f"l'arbre aux formes de D-47 et tape le numero `{faits['menu_optimisation']}` mesure, la "
        f"phrase de filtre nomme « {faits['filtres'][7]} », la phrase negative ne doit pas etre "
        f"signalee (D-58, D-60)"
    )


def test_aiguillage_sans_renvoi_obsolete(docs_dir: Path, app, normalize) -> None:
    """`GUIDE_WIZARD.md` ne porte aucun renvoi obsolete — **ROUGE jusqu'au plan 04-03** (WIZ-03).

    Ce test applique le detecteur au fichier **livre**, sans le modifier : c'est l'etat rouge du
    critere 5 (D-59a). Le fichier est encore l'ancien guide, il cite donc encore le menu `3` pour
    l'optimisation, presente `F7` comme les armes a distance et annonce une arrivee « directe » dans
    le wizard. La correction appartient au plan 04-03 (vague 4), qui produira le vert ; **ce plan ne
    touche jamais le fichier** et le controle n'est jamais affaibli pour obtenir un vert.

    Ce que le test prouve quand il passe : le detecteur ne signale **rien** sur l'aiguillage corrige.
    Il ne prouve pas — et ne revendique pas — qu'aucun autre renvoi obsolete n'existe ailleurs :
    trois formes nommees sont couvertes, aucune exhaustivite n'est revendiquee (D-58/D-26). Chaque
    constat relaie la valeur fautive, la valeur attendue lue au rendu et le **fichier de code
    producteur** (`{SOURCE_ROUTES}` pour le menu et l'arrivee, `{SOURCE_SPEC}` pour le couple
    `F6`/`F7`), un constat sans producteur etant un defaut de forme a corriger (D-13, D-65).
    """
    chemin = RACINE_DEPOT / GUIDE_WIZARD
    if not chemin.is_file():
        raise AssertionError(
            f"{GUIDE_WIZARD} : aiguillage introuvable ({chemin}) ; attendu le fichier de la racine "
            f"que le perimetre WIZ-03 designe, decrit par .planning/PROJECT.md"
        )
    texte = chemin.read_text(encoding="utf-8")
    faits = _faits_du_rendu(app, normalize)
    constats = renvois_obsoletes(texte, faits)

    assert not constats, (
        f"{GUIDE_WIZARD} : renvois obsoletes signales sur la page controlee : "
        + " ; ".join(constats)
        + f" ; attendu un aiguillage sans renvoi vers un menu, un filtre ou une arrivee disparus, "
        f"chaque constat nommant sa valeur fautive, la valeur attendue lue au rendu et son fichier "
        f"de code producteur ({SOURCE_ROUTES} pour le menu et l'arrivee, {SOURCE_SPEC} pour le "
        f"couple F6/F7) — {LIMITE_HONNETE} ; le vert de ce controle appartient au plan 04-03, qui "
        f"corrige l'aiguillage, jamais a un affaiblissement du detecteur"
    )


