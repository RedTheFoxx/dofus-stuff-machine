# dofus-stuff-machine

Outils pour travailler avec les objets et ressources de Dofus : calculs, générateurs de panoplies, encyclopédie, etc.

## Documentation utilisateur

La documentation utilisateur commence par un sommaire unique : [Sommaire de la documentation](docs/sommaire.md).

## Base locale Dofus

Package Python stdlib (`dofus_stuff/`), basé sur l'API [Dofusdude](https://api.dofusdu.de/) ([documentation](https://docs.dofusdu.de)).

Une copie complète de la DB (équipements, ressources, consommables, quêtes, cosmétiques, montures, panoplies) est stockée en SQLite dans `.data/dofus.sqlite3`. Au chargement, si le dernier check date de plus de 24h, la version API est re-testée et la base resynchronisée si elle a changé. Les commandes CLI / calculs futurs travaillent ensuite depuis un catalogue chargé en mémoire.

### Prérequis

- Python 3.11+

### Installation

```bash
pip install -e ".[dev]"
```

### Usage CLI

```bash
python fetcher.py version
python -m dofus_stuff version

python fetcher.py search "Cape d'Atcham"
python fetcher.py search "Cape" --limit 20
python fetcher.py item 44
python fetcher.py list --page 1 --size 5
python fetcher.py self-test

# Optimiseur — démo / flags / interactif
python fetcher.py --offline optimize --demo
python fetcher.py --offline optimize --level 123 --max intelligence \
  --base-int 200 --scroll-int 100
python fetcher.py --offline optimize --demo --classic-only
python fetcher.py --offline optimize --level 200 --max intelligence \
  --target intelligence=1200 pa=11 --weight intelligence=2 \
  --ban 123 --force 456 --stop-when-satisfied --seed 42
python fetcher.py --offline optimize
```

Dans l’interface web (`python -m dofus_stuff.web`), **4. Optimisation de stuff**
ouvre une recommandation en trois choix : **classe, élément(s), niveau**.
Saisissez par exemple `Cra`, puis `terre air`, puis `123` pour lancer le calcul.
`multi` sélectionne les quatre éléments. Les noms de classes avec accents sont acceptés.

Les points de caractéristiques sont répartis automatiquement (5 par niveau gagné),
sans supposer de parchemins ni d'exos. Le score valorise les éléments choisis,
la puissance, les dommages, et l'élément le plus faible en multi. Des objectifs
souples de PA/PM et de vitalité accompagnent la progression. Les préférences de
portée, d'invocations et de distance/mêlée sont des heuristiques de classe modifiables.
La vitalité affichée est la vitalité ajoutée, pas le total de points de vie.

`AVANCE` ouvre les réglages détaillés ; après calcul, `EDIT` permet d'ajuster
le profil puis de relancer. Le design terminal et les raccourcis sont conservés.

**Guide détaillé :** [GUIDE_WIZARD.md](GUIDE_WIZARD.md)

Le solveur et la recherche locale utilisent le même score sur le build agrégé,
avec les bonus de panoplie et les cibles plafonnées. Le préfiltrage conserve aussi
des spécialistes par caractéristique. Les conditions évaluables sont vérifiées
après calcul ; les objectifs manqués et emplacements requis vides sont signalés.
L'indice de recherche ne mesure ni la qualité en combat ni une optimalité sur tout
le catalogue : CP-SAT travaille sur un sous-ensemble de candidats. Les prix,
les effets déclenchés et les rotations de sorts ne sont pas simulés. Certaines
conditions non numériques (quêtes, alignement, etc.) restent à vérifier en jeu.

Les bases de progression sont documentées dans le [guide des caractéristiques](https://dofusbuilds.com/guides/characteristic-points).
Les seuils PA/PM et poids de recommandation sont des choix du projet, pas des exigences du jeu.

#### Base locale

```bash
python fetcher.py db status
python fetcher.py db sync            # forcer une sync complète
python fetcher.py db clear           # vider la base
```

Les anciennes sous-commandes `cache stats|fill|clear` restent acceptées en alias.

#### Options globales

| Option | Description |
|--------|-------------|
| `--timeout N` | Timeout HTTP en secondes (défaut : 15) |
| `--data-dir DIR` | Répertoire de la base (défaut : `.data/`) |
| `--force-sync` | Ignorer la fenêtre 24h et forcer vérif/sync |
| `--offline` | Ne pas contacter l'API (échoue si base vide) |

### Interface web (terminal rétro)

```bash
python -m dofus_stuff.web
# ou : dofus-stuff-web
```

Par défaut : mode offline (base locale uniquement), écoute sur `http://127.0.0.1:5000`.

Le menu principal propose **1. Recherche d'objets**, **2. Liste des équipements**,
**3. Panoplies** et **4. Optimisation de stuff**. L'entrée **5. Système** regroupe le détail d'un équipement par ID,
la version locale, le self-test et la gestion de la base.

| Variable / option | Description |
|-------------------|-------------|
| `--data-dir DIR` / `DOFUS_DATA_DIR` | Répertoire de la base |
| `--offline` / `DOFUS_OFFLINE=1` | Pas d'API (défaut) |
| `--online` | Autoriser sync au démarrage / menu DB |
| `--timeout N` / `DOFUS_TIMEOUT` | Timeout HTTP |
| `--host` / `--port` | Bind HTTP |

### Tests

```bash
pytest
```

### Attribution

Données issues de [Dofusdude](https://dofusdu.de/) / [doduapi](https://github.com/dofusdude/doduapi).
