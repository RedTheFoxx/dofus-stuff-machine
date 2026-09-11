# Phase 5 — Journal de discussion (mode `--auto`)

**Date :** 2026-09-11
**Mode :** `--auto` — le porteur du projet a choisi « Run discuss-phase first » puis « Research first ».
En mode `--auto`, chaque question retient **l'option recommandée**, sans invite interactive. Les
sélections sont consignées ci-dessous pour audit.

## Décisions prises par le porteur du projet avant la discussion

| Question | Réponse retenue |
|----------|-----------------|
| Aucun `CONTEXT.md` pour la phase 5 — continuer ou capturer les décisions d'abord ? | **Run discuss-phase first** |
| Rechercher avant de planifier la phase 5 ? | **Research first (Recommended)** |

Cadrage transmis par le porteur, repris tel quel dans `05-CONTEXT.md` : `docs/sommaire.md` gagne
l'entrée « Base locale » **à cette phase seulement** ; les renvois se font **par lien seulement quand
la cible existe** (leçon D-44) ; les commandes destructrices sont signalées **sur la même ligne** et
restent **hors de tout parcours** ; la phase porte en plus le contrôle de complétude des renvois de
`README.md`.

## Zones grises analysées et sélections `[auto]`

Les zones grises de cette phase ont été dérivées des 5 critères de succès du ROADMAP, de
`BASE-01`→`BASE-03`, des décisions héritées (D-01…D-67) et des règles du run. Aucune zone déjà
tranchée par une phase antérieure n'a été rouverte.

```
[auto] Périmètre de la page — Q: "Que doit posséder `docs/base-locale.md` ?" → Selected: "Une seule source : fichier, catégories, fenêtre 24 h, deux défauts hors-ligne, champs d'état" (recommended default) → D-68
[auto] Gabarit — Q: "Quel gabarit de page appliquer ?" → Selected: "Gabarit D-01 hérité sans exception (H1 = libellé d'index, Source de vérité, retour au sommaire, CRLF/UTF-8 sans BOM)" (recommended default) → D-69
[auto] Index — Q: "Quand `docs/sommaire.md` gagne-t-il l'entrée Base locale ?" → Selected: "À cette phase, une seule ligne ; liste épinglée des 8 pages en phase 6" (recommended default) → D-70
[auto] Défauts hors-ligne — Q: "Comment énoncer les deux défauts hors-ligne ?" → Selected: "Séparément, chacun nommé par sa surface : web hors-ligne par défaut ; CLI en ligne par défaut, donc `--offline` requis" (recommended default) → D-71
[auto] Drapeaux — Q: "D'où viennent les orthographes des drapeaux et leurs textes d'aide ?" → Selected: "Lus dans le code au moment de la rédaction, jamais écrits de mémoire" (recommended default) → D-72
[auto] Fenêtre 24 h — Q: "Comment documenter la fenêtre de re-check ?" → Selected: "Depuis `dofus_stuff/sync.py` (`CHECK_INTERVAL_SECONDS`), constante nommée, aucune valeur volatile" (recommended default) → D-73
[auto] Fichier et catégories — Q: "D'où viennent le nom du fichier et les catégories stockées ?" → Selected: "Du code (`DB_NAME`, schéma) ; aucune catégorie que le code ne stocke pas" (recommended default) → D-74
[auto] Champs d'état — Q: "Comment citer les champs de l'état de la base ?" → Selected: "Par leurs noms, produits par le code (constante publique ou rendu), sans aucune valeur volatile" (recommended default) → D-75
[auto] Champs non ancrables — Q: "Que faire d'un champ qu'aucun contrôle ne peut ancrer ?" → Selected: "Ne pas le citer" (recommended default) → D-76
[auto] `db status` — Q: "Comment traiter la création du fichier par `db status` ?" → Selected: "Le décrire tel quel et le prouver hors `.data/` (répertoire temporaire)" (recommended default) → D-77
[auto] `db sync --offline` — Q: "Comment traiter le refus ?" → Selected: "Citer le message réel du code, jamais une paraphrase" (recommended default) → D-78
[auto] Synchro web hors-ligne — Q: "Comment traiter l'écran web qui contacte l'API même hors-ligne ?" → Selected: "Le dire explicitement comme le seul endroit où le hors-ligne ne s'applique pas" (recommended default) → D-79
[auto] Commandes destructrices — Q: "Comment présenter `db clear` et `PURGE OUI` ?" → Selected: "Signalées destructrices sur la même ligne, hors de tout parcours" (recommended default) → D-80
[auto] Intégrité de `.data/` — Q: "Comment prouver qu'aucun contrôle n'écrit sous `.data/` ?" → Selected: "Répertoire temporaire uniquement + empreinte de la base mesurée avant/après la suite entière ; aucune commande destructrice, aucune synchro, aucun réseau" (recommended default) → D-81
[auto] Contrôles d'ancrage — Q: "Où vivent les contrôles et que réutilisent-ils ?" → Selected: "Module dédié `tests/test_docs_base_locale.py`, fixtures partagées réutilisées (D-12)" (recommended default) → D-82
[auto] Constats — Q: "Que doit citer un échec ?" → Selected: "Page + valeur attendue + fichier de code producteur (D-13)" (recommended default) → D-83
[auto] Morsures — Q: "Comment jouer les morsures ?" → Selected: "Sur copie verte en répertoire temporaire avant mutation ; sorties réellement obtenues" (recommended default) → D-84
[auto] Limites — Q: "Le module revendique-t-il une exhaustivité ?" → Selected: "Non : il déclare ses limites de couverture et de précision" (recommended default) → D-85
[auto] Renvois — Q: "Comment renvoyer vers les pages voisines ?" → Selected: "Par lien seulement là où la cible existe ; aucun lien mort" (recommended default) → D-86
[auto] Complétude README — Q: "Traiter le contrôle de complétude demandé par le porteur (`T6`) ?" → Selected: "Prendre le critère à la lettre (les renvois de `README.md` résolvent) ; le libellé `T6` n'ayant aucune définition dans les artefacts, ne pas l'étendre" (recommended default) → D-87
[auto] Code produit — Q: "Modifie-t-on `dofus_stuff/**` ?" → Selected: "Non — le code est la référence" (recommended default) → D-88
[auto] Base et réseau — Q: "La phase touche-t-elle la base ou le réseau ?" → Selected: "Aucune resynchronisation Dofusdude, hors-ligne d'abord, aucun `db clear`/drop/suppression" (recommended default) → D-89
[auto] Conventions — Q: "Quelles conventions appliquer ?" → Selected: "Celles des phases 1 à 4, telles quelles (D-01…D-67)" (recommended default) → D-90
[auto] Git et dépendances — Q: "Comment livrer ?" → Selected: "Commits locaux par chemin explicite, aucune publication, aucune dépendance ajoutée" (recommended default) → D-91
```

## Traçabilité des todos

Aucun todo en attente ne correspond au périmètre de la phase 5 (la correspondance par phase n'a remonté
aucun résultat) : pas de todo replié, pas de todo écarté.

## Zones laissées à l'appréciation de Claude

Consignées sous « Claude's Discretion » dans `05-CONTEXT.md` : ordre des sections, formulation de
l'introduction, nombre et forme des contrôles, regroupement ou non des deux défauts hors-ligne dans une
même section, termes exacts de l'avertissement destructeur.

Passage unique : aucune passe supplémentaire n'a été relancée après l'écriture de `05-CONTEXT.md`.
