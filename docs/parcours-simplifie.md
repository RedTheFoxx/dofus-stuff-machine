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
