"""Invariants de structure de la documentation utilisateur (sans import du produit)."""

import re
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
            if cible.startswith(LIENS_EXTERNES) or cible.startswith("#"):
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

    cibles = set(LINK.findall(sommaire.read_text(encoding="utf-8")))
    pages = {page.name for page in _pages(docs_dir) if page.name != "sommaire.md"}

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
            if cible.startswith("#"):
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
