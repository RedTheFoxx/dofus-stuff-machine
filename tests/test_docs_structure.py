"""Invariants de structure de la documentation utilisateur (sans import du produit)."""

import re
import shutil
from pathlib import Path

LINK = re.compile(r"\[[^\]]*\]\((?P<target>[^)\s]+)\)")
H1 = re.compile(r"^#\s+(?P<title>.+?)\s*$", re.MULTILINE)

LIENS_EXTERNES = ("http://", "https://", "mailto:")
MOTIF_ABSOLU = re.compile(r"^[A-Za-z]:[\\/]")
H2 = re.compile(r"^##\s+(?P<titre>.+?)\s*$", re.MULTILINE)

# Ancrages du pilotage clavier (INST-03, D-09) et de la commande de lancement web.
TITRE_CLAVIER = "## Pilotage clavier"
LANCEMENT_WEB = "python -m dofus_stuff.web"
TOUCHES_CLAVIER = ("F3", "F7", "F8", "ESC", "PageUp", "PageDown")

# Jetons de commande destructrice interdits dans la page d'installation (T-01-05).
COMMANDE_DESTRUCTRICE = re.compile(r"\bdb\s+clear\b")
JETON_PURGE = "PURGE"


def _pages(docs_dir: Path) -> list[Path]:
    """Pages Markdown presentes sous docs/ ; liste vide si le dossier est absent (D-13)."""
    if not docs_dir.is_dir():
        return []
    return sorted(docs_dir.rglob("*.md"))


def _sommaire_absent() -> list[str]:
    """Probleme lisible du sommaire manquant, au lieu d'une exception (D-13)."""
    return [
        "docs/sommaire.md : absent ; attendu le point d'entree unique de la "
        "documentation utilisateur a la racine du depot (D-04)"
    ]


def problemes_liens(docs_dir: Path) -> list[str]:
    """Cibles de liens non resolues de docs/ ; chaque probleme cite la page, la cible et la racine (D-13)."""
    sommaire = docs_dir / "sommaire.md"
    if not sommaire.is_file():
        return _sommaire_absent()

    racine = docs_dir.parent.resolve()
    problemes: list[str] = []

    for page in _pages(docs_dir):
        nom = page.relative_to(docs_dir.parent).as_posix()
        for cible in LINK.findall(page.read_text(encoding="utf-8")):
            if cible.startswith(LIENS_EXTERNES):
                continue
            if "#" in cible:
                problemes.append(
                    f"{nom} : ancre interdite : {cible} ; attendu un lien de fichier a "
                    f"fichier vers une page de {docs_dir.name}/ (D-01, T-01-04)"
                )
                continue
            if cible.startswith("/") or MOTIF_ABSOLU.match(cible):
                problemes.append(
                    f"{nom} : cible absolue interdite : {cible} ; attendu une cible "
                    f"relative a {racine.as_posix()}"
                )
                continue
            if "\\" in cible:
                problemes.append(
                    f"{nom} : cible contenant un antislash interdite : {cible} ; attendu "
                    f"une cible relative a {racine.as_posix()}"
                )
                continue
            if cible.startswith("file://"):
                problemes.append(
                    f"{nom} : schema file:// interdit : {cible} ; attendu une cible "
                    f"relative a {racine.as_posix()}"
                )
                continue
            resolue = (page.parent / cible).resolve()
            if resolue != racine and racine not in resolue.parents:
                problemes.append(
                    f"{nom} : cible hors de la racine du depot : {cible} ; attendu un "
                    f"chemin sous {racine.as_posix()}"
                )
                continue
            if not resolue.exists():
                problemes.append(
                    f"{nom} : lien mort vers {cible} ; cible attendue sur disque sous "
                    f"{racine.as_posix()}"
                )
    return problemes


def problemes_index(docs_dir: Path) -> list[str]:
    """Egalite d'ensembles entre les cibles du sommaire et les pages presentes (SOMM-02, D-06)."""
    sommaire = docs_dir / "sommaire.md"
    if not sommaire.is_file():
        return _sommaire_absent()

    # Cibles du sommaire et pages presentes comparees comme chemins relatifs a docs/ (SOMM-02, D-06) :
    # une page imbriquee non listee est ainsi une derive, au lieu de passer pour un nom deja liste.
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


def test_docs_directory_has_sommaire(docs_dir: Path) -> None:
    """docs/ existe et contient le sommaire du point d'entree (SOMM-01, D-04)."""
    assert docs_dir.is_dir(), (
        f"docs/ : dossier absent : {docs_dir.as_posix()} ; attendu le dossier de "
        f"documentation a la racine du depot (D-04)"
    )
    sommaire = docs_dir / "sommaire.md"
    assert sommaire.is_file(), (
        f"docs/sommaire.md : page absente : {sommaire.as_posix()} ; attendu le point "
        f"d'entree unique de la documentation utilisateur (D-04)"
    )


def test_sommaire_lists_every_document(docs_dir: Path) -> None:
    """Le sommaire liste exactement les pages presentes sous docs/ (SOMM-02, D-06)."""
    problemes = problemes_index(docs_dir)
    assert problemes == [], "\n".join(problemes)


def test_sommaire_links_resolve(docs_dir: Path) -> None:
    """Chaque cible de lien de docs/sommaire.md se resout sur disque (SOMM-02, D-06)."""
    sommaire = docs_dir / "sommaire.md"
    assert sommaire.is_file(), (
        f"docs/sommaire.md : page absente : {sommaire.as_posix()} ; attendu le point "
        f"d'entree unique de la documentation utilisateur (D-04)"
    )
    problemes = [p for p in problemes_liens(docs_dir) if p.startswith("docs/sommaire.md")]
    assert problemes == [], "\n".join(problemes)


def test_all_relative_links_resolve(docs_dir: Path) -> None:
    """Chaque lien relatif de docs/ se resout sous la racine du depot (SOMM-02, T-01-04)."""
    problemes = problemes_liens(docs_dir)
    assert problemes == [], "\n".join(problemes)


def test_no_anchor_or_absolute_links(docs_dir: Path) -> None:
    """Aucune cible ne porte d'ancre, de chemin absolu, d'antislash ni de schema file:// (D-01, T-01-04)."""
    racine = docs_dir.parent
    problemes: list[str] = []

    for page in _pages(docs_dir):
        nom = page.relative_to(racine).as_posix()
        for cible in LINK.findall(page.read_text(encoding="utf-8")):
            if cible.startswith(LIENS_EXTERNES):
                continue
            if "#" in cible:
                problemes.append(
                    f"{nom} : ancre interdite : {cible} ; attendu un lien de fichier a "
                    f"fichier vers une page de {docs_dir.name}/ (T-01-04)"
                )
            elif cible.startswith("/") or MOTIF_ABSOLU.match(cible):
                problemes.append(
                    f"{nom} : cible absolue interdite : {cible} ; attendu une cible "
                    f"relative a {racine.as_posix()} (T-01-04)"
                )
            elif "\\" in cible:
                problemes.append(
                    f"{nom} : antislash interdit dans la cible : {cible} ; attendu une "
                    f"cible relative a {racine.as_posix()} (T-01-04)"
                )
            elif cible.startswith("file://"):
                problemes.append(
                    f"{nom} : schema file:// interdit : {cible} ; attendu une cible "
                    f"relative a {racine.as_posix()} (T-01-04)"
                )
    assert problemes == [], "\n".join(problemes)


def test_readme_links_to_sommaire(docs_dir: Path) -> None:
    """README.md porte un lien unique vers docs/sommaire.md et la cible existe (SOMM-01, D-10)."""
    racine = docs_dir.parent
    readme = racine / "README.md"
    assert readme.is_file(), (
        f"README.md : fichier absent : {readme.as_posix()} ; attendu le point d'entree "
        f"du lecteur a la racine du depot (SOMM-01)"
    )

    cibles = [
        cible
        for cible in LINK.findall(readme.read_text(encoding="utf-8"))
        if cible == "docs/sommaire.md"
    ]
    assert len(cibles) == 1, (
        f"README.md : {len(cibles)} lien(s) vers docs/sommaire.md dans "
        f"{readme.as_posix()} ; attendu exactement 1 cible docs/sommaire.md (D-10)"
    )
    assert (racine / "docs/sommaire.md").is_file(), (
        f"README.md : cible docs/sommaire.md absente sur disque : "
        f"{(racine / 'docs/sommaire.md').as_posix()} ; attendu docs/sommaire.md "
        f"a la racine du depot (SOMM-01, D-10)"
    )


def _page(docs_dir: Path, nom: str) -> Path:
    """Chemin de la page `nom` sous docs/ ; chemin theorique si elle est absente (D-13)."""
    for page in _pages(docs_dir):
        if page.name == nom:
            return page
    return docs_dir / nom


def _section(texte: str, titre: str) -> str | None:
    """Contenu de la section `titre` jusqu'au titre de niveau 2 suivant (None si le titre manque)."""
    debut = texte.find(titre)
    if debut == -1:
        return None
    suite = texte[debut + len(titre) :]
    suivant = H2.search(suite)
    return suite if suivant is None else suite[: suivant.start()]


def test_pilotage_clavier_avant_lancement(docs_dir: Path) -> None:
    """Le pilotage clavier est decrit avant la commande de lancement web (INST-03, D-09)."""
    page = _page(docs_dir, "installation.md")
    assert page.is_file(), (
        f"docs/installation.md : page absente : {page.as_posix()} ; attendu la page "
        f"d'installation du lecteur neuf (INST-01)"
    )
    texte = page.read_text(encoding="utf-8")

    position_clavier = texte.find(TITRE_CLAVIER)
    assert position_clavier != -1, (
        f"docs/installation.md : titre « {TITRE_CLAVIER} » absent de {page.as_posix()} ; "
        f"attendu une section decrivant le champ de saisie et les touches, source "
        f"dofus_stuff/web/static/js/terminal.js (INST-03, D-09)"
    )

    position_lancement = texte.find(LANCEMENT_WEB)
    assert position_lancement != -1, (
        f"docs/installation.md : commande de lancement « {LANCEMENT_WEB} » absente de "
        f"{page.as_posix()} ; attendu la commande de lancement de l'interface, source "
        f"dofus_stuff/web/__main__.py (INST-02)"
    )

    assert position_clavier < position_lancement, (
        f"docs/installation.md : ordre fautif dans {page.as_posix()} — le titre "
        f"« {TITRE_CLAVIER} » (position {position_clavier}) doit preceder la commande "
        f"« {LANCEMENT_WEB} » (position {position_lancement}) ; attendu le pilotage "
        f"clavier AVANT le lancement de l'interface (INST-03, D-09)"
    )

    section = _section(texte, TITRE_CLAVIER)
    assert section is not None, (
        f"docs/installation.md : section « {TITRE_CLAVIER} » introuvable ou vide dans "
        f"{page.as_posix()} ; attendu la description du pilotage clavier, source "
        f"dofus_stuff/web/static/js/terminal.js (INST-03, D-09)"
    )
    for touche in TOUCHES_CLAVIER:
        assert touche in section, (
            f"docs/installation.md : touche « {touche} » non documentee dans la section "
            f"« {TITRE_CLAVIER} » de {page.as_posix()} ; attendu cette touche, source "
            f"dofus_stuff/web/static/js/terminal.js (INST-03, D-09)"
        )


def test_no_destructive_command_in_installation(docs_dir: Path) -> None:
    """La page d'installation ne porte aucun jeton de commande destructrice (T-01-05)."""
    page = _page(docs_dir, "installation.md")
    assert page.is_file(), (
        f"docs/installation.md : page absente : {page.as_posix()} ; attendu la page "
        f"d'installation du lecteur neuf (INST-01)"
    )
    texte = page.read_text(encoding="utf-8")

    assert "--offline db status" in texte, (
        f"docs/installation.md : premier contact CLI « --offline db status » absent de "
        f"{page.as_posix()} ; attendu le seul premier contact hors-ligne de la page, "
        f"source dofus_stuff/cli.py (INST-01, T-01-06)"
    )

    destructrice = COMMANDE_DESTRUCTRICE.search(texte)
    assert destructrice is None, (
        f"docs/installation.md : commande destructrice trouvee : "
        f"« {destructrice.group(0) if destructrice else ''} » dans {page.as_posix()} ; "
        f"attendu aucune commande de vidage de la base locale, source "
        f"dofus_stuff/cli.py (T-01-05)"
    )
    assert JETON_PURGE not in texte, (
        f"docs/installation.md : jeton « {JETON_PURGE} » trouve dans {page.as_posix()} ; "
        f"attendu aucune commande de suppression des sauvegardes, source "
        f"dofus_stuff/web/routes.py (T-01-05)"
    )


# --- Gabarit de page : H1, ligne de retour, encodage, normalisation (SOMM-03, GARD-01) ---

# Entree d'index du sommaire avec son libelle et sa cible (meme source que problemes_index, SOMM-02, D-06).
LIEN_LIBELLE = re.compile(r"\[(?P<libelle>[^\]]*)\]\((?P<cible>[^)\s]+)\)")

# Jetons de brouillon interdits, compares sur le texte normalise (casse et accents ignores, D-11).
JETONS_BROUILLON = ("todo", "a completer", "lorem")

# Longueur minimale d'une page livree, en caracteres (GARD-01).
LONGUEUR_MINIMALE = 300


def _lire_page(page: Path) -> str | None:
    """Texte de la page lu en UTF-8 strict, ou None si le decodage echoue (GARD-01, D-11)."""
    try:
        return page.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return None


def pages_listees(docs_dir: Path) -> list[tuple[str, str]]:
    """Couples (libelle d'index, cible) des entrees de docs/sommaire.md, dans l'ordre du fichier (SOMM-02)."""
    sommaire = docs_dir / "sommaire.md"
    if not sommaire.is_file():
        return []
    return [
        (entree.group("libelle"), entree.group("cible"))
        for entree in LIEN_LIBELLE.finditer(sommaire.read_text(encoding="utf-8"))
    ]


def problemes_h1(docs_dir: Path, normalize) -> list[str]:
    """H1 unique de chaque page, egal a son libelle d'index (SOMM-03, D-11)."""
    sommaire = docs_dir / "sommaire.md"
    if not sommaire.is_file():
        return _sommaire_absent()

    libelles = {cible: libelle for libelle, cible in pages_listees(docs_dir)}
    problemes: list[str] = []

    for page in _pages(docs_dir):
        if page.name == "sommaire.md":
            continue
        nom = page.relative_to(docs_dir.parent).as_posix()
        libelle = libelles.get(page.relative_to(docs_dir).as_posix())

        if libelle is None:
            problemes.append(
                f"{nom} : page non listee dans docs/sommaire.md ; attendu une ligne "
                f"d'index dont le libelle egale le H1 de {page.as_posix()} (SOMM-03, D-06)"
            )

        texte = _lire_page(page)
        if texte is None:
            problemes.append(
                f"{nom} : fichier non decodable en UTF-8 strict ; attendu une page "
                f"decodable, listee dans docs/sommaire.md (GARD-01, D-11)"
            )
            continue

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
    return problemes


def problemes_retour_sommaire(docs_dir: Path) -> list[str]:
    """Chaque page renvoie au sommaire par un lien dont la cible resolue est sommaire.md (SOMM-03, D-01)."""
    sommaire = docs_dir / "sommaire.md"
    if not sommaire.is_file():
        return _sommaire_absent()

    cible_sommaire = sommaire.resolve()
    problemes: list[str] = []

    for page in _pages(docs_dir):
        if page.name == "sommaire.md":
            continue
        nom = page.relative_to(docs_dir.parent).as_posix()
        texte = _lire_page(page)
        if texte is None:
            problemes.append(
                f"{nom} : fichier non decodable en UTF-8 strict ; attendu une page "
                f"portant un lien vers {cible_sommaire.as_posix()} (SOMM-03, D-11)"
            )
            continue

        retour = any(
            (page.parent / cible).resolve() == cible_sommaire
            for cible in LINK.findall(texte)
            if not cible.startswith(LIENS_EXTERNES)
        )
        if not retour:
            problemes.append(
                f"{nom} : aucune ligne de retour vers docs/sommaire.md ; attendu un lien "
                f"dont la cible resolue est {cible_sommaire.as_posix()} dans "
                f"{page.as_posix()} (SOMM-03, D-01)"
            )
    return problemes


def problemes_encodage(docs_dir: Path, normalize) -> list[str]:
    """Decodage UTF-8 strict, absence de jeton de brouillon et longueur minimale (GARD-01, D-11)."""
    problemes: list[str] = []

    for page in _pages(docs_dir):
        nom = page.relative_to(docs_dir.parent).as_posix()
        texte = _lire_page(page)
        if texte is None:
            problemes.append(
                f"{nom} : fichier non decodable en UTF-8 strict ; attendu une page "
                f"decodable, listee dans docs/sommaire.md (GARD-01, D-11)"
            )
            continue

        normalise = normalize(texte)
        for jeton in JETONS_BROUILLON:
            if jeton in normalise:
                problemes.append(
                    f"{nom} : jeton de brouillon « {jeton} » present dans "
                    f"{page.as_posix()} ; attendu une page redigee, listee dans "
                    f"docs/sommaire.md (GARD-01)"
                )

        longueur = len(texte.strip())
        if longueur < LONGUEUR_MINIMALE:
            problemes.append(
                f"{nom} : page de {longueur} caracteres dans {page.as_posix()} ; attendu "
                f"au moins {LONGUEUR_MINIMALE} caracteres pour une page livree (GARD-01)"
            )
    return problemes


def test_h1_matches_sommaire_entry(docs_dir: Path, normalize) -> None:
    """Chaque page porte un unique H1 egal a son libelle d'index (SOMM-03, D-11)."""
    problemes = problemes_h1(docs_dir, normalize)
    assert problemes == [], "\n".join(problemes)


def test_pages_have_back_link(docs_dir: Path) -> None:
    """Chaque page porte une ligne de retour vers docs/sommaire.md (SOMM-03, D-01)."""
    problemes = problemes_retour_sommaire(docs_dir)
    assert problemes == [], "\n".join(problemes)


def test_documents_are_utf8_and_not_drafts(docs_dir: Path, normalize) -> None:
    """Chaque page est en UTF-8 strict, sans jeton de brouillon et assez longue (GARD-01)."""
    problemes = problemes_encodage(docs_dir, normalize)
    assert problemes == [], "\n".join(problemes)


def test_sommaire_index_labels_are_unique(docs_dir: Path, normalize) -> None:
    """Deux entrees d'index ne portent pas le meme libelle, et le sommaire ne s'auto-liste pas (SOMM-02)."""
    cible_sommaire = (docs_dir / "sommaire.md").resolve()
    problemes: list[str] = []
    vus: dict[str, str] = {}

    for libelle, cible in pages_listees(docs_dir):
        cle = normalize(libelle)
        if cle in vus:
            problemes.append(
                f"docs/sommaire.md : libelle d'index « {libelle} » deja porte par "
                f"« {vus[cle]} » ; attendu un libelle distinct par page listee "
                f"(SOMM-02, SOMM-03)"
            )
        else:
            vus[cle] = libelle

        if (docs_dir / cible).resolve() == cible_sommaire:
            problemes.append(
                f"docs/sommaire.md : le sommaire se liste lui-meme comme cible "
                f"« {cible} » ; attendu uniquement les pages de contenu de docs/ "
                f"(SOMM-02, D-05)"
            )

    assert problemes == [], "\n".join(problemes)


def test_normalisation_insensible_aux_accents_et_casse(normalize) -> None:
    """La normalisation de D-11 unifie accents, casse, entites HTML, espaces et fins de ligne (D-11, D-12)."""
    reference = "tests/conftest.py::_normalize (D-11, D-12)"

    assert normalize("Éléments") == normalize("elements"), (
        "normalisation : « Éléments » et « elements » doivent donner la meme valeur "
        f"normalisee ; attendu la normalisation de {reference}"
    )
    assert normalize("l&#39;objet") == normalize("l'objet"), (
        "normalisation : l'entite HTML « &#39; » et l'apostrophe droite doivent donner "
        f"la meme valeur normalisee ; attendu la normalisation de {reference}"
    )
    assert normalize("A  \t B") == normalize("A B"), (
        "normalisation : les espaces multiples (dont tabulation) doivent etre reduits a "
        f"une espace simple ; attendu la normalisation de {reference}"
    )
    assert normalize("a\r\nb") == normalize("a\nb"), (
        "normalisation : les fins de ligne CRLF et LF doivent donner la meme valeur "
        f"normalisee ; attendu la normalisation de {reference}"
    )


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

    page = copie / "installation.md"
    livree = docs_dir / "installation.md"

    # Derive (a) : ligne de retour devenue un lien mort dans la copie.
    page.write_text(
        page.read_text(encoding="utf-8").replace("(sommaire.md)", "(sommaire.mrd)"),
        encoding="utf-8",
    )
    liens = problemes_liens(copie)
    assert any("sommaire.mrd" in probleme for probleme in liens), (
        "copie de docs/ : le lien mort vers sommaire.mrd injecte dans installation.md "
        "n'est pas detecte par problemes_liens() ; attendu un probleme nommant la "
        "cible injectee (critere 5, GARD-01)\n" + "\n".join(liens)
    )

    # Derive (b) : page presente dans la copie mais absente de l'index du sommaire.
    (copie / "glossaire.md").write_text(
        "# Glossaire\r\n\r\nPage injectee par le test de mutation.\r\n", encoding="utf-8"
    )
    index = problemes_index(copie)
    assert any("glossaire.md" in probleme for probleme in index), (
        "copie de docs/ : la page glossaire.md non listee dans sommaire.md n'est pas "
        "detectee par problemes_index() ; attendu un probleme nommant glossaire.md "
        "(critere 5, GARD-01)\n" + "\n".join(index)
    )

    # Derive (c) : H1 divergent du libelle d'index, dans la copie seulement.
    page.write_text(
        page.read_text(encoding="utf-8").replace("# Installation", "# Installation provisoire", 1),
        encoding="utf-8",
    )
    titres = problemes_h1(copie, normalize)
    assert any("Installation provisoire" in probleme for probleme in titres), (
        "copie de docs/ : le H1 divergent « Installation provisoire » injecte dans "
        "installation.md n'est pas detecte par problemes_h1() ; attendu un probleme "
        "nommant le H1 injecte (critere 5, SOMM-03, D-11)\n" + "\n".join(titres)
    )

    # L'arbre livre n'a pas ete touche : la mutation ne vit que dans tmp_path (T-01-07).
    texte_livre = livree.read_text(encoding="utf-8")
    assert "(sommaire.md)" in texte_livre, (
        f"docs/installation.md livre : la ligne de retour vers sommaire.md a disparu de "
        f"{livree.as_posix()} ; attendu un arbre livre intact, la mutation ne s'appliquant "
        f"qu'a {copie.as_posix()} (T-01-07, critere 5)"
    )
    assert texte_livre.startswith("# Installation"), (
        f"docs/installation.md livre : le H1 « # Installation » a disparu de "
        f"{livree.as_posix()} ; attendu un arbre livre intact, la mutation ne s'appliquant "
        f"qu'a {copie.as_posix()} (T-01-07, critere 5)"
    )
    assert not (docs_dir / "glossaire.md").exists(), (
        f"docs/glossaire.md : page injectee presente dans l'arbre livre : "
        f"{(docs_dir / 'glossaire.md').as_posix()} ; attendu cette page uniquement dans la "
        f"copie jetable, jamais sous docs/ (T-01-07, critere 5)"
    )
