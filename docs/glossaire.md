# Glossaire

Cette page recense le vocabulaire employé par l'outil et par cette documentation : un mot par ligne, ce qu'il recouvre, le fichier ou la page qui l'emploie, et la page qui le détaille quand elle existe déjà.

La règle de cette page est celle d'une seule source par énoncé : quand une page de cette documentation définit déjà un terme, l'entrée du glossaire **renvoie** vers elle au lieu de la redéfinir. Le glossaire ne définit donc que ce qu'aucune autre page ne définit, et il ne recopie jamais une définition déjà écrite ailleurs.

## Les termes

Chaque ligne porte quatre colonnes : le **terme**, sa **définition** — ou le renvoi vers la page qui le définit —, le **fichier ou la page qui l'emploie**, et la **page qui le définit déjà**. Cette dernière vaut un tiret quand le glossaire est le premier à définir le terme. Les termes sont rangés dans l'ordre de leur forme normalisée : accents, casse et espaces ne comptent pas pour ce classement.

| Terme | Définition | Employé par | Déjà défini dans |
|-------|------------|-------------|------------------|
| `index` | la table page → sujet du sommaire, qui donne pour chaque page le sujet qu'elle traite | `docs/sommaire.md` | - |
| `parcours conseillé` | l'ordre de lecture proposé par le sommaire, du premier pas au dernier | `docs/sommaire.md` | - |
| `sommaire` | le point d'entrée unique de cette documentation, qui porte le parcours conseillé et l'index | `docs/sommaire.md` | - |
| `source de vérité` | le bloc par lequel une page nomme le code dont elle procède ; c'est un titre de section du gabarit des pages, pas un terme du produit | `docs/base-locale.md` | - |
| `stuff` | l'ensemble d'équipement optimisé pour un niveau, tel que l'outil le compose | `dofus_stuff/cli.py` | - |

Aucune de ces cinq lignes n'est une définition recopiée : chacune dit ce que le mot recouvre, et elle renvoie ailleurs dès qu'une page le détaille déjà.

## Source de vérité

- `docs/sommaire.md` : l'index des pages et le parcours conseillé, dont les libellés sont repris ici.
- `dofus_stuff/cli.py` : l'aide du parseur de la ligne de commande, où les mots du produit sont employés.
- `dofus_stuff/model/solver_spec.py` : les groupes d'emplacements et les statistiques du modèle de calcul.
- `dofus_stuff/web/optimize_wizard.py` : les libellés des écrans du wizard avancé.

[Retour au sommaire](sommaire.md)
