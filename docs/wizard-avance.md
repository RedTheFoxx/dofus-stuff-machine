# Wizard avancé

Cette page décrit le parcours avancé de l'interface web, écran par écran, tel que l'outil le rend. Tous les titres, libellés, formats et touches cités ici sont lus sur le rendu réel : ils sont recopiés tels que le produit les affiche, jamais de mémoire. La surface des commandes n'est pas recopiée ici : elle appartient à [la page CLI](cli.md), et le wizard avancé n'existe que dans l'interface web, il n'a aucune commande en ligne de commande.

## Les 9 étapes du wizard

Le wizard avancé s'affiche un écran à la fois. Les neuf écrans se suivent toujours dans cet ordre, et c'est l'ordre que le code parcourt quand une entrée vide fait passer à la suite :

1. `SLOTS ET FILTRES` (`slots`) : les emplacements d'équipement à optimiser et les filtres de type. Chaque emplacement se bascule par son numéro, chaque filtre par sa touche `F<n>`.
2. `OPTIONS SOLVEUR` (`options`) : les réglages du calcul, du niveau au budget de temps. Chaque option s'édite en tapant son numéro.
3. `CARACTERISTIQUES` (`caracs`) : les caractéristiques principales, une ligne par caractéristique. Une ligne s'édite en tapant son numéro.
4. `PA / PM / PO` (`papmpo`) : les objectifs de PA, de PM et de portée, avec leur part d'exo. Une ligne s'édite de la même façon.
5. `RESISTANCES` (`resistances`) : les résistances, en pourcentage et en valeur fixe. Même édition, par numéro de ligne.
6. `DOMMAGES` (`damages`) : les dommages, leurs pourcentages et les dommages d'armes ou de sorts. Même édition, par numéro de ligne.
7. `DIVERS` (`misc`) : les autres caractéristiques, de l'initiative au pod. Même édition, par numéro de ligne.
8. `ITEMS INTERDITS / FORCES` (`items`) : les objets à exclure et les objets à imposer, saisis avec la syntaxe `+ID`, `-ID`, `!ID` ou `CLEAR`.
9. `RECAPITULATIF` (`recap`) : le résumé des réglages, avec `GO` pour lancer le calcul, `RESET` pour repartir de zéro, `SAVES` pour les stuffs sauvegardés et `1` à `8` pour revenir à un écran.

Chaque écran porte le titre de son étape dans sa ligne d'en-tête, avec son mot-clé entre accents graves. Les écrans de statistiques affichent `N=EDIT` et sont paginés automatiquement quand leur corps dépasse la hauteur de l'écran.

## Slots et filtres

Cet écran règle ce que le calcul a le droit d'utiliser. Il annonce deux listes — `SLOTS (N=TOGGLE) :` pour les emplacements, `FILTRES TYPES (F+N) :` pour les filtres de type — et rappelle la commande `N=TOGGLE SLOT  FN=TOGGLE FILTRE`. Une entrée vide n'est pas un refus : elle passe à l'étape suivante.

### Les 11 emplacements

| Numéro | Emplacement |
| --- | --- |
| 1 | `AMULETTE` |
| 2 | `ANNEAUX` |
| 3 | `CEINTURE` |
| 4 | `BOTTES` |
| 5 | `COIFFE` |
| 6 | `CAPE` |
| 7 | `ARME` |
| 8 | `BOUCLIER` |
| 9 | `DOFUS/TROPHEES` |
| 10 | `FAMILIER/MONTURE` |
| 11 | `PRYSMARADITE` |

### Les 10 filtres de type

| Touche | Filtre |
| --- | --- |
| `F1` | `FAMILIER` |
| `F2` | `MONTILIER` |
| `F3` | `DRAGODINDE` |
| `F4` | `MULDO` |
| `F5` | `VOLKORNE` |
| `F6` | `ARMES DISTANCE` |
| `F7` | `ARMES MELEE` |
| `F8` | `DOFUS` |
| `F9` | `TROPHEE` |
| `F10` | `PRYSMARADITE` |

La touche `F6` bascule les armes à distance (`ARMES DISTANCE`) et la touche `F7` bascule les armes de mêlée (`ARMES MELEE`). `F7` n'est donc pas la touche des armes à distance, contrairement à ce qu'annonçait l'ancien guide.

### Ce que la saisie accepte

Chaque emplacement affiché porte son numéro et son état : `ON` quand il est actif, `OFF` quand il ne l'est pas. Taper un numéro de `1` à `11` bascule l'emplacement correspondant.

Chaque filtre affiché porte sa touche `F<n>`, avec `n` de `1` à `10` : taper `F` suivi du numéro bascule le filtre. La casse est ignorée, donc `f7` a le même effet que `F7`.

### Erreurs et refus

- Une saisie qui n'est ni un numéro de `1` à `11` ni une touche `F<n>` rend `SAISIE INVALIDE`.
- Une touche au-delà de `F10`, par exemple `F11`, rend `FILTRE INVALIDE`.
- Désactiver le dernier emplacement encore actif rend `AU MOINS UN SLOT REQUIS` : il en faut toujours un.
- Une entrée vide n'est pas un refus : elle passe à l'étape suivante.

## Source de vérité

- `dofus_stuff/web/optimize_wizard.py` : liste ordonnée des étapes (`WIZARD_STEPS`), titres rendus (`STEP_TITLES`), libellés d'emplacements (`SLOT_GROUP_LABELS`), libellés de filtres (`TYPE_FILTER_LABELS`) et corps de chaque écran.
- `dofus_stuff/web/routes.py` : route `/optimize/wizard/<etape>`, ligne d'en-tête, lignes de statut et barre de touches.
- `dofus_stuff/model/solver_spec.py` : ordre des emplacements (`SLOT_GROUPS`) et touches des filtres de type (`TYPE_FILTER_KEYS`).
- `dofus_stuff/web/screens.py` : mise en page de l'écran et pagination du corps.
- `dofus_stuff/web/templates/screen.html` : gabarit HTML réellement rendu.

[Retour au sommaire](sommaire.md)
