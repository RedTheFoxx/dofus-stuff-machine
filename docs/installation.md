# Installation

Cette page décrit l'installation de dofus-stuff-machine, du prérequis Python au premier lancement en ligne de commande.

## Prérequis

- Python 3.11+ : `pyproject.toml` déclare `requires-python = ">=3.11"`.

## Installation

```bash
pip install -e ".[dev]"
```

## Vérification

```bash
.venv/Scripts/python.exe -m pytest -q
```

## Premier lancement

```bash
python fetcher.py --offline db status
```

## Source de vérité

- `pyproject.toml` : dépendances, extra `dev` et configuration de pytest.
- `fetcher.py` : point d'entrée de la ligne de commande.
- `dofus_stuff/cli.py` : parseur et commandes réellement disponibles.

[Retour au sommaire](sommaire.md)
