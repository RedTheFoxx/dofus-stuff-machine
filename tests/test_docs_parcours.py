"""Ancrage de la page `docs/parcours-simplifie.md` sur le rendu reel du parcours simplifie.

Le contrat va du rendu vers la page : les trois ecrans du parcours simplifie sont rendus par le
client de test Flask, en processus, sur la fixture `app` de `tests/conftest.py` (D-32), puis les
libelles lus dans les lignes du corps et dans la ligne de statut sont compares a ceux que la page
cite. Chaque entree citee par la page est rejouee sur le rendu et classee par ce que l'outil fait
reellement : une entree acceptee redirige ou atteint l'appel d'optimisation, une entree refusee
re-rend le meme ecran avec le message attendu au debut de la ligne de statut. Aucun serveur n'est
lance, aucun socket n'est ouvert, le programme du produit n'est jamais execute et rien n'est ecrit
sous `.data/` : la fixture `app` construit sa propre base dans un dossier temporaire.

Limite nommee : la garde `ast` de ce module est une demonstration statique et indirecte. Elle dit
ce que ce module importe et appelle, pas ce qu'un autre chemin ferait. La preuve directe qu'aucune
ecriture n'a lieu sous `.data/` est la mesure d'empreinte prise autour de la suite entiere
(plan 03-04). Le seul appel au produit qui soit court-circuite est l'etape 3 : elle est patchee
pour ne pas lancer le solveur, dont le resultat n'est ni deterministe ni utile ici.

Limite nommee (plan 03-03) : le comportement de sauvegarde du navigateur (compteur, eviction, purge,
hydratation de la liste) n'est **pas** executable dans cet environnement — ni `localStorage`, ni
`shift`. Le module controle donc des **litteraux** lus dans
`dofus_stuff/web/static/js/terminal.js` (la cle de stockage et la valeur de la limite) et les
libelles rendus par le client : cela prouve que la page et le code ne divergent pas, **pas** que le
navigateur se comporte ainsi. L'export Dofusbook, lui, est eprouve par une surface publique pure
(`build_dofusbook_url`) dont la charge utile est decodee (`base64` + `msgpack`).
"""

from __future__ import annotations

import ast
import base64
import importlib
import re
from pathlib import Path
from unittest.mock import patch

import msgpack

from dofus_stuff.optimize.recommend import CLASSES, ELEMENTS
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

# Contrat de titres de la page, fige pour toute la phase : chaque titre est ecrit au caractere
# pres, le helper `section` de `tests/conftest.py` ne normalisant pas un titre. Les titres des
# plans 03-02 a 03-04 sont poses des maintenant pour qu'une derive de titre soit vue au plus tot.
TITRE_SOURCE = "## Source de vérité"
TITRE_CLASSE = "## Question 1/3 : la classe"
TITRE_ELEMENTS = "## Question 2/3 : les éléments"
TITRE_NIVEAU = "## Question 3/3 : le niveau"
TITRE_RESULTAT = "## Lire le résultat"
TITRE_SAUVEGARDE = "## Sauvegarder et exporter"
TITRE_SUPPOSE = "## Ce que l'outil suppose"
TITRE_LIMITES = "## Ce que l'outil ne fait pas"

SOUS_TITRE_ACCEPTEES = "### Entrées acceptées"
SOUS_TITRE_REFUSEES = "### Erreurs et refus"

# Une entree de question est ecrite dans sa sous-section, jamais en prose : c'est la table qui est
# lue, une phrase n'etant pas une entree epinglee.
ETAPES = (
    ("classe", TITRE_CLASSE),
    ("elements", TITRE_ELEMENTS),
    ("niveau", TITRE_NIVEAU),
)

# Chemin de code cite entre accents graves (meme motif que `tests/test_docs_code_anchor.py:25`) :
# il porte sur la page entiere, pas seulement sur le bloc « Source de verite ».
CHEMIN_CITE = re.compile(r"`(?P<chemin>[\w./-]+\.(?:py|toml|js|md|json|sql))`")

# Couple numero <-> libelle tel qu'il est rendu : `routes.py:989` ecrit `f"{j + 1:2}. {CLASSES[j]:12}"`
# et `routes.py:993` ecrit `1. Terre    2. Feu    3. Eau    4. Air`. Le motif est applique ligne
# par ligne avec `finditer`, une ligne rendue portant jusqu'a trois couples separes par des espaces.
MOTIF_COUPLE_RENDU = re.compile(r"(?P<numero>\d{1,2})\.\s+(?P<libelle>[A-Za-zÀ-ÿ][A-Za-zÀ-ÿ' -]*)")

# Marqueurs du gabarit reel (`dofus_stuff/web/templates/screen.html:30-49`) : le corps visible est
# encadre par `id="body"` et par la seule ligne de statut, qui porte les messages d'erreur.
MARQUEUR_CORPS = 'id="body">'
MARQUEUR_STATUT = '<div class="row status'
LIGNE_CORPS = re.compile(r'<div class="row">(.*?)</div>', re.S)
LIBELLE_SAISIE = re.compile(r'<label class="input-label meta">(.*?)</label>', re.S)
TOUCHE_BARRE = re.compile(
    r'<span class="fkey-key meta">([^<]*)</span>'
    r'<span class="fkey-eq meta">=</span>'
    r'<span class="fkey-label">([^<]*)</span>'
)

# Table epinglee des entrees du parcours simplifie, mesurees sur le rendu : (etape, valeur, attendu).
# `attendu` vaut soit ("redirige", cible), soit ("refuse", debut du message de la ligne de statut),
# soit ("optimisation", niveau retenu) pour un niveau accepte, ou le solveur est court-circuite.
ENTREES_MESUREES = [
    # Question 1/3 : nom compare apres normalisation des accents et de la casse, ou numero 1 a 19.
    ("classe", "Cra", ("redirige", "/optimize/quick/elements")),
    ("classe", "crâ", ("redirige", "/optimize/quick/elements")),
    ("classe", "1", ("redirige", "/optimize/quick/elements")),
    ("classe", "19", ("redirige", "/optimize/quick/elements")),
    ("classe", "019", ("redirige", "/optimize/quick/elements")),
    ("classe", " 3 ", ("redirige", "/optimize/quick/elements")),
    ("classe", "eliotrop", ("refuse", "Saisissez le nom ou le numéro de votre classe.")),
    ("classe", "0", ("refuse", "Saisissez le nom ou le numéro de votre classe.")),
    ("classe", "20", ("refuse", "Saisissez le nom ou le numéro de votre classe.")),
    # Question 2/3 : separateurs espace, virgule ou plus ; chiffres 1 a 4 ; `multi` seul.
    ("elements", "terre", ("redirige", "/optimize/quick/niveau")),
    ("elements", "terre air", ("redirige", "/optimize/quick/niveau")),
    ("elements", "terre,air", ("redirige", "/optimize/quick/niveau")),
    ("elements", "terre+air", ("redirige", "/optimize/quick/niveau")),
    ("elements", "1 3", ("redirige", "/optimize/quick/niveau")),
    ("elements", "multi", ("redirige", "/optimize/quick/niveau")),
    ("elements", "multi terre", ("refuse", "Exemple : feu, terre air, ou multi.")),
    ("elements", "arbre", ("refuse", "Exemple : feu, terre air, ou multi.")),
    ("elements", "5", ("refuse", "Exemple : feu, terre air, ou multi.")),
    # Question 3/3 : entier de 1 a 200 ; `AVANCE` ouvre les reglages detailles au lieu de calculer.
    ("niveau", "150", ("optimisation", 150)),
    ("niveau", "050", ("optimisation", 50)),
    ("niveau", "200", ("optimisation", 200)),
    ("niveau", "AVANCE", ("redirige", "/optimize/wizard/recap")),
    ("niveau", "201", ("refuse", "Saisissez un niveau entre 1 et 200.")),
    ("niveau", "0", ("refuse", "Saisissez un niveau entre 1 et 200.")),
    ("niveau", "50.0", ("refuse", "Saisissez un niveau entre 1 et 200.")),
]

# Listes epinglees par etape : la table de la page ne peut citer que ces valeurs, et elle doit les
# citer toutes. Une liste vide rendrait la regle infalsifiable : le controle l'exige donc non vide.
VALEURS_ACCEPTEES = {
    "classe": ("Cra", "crâ", "1", "19", "019", " 3 "),
    "elements": ("terre", "terre air", "terre,air", "terre+air", "1 3", "multi"),
    "niveau": ("150", "050", "200", "AVANCE"),
}
VALEURS_REFUSEES = {
    "classe": ("eliotrop", "0", "20"),
    "elements": ("multi terre", "arbre", "5"),
    "niveau": ("201", "0", "50.0"),
}

# Messages de refus reellement rendus, un par etape : ils sont exiges au debut de la ligne de statut
# et cites au mot pres dans la sous-section « Erreurs et refus » de la section correspondante.
MESSAGES_REFUS = {
    "classe": ("Saisissez le nom ou le numéro de votre classe.",),
    "elements": ("Exemple : feu, terre air, ou multi.",),
    "niveau": ("Saisissez un niveau entre 1 et 200.",),
}

# Rappel de la touche attendue, telle qu'elle est rendue dans la ligne de statut du refus.
INDICE_ENTREE = {
    "classe": "ENTREE=SUIVANT",
    "elements": "ENTREE=SUIVANT",
    "niveau": "ENTREE=CALCULER",
}

# Menus numerotes rendus, avec la ligne du code qui les produit : la cle est le nom de l'etape de
# l'URL, la valeur attendue est le nombre de numeros du menu.
MENUS_RENDUS = (
    ("classe", TITRE_CLASSE, 989, len(CLASSES)),
    ("elements", TITRE_ELEMENTS, 993, len(ELEMENTS)),
)
LIGNE_MENU_CLASSE = 989
LIGNE_MENU_ELEMENTS = 993

# Phrase epinglee de la page et module du parcours en ligne de commande dont les litteraux sont
# sondes : la page affirme ce que ce module ne contient pas (D-33). Le mot est cherche entier,
# apres normalisation des accents et de la casse.
MOTIF_PAGE_CLI = "ne pose pas ces trois questions"
SOURCE_PROFIL = "dofus_stuff/optimize/profile_input.py"
MOTS_PROFIL_INTERDITS = (r"\bclasses?\b", r"\belements?\b")

# --- Resultat : pagination, emplacement du calcul, libelles de slot (plan 03-02) ---

# Session du resultat : les quatre elements. Mesure : la fixture rend alors trois pages et les
# diagnostics tombent en page 2/3, jamais sur la derniere page — d'ou l'assertion POSITIONNELLE.
ETAT_RESULTAT = {"classe": "Cra", "elements": list(ELEMENTS)}
NIVEAU_RESULTAT = "200"

# Carte de pagination lue dans la ligne de statut, jamais dans le corps (dofus_stuff/web/routes.py:145).
MOTIF_PAGE_STATUT = re.compile(r"PAGE (?P<page>\d+)/(?P<total>\d+)")

# Attributs de la coquille qui doivent s'accorder avec la ligne de statut (screen.html:13-14,19).
ATTRIBUTS_COQUILLE = ("data-body-page", "data-body-total", "data-mode")

# Les trois libelles du bloc de diagnostics (dofus_stuff/optimize/api.py:329,338-340), inseres en fin
# de resultat par dofus_stuff/optimize/api.py:432-434 pour le flux simplifie.
MARQUEURS_DIAGNOSTICS = ("Méthode : ", "Score : ", "Indice de recherche : ")
PHRASE_CATALOGUE = "Recherche sur une sélection du catalogue ; optimalité globale non garantie."
PREFIXE_EQUIPEMENT = "Équipement :"
PREFIXE_GREEDY = "Greedy:"
EMPLACEMENT_VIDE = "(vide)"

# Touches du resultat, mesurees : dofus_stuff/web/routes.py:137-141 produit « Page prec » / « Page
# suiv » pour le resultat ; « Precedent » / « Suivant » ne sont produits que pour le wizard avance.
TOUCHES_RESULTAT = (("F7", "Page prec"), ("F8", "Page suiv"), ("ESC", "Retour"))
TOUCHES_WIZARD = (("F7", "Precedent"), ("F8", "Suivant"))

# Tournure interdite par la reformulation enregistree d'ECR-2 : les diagnostics sont en fin de
# resultat, jamais « sur la derniere page » (mesure M6 : page 2/3 sur la fixture ; M11 : 6 puis 7
# pages sur la base reelle). Comparee apres normalisation, comme le reste de la page (D-11).
TOURNURE_DERNIERE_PAGE = "dernière page"

# Valeurs volatiles : une methode, un score, un indice ou un total figes dans la page seraient faux
# a la prochaine execution (mesure M11 : deux executions, deux methodes, six puis sept pages).
MOTIFS_VALEURS_VOLATILES = (
    r"Score :\s*\d",
    r"Indice de recherche :\s*\d",
    r"Greedy:\s*\d",
    r"Méthode :\s*[a-z]",
)

# Etat minimal de session par etape, ecrit sous la cle que la vue lit. La forme est mesuree et ne
# doit pas etre « simplifiee » : injecter les memes cles a la racine de la session laisse l'etat
# vide et fait repondre une redirection vers `/optimize` a tous les POST d'elements et de niveau,
# ce qui rendrait faux chaque verdict epingle.
ETATS_ETAPE = {
    "classe": {},
    "elements": {"classe": "Cra"},
    "niveau": {"classe": "Cra", "elements": ["terre"]},
}

# Limite mesuree, jamais presentee comme une protection du serveur : `maxlength="40"` est une
# contrainte du navigateur, `client.post` l'ignore, et le serveur n'a pas de borne de longueur
# propre sur la saisie du parcours simplifie.

# Racines dont un import, direct ou atteint par la cloture transitive, signalerait un risque reel :
# ouvrir la base, lancer un processus, ouvrir une socket, joindre le reseau. Le controle porte sur
# le risque, jamais sur une liste blanche de modules produit a tenir a jour.
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


def _libelle_saisie(reponse) -> str:
    """Texte interieur du libelle du champ de saisie, tel qu'il est rendu.

    Le jeton `CHOIX` apparait aussi dans la ligne de corps `VOTRE STUFF EN 3 CHOIX` : l'assertion
    porte donc sur le libelle du champ, jamais sur le corps.
    """
    trouve = LIBELLE_SAISIE.search(reponse.get_data(as_text=True))
    return "" if trouve is None else trouve.group(1)


def _couples_du_rendu(lignes: list[str]) -> dict[int, list[str]]:
    """Couples numero -> libelles lus dans des lignes rendues (une liste, jamais une valeur seule).

    Une liste et non une valeur unique : un numero rendu deux fois avec deux libelles differents
    doit rester visible au lieu d'etre ecrase par le dernier lu.
    """
    couples: dict[int, list[str]] = {}
    for ligne in lignes:
        for trouve in MOTIF_COUPLE_RENDU.finditer(ligne):
            couples.setdefault(int(trouve.group("numero")), []).append(trouve.group("libelle").strip())
    return couples


def _couples_de_section(texte: str, titre: str, section) -> dict[int, list[str]]:
    """Couples numero -> libelles cites par UNE section de la page.

    La lecture est scopee par section, jamais faite sur la page entiere : les menus des classes et
    des elements partagent les numeros 1 a 4, un dictionnaire global rapporterait donc quatre
    constats sur une page pourtant correcte. Le corps de section vient du helper partage `section`,
    qui refuse de lire une page sans la nommer (D-13).
    """
    return _couples_du_rendu(section(texte, titre, PAGE).splitlines())


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


def _valeurs_tableau(sous_texte: str) -> list[str]:
    """Premieres cellules des lignes de tableau, en-tete et ligne de separation exclues.

    Seule une cellule ecrite entre accents graves est une valeur : les lignes de tableau sont lues,
    jamais la prose, et l'en-tete comme la ligne de separation sont ainsi ecartes sans les nommer.
    """
    valeurs: list[str] = []
    for ligne in sous_texte.splitlines():
        ligne = ligne.strip()
        if not ligne.startswith("|"):
            continue
        cellules = ligne.split("|")[1:-1]
        if not cellules:
            continue
        premiere = cellules[0].strip()
        if len(premiere) >= 2 and premiere.startswith("`") and premiere.endswith("`"):
            valeurs.append(premiere[1:-1])
    return valeurs


def test_trois_questions_et_avance_rendus(docs_dir: Path, app, normalize, section) -> None:
    """Les trois questions et `AVANCE` sont rendues telles quelles et citees par la page (V1)."""
    texte = _texte_page(docs_dir)
    client = app.test_client()
    ecran_classe = client.get("/optimize/quick/classe")
    client.post("/optimize/quick/classe", data={"cmd": "Cra"})
    ecran_elements = client.get("/optimize/quick/elements")
    client.post("/optimize/quick/elements", data={"cmd": "terre"})
    ecran_niveau = client.get("/optimize/quick/niveau")

    ecrans = [
        (TITRE_CLASSE, "1/3 - Quelle est votre classe ?", ecran_classe, len(CLASSES)),
        (TITRE_ELEMENTS, "2/3 - Quels éléments privilégier ?", ecran_elements, len(ELEMENTS)),
        (TITRE_NIVEAU, "3/3 - Quel est votre niveau ? (1 à 200)", ecran_niveau, None),
    ]
    avance = "AVANCE : personnaliser les réglages"

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
        if normalize(avance) not in lignes:
            constats.append(
                f"{PAGE} : le libelle « {avance} » n'est pas rendu dans les lignes du corps de "
                f"l'ecran « {titre} » ; attendu ce libelle sur les trois ecrans, produit par "
                f"{SOURCE_ROUTES}"
            )
        if normalize(_libelle_saisie(reponse)) != normalize("CHOIX : ["):
            constats.append(
                f"{PAGE} : le libelle du champ de saisie de l'ecran « {titre} » vaut "
                f"« {_libelle_saisie(reponse)} » ; attendu « CHOIX : [ », comme rendu par "
                f"{SOURCE_ROUTES}"
            )
        if ("ESC", "Retour") not in _touches(reponse):
            constats.append(
                f"{PAGE} : le couple de touche (« ESC », « Retour ») est absent de la barre de "
                f"l'ecran « {titre} » ; attendu ce couple rendu par {SOURCE_ROUTES}"
            )
        if couples_attendus is not None:
            rendus = _couples_du_rendu(_lignes_du_corps(reponse))
            if len(rendus) != couples_attendus:
                constats.append(
                    f"{PAGE} : l'ecran « {titre} » rend {len(rendus)} numeros de menu ; attendu "
                    f"{couples_attendus}, comme rendu par {SOURCE_ROUTES}"
                )
        corps_page = normalize(section(texte, titre, PAGE))
        if normalise not in corps_page:
            constats.append(
                f"{PAGE} : la section « {titre} » ne cite pas le libelle « {question} » ; attendu "
                f"ce libelle, rendu par {SOURCE_ROUTES}"
            )
        if normalize(avance) not in corps_page:
            constats.append(
                f"{PAGE} : la section « {titre} » ne cite pas le libelle « {avance} » ; attendu ce "
                f"libelle, rendu par {SOURCE_ROUTES}"
            )

    assert not constats, (
        f"{PAGE} : constats sur les trois questions du parcours simplifie : "
        + " ; ".join(constats)
        + f" ; attendu les trois questions et « {avance} » rendus par {SOURCE_ROUTES} et cites "
        f"par la section correspondante de la page"
    )


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


def test_entrees_citees_acceptees_et_refusees(docs_dir: Path, app, section, normalize) -> None:
    """Chaque entree citee par la page est rejouee sur le rendu et classee (V2, V3).

    Le rendu decide du verdict, jamais la page : une entree est acceptee si le POST redirige vers
    l'etape attendue (ou atteint l'appel d'optimisation, court-circuite ici), et refusee si l'ecran
    courant est re-rendu en 200 avec le message attendu au debut de la ligne de statut.
    """
    texte = _texte_page(docs_dir)
    constats: list[str] = []

    for etape, valeur, attendu in ENTREES_MESUREES:
        client = _client_etape(app, etape)
        if attendu[0] == "optimisation":
            with patch(
                "dofus_stuff.web.routes._run_optimize_and_redirect", return_value="computed"
            ) as court_circuit:
                reponse = client.post(f"/optimize/quick/{etape}", data={"cmd": valeur})
            if reponse.get_data(as_text=True) != "computed" or not court_circuit.called:
                constats.append(
                    f"{PAGE} : la saisie « {valeur} » de l'etape « {etape} » n'atteint pas l'appel "
                    f"d'optimisation ; attendu un niveau accepte par {SOURCE_ROUTES}"
                )
                continue
            with client.session_transaction() as session:
                etat = dict(session.get("recommendation_input") or {})
            if etat.get("niveau") != attendu[1]:
                constats.append(
                    f"{PAGE} : la saisie « {valeur} » de l'etape « {etape} » retient le niveau "
                    f"{etat.get('niveau')!r} ; attendu {attendu[1]!r}, comme lu par {SOURCE_ROUTES}"
                )
            continue

        reponse = client.post(f"/optimize/quick/{etape}", data={"cmd": valeur})
        if attendu[0] == "redirige":
            cible = reponse.headers.get("Location", "")
            if reponse.status_code != 302 or not cible.endswith(attendu[1]):
                constats.append(
                    f"{PAGE} : la saisie « {valeur} » de l'etape « {etape} » n'est pas acceptee "
                    f"({reponse.status_code} vers « {cible} ») ; attendu une redirection vers "
                    f"« {attendu[1]} », comme rendu par {SOURCE_ROUTES}"
                )
        else:
            statut = _statut(reponse)
            if reponse.status_code != 200 or not statut.startswith(attendu[1]):
                constats.append(
                    f"{PAGE} : la saisie « {valeur} » de l'etape « {etape} » n'est pas refusee comme "
                    f"la page le dit (statut {reponse.status_code}, ligne de statut « {statut} ») ; "
                    f"attendu 200 et une ligne de statut commencant par « {attendu[1]} », comme rendu "
                    f"par {SOURCE_ROUTES}"
                )

    for etape, titre in ETAPES:
        corps = section(texte, titre, PAGE)
        tables = (
            (SOUS_TITRE_ACCEPTEES, VALEURS_ACCEPTEES[etape], "acceptees"),
            (SOUS_TITRE_REFUSEES, VALEURS_REFUSEES[etape], "refusees"),
        )
        sous_textes: dict[str, str] = {}
        for sous_titre, _, _ in tables:
            try:
                sous_textes[sous_titre] = _sous_section(corps, sous_titre)
            except AssertionError as erreur:
                constats.append(str(erreur))
                sous_textes[sous_titre] = ""
        for sous_titre, epinglees, nom_regle in tables:
            if not epinglees:
                constats.append(
                    f"aucune saisie {nom_regle} epinglee pour l'etape « {etape} » ; attendu une "
                    f"liste non vide, une regle sans objet n'etant pas falsifiable"
                )
                continue
            citees = _valeurs_tableau(sous_textes[sous_titre])
            for valeur in citees:
                if valeur not in epinglees:
                    constats.append(
                        f"{PAGE} : la table « {sous_titre} » de la section « {titre} » cite la "
                        f"saisie « {valeur} », absente des saisies {nom_regle} mesurees de cette "
                        f"etape ({', '.join(epinglees)}) ; attendu une valeur rejouee sur le rendu "
                        f"de {SOURCE_ROUTES}"
                    )
            for valeur in epinglees:
                if valeur not in citees:
                    constats.append(
                        f"{PAGE} : la table « {sous_titre} » de la section « {titre} » ne cite pas "
                        f"la saisie « {valeur} » ; attendu chaque saisie {nom_regle} mesuree de "
                        f"cette etape, epinglee dans ce module"
                    )
        refus = normalize(sous_textes[SOUS_TITRE_REFUSEES])
        for message in MESSAGES_REFUS[etape]:
            if normalize(message) not in refus:
                constats.append(
                    f"{PAGE} : la sous-section « {SOUS_TITRE_REFUSEES} » de la section « {titre} » "
                    f"ne cite pas le message « {message} » ; attendu ce message, rendu par "
                    f"{SOURCE_ROUTES} au debut de la ligne de statut"
                )
        if normalize("ligne de statut") not in refus:
            constats.append(
                f"{PAGE} : la sous-section « {SOUS_TITRE_REFUSEES} » de la section « {titre} » ne "
                f"dit pas ou le lecteur lit le message ; attendu une mention de la ligne de statut, "
                f"seul emplacement du message rendu par {SOURCE_ROUTES}"
            )
        if normalize(INDICE_ENTREE[etape]) not in refus:
            constats.append(
                f"{PAGE} : la sous-section « {SOUS_TITRE_REFUSEES} » de la section « {titre} » ne "
                f"cite pas « {INDICE_ENTREE[etape]} » ; attendu la touche affichee par "
                f"{SOURCE_ROUTES} avec le message de refus"
            )

    assert not constats, (
        f"{PAGE} : constats sur les entrees du parcours simplifie : "
        + " ; ".join(constats)
        + f" ; attendu chaque entree citee par la page acceptee ou refusee par le rendu de "
        f"{SOURCE_ROUTES}, avec le message attendu au debut de la ligne de statut"
    )


def _reponse_menu(app, cle: str):
    """Ecran qui porte le menu numerote de l'etape : la question 1, ou la question 2 apres un POST."""
    client = app.test_client()
    if cle == "classe":
        return client.get("/optimize/quick/classe")
    client.post("/optimize/quick/classe", data={"cmd": "Cra"})
    return client.get("/optimize/quick/elements")


def _libelles_entre_guillemets(libelles: list[str]) -> str:
    """Libelles joints pour un message d'echec, chacun entre guillemets francais."""
    return " et ".join("« " + libelle + " »" for libelle in libelles)


def test_couples_numeros_libelles_par_section(docs_dir: Path, app, section, normalize) -> None:
    """Le couple numero <-> libelle des deux menus est compare au rendu, section par section (V4).

    La verite vient du rendu, jamais d'une liste ecrite de memoire : le menu des classes est rendu
    par `dofus_stuff/web/routes.py:989` et le menu des elements par `dofus_stuff/web/routes.py:993`.
    La comparaison est scopee par section, les deux menus partageant les numeros 1 a 4.
    """
    texte = _texte_page(docs_dir)
    constats: list[str] = []

    for cle, titre, ligne_code, attendus in MENUS_RENDUS:
        couples = _couples_du_rendu(_lignes_du_corps(_reponse_menu(app, cle)))
        if len(couples) != attendus:
            constats.append(
                f"{PAGE} : le menu rendu de l'etape « {cle} » compte {len(couples)} numeros ; attendu "
                f"{attendus}, comme rendu par {SOURCE_ROUTES}:{ligne_code} — une verite vide ou "
                f"tronquee ne doit pas rendre ce controle silencieusement vert"
            )
            continue
        cites = _couples_de_section(texte, titre, section)
        for numero, libelles in sorted(couples.items()):
            libelle_rendu = libelles[0]
            cites_ici = cites.get(numero, [])
            if len(cites_ici) > 1:
                constats.append(
                    f"{PAGE} : dans « {titre} », le numero {numero} est cite deux fois avec deux "
                    f"libelles differents ({_libelles_entre_guillemets(cites_ici)}) ; attendu le "
                    f"libelle « {libelle_rendu} » (couple « {numero}. {libelle_rendu} » tel que rendu "
                    f"par {SOURCE_ROUTES}:{ligne_code})"
                )
            elif not cites_ici:
                constats.append(
                    f"{PAGE} : dans « {titre} », le numero {numero} n'est associe a aucun libelle ; "
                    f"attendu le couple « {numero}. {libelle_rendu} » tel que rendu par "
                    f"{SOURCE_ROUTES}:{ligne_code}"
                )
            elif normalize(cites_ici[0]) != normalize(libelle_rendu):
                constats.append(
                    f"{PAGE} : dans « {titre} », le numero {numero} est associe au libelle "
                    f"« {cites_ici[0]} » ; attendu « {libelle_rendu} » (couple "
                    f"« {numero}. {libelle_rendu} » tel que rendu par {SOURCE_ROUTES}:{ligne_code})"
                )
        for numero in sorted(set(cites) - set(couples)):
            constats.append(
                f"{PAGE} : dans « {titre} », le numero {numero} n'existe dans aucun menu rendu "
                f"(« {SOURCE_ROUTES}:{LIGNE_MENU_CLASSE} » ni "
                f"« {SOURCE_ROUTES}:{LIGNE_MENU_ELEMENTS} ») ; attendu un numero des menus rendus"
            )

    total = _couples_du_rendu(texte.splitlines())
    occurrences = sum(len(libelles) for libelles in total.values())
    attendues = len(CLASSES) + len(ELEMENTS)
    if occurrences != attendues:
        constats.append(
            f"{PAGE} : la page cite {occurrences} couples numero <-> libelle ; attendu {attendues}, "
            f"soit les {len(CLASSES)} couples du menu des classes et les {len(ELEMENTS)} couples du "
            f"menu des elements, chacun une seule fois — un second exemplaire ferait deux verites a "
            f"tenir, rendues par {SOURCE_ROUTES}:{LIGNE_MENU_CLASSE} et "
            f"{SOURCE_ROUTES}:{LIGNE_MENU_ELEMENTS}"
        )

    assert not constats, (
        f"{PAGE} : constats sur les couples numero <-> libelle des deux menus : "
        + " ; ".join(constats)
        + f" ; attendu les couples des menus rendus par {SOURCE_ROUTES}:{LIGNE_MENU_CLASSE} et "
        f"{SOURCE_ROUTES}:{LIGNE_MENU_ELEMENTS}, compares section par section, la page non mutee "
        f"etant verte"
    )


# --- Correspondance libelle technique -> nom complet des emplacements (plan 03-02, ECR-1) ---

# Nom de la table de libelles rendue par le resultat, extraite par `ast` et jamais recopiee de
# memoire (D-42) : dofus_stuff/optimize/api.py:362-380.
TABLE_SLOTS = "display_slots"

# Nombre de libelles rendus, mesure sur la table `display_slots` : la garde empeche qu'une verite
# vide ou tronquee rende le controle silencieusement vert.
NOMBRE_SLOTS = 17

# Table epinglee (libelle, nom complet, fichier source, aiguille de ligne) : l'aiguille est le
# fragment qui porte le nom dans sa source, patron `LIBELLES_SOURCE` de
# tests/test_docs_code_anchor.py:61-74. Les noms complets sont recopies exactement du commentaire de
# `_GROUP_SLOTS` (dofus_stuff/web/dofusbook_export.py:26-37), codes Dofusbook inclus ; `prysma` est
# le seul emplacement absent de cet export, son nom venant de dofus_stuff/model/solver_spec.py:53.
SLOTS_MESURE = (
    ("amulet", "amulette (am)", SOURCE_DOFUSBOOK, '"amulet",'),
    ("ring_a", "anneaux (a1, a2)", SOURCE_DOFUSBOOK, '"ring_a"'),
    ("ring_b", "anneaux (a1, a2)", SOURCE_DOFUSBOOK, '"ring_b"'),
    ("belt", "ceinture (ce)", SOURCE_DOFUSBOOK, '"belt",'),
    ("boots", "bottes (bo)", SOURCE_DOFUSBOOK, '"boots",'),
    ("hat", "coiffe (ch)", SOURCE_DOFUSBOOK, '"hat",'),
    ("cape", "cape (ca)", SOURCE_DOFUSBOOK, '"cape",'),
    ("weapon", "arme (ar)", SOURCE_DOFUSBOOK, '"weapon",'),
    ("shield", "bouclier (br)", SOURCE_DOFUSBOOK, '"shield",'),
    ("dofus_1", "dofus", SOURCE_DOFUSBOOK, '"dofus_1"'),
    ("dofus_2", "dofus", SOURCE_DOFUSBOOK, '"dofus_2"'),
    ("dofus_3", "dofus", SOURCE_DOFUSBOOK, '"dofus_3"'),
    ("dofus_4", "dofus", SOURCE_DOFUSBOOK, '"dofus_4"'),
    ("dofus_5", "dofus", SOURCE_DOFUSBOOK, '"dofus_5"'),
    ("dofus_6", "dofus", SOURCE_DOFUSBOOK, '"dofus_6"'),
    ("pet", "familier/monture (fa)", SOURCE_DOFUSBOOK, '"pet",'),
    ("prysma", "prysmaradite", SOURCE_SPEC, '"prysmaradite",'),
)

# Libelle de tableau : seules les cellules ecrites entre accents graves sont des libelles, la prose
# n'en portant pas — les lignes du tableau sont lues, pas la prose.
LIBELLE_ENTRE_ACCENTS = re.compile(r"`([^`]+)`")

# Titre de la section qui porte la table de correspondance (posee par ce plan).
TITRE_CORRESPONDANCE = "## Correspondance des libellés"

# Tournures interdites par la reformulation enregistree d'ECR-1 : la regle de troncature `clip`
# existe (dofus_stuff/web/screens.py:14-20) mais ne se declenche pas dans ce flux (mesure M7 : zero
# ligne rendue du resultat ne porte de points de suspension, et les libelles sont completes par le
# format `f\"  {slot:8s} : \"`, jamais coupes).
TRONCATURE_PAGE = "libellé tronqué"
POINTS_DE_SUSPENSION = "…"


def _attribut(reponse, nom: str) -> str | None:
    """Valeur d'un attribut `data-*` de la coquille, ou None si l'attribut est absent du rendu."""
    trouve = re.search(rf'{nom}="(?P<valeur>[^"]*)"', reponse.get_data(as_text=True))
    return None if trouve is None else trouve.group("valeur")


def test_pagination_et_emplacement_du_calcul(app, docs_dir, section, normalize) -> None:
    """La carte de pagination et l'emplacement des diagnostics sont lus sur le rendu reel (V5, V6).

    Le controle est **positionnel**, jamais indexe sur un numero de page : sur la fixture les
    diagnostics tombent en page 2/3, et la meme execution sur la base reelle donne six puis sept
    pages pour la meme demande (mesures M6 et M11). Exiger la derniere page serait donc faux sur une
    implementation correcte — c'est la reformulation enregistree d'ECR-2. Aucune assertion ne porte
    sur `data-stuff-payload` ni sur la reponse entiere : la charge utile y porte tout le resultat sur
    chaque page, accents echappes, ce qui rendrait `« Méthode » in response.data` faux sur la page 1
    et `« Score » in response.data` vrai sur une page qui ne l'affiche pas (mesure M6).
    """
    texte = _texte_page(docs_dir)
    constats: list[str] = []

    # 1. Rendu reel du resultat : un seul calcul de solveur sur la fixture (mesure 0,29 s).
    client = app.test_client()
    with client.session_transaction() as session:
        session["recommendation_input"] = dict(ETAT_RESULTAT)
    reponse = client.post("/optimize/quick/niveau", data={"cmd": NIVEAU_RESULTAT})
    cible = reponse.headers.get("Location", "")
    if reponse.status_code != 302 or not cible.endswith("/optimize/result"):
        constats.append(
            f"{PAGE} : le calcul du niveau {NIVEAU_RESULTAT} repond {reponse.status_code} vers "
            f"« {cible} » ; attendu une redirection vers « /optimize/result », seul ecran qui rend "
            f"la carte de pagination et le bloc de diagnostics ({SOURCE_ROUTES})"
        )
    premiere = client.get("/optimize/result")
    if premiere.status_code != 200:
        constats.append(
            f"{PAGE} : l'ecran du resultat repond {premiere.status_code} ; attendu 200, rendu par "
            f"{SOURCE_ROUTES} (optimize_result)"
        )
    if constats:
        assert not constats, (
            f"{PAGE} : constat sur le rendu du resultat du parcours simplifie : " + " ; ".join(constats)
        )

    # 2. Carte de pagination dans la ligne de statut, coherente avec les attributs de la coquille.
    statut = _statut(premiere)
    trouve = MOTIF_PAGE_STATUT.search(statut)
    total: int | None = None
    if trouve is None:
        constats.append(
            f"{PAGE} : la ligne de statut « {statut} » de la premiere page ne porte pas la carte de "
            f"pagination « PAGE 1/<total> » ; attendu cette carte, posee par {SOURCE_ROUTES}:145 "
            f"quand le resultat depasse une page"
        )
    else:
        numero_page, total_lu = int(trouve.group("page")), int(trouve.group("total"))
        total = total_lu
        if numero_page != 1:
            constats.append(
                f"{PAGE} : la premiere page porte « PAGE {numero_page}/{total_lu} » ; attendu "
                f"« PAGE 1/<total> », comme rendu par {SOURCE_ROUTES}:145"
            )
        if total_lu < 2:
            constats.append(
                f"{PAGE} : le resultat de la fixture tient sur {total_lu} page(s) ; attendu au moins "
                f"2, faute de quoi la carte et les touches F7/F8 n'existent pas et ce controle ne "
                f"mesurerait rien ({SOURCE_ROUTES}:143-146)"
            )

    attendus_attributs = {
        "data-body-page": "1",
        "data-body-total": None if total is None else str(total),
        "data-mode": "result",
    }
    for nom in ATTRIBUTS_COQUILLE:
        valeur = _attribut(premiere, nom)
        if valeur is None:
            constats.append(
                f"{PAGE} : l'attribut « {nom} » est absent du rendu du resultat ; attendu cet "
                f"attribut de la coquille, renseigne par {SOURCE_ROUTES} (screen.html)"
            )
            continue
        attendu = attendus_attributs[nom]
        if attendu is not None and valeur != attendu:
            constats.append(
                f"{PAGE} : l'attribut « {nom} » vaut « {valeur} » ; attendu « {attendu} », coherent "
                f"avec la ligne de statut « {statut} » ({SOURCE_ROUTES}:143-150)"
            )

    if total is not None:
        statut_derniere = _statut(client.get(f"/optimize/result?page={total}"))
        if f"PAGE {total}/{total}" not in statut_derniere:
            constats.append(
                f"{PAGE} : la ligne de statut de la page {total} vaut « {statut_derniere} » ; "
                f"attendu le fragment « PAGE {total}/{total} », comme rendu par {SOURCE_ROUTES}:145"
            )

    # 3. Barre de touches du resultat, distincte de celle du wizard avance.
    touches = _touches(premiere)
    for touche in TOUCHES_RESULTAT:
        if touche not in touches:
            constats.append(
                f"{PAGE} : le couple de touche (« {touche[0]} », « {touche[1]} ») est absent de la "
                f"barre du resultat ; attendu ce couple rendu par {SOURCE_ROUTES}:137-141"
            )
    for touche in TOUCHES_WIZARD:
        if touche in touches:
            constats.append(
                f"{PAGE} : le couple de touche (« {touche[0]} », « {touche[1]} ») est rendu sur le "
                f"resultat ; attendu les libelles du resultat, ceux du wizard avance etant reserves "
                f"aux ecrans qui passent f7_url/f8_url ({SOURCE_ROUTES}:137-141)"
            )

    # 4. Position des diagnostics, sur les pages concatenees dans l'ordre du resultat.
    if total is not None:
        toutes: list[str] = []
        for numero in range(1, total + 1):
            toutes.extend(_lignes_du_corps(client.get(f"/optimize/result?page={numero}")))
        equipements = [index for index, ligne in enumerate(toutes) if ligne.startswith(PREFIXE_EQUIPEMENT)]
        greeds = [index for index, ligne in enumerate(toutes) if ligne.startswith(PREFIXE_GREEDY)]
        if not equipements:
            constats.append(
                f"{PAGE} : aucune ligne « {PREFIXE_EQUIPEMENT} » dans le resultat concatene ; attendu "
                f"la liste des emplacements rendue par {SOURCE_API}:384"
            )
        if not greeds:
            constats.append(
                f"{PAGE} : aucune ligne « {PREFIXE_GREEDY} » dans le resultat concatene ; attendu la "
                f"borne du solveur rendue par {SOURCE_API}:436"
            )
        positions = {
            marqueur: [index for index, ligne in enumerate(toutes) if marqueur in ligne]
            for marqueur in MARQUEURS_DIAGNOSTICS
        }
        for marqueur, ou in positions.items():
            if not ou:
                constats.append(
                    f"{PAGE} : le marqueur « {marqueur} » est absent du resultat concatene ; attendu "
                    f"ce diagnostic en fin de resultat, apres le dernier « {PREFIXE_EQUIPEMENT} » et "
                    f"avant « {PREFIXE_GREEDY} », insere par {SOURCE_API}:432-434"
                )
                continue
            if equipements and ou[0] <= equipements[-1]:
                constats.append(
                    f"{PAGE} : le marqueur « {marqueur} » apparait avant le dernier "
                    f"« {PREFIXE_EQUIPEMENT} » (lignes {ou} contre {equipements[-1]}) ; attendu les "
                    f"diagnostics en fin de resultat ({SOURCE_API}:432-434)"
                )
            if greeds and ou[-1] >= greeds[0]:
                constats.append(
                    f"{PAGE} : le marqueur « {marqueur} » apparait apres « {PREFIXE_GREEDY} » "
                    f"(lignes {ou} contre {greeds[0]}) ; attendu les diagnostics avant cette ligne "
                    f"({SOURCE_API}:432-436)"
                )
        if all(positions.values()):
            dernier_diagnostic = max(max(ou) for ou in positions.values())
            catalogue = [
                index for index, ligne in enumerate(toutes) if ligne.strip() == PHRASE_CATALOGUE
            ]
            if not catalogue:
                constats.append(
                    f"{PAGE} : la phrase « {PHRASE_CATALOGUE} » est absente du resultat concatene ; "
                    f"attendu cette phrase juste apres le dernier diagnostic ({SOURCE_API}:434)"
                )
            elif catalogue[0] != dernier_diagnostic + 1:
                constats.append(
                    f"{PAGE} : la phrase du catalogue est en position {catalogue[0]} ; attendu la "
                    f"position {dernier_diagnostic + 1}, immediatement apres le dernier diagnostic "
                    f"({SOURCE_API}:432-434)"
                )
        if not any(EMPLACEMENT_VIDE in ligne for ligne in toutes):
            constats.append(
                f"{PAGE} : aucune ligne du resultat ne porte « {EMPLACEMENT_VIDE} » ; attendu un "
                f"emplacement vide rendu tel quel par {SOURCE_API}:384-385"
            )

    # 5. Cote page : la section « Lire le resultat » cite ce que le rendu produit, et ne fige rien.
    corps_page = section(texte, TITRE_RESULTAT, PAGE)
    for attendu in (
        "ENTREE=VALIDER",
        "F7=Page prec",
        "F8=Page suiv",
        "PAGE n/total",
        "en fin de résultat",
        PHRASE_CATALOGUE,
        EMPLACEMENT_VIDE,
    ):
        if attendu not in corps_page:
            constats.append(
                f"{PAGE} : la section « {TITRE_RESULTAT} » ne cite pas « {attendu} » ; attendu ce "
                f"fragment du resultat, rendu par {SOURCE_ROUTES}:143-147 et {SOURCE_API}:432-434"
            )
    if normalize(TOURNURE_DERNIERE_PAGE) in normalize(corps_page):
        constats.append(
            f"{PAGE} : la section « {TITRE_RESULTAT} » dit « {TOURNURE_DERNIERE_PAGE} » ; attendu "
            f"« en fin de résultat », la position reelle des diagnostics etant relative a la fin du "
            f"resultat, pas a la derniere page ({SOURCE_API}:432-434)"
        )
    for motif in MOTIFS_VALEURS_VOLATILES:
        trouve_valeur = re.search(motif, corps_page)
        if trouve_valeur is not None:
            constats.append(
                f"{PAGE} : la section « {TITRE_RESULTAT} » fige la valeur "
                f"« {trouve_valeur.group(0)} » (motif {motif!r}) ; attendu aucune valeur volatile : "
                f"methode, score, indice et total de pages changent d'une execution a l'autre "
                f"({SOURCE_API}:329-341)"
            )

    assert not constats, (
        f"{PAGE} : constats sur la pagination et l'emplacement du calcul (marqueurs attendus : "
        + ", ".join(MARQUEURS_DIAGNOSTICS)
        + ") : "
        + " ; ".join(constats)
        + f" ; attendu la carte « PAGE 1/<total> » dans la ligne de statut ({SOURCE_ROUTES}:145), la "
        f"derniere page atteinte, les trois marqueurs en fin de resultat, apres le dernier "
        f"« {PREFIXE_EQUIPEMENT} » et avant « {PREFIXE_GREEDY} » ({SOURCE_API}:432-434), et aucune "
        f"valeur volatile dans la section « {TITRE_RESULTAT} »"
    )


def test_parcours_cli_ne_pose_pas_les_trois_questions(docs_dir: Path, normalize) -> None:
    """La page dit ce que le parcours en ligne de commande ne contient pas (D-33).

    Demonstration indirecte : la sonde lit le TEXTE de `dofus_stuff/optimize/profile_input.py` et
    ses litteraux de chaine par `ast`, elle n'execute jamais la ligne de commande et n'appelle
    jamais son point d'entree. Une invite composee ailleurs, ou construite dynamiquement, lui
    echapperait : c'est une limite nommee, pas une couverture revendiquee.
    """
    texte = _texte_page(docs_dir)
    constats: list[str] = []

    if normalize(MOTIF_PAGE_CLI) not in normalize(texte):
        constats.append(
            f"{PAGE} : la phrase « {MOTIF_PAGE_CLI} » est absente ; attendu cette phrase, qui evite "
            f"de croire que le parcours en ligne de commande pose les memes questions que le "
            f"parcours guide ({SOURCE_PROFIL})"
        )

    chemin = RACINE_DEPOT / SOURCE_PROFIL
    litteraux: list[str] = []
    if not chemin.is_file():
        constats.append(
            f"{SOURCE_PROFIL} : module introuvable ({chemin}) ; attendu le module des questions "
            f"guidees du parcours en ligne de commande, cite par {PAGE}"
        )
    else:
        arbre = ast.parse(chemin.read_text(encoding="utf-8"))
        litteraux = [
            noeud.value
            for noeud in ast.walk(arbre)
            if isinstance(noeud, ast.Constant) and isinstance(noeud.value, str)
        ]

    if not litteraux:
        constats.append(
            f"{SOURCE_PROFIL} : aucun litteral de chaine lu ; attendu un module non vide, faute de "
            f"quoi ce controle ne prouverait rien sur la phrase « {MOTIF_PAGE_CLI} » de {PAGE}"
        )
    for litteral in litteraux:
        normalise = normalize(litteral)
        for motif in MOTS_PROFIL_INTERDITS:
            if re.search(motif, normalise):
                constats.append(
                    f"{SOURCE_PROFIL} : le litteral « {litteral} » contient une invite de classe ou "
                    f"d'element ; attendu l'absence de toute invite de ce genre, pour que la phrase "
                    f"« {MOTIF_PAGE_CLI} » de {PAGE} reste vraie"
                )

    assert not constats, (
        f"{PAGE} : constats sur le parcours en ligne de commande : "
        + " ; ".join(constats)
        + f" ; attendu la phrase « {MOTIF_PAGE_CLI} » et aucun litteral de classe ni d'element "
        f"dans {SOURCE_PROFIL}"
    )


def _libelles_display_slots() -> tuple[str, ...]:
    """Libelles de la table `display_slots`, extraits par `ast` de `dofus_stuff/optimize/api.py`.

    La verite vient du code, jamais d'une liste ecrite de memoire (D-42). Un echec nomme le fichier,
    la table et la plage de lignes, et dit que la table a peut-etre ete renommee : jamais un
    `AttributeError` brut, qui ne dirait ni quel fichier ni quelle table lire.
    """
    chemin = RACINE_DEPOT / SOURCE_API
    if not chemin.is_file():
        raise AssertionError(
            f"{SOURCE_API} : module introuvable ({chemin}) ; attendu la table « {TABLE_SLOTS} » "
            f"(lignes 362-380), qui porte les libelles d'emplacement rendus par le resultat"
        )
    arbre = ast.parse(chemin.read_text(encoding="utf-8"))
    for noeud in ast.walk(arbre):
        cibles: list[str] = []
        valeur: ast.expr | None = None
        if isinstance(noeud, ast.Assign):
            cibles = [cible.id for cible in noeud.targets if isinstance(cible, ast.Name)]
            valeur = noeud.value
        elif isinstance(noeud, ast.AnnAssign) and isinstance(noeud.target, ast.Name):
            cibles = [noeud.target.id]
            valeur = noeud.value
        if TABLE_SLOTS not in cibles or not isinstance(valeur, ast.Tuple):
            continue
        elements = [
            element.value
            for element in valeur.elts
            if isinstance(element, ast.Constant) and isinstance(element.value, str)
        ]
        if not elements or len(elements) != len(valeur.elts):
            continue
        return tuple(elements)
    raise AssertionError(
        f"{SOURCE_API} : table « {TABLE_SLOTS} » (lignes 362-380) introuvable, ou non lisible comme "
        f"un tuple de chaines ; attendu cette table, qui porte les libelles d'emplacement rendus par "
        f"le resultat — elle a peut-etre ete renommee ou remplacee"
    )


def test_correspondance_libelles_slots(docs_dir: Path, section, normalize) -> None:
    """La table de la page couvre exactement les libelles de `display_slots` (V7, ECR-1).

    La correspondance porte sur le **libelle technique** et son nom complet, jamais sur une
    troncature : dans ce flux aucun libelle n'est coupe (mesure M7). Chaque nom complet est recopie
    de la source qui le porte et re-verifie sur la ligne qui le porte (patron `LIBELLES_SOURCE`),
    jamais ecrit de memoire (D-42). Les libelles du tableau sont lus **lignes de tableau**, jamais
    la prose : une meme ligne peut en porter plusieurs, comme les six `dofus_1` a `dofus_6`.
    """
    texte = _texte_page(docs_dir)
    constats: list[str] = []
    epingles = tuple(entree[0] for entree in SLOTS_MESURE)

    # 1. La verite des libelles est lue dans le code, et une verite vide est un echec nomme.
    try:
        libelles = _libelles_display_slots()
    except AssertionError as erreur:
        libelles = ()
        constats.append(str(erreur))

    if libelles and len(libelles) != NOMBRE_SLOTS:
        manquants = [libelle for libelle in epingles if libelle not in libelles]
        inventes = [libelle for libelle in libelles if libelle not in epingles]
        constats.append(
            f"{SOURCE_API}:362-380 : la table « {TABLE_SLOTS} » compte {len(libelles)} libelles ; "
            f"attendu {NOMBRE_SLOTS} (mesure). Libelles epingles absents du code : "
            f"{', '.join(manquants) or 'aucun'} ; libelles du code absents de la table epinglee : "
            f"{', '.join(inventes) or 'aucun'} ; si un emplacement est ajoute ou retire, la page et "
            f"ce module changent dans le meme commit"
        )

    # 2. Chaque entree epinglee est re-verifiee dans la source citee.
    for libelle, nom_complet, chemin_source, aiguille in SLOTS_MESURE:
        chemin = RACINE_DEPOT / chemin_source
        if not chemin.is_file():
            constats.append(
                f"{chemin_source} : source introuvable ({chemin}) ; attendu le fichier qui porte le "
                f"nom complet « {nom_complet} » du libelle « {libelle} » cite par {PAGE}"
            )
            continue
        portantes = [
            ligne for ligne in chemin.read_text(encoding="utf-8").splitlines() if aiguille in ligne
        ]
        if not portantes:
            constats.append(
                f"{chemin_source} : aucune ligne ne porte l'aiguille « {aiguille} » ; attendu la "
                f"ligne qui porte a la fois cette aiguille et le nom complet « {nom_complet} » du "
                f"libelle « {libelle} » cite par {PAGE}"
            )
            continue
        if not any(normalize(nom_complet) in normalize(ligne) for ligne in portantes):
            constats.append(
                f"{chemin_source} : le nom complet « {nom_complet} » du libelle « {libelle} » cite "
                f"par {PAGE} n'est plus lisible sur la ligne qui porte « {aiguille} » ; attendu ce "
                f"nom complet sur cette meme ligne, recopie de la source qui le porte"
            )

    # 3. Les lignes du tableau couvrent exactement les libelles rendus, chacune avec son nom complet.
    corps_page = section(texte, TITRE_CORRESPONDANCE, PAGE)
    lignes_tableau = [
        ligne for ligne in corps_page.splitlines() if ligne.strip().startswith("|")
    ]
    libelles_page: list[str] = []
    for ligne in lignes_tableau:
        libelles_page.extend(LIBELLE_ENTRE_ACCENTS.findall(ligne))
    occurrences = {libelle: libelles_page.count(libelle) for libelle in sorted(set(libelles_page))}

    if not libelles_page:
        constats.append(
            f"{PAGE} : la section « {TITRE_CORRESPONDANCE} » ne porte aucun libelle entre accents "
            f"graves ; attendu la table des {NOMBRE_SLOTS} emplacements rendus par "
            f"{SOURCE_API}:362-380"
        )
    for libelle, nombre in occurrences.items():
        if libelle not in epingles:
            constats.append(
                f"{PAGE} : la table de « {TITRE_CORRESPONDANCE} » cite le libelle « {libelle} », "
                f"absent de {SOURCE_API}:362-380 ; attendu un libelle reellement rendu par le "
                f"resultat, jamais un emplacement invente"
            )
        elif nombre != 1:
            constats.append(
                f"{PAGE} : le libelle « {libelle} » apparait {nombre} fois dans la table de "
                f"« {TITRE_CORRESPONDANCE} » ; attendu une seule ligne par libelle, un second "
                f"exemplaire faisant deux verites a tenir ({SOURCE_API}:362-380)"
            )
    for libelle in epingles:
        if occurrences.get(libelle, 0) == 0:
            constats.append(
                f"{PAGE} : le libelle « {libelle} » de {SOURCE_API}:362-380 est absent de la table "
                f"de « {TITRE_CORRESPONDANCE} » ; attendu chaque libelle rendu par le resultat, "
                f"epingle dans ce module"
            )
    for libelle, nom_complet, _, _ in SLOTS_MESURE:
        porteuses = [ligne for ligne in lignes_tableau if f"`{libelle}`" in ligne]
        if not porteuses:
            continue  # deja signale comme manquant
        if not any(normalize(nom_complet) in normalize(ligne) for ligne in porteuses):
            constats.append(
                f"{PAGE} : la ligne de table qui porte « {libelle} » ne porte pas son nom complet "
                f"« {nom_complet} » ; attendu ce nom sur la meme ligne, recopie de la source qui le "
                f"porte ({SOURCE_DOFUSBOOK}:26-37, ou {SOURCE_SPEC} pour « prysma »)"
            )

    # 4. Aucune troncature n'est promise : elle n'existe pas dans ce flux (mesure M7).
    if normalize(TRONCATURE_PAGE) in normalize(corps_page):
        constats.append(
            f"{PAGE} : la section « {TITRE_CORRESPONDANCE} » parle de « {TRONCATURE_PAGE} » ; "
            f"attendu aucune troncature : la regle `clip` ({SOURCE_SCREENS}:14-20) ne se declenche "
            f"pas dans ce flux, le resultat completant les libelles par des espaces"
        )
    if POINTS_DE_SUSPENSION in corps_page:
        constats.append(
            f"{PAGE} : la section « {TITRE_CORRESPONDANCE} » contient le caractere "
            f"« {POINTS_DE_SUSPENSION} » ; attendu aucun point de suspension : le rendu n'en produit "
            f"aucun dans ce flux (mesure M7), et une troncature inexistante ne doit pas etre promise "
            f"au lecteur ({SOURCE_SCREENS}:14-20)"
        )

    assert not constats, (
        f"{PAGE} : constats sur la correspondance des libelles d'emplacement (table "
        f"« {TABLE_SLOTS} » de {SOURCE_API}:362-380) : "
        + " ; ".join(constats)
        + f" ; attendu la table des {NOMBRE_SLOTS} libelles rendus par le resultat, chacun avec le "
        f"nom complet recopie de sa source ({SOURCE_DOFUSBOOK}:26-37, {SOURCE_SPEC} pour "
        f"« prysma »), sans aucune troncature"
    )


def test_source_de_verite_et_chemins_cites(docs_dir: Path, section) -> None:
    """La section « Source de verite » cite du code, et tout chemin cite existe sur disque."""
    texte = _texte_page(docs_dir)
    bloc = section(texte, TITRE_SOURCE, PAGE)
    constats: list[str] = []

    chemins_bloc = sorted(set(CHEMIN_CITE.findall(bloc)))
    if not chemins_bloc:
        constats.append(
            f"la section « {TITRE_SOURCE} » ne cite aucun chemin de code ; attendu au moins "
            f"{SOURCE_ROUTES} et {SOURCE_RECOMMEND}"
        )
    for attendu in (SOURCE_ROUTES, SOURCE_RECOMMEND):
        if attendu not in chemins_bloc:
            constats.append(
                f"la section « {TITRE_SOURCE} » ne cite pas « {attendu} » ; attendu ce chemin, "
                f"qui porte les ecrans et les libelles du parcours simplifie"
            )

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

    assert not constats, (
        f"{PAGE} : constats sur le bloc « {TITRE_SOURCE} » : "
        + " ; ".join(constats)
        + f" ; attendu des chemins de code reels, dont {SOURCE_ROUTES} et {SOURCE_RECOMMEND}"
    )


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


def _chemin_module(module: str) -> Path | None:
    """Fichier du module produit, resolu depuis la racine du depot ; None s'il est introuvable."""
    base = RACINE_DEPOT.joinpath(*module.split("."))
    for candidat in (base.with_suffix(".py"), base / "__init__.py"):
        if candidat.is_file():
            return candidat
    return None


def _cloture_produit(modules: set[str]) -> tuple[set[str], set[str], set[str]]:
    """Cloture transitive des imports produit : (modules atteints, interdits, non resolus).

    La cloture va jusqu'au point fixe : un module produit atteint est analyse a son tour, ce qui
    permet d'attraper un import de la base locale tire par un module public intermediaire.
    """
    atteints: set[str] = set()
    interdits: set[str] = set()
    non_resolus: set[str] = set()
    a_voir = [
        module for module in modules if module == "dofus_stuff" or module.startswith("dofus_stuff.")
    ]
    while a_voir:
        module = a_voir.pop()
        if not (module == "dofus_stuff" or module.startswith("dofus_stuff.")):
            continue
        if module in atteints:
            continue
        atteints.add(module)
        chemin = _chemin_module(module)
        if chemin is None:
            non_resolus.add(module)
            continue
        for importe in _imports_du_module(ast.parse(chemin.read_text(encoding="utf-8"))):
            if importe.split(".")[0] in RACINES_INTERDITES or importe == MODULE_BASE_INTERDIT:
                interdits.add(f"{module} importe {importe}")
            a_voir.append(importe)
    return atteints, interdits, non_resolus


def test_garde_ni_base_ni_processus_ni_reseau() -> None:
    """Le module d'ancrage n'ouvre ni la base, ni un processus, ni une socket, ni le reseau (V15b).

    La propriete est verifiee sur le texte de ce module par `ast`, et jamais par une recherche de
    chaines : le module cite lui-meme les noms interdits dans ses messages, une recherche textuelle
    se detecterait elle-meme. Le controle porte sur le risque reel — ouvrir la base, lancer un
    processus, ouvrir une socket, joindre le reseau, supprimer un fichier — donc un import public
    pur ajoute plus tard passe sans revision, alors qu'un import qui tirerait la base rougit.
    """
    arbre = ast.parse(Path(__file__).read_text(encoding="utf-8"))
    importes = _imports_du_module(arbre)
    appeles = _appels_du_module(arbre)
    atteints, interdits_cloture, non_resolus = _cloture_produit(importes)

    constats: list[str] = []
    racines = sorted(module for module in importes if module.split(".")[0] in RACINES_INTERDITES)
    if racines:
        constats.append(
            f"import(s) de base, de processus, de socket ou de reseau : {', '.join(racines)} ; "
            f"attendu aucun de ces imports dans le module d'ancrage decrit par {PAGE} "
            f"({SOURCE_ROUTES}, etapes 1 a 3)"
        )
    if MODULE_BASE_INTERDIT in importes or any(
        module.startswith(MODULE_BASE_INTERDIT + ".") for module in importes
    ):
        constats.append(
            f"import de « {MODULE_BASE_INTERDIT} » ; attendu aucun import de la base locale, "
            f"la fixture `app` construisant sa propre base temporaire ({SOURCE_ROUTES})"
        )
    if interdits_cloture:
        constats.append(
            f"import(s) interdit(s) atteint(s) par la cloture transitive des imports produit : "
            + ", ".join(sorted(interdits_cloture))
        )
    if non_resolus:
        constats.append(
            f"import(s) produit non resolus depuis la racine du depot : "
            + ", ".join(sorted(non_resolus))
        )
    if len(atteints) < 3:
        constats.append(
            f"la cloture transitive ne compte que {len(atteints)} module(s) produit atteint(s) ; "
            f"attendu au moins 3, faute de quoi le controle ne mesurerait rien"
        )
    if APPEL_PRODUIT in appeles:
        constats.append(
            f"appel a {APPEL_PRODUIT}() dans le module d'ancrage ; attendu un ancrage par le "
            f"client de test Flask de {SOURCE_ROUTES}, le produit n'etant jamais execute"
        )
    suppressions = sorted(set(APPELS_SUPPRESSION) & appeles)
    if suppressions:
        constats.append(
            f"appel(s) de suppression de fichier : {', '.join(suppressions)} ; attendu aucun appel "
            f"destructif dans le module d'ancrage decrit par {PAGE}"
        )

    assert not constats, (
        f"{PAGE} : constats sur la garde « ni base, ni processus, ni reseau » : "
        + " ; ".join(constats)
        + f" ; attendu un module d'ancrage qui rend les ecrans de {SOURCE_ROUTES} en processus, "
        f"sans ouvrir la base locale ni joindre le reseau"
    )


# --- Sauvegarde navigateur et export Dofusbook : les deux ecrans qui les exposent (plan 03-03) ---

# Ligne d'en-tete de la coquille (`dofus_stuff/web/templates/screen.html:24`) : le programme de
# l'ecran y est rendu par `header_line` (`dofus_stuff/web/screens.py:77-96`).
MARQUEUR_ENTETE = '<div class="row header" id="header-row">'

# Champ de saisie de la coquille, lu **dans la balise du champ** : une recherche libre de
# `name="..."` trouverait d'abord le `<meta name="viewport">` de l'en-tete HTML.
MOTIF_CHAMP_SAISIE = re.compile(r'<input class="field"(?P<attributs>[^>]*)>', re.S)
MOTIF_ATTRIBUT_CHAMP = re.compile(r'(?P<nom>[a-z-]+)="(?P<valeur>[^"]*)"')

# Cle de session lue par le `GET /optimize/result` (`dofus_stuff/web/routes.py:893` et `:1318`).
SESSION_RESULTAT = "optimize_result_lines"

# Libelles des deux ecrans qui exposent la sauvegarde et l'export, mesures sur le rendu : l'ecran
# `SAV-01` est rendu par `dofus_stuff/web/routes.py:1280-1295` (route `/saves`) et la ligne de statut
# du resultat par `dofus_stuff/web/routes.py:1380`.
ECRAN_SAUVEGARDES = "SAV-01"
ATTENTE_SAUVEGARDES = "CHARGEMENT DES SAUVEGARDES LOCALES…"
STATUT_SAUVEGARDES = "N OUVRIR | DEL N | PURGE OUI"
STATUT_RESULTAT = "ID DETAIL | SAVE [NOM] | SAVES | EDIT | DB"
TOUCHES_SAUVEGARDES = (("ESC", "Retour"),)
MODE_SAUVEGARDES = "saves"
MODE_RESULTAT = "result"
CHAMP_SAUVEGARDES = ("cmd", "40")

# Fragments que la section « Sauvegarder et exporter » doit citer : chacun est rendu par l'un des
# deux ecrans, et aucun n'est recopie d'une surface de commandes (D-37).
FRAGMENTS_PAGE_SAUVEGARDE = (
    "SAVE [NOM]",
    "SAVES",
    ATTENTE_SAUVEGARDES,
    STATUT_SAUVEGARDES,
)

# Balise des blocs d'exemples de commandes (D-24) : la surface de commandes appartient a
# `docs/cli.md`, la section ne doit donc porter aucun bloc de ce genre (D-37).
BALISE_COMMANDE = "```console"

# Etat de session du resultat injecte sans lancer de solveur : le `GET /optimize/result` ne lit que
# `optimize_result_lines`. La saisie `DB`, seule a exiger le build, est couverte, patchee, par
# `tests/test_web.py:668` et interdite ici par `test_aucun_post_db_sans_patch`.
LIGNES_RESULTAT_INJECTE = ("Niveau 50", "Score : 1")


def _entete(reponse) -> str:
    """Texte de la ligne d'en-tete de la coquille, ou "" si le marqueur est absent du rendu."""
    texte = reponse.get_data(as_text=True)
    if MARQUEUR_ENTETE not in texte:
        return ""
    return texte.split(MARQUEUR_ENTETE, 1)[1].split("</div>", 1)[0]


def _champ_saisie(reponse) -> dict[str, str]:
    """Attributs de la balise du champ de saisie, lus dans cette balise et nulle part ailleurs."""
    trouve = MOTIF_CHAMP_SAISIE.search(reponse.get_data(as_text=True))
    if trouve is None:
        return {}
    return {
        attribut.group("nom"): attribut.group("valeur")
        for attribut in MOTIF_ATTRIBUT_CHAMP.finditer(trouve.group("attributs"))
    }


def test_ecrans_de_sauvegarde_et_export(app, docs_dir: Path, section, normalize) -> None:
    """Les deux ecrans qui exposent la sauvegarde et l'export rendent leurs libelles (V8).

    Aucune saisie n'est postee sur l'ecran de resultat : le rendu est obtenu en injectant l'etat de
    session, exactement comme `tests/test_web.py:668-671`. La saisie `DB` appelle
    `webbrowser.open_new_tab` **cote serveur** et est couverte, patchee, par `tests/test_web.py:668`.
    """
    texte = _texte_page(docs_dir)
    constats: list[str] = []

    # 1. L'ecran des sauvegardes : en-tete, corps d'attente, ligne de statut, coquille et champ.
    sauvegardes = app.test_client().get("/saves")
    if sauvegardes.status_code != 200:
        constats.append(
            f"{PAGE} : l'ecran des sauvegardes repond {sauvegardes.status_code} ; attendu 200, "
            f"rendu par {SOURCE_ROUTES}:1280-1295"
        )
    else:
        if ECRAN_SAUVEGARDES not in _entete(sauvegardes):
            constats.append(
                f"{PAGE} : l'en-tete de l'ecran des sauvegardes ne porte pas "
                f"« {ECRAN_SAUVEGARDES} » (en-tete lue : « {_entete(sauvegardes)} ») ; attendu cet "
                f"identifiant d'ecran, rendu par {SOURCE_ROUTES}:1280-1295"
            )
        lignes = [normalize(ligne) for ligne in _lignes_du_corps(sauvegardes)]
        if normalize(ATTENTE_SAUVEGARDES) not in lignes:
            constats.append(
                f"{PAGE} : le corps de l'ecran des sauvegardes ne porte pas "
                f"« {ATTENTE_SAUVEGARDES} » ; attendu ce texte d'attente, rendu par "
                f"{SOURCE_ROUTES}:1287 puis remplace par la liste cote navigateur ({SOURCE_JS})"
            )
        statut = _statut(sauvegardes)
        if not statut.startswith(STATUT_SAUVEGARDES):
            constats.append(
                f"{PAGE} : la ligne de statut de l'ecran des sauvegardes vaut « {statut} » ; attendu "
                f"une ligne commencant par « {STATUT_SAUVEGARDES} », rendue par "
                f"{SOURCE_ROUTES}:1293"
            )
        if _attribut(sauvegardes, "data-mode") != MODE_SAUVEGARDES:
            constats.append(
                f"{PAGE} : l'attribut « data-mode » de l'ecran des sauvegardes vaut "
                f"« {_attribut(sauvegardes, 'data-mode')} » ; attendu « {MODE_SAUVEGARDES} », comme "
                f"rendu par {SOURCE_ROUTES}:1294"
            )
        for attribut, attendu in (
            ("name", CHAMP_SAUVEGARDES[0]),
            ("maxlength", CHAMP_SAUVEGARDES[1]),
        ):
            valeur = _champ_saisie(sauvegardes).get(attribut)
            if valeur != attendu:
                constats.append(
                    f"{PAGE} : l'attribut « {attribut} » du champ de saisie de l'ecran des "
                    f"sauvegardes vaut « {valeur} » ; attendu « {attendu} », comme rendu par "
                    f"{SOURCE_ROUTES}:1288-1290"
                )
        for touche in TOUCHES_SAUVEGARDES:
            if touche not in _touches(sauvegardes):
                constats.append(
                    f"{PAGE} : le couple de touche (« {touche[0]} », « {touche[1]} ») est absent de "
                    f"la barre de l'ecran des sauvegardes ; attendu ce couple, rendu par "
                    f"{SOURCE_ROUTES}:1291"
                )

    # 2. L'ecran de resultat, obtenu par injection d'etat : sa ligne de statut annonce `SAVE [NOM]`,
    #    `SAVES` et `DB`, sans qu'aucune saisie soit postee.
    client = app.test_client()
    with client.session_transaction() as session:
        session[SESSION_RESULTAT] = list(LIGNES_RESULTAT_INJECTE)
    resultat = client.get("/optimize/result")
    if resultat.status_code != 200:
        constats.append(
            f"{PAGE} : l'ecran du resultat repond {resultat.status_code} apres injection de l'etat "
            f"de session ; attendu 200, rendu par {SOURCE_ROUTES}, qui lit « {SESSION_RESULTAT} » "
            f"({SOURCE_ROUTES}:893 et :1318)"
        )
    else:
        statut_resultat = _statut(resultat)
        if not statut_resultat.startswith(STATUT_RESULTAT):
            constats.append(
                f"{PAGE} : la ligne de statut du resultat vaut « {statut_resultat} » ; attendu une "
                f"ligne commencant par « {STATUT_RESULTAT} », rendue par {SOURCE_ROUTES}:1380"
            )
        for commande in ("SAVE [NOM]", "SAVES", "DB"):
            if commande not in statut_resultat:
                constats.append(
                    f"{PAGE} : la ligne de statut du resultat ne porte pas « {commande} » ; attendu "
                    f"cette saisie parmi celles annoncees par la ligne de statut, rendue par "
                    f"{SOURCE_ROUTES}:1380"
                )
        if _attribut(resultat, "data-mode") != MODE_RESULTAT:
            constats.append(
                f"{PAGE} : l'attribut « data-mode » de l'ecran du resultat vaut "
                f"« {_attribut(resultat, 'data-mode')} » ; attendu « {MODE_RESULTAT} », comme rendu "
                f"par {SOURCE_ROUTES}:1382"
            )

    # 3. Cote page : la section cite ces libelles et ne recopie aucune commande (D-37).
    corps_page = ""
    try:
        corps_page = section(texte, TITRE_SAUVEGARDE, PAGE)
    except AssertionError as erreur:
        constats.append(str(erreur))
    for fragment in FRAGMENTS_PAGE_SAUVEGARDE:
        if normalize(fragment) not in normalize(corps_page):
            constats.append(
                f"{PAGE} : la section « {TITRE_SAUVEGARDE} » ne cite pas « {fragment} » ; attendu ce "
                f"fragment, rendu par {SOURCE_ROUTES}:1280-1295 ou :1380"
            )
    if BALISE_COMMANDE in corps_page:
        constats.append(
            f"{PAGE} : la section « {TITRE_SAUVEGARDE} » porte un bloc de commandes recopiables "
            f"« {BALISE_COMMANDE} » ; attendu aucun bloc de ce genre, la surface de commandes "
            f"appartenant a la page CLI (D-37), pas a cette page"
        )

    assert not constats, (
        f"{PAGE} : constats sur les ecrans qui exposent la sauvegarde et l'export (attendus : "
        f"« {ECRAN_SAUVEGARDES} », « {ATTENTE_SAUVEGARDES} » et « {STATUT_SAUVEGARDES} » pour "
        f"l'ecran des sauvegardes, « {STATUT_RESULTAT} » pour le resultat) : "
        + " ; ".join(constats)
        + f" ; attendu ces libelles rendus par {SOURCE_ROUTES}:1280-1295 et :1380, et cites par la "
        f"section « {TITRE_SAUVEGARDE} » de {PAGE}"
    )


# --- Limite de sauvegarde ancree sur le JS et export Dofusbook (plan 03-03, ECR-5, M8/M9) ---

# Motifs des deux constantes du client de sauvegarde, lues dans le fichier JS et jamais recopiees de
# memoire (D-42) : `dofus_stuff/web/static/js/terminal.js:14-15`.
MOTIF_SAVES_KEY = re.compile(r'var\s+SAVES_KEY\s*=\s*"(?P<valeur>[^"]+)"')
MOTIF_MAX_SAVES = re.compile(r"var\s+MAX_SAVES\s*=\s*(?P<valeur>\d+)")
LIGNE_SAVES_KEY = 14
LIGNE_MAX_SAVES = 15

# Fil de la limite : `stuffs.shift()` tant que la liste est pleine (`terminal.js:294-318`).
LIGNES_EVICTION = "294-318"

# Tournures epinglees de la section. L'eviction est **silencieuse** (ECR-5) : « 20 maximum » seul
# serait exact mais trompeur, puisque la sauvegarde en trop remplace la plus ancienne sans message
# d'echec. La `prysma` (prysmaradite) n'appartient a aucun des dix groupes d'export (M9).
TOURNURE_EVICTION = "les plus anciennes sont remplacées"
TOURNURE_LIMITE_INTERDITE = "20 maximum"
TOURNURE_NON_EXPORTEE = "n'est pas exportée"
JETON_PRYSMARADITE = "prysma"

# Libelles produits par le client de sauvegarde, exiges dans la page **et** sur une ligne du fichier
# JS (patron `LIBELLES_SOURCE` de `tests/test_docs_code_anchor.py:61-74`) : un libelle qui disparait
# d'un cote ou de l'autre rougit.
LIBELLES_JS_SAUVEGARDE = (
    ("DB DOFUSBOOK", 400),
    ("BACK LISTE", 400),
    ("SAUVEGARDES PURGEES", 466),
)

# Empreinte du constat qui porte le nombre d'emplacements exportes, ecrite **dans une constante** et
# jamais en clair dans la ligne d'assertion : pytest reproduit la ligne source du `assert` dans sa
# sortie, un motif ecrit en clair y serait donc trouve meme si aucun constat n'etait produit, et la
# morsure cesserait d'etre discriminante.
MOTIF_EMPREINTE_EXPORT = "nombre d'emplacements exportes mesure"

# Module produit dont la fonction d'export et l'URL d'import sont publiques (D-14) : l'importation
# statique donne la fonction a appeler, `importlib` donne la valeur courante de l'URL. Aucune
# introspection privee.
SOURCE_MODULE_DOFUSBOOK = "dofus_stuff.web.dofusbook_export"
NOM_ATTRIBUT_URL_IMPORT = "DOFUSBOOK_IMPORT_URL"

# Stuff d'epreuve de l'export : les seize emplacements exportes plus la `prysma`, identifiants tous
# distincts. `build_dofusbook_url` est pure : elle n'ouvre aucune base et ne joint aucun reseau.
ID_PRYSMARADITE = 999
NIVEAU_EXPORT = 137
SLOTS_EXPORT = {
    "cape": 501,
    "hat": 502,
    "belt": 503,
    "boots": 504,
    "amulet": 505,
    "ring_a": 506,
    "ring_b": 507,
    "dofus_1": 601,
    "dofus_2": 602,
    "dofus_3": 603,
    "dofus_4": 604,
    "dofus_5": 605,
    "dofus_6": 606,
    "shield": 508,
    "weapon": 509,
    "pet": 510,
    "prysma": ID_PRYSMARADITE,
}
NOMBRE_EMPLACEMENTS_EXPORTES = 16
NOMBRE_GROUPES_EXPORT = 10
LONGUEUR_CARACTERISTIQUES = 51


def _litteral_js(motif: re.Pattern[str]) -> str:
    """Valeur d'une constante du client de sauvegarde, lue dans le fichier JS (D-42).

    Controle de **litteral source**, jamais de comportement : aucun moteur JavaScript n'est
    disponible ici (ni `localStorage`, ni `shift`). Un echec nomme le fichier, le motif et la
    consequence, plutot que de laisser remonter une exception brute.
    """
    chemin = RACINE_DEPOT / SOURCE_JS
    if not chemin.is_file():
        raise AssertionError(
            f"{SOURCE_JS} : fichier introuvable ({chemin}) ; attendu le client de sauvegarde du "
            f"navigateur, qui porte les constantes citees par {PAGE}"
        )
    trouve = motif.search(chemin.read_text(encoding="utf-8"))
    if trouve is None:
        raise AssertionError(
            f"{SOURCE_JS} : aucune ligne ne porte le motif {motif.pattern!r} ; attendu les "
            f"constantes de sauvegarde du navigateur (lignes {LIGNE_SAVES_KEY} et "
            f"{LIGNE_MAX_SAVES}) — la constante a peut-etre ete renommee : la page {PAGE} doit etre "
            f"mise a jour dans le meme commit"
        )
    return trouve.group("valeur")


def _url_import() -> str:
    """URL d'import portee par le module produit, lue sur son attribut public (D-14, D-42)."""
    module = importlib.import_module(SOURCE_MODULE_DOFUSBOOK)
    return str(getattr(module, NOM_ATTRIBUT_URL_IMPORT))


def test_sauvegarde_navigateur_et_export_dofusbook(docs_dir: Path, section, normalize) -> None:
    """La limite vient du JS et l'export est prouve pur : seize emplacements, `prysma` exclue (V9, V10).

    Controle de **litteraux source** pour la sauvegarde du navigateur (cle, valeur de la limite,
    libelles) : aucun moteur JavaScript n'existe ici, donc ni `localStorage`, ni `shift`, ni
    hydratation de liste ne sont exerces. Controle **comportemental** pour l'export, sur la surface
    publique pure `build_dofusbook_url`. La fixture `app` n'est pas consommee : aucun ecran n'est
    rendu ici, les deux ecrans qui exposent la sauvegarde et l'export etant rendus par
    `test_ecrans_de_sauvegarde_et_export`.
    """
    texte = _texte_page(docs_dir)
    constats: list[str] = []

    # 1. Valeur de la limite et cle de stockage, lues dans le fichier JS, jamais de memoire (D-42).
    try:
        cle_stockage = _litteral_js(MOTIF_SAVES_KEY)
    except AssertionError as erreur:
        cle_stockage = ""
        constats.append(str(erreur))
    try:
        limite = _litteral_js(MOTIF_MAX_SAVES)
    except AssertionError as erreur:
        limite = ""
        constats.append(str(erreur))

    corps_page = ""
    try:
        corps_page = section(texte, TITRE_SAUVEGARDE, PAGE)
    except AssertionError as erreur:
        constats.append(str(erreur))
    normalise = normalize(corps_page)

    if limite and not re.search(rf"(?<![\d.]){re.escape(limite)}(?![\d])", corps_page):
        constats.append(
            f"{PAGE} : la section « {TITRE_SAUVEGARDE} » ne cite pas la limite de sauvegarde portee "
            f"par {SOURCE_JS}:{LIGNE_MAX_SAVES} (« MAX_SAVES = {limite} ») ; attendu cette valeur, "
            f"lue dans le fichier a chaque execution — une valeur ecrite de memoire perime sans rien "
            f"faire rougir"
        )
    if cle_stockage and cle_stockage not in corps_page:
        constats.append(
            f"{PAGE} : la section « {TITRE_SAUVEGARDE} » ne cite pas la cle de stockage "
            f"« {cle_stockage} » portee par {SOURCE_JS}:{LIGNE_SAVES_KEY} ; attendu cette cle, lue "
            f"dans le fichier a chaque execution (D-42)"
        )

    # 2. L'eviction est dite honnetement : silencieuse, sans refus ni message d'echec (ECR-5).
    if normalize(TOURNURE_EVICTION) not in normalise:
        constats.append(
            f"{PAGE} : la section « {TITRE_SAUVEGARDE} » ne dit pas « {TOURNURE_EVICTION} » ; "
            f"attendu cette tournure : l'eviction du plus ancien est silencieuse "
            f"({SOURCE_JS}:{LIGNES_EVICTION} : `shift` tant que la liste est pleine, sans message "
            f"d'echec)"
        )
    if normalize(TOURNURE_LIMITE_INTERDITE) in normalise:
        constats.append(
            f"{PAGE} : la section « {TITRE_SAUVEGARDE} » dit « {TOURNURE_LIMITE_INTERDITE} » ; "
            f"attendu la tournure honnete « {TOURNURE_EVICTION} » : la sauvegarde en trop remplace "
            f"la plus ancienne sans message d'echec ({SOURCE_JS}:{LIGNES_EVICTION})"
        )

    # 3. Libelles du client de sauvegarde : exiges dans la page **et** sur une ligne du fichier JS.
    chemin_js = RACINE_DEPOT / SOURCE_JS
    lignes_js = chemin_js.read_text(encoding="utf-8").splitlines() if chemin_js.is_file() else []
    for libelle, ligne_source in LIBELLES_JS_SAUVEGARDE:
        if normalize(libelle) not in normalise:
            constats.append(
                f"{PAGE} : la section « {TITRE_SAUVEGARDE} » ne cite pas le libelle « {libelle} » ; "
                f"attendu ce libelle, rendu par {SOURCE_JS}:{ligne_source}"
            )
        if not any(libelle in ligne for ligne in lignes_js):
            constats.append(
                f"{SOURCE_JS} : aucune ligne ne porte le libelle « {libelle} » ; attendu ce libelle, "
                f"rendu par le client de sauvegarde (ligne {ligne_source}) et cite par la section "
                f"« {TITRE_SAUVEGARDE} » — un libelle qui disparait d'un cote ou de l'autre doit "
                f"rougir"
            )

    # 4. L'export, par la surface publique pure : charge utile decodee (base64 puis msgpack).
    url = build_dofusbook_url(SLOTS_EXPORT, NIVEAU_EXPORT)
    total_exporte: int | None = None
    if "stuff=" not in url:
        constats.append(
            f"{SOURCE_DOFUSBOOK} : l'URL produite ne porte pas de jeton « stuff= » ; attendu le jeton "
            f"d'import Dofusbook, pour {len(SLOTS_EXPORT)} emplacements fournis et le niveau "
            f"{NIVEAU_EXPORT}"
        )
    else:
        charge = msgpack.unpackb(base64.b64decode(url.split("stuff=", 1)[1]), raw=False)
        if not isinstance(charge, list) or len(charge) != 6:
            constats.append(
                f"{SOURCE_DOFUSBOOK} : la charge utile decodee n'a pas la forme "
                f"[caracs, points, niveau, flags, counts, ids] ; attendu cette forme mesuree "
                f"(recue : {type(charge).__name__}, "
                f"{len(charge) if isinstance(charge, list) else 0} elements)"
            )
        else:
            caracs, points, niveau, flags, counts, ids = charge
            if (
                not isinstance(caracs, list)
                or not isinstance(points, list)
                or len(caracs) != LONGUEUR_CARACTERISTIQUES
                or len(points) != LONGUEUR_CARACTERISTIQUES
            ):
                constats.append(
                    f"{SOURCE_DOFUSBOOK} : la charge utile porte "
                    f"{len(caracs) if isinstance(caracs, list) else '?'} caracteristiques et "
                    f"{len(points) if isinstance(points, list) else '?'} points ; attendu "
                    f"{LONGUEUR_CARACTERISTIQUES} de chaque, comme les lit l'import Dofusbook"
                )
            if niveau != NIVEAU_EXPORT:
                constats.append(
                    f"{SOURCE_DOFUSBOOK} : le niveau porte par la charge utile vaut {niveau!r} ; "
                    f"attendu {NIVEAU_EXPORT!r}, la valeur passee a `build_dofusbook_url`"
                )
            if flags != 0:
                constats.append(
                    f"{SOURCE_DOFUSBOOK} : les drapeaux de la charge utile valent {flags!r} ; attendu "
                    f"0, la valeur posee par l'export pour des emplacements connus"
                )
            if not isinstance(counts, list) or len(counts) != NOMBRE_GROUPES_EXPORT:
                constats.append(
                    f"{SOURCE_DOFUSBOOK} : la charge utile porte "
                    f"{len(counts) if isinstance(counts, list) else '?'} groupes de comptes ; attendu "
                    f"{NOMBRE_GROUPES_EXPORT} (cape, coiffe, ceinture, bottes, amulette, anneaux, "
                    f"dofus, bouclier, arme, familier)"
                )
            elif not all(isinstance(nombre, int) for nombre in counts):
                constats.append(
                    f"{SOURCE_DOFUSBOOK} : {MOTIF_EMPREINTE_EXPORT} impossible : les comptes de "
                    f"groupe ne sont pas tous des entiers ({counts!r})"
                )
            else:
                total_exporte = sum(counts)
                if total_exporte != NOMBRE_EMPLACEMENTS_EXPORTES:
                    constats.append(
                        f"{SOURCE_DOFUSBOOK} : {MOTIF_EMPREINTE_EXPORT} — {total_exporte} pour "
                        f"{len(SLOTS_EXPORT)} emplacements fournis ; attendu "
                        f"{NOMBRE_EMPLACEMENTS_EXPORTES} : la `{JETON_PRYSMARADITE}` n'appartient a "
                        f"aucun des {NOMBRE_GROUPES_EXPORT} groupes d'import"
                    )
            if not isinstance(ids, list):
                constats.append(
                    f"{SOURCE_DOFUSBOOK} : les identifiants exportes ne forment pas une liste "
                    f"({type(ids).__name__}) ; attendu les identifiants Ankama a plat"
                )
            else:
                if ID_PRYSMARADITE in ids:
                    constats.append(
                        f"{SOURCE_DOFUSBOOK} : l'identifiant {ID_PRYSMARADITE} de la "
                        f"`{JETON_PRYSMARADITE}` figure dans les identifiants exportes ; attendu son "
                        f"absence : la prysmaradite ne part pas vers Dofusbook"
                    )
                if total_exporte is not None and len(ids) != total_exporte:
                    constats.append(
                        f"{SOURCE_DOFUSBOOK} : {len(ids)} identifiants pour {total_exporte} "
                        f"emplacements comptes ; attendu un identifiant par emplacement exporte"
                    )

    # 5. Cote page : le nombre est celui du calcul, la `prysma` est exclue, l'URL vient du module.
    if total_exporte is not None and not re.search(
        rf"(?<![\d.]){total_exporte}(?![\d])", corps_page
    ):
        constats.append(
            f"{PAGE} : la section « {TITRE_SAUVEGARDE} » ne cite pas le nombre d'emplacements "
            f"exportes « {total_exporte} » ; attendu ce nombre, {MOTIF_EMPREINTE_EXPORT} a chaque "
            f"execution depuis la charge utile de `build_dofusbook_url` ({SOURCE_DOFUSBOOK})"
        )
    lignes_prysma = [
        ligne
        for ligne in corps_page.splitlines()
        if JETON_PRYSMARADITE in ligne and normalize(TOURNURE_NON_EXPORTEE) in normalize(ligne)
    ]
    if not lignes_prysma:
        constats.append(
            f"{PAGE} : la section « {TITRE_SAUVEGARDE} » ne dit pas, sur une meme ligne, que la "
            f"« {JETON_PRYSMARADITE} » « {TOURNURE_NON_EXPORTEE} » ; attendu cette phrase : la "
            f"prysmaradite n'appartient a aucun des {NOMBRE_GROUPES_EXPORT} groupes d'export "
            f"({SOURCE_DOFUSBOOK})"
        )
    url_import = _url_import()
    if f"`{url_import}`" not in corps_page:
        constats.append(
            f"{PAGE} : la section « {TITRE_SAUVEGARDE} » ne cite pas, entre accents graves, l'URL "
            f"d'import portee par {SOURCE_DOFUSBOOK} (DOFUSBOOK_IMPORT_URL : « {url_import} ») ; "
            f"attendu cette adresse, lue sur l'attribut public du module a chaque execution, et citee "
            f"entre accents graves car c'est une adresse technique, pas un lien externe (D-01)"
        )

    assert not constats, (
        f"{PAGE} : constats sur la limite de sauvegarde du navigateur et l'export Dofusbook (limite "
        f"lue dans {SOURCE_JS}:{LIGNE_MAX_SAVES}, cle lue dans {SOURCE_JS}:{LIGNE_SAVES_KEY}, export "
        f"eprouve par `build_dofusbook_url` de {SOURCE_DOFUSBOOK}) : "
        + " ; ".join(constats)
        + f" ; attendu la valeur « MAX_SAVES = {limite} » et la cle « {cle_stockage} » cites par la "
        f"section « {TITRE_SAUVEGARDE} », la tournure « {TOURNURE_EVICTION} », "
        f"{NOMBRE_EMPLACEMENTS_EXPORTES} emplacements exportes au plus et la "
        f"`{JETON_PRYSMARADITE}` exclue"
    )


def test_aucun_post_db_sans_patch() -> None:
    """Le harnais ne poste jamais `DB` : cette saisie ouvre un navigateur cote serveur (T-12).

    La saisie `DB` de l'ecran de resultat passe par `_open_dofusbook`, qui appelle
    `webbrowser.open_new_tab` **cote serveur** (`dofus_stuff/web/routes.py:1326-1337`) : un test qui
    la posterait sans patcher lancerait un navigateur pendant la suite. Le comportement est couvert,
    patche, par `tests/test_web.py:668` ; ce controle statique garantit que le present module ne la
    poste jamais.
    """
    arbre = ast.parse(Path(__file__).read_text(encoding="utf-8"))
    constats: list[str] = []

    importes = _imports_du_module(arbre)
    navigateur = sorted(
        module for module in importes if module == "webbrowser" or module.startswith("webbrowser.")
    )
    if navigateur:
        constats.append(
            f"import(s) de navigateur dans le module d'ancrage : {', '.join(navigateur)} ; attendu "
            f"aucun import de ce genre : la saisie `DB` ouvre un navigateur cote serveur "
            f"({SOURCE_ROUTES}:1326-1337)"
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
            if paires.get("cmd", "").strip().casefold() == "db":
                constats.append(
                    f"saisie `cmd` = « DB » postee ligne {noeud.lineno} ; attendu aucune saisie "
                    f"`DB` : elle appelle `webbrowser.open_new_tab` cote serveur "
                    f"({SOURCE_ROUTES}:1326-1337) et lancerait un navigateur pendant la suite — le "
                    f"comportement est couvert, patche, par tests/test_web.py:668"
                )

    assert not constats, (
        f"{PAGE} : constats sur la garde « aucun post de DB sans patch » : "
        + " ; ".join(constats)
        + f" ; attendu un module d'ancrage qui ne poste jamais `DB`, cette saisie ouvrant un "
        f"navigateur cote serveur ({SOURCE_ROUTES}:1326-1337)"
    )
