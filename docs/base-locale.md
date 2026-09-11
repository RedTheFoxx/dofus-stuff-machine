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

## Le mode hors-ligne du web

L'interface web **démarre hors-ligne** : le mode hors-ligne y est le défaut, et l'option `--offline` y est donc active sans rien préciser. C'est `--no-offline` — ou son équivalent `--online` — qui autorise le contact de l'API au démarrage. Le parseur de l'interface le dit lui-même, dans l'aide qu'il rend :

> `--offline, --no-offline` — Ne pas contacter l'API au démarrage (défaut : oui)

Ce que le mode hors-ligne change au démarrage de l'interface est radical : la vérification de version **n'a pas lieu du tout**. Le chargement du catalogue est ouvert avec `skip_sync` (`dofus_stuff/web/__init__.py`) et `Catalog.load(skip_sync=True)` n'appelle pas `ensure_up_to_date` : la fenêtre de re-check n'est pas consultée, l'API n'est pas interrogée, et une base locale vide n'est pas une erreur — l'interface s'ouvre simplement sur un catalogue vide, ce qui est l'état normal d'un premier lancement.

Le mode hors-ligne règle donc le **démarrage** de l'interface web. Il ne dit rien des gestes que vous demandez explicitement depuis un écran.

## Le mode hors-ligne de la ligne de commande

La ligne de commande, elle, **est en ligne par défaut** : `--offline` n'y est pas actif et il y est donc **requis** pour ne pas contacter l'API. Son aide le rappelle :

> `--offline` — Ne pas contacter l'API (échoue si la base locale est vide)

Ce que le mode hors-ligne change sur cette surface est différent de l'interface web : la fenêtre de re-check **est** consultée au chargement du catalogue. Tant qu'elle n'est pas écoulée, aucune requête n'est émise et l'outil travaille sur sa copie locale ; une fois la fenêtre écoulée, la synchronisation est refusée faute de réseau et l'outil continue avec la base locale telle qu'elle est. Une base locale **vide**, en revanche, n'est pas un état utilisable : la commande s'arrête alors sur une erreur, parce qu'elle n'a rien à lire et n'a pas le droit de remplir la base.

Les deux surfaces ne partagent donc pas le même défaut : le web démarre hors-ligne, la ligne de commande démarre en ligne. Une phrase qui parlerait d'« un outil hors-ligne par défaut » sans nommer la surface serait fausse sur l'une des deux.

## L'état de la base en ligne de commande

`python fetcher.py --offline db status` affiche l'état de la base locale, libellé par libellé. Les noms de champs décrits ici sont ceux que cette commande écrit réellement ; les valeurs, elles, sont produites à l'exécution et ne sont pas recopiées dans cette page.

| Libellé écrit par la commande | Ce qu'il porte |
|-------------------------------|----------------|
| `Fichier :` | le chemin complet du fichier de la base sur votre poste |
| `Version jeu :` | la version du jeu enregistrée dans la base |
| `Dernier check :` | depuis combien de temps la version du jeu n'a pas été vérifiée |
| `Entrées :` | le nombre d'objets présents dans la base |
| `Par catégorie :` | suit le nombre d'objets de chaque catégorie stockée |

Quand la base locale est vide, deux champs prennent une autre forme : la commande écrit alors `Version jeu : (aucune)` et `Dernier check : (aucun)`.

La ligne `Par catégorie :` n'apparaît que si la base contient au moins un objet : sur une base vide, elle n'est pas écrite du tout, et aucune ligne de catégorie ne la suit. Quand elle est écrite, chaque catégorie occupe la ligne suivante, sous la forme `  - <catégorie> : <nombre>`.

Les libellés de cette surface sont accentués et en minuscules, tels que la ligne de commande les écrit.

## L'état de la base dans l'interface web

Le même état est accessible depuis l'interface web, sur l'écran d'état de la base (`/db/status`). Les libellés y sont écrits dans une autre forme : tout en majuscules et sans accents. Ce n'est pas une faute de frappe, c'est la forme que cette surface rend.

| Libellé rendu par l'écran | Ce qu'il porte |
|---------------------------|----------------|
| `FICHIER :` | le chemin complet du fichier de la base |
| `VERSION JEU :` | la version du jeu enregistrée dans la base |
| `DERNIER CHECK :` | depuis combien de temps la version du jeu n'a pas été vérifiée |
| `ENTREES :` | le nombre d'objets présents dans la base |
| `PAR CATEGORIE :` | suit le nombre d'objets de chaque catégorie stockée |

Quand la base locale est vide, l'écran rend `VERSION JEU : (aucune)` et `DERNIER CHECK : (AUCUN)`, en majuscules comme le reste de cette surface.

La ligne `PAR CATEGORIE :` n'apparaît elle aussi que si la base contient au moins un objet : sur une base vide, elle est absente.

Le même état ne s'écrit donc pas de la même façon sur les deux surfaces : `Entrées :` est accentué en ligne de commande, `ENTREES :` ne l'est pas dans l'interface web. Cette page ne lisse pas cet écart, parce que la différence est celle du code.

## Le premier contact crée la base

Consulter l'état de la base **crée la base si elle n'existe pas** : le dossier `.data/` d'abord, le fichier `dofus.sqlite3` ensuite. C'est vrai des deux surfaces, et c'est le code qui le fait, pas un geste d'installation : la commande hors-ligne `python fetcher.py --offline db status` et l'écran d'état de l'interface web, au chemin `/db/status`, traversent tous deux `Database.open`, qui crée le dossier parent puis ouvre — et donc crée — le fichier.

La conséquence pratique est qu'un état affiché ne prouve pas que la base est peuplée. Une base fraîchement créée porte ses deux tables et son index, mais aucune fiche : côté ligne de commande, l'état écrit alors `Version jeu : (aucune)`, `Dernier check : (aucun)` et `Entrées : 0`, sans aucune ligne de catégorie ; côté web, l'écran rend `VERSION JEU : (aucune)`, `DERNIER CHECK : (AUCUN)` et `ENTREES : 0`, sans `PAR CATEGORIE :`.

Autrement dit : voir une base locale exister ne dit rien de son contenu. Pour la remplir, il faut une synchronisation — et la surface des commandes est décrite par [la page CLI](cli.md).

## La synchronisation refuse le mode hors-ligne

La synchronisation a besoin du réseau : comparer la version du jeu et récupérer le catalogue supposent l'un et l'autre l'API. La commande de synchronisation refuse donc le mode hors-ligne, et elle le dit avec ce message, écrit dans `dofus_stuff/cli.py` :

> `Erreur : --offline incompatible avec db sync`

La commande sort alors avec un code de retour non nul : rien n'est synchronisé, et la base locale reste telle qu'elle était. Le piège est l'ordre des arguments — l'option globale s'écrit **avant** la sous-commande, et la forme fautive la place après : le refus vise la forme `--offline db sync`. Le détail des sous-commandes et de leurs options appartient à [la page CLI](cli.md).

## L'écran de synchronisation du web contacte l'API

C'est le seul endroit où le mode hors-ligne ne s'applique pas. L'écran de synchronisation, au chemin `/db/sync`, annonce d'abord ce qu'il va faire, avant de demander une confirmation :

> CETTE OPERATION CONTACTE L'API DOFUSDUDE

La suite de l'écran prévient que l'opération peut prendre plusieurs minutes, puis attend la confirmation. Le fait à retenir est que confirmer lance réellement la synchronisation, **même hors-ligne** : le mode hors-ligne règle le démarrage de l'interface — ne pas contacter l'API au démarrage — et non cette demande explicite. Une interface ouverte hors-ligne peut donc contacter l'API dès que vous confirmez cet écran.

## Les commandes destructrices

Deux commandes du produit détruisent des données. Elles sont décrites ici pour être **reconnues**, jamais pour être lancées, et chacune est signalée sur sa propre ligne :

`db clear` (et son second nom, l'alias de cache `cache clear`) est destructrice : elle vide entièrement la base locale en exécutant les deux instructions de suppression que le code porte, `DELETE FROM items` puis `DELETE FROM meta` — le fichier n'est pas supprimé du disque, mais les deux tables sont vidées et les entrées locales disparaissent ; le détail de la sous-commande appartient à [la page CLI](cli.md).

PURGE OUI est destructrice : elle supprime les sauvegardes du navigateur pour cette interface.

Ces deux commandes ne sont l'étape d'aucun parcours de cette page : aucune des deux n'est nécessaire pour lire, rechercher, optimiser ou sauvegarder un stuff, et elles sont décrites ici pour être reconnues au moment où on les croise, pas pour être suivies.

## Source de vérité

- `dofus_stuff/database.py` : nom du fichier de la base (`DB_NAME`), dossier par défaut (`DEFAULT_DATA_DIR`), clés de la table `meta`, catégories stockées (`ITEM_KINDS`) et schéma créé à l'ouverture.
- `dofus_stuff/sync.py` : fenêtre de re-check (`CHECK_INTERVAL_SECONDS`) et décision de resynchroniser ou non.
- `dofus_stuff/api.py` : sources réellement téléchargées, une par catégorie stockée (`SYNC_SOURCES`).

[Retour au sommaire](sommaire.md)
