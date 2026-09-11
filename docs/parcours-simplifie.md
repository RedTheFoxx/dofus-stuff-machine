# Parcours simplifié

Cette page suit le parcours simplifié de l'interface web, question par question : la classe, les éléments, puis le niveau. Pour chacune, elle recopie l'écran tel qu'il s'affiche et dit ce que la saisie accepte.

Toutes les affirmations de cette page viennent du rendu réel de la vue web. La surface des commandes n'est pas recopiée ici : elle appartient à [la page CLI](cli.md). Les écrans du wizard avancé et le fonctionnement de la base locale seront décrits dans les pages qui leur seront consacrées. Le parcours en ligne de commande, lui, ne pose pas ces trois questions : la classe et les éléments n'existent que dans le parcours guidé de l'interface web.

## Question 1/3 : la classe

L'écran s'ouvre sur le menu des dix-neuf classes, chacune accompagnée de son numéro. Le titre du programme affiché en haut d'écran est `** RECOMMANDATION DE STUFF **`.

```text
VOTRE STUFF EN 3 CHOIX

1/3 - Quelle est votre classe ?

 1. Cra              2. Ecaflip          3. Eliotrope
 4. Eniripsa         5. Enutrof          6. Feca
 7. Forgelance       8. Huppermage       9. Iop
10. Osamodas        11. Ouginak         12. Pandawa
13. Roublard        14. Sacrieur        15. Sadida
16. Sram            17. Steamer         18. Xelor
19. Zobal

AVANCE : personnaliser les réglages
```

Le champ de saisie porte le libellé `CHOIX`, et la barre de touches affiche `ESC=Retour`.

### Entrées acceptées

| Saisie | Ce que l'outil fait |
|--------|---------------------|
| `Cra` | passe à l'étape 2 |
| `crâ` | passe à l'étape 2 : accents et casse sont ignorés |
| `1` | passe à l'étape 2 : le numéro 1 désigne Cra |
| `19` | passe à l'étape 2 : le numéro 19 désigne Zobal |
| `019` | passe à l'étape 2 : le zéro de tête est admis |
| ` 3 ` | passe à l'étape 2 : les espaces autour sont retirés |

Le nom de la classe est comparé après suppression des accents et de la casse : `Crâ` et `cra` désignent la même classe. Un numéro de 1 à 19 est accepté, avec ou sans zéro de tête, et les espaces placés autour de la saisie sont retirés avant la comparaison. Le début du nom ne suffit pas : la comparaison est une égalité, pas un préfixe, et `eliotrop` est refusé pour cette raison.

### Erreurs et refus

| Saisie refusée | Message affiché |
|----------------|-----------------|
| `eliotrop` | Saisissez le nom ou le numéro de votre classe. |
| `0` | Saisissez le nom ou le numéro de votre classe. |
| `20` | Saisissez le nom ou le numéro de votre classe. |

Un refus n'est pas une erreur de page : l'écran de la question reste affiché à l'identique et le message apparaît dans la ligne de statut, en bas de l'écran, juste avant `ENTREE=SUIVANT`. Le champ de saisie est vidé, la valeur refusée n'est pas conservée.

## Question 2/3 : les éléments

Une fois la classe retenue, l'écran rappelle la classe choisie puis affiche le menu des quatre éléments.

```text
VOTRE STUFF EN 3 CHOIX

Classe : Cra

2/3 - Quels éléments privilégier ?

1. Terre    2. Feu    3. Eau    4. Air

Un ou plusieurs : feu / terre air / 1 3 / multi
Le multi valorise aussi votre élément le plus faible.

AVANCE : personnaliser les réglages
```

### Entrées acceptées

| Saisie | Ce que l'outil fait |
|--------|---------------------|
| `terre` | passe à l'étape 3 avec le seul élément terre |
| `terre air` | passe à l'étape 3 avec terre et air |
| `terre,air` | idem : la virgule sépare deux éléments |
| `terre+air` | idem : le signe plus sépare deux éléments |
| `1 3` | passe à l'étape 3 avec terre et eau : les chiffres désignent les éléments |
| `multi` | passe à l'étape 3 avec les quatre éléments |

Plusieurs éléments se séparent par un espace, une virgule ou un signe plus, et ces séparateurs se mélangent librement. Les chiffres `1`, `2`, `3` et `4` désignent respectivement Terre, Feu, Eau et Air. Le mot `multi` vaut à lui seul les quatre éléments. Un élément cité deux fois n'est compté qu'une fois.

### Erreurs et refus

| Saisie refusée | Message affiché |
|----------------|-----------------|
| `multi terre` | Exemple : feu, terre air, ou multi. |
| `arbre` | Exemple : feu, terre air, ou multi. |
| `5` | Exemple : feu, terre air, ou multi. |

`multi` n'est accepté que seul : mêlé à un autre élément, la saisie est refusée. Un mot qui ne désigne aucun élément, ou un chiffre hors de la plage des quatre éléments, est refusé de la même façon. Le refus redessine l'écran courant et le message s'affiche dans la ligne de statut, juste avant `ENTREE=SUIVANT`.

## Question 3/3 : le niveau

Le dernier écran rappelle la classe et les éléments retenus, puis demande un niveau entre 1 et 200.

```text
VOTRE STUFF EN 3 CHOIX

Cra - terre

3/3 - Quel est votre niveau ? (1 à 200)

ENTREE lance la recherche de votre équipement.
PA/PM et vitalité sont pris en compte selon le niveau.
Points répartis automatiquement, sans exo ni parchemins.
Jets moyens ; préférences de classe ajustables après calcul.

AVANCE : personnaliser les réglages
```

### Entrées acceptées

| Saisie | Ce que l'outil fait |
|--------|---------------------|
| `150` | lance la recherche puis affiche le résultat |
| `050` | idem : le zéro de tête est admis, le niveau retenu est 50 |
| `200` | idem : 200 est le niveau le plus élevé accepté |
| `AVANCE` | ouvre les réglages détaillés, au lieu de lancer la recherche |

### Erreurs et refus

| Saisie refusée | Message affiché |
|----------------|-----------------|
| `201` | Saisissez un niveau entre 1 et 200. |
| `0` | Saisissez un niveau entre 1 et 200. |
| `50.0` | Saisissez un niveau entre 1 et 200. |

Le niveau doit être un nombre entier compris entre 1 et 200 : une valeur décimale, un nombre négatif ou un nombre hors bornes est refusé. Le message s'affiche dans la ligne de statut, juste avant `ENTREE=CALCULER`.

### Passer aux réglages détaillés

La ligne `AVANCE : personnaliser les réglages` accepte les mêmes orthographes que les autres saisies du parcours : `AVANCE` fonctionne quelle que soit la casse et avec des espaces autour. Elle est rendue sur les trois étapes, y compris celle du niveau, et elle ouvre les réglages détaillés du stuff.

## Source de vérité

- `dofus_stuff/web/routes.py` : écrans et libellés des trois questions.
- `dofus_stuff/optimize/recommend.py` : liste des classes, paliers PA/PM et heuristiques de classe.
- `dofus_stuff/optimize/api.py` : lignes du résultat et emplacements affichés.
- `dofus_stuff/model/solver_spec.py` : capital de points par niveau.
- `dofus_stuff/optimize/score.py` : « indice de recherche ».
- `dofus_stuff/optimize/candidates.py` : sélection du catalogue.
- `dofus_stuff/web/static/js/terminal.js` : sauvegardes du navigateur.
- `dofus_stuff/web/dofusbook_export.py` : export Dofusbook.

[Retour au sommaire](sommaire.md)
