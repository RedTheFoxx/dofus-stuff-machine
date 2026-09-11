---
phase: 04-wizard-avanc-et-r-sorption-de-la-dette-guide-wizard
plan: 03
subsystem: documentation
tags: [markdown, pytest, detecteur-pur, renvois-obsoletes, aiguillage, dette-de-renvoi, etat-vert, crlf, sqlite-hors-ligne, documentation-francaise]

# Dependency graph
requires:
  - phase: 04-wizard-avanc-et-r-sorption-de-la-dette-guide-wizard
    plan: 04
    provides: "tests/test_docs_wizard.py (le detecteur de renvois obsoletes : fonction pure a trois formes nommees, attentes mesurees au rendu, constats nommant la valeur fautive, la valeur attendue et le fichier producteur), `tests/fixtures/guide-wizard-obsolete.md` (la copie figee qui rend le rouge relancable) et l'observation ROUGE du critere 5"
  - phase: 04-wizard-avanc-et-r-sorption-de-la-dette-guide-wizard
    plan: 02
    provides: "docs/wizard-avance.md : la page unique et son ancrage (arrivee reelle sur le recap, couples de touches par etape, exemple guide migre) vers laquelle l'aiguillage pointe"
provides:
  - "GUIDE_WIZARD.md : l'aiguillage corrige de 18 lignes (un H1, l'avis de deplacement vers docs/wizard-avance.md, l'arborescence de menus lue au code — 4 = OPTIMISATION, 3 = PANOPLIES, 5 = SYSTEME — et le second lien vers docs/sommaire.md)"
  - "README.md : la ligne « Guide detaille » retiree sans texte de remplacement (D-62), aucun renvoi produit, et son lien unique vers docs/sommaire.md conserve"
  - "tests/test_docs_wizard.py : test_aiguillage_et_readme et ses trois constantes de motif (MOTIF_AIGUILLAGE_BRUYANT, MOTIF_LIEN_PRODUIT, MOTIF_LIEN_AIGUILLAGE) ; 171 lignes ajoutees, 0 retiree — aucun predicat ni assertion du detecteur de 04-04 n'est touche"
  - "Le VERD du critere 5 : test_aiguillage_sans_renvoi_obsolete passe (zero constat sur le fichier livre) pendant que test_copie_figee_signalee_par_le_detecteur exige toujours ses trois constats sur la copie figee — la transition rouge -> vert de la meme phase (D-59a/D-59b)"
  - "docs/parcours-simplifie.md : les deux renvois en prose (lignes 5 et 256) portent un vrai lien vers wizard-avance.md, sans qu'aucun autre enonce de la page soit modifie (la ligne 140 reste intacte, D-64)"
  - "tests/test_docs_parcours.py : PAGES_INEXISTANTES reduit a la seule page reellement inexistante, LIENS_LEGITIMES_VERS_L_AIGUILLAGE, et test_lien_wizard_avance_legitime (cinq invariants, quatre constantes de motif)"
affects: [verification-phase-4, ship]

# Actuals (#2632) — mesures sur la meme echelle que l'estimate du plan (chars/4 du diff realise).
# L'ecart avec l'estimate (74 000) est consigne tel quel : il mesure le pessimisme de l'estimate, pas un
# travail non fait (les deux taches sont livrees, 8/8 morsures detectees et le vert du critere 5 obtenu).
actuals:
  tokens: 8162     # chars/4 sur le diff realise (19 712 caracteres ajoutes, 12 938 retires, 2 commits)
  tasks: 2
  commits: 2       # MESURE en ecriture du SUMMARY : git rev-list --count 70085c6..HEAD ; le commit de
                   # metadonnees du plan (SUMMARY + STATE + ROADMAP) s'y ajoute et n'est pas compte ici
  plan_head_before: 70085c6b25d497d2f26d15a592b7bf4ddccf0386

# Tech tracking
tech-stack:
  added: []          # aucune dependance ajoutee (pyproject.toml inchange) ; aucune installation
  patterns:
    - "Le vert d'un controle de contenu s'obtient par la **correction du fichier juge** : le controle du fichier livre passe pendant que la copie figee reste signalee, donc la morsure ne s'eteint pas en meme temps que le vert (D-59a/D-59b)"
    - "Un fichier de la racine du depot (l'aiguillage, le README) est couvert par le module qui porte deja ses controles voisins : `test_docs_structure.py` ne parcourt que `docs/**`, donc les invariants de l'aiguillage vivent dans `tests/test_docs_wizard.py` et le renvoi legitime dans `tests/test_docs_parcours.py`, a cote de son modele (`PAGES_INEXISTANTES`)"
    - "Absence d'enonce de contenu mesuree par des marqueurs nommes : ceux du rendu pour les options du solveur (lues a `/optimize/wizard/options`), ceux du code pour le refus de la syntaxe d'items et les deux formats d'edition des quatre nombres — jamais une liste recopiee"
    - "Une reserve (`PAGES_INEXISTANTES`) est rendue **inversible** par une garde qui refuse qu'une page existante soit declaree inexistante : reduire la reserve est obligatoire des que la cible est livree (D-63)"
    - "Un renvoi qui perd sa cible reste identifiable : l'ancre est cherchee sur la ligne **depouillee de ses crochets de lien**, sinon la morsure « lien retire » serait indiscernable d'une phrase deplacee"

key-files:
  created: []
  modified:
    - GUIDE_WIZARD.md
    - README.md
    - tests/test_docs_wizard.py
    - docs/parcours-simplifie.md
    - tests/test_docs_parcours.py

key-decisions:
  - "L'aiguillage porte l'arborescence de menus **lue au code** (D-47) : `4. OPTIMISATION`, `3. PANOPLIES`, `5. SYSTEME`, aux formes abregees que D-47 prescrit, avec les libelles rendus complets (`RECHERCHE D'OBJETS`, `LISTE DES EQUIPEMENTS`) pour les entrees 1 et 2. C'est exactement le texte corrige type que porte le temoin legitime du detecteur de 04-04."
  - "Le fichier est ramene de 330 a **18 lignes** (plafond du plan : 20) et reste en CRLF, UTF-8 sans BOM : la convention mesuree du depot est conservee, sans seconde convention."
  - "Le `H1` et le texte de l'avis de deplacement relevent de Claude's Discretion (04-CONTEXT.md) : le controle ne fige donc **pas** la formulation, seulement la forme courte, les deux liens et l'absence d'enonce de contenu."
  - "La phrase « tapez `3` pour ouvrir l'optimisation » est remplacee par « Tapez `4` puis Entree pour ouvrir l'optimisation » : l'invitation porte le numero **mesure** (4), ce que le detecteur exige (forme (a))."
  - "`README.md` perd la ligne « Guide detaille » **sans texte de remplacement** (D-62) : aucun renvoi n'est ajoute vers `docs/wizard-avance.md`, et la section « Documentation utilisateur » garde son lien **unique** vers `docs/sommaire.md` (D-10/D-29, D-17)."
  - "Les deux renvois de `docs/parcours-simplifie.md` deviennent de **vrais liens** (`[wizard avancé](wizard-avance.md)`) et rien d'autre ne bouge sur ces deux lignes : la ligne 140 (`Precedent`/`Suivant`) reste intacte (D-64), ce que `git diff` prouve (2 lignes modifiees, 2 ajoutees)."
  - "`PAGES_INEXISTANTES` perd `wizard-avance.md` et garde `base-locale.md` : les phrases `RENVOIS_SANS_LIEN` (`réglages avancés`, `base locale`) restent presentes, donc la dette restante reste visible au lieu d'etre masquee par la levee de D-44."
  - "`test_lien_wizard_avance_legitime` exige les cinq invariants de la tache 2 et **rien de plus** : il ne relit pas la prose de la page en dehors des deux renvois qu'il nomme, et ne revendique aucune exhaustivite."
  - "Le vert du critere 5 est consigne avec ses deux commandes, et **aucune** validite humaine n'est revendiquee : le rouge venait d'une sortie de commande (04-04), le vert vient de la meme suite apres correction du fichier."

patterns-established:
  - "Pattern 9 : un controle dont le rouge est transitoire se prolonge par le controle de sa **forme corrigee** — la morsure survit (copie figee) et le vert du fichier livre est exige par des invariants separes de ceux du detecteur"
  - "Pattern 10 : une reserve de cibles (page declaree inexistante) porte sa propre garde d'existence, ce qui rend sa reduction obligatoire, verifiable et inversable au moment ou la cible est livree"

requirements-completed: [WIZ-03]

coverage:
  - id: D1
    description: "`GUIDE_WIZARD.md` est un aiguillage de 18 lignes : un seul `H1`, l'avis de deplacement vers `docs/wizard-avance.md`, l'arborescence de menus lue au code (4 = OPTIMISATION, jamais 3), un lien vers la page unique et un lien vers `docs/sommaire.md`, sans aucun enonce de contenu"
    requirement: "WIZ-03"
    verification:
      - kind: unit
        ref: "tests/test_docs_wizard.py#test_aiguillage_et_readme"
        status: pass
      - kind: integration
        ref: "./.venv/Scripts/python.exe -m pytest -q -> 203 passed"
        status: pass
    human_judgment: false
  - id: D2
    description: "`README.md` ne mentionne plus `GUIDE_WIZARD`, n'ajoute aucun renvoi vers `docs/wizard-avance.md` et garde exactement un lien markdown vers `docs/sommaire.md`"
    requirement: "WIZ-03"
    verification:
      - kind: unit
        ref: "tests/test_docs_wizard.py#test_aiguillage_et_readme"
        status: pass
      - kind: unit
        ref: "tests/test_docs_structure.py#test_readme_links_to_sommaire"
        status: pass
    human_judgment: false
  - id: D3
    description: "Le critere 5 passe **de rouge a vert** : `test_aiguillage_sans_renvoi_obsolete` est vert sur le fichier livre pendant que `test_copie_figee_signalee_par_le_detecteur` exige toujours ses trois constats sur `tests/fixtures/guide-wizard-obsolete.md`, et 4 derives epinglees (lien retire, phrase d'arrivee directe reintroduite, ligne « Guide detaille » remise, enonce de contenu remis) font rougir la suite"
    requirement: "WIZ-03"
    verification:
      - kind: unit
        ref: "tests/test_docs_wizard.py#test_aiguillage_sans_renvoi_obsolete + #test_copie_figee_signalee_par_le_detecteur -> 2 passed"
        status: pass
      - kind: integration
        ref: "batterie de morsures 04-03 tache 1 : 4/4 detectees, motif cherche present, chacune sur copie verte avant mutation"
        status: pass
    human_judgment: false
  - id: D4
    description: "La dette D-44 est levee : les deux renvois en prose de `docs/parcours-simplifie.md` portent un lien vers `wizard-avance.md`, `PAGES_INEXISTANTES` est reduit a `base-locale.md` dans le **meme commit**, la reserve ne peut pas declarer inexistante une page qui existe, et chaque cible de l'aiguillage vers `docs/` est declaree ET existe"
    requirement: "WIZ-03"
    verification:
      - kind: unit
        ref: "tests/test_docs_parcours.py#test_lien_wizard_avance_legitime"
        status: pass
      - kind: integration
        ref: "batterie de morsures 04-03 tache 2 : 4/4 detectees sur copie verte avant mutation"
        status: pass
      - kind: integration
        ref: "git log -1 --name-only -> docs/parcours-simplifie.md et tests/test_docs_parcours.py dans le commit eeaa93f"
        status: pass
    human_judgment: false
  - id: D5
    description: "La ligne ~140 de `docs/parcours-simplifie.md` (`Precedent`/`Suivant`) reste **intacte** : aucun autre enonce de la page n'est modifie par la conversion des deux renvois"
    verification:
      - kind: integration
        ref: "git diff --unified=0 70085c6..eeaa93f -- docs/parcours-simplifie.md -> 2 lignes modifiees (5 et 256), ligne 140 absente du diff"
        status: pass
      - kind: integration
        ref: "tests/test_docs_wizard.py#test_touches_et_commandes_par_etape (controle par etape de la phase 4 : aucune assertion ne contredit la ligne 140)"
        status: pass
    human_judgment: false
  - id: D6
    description: "`.data/dofus.sqlite3` est intact (taille, mtime_ns, sha256) apres la suite complete, et aucun fichier de `dofus_stuff/**` n'est modifie"
    verification:
      - kind: integration
        ref: "24989696:1788730056843137500:e3793d64cb7939ad1a51837b075b6b95e03d64c878fcb9cc07f86c00bb8fef7b avant et apres la suite"
        status: pass
      - kind: integration
        ref: "git status --short -> aucun fichier de dofus_stuff/ modifie ; aucun ajout d'affichage hors des 5 fichiers du plan"
        status: pass
    human_judgment: false

# Metrics
duration: 6min
completed: 2026-09-11
status: complete
---

# Phase 4 : Wizard avance et resorption de la dette GUIDE_WIZARD — Plan 03 Summary

**Le critere 5 passe ROUGE a VERT par la seule correction du contenu : `GUIDE_WIZARD.md` est ramene de 330 a 18 lignes (arborescence lue au code — `4. OPTIMISATION`, pas `3` —, deux liens de navigation, aucun enonce de contenu), `README.md` perd son pointeur produit, et le detecteur de 04-04, inchange au caractere pres, ne signale plus rien sur le fichier livre pendant que sa copie figee reste signalee. La dette D-44 est levee dans le meme commit que sa cible : les deux renvois de `docs/parcours-simplifie.md` deviennent de vrais liens et `PAGES_INEXISTANTES` est reduit a la seule page reellement inexistante.**

## Performance

- **Duration:** environ 6 min de lecture/execution (19:14:17Z -> 19:20:12Z), dont 58 s entre le premier et le dernier commit de tache
- **Started:** 2026-09-11T19:14:17Z
- **Completed:** 2026-09-11T21:18:50+02:00 (dernier commit de tache : `eeaa93f`)
- **Tasks:** 2
- **Files modified:** 5 (`GUIDE_WIZARD.md` 330 -> 18 lignes, `README.md` -2 lignes, `tests/test_docs_wizard.py` +171, `docs/parcours-simplifie.md` 2 lignes, `tests/test_docs_parcours.py` +165 -2)

## Accomplishments

- **Le critere 5 est vert, et le vert vient de la correction — jamais d'un detecteur affaibli.** Le detecteur de 04-04 est **inchange** : `git show --numstat ba11149 -- tests/test_docs_wizard.py` rend `171 0` — 171 lignes ajoutees, **zero retiree**. Aucun predicat de `renvois_obsoletes`, aucun champ de `_faits_du_rendu`, aucune assertion de `test_aiguillage_sans_renvoi_obsolete` n'est touche.
- **La transition rouge -> vert, verbatim** (les deux commandes et leurs sorties reelles, § *Le vert observe, verbatim*) : `1 failed, 200 passed` avant (l'echec unique etait `test_aiguillage_sans_renvoi_obsolete`, avec les trois formes nommees) ; `203 passed` apres (les deux tests nouveaux plus le passage au vert du controle existant).
- **La morsure ne s'eteint pas avec le vert** (D-59a/D-59b) : `test_copie_figee_signalee_par_le_detecteur` passe **encore** avec ses trois constats exiges sur `tests/fixtures/guide-wizard-obsolete.md`, dont le libelle rendu du menu d'optimisation et celui de `F7` ; la copie figee est **byte-identique** (`git diff --quiet -- tests/fixtures/guide-wizard-obsolete.md` est vrai).
- **`GUIDE_WIZARD.md` est un aiguillage de 18 lignes** (plafond du plan : 20), CRLF, UTF-8 sans BOM : un `H1`, l'avis de deplacement vers `docs/wizard-avance.md`, l'arborescence de menus **lue au code** (`1. RECHERCHE D'OBJETS`, `2. LISTE DES EQUIPEMENTS`, `3. PANOPLIES`, `4. OPTIMISATION`, `5. SYSTEME` — les formes abregees que D-47 prescrit), l'invitation « Tapez `4` puis **Entree** pour ouvrir l'optimisation. » et le second lien vers `docs/sommaire.md`. Aucune table des touches, aucun format des quatre nombres, aucune syntaxe d'items, aucun exemple guide, aucun `db clear` : ce sont les quatre marqueurs d'enonce de contenu et la commande destructrice que le nouveau controle exige absents.
- **`README.md` perd son pointeur produit sans texte de remplacement** (D-62) : plus aucune occurrence de `GUIDE_WIZARD` ni de `wizard-avance`, et **exactement un** lien markdown vers `docs/sommaire.md` (le controle de structure de la phase 1 le garde de son cote).
- **La dette D-44 est levee dans le meme commit que sa cible** (D-63) : les deux renvois en prose (`docs/parcours-simplifie.md` lignes 5 et 256) portent `[wizard avancé](wizard-avance.md)`, `PAGES_INEXISTANTES` passe de `("wizard-avance.md", "base-locale.md")` a `("base-locale.md",)`, et le commit `eeaa93f` porte **les deux** fichiers (verifie par le controle de commit du plan, § *Le vert observe, verbatim*). Aucun autre enonce de la page n'est touche : la ligne 140 (`Precedent`/`Suivant`) reste intacte (D-64).
- **La reserve ne peut plus mentir** : `test_lien_wizard_avance_legitime` refuse toute entree de `PAGES_INEXISTANTES` qui correspond a une page existant sur disque — c'est cette garde qui rend la reduction obligatoire et **inversible** (remettre `wizard-avance.md` dans la reserve fait rougir la suite, mutation `pages_inexistantes_non_reduite`).
- **Le renvoi de l'aiguillage est un renvoi legitime prouve a cote de son modele** : chaque cible de lien de `GUIDE_WIZARD.md` vers `docs/` doit etre **declaree** dans `LIENS_LEGITIMES_VERS_L_AIGUILLAGE` **et** exister depuis la racine du depot. Les deux derives epinglees le prouvent : cible cassee -> « lien vers une page inexistante », `docs/cli.md` ajoute sans declaration -> « lien non declare ».
- **Huit derives epinglees, huit detectees, chacune sur une copie verte avant mutation** : 4/4 pour la tache 1 (lien de l'aiguillage retire, phrase d'arrivee directe reintroduite, ligne « Guide detaille » remise dans le README, enonce de contenu remis dans l'aiguillage) et 4/4 pour la tache 2 (lien D-63 retire, page existante remise dans la reserve, cible de l'aiguillage cassee, lien non declare ajoute).
- **Aucune ecriture hors des 5 fichiers du plan, aucune execution du produit, aucun reseau** : `.data/dofus.sqlite3` garde taille, `mtime_ns` et SHA-256 (`24989696:1788730056843137500:e3793d64cb7939ad1a51837b075b6b95e03d64c878fcb9cc07f86c00bb8fef7b`), aucun fichier de `dofus_stuff/**` n'est modifie, aucune dependance n'est ajoutee (`pyproject.toml` inchange, aucun `pip install`), et le module de la phase 3 passe de 17 a 18 tests **tous verts**.
- **La formulation reste libre, les invariants sont tenus** : le `H1` (« Guide du wizard : aiguillage ») et l'avis de deplacement relevent de Claude's Discretion (04-CONTEXT.md) ; le controle ne fige donc pas la prose, seulement la forme courte, les deux liens, les cibles existantes et l'absence d'enonce de contenu.

## Task Commits

Each task was committed atomically:

1. **Tache 1 : reduire `GUIDE_WIZARD.md` a l'aiguillage corrige, nettoyer `README.md`, obtenir le vert du critere 5** — `ba11149` (feat) : 9/321 `GUIDE_WIZARD.md`, 0/2 `README.md`, 171/0 `tests/test_docs_wizard.py`
2. **Tache 2 : lever la dette D-63 et reduire la reserve dans le meme commit** — `eeaa93f` (docs) : 2/2 `docs/parcours-simplifie.md`, 165/2 `tests/test_docs_parcours.py`

**Plan metadata:** `docs(04-03): complete ...` (voir le commit de metadonnees du plan, qui porte ce SUMMARY et la mise a jour de STATE/ROADMAP ; il n'est pas compte dans `actuals.commits`)

## Files Created/Modified

- `GUIDE_WIZARD.md` — **reecrit** : 330 -> 18 lignes. Contenu : `H1`, avis de deplacement vers `docs/wizard-avance.md` (lien), arborescence de menus lue au code (`4. OPTIMISATION`, `3. PANOPLIES`, `5. SYSTEME`), invitation a taper `4`, second lien vers `docs/sommaire.md`. Toute la matiere retiree avait deja une destination : l'exemple guide et les sections de contenu vivent dans `docs/wizard-avance.md` (plans 04-01/04-02, D-55), l'original reste dans `tests/fixtures/guide-wizard-obsolete.md` (D-59b) et dans l'historique git (D-49).
- `README.md` — **la ligne `**Guide détaillé :** [GUIDE_WIZARD.md](GUIDE_WIZARD.md)` (ligne 63, emplacement verifie au fichier reel avant edition) est supprimee sans texte de remplacement (D-62) ; aucune autre ligne n'est touchee.
- `tests/test_docs_wizard.py` — **complete** (+171 lignes, 0 retiree) : les constantes `LIGNES_MAX_AIGUILLAGE`, `CIBLE_AIGUILLAGE`, `CIBLE_SOMMAIRE`, `NOM_PRODUIT_AIGUILLAGE`, `NOM_PAGE_WIZARD`, `MOTIF_AIGUILLAGE_BRUYANT`, `MOTIF_LIEN_PRODUIT`, `MOTIF_LIEN_AIGUILLAGE`, `MOTIF_LIEN_MARKDOWN`, `MARQUEURS_DE_CONTENU`, et le test `test_aiguillage_et_readme` (cinq blocs : forme courte, deux liens et cibles existantes, marqueurs d'enonce de contenu compares normalises, lignes d'options du solveur lues au rendu de `/optimize/wizard/options`, README sans renvoi produit avec un seul lien vers le sommaire). Le module passe de 15 a 16 tests.
- `docs/parcours-simplifie.md` — **2 lignes** : les deux renvois en prose (5 et 256) portent `[wizard avancé](wizard-avance.md)`. Les phrases exigees par `RENVOIS_SANS_LIEN` restent presentes et la ligne de retour au sommaire ne bouge pas ; 269 lignes avant et apres, CRLF 269/269, sans BOM.
- `tests/test_docs_parcours.py` — **complete et reduit** (+165, -2) : `PAGES_INEXISTANTES` reduit a `("base-locale.md",)` avec son commentaire mis a jour, `LIENS_LEGITIMES_VERS_L_AIGUILLAGE`, les constantes `PAGE_WIZARD`, `GUIDE_WIZARD`, `PREFIXE_DOCS`, `ANCRES_RENVOI_D63`, `MOTIF_LIEN_MARKDOWN` et les quatre motifs (`MOTIF_LIEN_D63`, `MOTIF_PAGES_INEXISTANTES`, `MOTIF_LIEN_NON_DECLARE`, `MOTIF_LIEN_MORT`), puis `test_lien_wizard_avance_legitime` avec ses cinq invariants. Le module passe de 17 a 18 tests.

## Decisions Made

- **Aiguillage aux formes abregees de D-47** (`4. OPTIMISATION`, `3. PANOPLIES`, `5. SYSTEME`) : ce sont les formes que D-47 prescrit et le texte corrige type que porte le temoin legitime du detecteur de 04-04 — un aiguillage ecrit autrement aurait ete declare fautif ou n'aurait pas ete reconnu comme le texte attendu.
- **Le fichier livre garde la convention mesuree du depot** (CRLF, UTF-8 sans BOM, 18/18 CRLF) et reste sous le plafond de 20 lignes, sans seconde convention introduite.
- **Le controle ne fige pas la prose** : seuls la forme courte, les deux liens, l'existence des cibles et l'absence des enonces de contenu nommes sont exiges, ce qui laisse le `H1` et l'avis de deplacement a Claude's Discretion.
- **Les enonces de contenu sont juges par des marqueurs nommes, pas par une recopie** : le refus de la syntaxe d'items et les deux formats d'edition sont ceux du code (`optimize_wizard.py:424`, `routes.py:1254` et `:1260`), les lignes d'options du solveur sont **lues au rendu** de `/optimize/wizard/options`, et la commande destructrice est le motif deja employe par la garde de la page d'installation (D-61).
- **`README.md` ne recoit aucun renvoi de remplacement** : retirer la ligne suffit, et compter exactement un lien vers le sommaire rend le controle de structure discriminant (D-10/D-29, D-17).
- **La reserve est liee a sa garde d'existence** : la reduction de `PAGES_INEXISTANTES` et le nouveau controle vivent dans le meme commit que le lien, ce que le controle de commit du plan verifie nommement.
- **Le vert est consigne tel quel**, avec ses deux commandes et la mesure d'empreinte de la base locale ; aucune validite humaine n'est revendiquee et aucune exhaustivite de detection ne l'est non plus (trois formes nommees, D-58/D-26).

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 — Blocage : forme du controle] La fixture `app` a ete ajoutee a la signature de `test_aiguillage_et_readme`**

- **Found during:** Tache 1 (ecriture du test)
- **Issue:** l'action du plan nomme la signature `test_aiguillage_et_readme(docs_dir, normalize)` mais exige aussi que le controle mesure « l'absence des lignes d'options du solveur » — or ces lignes n'existent dans aucune constante publique (`body_options` ecrit onze lignes litterales), et `D-14` interdit de se coller a une constante privee. Mesurer au rendu, comme le reste du module, demande le client de test Flask, donc la fixture `app`.
- **Fix:** signature `test_aiguillage_et_readme(docs_dir: Path, app, normalize)` ; les libelles d'options sont lus a `/optimize/wizard/options` par les helpers **existants** du module (`_lignes_du_corps`, `_options_du_rendu`) et compares a la ligne de l'aiguillage par appartenance de mots significatifs. Aucun helper n'est recopie de `tests/conftest.py` ni d'un autre module (D-12).
- **Files modified:** `tests/test_docs_wizard.py` (meme commit que la tache 1)
- **Verification:** `test_aiguillage_et_readme` passe ; la batterie de la tache 1 reste **4/4** (les quatre mutations sont detectees) ; la suite complete est verte.
- **Committed in:** `ba11149` (part of task 1 commit)

---

**Total deviations:** 1 auto-fixed (1 forme de controle, sans changement de perimetre).
**Impact on plan:** aucun ecart de perimetre — les cinq fichiers du plan sont exactement ceux modifies, aucun fichier de `dofus_stuff/**` n'est touche, le detecteur et sa copie figee restent intacts au caractere pres, et aucune dependance n'est ajoutee.

## Issues Encountered

- **Le plan annoncait un defaut de quoting possible dans ses commandes `<automated>` : il ne s'est pas produit ici.** Les deux batteries (tache 1 et tache 2) ont ete executees **telles qu'elles sont ecrites** dans le plan, sans correction d'adresse ni de quoting : `4/4` morsures detectees pour chacune, et le controle de commit de la tache 2 a rendu `eeaa93f`. Aucune deviation de commande n'est donc consignee (contrairement aux plans 04-01, 04-02 et 04-04).
- **La note d'etat du module de 04-04 reste la trace de sa fenetre rouge.** La docstring de `tests/test_docs_wizard.py` annonce que `test_aiguillage_sans_renvoi_obsolete` est rouge « tant que l'aiguillage livre `GUIDE_WIZARD.md` n'a pas ete corrige (plan 04-03, vague 4) » : elle est un enregistrement de l'etat **de la vague 3** et n'a pas ete touchee, parce que le plan de cette vague interdit de modifier le detecteur et ses tests (`171 0`), et que sa correction n'en faisait pas partie. La transition rouge -> vert est consignee **ici**, dans ce SUMMARY, avec ses deux sorties reelles ; la verification de phase doit lire cette section avant de conclure a un rouge residuel.
- **La deviation de ce plan n'a pas pu etre inscrite au registre des fenetres cassees** : `gsd-tools windows append --kind deviation ...` refuse d'ecrire (`windows_ledger_table_drift` — la ligne 5 du tableau rendu de `.planning/WINDOWS.md` diverge de l'entree JSON de la phase 3, qui est la source de verite, et l'outil interdit de corriger le tableau a la main). L'ecart est **anterieur** a ce plan (aucune entree de phase 4 n'a ete ajoutee par 04-01, 04-02 ni 04-04) et ne releve pas de la correction du fichier juge : la deviation reste donc consignee ici, dans la section *Deviations from Plan*, et le registre porte toujours ses 6 entrees ouvertes. `windows status` rend `open_count: 6`, `last_updated: 2026-09-11T13:37:27.213Z` — inchange par ce plan.
- **L'estimate du plan (74 000 tokens) surestime largement le travail realise** (mesure : 8 162 tokens sur la meme echelle, chars/4 du diff). L'ecart est consigne tel quel dans `actuals` : il calibre les prochains estimates, il n'est pas lisse.

## Le vert observe, verbatim

La suite complete, avant et apres la correction du fichier livre (commandes et sorties reelles) :

```
$ ./.venv/Scripts/python.exe -m pytest -q          # AVANT (etat rouge du plan 04-04)
1 failed, 200 passed in 3.78s
# l'echec unique : tests/test_docs_wizard.py::test_aiguillage_sans_renvoi_obsolete
#   ... renvoi obsolete (a) : la ligne « Tapez `3` puis **Entrée** pour ouvrir l'optimisation. » invite a taper `3` ...
#   ... renvoi obsolete (b) : la ligne « Exemple : pour **interdire les armes à distance**, tapez `F7` ... » ...
#   ... renvoi obsolete (c) : la ligne « Vous arrivez **directement** dans le wizard (...) » ...

$ ./.venv/Scripts/python.exe -m pytest -q          # APRES (tache 2 committee)
203 passed in 3.51s

$ ./.venv/Scripts/python.exe -m pytest tests/test_docs_wizard.py -k "aiguillage_sans_renvoi_obsolete or copie_figee_signalee" -v
tests/test_docs_wizard.py::test_copie_figee_signalee_par_le_detecteur PASSED [ 50%]
tests/test_docs_wizard.py::test_aiguillage_sans_renvoi_obsolete PASSED   [100%]
2 passed, 14 deselected in 0.11s

$ git diff --quiet -- tests/fixtures/guide-wizard-obsolete.md && echo "copie figee inchangee"
tests/fixtures/guide-wizard-obsolete.md inchange (git diff --quiet vrai)

$ ./.venv/Scripts/python.exe -m pytest tests/test_docs_parcours.py -q     # module de la phase 3
18 passed in 0.71s
```

Les huit morsures, verbatim (chacune sur une copie **verte** avant mutation) :

```
mutation detectee (aiguillage_sans_lien), motif "aiguillage sans lien vers la page"
mutation detectee (renvoi_direct_reintroduit), motif "renvoi obsolete (c)"
mutation detectee (readme_revert), motif "renvoi produit vers un fichier non indexe"
mutation detectee (aiguillage_bruyant), motif "aiguillage qui decrit encore le wizard"
morsures 04-03 tache 1 : 4/4 detectees (copie verte avant chaque mutation)

mutation detectee (lien_d63_retire), motif "renvoi en prose sans lien"
mutation detectee (pages_inexistantes_non_reduite), motif "page declaree inexistante alors qu'elle existe"
mutation detectee (lien_mort_dans_aiguillage), motif "lien vers une page inexistante"
mutation detectee (lien_non_declare), motif "lien non declare"
morsures 04-03 tache 2 : 4/4 detectees (copie verte avant chaque mutation)

$ git log -1 --name-only  -> controle de commit de la tache 2
lien D-63 et reduction de la reserve dans le meme commit : eeaa93f
```

La preuve que la correction n'a touche aucun predicat du detecteur :

```
$ git show --numstat --format="%h %s" ba11149
ba11149 feat(04-03): aiguillage corrige, README debarrasse de son pointeur produit et vert du critere 5
9	321	GUIDE_WIZARD.md
0	2	README.md
171	0	tests/test_docs_wizard.py        # <- 0 ligne retiree : detecteur et assertions intacts
```

## Known Stubs

Aucun. Les cinq fichiers livres ne portent ni valeur vide qui remonterait a l'affichage, ni texte de remplacement, ni `TODO`/`FIXME`, ni test saute : la ligne 1 de l'aiguillage est son `H1`, la reserve de pages inexistantes est reduite a la seule page qui n'existe pas (`base-locale.md`, dette restante **visible**), et aucun controle n'a ete desactive ou assoupli.

## User Setup Required

None — no external service configuration required. Le plan travaille en mode hors ligne : aucune dependance ajoutee (`pyproject.toml` inchange), aucun serveur lance, aucun socket ouvert, aucun reseau, rien d'ecrit sous `.data/` ni sous `.doc-agent/`, et aucune commande destructrice (aucun `db clear`) n'est executee ni presentee comme une etape.

## Next Phase Readiness

- **La phase 4 est complete cote contenu** : les cinq criteres de succes du ROADMAP sont satisfaits, les quatre plans sont resumes, et la suite entiere est **verte** (`203 passed`).
- **Le critere 5 est vert par correction, et sa morsure est intacte** : `test_aiguillage_sans_renvoi_obsolete` passe sur le fichier livre, `test_copie_figee_signalee_par_le_detecteur` exige toujours ses trois constats sur la copie figee, et les huit morsures de ce plan sont relancables telles quelles (aucune n'ecrit dans l'arbre de travail).
- **Contrat pose pour la verification de phase** : lire la docstring du module de 04-04 comme l'enregistrement de sa fenetre rouge, et la transition dans ce SUMMARY (§ *Le vert observe, verbatim*) avant de conclure ; re-mesurer `.data/dofus.sqlite3` autour de la suite entiere ; et rejouer les deux batteries de morsures si le vert est mis en doute.
- **Limite nommee, non un blocage** : le detecteur couvre **trois** formes nommees et ne revendique aucune exhaustivite (D-58/D-26) ; la prose libre des fichiers de la racine (le `H1`, l'avis de deplacement) n'est pas verifiee, ce que le docstring du nouveau test ecrit noir sur blanc. Aucune action humaine n'est requise par ce plan, aucun secret, aucun reseau, aucune publication.

## Self-Check: PASSED

- `GUIDE_WIZARD.md` : FOUND (18 lignes, 18/18 CRLF, sans BOM)
- `README.md` : FOUND (aucune occurrence de `GUIDE_WIZARD`, un seul lien vers `docs/sommaire.md`)
- `tests/test_docs_wizard.py` : FOUND (16 tests)
- `docs/parcours-simplifie.md` : FOUND (deux liens vers `wizard-avance.md`, ligne 140 intacte)
- `tests/test_docs_parcours.py` : FOUND (18 tests, reserve reduite)
- Commit `ba11149` : FOUND
- Commit `eeaa93f` : FOUND
- Suite complete : `203 passed` ; `.data/dofus.sqlite3` : empreinte identique

---

*Phase: 04-wizard-avanc-et-r-sorption-de-la-dette-guide-wizard*
*Completed: 2026-09-11*
