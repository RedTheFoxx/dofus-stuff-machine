# Wizard avancé

Cette page décrit le parcours avancé de l'interface web, écran par écran, tel que l'outil le rend. Tous les titres, libellés, formats et touches cités ici sont lus sur le rendu réel : ils sont recopiés tels que le produit les affiche, jamais de mémoire. La surface des commandes n'est pas recopiée ici : elle appartient à [la page CLI](cli.md), et le wizard avancé n'existe que dans l'interface web, il n'a aucune commande en ligne de commande.

## Arriver au wizard

Le wizard avancé n'est pas la première page de l'optimisation : il vient après un parcours de trois questions. Le chemin réel est celui-ci, et il est lisible dans les écrans que l'outil rend :

1. Au menu principal, la ligne `4. OPTIMISATION DE STUFF` ouvre l'optimisation. C'est cette entrée, et pas une autre, qui mène au parcours.
2. La première page demande la classe (`1/3 - Quelle est votre classe ?`), la deuxième les éléments (`2/3 - Quels éléments privilégier ?`), la troisième le niveau (`3/3 - Quel est votre niveau ? (1 à 200)`).
3. La ligne `AVANCE : personnaliser les réglages`, proposée sur les trois pages, ouvre le wizard. La casse est ignorée : `avance` fait la même chose.

L'écran sur lequel on arrive est le **récapitulatif**, pas les emplacements. Le récapitulatif résume les réglages recommandés pour la classe, les éléments et le niveau qui viennent d'être saisis ; c'est de là que les autres écrans se rejoignent.

Chaque écran du wizard porte son identifiant dans sa ligne d'en-tête, dans l'ordre des étapes :

| Étape | Identifiant de l'écran |
| --- | --- |
| 1. `slots` | `OPT-W1` |
| 2. `options` | `OPT-W2` |
| 3. `caracs` | `OPT-W3` |
| 4. `papmpo` | `OPT-W4` |
| 5. `resistances` | `OPT-W5` |
| 6. `damages` | `OPT-W6` |
| 7. `misc` | `OPT-W7` |
| 8. `items` | `OPT-W8` |
| 9. `recap` | `OPT-W9` |

Le sous-écran d'édition, ouvert par un numéro d'option ou de ligne, porte l'identifiant `OPT-WED` : le même, quelle que soit la ligne éditée.

Adresser un écran qui n'existe pas ne rend aucune page : le message `ECRAN WIZARD INCONNU` s'affiche et l'outil ramène au menu principal.

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

## Les 11 options du solveur

L'écran annonce `OPTIONS (N=EDIT) :` et rappelle `N=CHOISIR OPTION`. Chaque option porte son numéro et son libellé rendus :

| Numéro | Option |
| --- | --- |
| 1 | `NIVEAU` |
| 2 | `JET` |
| 3 | `DUREE (S)` |
| 4 | `SEED` |
| 5 | `TOP-K` |
| 6 | `CP-SAT` |
| 7 | `STOP SI CIBLES` |
| 8 | `AUTO POINTS` |
| 9 | `ALLOW POWER` |
| 10 | `ALLOW DOMMAGES` |
| 11 | `ALLOW DOM CRIT` |

Les numéros se comportent de deux façons, et l'écran ne prévient pas de la différence :

- `1` à `5` ouvrent un sous-écran d'édition : son en-tête porte `OPT-WED`, son libellé de saisie est `VAL` et son champ est limité à `maxlength=20`. Enregistrer une valeur y rend `VALEUR ENREGISTREE`.
- `6` à `11` basculent l'option immédiatement, sans sous-écran, et rendent `OPTION MISE A JOUR`.

Les refus de cet écran sont ceux du rendu : un numéro hors liste rend `OPTION INVALIDE`, et une saisie qui n'est pas un numéro rend `SAISIR UN NUMERO D'OPTION`.

Les valeurs acceptées par le sous-écran d'édition sont celles du code : `JET` n'accepte que `min`, `average` ou `max`, la casse étant ignorée, et rend `JET = MIN|AVERAGE|MAX` sinon ; `SEED` accepte une entrée vide, `-`, `none` ou `aucun`, qui rendent `(aucun)` ; `TOP-K` a un plancher de `1`. Le niveau, la durée et les autres options sont lus comme des nombres, sans borne ni signe imposés par l'écran : cette page ne les présente donc pas comme des entrées garanties et ne recommande aucune valeur négative.

## Les quatre nombres d'une ligne

Sur les écrans de statistiques, chaque ligne porte quatre nombres : `B` pour la base, `P` pour les points répartis — ou `E` pour la part d'exo —, `C` pour la cible et `W` pour le poids. Selon l'écran, la ligne prend donc l'une de ces deux formes, et l'écran d'édition les nomme telles quelles :

| Écran | Forme affichée |
| --- | --- |
| `CARACTERISTIQUES` | `FORMAT : BASE POINTS CIBLE POIDS` |
| `PA / PM / PO` | `FORMAT : BASE EXO CIBLE POIDS` |

Les écrans `RESISTANCES`, `DOMMAGES` et `DIVERS` emploient la même forme que `CARACTERISTIQUES` : seuls les objectifs de `PA / PM / PO` portent une part d'exo. Les deux formes ne sont jamais fusionnées : la première demande base, points, cible et poids, la seconde base, exo, cible et poids.

L'édition d'une ligne se fait en deux temps. Sur l'écran de liste, qui affiche `N=EDIT`, on tape le **numéro** de la ligne : une saisie qui n'est pas un numéro rend `SAISIR LE NUMERO DE LA LIGNE`, et un numéro hors liste rend `NUMERO INVALIDE`. Le sous-écran d'édition affiche alors `EDITION : <NOM DE LA LIGNE>`, la valeur actuelle et la forme attendue, puis demande la nouvelle valeur.

La nouvelle valeur doit porter **exactement quatre nombres**, séparés par des espaces ou par des virgules. Toute autre quantité rend le message de la forme de l'écran : c'est le message de refus de cette édition, et il est identique à la forme affichée juste au-dessus. Une valeur qui n'est pas un nombre fait remonter le message du convertisseur tel quel. Une entrée vide n'est pas un refus : elle annule l'édition et revient à la liste. Une saisie valide rend `CARAC ENREGISTREE`.

## Interdire, forcer, retirer un objet

Cet écran tient deux listes : les objets **interdits**, que le calcul ne doit pas utiliser, et les objets **forcés**, qu'il doit utiliser. Il annonce sa syntaxe avant les deux listes :

| Saisie | Ce que l'écran annonce |
| --- | --- |
| `+ID` | `AJOUTER INTERDIT` |
| `-ID` | `AJOUTER FORCE` |
| `!ID` | `RETIRER (BAN OU FORCE)` |
| `CLEAR` | `VIDER LISTES` |

Ce que la saisie fait réellement :

- `+ID` ajoute l'objet à la liste des interdits. `+ID` n'est donc pas une saisie refusée : c'est le verbe « ajouter un interdit ».
- `-ID` ajoute l'objet à la liste des forcés.
- `!ID` retire l'objet des deux listes.
- `CLEAR` vide les deux listes, et sa variante en minuscules `clear` fait la même chose.
- Les espaces autour de la saisie sont acceptés.
- Un objet ajouté à une liste est retiré de l'autre : il ne peut pas être interdit et forcé en même temps.
- Au-delà de 8 entrées, l'affichage d'une liste est tronqué et se termine par une ligne d'ellipse.
- Quand elle est vide, une liste rend l'état vide `(aucun)`. C'est le cas des deux listes sur un écran neuf, et après `CLEAR`.

Le **seul** refus de cet écran est le message rendu quand la saisie n'est ni `CLEAR` ni `clear`, ni un préfixe `+`, `-` ou `!` suivi de chiffres : `SYNTAXE : +ID | -ID | !ID | CLEAR`.

Un identifiant **sans préfixe**, par exemple `12345`, tombe dans ce cas et est donc refusé, alors que `+12345` ne l'est pas.

## Exemple guidé

Objectif : un premier stuff **Intelligence** au niveau `123`. L'exemple ne fait que ce que les écrans acceptent, et il passe par le chemin d'arrivée réel décrit plus haut.

1. Menu principal : `4` puis Entrée ouvre `4. OPTIMISATION DE STUFF`.
2. Répondez aux trois questions : la classe, puis `2/3 - Quels éléments privilégier ?` avec `terre`, puis `3/3 - Quel est votre niveau ? (1 à 200)` avec `123`.
3. Sur cette troisième page, `AVANCE` (`AVANCE : personnaliser les réglages`) ouvre le wizard : vous êtes sur le `RECAPITULATIF`.
4. Réglez le niveau du calcul. Depuis le récapitulatif, le chiffre `2` ramène à l'écran `OPTIONS SOLVEUR`, puis `1` ouvre l'édition de `NIVEAU` et la valeur `123` l'enregistre (`VALEUR ENREGISTREE`). La ligne rendue devient `1. NIVEAU = 123`.
5. Donnez un poids à l'Intelligence. Depuis le récapitulatif, le chiffre `3` ramène à `CARACTERISTIQUES`, puis `4` ouvre la ligne `Intelligence` et la valeur `300 0 0 1` l'enregistre (`CARAC ENREGISTREE`). La ligne rendue devient `4. Intelligence B=300 P=0 C=0 W=1`.

   Le `300` est une décision du lecteur, pas une contrainte de l'outil : le wizard ne connaît pas les parchemins et ne les édite pas. Ce `300` peut être la base du personnage (200) augmentée de 100 parchemins ; le poids `1` demande simplement de maximiser l'Intelligence.
6. Variante, une cible de PA. Depuis le récapitulatif, le chiffre `4` ramène à `PA / PM / PO`, puis `1` ouvre la ligne `PA` et la valeur `6 0 11 5` l'enregistre. La ligne rendue devient `1. PA B=6 E=0 C=11 W=5` : base 6 PA, exo 0, cible 11, poids 5. C'est la forme de cet écran (`FORMAT : BASE EXO CIBLE POIDS`), qui n'est pas celle des caractéristiques (`FORMAT : BASE POINTS CIBLE POIDS`) : quatre nombres dans les deux cas, mais pas les mêmes.
7. Revenez au récapitulatif. Depuis l'écran où vous êtes, `F8` (`Suivant`) passe à l'écran suivant, et l'entrée vide fait la même chose. Quand le récapitulatif affiche vos valeurs, tapez `GO` (`GO = LANCER`) : le calcul se lance et son résultat remplace l'écran.

Aucune commande destructrice n'appartient à ce parcours : l'exemple ne vide aucune liste, ne supprime rien et ne touche pas à la base locale. Ce que le calcul produit, et comment le lire, est décrit dans [le parcours simplifié](parcours-simplifie.md).

## Source de vérité

- `dofus_stuff/web/optimize_wizard.py` : liste ordonnée des étapes (`WIZARD_STEPS`), titres rendus (`STEP_TITLES`), libellés d'emplacements (`SLOT_GROUP_LABELS`), libellés de filtres (`TYPE_FILTER_LABELS`), lignes des onze options, des listes de statistiques et des items, et formats d'édition.
- `dofus_stuff/web/routes.py` : route `/optimize/wizard/<etape>`, ligne d'en-tête, lignes de statut, sous-écrans d'édition et barre de touches.
- `dofus_stuff/model/solver_spec.py` : ordre des emplacements (`SLOT_GROUPS`) et touches des filtres de type (`TYPE_FILTER_KEYS`).
- `dofus_stuff/web/screens.py` : mise en page de l'écran et pagination du corps.
- `dofus_stuff/web/templates/screen.html` : gabarit HTML réellement rendu, dont la ligne de statut.

[Retour au sommaire](sommaire.md)
