# Walking Skeleton — dofus-stuff-machine (documentation utilisateur)

**Phase:** 1 — Socle documentaire, installation et harnais vérifiable
**Generated:** 2026-09-11
**Note de cadrage :** ce projet n'est pas une application à construire mais un **milestone documentaire** sur un produit figé. Le « Walking Skeleton » est donc la plus petite chaîne **documentation + garde-fou** traversant toutes les couches que les phases suivantes réutiliseront : pages `docs/`, point d'entrée `README.md`, harnais `pytest`, ancrage sur les surfaces publiques du code. Les champs du gabarit sont conservés ; les valeurs sont celles du projet réel, aucune couche n'est inventée.

## Capability Proven End-to-End

Un lecteur ouvre `README.md`, atteint `docs/sommaire.md` par un lien unique, puis `docs/installation.md` ; et une dérive injectée dans une copie de `docs/` (lien mort, page non listée, H1 divergent) fait échouer la suite `.venv/Scripts/python.exe -m pytest -q` alors que l'arbre livré reste vert.

## Architectural Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Format de documentation | Markdown nu, un thème par fichier, `docs/` à plat (ASCII minuscule, `kebab-case`) | Décision amont (`OUT2-01` hors périmètre) : aucune dépendance de générateur, structure vérifiable par des tests simples |
| Point d'entrée | `README.md` → un lien unique vers `docs/sommaire.md` (D-10) ; le sommaire croît par phase (D-05) | Une information à un seul endroit ; l'exhaustivité bidirectionnelle reste un vrai signal |
| Gabarit de page | H1 unique, phrase d'introduction, sections courtes, bloc « Source de vérité », ligne de retour (D-01) | Gabarit pauvre ⇒ deux expressions régulières suffisent à le contrôler |
| Harnais de vérification | `pytest` 9.1.1 déjà installé (`[tool.pytest.ini_options]` dans `pyproject.toml`), helpers dans `tests/conftest.py` (D-12) | Aucune dépendance nouvelle ; les fixtures existantes (`catalog`, `app`, `client`) restent inchangées |
| Interpréteur de référence | `.venv/Scripts/python.exe` (D-15) | Shell de ce poste Windows ; le `python` ambiant n'a pas `pytest` |
| Ancrage au code | Surfaces publiques uniquement : `dofus_stuff/web/__main__.py::build_parser` (`parse_args`, `format_help`) et `dofus_stuff/cli.py::build_parser` (D-14) | `argparse` sort par `SystemExit(2)` : chaque sonde convertit cet exit en assertion localisante (D-13) |
| Comparaison de libellés | Toujours après normalisation (entités HTML, accents, casse, espaces, CRLF/LF) (D-11) | Le rendu échappe l'apostrophe (`D&#39;OBJETS`) : la comparaison brute serait fausse |
| Écriture pendant les tests | Uniquement dans `tmp_path` (copie via `shutil.copytree`) | L'arbre `docs/` est la source de vérité et `.data/dofus.sqlite3` ne doit jamais être touchée |
| Exécution locale documentée | `pip install -e ".[dev]"` puis `.venv/Scripts/python.exe -m pytest -q`, premier contact CLI `python fetcher.py --offline db status`, interface web `python -m dofus_stuff.web` sur `http://127.0.0.1:5000` | Remplace le « deployment target » : aucun déploiement distant n'existe ni n'est autorisé ; l'exécution locale documentée exerce la chaîne complète |

## Stack Touched in Phase 1

- [x] Socle : `README.md` (section « Documentation utilisateur »), `docs/sommaire.md`, `docs/installation.md`
- [x] Lecture réelle du disque : helpers purs `(docs_dir: Path) -> list[str]` exécutés contre l'arbre livré
- [x] Écriture réelle (isolée) : mutation sur `shutil.copytree(docs_dir, tmp_path / "docs")` — jamais `docs/`, jamais `.data/`
- [x] Interaction réelle avec le produit : `build_parser()`, `parse_args`, `format_help` (aucun `main()`, aucune base, aucune socket)
- [x] Exécution locale documentée et reproductible : `pytest -q` (suite complète) et lancement web sur l'adresse par défaut

## Out of Scope (Deferred to Later Slices)

- `docs/cli.md` (phase 2), `docs/parcours-simplifie.md` (phase 3), `docs/wizard-avance.md` et résorption de `GUIDE_WIZARD.md` (phase 4), `docs/base-locale.md` (phase 5), `docs/depannage.md` + `docs/glossaire.md` + liste épinglée des 8 pages (phase 6).
- Générateur de site statique (MkDocs/Sphinx), vérificateur de liens externes, intégration continue distante (`OUT2-01`, `OUT2-02`, `OUT2-03`).
- Toute modification de `dofus_stuff/**`, toute nouvelle dépendance, toute écriture sous `.data/`, tout accès réseau, toute publication.
- Contrôle des renvois obsolètes (phase 4), test de mutation élargi et complétude épinglée (phase 6).

## Subsequent Slice Plan

Chaque phase suivante ajoute une tranche verticale **doc + contrôle** sur la même architecture, sans la modifier :

- **Phase 2** : `docs/cli.md` + ancrage des sous-commandes, options globales, options d'`optimize` et des exemples (analyse par `shlex` + parseur réel).
- **Phase 3** : `docs/parcours-simplifie.md` + contrôles de rendu (client de test Flask) sur les libellés du flux simplifié.
- **Phase 4** : `docs/wizard-avance.md` devient la source unique ; `GUIDE_WIZARD.md` réduit à un aiguillage ; contrôle des renvois obsolètes observé rouge puis vert.
- **Phase 5** : `docs/base-locale.md` + contrôles d'ancrage des noms de champs, sans écriture sous `.data/` ni réseau.
- **Phase 6** : `docs/depannage.md`, `docs/glossaire.md`, liste épinglée des 8 pages, complétude vérifiée et preuve finale que les garde-fous mordent.
