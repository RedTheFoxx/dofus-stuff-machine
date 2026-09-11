# CLI

Cette page décrit la ligne de commande de dofus-stuff-machine : les sous-commandes de `fetcher.py`, les options qu'elles acceptent, les valeurs par défaut relevées dans le parseur et un exemple analysable par commande.

Le point d'entrée est `fetcher.py`, à la racine du dépôt : les commandes de cette page s'écrivent depuis cette racine. Le parseur de la ligne de commande ne connaît que les options déclarées dans `dofus_stuff/cli.py` : cette page n'en présente donc aucune qui ne soit définie dans le produit.

## Options globales

Les options globales sont déclarées sur le parseur racine du programme : elles s'écrivent **avant** la sous-commande, qui reçoit ensuite ses propres options.

| Option | Rôle | Défaut |
|--------|------|--------|
| `--timeout` | délai HTTP en secondes | `15` |
| `--data-dir` | répertoire de la base locale | le dossier `.data/` à la racine du dépôt |
| `--force-sync` | ignorer la fenêtre 24 h et forcer une vérification / synchronisation de version | faux |
| `--offline` | ne pas contacter l'API (échoue si la base locale est vide) | faux |

Chaque défaut de ce tableau est la valeur que le parseur donne à l'option quand elle n'est pas écrite. L'aide de `--data-dir` imprime le chemin absolu du dossier utilisé sur la machine courante : c'est une valeur propre au poste, à ne jamais recopier telle quelle.

Les options globales n'existent qu'au niveau racine du parseur : elles s'écrivent **avant** la sous-commande. La forme fautive `db status --offline` est refusée, le parseur imprimant la ligne suivante sur sa sortie d'erreur et sortant avec le code de retour 2 (source du parseur : `dofus_stuff/cli.py`).

```text
fetcher.py: error: unrecognized arguments: --offline
```

`--offline` et la synchronisation de la base sont en revanche **incompatibles** : la synchronisation a besoin du réseau. La commande `--offline db sync` sort avec le code de retour 1 et le message suivant. La règle « toutes les commandes portent `--offline` » de la page d'installation ne s'applique donc pas ici, où les commandes de synchronisation sont décrites à part. Le détail de la fenêtre de 24 h et de la resynchronisation est traité avec la base locale.

```text
Erreur : --offline incompatible avec db sync
```

## version

Afficher la version Dofus de la base locale. Cette sous-commande n'accepte aucune option propre.

```console
python fetcher.py --offline version
```

## self-test

Vérifier la base locale et des objets connus. Cette sous-commande n'accepte aucune option propre.

```console
python fetcher.py --offline self-test
```

## search

Rechercher des objets dans la base locale.

| Élément | Rôle | Défaut |
|---------|------|--------|
| `query` | terme de recherche (sensible à la casse) | requis |
| `--limit` | nombre maximum de résultats | `10` |

```console
python fetcher.py --offline search Atcham
```

## item

Afficher le détail d'un équipement par son ID Ankama.

| Élément | Rôle | Défaut |
|---------|------|--------|
| `ankama_id` | ID Ankama de l'objet, entier | requis |

```console
python fetcher.py --offline item 44
```

## list

Lister une page d'équipements.

| Élément | Rôle | Défaut |
|---------|------|--------|
| `--page` | numéro de page | `1` |
| `--size` | taille de page | `5` |

```console
python fetcher.py --offline list --page 2
```

## optimize

Optimiser un stuff pour un niveau et une ou des caractéristiques.

Sans `--level`, sans `--max` et sans `--demo`, aucun profil n'est fourni : `python fetcher.py --offline optimize` ouvre alors les questions guidées, choisies par la fonction de `dofus_stuff/optimize/profile_input.py`. Cette ligne est décrite en prose plutôt que donnée en exemple : la suite du parcours dépend des réponses.

Les options propres à cette sous-commande sont réparties en quatre groupes.

### Profil et objectifs

| Option | Rôle | Défaut |
|--------|------|--------|
| `--level` | niveau du personnage | aucun |
| `--max` | caractéristique(s) à maximiser (ex : intelligence) | aucune |
| `--target` | cibles `STAT=valeur` (ex : intelligence=1200 pa=11) | aucune |
| `--weight` | poids `STAT=valeur` (ex : intelligence=2 vitalite=0.5) | aucun |
| `--auto-points` | répartir automatiquement les points de caractéristiques | faux |
| `--demo` | profil de démonstration niveau 123 / maximum en intelligence, qui ignore `--level`, `--max` et les caractéristiques de base | faux |
| `--stop-when-satisfied` | s'arrêter dès que les cibles sont atteintes | faux |

### Contraintes de sélection

| Option | Rôle | Défaut |
|--------|------|--------|
| `--ban` | IDs Ankama interdits | aucun |
| `--force` | IDs Ankama obligatoires | aucun |
| `--classic-only` | ignorer Dofus, trophées, familier et prysmaradite | faux |
| `--allow-power` | autoriser la puissance à la place des caractéristiques | faux |
| `--allow-damages` | autoriser les dommages à la place des dommages élémentaires | faux |
| `--allow-crit-damages` | autoriser les dommages critiques à la place des dommages élémentaires | faux |

### Caractéristiques de base et scrolls

| Option | Rôle | Défaut |
|--------|------|--------|
| `--base-int` | intelligence hors stuff (capital déjà converti) | `0` |
| `--base-vit` | aucune description dans l'aide du parseur | `0` |
| `--base-str` | aucune description dans l'aide du parseur | `0` |
| `--base-cha` | aucune description dans l'aide du parseur | `0` |
| `--base-agi` | aucune description dans l'aide du parseur | `0` |
| `--base-wis` | aucune description dans l'aide du parseur | `0` |
| `--scroll-int` | aucune description dans l'aide du parseur | `0` |
| `--scroll-vit` | aucune description dans l'aide du parseur | `0` |
| `--scroll-str` | aucune description dans l'aide du parseur | `0` |
| `--scroll-cha` | aucune description dans l'aide du parseur | `0` |
| `--scroll-agi` | aucune description dans l'aide du parseur | `0` |
| `--scroll-wis` | aucune description dans l'aide du parseur | `0` |

Onze de ces douze options n'ont aucune description dans l'aide du parseur : elles sont donc données par leur nom et leur valeur par défaut, sans ajouter un sens que le produit ne déclare pas.

### RNG et performances

| Option | Rôle | Défaut |
|--------|------|--------|
| `--jet` | mode de jets d'objets, l'un de `min`, `average` ou `max` | `average` |
| `--top-k` | candidats top-K par slot | `30` |
| `--time-limit` | délai CP-SAT en secondes | `5.0` |
| `--no-cpsat` | désactiver CP-SAT (greedy et recherche locale uniquement) | faux |
| `--seed` | graine du générateur aléatoire | aucune |

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
