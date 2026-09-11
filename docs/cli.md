# CLI

Cette page décrit la ligne de commande de dofus-stuff-machine : les sous-commandes de `fetcher.py`, les options qu'elles acceptent, les valeurs par défaut relevées dans le parseur et un exemple analysable par commande.

Le point d'entrée est `fetcher.py`, à la racine du dépôt : les commandes de cette page s'écrivent depuis cette racine.

## Options globales

Les options globales sont déclarées sur le parseur racine du programme : elles s'écrivent **avant** la sous-commande, qui reçoit ensuite ses propres options.

| Option | Rôle | Défaut |
|--------|------|--------|
| `--timeout` | délai HTTP en secondes | `15` |
| `--data-dir` | répertoire de la base locale | le dossier `.data/` à la racine du dépôt |
| `--force-sync` | ignorer la fenêtre 24 h et forcer une vérification / synchronisation de version | faux |
| `--offline` | ne pas contacter l'API (échoue si la base locale est vide) | faux |

## version

Afficher la version Dofus de la base locale.

```console
python fetcher.py --offline version
```

## self-test

Vérifier la base locale et des objets connus.

```console
python fetcher.py --offline self-test
```

## search

Rechercher des objets dans la base locale.

```console
python fetcher.py --offline search Atcham
```

## item

Afficher le détail d'un équipement par son ID Ankama.

```console
python fetcher.py --offline item 44
```

## list

Lister une page d'équipements.

```console
python fetcher.py --offline list --page 2
```

## optimize

Optimiser un stuff pour un niveau et une ou des caractéristiques.

```console
python fetcher.py --offline optimize --demo
```

## db

Gérer la base locale.

```console
python fetcher.py --offline db status
```

## cache

`cache` est le second nom des mêmes sous-commandes que `db` : la forme `cache <sous-commande>` est équivalente à `db <sous-commande>`.

```console
python fetcher.py --offline cache status
```

## Source de vérité

- `fetcher.py` : point d'entrée de la ligne de commande.
- `dofus_stuff/cli.py` : parseur et commandes réellement disponibles ; la fonction `build_parser()` y déclare la surface documentée ici.
- `dofus_stuff/database.py` : suppression effective des tables par `db clear`, la commande destructrice qui vide la base locale.
- `dofus_stuff/optimize/profile_input.py` : choix du mode interactif de l'optimisation.

[Retour au sommaire](sommaire.md)
