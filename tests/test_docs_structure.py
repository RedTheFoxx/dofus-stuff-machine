"""Invariants de structure de la documentation utilisateur (sans import du produit)."""

import re
from pathlib import Path

LINK = re.compile(r"\[[^\]]*\]\((?P<target>[^)\s]+)\)")
H1 = re.compile(r"^#\s+(?P<title>.+?)\s*$", re.MULTILINE)

LIENS_EXTERNES = ("http://", "https://", "mailto:")
MOTIF_ABSOLU = re.compile(r"^[A-Za-z]:[\\/]")


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
