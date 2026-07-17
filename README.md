# dofus-stuff-machine

Outils pour travailler avec les objets et ressources de Dofus : calculs, générateurs de panoplies, encyclopédie, etc.

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

Dans l’interface web (`python -m dofus_stuff.web`) : menu **7. OPTIMISATION DE STUFF**
ouvre directement le **wizard Stuffer** (slots, filtres, cibles/poids, items, options).

**Guide débutant détaillé :** [GUIDE_WIZARD.md](GUIDE_WIZARD.md)

Le wizard permet de configurer slots, filtres de types, base/points/cible/poids par carac,
exo PA/PM/PO, items interdits/forcés, substitutions et options solveur.

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
