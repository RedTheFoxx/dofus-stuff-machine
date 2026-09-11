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
"""

from __future__ import annotations

import ast
import re
from pathlib import Path
from unittest.mock import patch

from dofus_stuff.optimize.recommend import CLASSES, ELEMENTS

RACINE_DEPOT = Path(__file__).resolve().parents[1]
PAGE = "parcours-simplifie.md"
SOMMAIRE = "sommaire.md"
SOURCE_ROUTES = "dofus_stuff/web/routes.py"
SOURCE_RECOMMEND = "dofus_stuff/optimize/recommend.py"
SOURCE_API = "dofus_stuff/optimize/api.py"
SOURCE_JS = "dofus_stuff/web/static/js/terminal.js"
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
