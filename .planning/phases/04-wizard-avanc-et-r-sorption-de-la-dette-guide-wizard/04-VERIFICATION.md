---
phase: 04-wizard-avanc-et-r-sorption-de-la-dette-guide-wizard
verified: 2026-09-11T19:45:14Z
status: passed
score: 19/19 must-haves verified (0 present-behavior-unverified, 0 override, 0 gap)
covered_files:
  - .planning/REQUIREMENTS.md
  - .planning/phases/04-wizard-avanc-et-r-sorption-de-la-dette-guide-wizard/04-01-PLAN.md
  - .planning/phases/04-wizard-avanc-et-r-sorption-de-la-dette-guide-wizard/04-01-SUMMARY.md
  - .planning/phases/04-wizard-avanc-et-r-sorption-de-la-dette-guide-wizard/04-02-PLAN.md
  - .planning/phases/04-wizard-avanc-et-r-sorption-de-la-dette-guide-wizard/04-02-SUMMARY.md
  - .planning/phases/04-wizard-avanc-et-r-sorption-de-la-dette-guide-wizard/04-03-PLAN.md
  - .planning/phases/04-wizard-avanc-et-r-sorption-de-la-dette-guide-wizard/04-03-SUMMARY.md
  - .planning/phases/04-wizard-avanc-et-r-sorption-de-la-dette-guide-wizard/04-04-PLAN.md
  - .planning/phases/04-wizard-avanc-et-r-sorption-de-la-dette-guide-wizard/04-04-SUMMARY.md
  - .planning/phases/04-wizard-avanc-et-r-sorption-de-la-dette-guide-wizard/04-GAP-SUMMARY.md
  - .planning/phases/04-wizard-avanc-et-r-sorption-de-la-dette-guide-wizard/04-REVIEW.md
  - GUIDE_WIZARD.md
  - README.md
  - docs/parcours-simplifie.md
  - docs/sommaire.md
  - docs/wizard-avance.md
  - tests/fixtures/guide-wizard-obsolete.md
  - tests/test_docs_parcours.py
  - tests/test_docs_wizard.py
covered_digest: "v1:sha256:d70c70179cdaeaa658830e4f53958c8ec4b0284dafeb441316cf526dcb034115"
behavior_unverified: 0
overrides_applied: 0
coincidental_reliance_items:
  - truth: "La page docs/wizard-avance.md est conforme de bout en bout : un seul H1 egal au libelle d'index, neuf sections de niveau 2 dans l'ordre, le bloc « Source de verite », la ligne de retour, aucun lien externe, aucun bloc de commandes, UTF-8 sans BOM et fins de ligne CRLF sur toutes les lignes"
    reason: undeclared-precondition
    harden: "Le controle `if retours != fins` (tests/test_docs_wizard.py:1826-1831) exige le CRLF exact sur les octets de l'arbre de travail. Or `git ls-files --eol docs/wizard-avance.md` repond `i/lf w/crlf attr/` (aucun `.gitattributes`, `core.autocrlf=true` local) : sur un clone ou `core.autocrlf` vaut `false`/`input`, la meme page versionnee arrive en LF et la suite rougit pour une raison qui n'appartient pas au fichier. C'est la meme conclusion que celle deja inscrite dans 03-VERIFICATION.md pour l'assertion jumelle, et `.claude/CLAUDE.md` l'interdit explicitement (« ne pas asserter sur les octets de fin de ligne », HIGH). Le durcissement attendu : garder le BOM et exiger des fins de ligne **homogenes** (`if retours not in (0, fins)`), ce qui garde la morsure sur le vrai piege (fins melangees) sans dependre d'un reglage git local."
prohibitions:
  declared: 22
  structured_tiers_declared: 0
  note: "Les quatre plans declarent 22 prohibitions en texte libre (aucun champ `status`/`verification`, donc aucun palier test/jugement a router). Je les ai verifiees une par une comme des controles negatifs mesurables ; le detail et les preuves sont en section « Prohibitions » du corps du rapport. Aucune n'est un palier `test` non arme — la notion de palier n'est pas declaree par cette phase — et aucune n'est violee par le livrable."
---

# Phase 4 : Wizard avancé et résorption de la dette `GUIDE_WIZARD` — Rapport de vérification

**Objectif de phase** (verbatim, `.planning/ROADMAP.md`) : « Le flux avancé est décrit dans une source unique alignée sur le code, et `GUIDE_WIZARD.md` ne contredit plus le produit. »
**Vérifié le :** 2026-09-11T19:45:14Z
**Statut :** `passed`
**Re-vérification :** non — vérification initiale (Step 0 : aucun `*-VERIFICATION.md` antérieur dans le dossier de phase)

## Verdict

Les **cinq critères de succès du ROADMAP** sont **atteints et démontrés par le rendu réel**, pas par la prose des SUMMARY. Les 19 must-haves retenus (les 5 critères du ROADMAP fusionnés avec les vérités distinctes des quatre plans, dédupliquées) sont vérifiés : **0 gap, 0 présent-mais-comportement-non-exercé, 0 override**.

Ce que je n'ai pas lu mais **re-mesuré moi-même**, en processus, hors ligne, sans `main()`, sans POST `GO` volontaire, sans écriture sous `.data/` :

1. **Le critère 5 est rouge puis vert, et je l'ai re-dérivé sur une copie hors dépôt.** `git archive` des trois états vers `/tmp` (aucun fichier suivi modifié, aucune branche créée) : à `d841500` (fin de la vague 3, aiguillage encore obsolète) la suite donne **`1 failed, 198 passed, 2 skipped`**, l'échec étant **nommément** `tests/test_docs_wizard.py::test_aiguillage_sans_renvoi_obsolete`, avec les **trois formes nommées** dans le message (menu `3`/`4`, `F7` présenté comme armes distance, arrivée « directement ») ; à `1b0a17a` (fin de la vague 4) **`201 passed, 2 skipped`**, à `fd3b2dd` **`203 passed, 2 skipped`**, et dans le dépôt **`205 passed`**. Le détecteur est **inchangé depuis `4ebc5c9`** (`git diff 4ebc5c9 HEAD -- tests/test_docs_wizard.py` ne touche ni `renvois_obsoletes`, ni `_faits_du_rendu`, ni les trois prédicats) : la mesure porte donc bien sur le détecteur livré.
2. **Les deux constats critiques de `04-REVIEW.md` sont réellement clos.** CR-01 : les cinq lignes de l'arborescence de `GUIDE_WIZARD.md` sont **égales au rendu** de `GET /` (`1. RECHERCHE D'OBJETS`, `2. LISTE DES EQUIPEMENTS`, `3. LISTE DES PANOPLIES`, `4. OPTIMISATION DE STUFF`, `5. SYSTEME`) et le contrôle d'égalité **mord** sur les six mutations que j'ai construites, y compris les deux formes abrégées que le détecteur, par tolérance voulue, laisse passer. CR-02 : la phrase de `docs/parcours-simplifie.md:~140` dit la vérité **par étape**, et l'ancre renforcée **mord** (2 constats sur la phrase d'avant le gap, 0 sur la phrase livrée) — mesure faite sur des copies en mémoire, jamais sur le fichier du dépôt.
3. **La suite n'a été ni affaiblie ni contournée.** `tests/test_docs_wizard.py` : **+2721 / −0** (ajouts seuls). `tests/test_docs_parcours.py` : **0 assertion retirée** (19 → **20** assertions), les 10 lignes retirées sont un renommage de constante à valeur identique, la reformulation d'un message d'échec et la réduction de `PAGES_INEXISTANTES` ; aucun `pytest.skip`/`xfail`/`mark` ajouté à part le **saut déclaré** de la mesure d'empreinte, qui **ne se déclenche pas** dans le dépôt (`0 skipped`).

**Ce qui n'est pas vert, et pourquoi ce n'est pas un gap :** cinq avertissements de revue restent ouverts et **nommés** (WR-01 à WR-05), plus quatre informations (IN-01 à IN-04). Je les ai tous re-mesurés ; **aucun n'invalide un critère de succès** et aucun n'est un marqueur de dette (`TBD`/`FIXME`/`XXX`) : zéro marqueur dans les huit fichiers de la phase. En revanche deux d'entre eux sont de **vraies imperfections du livrable** (et non de simples fragilités de harnais) : la règle des refus de l'écran `slots` de `docs/wizard-avance.md` (WR-01, contre-exemple mesuré : `12` → `SLOT INVALIDE`, message jamais cité par la page) et le fait produit du repli `POIDS : (aucun — defaut INT)`, rendu par le récapitulatif mais atteignable par aucune page (WR-05). Je les reporte comme avertissements avec leur remède d'une ligne, **sans** les transformer en gap : les critères 1 à 3 énumèrent les libellés, les formats, la syntaxe et les commandes, et tous ces points-là sont exacts au rendu (le détail du raisonnement est en section « Avertissements ouverts — jugement »).

## Goal Achievement

### Observable Truths

| # | Vérité (source) | Statut | Preuve |
| --- | --- | --- | --- |
| T1 | SC1 — les 9 étapes sont citées dans l'ordre exact du code avec leurs titres réellement rendus | ✓ VERIFIED | `WIZARD_STEPS` rendu écran par écran : `OPT-W1 SLOTS ET FILTRES`, `W2 OPTIONS SOLVEUR`, `W3 CARACTERISTIQUES`, `W4 PA / PM / PO`, `W5 RESISTANCES`, `W6 DOMMAGES`, `W7 DIVERS`, `W8 ITEMS INTERDITS / FORCES`, `W9 RECAPITULATIF` ; la page cite les neuf, dans cet ordre (`## Les 9 étapes du wizard`, l. 33-45) |
| T2 | SC1 — les 11 emplacements et les 10 filtres sont cités avec **leur propre numéro**, dont `F6` = `ARMES DISTANCE` et `F7` = `ARMES MELEE` | ✓ VERIFIED | Rendu des deux pages de `/optimize/wizard/slots` : `1. AMULETTE … 11. PRYSMARADITE`, `F1. FAMILIER … F10. PRYSMARADITE`, avec `F6. [ON ] ARMES DISTANCE` et `F7. [ON ] ARMES MELEE` ; la table de la page (l. 55-88) égale ces couples au libellé près ; seconde source corroborée : `TYPE_FILTER_KEYS[5]`/`[6]` |
| T3 | SC1 — les 11 options de `OPTIONS SOLVEUR` sont citées et **dérivées du rendu** (jamais d'une table locale) | ✓ VERIFIED | Corps rendu : `1. NIVEAU`, `2. JET`, `3. DUREE (S)`, `4. SEED`, `5. TOP-K`, `6. CP-SAT`, `7. STOP SI CIBLES`, `8. AUTO POINTS`, `9. ALLOW POWER`, `10. ALLOW DOMMAGES`, `11. ALLOW DOM CRIT` — ensemble égal à celui de la page (l. 96-108) |
| T4 | SC2 — les deux formats d'édition des quatre nombres ne sont **jamais fusionnés** et sont ceux du code | ✓ VERIFIED | Sous-écran `OPT-WED` ligne 4 de `CARACTERISTIQUES` → `FORMAT : BASE POINTS CIBLE POIDS` ; ligne 1 de `PA / PM / PO` → `FORMAT : BASE EXO CIBLE POIDS` ; les deux formes sont citées séparément (l. 130-135) ; les refus de quantité portent bien le message de la forme de l'écran (mesuré : `300 0 0` → `FORMAT : BASE POINTS CIBLE POIDS`, `6 0 11` → `FORMAT : BASE EXO CIBLE POIDS`) |
| T5 | SC2 — la syntaxe d'items est citée telle que le code l'applique : `+ID` = interdit (et **pas** un refus), `-ID` = forcé, `!ID` = retiré, `CLEAR`/`clear` = vider, un identifiant sans préfixe refusé | ✓ VERIFIED | Corps rendu : `+ID AJOUTER INTERDIT`, `-ID AJOUTER FORCE`, `!ID RETIRER (BAN OU FORCE)`, `CLEAR VIDER LISTES` ; mesuré : `+12345` → `LISTE ITEMS MISE A JOUR`, `-12345` déplace l'objet (`INTERDITS (0)` / `FORCES (1)`), `!12345` vide les deux, `clear` accepté, `12345` → `SYNTAXE : +ID | -ID | !ID | CLEAR` (message exact du code), espaces autour acceptés ; état vide `(aucun)` dans **les deux** états (client neuf **et** après `CLEAR`) ; troncature `… +2` au-delà de 8 entrées |
| T6 | SC3 — les couples touche/libellé sont cités **par étape**, extrémités comprises | ✓ VERIFIED | Mesure des neuf barres : `1. slots` = `F7=Page prec`, `F8=Suivant` ; `2..8` = `F7=Precedent`, `F8=Suivant` ; `9. recap` = `F7=Precedent`, `F8=Page suiv` ; `ESC=Retour` sur les neuf — identiques à la table de la page (l. 172-183) |
| T7 | SC3 — les commandes du récapitulatif (`GO`, `RESET`, `SAVES`, `1`-`8`) sont citées et celles qui n'exécutent pas le solveur sont prouvées par l'action | ✓ VERIFIED | Corps du récapitulatif : `GO = LANCER  RESET = REINITIALISER  1-8 = RETOUR ECRAN` / `SAVES = STUFFS SAUVEGARDES` ; mesuré : `RESET` → `/optimize/wizard/slots` (+ `WIZARD REINITIALISE`), `SAVES`/`saves` → `/saves`, chaque chiffre `n` de `1` à `8` → `/optimize/wizard/WIZARD_STEPS[n-1]` (8/8 conformes), `9`/`XYZ` → refus avec la liste `GO \| RESET \| SAVES \| 1-8` rendue ; `GO` **jamais posté par le harnais** (garde `ast` sur `cmd` insensible à la casse) |
| T8 | SC4 — `GUIDE_WIZARD.md` ne décrit plus le wizard : aiguillage court (≤ 20 lignes), **arborescence de menus corrigée**, lien vers la source unique et vers le sommaire | ✓ VERIFIED | Fichier : 18 lignes, un seul `H1`, deux liens (`docs/wizard-avance.md`, `docs/sommaire.md`), aucun énoncé de contenu ; arborescence **égale au rendu** de `GET /` après normalisation ; `3. OPTIMISATION DE STUFF` et `Tapez 3 puis` **absents** de `README.md`, `GUIDE_WIZARD.md` et `docs/**` (exigence littérale de `.claude/CLAUDE.md` § 4.2, vérifiée) |
| T9 | SC4 — `README.md` ne renvoie plus vers `GUIDE_WIZARD.md` pour l'usage produit | ✓ VERIFIED | `git diff c2afc42 HEAD -- README.md` = exactement **−2 lignes** (la ligne « Guide détaillé » et sa ligne vide), **sans texte de remplacement** ; `grep GUIDE_WIZARD README.md` → aucune occurrence ; un seul lien vers `docs/sommaire.md` (l. 7), exigé par le contrôle |
| T10 | SC5 — le contrôle des renvois obsolètes est observé **rouge** sur l'état antérieur (trois formes) **puis vert** après correction, dans la même phase | ✓ VERIFIED | Re-mesuré sur copies hors dépôt : `d841500` → `1 failed, 198 passed, 2 skipped`, échec = `test_aiguillage_sans_renvoi_obsolete`, message portant les 3 formes ; détecteur appliqué au texte `c2afc42:GUIDE_WIZARD.md` → **8 constats** (formes a/a/a/a/a/a, b, c) ; fichier livré → **0 constat** ; `1b0a17a` → `201 passed, 2 skipped` ; dépôt → `205 passed` |
| T11 | 04-01/04-02 — le chemin d'arrivée réel est mesuré et cité : menu `4` → `/optimize` → les trois questions → `AVANCE` → **récapitulatif** ; les identifiants d'écrans `OPT-W1`…`OPT-W9` / `OPT-WED` sont cités ; un écran inconnu rend `ECRAN WIZARD INCONNU` | ✓ VERIFIED | Chaîne rejouée pas à pas : `POST / selection=4` → `/optimize` ; `GET /optimize` → `/optimize/quick/classe` ; les deux réponses → `/optimize/quick/elements` → `/optimize/quick/niveau` → `POST … AVANCE` (et `avance`) → `/optimize/wizard/recap` ; en-têtes mesurés `OPT-W1`…`OPT-W9` ; `GET /optimize/wizard/inconnu` → 302 `/` puis statut `ECRAN WIZARD INCONNU` sur l'écran du menu ; la page dit ce chemin (l. 7-21) |
| T12 | 04-01/04-02 — l'exemple guidé migré est réancré au rendu : les trois éditions sont rejouées et les lignes rendues sont citées | ✓ VERIFIED | Rejoué sur clients neufs : option `1` + `123` → `VALEUR ENREGISTREE` puis `1. NIVEAU          = 123` ; `CARACTERISTIQUES` ligne `4` + `300 0 0 1` → `CARAC ENREGISTREE` puis `4. Intelligence       B=300 P=0 C=0 W=1` ; `PA / PM / PO` ligne `1` + `6 0 11 5` → `1. PA                 B=6 E=0 C=11 W=5` ; les trois lignes sont citées par la page (l. 200-214), la variante « cible PA » survit (le code porte `with_exo`), la justification « 200 + 100 parchemins » est présentée comme un **choix du lecteur** |
| T13 | 04-01 — la page tient sa forme de bout en bout (H1 unique = libellé d'index, 9 sections dans l'ordre, bloc « Source de vérité » dont chaque chemin existe, ligne de retour, aucun lien externe, aucun bloc de commandes, UTF-8 sans BOM, CRLF) | ✓ VERIFIED (coincidental-reliance) | `H1 = # Wizard avancé` = libellé d'index ; 9 sections dans l'ordre attendu ; les 5 chemins du bloc « Source de vérité » existent sur disque (vérifié un par un) ; dernière ligne non vide `[Retour au sommaire](sommaire.md)` ; aucun `console`, aucun lien externe ; 16554 octets, aucun BOM. **La partie CRLF est un vert coïncident** (voir `coincidental_reliance_items`) |
| T14 | 04-01 — `docs/sommaire.md` croît d'**exactement une** cible et les gardes de structure restent vertes sans exception | ✓ VERIFIED | `git diff` : **+1** ligne (la ligne `\| [Wizard avancé](wizard-avance.md) \|`) ; les 14 tests de `tests/test_docs_structure.py` (exhaustivité bidirectionnelle, H1, retour, encodage, liens) sont verts, et le module de la phase 3 ne se dégrade pas |
| T15 | 04-02 — D-64 : l'affirmation de `docs/parcours-simplifie.md` (~l. 140) reste **vraie** après cette phase | ✓ VERIFIED | Phrase livrée : « … le wizard avancé, qui n'est pas décrit ici, affiche `Precedent` et `Suivant` **sur ses écrans intermédiaires, et `Page prec` / `Page suiv` à ses deux extrémités** » — conforme aux neuf barres mesurées ; l'ancre `_constats_touches_wizard` rend 0 constat sur le texte livré et **2 constats** sur la phrase d'avant le gap (mesure en mémoire) |
| T16 | 04-02 — l'empreinte de `.data/dofus.sqlite3` (taille, `mtime_ns`, SHA-256) est identique autour des rendus, ou saut **explicite** si la base est absente | ✓ VERIFIED | Dans le dépôt : `205 passed, 0 skipped` (le saut ne se déclenche pas) ; `mtime` de `.data/dofus.sqlite3` inchangé (2026-09-06 23:27:36) avant et après mes trois exécutions ; sur les copies archivées (sans `.data/`) les deux mesures sautent **en nommant la raison** (`base locale absente : la mesure d'empreinte n'a pas d'objet`) — mesuré, pas supposé |
| T17 | 04-03 — la dette D-44 est levée : les deux renvois en prose deviennent de vrais liens, la réserve perd son entrée, et la réserve **ne peut plus mentir** | ✓ VERIFIED | `docs/parcours-simplifie.md` l. 5 et l. 256 portent `[wizard avancé](wizard-avance.md)` ; `PAGES_INEXISTANTES = ("base-locale.md",)` ; l'invariant 2 de `test_lien_wizard_avance_legitime` refuse toute entrée de la réserve qui existerait sur disque ; l'invariant 3/4 exige que chaque cible de lien de `GUIDE_WIZARD.md` vers `docs/` soit **déclarée et existante** ; les phrases de `RENVOIS_SANS_LIEN` (`base-locale.md` inexistante) restent présentes |
| T18 | 04-04 — la copie figée est signalée par le **même** détecteur (trois formes, au moins trois constats) et les renvois **légitimes ne sont pas signalés** | ✓ VERIFIED | `tests/fixtures/guide-wizard-obsolete.md` → constats des trois formes (dont un nommant le libellé rendu du menu de l'optimisation et un nommant `ARMES MELEE` pour `F7`) ; les quatre témoins `TEMOINS_LEGITIMES` rendent **0 constat** chacun (mesuré) ; la copie s'annonce dans son en-tête comme pièce de test et n'est citée par aucune page de `docs/` |
| T19 | 04-04 — la fenêtre rouge est **bornée** : sélectionné par son nom, un seul test échoue et c'est `test_aiguillage_sans_renvoi_obsolete` | ✓ VERIFIED | Copie archivée de `d841500` : `1 failed, 198 passed, 2 skipped` — le résumé pytest nomme ce seul test, aucun autre échec, l'échec étant une assertion sur `GUIDE_WIZARD.md` (le fichier livré, pas la copie figée) |

**Score :** 19/19 vérités vérifiées (0 présent-comportement-non-exercé, 0 override, 1 vert coïncident déclaré)

### Deferred Items

Aucun. Je n'ai reporté aucun item vers une phase ultérieure : les cinq critères de la phase 4 sont tenus, et les avertissements ouverts (WR-01, WR-05) ne sont **pas** couverts par le périmètre annoncé des phases 5 et 6 du `ROADMAP.md` (base locale / hors-ligne ; dépannage, glossaire, complétude et preuve finale). Les reporter « par défaut » ferait dire au roadmap plus qu'il ne dit — c'est pourquoi ils sont consignés en avertissements, avec leur remède, et non en `deferred`.

### Required Artifacts

| Artefact | Attendu | Statut | Détail (existence → substance → câblage) |
| --- | --- | --- | --- |
| `docs/wizard-avance.md` | page unique du flux avancé (≥ 130 puis ≥ 180 lignes) | ✓ VERIFIED | 224 lignes (UTF-8 sans BOM), 9 sections épinglées dans l'ordre, les 11 emplacements, les 10 filtres, les 11 options, les deux formats, la syntaxe d'items, la table de touches par étape, l'exemple guidé, le bloc « Source de vérité » → **câblée** : indexée au sommaire, liée par `GUIDE_WIZARD.md` et par `docs/parcours-simplifie.md` (×2), contrôlée par 18 tests |
| `docs/sommaire.md` | +1 ligne d'index | ✓ VERIFIED | 22 lignes ; la ligne `\| [Wizard avancé](wizard-avance.md) \| … \|` est présente dans la table `## Index` ; la liste « Parcours conseillé » n'a **pas** gagné de lien markdown → **câblée** : le contrôle bidirectionnel de structure est vert |
| `tests/test_docs_wizard.py` | module d'ancrage (≥ 240 → 380 → 470 → 500 lignes) | ✓ VERIFIED | 2721 lignes (+2721/−0) ; 18 tests verts ; contient `def renvois_obsoletes`, `test_page_et_index_du_wizard`, `test_touches_et_commandes_par_etape`, `test_aiguillage_et_readme`, la garde `ast` de clôture, la garde d'empreinte → **câblé** : `pytest -q` le collecte et le fait passer |
| `tests/test_docs_parcours.py` | renvoi légitime + réserve réduite (≥ 2740 lignes) | ✓ VERIFIED | 2990 lignes, 18 tests verts ; contient `test_lien_wizard_avance_legitime` ; assertions 19 → 20, **0 retirée** → **câblé** : couvre les deux renvois de la page et les cibles de l'aiguillage |
| `GUIDE_WIZARD.md` | aiguillage (≥ 8 lignes, ≤ 20) | ✓ VERIFIED | 18 lignes, −321/+9 ; un seul `H1`, deux liens dont les cibles existent, arborescence égale au rendu ; contient `docs/wizard-avance.md` → **câblé** : `test_aiguillage_et_readme`, `test_aiguillage_sans_renvoi_obsolete`, `test_arborescence_de_l_aiguillage_egale_le_menu_rendu` et `test_lien_wizard_avance_legitime` le lisent et sont verts |
| `README.md` | sans la ligne « Guide détaillé » (≥ 60 lignes) | ✓ VERIFIED | 123 lignes, 2 lignes retirées ; contient `docs/sommaire.md` une seule fois → **câblé** : `test_aiguillage_et_readme` exige l'absence de tout renvoi produit et l'unicité du lien vers le sommaire |
| `docs/parcours-simplifie.md` | deux renvois devenus des liens (≥ 260 lignes) | ✓ VERIFIED | 269 lignes, +3/−3 (les deux renvois, plus la phrase CR-02) ; contient `](wizard-avance.md)` ×2 → **câblé** : `test_lien_wizard_avance_legitime` et `test_pagination_et_emplacement_du_calcul` |
| `tests/fixtures/guide-wizard-obsolete.md` | copie figée signalée (≥ 18 lignes) | ✓ VERIFIED | 39 lignes, +39/−0 ; contient `OPTIMISATION DE STUFF` et les trois formes → **câblé** : `_lire_fixture` la lit en UTF-8 explicite et `test_copie_figee_signalee_par_le_detecteur` exige les trois constats |

Aucun artefact n'est MISSING, STUB, ORPHANED ni HOLLOW.

### Key Link Verification

| From | To | Via | Statut | Détail |
| --- | --- | --- | --- | --- |
| `tests/test_docs_wizard.py` | `dofus_stuff/web/optimize_wizard.py` | `WIZARD_STEPS`, `STEP_TITLES`, `TYPE_FILTER_LABELS` | ✓ WIRED | importés en tête du module (jamais recopiés) ; la permutation de deux valeurs de `TYPE_FILTER_LABELS` ou de deux entrées de `WIZARD_STEPS` est mesurée comme mordante par les plans (et le contrôle lit le rendu, pas la table) |
| `tests/test_docs_wizard.py` | `dofus_stuff/model/solver_spec.py` | `TYPE_FILTER_KEYS[5]`/`[6]`, `SLOT_GROUPS` | ✓ WIRED | importés ; seconde source du couple `F6`/`F7` et de l'ordre des 11 emplacements ; mesuré cohérent avec le rendu |
| `tests/test_docs_wizard.py` | `dofus_stuff/web/templates/screen.html` | marqueurs `id="body">`, `class="row status`, `row header` | ✓ WIRED | les trois marqueurs existent au gabarit (l. 24, 31, 49) et sont effectivement trouvés dans le rendu (les 18 tests l'exigent) |
| `tests/test_docs_wizard.py` | `tests/fixtures/guide-wizard-obsolete.md` | `_lire_fixture` | ✓ WIRED | lecture en UTF-8 explicite ; 3 constats rendus (mesuré) |
| `tests/test_docs_wizard.py` | `.data/dofus.sqlite3` | empreinte (taille, `mtime_ns`, SHA-256) **sans écriture** | ✓ WIRED | identique avant/après ; `mtime` 2026-09-06 23:27:36 conservé autour de mes exécutions ; saut déclaré si absente |
| `docs/wizard-avance.md` | `docs/sommaire.md` | ligne d'index + `[Retour au sommaire]` | ✓ WIRED | les deux présentes ; le contrôle bidirectionnel de structure est vert |
| `GUIDE_WIZARD.md` | `docs/wizard-avance.md` + `docs/sommaire.md` | les deux liens de navigation | ✓ WIRED | cibles existantes et **déclarées** dans `LIENS_LEGITIMES_VERS_L_AIGUILLAGE` (invariants 3 et 4) |
| `docs/parcours-simplifie.md` | `docs/wizard-avance.md` | deux renvois en prose convertis | ✓ WIRED | `](wizard-avance.md)` aux lignes 5 et 256, mesuré intact après le gap |
| `GUIDE_WIZARD.md` | `dofus_stuff/web/routes.py` | arborescence lue au **corps rendu** du menu | ✓ WIRED | égalité mesurée contre `GET /` ; le contrôle d'égalité mord sur 6 mutations sur 6 |

### Data-Flow Trace (Level 4)

Cette phase ne rend aucune donnée dynamique : la chaîne à tracer est « **valeur citée par la page ← valeur rendue ← producteur de code** », et non « donnée ← requête ».

| Valeur citée | Source réelle (mesurée) | Producteur | Donnée réelle | Statut |
| --- | --- | --- | --- | --- |
| les 9 titres d'étapes | en-tête des neuf écrans | `dofus_stuff/web/optimize_wizard.py` (`STEP_TITLES`) via `routes.py` | oui (9/9 recontrôlés) | ✓ FLOWING |
| les 11 emplacements + 10 filtres | corps de `/optimize/wizard/slots` (pages 1 et 2) | `SLOT_GROUP_LABELS` / `TYPE_FILTER_LABELS` sur l'ordre de `SLOT_GROUPS` / `TYPE_FILTER_KEYS` | oui (21/21) | ✓ FLOWING |
| les 11 options | corps de `/optimize/wizard/options` | lignes littérales de `body_options` | oui (11/11) | ✓ FLOWING |
| les messages de refus (slots, options, items, édition) | ligne de statut du rendu | `apply_slots_input` / `apply_options_input` / `apply_items_input` / `apply_stat_edit` | oui (postés et lus) | ✓ FLOWING |
| les couples touche/libellé | barre de touches des neuf écrans | `_wizard_fkeys` + `routes.py:138-139` | oui (9/9) | ✓ FLOWING |
| les commandes du récapitulatif | corps + ligne de statut du récapitulatif | `body_recap` + routeur | oui (libellés cités, `RESET`/`SAVES`/`1`-`8` prouvés par la redirection) | ✓ FLOWING |
| l'arborescence de `GUIDE_WIZARD.md` | corps du menu `GET /` | `routes.py` (fonction `menu`) | oui (5/5, égalité) | ✓ FLOWING |
| la vérité des touches de `docs/parcours-simplifie.md` | barres `slots` et `recap` | `routes.py:138-139` | oui (deux extrémités mesurées) | ✓ FLOWING |

### Behavioral Spot-Checks

| Comportement | Commande | Résultat | Statut |
| --- | --- | --- | --- |
| la suite du dépôt est verte | `./.venv/Scripts/python.exe -m pytest -q` | `205 passed in 3.55s` (0 failed, 0 skipped) | ✓ PASS |
| le rouge du critère 5 est réel et borné | `git archive d841500 \| tar -x -C /tmp/… && pytest -q` | `1 failed, 198 passed, 2 skipped` ; échec nommé `test_aiguillage_sans_renvoi_obsolete` ; les 3 formes dans le message | ✓ PASS |
| le vert du critère 5 (fin de vague 4) | `git archive 1b0a17a … && pytest -q` | `201 passed, 2 skipped` (les 2 sauts sont les mesures d'empreinte, base absente de l'archive) | ✓ PASS |
| le vert après le gap | `git archive fd3b2dd … && pytest -q` | `203 passed, 2 skipped` | ✓ PASS |
| le détecteur signale l'état antérieur | `renvois_obsoletes(texte de c2afc42:GUIDE_WIZARD.md, faits mesurés)` | `8 constats` : 6× forme (a) (dont `3. OPTIMISATION DE STUFF`, `4. SYSTEME` ×3, `4. GESTION DE LA BASE`), 1× (b) (`F7` = armes à distance), 1× (c) (arrivée « directement ») | ✓ PASS |
| le détecteur est muet sur le fichier livré | `renvois_obsoletes(GUIDE_WIZARD.md, faits)` | `0 constat` | ✓ PASS |
| les renvois légitimes ne sont pas signalés | les 4 témoins de `TEMOINS_LEGITIMES` | `0 constat` chacun | ✓ PASS |
| le contrôle d'égalité de l'arborescence mord | 6 mutations sur copie en mémoire (`3. PANOPLIES`, `4. OPTIMISATION`, `5. SYSTEMES`, `3. LISTE DES PANOPLIE`, `2. LISTE DES EQUIPEMENTS X`, `4. OPTIMISATION DE STUF`) | `1 constat` chacune (6/6) ; `0` sur le texte livré ; `1 constat` si aucune ligne `N. LIBELLE` (non vacuité) | ✓ PASS |
| l'ancre CR-02 mord | `_constats_touches_wizard` sur la phrase d'avant le gap (mémoire) | `2 constats` (ne cite pas `Page prec`, ne cite pas `Page suiv`) ; `1 constat` si une seule extrémité est retirée ; `0` sur le texte livré | ✓ PASS |
| l'arrivée réelle est le récapitulatif | chaîne `POST /(4)` → `GET /optimize` → 3 questions → `AVANCE` | `302 /optimize` → `302 /optimize/quick/classe` → … → `302 /optimize/wizard/recap` (casse ignorée pour `AVANCE`) | ✓ PASS |
| les couples de touches par étape | rendu des 9 écrans | conformes à la table de la page, extrémités comprises | ✓ PASS |
| les formats d'édition ne sont pas fusionnés | `OPT-WED` ligne 4 de `caracs`, ligne 1 de `papmpo` | `FORMAT : BASE POINTS CIBLE POIDS` / `FORMAT : BASE EXO CIBLE POIDS` | ✓ PASS |
| la syntaxe d'items telle que le code l'applique | 7 saisies postées sur `/optimize/wizard/items` | `+12345` accepté, `-12345` déplace, `!12345` retire, `CLEAR`/`clear` vident, `12345` refusé avec le message exact, espaces tolérés, `(aucun)` dans les deux états | ✓ PASS |
| l'empreinte de `.data/` est stable | `mtime`/taille avant et après mes trois exécutions complètes | `.data/dofus.sqlite3` : 24 989 696 octets, `mtime` 2026-09-06 23:27:36, inchangé | ✓ PASS |
| aucun renvoi produit dans le README | `grep -n "GUIDE_WIZARD\|wizard-avance" README.md` | aucune occurrence | ✓ PASS |
| les exigences littérales de `.claude/CLAUDE.md` § 4.2 | `grep -rn "3\. OPTIMISATION DE STUFF" README.md GUIDE_WIZARD.md docs/` et motif `Tapez 3 puis` | absents ; `4. OPTIMISATION DE STUFF` présent (GUIDE + page), `5. SYSTEME` présent (GUIDE) | ✓ PASS |
| aucun marqueur de dette ajouté | `grep -E "TBD\|FIXME\|XXX\|TODO\|HACK\|PLACEHOLDER"` sur les 8 fichiers | 0 occurrence partout | ✓ PASS |
| aucune publication distante | `git log origin/main..HEAD` / `git branch -r --contains c2afc42` | `origin/main` figé à `1d475f9` (2026-09-07), 112 commits locaux non poussés, aucun commit de la phase sur une branche distante | ✓ PASS |

### Probe Execution

Aucune sonde n'est déclarée ni conventionnelle : `find scripts -path '*/tests/probe-*.sh'` ne rend **rien**, et aucune mention de `probe-*.sh` n'apparaît dans les quatre `04-*-PLAN.md` ni dans les SUMMARY. Les « morsures » de cette phase sont des blocs bash de `verification` (copies jetables) et, pour la partie durable, des tests pytest — dont la morsure de CR-01 vit dans `test_arborescence_abregee_signalee_par_le_controle` et celle de CR-02 dans les assertions de `tests/test_docs_parcours.py`. **Step 7c : SKIPPED (aucun fichier de sonde déclaré ou conventionnel).**

### Requirements Coverage

| Exigence | Plan source | Description | Statut | Preuve |
| --- | --- | --- | --- | --- |
| WIZ-01 | 04-01 (`requirements: [WIZ-01]`) | Un lecteur peut parcourir les étapes du wizard, éditer les formats de caractéristiques et utiliser la syntaxe d'items interdits/forcés | ✓ SATISFIED | T1, T2, T3 (parcours), T4 (les deux formats), T5 (syntaxe d'items) ; `docs/wizard-avance.md` indexée et contrôlée par 18 tests |
| WIZ-02 | 04-02 | Un lecteur connaît les commandes et les touches réellement actives du wizard | ✓ SATISFIED | T6 (touches par étape), T7 (commandes du récapitulatif, `RESET`/`SAVES`/`1`-`8` prouvés par la redirection), T11 (chemin d'arrivée et identifiants d'écrans), T12 (exemple guidé rejoué) |
| WIZ-03 | 04-03 **et** 04-04 | `GUIDE_WIZARD.md` ne contredit plus le code : contenu migré vers `docs/wizard-avance.md` comme source unique, fichier racine réduit à un aiguillage corrigé, `README.md` redirigé | ✓ SATISFIED | T8, T9 (aiguillage corrigé, README redirigé), T10, T19 (détecteur rouge → vert, rouge borné et relançable), T17 (dette D-44 levée), T18 (copie figée + témoins légitimes) |

**Exigences orphelines de la phase 4 : aucune.** `.planning/REQUIREMENTS.md` mappe exactement `WIZ-01`, `WIZ-02`, `WIZ-03` à « Phase 4 » (table de répartition, 3 exigences) et les quatre plans déclarent l'ensemble `{WIZ-01, WIZ-02, WIZ-03}` — chaque identifiant est réclamé par au moins un plan et aucun plan ne réclame d'exigence hors phase. Les 22 autres exigences du milestone appartiennent aux phases 1, 2, 3, 5 et 6 et ne sont **pas** revendiquées ici.

### Anti-Patterns Found

Aucun marqueur de dette (`TBD`/`FIXME`/`XXX`), aucun stub (le rendu est mesuré, pas simulé), aucune implémentation vide, aucun `return null` — la phase est documentaire et ses artefacts sont des pages et des contrôles. La table ci-dessous liste les constats de robustesse et d'exactitude que j'ai **re-mesurés** moi-même ; aucun n'est un bloqueur.

| Fichier | Ligne | Motif | Gravité | Impact |
| --- | --- | --- | --- | --- |
| `docs/wizard-avance.md` | 93 | Règle de refus trop générale : « une saisie qui n'est ni un numéro de `1` à `11` ni une touche `F<n>` rend `SAISIE INVALIDE` » | ⚠️ WARNING (WR-01) | **Faux pour un numéro hors liste**, mesuré : `0`, `12`, `13` → `SLOT INVALIDE`, message **jamais cité** par la page (`apply_slots_input`, `optimize_wizard.py:281-309`). Le contrôle du module ne poste que `abc` → `SAISIE INVALIDE` et `F11` → `FILTRE INVALIDE`, donc la dérive passe. N'invalide aucun critère (les critères 1-3 énumèrent libellés, formats, syntaxe et commandes) mais c'est une **imperfection réelle du livrable**. Remède : trois puces bornées (`SAISIE INVALIDE` / `SLOT INVALIDE` / `FILTRE INVALIDE`) et poster `12` et `F0` |
| `docs/wizard-avance.md` | 139 | « fait remonter le message du convertisseur **tel quel** » | ℹ️ INFO (IN-01) | Mesuré : le routeur applique `flash(str(exc).upper()[:COLS], "error")` → `COULD NOT CONVERT STRING TO FLOAT: 'A'` (capitales, tronqué). « tel quel » est inexact ; le reste de la page est rigoureux sur la casse |
| `tests/test_docs_wizard.py` | 1826-1831 | `if retours != fins` : exige le CRLF exact sur les octets de l'arbre de travail | ⚠️ WARNING (WR-02) | Vert pour une raison étrangère au fichier : `git ls-files --eol docs/wizard-avance.md` = `i/lf w/crlf attr/` (aucun `.gitattributes`, `core.autocrlf=true` **local**). Sur un clone configuré autrement, la même page versionnée rougit — et `.claude/CLAUDE.md` l'interdit (« ne pas asserter sur les octets de fin de ligne », HIGH). Même conclusion que l'advisory de `03-VERIFICATION.md` pour l'assertion jumelle ; consigné en `coincidental_reliance_items` |
| `tests/test_docs_wizard.py` | 91-101, 348-407, 826-903 | 6 helpers et 6 constantes recopiés **octet pour octet** de `tests/test_docs_parcours.py` (mesuré par comparaison `ast` : `_appels_du_module`, `_champ_saisie`, `_imports_du_module`, `_lignes_du_corps`, `_statut`, `_touches`) | ⚠️ WARNING (WR-03) | Contredit la règle écrite dans `tests/conftest.py` (« un helper dupliqué finit par diverger »). Un déplacement de marqueur du gabarit devra être corrigé deux fois ; aucun impact sur les critères |
| `tests/test_docs_wizard.py` | 354, 376 | `texte.split(MARQUEUR_CORPS, 1)[1]` / `split(MARQUEUR_STATUT, 1)[1]` : `IndexError` nu | ⚠️ WARNING (WR-04) | **Observé pendant cette vérification** : mon premier harnais a touché ce chemin et a rendu `IndexError: list index out of range` (fichier et ligne, sans nommer le marqueur ni la page), au lieu du constat localisant que D-13 impose. Solidité du harnais, hors des critères |
| `GUIDE_WIZARD.md` (état antérieur §9/§12) + `docs/wizard-avance.md` | — | Le fait produit du repli par défaut des poids n'a aucun propriétaire : le récapitulatif rend `POIDS : (aucun — defaut INT)` (mesuré) et `grep -rn "défaut INT\|défaut Intelligence\|au moins un poids" docs/ GUIDE_WIZARD.md README.md` ne rend **rien** | ⚠️ WARNING (WR-05) | Deux sections du guide supprimé n'ont pas de destination déclarée, et le seul fait vérifiable au rendu qu'elles portaient reste hors documentation. N'invalide aucun critère (aucun n'énumère ce fait) mais laisse une connaissance atteignable seulement en lisant le solveur. Remède : une phrase adossée au rendu à côté de l'étape `RECAPITULATIF` |
| `tests/test_docs_wizard.py` | 20-26, 2114-2117 | Docstring encore au présent de l'état **rouge** (« Etat attendu pendant la phase : … est **ROUGE** tant que l'aiguillage … n'a pas ete corrige (plan 04-03, vague 4) »), renvois de plan caducs | ℹ️ INFO (IN-04) | La phase est terminée et le contrôle est vert : la première chose que lit un relecteur du module décrit l'inverse de la mesure enregistrée |
| `tests/test_docs_wizard.py` | 126-128 | `MOTIF_OPTION_RENDUE` exige un `=` : le contrôle « aucun énoncé de contenu » de l'aiguillage ne mord que la forme `N. LIBELLE = VALEUR` | ℹ️ INFO (IN-02) | Une ligne de contenu réintroduite sous une autre forme (`1. NIVEAU`, `\| 1 \| NIVEAU \|`) passerait ; l'assertion annonce « sans aucun énoncé de contenu » et vérifie moins que son énoncé |
| `tests/test_docs_wizard.py` | 1324, 1336, 1475 | `if "VAL" not in texte` : cherche `VAL` n'importe où, donc satisfait par `VALEUR ENREGISTREE` cité plus haut | ℹ️ INFO (IN-03) | Contrôle vert pour la mauvaise raison (le module dispose déjà de `_cite_en_mot_entier`) |
| `tests/test_docs_wizard.py` | 275-290 | `TEMOIN_AIGUILLAGE_CORRIGE` porte encore les formes abrégées `3. PANOPLIES` / `4. OPTIMISATION` comme **témoin légitime** | ℹ️ INFO (constat de vérification, hors revue) | Le même texte est déclaré légitime par le témoin du détecteur et fautif par le contrôle d'égalité (portées différentes : jugement de prose tolérant vs arborescence livrée). Les deux contrôles passent sur l'état livré, mais un relecteur peut être trompé sur ce qui est « corrigé ». Aligner le témoin sur les libellés rendus, ou documenter explicitement son rôle |
| `GUIDE_WIZARD.md` | 10-14 | Le bloc de l'arborescence porte une ligne blanche après `3.` mais pas après `4.`, alors que le rendu en porte une aux deux endroits | ℹ️ INFO | Écart de **mise en forme** seulement : le contrôle d'égalité lit les lignes `N. LIBELLE`, et les cinq libellés sont exacts. Aucun impact sur la lecture ni sur les critères |

## Critère 5 — re-mesuré, pas lu

Les SUMMARY des plans 04-03 et 04-04 annoncent un rouge `1 failed, 200 passed` puis un vert. Je n'ai pas pris ces chiffres pour argent comptant : j'ai reconstruit les états dans des copies **hors du dépôt** (`git archive <commit> | tar -x -C /tmp/…`), donc sans `git checkout`, sans création ni changement de branche et sans modifier un seul fichier suivi. Le contrôle d'identité du paquet importé a été fait à chaque fois (`dofus_stuff.__file__` résout bien dans la copie), sans quoi l'installation éditable du dépôt aurait masqué l'expérience.

| État re-mesuré | Commit | Sortie pytest réelle | Lecture |
| --- | --- | --- | --- |
| fin de vague 3 (détecteur écrit, aiguillage **encore** obsolète) | `d841500` | `1 failed, 198 passed, 2 skipped` | **Rouge**, comme le critère 5 l'exige. Le résumé pytest nomme **un seul** échec : `tests/test_docs_wizard.py::test_aiguillage_sans_renvoi_obsolete`. Son message porte les **trois formes nommées** : (a) « Tapez `3` … pour ouvrir l'optimisation » (le numéro mesuré est `4`), (a) `3. OPTIMISATION DE STUFF` et (a) `4. SYSTEME` ×3 et `4. GESTION DE LA BASE` (numéro 4 du menu rendu = `OPTIMISATION DE STUFF`), (b) `F7` « armes à distance » alors que le libellé rendu de `F7` est `ARMES MELEE`, (c) « Vous arrivez **directement** dans le wizard » alors que la chaîne mesurée atteint `recap` |
| fin de vague 4 (aiguillage corrigé) | `1b0a17a` | `201 passed, 2 skipped` | **Vert**, obtenu par la correction du fichier livré — le détecteur n'a pas bougé depuis `4ebc5c9` (`git diff 4ebc5c9 HEAD -- tests/test_docs_wizard.py` ne touche aucune de ses fonctions) |
| après la clôture des deux constats critiques | `fd3b2dd` | `203 passed, 2 skipped` | Vert, +2 tests (le contrôle d'égalité de l'arborescence et sa morsure) |
| dépôt tel que livré | `HEAD` = `fd3b2dd` | `205 passed in 3.55s` (**0 failed, 0 skipped**) | Vert, conforme à la barre annoncée |

**Écart apparent sur le compte, expliqué et non masqué.** Les SUMMARY annoncent `200 passed` pour l'état rouge ; j'ai mesuré `198 passed, 2 skipped`. L'écart vient du **saut déclaré** des deux mesures d'empreinte : dans une copie `git archive`, `.data/dofus.sqlite3` n'existe pas (`SKIPPED [1] tests/test_docs_parcours.py:2574: base locale absente …` et `SKIPPED [1] tests/test_docs_wizard.py:2244: base locale absente …`), donc 200 = 198 + 2 selon que la base est présente. La relation se vérifie sur les trois autres états (+2 systématique : 201/203, et 205 dans le dépôt où le saut ne se déclenche pas). Le compte de **205** annoncé par la phase est donc exact dans le dépôt, et le rouge du critère 5 est **reproduit à l'identique** : un seul échec, nommé, portant les trois formes.

**Le détecteur appliqué à l'état antérieur, par moi.** Le texte de `git show c2afc42:GUIDE_WIZARD.md` (identique octet pour octet à celui de `git show 4ebc5c9:GUIDE_WIZARD.md`, vérifié par `cmp`), écrit dans un fichier temporaire **hors du dépôt**, est signalé par le détecteur livré avec **8 constats** couvrant les trois formes. Le fichier livré rend **0 constat**. Le fichier de l'arbre de travail est identique à `HEAD:GUIDE_WIZARD.md` (comparé hors CRLF). Aucun fichier suivi n'a été touché pour cette mesure (`git status --porcelain` inchangé avant/après : uniquement les éléments non suivis de l'hôte de planification).

## Les deux arbitrages — jugés, pas déférés

### CR-01 : D-47 dont les étiquettes ont été remplacées par celles du rendu

**Le fait.** D-47 prescrivait `4. OPTIMISATION` (et non `3`), `3. PANOPLIES`, `5. SYSTEME`, « lues dans le code », en citant `dofus_stuff/web/routes.py` (`menu_post`, l. ~217-222). Mesure : `menu_post` est une **table de routage** (`{"1": "terminal.search", …, "5": "terminal.system_menu"}`) qui porte les numéros et **aucun libellé**. Les libellés ne vivent que dans le corps rendu de `GET /`. L'exécution a donc écrit les étiquettes approchées sous la phrase « Le menu principal du produit, lui, garde son **arborescence réelle** » — une affirmation que le produit démentait. Le passage de clôture a conservé la numérotation de D-47 et **remplacé les étiquettes** par celles du rendu.

**Mon jugement : l'override est justifié, et il ne casse rien.**

- Il **sert** le critère 4 (« aiguillage de menus corrigé ») et l'objectif de phase (« `GUIDE_WIZARD.md` ne contredit plus le produit ») : mesuré, les cinq lignes du fichier sont désormais égales, après normalisation, aux cinq libellés que `GET /` rend réellement (`1. RECHERCHE D'OBJETS`, `2. LISTE DES EQUIPEMENTS`, `3. LISTE DES PANOPLIES`, `4. OPTIMISATION DE STUFF`, `5. SYSTEME` — `5. SYSTEME` **confirmé par la mesure**, pas supposé).
- Il **honore l'intention** de D-47 (« lu dans le code, jamais écrit de mémoire ») mieux que le texte de D-47 lui-même : la source citée par D-47 ne porte pas de libellés, la mesure du rendu les porte tous.
- Il **ne désarme aucun contrôle** : la tolérance par appartenance de mots du détecteur est intacte (elle est *voulue*, et `test_renvois_legitimes_non_signales` l'exige) ; le contrôle ajouté est une assertion **séparée, d'égalité**, et sa morsure est prouvée à chaque exécution de la suite par mutation d'une **copie en mémoire** du fichier livré (`test_arborescence_abregee_signalee_par_le_controle`), sans jamais écrire le fichier du dépôt.
- Il **conserve** ce que D-47 existait pour résorber : la phrase obsolète « tapez `3` puis Entrée » a disparu (`grep -rniE "tapez *\`?3\`? *puis"` → rien dans `README.md`, `GUIDE_WIZARD.md`, `docs/`), et la phrase livrée « Tapez `4` puis **Entrée** pour ouvrir l'optimisation » est **vraie** au rendu (`POST / selection=4` → `302 /optimize`).
- **La tension résiduelle, nommée** : le témoin de légitimité du détecteur (`TEMOIN_AIGUILLAGE_CORRIGE`) porte encore `3. PANOPLIES` / `4. OPTIMISATION` comme la forme corrigée type, alors que le contrôle d'égalité refuse exactement ces deux chaînes sur le fichier livré. Les deux contrôles ont des portées différentes et sont verts tous les deux, mais la coexistence peut tromper un relecteur : c'est consigné en INFO, pas en gap (aucun critère n'est en jeu).

**Ce que je n'ai pas accepté sans preuve :** que le contrôle d'égalité puisse passer **par vacuité**. Je l'ai attaqué : sur un texte vide, sur un texte sans arborescence, et sur une arborescence écrite en tableau (`| 3 | PANOPLIES |`), il rend **1 constat** (« le texte controle ne porte aucune ligne `N. LIBELLE` ») — la vacuité est fermée. Sur six mutations dont deux abréviations que le détecteur laisse passer, il rend **1 constat chacune**. Le retrait pur et simple des deux lignes mutées est attrapé par le test de mutation (« la ligne … est absente du texte livre »). La seule échappatoire réelle est la limite **déclarée** par la docstring (« une arborescence ecrite sans numero n'y serait pas mesuree ») — et cette déclaration est **conservatrice** : un tel texte fait en réalité rougir le contrôle.

### CR-02 : D-64 l'emporte sur la lecture stricte de D-63

**Le fait.** La phrase de `docs/parcours-simplifie.md:~140` (« le wizard avancé … affiche `Precedent` et `Suivant` **à la place** ») était déjà trop générale, et la phase venait de publier la page qui la contredit. Mesure : l'étape 1 (`slots`) rend `[('F7', 'Page prec'), ('F8', 'Suivant'), ('ESC', 'Retour')]`, le récapitulatif `[('F7', 'Precedent'), ('F8', 'Page suiv'), ('ESC', 'Retour')]` (`routes.py:138-139`, `f7_label = "Precedent" if f7_url else "Page prec"`). D-63 prescrivait « aucun autre énoncé de cette page n'est modifié » ; D-64 exigeait que l'affirmation reste **vraie**.

**Mon jugement : le porteur a tranché correctement.** D-63 était une règle de périmètre, D-64 un critère de vérité ; laisser la phrase telle quelle aurait conservé, dans une page livrée, une affirmation que la mesure et la page sœur démentent — c'est-à-dire exactement le défaut que la phase existe pour résorber. La retouche est **minimale** (une phrase, une ligne, objet et registre conservés ; le membre « qui n'est pas décrit ici » a été laissé au singulier pour ne pas capturer l'ancre D-63 au pluriel), et ses **deux liens D-63 sont intacts** (`](wizard-avance.md)` aux lignes 5 et 256 — mesuré).

**L'ancre renforcée mord, et je l'ai vérifié indépendamment** : sur la phrase d'avant le gap (mutation en mémoire), `_constats_touches_wizard` rend **2 constats** (« ne cite pas `Page prec` », « ne cite pas `Page suiv` ») ; en ne retirant qu'une extrémité, **1 constat** ; sur la phrase livrée, `0`. Le garde-fou porte bien sur la partie **après** l'ancre (`ANCRE_TOUCHES_WIZARD`), donc les libellés du **résultat** cités plus haut dans la même ligne ne peuvent pas le satisfaire — c'est ce qui le rend non vacuolaire, contrairement au défaut IN-02 qu'il évite explicitement. Côté suite : `tests/test_docs_parcours.py` passe de **19 à 20** assertions, **0 retirée** ; `TOUCHES_WIZARD` → `TOUCHES_WIZARD_INTERMEDIAIRES` à valeur identique au caractère près, avec la même assertion négative (`if touche in touches:`) et le même message, plus deux extrémités **mesurées au rendu**.

## Avertissements ouverts — jugement

Les cinq avertissements de `04-REVIEW.md` restent ouverts et **nommés** ; aucun n'est masqué. Je les ai re-mesurés un par un (voir la table des anti-motifs) et je réponds à la question posée : **aucun n'invalide un critère de succès** — et je dis lesquels sont de vraies imperfections du livrable, pour qu'ils ne soient pas pris pour de simples fragilités de harnais.

| Réf. | Invalide un critère ? | Pourquoi, en une phrase |
| --- | --- | --- |
| WR-01 (règle de refus des `slots`) | **Non** — mais c'est une imperfection **réelle du livrable** | Les critères 1 à 3 énumèrent les libellés, les formats d'édition, la syntaxe d'items et les commandes ; les refus hors liste de l'écran `slots` n'y figurent pas. Le contre-exemple est néanmoins mesuré (`12` → `SLOT INVALIDE`, message jamais cité) : une phrase de la source unique est inexacte pour une saisie hors liste. Remède d'une ligne, et deux saisies à ajouter au corpus de refus |
| WR-02 (assertion CRLF) | **Non** — vert coïncident déclaré | Aucun critère ne porte sur les octets de fin de ligne ; la page est conforme et le contrôle mesure un artefact git local. Consigné en `coincidental_reliance_items` avec le durcissement attendu |
| WR-03 (helpers recopiés) | **Non** | Duplication de harnais, sans effet sur ce que la phase prouve ; la règle de `tests/conftest.py` est enfreinte (dette de maintenabilité) |
| WR-04 (`IndexError` nu) | **Non** | Solidité du harnais : j'ai moi-même touché le chemin et reçu un `IndexError` sans localisation — c'est un manquement à l'exigence de message localisant (D-13), pas un critère de phase |
| WR-05 (§9/§12 sans propriétaire, fait `POIDS : (aucun — defaut INT)` introuvable) | **Non** — mais c'est une imperfection **réelle du livrable** | Aucun critère n'énumère ce fait ; il reste que le seul fait produit encore vérifiable de ces deux sections n'est atteignable que dans le code du solveur. Remède : une phrase adossée au rendu près de l'étape `RECAPITULATIF` |

**Pourquoi je ne les transforme pas en `gaps_found`.** La règle de décision ne déclenche un gap que sur une vérité **retenue** qui échoue, un artefact manquant/stub, un lien non câblé ou un bloqueur (marqueur de dette, atteinte à l'objectif). Les 19 vérités issues des critères du ROADMAP et des plans tiennent, aucune n'échoue ; il n'y a **aucun** marqueur `TBD`/`FIXME`/`XXX` dans les huit fichiers ; l'objectif de phase (« source unique alignée sur le code » + « `GUIDE_WIZARD.md` ne contredit plus le produit ») est tenu pour **toutes** les affirmations que `GUIDE_WIZARD.md` porte (vérifiées une par une : aiguillage, arborescence, instruction d'entrée, renvoi au sommaire) et pour tous les libellés, formats, messages et commandes que les critères nomment. WR-01 et WR-05 sont des **défauts d'exactitude** à corriger — je les signale comme tels et je recommande de les fermer (la consigne du porteur de projet est de choisir la solution la plus simple qui livre un produit fonctionnel, testé et maintenable ; une phrase inexacte dans la source unique de référence ne doit pas s'installer durablement). Les marquer `gaps_found` ferait échouer une phase dont les cinq critères sont démontrés, pour deux phrases hors du contrat énuméré ; les taire serait malhonnête. C'est la position que j'assume, en la rendant vérifiable.

## Prohibitions (22 déclarées, 22 contrôlées)

Les plans 04-01 à 04-04 déclarent 6 + 5 + 5 + 6 = **22 prohibitions**, en texte libre (aucun champ `status`/`verification`, donc aucun palier test/jugement à router — ce n'est pas un manquement, la phase n'a pas déclaré de paliers). Contrôles négatifs, mesurés :

- **Aucune commande destructrice présentée ni exécutée** : `grep -rn -iE "db clear|drop table|purge oui|rm -rf" GUIDE_WIZARD.md docs/wizard-avance.md` → **rien** ; l'aiguillage et la page du wizard n'en portent aucune trace, et l'exemple guidé se termine explicitement sur « Aucune commande destructrice n'appartient à ce parcours ». (`db clear` apparaît dans `README.md:80` et `docs/cli.md`, **hors** du périmètre de cette phase : la modification du `README.md` par la phase 4 est de −2 lignes, la ligne préexistante n'a pas été touchée.)
- **Rien sous `.data/` ni `.doc-agent/`** : `mtime`/taille de `.data/dofus.sqlite3` inchangés (2026-09-06 23:27:36, 24 989 696 octets) autour de mes trois exécutions complètes ; aucun `drop`, aucune suppression, aucun `db clear` dans le diff de la phase ; le module de test **n'importe pas** `dofus_stuff.database` et la garde `ast` refuse `remove`/`unlink`/`rmdir`/`rmtree`.
- **`main()` jamais exécuté** : la garde `ast` refuse tout appel `main` et la suite est verte ; aucun processus produit lancé.
- **Le solveur n'est jamais exécuté par le harnais** : la garde `ast` refuse toute paire `data={"cmd": "GO"}` (comparaison `casefold()`), et aucun test ne poste `GO` — le libellé n'est **cité** que depuis le rendu du récapitulatif. (Le `RESET`, le `SAVES` et les chiffres `1`-`8`, eux, sont postés : ils ne lancent pas le calcul.)
- **`dofus_stuff/**` non modifié** : `git diff --name-only c2afc42 HEAD` hors `.planning/` rend exactement les **huit** fichiers documentaires/tests ; aucun fichier de `dofus_stuff/` — le code est resté le référentiel.
- **Aucune publication, aucun déploiement, aucun achat** : `origin/main` est figé à `1d475f9` (2026-09-07), **112** commits locaux non poussés, et `git branch -r --contains c2afc42` ne rend aucune branche distante ; aucun commit de la phase n'est sorti du dépôt.
- **La copie figée n'est pas présentée comme de la documentation** : `tests/fixtures/guide-wizard-obsolete.md` vit sous `tests/`, son en-tête déclare « Ce n'est PAS de la documentation », et aucune page de `docs/` ni le sommaire ne la citent.
- **Aucune exhaustivité revendiquée** : `LIMITE_HONNETE` est dans le module **et** dans les messages (« le detecteur couvre trois formes nommees … ne revendique aucune exhaustivite ») ; les trois prédicats existent bien et un seul (`MOTIFS_RENVOI` de longueur 3). Vérifié : l'énoncé produit est « le détecteur ne signale rien sur l'aiguillage corrigé », jamais « plus aucun renvoi obsolète n'existe ». Deux limites **déclarées** ont été testées comme vraies : la couverture (3 formes, pas plus) et la précision (les jetons `N. LIBELLE` sont jugés contre les libellés **mesurés** de premier niveau — un renvoi vers un sous-menu portant le même numéro est effectivement rapporté comme forme (a), ce que le module annonce).

## Limites honnêtes déclarées — vérifiées comme vraies

Une page ou un test qui revendique plus qu'il ne contrôle est lui-même un défaut. J'ai donc testé les déclarations de portée :

| Déclaration | Où | Vraie ? |
| --- | --- | --- |
| « la prose libre de la page n'est pas vérifiée par un test ; aucune exhaustivité de la rédaction » | docstring du module | ✓ vrai — les contrôles portent sur les libellés, nombres et messages **cités** |
| « le détecteur couvre trois formes nommées, aucune exhaustivité » | `LIMITE_HONNETE` + messages d'échec | ✓ vrai — 3 prédicats, mesurés, et les témoins légitimes ne sont pas signalés (0 constat ×4) |
| « le contrôle d'arborescence porte sur les lignes `N. LIBELLE` ; une arborescence sans numéro n'y serait pas mesurée » | docstring de `_constats_arborescence` | ✓ vrai **et conservateur** — un tableau `\| 3 \| PANOPLIES \|` fait en réalité rougir le contrôle (1 constat de vacuité) |
| « l'exécution réelle de `GO` n'est pas rejouée ici : elle est couverte, patchée, par `tests/test_web.py` » | 04-02, assumptions | ✓ vrai — `test_optimize_wizard_go_mocked` existe dans `tests/test_web.py` et la garde `ast` interdit de poster `GO` ici |
| « le module saute explicitement si la base est absente au lieu de rendre un faux vert » | 04-02, must_haves | ✓ vrai — observé sur les copies archivées : 2 sauts nommant la raison, et **0 saut** dans le dépôt où la base est présente |
| « la copie figée est partielle et annoncée comme telle » | en-tête de la fixture | ✓ vrai — 39 lignes, en-tête HTML explicite, aucune citation depuis `docs/` |

## Human Verification Required

**Aucune.** Chaque critère d'acceptation est démontré par un contrôle automatique que j'ai exécuté moi-même (suite complète, copies archivées d'états antérieurs, rendu des écrans en processus, mutations en mémoire). Aucun critère ne dépend d'un aspect visuel, d'un service externe, d'un ressenti de performance ou d'une intégration réseau : la phase est documentaire et son référentiel est un rendu de terminal, dont le texte est mesurable. Les deux points qui auraient pu appeler un humain — « l'arborescence est-elle celle du produit ? » et « l'affirmation de la page sœur est-elle vraie ? » — ont été tranchés par la mesure (rendu de `GET /` ; barres des neuf écrans), pas par une opinion.

## Gaps Summary

**Aucun gap.** Les cinq critères de succès du ROADMAP sont tenus, les 19 vérités retenues sont vérifiées, les huit artefacts passent les quatre niveaux (existence, substance, câblage, flux de données), aucun lien clé n'est rompu, aucun marqueur de dette n'a été ajouté et aucune assertion n'a été retirée ou affaiblie. Les deux constats critiques de la revue de code sont **réellement clos** (CR-01 : arborescence égale au rendu, contrôle d'égalité mordant et non vacuolaire ; CR-02 : phrase vraie par étape, ancre renforcée qui mord) et le critère 5 est **re-mesuré** rouge puis vert sur des copies hors dépôt.

Ce qui reste ouvert est consigné en avertissements et informations, avec leur remède : **WR-01** (règle de refus des `slots` trop générale, `SLOT INVALIDE` jamais cité) et **WR-05** (fait du repli par défaut des poids hors documentation) sont les deux seuls **défauts d'exactitude du livrable** ; **WR-02** (assertion CRLF dépendante d'un réglage git local, interdite par `.claude/CLAUDE.md` § 11), **WR-03** (helpers recopiés), **WR-04** (`IndexError` nu, observé par moi) portent sur la robustesse du harnais ; **IN-01** à **IN-04** sont des précisions. Aucun n'invalide un critère, aucun n'est masqué, et le remède de chacun est nommé dans la table des anti-motifs.

## Notes de procédure (ce que j'ai fait, et un écart que je déclare)

- **Périmètre respecté** : aucune branche créée ni changée (`git branch --show-current` → `main`, avant et après) ; aucun `git checkout` ; aucune écriture sous `.data/` ni `.doc-agent/` ; aucun accès réseau ; `main()` jamais exécuté ; aucune commande destructive. Les copies d'états antérieurs sont des `git archive` décompressées **hors du dépôt** (`/tmp`), et `git status --porcelain` affiche exactement les mêmes entrées non suivies de l'hôte de planification avant et après cette vérification.
- **Écart déclaré — un `GO` non intentionnel.** Pendant une première passe d'énumération des refus du récapitulatif, j'ai posté `cmd=go` (minuscules) en croyant la comparaison sensible à la casse. Le produit la traite **insensiblement à la casse** : la requête a réellement lancé le solveur (`go` → `302 /optimize/result`), en processus, sur la base **temporaire** de mon harnais (aucune connexion réseau, `offline=True`, catalogue en mémoire, rien écrit sous le `.data/` du dépôt). C'est précisément le comportement que la garde `ast` du module interdit aux tests — la garde du livrable est donc plus stricte que ma sonde ne l'a été. Aucun POST `GO`/`go` par la suite : les énumérations suivantes ont évité cette valeur.
- **Ce que je n'ai pas pu vérifier sans un geste humain** : rien. Je n'ai inventé ni résultat de test, ni identifiant, ni validation.

---

_Vérifié : 2026-09-11T19:45:14Z_
_Vérificateur : Claude (gsd-verifier)_
