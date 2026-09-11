<!--
Copie figee d'un etat OBSOLETE de GUIDE_WIZARD.md, conservee comme piece de test (D-59b).
Ce n'est PAS de la documentation : ce fichier vit sous tests/ et n'est cite par aucune page de
docs/. Son seul role est de rendre le rouge du critere 5 relancable : le detecteur de renvois
obsoletes de tests/test_docs_wizard.py doit continuer de le signaler apres que l'aiguillage
livre a ete corrige (plan 04-03, vague 4). Extrait partiel et annonce comme tel : seules les
formes couvertes par le wizard avance sont reproduites, copiees verbatim depuis GUIDE_WIZARD.md.
-->

# Extraits obsoletes du guide (copie figee, piece de test)

## Aiguillage du menu principal (verbatim, GUIDE_WIZARD.md:35-45)

Tapez `3` puis **Entrée** pour ouvrir l’optimisation.

```
1. RECHERCHE D'OBJETS
2. LISTE DES EQUIPEMENTS
3. OPTIMISATION DE STUFF

4. SYSTEME
```

Vous arrivez **directement** dans le wizard (premier écran : slots et filtres).

## Occurrence secondaire du mauvais numero (verbatim, GUIDE_WIZARD.md:50-51)

L’option **4. SYSTEME** regroupe le reste : détail d’un équipement par ID, version locale,
self-test et gestion de la base.

## Filtres de types : la touche des armes a distance (verbatim, GUIDE_WIZARD.md:153-157)

| Saisie | Effet |
|--------|--------|
| `F1` | Autoriser / interdire les **familiers** |
| `F2` | Montiliers |
| `F3`… | Dragodindes, muldos, volkornes, armes distance/mêlée, dofus, trophées, prysmaradite |

Exemple : pour **interdire les armes à distance**, tapez `F7` (selon la liste affichée) jusqu’à voir `OFF`.
