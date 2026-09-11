# Wizard avancé

Cette page décrit le parcours avancé de l'interface web, écran par écran, tel que l'outil le rend. Tous les titres, libellés, formats et touches cités ici sont lus sur le rendu réel : ils sont recopiés tels que le produit les affiche, jamais de mémoire. La surface des commandes n'est pas recopiée ici : elle appartient à [la page CLI](cli.md), et le wizard avancé n'existe que dans l'interface web, il n'a aucune commande en ligne de commande.

## Les 9 étapes du wizard

Le wizard avancé s'affiche un écran à la fois. Les neuf écrans se suivent toujours dans cet ordre, et c'est l'ordre que le code parcourt quand une entrée vide fait passer à la suite :

1. `SLOTS ET FILTRES` (`slots`) : les emplacements d'équipement à optimiser et les filtres de type.
2. `OPTIONS SOLVEUR` (`options`) : les réglages du calcul, du niveau au budget de temps.
3. `CARACTERISTIQUES` (`caracs`) : les caractéristiques principales, une ligne par caractéristique.
4. `PA / PM / PO` (`papmpo`) : les objectifs de PA, de PM et de portée, avec leur part d'exo.
5. `RESISTANCES` (`resistances`) : les résistances, en pourcentage et en valeur fixe.
6. `DOMMAGES` (`damages`) : les dommages, leurs pourcentages et les dommages d'armes ou de sorts.
7. `DIVERS` (`misc`) : les autres caractéristiques, de l'initiative au pod.
8. `ITEMS INTERDITS / FORCES` (`items`) : les objets à exclure et les objets à imposer.
9. `RECAPITULATIF` (`recap`) : le résumé des réglages et les commandes de fin.

Chaque écran porte le titre de son étape dans sa ligne d'en-tête, avec son mot-clé entre accents graves. Les écrans de statistiques sont paginés automatiquement quand leur corps dépasse la hauteur de l'écran.

## Source de vérité

- `dofus_stuff/web/optimize_wizard.py` : liste ordonnée des étapes (`WIZARD_STEPS`), titres rendus (`STEP_TITLES`) et corps de chaque écran.
- `dofus_stuff/web/routes.py` : route `/optimize/wizard/<etape>`, ligne d'en-tête et barre de touches.
- `dofus_stuff/model/solver_spec.py` : emplacements et filtres de type adossés au modèle.
- `dofus_stuff/web/screens.py` : mise en page de l'écran et pagination du corps.
- `dofus_stuff/web/templates/screen.html` : gabarit HTML réellement rendu.

[Retour au sommaire](sommaire.md)
