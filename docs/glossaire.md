# Glossaire

Cette page recense le vocabulaire employé par l'outil et par cette documentation : un mot par ligne, ce qu'il recouvre, le fichier ou la page qui l'emploie, et la page qui le détaille quand elle existe déjà.

La règle de cette page est celle d'une seule source par énoncé : quand une page de cette documentation définit déjà un terme, l'entrée du glossaire **renvoie** vers elle au lieu de la redéfinir. Le glossaire ne définit donc que ce qu'aucune autre page ne définit, et il ne recopie jamais une définition déjà écrite ailleurs.

Les lignes qui portent un tiret dans la dernière colonne sont de ce fait les plus courtes : elles disent ce que le mot recouvre, et rien de plus, parce qu'aucune autre page ne le dit. Toutes les autres renvoient à la page qui l'explique en détail, pour que le même énoncé ne vive qu'à un seul endroit.

## Les termes

Chaque ligne porte quatre colonnes : le **terme**, sa **définition** — ou le renvoi vers la page qui le définit —, le **fichier ou la page qui l'emploie**, et la **page qui le définit déjà**. Cette dernière vaut un tiret quand le glossaire est le premier à définir le terme. Les termes sont rangés dans l'ordre de leur forme normalisée : accents, casse et espaces ne comptent pas pour ce classement.

| Terme | Définition | Employé par | Déjà défini dans |
|-------|------------|-------------|------------------|
| `base locale` | la copie locale des données Dofus, gardée dans un fichier SQLite de votre poste ; la page liée décrit ce qu'elle contient et sa fenêtre de re-check | `dofus_stuff/cli.py` | [Base locale](base-locale.md) |
| `bouclier` | l'emplacement d'équipement du même nom, omis du résultat quand il est vide ; la page liée le place dans la liste des emplacements | `dofus_stuff/model/slots.py` | [Parcours simplifié](parcours-simplifie.md) |
| `catégorie` | une des familles d'objets que la base locale range dans sa colonne de type ; la page liée les énumère une à une | `dofus_stuff/cli.py` | [Base locale](base-locale.md) |
| `cible` | la valeur de statistique à atteindre, saisie sous la forme `STAT=valeur` ; la page liée décrit les champs qui la portent | `dofus_stuff/cli.py` | [Wizard avancé](wizard-avance.md) |
| `exo` | la part de statistique exotique — PA, PM, portée — comptée hors des points de niveau ; la page liée décrit le cas du calcul sans exo | `dofus_stuff/model/solver_spec.py` | [Parcours simplifié](parcours-simplifie.md) |
| `familier` | l'emplacement d'équipement du familier ou de la monture, omis du résultat quand il est vide ; la page liée le place dans la liste | `dofus_stuff/model/slots.py` | [Parcours simplifié](parcours-simplifie.md) |
| `heuristique` | une recherche approchée du solveur, dont la borne est affichée entre crochets dans l'indice de recherche ; la page liée nomme les modes | `dofus_stuff/optimize/score.py` | [Parcours simplifié](parcours-simplifie.md) |
| `ID Ankama` | le numéro d'objet du jeu, qui identifie un objet dans la base locale ; la page liée décrit les options qui le prennent en argument | `dofus_stuff/cli.py` | [CLI](cli.md) |
| `index` | la table page → sujet du sommaire, qui donne pour chaque page le sujet qu'elle traite | `docs/sommaire.md` | - |
| `jet` | la valeur d'une ligne d'effet d'un objet, réglée sur le minimum, la moyenne ou le maximum ; la page liée décrit ce réglage | `dofus_stuff/cli.py` | [Wizard avancé](wizard-avance.md) |
| `ligne de statut` | la dernière ligne d'un écran du terminal web, celle où le produit écrit ses refus et ses invites ; la page liée en décrit le contenu | `docs/parcours-simplifie.md` | [Parcours simplifié](parcours-simplifie.md) |
| `mode hors-ligne` | le réglage qui empêche le contact de l'API : actif par défaut sur l'interface web, sur demande pour la ligne de commande ; la page liée décrit les deux surfaces | `docs/base-locale.md` | [Base locale](base-locale.md) |
| `palier` | le seuil auquel le coût d'un point de caractéristique ou la cible de PA et de PM change ; la page liée donne les paliers et leurs niveaux | `dofus_stuff/model/solver_spec.py` | [Parcours simplifié](parcours-simplifie.md) |
| `panoplie` | un ensemble d'objets du jeu dont les bonus s'activent par nombre de pièces ; la page liée nomme la catégorie qui la stocke | `dofus_stuff/catalog.py` | [Base locale](base-locale.md) |
| `parcours conseillé` | l'ordre de lecture proposé par le sommaire, du premier pas au dernier ; la section du sommaire porte ce nom | `docs/sommaire.md` | - |
| `poids` | le coefficient qui pèse une statistique dans le score, saisi sous la forme `STAT=valeur` ; la page liée décrit les champs qui le portent | `dofus_stuff/cli.py` | [Wizard avancé](wizard-avance.md) |
| `prysmaradite` | l'emplacement d'équipement de la prysmaradite, qui n'est pas exportée vers Dofusbook ; la page liée explique cette exception | `dofus_stuff/cli.py` | [Parcours simplifié](parcours-simplifie.md) |
| `sauvegarde locale` | un stuff gardé dans le navigateur, listé par l'écran des sauvegardes ; la page liée décrit cette liste et sa limite | `dofus_stuff/web/static/js/terminal.js` | [Parcours simplifié](parcours-simplifie.md) |
| `score` | la valeur que la recherche maximise pour comparer deux stuffs, affichée en fin de résultat ; la page liée rappelle que c'est une mesure interne | `dofus_stuff/optimize/score.py` | [Parcours simplifié](parcours-simplifie.md) |
| `slot` | l'emplacement d'équipement d'un stuff, tel que le modèle de calcul le nomme ; la page liée décrit l'écran qui les bascule | `dofus_stuff/web/optimize_wizard.py` | [Wizard avancé](wizard-avance.md) |
| `solveur` | le moteur qui cherche la meilleure sélection d'objets sous un budget de temps ; la page liée décrit le réglage de ce budget | `dofus_stuff/optimize/cpsat.py` | [Wizard avancé](wizard-avance.md) |
| `sommaire` | le point d'entrée unique de cette documentation, qui porte le parcours conseillé et l'index | `docs/sommaire.md` | - |
| `source de vérité` | le bloc par lequel une page nomme le code dont elle procède ; c'est un titre de section du gabarit des pages, pas un terme du produit | `docs/base-locale.md` | - |
| `stuff` | l'ensemble d'équipement optimisé pour un niveau, tel que l'outil le compose | `dofus_stuff/cli.py` | - |
| `synchronisation` | la mise à jour de la base locale depuis l'API Dofusdude, refusée en mode hors-ligne ; la page liée décrit son déclenchement | `dofus_stuff/cli.py` | [Base locale](base-locale.md) |
| `trophée` | un emplacement d'équipement du jeu, que l'écran décrit par la page liée bascule comme les Dofus ; la ligne de commande peut l'ignorer | `dofus_stuff/model/slots.py` | [Wizard avancé](wizard-avance.md) |
| `wizard` | le parcours multi-écrans qui configure le calcul, étape par étape ; la page liée décrit ses étapes et leurs touches | `dofus_stuff/web/optimize_wizard.py` | [Wizard avancé](wizard-avance.md) |

Aucune de ces lignes n'est une définition recopiée : celles qui portent un renvoi disent en une phrase ce que le mot recouvre et renvoient à la page qui le détaille ; celles qui portent un tiret sont les seules que le glossaire définit, parce qu'aucune autre page ne le fait.

La colonne « Employé par » est vérifiable : elle nomme un fichier ou une page où le mot est réellement employé. Elle ne prétend pas désigner l'unique endroit où le mot apparaît, seulement un endroit où il est employé, pour que vous puissiez le retrouver dans le produit ou dans la documentation.

Cette page ne juge pas la rédaction : elle tient les mots, leur ordre, leur employeur et le renvoi vers la page qui définit déjà. La clarté des phrases relève de la lecture, pas d'un contrôle.

## Source de vérité

- `docs/sommaire.md` : l'index des pages et le parcours conseillé, dont les libellés sont repris ici.
- `dofus_stuff/cli.py` : l'aide du parseur de la ligne de commande, où les mots du produit sont employés.
- `dofus_stuff/model/solver_spec.py` : les groupes d'emplacements et les statistiques du modèle de calcul.
- `dofus_stuff/web/optimize_wizard.py` : les libellés des écrans du wizard avancé.

[Retour au sommaire](sommaire.md)
