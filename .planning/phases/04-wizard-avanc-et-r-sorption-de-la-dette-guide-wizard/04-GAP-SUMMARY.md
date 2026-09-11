---
phase: 04-wizard-avanc-et-r-sorption-de-la-dette-guide-wizard
plan: gap-cr01-cr02
subsystem: documentation
tags: [cloture-de-gap, cr-01, cr-02, guide-wizard, parcours-simplifie, arborescence-rendue, ancrage-au-rendu, morsure-par-mutation, pytest, documentation-francaise]

# Dependency graph
requires:
  - phase: 04-wizard-avanc-et-r-sorption-de-la-dette-guide-wizard
    plan: review
    provides: "04-REVIEW.md : les deux constats critiques (CR-01 arborescence de l'aiguillage, CR-02 phrase des touches de parcours-simplifie.md) et les cinq avertissements que ce gap evalue puis laisse hors perimetre"
  - phase: 04-wizard-avanc-et-r-sorption-de-la-dette-guide-wizard
    plan: 03
    provides: "GUIDE_WIZARD.md (aiguillage corrige) et tests/test_docs_wizard.py (detecteur pur `renvois_obsoletes`, lecteur d'attentes mesurees `_faits_du_rendu`) : le fichier et le harnais sur lesquels le controle d'egalite s'ajoute"
  - phase: 04-wizard-avanc-et-r-sorption-de-la-dette-guide-wizard
    plan: 04
    provides: "docs/wizard-avance.md : la table par etape des couples F7/F8/ESC des neuf ecrans, seule page que le rendu autorise a citer, et la reference qui rendait la phrase de CR-02 visiblement fausse"
provides:
  - "GUIDE_WIZARD.md : l'arborescence portant les libelles du corps rendu (`3. LISTE DES PANOPLIES`, `4. OPTIMISATION DE STUFF`, `5. SYSTEME` confirme), et non plus ceux du routage"
  - "tests/test_docs_wizard.py : `_constats_arborescence(texte, menus, normalize)` (egalite, apres normalisation, entre chaque ligne `N. LIBELLE` et le libelle que `GET /` rend pour ce numero), le motif de morsure `MOTIF_ARBORESCENCE`, et deux tests nouveaux — `test_arborescence_de_l_aiguillage_egale_le_menu_rendu` et `test_arborescence_abregee_signalee_par_le_controle` (morsure par mutation d'une copie en memoire du fichier livre)"
  - "docs/parcours-simplifie.md : la phrase des touches (~ligne 140) disant la verite **par etape** du wizard, extremites comprises (D-64 satisfaite)"
  - "tests/test_docs_parcours.py : `TOUCHES_RESULTAT` / `TOUCHES_WIZARD_INTERMEDIAIRES` (meme valeur que l'ancien `TOUCHES_WIZARD`, meme assertion negative), les deux extremites du wizard exigees au rendu (`EXTREMITE_WIZARD_SANS_PRECEDENT`, `EXTREMITE_WIZARD_SANS_SUIVANT`) et `_constats_touches_wizard(texte, normalize)` (la phrase de la page doit citer les libelles des ecrans intermediaires **et** ceux des deux extremites)"
affects: [verification-phase-4, wiz-03, d-64]

# Actuals (#2632) — mesures sur la meme echelle qu'un estimate le serait (chars/4 du diff realise).
# Aucun estimate n'etait attache a ce gap : les valeurs ci-dessous sont purement descriptives.
# AUCUN lissage : ni l'arrondi vers un chiffre qui plairait, ni l'exclusion du retravail.
# Perimetre du compte, nomme pour etre verifiable : les QUATRE fichiers livres. Ce resume lui-meme
# n'y est pas inclus (~31 400 octets, soit ≈ 7 850 tokens a la meme echelle) — le compter rendrait la
# valeur dependante de sa propre redaction, d'ou l'approximation assumee sur cette seconde ligne.
# Reproduire le compte des quatre fichiers : `git diff --unified=0 <base>..HEAD`, puis caracteres des
# lignes ajoutees moins caracteres des lignes retirees, divise par 4.
actuals:
  tokens: 3563     # chars/4 sur le diff realise des quatre fichiers livres (15 418 ajoutes, 1 164 retires)
  tokens_avec_resume: 11413   # ≈ 3 563 + 7 850 (ce resume, ~31 400 octets, meme echelle chars/4)
  tasks: 4
  commits: 4       # MESURE : git rev-list --count 7b2ebc2dbcd8fe93ce77f2c7af8ac1ca0d9692c2..HEAD
  plan_head_before: 7b2ebc2dbcd8fe93ce77f2c7af8ac1ca0d9692c2

# Tech tracking
tech-stack:
  added: []          # aucune dependance ajoutee (pyproject.toml inchange, aucun import nouveau)
  patterns:
    - "Controle d'egalite **complementaire** du detecteur, jamais substitut : le detecteur juge un jeton de menu par appartenance de mots significatifs (tolerance voulue de D-47, exigee par `test_renvois_legitimes_non_signales`), le controle ajoute juge par egalite apres la normalisation du depot (D-11). Les deux regles coexistent, aucune n'est touchee"
    - "Morsure mesurable sur un **texte**, jamais sur un chemin : `_constats_arborescence` et `_constats_touches_wizard` recoivent le texte a juger, ce qui rend la mutation possible sur une copie en memoire et rend le fichier du depot intouchable par un test"
    - "Verite **par etape** ancree au rendu : les deux extremites du wizard sont mesurees (`/optimize/wizard/slots`, `/optimize/wizard/recap`) et non deduites d'une regle generale, qui serait fausse"
    - "Garde portant sur la partie **apres l'ancre** d'une phrase : la page ecrit un paragraphe par ligne, donc une garde sur la ligne entiere aurait ete satisfaite par les libelles du resultat cites un peu plus haut dans la meme ligne"
    - "Motifs de morsure portes par des constantes (`MOTIF_ARBORESCENCE`, `MOTIF_TOUCHES_WIZARD`), jamais ecrits en clair dans la ligne d'assertion : pytest reproduit cette ligne dans sa sortie"

key-files:
  created:
    - .planning/phases/04-wizard-avanc-et-r-sorption-de-la-dette-guide-wizard/04-GAP-SUMMARY.md
  modified:
    - GUIDE_WIZARD.md
    - docs/parcours-simplifie.md
    - tests/test_docs_wizard.py
    - tests/test_docs_parcours.py

key-decisions:
  - "CR-01 : les etiquettes de l'arborescence sont lues au **corps rendu** (`routes.py`, fonction `menu`), jamais au routage (`menu_post`, lignes ~217-222, qui ne porte que des noms de vues et aucun libelle). La correction de numerotation de D-47 (`4`, non `3`) est conservee, son *intention* — « lu dans le code, jamais ecrit de memoire » — est enfin satisfaite par la source qui porte les libelles"
  - "CR-01 : la regle d'appartenance de mots du detecteur n'est **pas** resserree — elle est voulue, et la resserrer declarerait fautif le texte que D-47 prescrit. Le controle ajoute est une assertion separee, d'egalite, et sa morsure est prouvee par mutation"
  - "CR-01 : mutation appliquee a une **copie en memoire** derivee du fichier livre, jamais au fichier lui-meme ; la preuve est durable, puisqu'elle vit dans la suite et non dans une session"
  - "CR-02 : la phrase de `docs/parcours-simplifie.md` est **qualifiee par etape** (ecrans intermediaires / deux extremites), et non laissee telle quelle : le rendu mesure des neuf ecrans la contredit aux deux bouts, dont l'etape 1 rend `Page prec` et le recapitulatif `Page suiv`. D-64 prime sur la lecture stricte de D-63 (« aucun autre enonce n'est modifie ») des lors que la consigne du porteur est « la phrase doit rester vraie »"
  - "CR-02 : `TOUCHES_WIZARD` est **renomme** (`TOUCHES_WIZARD_INTERMEDIAIRES`) sans changer sa valeur ni l'assertion qui l'emploie — aucune assertion supprimee ni affaiblie — et deux extremites mesurees au rendu sont ajoutees, ce qui fait mordre l'ancre sur la barre du wizard et non plus seulement sur une lecture de la page"
  - "Perimetre : aucun avertissement de `04-REVIEW.md` n'est corrige. Deux d'entre eux portent sur `docs/wizard-avance.md`, hors des fichiers autorises par la consigne ; les trois autres (controle CRLF mesure sur un artefact git local, helpers recopies d'un module de test a l'autre, `IndexError` nu dans deux lecteurs) sont des travaux de solidite hors des deux constats critiques closes ici. Ils restent ouverts et nommes, aucun n'etant masque"
  - "Aucun fichier de `dofus_stuff/**` n'est modifie : le code reste le referentiel, la documentation s'y conforme (D-19/D-66)"

metrics:
  duration: "1 vague (4 commits de contenu, 1 commit de metadonnees)"
  completed: "2026-09-11"
  tasks: 4
  files: 4

status: complete
---

# Phase 04 — clôture de gap : les deux constats critiques de `04-REVIEW.md`

L'arborescence de l'aiguillage porte désormais les libellés du **corps rendu** par `GET /`
(`3. LISTE DES PANOPLIES`, `4. OPTIMISATION DE STUFF`), un contrôle d'**égalité** adossé au rendu et sa
**morsure par mutation** gardent cette conformité, et la phrase des touches de
`docs/parcours-simplifie.md` dit la vérité **par étape** du wizard, extrémités comprises — D-64 est
satisfaite, et les deux fichiers du jeu documentaire ne se contredisent plus sur la même rangée de
menu ni sur la même touche.

## Ce que ce gap ferme, et ce qu'il ne touche pas

Fermé : **CR-01** (l'arborescence de `GUIDE_WIZARD.md` n'était pas celle que le produit rend, sous une
phrase annonçant « l'arborescence réelle » — le critère WIZ-03 restait donc faux) et **CR-02** (la
phrase de `docs/parcours-simplifie.md` ~ligne 140 généralisait, et cette phase venait de publier le
document qui la contredit).

Non touché : `dofus_stuff/**` (le code est le référentiel, D-19), `tests/fixtures/guide-wizard-obsolete.md`
et sa morsure, le détecteur `renvois_obsoletes` et `test_aiguillage_sans_renvoi_obsolete`, les deux
liens D-63 (lignes 5 et 256 de la page du parcours, mesurés intacts), et les cinq avertissements de la
revue (nommés plus bas, aucun n'étant masqué). Aucune commande destructrice, aucune écriture sous
`.data/`, aucun accès réseau, `main()` jamais exécuté, `GO` jamais posté.

## CR-01 — l'arborescence de l'aiguillage

### La décision arbitrée, reprise telle quelle

D-47 exigeait l'arborescence « **lue dans le code**, jamais écrite de mémoire » et citait
`dofus_stuff/web/routes.py` (`menu_post`, lignes ~217-222). Ces lignes-là sont la **table de routage**
`{"1": "terminal.search", … "5": "terminal.system_menu"}` : elles donnent les **numéros**, et les
numéros sont justes, mais elles ne portent **aucun libellé**. Les étiquettes avaient donc été écrites
depuis la mauvaise source, et le contrôle du détecteur — appartenance de mots, tolérance voulue pour
les formes abrégées que D-47 prescrit — laissait passer `3. PANOPLIES` et `4. OPTIMISATION`.

Décision appliquée : **conservée** la correction de numérotation (`4`, non `3`), **remplacées** les
étiquettes par celles du **corps rendu**, lues à l'exécution (D-36 : le rendu est la référence).
Aucune re-discussion du choix, aucune modification du contrat du détecteur.

### Ce qui a été mesuré, puis écrit

Rendu de `GET /` mesuré au client de test Flask, en processus, hors ligne (`app` de `tests/conftest.py`,
base construite sous `tmp_path`), corps du menu ligne par ligne :

```text
[00] "1. RECHERCHE D'OBJETS                    …"
[01] '2. LISTE DES EQUIPEMENTS                 …'
[02] '3. LISTE DES PANOPLIES                   …'
[03] '                                         …'
[04] '4. OPTIMISATION DE STUFF                 …'
[05] '                                         …'
[06] '5. SYSTEME                               …'
```

Capturées par le motif de ligne de menu (`^\s*(\d)\.\s+(.+?)\s*$`), les attentes sont :

```text
1. "RECHERCHE D'OBJETS"      normalize="recherche d'objets"
2. 'LISTE DES EQUIPEMENTS'   normalize='liste des equipements'
3. 'LISTE DES PANOPLIES'     normalize='liste des panoplies'
4. 'OPTIMISATION DE STUFF'   normalize='optimisation de stuff'
5. 'SYSTEME'                 normalize='systeme'
```

`GUIDE_WIZARD.md` est donc passé de

```text
3. PANOPLIES

4. OPTIMISATION
5. SYSTEME
```

à

```text
3. LISTE DES PANOPLIES

4. OPTIMISATION DE STUFF
5. SYSTEME
```

Le reste du fichier est **inchangé** : `H1`, l'avis de déplacement, les deux liens de navigation, la
phrase « Tapez `4` puis **Entrée** pour ouvrir l'optimisation » (l'instruction correcte, celle que
D-47 existait pour resorber dans sa forme obsolète « `3` ») et les 18 lignes du signpost
(`LIGNES_MAX_AIGUILLAGE = 20`). `5. SYSTEME` a été **confirmé** par la mesure, non supposé. La ligne
blanche entre `3.` et `4.` est conservée telle quelle : le rendu réel en porte une au même endroit, et
la consigne demandait de ne pas toucher à la structure.

### Le contrôle ajouté

`_constats_arborescence(texte, menus, normalize)` : chaque ligne `N. LIBELLE` du texte jugé doit être,
**après la normalisation du dépôt (D-11)**, égale au libellé que le menu rend pour ce numéro. Le texte
est reçu en clair, jamais comme un chemin — c'est ce qui rend la morsure mesurable sans écrire un
fichier de documentation.

Deux tests l'emploient :

| Test | Ce qu'il tient |
| --- | --- |
| `test_arborescence_de_l_aiguillage_egale_le_menu_rendu` | Le fichier livré, contre le menu rendu par `GET /` (attentes lues par `_faits_du_rendu`, la même mesure que le détecteur) |
| `test_arborescence_abregee_signalee_par_le_controle` | La **morsure** : témoin conforme, puis chaque mutation substituée à une **copie en mémoire** du fichier réel, qui doit produire au moins un constat |

La règle d'appartenance du détecteur est **intacte** — et l'est par nécessité : `_mots_significatifs`
reste le jugement du détecteur, `TEMOIN_AIGUILLAGE_CORRIGE` (témoin légitime portant les formes
abrégées `3. PANOPLIES` / `4. OPTIMISATION`) n'a pas été touché, `test_renvois_legitimes_non_signales`
passe toujours, et le vert du critère 5 reste atteint par la correction du fichier livré, jamais par un
détecteur affaibli.

### Morsures observées (sortie réelle)

Mesure indépendante, sur le fichier tel qu'il était **au dernier commit avant ce gap**
(`git show HEAD:GUIDE_WIZARD.md` — donc l'état exact que la revue a jugé), puis sur les deux mutations,
puis sur le fichier corrigé :

```text
### ETAT REVU (HEAD, avant correction) :
  - arborescence dont un libelle n'est pas celui du menu rendu : la ligne « 3. PANOPLIES » n'est pas le libelle rendu
    du menu 3 ; le rendu de GET / associe 3 a « LISTE DES PANOPLIES », construit par dofus_stuff/web/routes.py (menu).
    Attendu le libelle **rendu**, compare normalise (D-11) : le detecteur, lui, juge par appartenance de mots
    significatifs et laisse donc passer une forme abregée (D-47)
  - arborescence dont un libelle n'est pas celui du menu rendu : la ligne « 4. OPTIMISATION » n'est pas le libelle rendu
    du menu 4 ; le rendu de GET / associe 4 a « OPTIMISATION DE STUFF », construit par dofus_stuff/web/routes.py (menu). …

### ETAT CORRIGE (arbre de travail) : aucun constat

### MUTATION '3. LISTE DES PANOPLIES' -> '3. PANOPLIES' :
  - arborescence dont un libelle n'est pas celui du menu rendu : la ligne « 3. PANOPLIES » …

### MUTATION '4. OPTIMISATION DE STUFF' -> '4. OPTIMISATION' :
  - arborescence dont un libelle n'est pas celui du menu rendu : la ligne « 4. OPTIMISATION » …
```

Trois choses sont donc établies, et non supposées : le contrôle **aurait attrapé** la dérive signalée
par la revue (2 constats sur l'état jugé), il est **silencieux** sur l'état corrigé, et il **mord**
sur chacune des deux formes abrégées, sur une copie en mémoire et jamais sur le fichier du dépôt.

## CR-02 — la phrase des touches

### La vérité mesurée, par étape

Barres de raccourcis des neuf écrans du wizard, mesurées au rendu (`/optimize/wizard/<etape>`, client de
test Flask, en processus) :

```text
1. slots          [('F7', 'Page prec'), ('F8', 'Suivant'),  ('ESC', 'Retour')]
2. options        [('F7', 'Precedent'), ('F8', 'Suivant'),  ('ESC', 'Retour')]
3. caracs         [('F7', 'Precedent'), ('F8', 'Suivant'),  ('ESC', 'Retour')]
4. papmpo         [('F7', 'Precedent'), ('F8', 'Suivant'),  ('ESC', 'Retour')]
5. resistances    [('F7', 'Precedent'), ('F8', 'Suivant'),  ('ESC', 'Retour')]
6. damages        [('F7', 'Precedent'), ('F8', 'Suivant'),  ('ESC', 'Retour')]
7. misc           [('F7', 'Precedent'), ('F8', 'Suivant'),  ('ESC', 'Retour')]
8. items          [('F7', 'Precedent'), ('F8', 'Suivant'),  ('ESC', 'Retour')]
9. recap          [('F7', 'Precedent'), ('F8', 'Page suiv'), ('ESC', 'Retour')]
```

et la barre du résultat simplifié (page 1 sur la fixture) :

```text
[('F7', 'Page prec'), ('F8', 'Page suiv'), ('ESC', 'Retour')]
```

Un « le wizard affiche `Precedent` et `Suivant` » général est donc faux **aux deux extrémités** :
l'étape 1 n'a pas de précédent et rend `Page prec`, le récapitulatif n'a pas de suivant et rend
`Page suiv` (`routes.py:138-139` : `f7_label = "Precedent" if f7_url else "Page prec"`, et de même
pour `F8`). D-64 (« cette affirmation doit rester vraie après cette phase ») ne pouvait donc pas être
satisfaite en laissant la phrase telle quelle ; la lecture stricte de D-63 (« aucun autre énoncé de
cette page n'est modifié ») était en conflit, et le porteur a tranché pour D-64 : la phrase doit être
**vraie**.

### La phrase, et ce qui n'a pas bougé

Avant :

> Ces libellés sont ceux du résultat : le wizard avancé, qui n'est pas décrit ici, affiche `Precedent`
> et `Suivant` **à la place**.

Après :

> Ces libellés sont ceux du résultat : le wizard avancé, qui n'est pas décrit ici, affiche `Precedent`
> et `Suivant` **sur ses écrans intermédiaires, et `Page prec` / `Page suiv` à ses deux extrémités**.

Le registre et la brièveté de la page sont conservés (une seule phrase, une seule ligne, même
ponctuation d'annonce), son **objet** est conservé (la barre du wizard diffère de celle du résultat, et
le wizard est décrit ailleurs), et le membre de phrase qui renvoie au wizard — « qui n'est pas décrit
ici » — est **inchangé**.

Précision mesurée, à ne pas confondre avec un lien oublié : la phrase de la ligne 140 **ne porte aucun
lien** vers la page du wizard, ni avant ni après. Les deux liens de la dette D-63 vivent aux lignes 5
et 256 de cette page ; ils n'ont pas été touchés et ont été **vérifiés intacts**
(`[wizard avancé](wizard-avance.md)` présent sur les deux lignes). Le membre de phrase « qui n'est pas
décrit ici » a en outre été laissé au **singulier** : l'ancre D-63 `ne sont pas décrits ici` (pluriel)
ne le capture donc pas, et `test_lien_wizard_avance_legitime` (invariants 1 et 5) reste vert sur ses
deux lignes d'origine.

### L'ancre renforcée : ce qui change, ce qui ne change pas

`tests/test_docs_parcours.py` portait `TOUCHES_WIZARD = (("F7", "Precedent"), ("F8", "Suivant"))` avec
un commentaire affirmant que ces libellés « ne sont produits que pour le wizard avancé » — un
commentaire qui rendait la généralisation de la page plausible, alors que le contrôle lui-même ne
disait rien des extrémités.

Ce qui **ne change pas** (vérifiable au diff) : la valeur de la constante est identique au caractère
près, et l'assertion négative qui l'emploie — `if touche in touches:` → constat si un couple du wizard
est rendu **sur la barre du résultat** — garde exactement la même condition, la même portée et la même
morsure. Rien n'est supprimé, rien n'est affaibli, aucun contrôle n'est déplacé hors de la suite.

Ce qui **change** :

1. **Renommage justifié** : `TOUCHES_WIZARD` → `TOUCHES_WIZARD_INTERMEDIAIRES`, et le commentaire
   corrigé : `Precedent`/`Suivant` sont les libellés des **seuls écrans intermédiaires** (2 à 8), ceux
   qui ont un voisin de chaque côté ; le nom d'origine faisait dire à la constante plus qu'elle ne
   tenait.
2. **Les deux extrémités, mesurées au rendu** : `EXTREMITE_WIZARD_SANS_PRECEDENT = ("slots", (("F7", "Page prec"), ("F8", "Suivant")))`
   et `EXTREMITE_WIZARD_SANS_SUIVANT = ("recap", (("F7", "Precedent"), ("F8", "Page suiv")))`. Les deux
   écrans sont rendus dans le test et leurs couples exigés **un par un** : l'ancre mord désormais sur
   la barre du wizard elle-même (elle échoue si `routes.py:138-139` change de règle), au lieu de ne
   regarder que la barre du résultat.
3. **La phrase de la page est gardée** : `_constats_touches_wizard(texte, normalize)` exige que la
   phrase ancrée par « Ces libellés sont ceux du résultat » cite, **après son ancre**, `Precedent`,
   `Suivant`, `Page prec` **et** `Page suiv`. Le point essentiel, et la raison de porter la garde
   *après* l'ancre : la page écrit un paragraphe par ligne, et cette même ligne cite déjà
   `F7=Page prec` / `F8=Page suiv` **pour le résultat**. Une garde sur la ligne entière aurait donc
   été satisfaite par l'ancienne phrase générale — elle n'aurait rien gardé (IN-02 de la même revue
   nomme exactement ce défaut pour un autre contrôle).

### Morsures observées (sortie réelle)

Garde de la phrase, sur la page telle qu'elle était au **dernier commit avant ce gap**
(`git show HEAD:docs/parcours-simplifie.md`), puis sur la page corrigée :

```text
### PHRASE AU DERNIER COMMIT (etat revise) :
  - affirmation generale sur les touches du wizard : la phrase « Ces libellés sont ceux du résultat… » ne cite pas
    « Page prec » ; attendu la verite **par etape** — les libelles des ecrans intermediaires du wizard **et** ceux de
    ses deux extremites, comme rendu par dofus_stuff/web/routes.py:138-139 et mesure sur /optimize/wizard/slots et
    /optimize/wizard/recap. …
  - affirmation generale sur les touches du wizard : la phrase « Ces libellés sont ceux du résultat… » ne cite pas
    « Page suiv » ; …

### PHRASE DE L'ARBRE DE TRAVAIL (etat corrige) : aucun constat
```

Ancrage des extrémités sur le rendu, puis sur des **copies mutées en mémoire** de ces rendus (aucune
écriture, aucun fichier de code touché) :

```text
### EXTREMITE 'slots' — couples attendus (('F7', 'Page prec'), ('F8', 'Suivant'))
  couples rendus : [('F7', 'Page prec'), ('F8', 'Suivant'), ('ESC', 'Retour')]
  manquants      : aucun
  copie mutee    : [('F7', 'Precedent'), ('F8', 'Suivant'), ('ESC', 'Retour')]
  manquants      : [('F7', 'Page prec')]

### EXTREMITE 'recap' — couples attendus (('F7', 'Precedent'), ('F8', 'Page suiv'))
  couples rendus : [('F7', 'Precedent'), ('F8', 'Page suiv'), ('ESC', 'Retour')]
  manquants      : aucun
  copie mutee    : [('F7', 'Suivant'), ('F8', 'Page suiv'), ('ESC', 'Retour')]
  manquants      : [('F7', 'Precedent')]
```

Assertion négative conservée (le renommage ne l'a pas vidée), page du résultat mesurée :

```text
barre du resultat mesuree : [('F7', 'Page prec'), ('F8', 'Page suiv'), ('ESC', 'Retour')]
couples TOUCHES_WIZARD_INTERMEDIAIRES presents : aucun -> l'assertion negative est bien exercee, pas vacuaire
copie mutee du rendu  : [('F7', 'Precedent'), ('F8', 'Page suiv'), ('ESC', 'Retour')]
couples presents (copie mutee) : [('F7', 'Precedent')] -> le constat d'affichage sortirait
```

Les morsures des points 1 à 3 ont été produites par des scripts jetables sous `.gsd-tmp/` (répertoire
de travail **non suivi**, jamais indexé) et supprimés après mesure. La morsure **durable** est celle qui
vit dans la suite : `tests/test_docs_wizard.py::test_arborescence_abregee_signalee_par_le_controle`
rejoue les deux mutations à chaque exécution, et les contrôles de phrase et d'extrémités sont des
assertions ordinaires de `tests/test_docs_parcours.py`.

## Avertissements de `04-REVIEW.md` évalués, et pourquoi ils restent ouverts

| Réf. | Objet | Décision |
| --- | --- | --- |
| WR-01 | Énumération des refus de l'écran `slots` incomplète (`SLOT INVALIDE`) | **Hors périmètre** : porte sur `docs/wizard-avance.md`, qui ne fait pas partie des fichiers autorisés par la consigne. Constat réel, laissé ouvert |
| WR-02 | L'assertion CRLF de `test_docs_wizard.py` mesure un artefact git local (`core.autocrlf`), pas la page | **Hors périmètre** : fichier autorisé, mais le fait est étranger aux deux constats critiques (il porte sur `docs/wizard-avance.md` livrée au plan 04-04). Le corriger changerait le sens d'un contrôle existant, ce que la consigne réserve au contenu. Laissé ouvert |
| WR-03 | Helpers de rendu recopiés d'un module de test à l'autre, contre la leçon de `tests/conftest.py` | **Hors périmètre** : refonte du harnais partagé (plusieurs modules, fixtures de session), aucun lien avec CR-01/CR-02. Laissé ouvert |
| WR-04 | Deux lecteurs rendent un `IndexError` nu au lieu d'un constat localisant | **Hors périmètre** : solidité du harnais, hors des deux constats. Laissé ouvert |
| WR-05 | Deux sections du guide supprimé sans propriétaire, dont le repli `POIDS : (aucun — defaut INT)` | **Hors périmètre** : ajouter ce fait produit demanderait d'écrire dans `docs/wizard-avance.md`, interdit ici. Laissé ouvert |

Aucun de ces cinq points n'est masqué : ils sont nommés ici avec la raison de leur report. Choisir de
les corriger aurait fait sortir ce gap de son objet (deux constats critiques, modification chirurgicale
de quatre fichiers).

## Vérifications

Suite complète, sortie réelle, après les quatre commits de contenu :

```text
........................................................................ [ 35%]
........................................................................ [ 70%]
.............................................................            [100%]
205 passed in 3.55s
```

- **205 passed, 0 failed, 0 skipped, 0 xfailed** — la ligne de pytest n'annonce ni `skipped` ni
  `xfailed`, et le diff complet ne contient **aucun** appel `pytest.mark`/`skip`/`xfail` ajouté
  (`git diff 7b2ebc2..HEAD -- tests/` filtré : aucun).
- La barre de référence était **203 passed** au commit `7b2ebc2` ; le solde est **+2** : les deux tests
  ajoutés par CR-01. Aucun test n'a été supprimé, renommé ni déplacé.
- **Fichiers touchés** (`git diff --stat 7b2ebc2..HEAD`) : `GUIDE_WIZARD.md` (+2/−2),
  `docs/parcours-simplifie.md` (+1/−1), `tests/test_docs_parcours.py` (+101/−8),
  `tests/test_docs_wizard.py` (+152/−0). Exactement les quatre fichiers autorisés, rien d'autre.
- **`.data/` intacte** : `dofus.sqlite3` porte toujours son `mtime` du **2026-09-06 23:27**. Aucun
  `db clear`, aucun `drop`, aucune suppression, aucune écriture sous `.data/`.
- **Octets** : les quatre fichiers édités sont **UTF-8 sans BOM** et **CRLF sur toutes leurs lignes**
  (18/18, 269/269, 2721/2721, 2990/2990 retours chariot mesurés en fin de travail).
- **Liens D-63** : `[wizard avancé](wizard-avance.md)` présent aux lignes 5 et 256 de
  `docs/parcours-simplifie.md`, inchangé.
- **Forme de l'aiguillage** : `GUIDE_WIZARD.md` fait **18 lignes**, un seul `H1`, ses deux liens, et
  reste sans aucun énoncé de contenu — les contrôles de `test_aiguillage_et_readme` et de
  `test_aiguillage_sans_renvoi_obsolete` sont verts (18 tests dans `test_docs_wizard.py`, 18 dans
  `test_docs_parcours.py`).
- **Ce qui n'a pas été exécuté** : `main()`, tout POST `GO` (il lancerait le solveur), toute commande
  destructive, tout accès réseau, toute synchronisation Dofusdude. La base locale n'a pas été
  resynchronisée : le besoin ne l'exigeait pas.

## Écarts (Deviations from Plan)

Deux écarts, tous deux documentés plutôt que silencieux.

**1. [Rule 2 — fonctionnalité critique manquante] Un contrôle dérivé, `_constats_touches_wizard`.**

- **Constaté pendant :** task 4 (ancre CR-02).
- **Problème :** la garde de la phrase demandait d'être mesurable, or `tests/test_docs_parcours.py`
  écrit ses contrôles en ligne dans le test, sur le texte lu depuis le disque : la morsure n'aurait été
  démontrable qu'en modifiant temporairement la page du dépôt.
- **Correction :** la garde est extraite en fonction pure recevant le **texte**, comme
  `_constats_arborescence` côté CR-01. Aucune assertion n'en est affaiblie ; le test l'appelle avec la
  page livrée et la morsure est reproductible sur n'importe quel texte.
- **Fichiers :** `tests/test_docs_parcours.py`. **Commit :** `a498df6`.

**2. [Rule 3 — obstacle à la tâche] Le registre du plan (`plan_head_before`).**

- **Constaté pendant :** avant la rédaction de ce résumé.
- **Problème :** le registre de base n'avait pas été posé avant le premier commit, et la mesure
  automatique renvoyait donc `0` commit.
- **Correction :** la base a été réécrite à `7b2ebc2`, valeur **vérifiable** (`git rev-parse 9f09061^`,
  soit le parent du premier commit de ce gap) et non choisie pour arranger le compte. Le compte mesuré
  est de **4** commits ; le commit de métadonnées de ce résumé est le **5ᵉ**, postérieur à la mesure.
- **Fichiers :** aucun fichier du dépôt (registre interne à `.git`). **Effet :** `commits: 4` dans
  l'en-tête est une mesure, pas un récit.

Aucun écart de type Rule 4 (changement architectural), aucune porte d'authentification rencontrée,
aucune installation de paquet, aucun blocage de précondition.

## Commits

| Hash | Message | Contenu |
| --- | --- | --- |
| `9f09061` | `fix(04-gap): arborescence de GUIDE_WIZARD.md selon les libelles rendus (CR-01)` | `GUIDE_WIZARD.md` |
| `b7e4706` | `test(04-gap): controle d'egalite de l'arborescence et sa morsure par mutation (CR-01)` | `tests/test_docs_wizard.py` |
| `06c6461` | `fix(04-gap): la phrase des touches dit la verite par etape du wizard (CR-02)` | `docs/parcours-simplifie.md` |
| `a498df6` | `test(04-gap): ancre des touches du wizard par etape, renforcee (CR-02)` | `tests/test_docs_parcours.py` |

Chaque commit a été indexé **par chemin explicite** (jamais `git add .`), avec les crochets de dépôt
actifs (`--no-verify` jamais employé), sur `main` — branche autorisée par
`.planning/config.json` (`git.allow_default_branch_commits: true`), sans création ni changement de
branche. Les éléments de l'hôte de planification (`.gsd/`, `.gsd-tmp/`, `.doc-agent/`, `doc-agent.toml`,
`gsd-auto*.toml`, `.planning/state.json`, `.planning/config.json`, `.gitignore`) n'ont été ni indexés ni
modifiés.

## Self-Check

- `GUIDE_WIZARD.md` : `FOUND` (18 lignes, CRLF, sans BOM) — arborescence conforme au rendu mesuré.
- `docs/parcours-simplifie.md` : `FOUND` (269 lignes, CRLF, sans BOM) — phrase par étape, liens D-63
  intacts.
- `tests/test_docs_wizard.py` : `FOUND` (2721 lignes, CRLF, sans BOM) — 18 tests verts.
- `tests/test_docs_parcours.py` : `FOUND` (2990 lignes, CRLF, sans BOM) — 18 tests verts.
- Commits `9f09061`, `b7e4706`, `06c6461`, `a498df6` : `FOUND` dans `git log`.

**Self-Check: PASSED**

## Critères de succès

- [x] Les cinq lignes de l'arborescence de `GUIDE_WIZARD.md` égalent, après normalisation, les libellés
      que le menu rend réellement (mesurés à l'exécution, `5. SYSTEME` confirmé).
- [x] Une assertion nouvelle **échoue** si l'arborescence est ré-abrégée : bite observée sur `3. PANOPLIES`
      et `4. OPTIMISATION`, à chaque exécution de la suite (mutation sur copie en mémoire).
- [x] `docs/parcours-simplifie.md` énonce la vérité par étape, extrémités comprises.
- [x] L'ancre de `tests/test_docs_parcours.py` est **renforcée** (même valeur, même assertion négative,
      plus les deux extrémités mesurées et la garde de la phrase), avec ses bites montrées.
- [x] Suite complète verte : **205 passed**, 0 failed, 0 skipped, 0 xfailed — sortie réelle ci-dessus.
- [x] Chaque changement commité individuellement, par chemin explicite.
- [x] D-64 satisfaite : la phrase du parcours simplifié est **vraie** après cette phase, et la revue qui
      l'avait signalée comme fausse ne l'est plus.
