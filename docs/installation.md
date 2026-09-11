# Installation

Cette page décrit l'installation de dofus-stuff-machine, du prérequis Python au premier lancement en ligne de commande.

Le pilotage clavier de l'interface, puis son lancement dans le navigateur, sont décrits plus bas dans la même page.

## Prérequis

- **Python 3.11 ou plus récent** : `pyproject.toml` déclare `requires-python = ">=3.11"`.
- **`pip`**, fourni avec Python : c'est le seul gestionnaire de paquets utilisé par le projet.
- **`pytest`**, apporté par l'extra `dev` du projet : il n'y a rien d'autre à installer pour vérifier l'installation.

## Installation

1. Créer un environnement virtuel à la racine du dépôt :

```bash
python -m venv .venv
```

2. Activer cet environnement virtuel, puis installer le projet en mode éditable avec son extra `dev` :

```bash
pip install -e ".[dev]"
```

Cette commande est la seule procédure d'installation documentée : `pip` suffit, aucun autre gestionnaire de paquets n'est utilisé par le projet.

## Vérification

```bash
.venv/Scripts/python.exe -m pytest -q
```

La commande doit se terminer sans échec. Elle utilise l'interpréteur de l'environnement virtuel du dépôt : l'interpréteur Python du système, lui, n'a pas `pytest` installé.

Le nombre de tests affiché change à chaque phase du projet : ce n'est pas une valeur de référence, seul compte le fait qu'aucun test ne soit en échec.

## Premier lancement

```bash
python fetcher.py --offline db status
```

C'est le premier contact conseillé avec la ligne de commande :

- l'option globale `--offline` est placée **avant** la sous-commande `db status` ;
- la commande n'ouvre aucune connexion réseau et ne déclenche aucune resynchronisation Dofusdude ;
- elle **crée** la base locale si elle est absente, puis affiche ses caractéristiques : fichier utilisé, version du jeu, date du dernier contrôle et nombre d'entrées.

Les autres commandes (`version`, `search`, `self-test`, `optimize`) n'affichent un résultat que sur une base locale **déjà peuplée**. Obtenir une base peuplée suppose une synchronisation réseau (`db sync`) : cela sort du chemin minimal de cette page et n'y est pas documenté.

## Pilotage clavier

L'interface se pilote entièrement au clavier. Le champ de saisie situé en bas de l'écran reçoit le texte : on y tape la commande ou la réponse, puis on valide avec la touche Entrée (nom d'événement `Enter`). Un clic ailleurs sur la page ramène automatiquement le curseur dans ce champ.

Les touches actives, quel que soit l'écran :

| Touche | Effet | Libellé affiché |
|--------|-------|-----------------|
| `F3` | quitter l'interface | « Quitter » |
| `F7` | écran ou page précédente | « Precedent » ou « Page prec » |
| `F8` | écran ou page suivante | « Suivant » ou « Page suiv » |
| `ESC` | revenir en arrière | « Retour » |
| `PageUp` | page précédente | — |
| `PageDown` | page suivante | — |

- La touche `ESC` correspond à l'événement clavier nommé `Escape`.
- La barre de raccourcis affichée en bas d'écran est construite dynamiquement : sur le menu principal elle n'affiche que `F3` (« Quitter ») ; `F7` et `F8` n'y apparaissent que sur un écran paginé ou à une étape du wizard. Les touches du tableau restent actives partout, même quand la barre ne les montre pas.

Sources : `dofus_stuff/web/routes.py` (libellés affichés) et `dofus_stuff/web/static/js/terminal.js` (gestion des touches).

## Lancement de l'interface web

```bash
python -m dofus_stuff.web
```

L'interface démarre **en mode hors-ligne par défaut** : `--offline` est actif sans rien préciser. `--no-offline`, ou son équivalent `--online`, autorise le contact avec l'API Dofusdude.

Elle écoute par défaut sur `http://127.0.0.1:5000` : une fois le serveur lancé, ouvrir cette adresse dans un navigateur. `Ctrl+C` dans le terminal arrête le serveur. Sans base locale peuplée, l'interface démarre quand même (la base est créée si elle est absente), mais elle n'affiche alors aucun objet.

Options d'entrée de la commande :

| Option | Rôle |
|--------|------|
| `--data-dir` | répertoire de la base locale |
| `--offline` | ne pas contacter l'API (actif par défaut) |
| `--no-offline` | contacter l'API au démarrage |
| `--online` | équivalent de `--no-offline` |
| `--timeout` | délai HTTP en secondes |
| `--host` | adresse d'écoute (valeur par défaut `127.0.0.1`) |
| `--port` | port d'écoute (valeur par défaut `5000`) |

Seule l'adresse locale par défaut est documentée ici : faire écouter ce serveur de développement, qui n'a pas d'authentification, sur une autre interface réseau n'est pas décrit.

L'option `--debug` est réservée au développement : elle active le serveur de débogage de Flask et ne fait pas partie du chemin minimal.

## Erreurs fréquentes

### Base locale vide et mode hors-ligne

Sur une installation neuve (dossier `.data/` absent), la commande suivante échoue :

```bash
python fetcher.py --offline version
```

Elle se termine avec le code de retour 1 et la sortie d'erreur :

```text
Erreur : Base locale vide et --offline : impossible de synchroniser
```

Le message est levé par la garde hors-ligne `if offline:` de `ensure_up_to_date` dans `dofus_stuff/sync.py`, et `dofus_stuff/cli.py` l'affiche sous la forme `Erreur : <message>`.

**Solution** : commencer par la commande hors-ligne `python fetcher.py --offline db status` du chemin minimal, qui crée la base locale si elle est absente. Les commandes qui lisent réellement le catalogue demandent ensuite une base peuplée, obtenue par une synchronisation réseau (`db sync`), hors de cette page.

### Option globale placée après la sous-commande

Les options globales `--offline`, `--data-dir`, `--timeout` et `--force-sync` n'existent qu'au niveau racine du parseur : elles s'écrivent **avant** la sous-commande. La forme fautive `db status --offline` est refusée par le parseur, qui imprime sur sa sortie d'erreur la ligne `fetcher.py: error: unrecognized arguments: --offline` et sort avec le code 2 (source du parseur : `dofus_stuff/cli.py`).

### Ordre correct des options

Les options globales se placent **avant** la sous-commande, qui reçoit ensuite ses propres options. Autrement dit : `python fetcher.py --offline db status` est correct, alors que la même option placée après `db status` ne l'est pas.

### Ne jamais omettre le mode hors-ligne

Sans `--offline`, la ligne de commande interroge l'API Dofusdude par défaut et peut donc consommer le quota distant. C'est pourquoi **toutes** les commandes `fetcher.py` présentées dans cette page portent le drapeau hors-ligne.

## Source de vérité

- `pyproject.toml` : dépendances, extra `dev` et configuration de pytest.
- `fetcher.py` : point d'entrée de la ligne de commande.
- `dofus_stuff/cli.py` : parseur et commandes réellement disponibles.
- `dofus_stuff/sync.py` : synchronisation de la base locale et garde du mode hors-ligne.
- `dofus_stuff/web/__main__.py` : options et valeurs par défaut de l'interface web.
- `dofus_stuff/web/routes.py` : écrans et libellés affichés par l'interface web.
- `dofus_stuff/web/static/js/terminal.js` : gestion des touches du clavier.

[Retour au sommaire](sommaire.md)
