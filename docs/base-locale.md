# Base locale

Cette page décrit ce que l'outil garde sur votre poste : la base locale dans laquelle les fiches d'objets Dofus sont enregistrées, les catégories qui y entrent, et la fenêtre au bout de laquelle l'outil interroge de nouveau l'API Dofusdude. Tous les noms cités ici sont lus dans les constantes publiques de `dofus_stuff/database.py` et `dofus_stuff/sync.py` : cette page décrit le code de ce dépôt, elle ne recopie aucun chemin de votre poste. La surface des commandes, elle, est décrite par [la page CLI](cli.md).

## Le fichier de la base

L'outil range toute sa copie locale des données Dofus dans un seul fichier SQLite : `dofus.sqlite3`, placé dans le dossier `.data/` à la racine du dépôt. Le nom du fichier vient de la constante `DB_NAME` et le dossier de la constante `DEFAULT_DATA_DIR` : ni l'un ni l'autre n'est écrit deux fois dans le produit, et cette page les reprend tels quels.

Le fichier est créé au **premier contact**, c'est-à-dire au premier lancement d'une commande ou d'un écran qui touche la base : le dossier parent est créé s'il manque, puis le fichier lui-même. Une base absente n'est donc pas une erreur : c'est une base vide, que l'outil remplit à la première synchronisation.

Le fichier contient deux tables et un index, tous créés par `Database.open` :

- `meta` : les informations de service, sous forme de couples clé / valeur. Deux de ces clés sont nommées par le code : `game_version`, la version du jeu sous laquelle la copie locale a été enregistrée (constante `META_GAME_VERSION`), et `last_checked_at`, l'instant du dernier contrôle de version (constante `META_LAST_CHECKED_AT`).
- `items` : les objets eux-mêmes, une ligne par objet, chaque ligne portant sa catégorie, son identifiant Ankama et la fiche complète de l'objet.
- `idx_items_kind` : l'index posé sur la colonne des catégories de la table `items`, qui accélère les lectures par catégorie.

Cette page ne cite volontairement ni la taille du fichier ni son chemin complet sur votre poste : ces deux valeurs changent d'une installation à l'autre et ne décrivent pas le produit.

## Les catégories stockées

Chaque ligne de la table `items` porte une catégorie, écrite dans sa colonne `kind`. Cette colonne n'accepte pas n'importe quelle valeur : le produit en connaît sept, énumérées une à une par la constante `ITEM_KINDS`, et ce sont exactement celles que la synchronisation enregistre.

Les sept catégories stockées sont :

- `equipment` : les équipements — armes, armures, coiffes, capes, anneaux, ceintures, bottes, amulettes, boucliers et familiers.
- `resources` : les ressources, notamment celles qui entrent dans les recettes.
- `consumables` : les consommables.
- `quest` : les objets de quête.
- `cosmetics` : les objets cosmétiques.
- `mounts` : les montures.
- `sets` : les panoplies.

Aucune autre catégorie n'est enregistrée : cette liste est celle du produit, et cette page ne cite que ce que le code écrit réellement en base.

## La fenêtre de re-check de 24 heures

L'outil ne redemande pas la version du jeu à chaque lancement. Il note l'instant de son dernier contrôle dans la clé `last_checked_at` de la table `meta`, puis laisse passer une fenêtre avant de vérifier de nouveau : cette fenêtre est la constante `CHECK_INTERVAL_SECONDS`, déclarée dans `dofus_stuff/sync.py` par l'expression `24 * 60 * 60`.

Tant que la fenêtre n'est pas écoulée, le chargement du catalogue s'arrête là : aucune requête réseau n'est émise, et c'est la seule situation où une commande en ligne ne contacte pas l'API.

Quand la fenêtre est écoulée — et seulement dans ce cas — l'outil compare la version du jeu distante à la version locale. Si elles sont identiques, il se contente de noter le nouvel instant du contrôle ; si elles diffèrent, ou si la base locale est vide, il récupère tout le catalogue à nouveau.

L'option `--force-sync` court-circuite cette fenêtre : elle demande la vérification sans attendre le lendemain. L'option est décrite avec les autres dans [la page CLI](cli.md).

## Source de vérité

- `dofus_stuff/database.py` : nom du fichier de la base (`DB_NAME`), dossier par défaut (`DEFAULT_DATA_DIR`), clés de la table `meta`, catégories stockées (`ITEM_KINDS`) et schéma créé à l'ouverture.
- `dofus_stuff/sync.py` : fenêtre de re-check (`CHECK_INTERVAL_SECONDS`) et décision de resynchroniser ou non.
- `dofus_stuff/api.py` : sources réellement téléchargées, une par catégorie stockée (`SYNC_SOURCES`).

[Retour au sommaire](sommaire.md)
