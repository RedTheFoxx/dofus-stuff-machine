# Guide du Wizard d’optimisation de stuff

Ce guide explique comment utiliser le **wizard** de stuff-machine pour générer automatiquement un équipement Dofus, même si vous n’avez jamais utilisé l’outil.

---

## 1. À quoi sert le wizard ?

Le wizard vous aide à **décrire le personnage et les objectifs** (niveau, caractéristiques, contraintes), puis lance un **solveur** qui propose une combinaison d’objets (cape, coiffe, anneaux, dofus, etc.) adaptée.

Vous ne choisissez pas les objets un par un au départ : vous indiquez *ce que vous voulez obtenir* (par exemple beaucoup d’Intelligence, 11 PA, etc.), et l’outil cherche un stuff cohérent dans la base locale Dofus.

---

## 2. Démarrer l’interface

1. Ouvrez un terminal dans le projet.
2. Lancez l’interface web :

```bash
python -m dofus_stuff.web
```

3. Ouvrez le navigateur à l’adresse indiquée (en général `http://127.0.0.1:5000`).
4. Vous voyez un **écran noir type terminal** (pas un site web classique). C’est normal.

### Menu principal

Tapez `7` puis **Entrée** pour ouvrir l’optimisation.

```
7. OPTIMISATION DE STUFF
8. STUFFS SAUVEGARDES
```

Vous arrivez **directement** dans le wizard (premier écran : slots et filtres).

L’option **8** rouvre les stuffs que vous avez choisis de sauvegarder dans ce navigateur (voir section 7).

---

## 3. Comment fonctionne l’interface (très important)

L’écran est pensé comme un ancien terminal :

| Élément | Rôle |
|--------|------|
| Zone centrale | Texte d’aide et listes numérotées |
| Ligne jaune `[ … ]` | **Seul champ de saisie** : vous tapez une commande puis Entrée |
| Ligne du bas | Raccourcis clavier (`F7`, `F8`, `F12`…) |
| Message de statut | Infos / erreurs (souvent en rouge si erreur) |

### Touches à connaître

| Touche | Effet |
|--------|--------|
| **Entrée** | Valide la saisie. Sur la plupart des écrans, **Entrée à vide** = passer à l’écran suivant |
| **F7** | Écran / page **précédent** |
| **F8** | Écran / page **suivant** |
| **F12** | Retour au **menu principal** |
| **PageUp / PageDown** | Même idée que F7/F8 pour feuilleter |

Si un écran est trop long pour tenir d’un coup, le statut affiche `PAGE X/Y` : utilisez **F8** pour voir la suite.

> Astuce : cliquez une fois dans la zone jaune si le curseur n’est pas actif, puis tapez au clavier.

---

## 4. Parcours du wizard (vue d’ensemble)

Le wizard comporte **9 écrans** dans cet ordre :

1. **Slots et filtres** — quels emplacements remplir, quels types d’objets autoriser  
2. **Options solveur** — niveau, durée de calcul, réglages avancés  
3. **Caractéristiques** — Vitalité, Force, Intelligence, etc.  
4. **PA / PM / PO** — points d’action, de mouvement, portée (+ exo)  
5. **Résistances**  
6. **Dommages**  
7. **Divers** — initiative, prospection, tacle, etc.  
8. **Items interdits / forcés**  
9. **Récapitulatif** — vérification puis lancement avec `GO`

Vous n’êtes **pas obligé** de tout remplir. Pour un premier essai, lisez la section « Premier stuff en 5 minutes » plus bas.

---

## 5. Les quatre nombres d’une caractéristique (B / P / C / W)

Sur les écrans de stats, chaque ligne s’édite avec **4 valeurs** :

```text
BASE  POINTS  CIBLE  POIDS
```

Exemple pour l’Intelligence :

```text
200  0  1200  2
```

| Champ | Signification | Exemple |
|-------|----------------|---------|
| **BASE (B)** | Ce que le perso a **déjà hors stuff** (capital converti + bases naturelles, selon votre habitude) | `200` |
| **POINTS (P)** | Points de caractéristiques **encore à répartir** (ou déjà saisis ici) | `0` |
| **CIBLE (C)** | Valeur **totale** que vous visez avec le stuff inclus | `1200` |
| **POIDS (W)** | **Priorité** pour le solveur. Plus c’est haut, plus la carac compte | `2` |

### Règles simples

- Si **POIDS = 0** et **CIBLE = 0**, la carac est **ignorée** par l’objectif.
- Si **POIDS > 0** sans cible, le solveur **maximise** cette carac.
- Si **CIBLE > 0**, le solveur cherche surtout à **atteindre** cette valeur (puis peut continuer selon les poids).
- Pour **PA / PM / PO**, le format est un peu différent : `BASE  EXO  CIBLE  POIDS`  
  - **EXO** = bonus d’exo déjà présents sur le perso (souvent `0`).

### Comment éditer une ligne

1. Tapez le **numéro** de la ligne (ex. `4`) puis Entrée.  
2. Un sous-écran d’édition s’ouvre.  
3. Tapez les 4 nombres séparés par des espaces, puis Entrée.  
4. Vous revenez à la liste.

Entrée **vide** dans l’édition = annuler.

---

## 6. Détail de chaque écran

### Écran 1 — Slots et filtres

**Slots** = emplacements d’équipement (amulette, anneaux, coiffe, dofus…).

- Tapez un **numéro** (ex. `7`) pour activer / désactiver un slot (`ON` / `OFF`).
- Au moins **un** slot doit rester actif.

**Filtres de types** (préfixe `F`) :

| Saisie | Effet |
|--------|--------|
| `F1` | Autoriser / interdire les **familiers** |
| `F2` | Montiliers |
| `F3`… | Dragodindes, muldos, volkornes, armes distance/mêlée, dofus, trophées, prysmaradite |

Exemple : pour **interdire les armes à distance**, tapez `F7` (selon la liste affichée) jusqu’à voir `OFF`.

Puis **Entrée vide** ou **F8** pour continuer.

### Écran 2 — Options solveur

Tapez le **numéro** d’une option :

| N° | Option | Débutant : que mettre ? |
|----|--------|-------------------------|
| 1 | **Niveau** | Le niveau de votre perso (ex. `200`) |
| 2 | **Jet** | `average` (recommandé) ; `min` / `max` = jets d’objets pessimistes / optimistes |
| 3 | **Durée (s)** | Temps max de calcul, ex. `5` ou `10` |
| 4 | **Seed** | Laisser vide sauf pour reproduire un résultat |
| 5 | **Top-K** | Nombre de candidats par slot (défaut `30` ; plus grand = plus lent) |
| 6 | **CP-SAT** | Laisser `ON` (meilleur solveur) |
| 7 | **Stop si cibles** | `ON` = s’arrêter dès que les cibles sont atteintes |
| 8 | **Auto points** | `ON` = répartir automatiquement le capital de caracs restant |
| 9 | **Allow power** | Compter la **Puissance** comme carac élémentaire |
| 10 | **Allow dommages** | Compter les **Dommages** génériques pour les dom. élémentaires |
| 11 | **Allow dom crit** | Idem avec **Dommages critiques** |

Pour les options 6 à 11, le numéro **bascule** immédiatement ON/OFF.  
Pour 1 à 5, un écran demande la nouvelle valeur.

### Écrans 3 à 7 — Stats (caracs, PA/PM/PO, résistances, dommages, divers)

Même principe partout :

1. Repérez la ligne intéressante.  
2. Tapez son numéro.  
3. Saisissez `B P C W` (ou `B E C W` pour PA/PM/PO).

Vous pouvez **sauter** des écrans entiers avec Entrée vide / F8 si vous n’avez rien à y configurer.

### Écran 8 — Items interdits / forcés

Utilisez les **IDs Ankama** des objets (visibles dans la recherche / détail d’item de l’outil).

| Commande | Effet |
|----------|--------|
| `+12345` | **Interdit** l’objet `#12345` |
| `-12345` | **Force** l’objet `#12345` dans le stuff |
| `!12345` | Retire l’objet des deux listes |
| `CLEAR` | Vide interdits et forcés |

Un objet ne peut pas être à la fois interdit et forcé.

### Écran 9 — Récapitulatif

Vérifiez le résumé (niveau, poids, cibles, bans…).

| Saisie | Effet |
|--------|--------|
| `GO` (ou Entrée vide) | **Lance** le calcul |
| `RESET` | Remet le wizard à zéro |
| `1` … `8` | Retour rapide à l’écran correspondant |

Le calcul peut prendre quelques secondes. Ensuite s’affiche le **résultat**.

---

## 7. Lire le résultat

L’écran résultat montre notamment :

- le **score** et un **% de compatibilité** (qualité relative de la solution) ;
- la liste des **équipements** avec leur **ID Ankama** (`#…`) ;
- un extrait des **stats totales** ;
- les **panoplies** actives le cas échéant.

### Actions utiles

- **F8** : page suivante (souvent nécessaire pour voir tous les dofus / la fin des stats).  
- Tapez un **ID** (ex. `7252`) puis Entrée pour ouvrir le **détail** de l’objet.  
- Tapez **`SAVE`** (ou `SAVE mon label`) pour **garder ce stuff** dans le navigateur — ce n’est pas obligatoire.  
- **F12** : retour au menu (sans sauvegarder si vous n’avez pas tapé `SAVE`).

### Stuffs sauvegardés (menu 8)

Les sauvegardes restent **dans ce navigateur uniquement** (localStorage), jusqu’à 20 entrées.

Sur l’écran **STUFFS SAUVEGARDES** :

| Commande | Effet |
|----------|--------|
| `N` | Ouvre la sauvegarde numéro N |
| `BACK` | Depuis le détail, revient à la liste |
| `DEL N` | Supprime la sauvegarde N |
| `PURGE OUI` | Efface **toutes** les sauvegardes locales |
| **F12** | Retour au menu |

---

## 8. Premier stuff en 5 minutes (exemple guidé)

Objectif : perso **niveau 123**, build **Intelligence**, base 200 + parchemins 100 déjà inclus dans la base.

1. Menu → `7`  
2. **Slots** : laissez les défauts (Entrée vide / F8).  
3. **Options** :  
   - `1` puis `123` (niveau)  
   - F8 pour continuer  
4. **Caractéristiques** :  
   - trouvez **Intelligence** (souvent ligne `4`)  
   - saisie : `300 0 0 1`  
     - `300` = 200 base + 100 parchemins  
     - poids `1` = maximiser l’INT  
5. Passez les écrans suivants jusqu’au **récap** (Entrée vide / F8).  
6. Tapez `GO`.

Vous obtenez un premier stuff « max Intelligence » au niveau 123.

### Variante avec cible PA

Sur l’écran **PA / PM / PO**, éditez **PA** :

```text
6 0 11 5
```

Interprétation : base 6 PA, exo 0, **cible 11**, poids élevé → le solveur privilégie fortement les 11 PA.

---

## 9. Conseils pour de bons résultats

1. **Donnez au moins un poids** (`W > 0`) à une carac principale, sinon l’outil retombe sur un défaut Intelligence.  
2. Des **cibles irréalistes** (ex. 20 PA au niveau 50) donnent des stuffs incomplets ou étranges.  
3. Augmentez la **durée** (option 3) si le résultat semble faible.  
4. Utilisez **Stop si cibles** quand vous avez des seuils clairs (11 PA, 4 PM…) et voulez un résultat plus rapide.  
5. **Interdisez** les objets que vous n’avez pas / ne voulez pas (`+ID`).  
6. **Forcez** une pièce signature (`-ID`) si elle doit absolument être là.  
7. Feuilletez toujours le résultat avec **F8** : la première page ne montre souvent qu’une partie du stuff.

---

## 10. Problèmes fréquents

| Problème | Que faire |
|----------|-----------|
| Rien ne se passe au clavier | Cliquer dans le champ jaune `[ ]` |
| F7 / F8 ne marchent pas | Recharger la page (Ctrl+F5), vérifier que le focus n’est pas ailleurs |
| Je ne vois que 4 dofus | Appuyer sur **F8** (page suivante du résultat) |
| Erreur rouge après saisie | Relire le format (souvent 4 nombres, ou `+ID`) |
| Stuff vide / bizarre | Vérifier niveau, au moins un poids > 0, slots ON |
| Calcul long | Baisser Top-K ou durée ; activer « Stop si cibles » |

---

## 11. Lexique express

| Terme | Sens |
|-------|------|
| **Stuff** | Ensemble d’équipements du personnage |
| **Slot** | Emplacement (coiffe, cape, dofus…) |
| **Solveur** | Programme qui cherche la meilleure combinaison |
| **Poids** | Priorité d’une carac dans la recherche |
| **Cible** | Valeur totale souhaitée |
| **ID Ankama** | Numéro unique d’un objet dans Dofus |
| **Jet** | Tirage min / moyen / max des effets d’un objet |
| **Exo** | Bonus artificiel (souvent PA/PM/PO) |

---

## 12. Aller plus loin

- La **CLI** permet les mêmes idées en ligne de commande (`python fetcher.py --offline optimize …`) : utile pour automatiser.  
- Les données viennent de la **base locale** (menu 6 / sync) : gardez-la à jour pour des objets récents.

Si vous débutez vraiment : faites d’abord l’exemple de la section 8, regardez le résultat avec F8, ouvrez un item par son ID, puis recommencez en ajoutant une cible PA. C’est le meilleur moyen de comprendre le wizard.
