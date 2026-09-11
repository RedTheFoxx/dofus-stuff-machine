---
phase: 03-parcours-simplifi-document-depuis-le-rendu-r-el
verified: 2026-09-11T17:38:29Z
status: passed
score: 24/24 must-haves verified (0 present-behavior-unverified, 0 override, 0 gap)
covered_files:
  - .planning/REQUIREMENTS.md
  - .planning/phases/03-parcours-simplifi-document-depuis-le-rendu-r-el/03-01-PLAN.md
  - .planning/phases/03-parcours-simplifi-document-depuis-le-rendu-r-el/03-01-SUMMARY.md
  - .planning/phases/03-parcours-simplifi-document-depuis-le-rendu-r-el/03-02-PLAN.md
  - .planning/phases/03-parcours-simplifi-document-depuis-le-rendu-r-el/03-02-SUMMARY.md
  - .planning/phases/03-parcours-simplifi-document-depuis-le-rendu-r-el/03-03-PLAN.md
  - .planning/phases/03-parcours-simplifi-document-depuis-le-rendu-r-el/03-03-SUMMARY.md
  - .planning/phases/03-parcours-simplifi-document-depuis-le-rendu-r-el/03-04-PLAN.md
  - .planning/phases/03-parcours-simplifi-document-depuis-le-rendu-r-el/03-04-SUMMARY.md
  - docs/parcours-simplifie.md
  - docs/sommaire.md
  - tests/test_docs_parcours.py
covered_digest: "v1:sha256:769b8619b163eae5f6cce4b60102151721d3400c05e96fdcd2d1e699b91deabe"
behavior_unverified: 0
overrides_applied: 0
prohibitions:
  test_tier: 10
  test_tier_enforced: 10
  judgment_tier: 3
  judgment_tier_flagged: 3
  flag: "unverified-prohibition — human review recommended (jugements LLM, non autoritaires ; aucun ne bloque, aucun n'est silencieux)"
coincidental_reliance_items:
  - truth: "La page est complète et conforme : ... elle est en CRLF sans BOM (03-04, critère 5/V14)"
    reason: undeclared-precondition
    harden: "Le contrôle mesure les octets de l'arbre de travail, qui ne sont en CRLF que par le réglage local `core.autocrlf=true` (objet versionné `i/lf`, aucun `.gitattributes`) : exiger l'homogénéité des fins de ligne, jamais le CRLF exact, comme le demande `.claude/CLAUDE.md` §11 (« ne pas asserter sur les octets de fin de ligne »)"
  - truth: "Le harnais n'ouvre ni la base, ni un processus, ni un socket, ni le réseau ; la clôture transitive de ses imports ne contient ni racine interdite ni `dofus_stuff.database` (03-01, V15(b))"
    reason: undeclared-precondition
    harden: "La clôture est calculée sur les arêtes `ast` des modules atteints : elle ne modélise pas l'exécution du paquet parent, alors que le module importe `dofus_stuff.web.dofusbook_export`, ce qui exécute `dofus_stuff/web/__init__.py` (mesure : `dofus_stuff.database` et `sqlite3` présents dans `sys.modules`). Calculer la clôture réelle (`sys.modules` avant/après import) ou déclarer la racine `dofus_stuff.web`"
---

# Phase 3 : Parcours simplifié documenté depuis le rendu réel — Rapport de vérification

**Objectif de phase** (verbatim, `.planning/ROADMAP.md`) : « Un lecteur peut dérouler le flux simplifié classe → éléments → niveau, lire son résultat et comprendre ce que l'outil suppose. »
**Vérifié le :** 2026-09-11T17:38:29Z
**Statut :** `passed`
**Re-vérification :** non — vérification initiale (Step 0 : aucun `*-VERIFICATION.md` antérieur dans le dossier de phase)

## Verdict

Les **cinq critères de succès du ROADMAP** sont **atteints et démontrés par le rendu réel**, pas par la prose des SUMMARY. Les 24 must-haves (critères du ROADMAP fusionnés avec les vérités des quatre plans) sont vérifiés : **0 gap, 0 présent-mais-comportement-non-exercé, 0 override**. La suite est verte (**186 passed in 5.23s**), le module de la phase compte **17 tests (1.10 s)**, et l'empreinte de `.data/dofus.sqlite3` est **identique** autour de la suite entière.

Ce que je ne me suis pas contenté de lire :

1. **Le critère 5 (assertion négative) mord vraiment.** Ma propre batterie — **22 mutations** appliquées à des **copies jetables** de la page, jamais à l'arbre livré — est détectée **22/22**, chacune avec un constat qui nomme la page, la section, la valeur attendue et le fichier de code. Inverser `9. Iop` en `9. Feca`, permuter `3. Eau`, inventer une entrée acceptée, reformuler un message de refus, épingler `Score : 123`, écrire « dernière page » : tout rougit. La copie non mutée reste verte avant chaque mutation.
2. **Les deux écarts enregistrés (ÉCR-1, ÉCR-2) tiennent** : aucune ligne rendue ne porte de troncature, et la position des diagnostics est relative à la **fin** du résultat, pas à la dernière page. Mesure indépendante sur l'état du module (Cra, quatre éléments, niveau 200) : **3 pages, `Méthode : ` et `Score : ` en page 2/3**, la phrase du catalogue immédiatement après.
3. **Le rendu d'une seule page** (que la page revendique sans carte ni `F7`/`F8`) a été mesuré par moi : statut `ID DETAIL | SAVE [NOM] | SAVES | EDIT | DB — ENTREE=VALIDER`, barre de touches réduite à (`ESC`, `Retour`), `data-body-total="1"`.

Deux constats de revue sont **tranchés dans ce rapport avec une mesure, pas une opinion** : **WR-01** est confirmé (et aggravé — la page correcte en LF rougit, ce qui contredit `.claude/CLAUDE.md` §11) ; **WR-02** est **partiellement un faux positif** (le commentaire visé décrit un rendu qui, mesuré, place bien les diagnostics sur la dernière page — 2/2 —, la mesure « page 2/3 » de la revue venant d'un **autre** profil). Deux constats supplémentaires ont été mesurés et sont reportés en avertissement sans être des gaps : la **clôture d'imports** de la garde `ast` n'est pas la clôture réelle (voir « Faux verts mesurés »), et la défense en profondeur des libellés du résultat reste **à une jambe** sur deux littéraux.

Aucune vérification humaine n'est requise : chaque critère d'acceptation est prouvé par un contrôle automatique, et les deux limites non falsifiables de la phase (`03-VALIDATION.md` § « Vérités non falsifiables ») sont **déclarées**, pas maquillées.

## 1. Reproductibilité et périmètre (contraintes respectées)

```bash
cd C:/Users/Red/Documents/Projets/dofus-stuff-machine
.venv/Scripts/python.exe -m pytest -q
```

```text
........................................................................ [ 38%]
........................................................................ [ 77%]
..........................................                               [100%]
186 passed in 5.23s
```

- **186 passed** avec l'interpréteur épinglé du venv (l'interpréteur ambiant n'a pas pytest). Module de la phase seul : **17 passed in 1.10s**, aucun `skip`.
- **Empreinte de la base locale, avant et après la suite entière** (V15(a)) — mesure faite par la vérification, pas par le module :

| Instant | taille | `mtime_ns` | SHA-256 |
|---------|--------|------------|---------|
| avant `pytest -q` | 24 989 696 | 1 788 730 056 843 137 500 | `e3793d64cb7939ad1a51837b075b6b95e03d64c878fcb9cc07f86c00bb8fef7b` |
| après `pytest -q` | 24 989 696 | 1 788 730 056 843 137 500 | `e3793d64cb7939ad1a51837b075b6b95e03d64c878fcb9cc07f86c00bb8fef7b` |

  Les trois composantes sont **identiques** ; la valeur coïncide avec celle consignée par les SUMMARY (`24 989 696`, `mtime_ns 1788730056843137500`). Aucune écriture, aucune resynchronisation, aucun réseau : je n'ai lancé ni serveur, ni `main()`, ni navigateur ; toutes les mutations ont été appliquées à des copies sous le répertoire temporaire système, **jamais** dans l'arbre livré.
- **Périmètre** : sur les 17 commits de la phase (`git diff --name-only 8f437bd..HEAD`, `8f437bd` = tête de la phase 2), seuls `docs/parcours-simplifie.md`, `docs/sommaire.md`, `tests/test_docs_parcours.py` et des fichiers `.planning/` sont touchés. **Aucun** chemin `dofus_stuff/**`, `README.md`, `GUIDE_WIZARD.md`, `pyproject.toml` ni `fetcher.py`. `git status --porcelain -- docs tests` est vide : le harnais n'a pas plié la page, et la page n'a pas été pliée pour le harnais.
- **Hygiène d'octets de la page** (mesurée en binaire) : 20 015 octets, **269 CRLF pour 269 fins de ligne**, aucun BOM, un seul H1, **9 sections de niveau 2** dans l'ordre épinglé, dernière ligne `[Retour au sommaire](sommaire.md)`. La page ne contient **aucune** occurrence de « dernière page », **aucun** bloc ` ```console `, **aucun** lien externe. La seule occurrence de `…` est le texte d'attente **rendu** par `routes.py` (`CHARGEMENT DES SAUVEGARDES LOCALES…`), pas une troncature de libellé.

## 2. Les cinq critères de succès du ROADMAP

| # | Critère (ROADMAP) | Verdict | Preuve mesurée |
|---|-------------------|---------|----------------|
| 1 | Les trois questions et `AVANCE : personnaliser les réglages` cités tels qu'ils sont rendus, avec les entrées acceptées (nom ou numéro de classe, éléments et alias, séparateurs) et les messages d'erreur réels | ✓ ATTEINT | Rendu par `test_client` : `1/3 - Quelle est votre classe ?`, `2/3 - Quels éléments privilégier ?`, `3/3 - Quel est votre niveau ? (1 à 200)`, `AVANCE : personnaliser les réglages` dans les **lignes du corps** des trois écrans (`routes.py:1000-1010`) et cités dans la section correspondante. 25 entrées épinglées **rejouées sur le rendu** (302 ou 200 + message), tables de la page exigées dans **les deux sens**. Mutations M3 (entrée inventée), M4 (message reformulé), M5 (ligne `AVANCE` renommée) : rouges, constat attribué. |
| 2 | Le lecteur sait lire son résultat : carte de pagination, emplacement réel de `Méthode`, `Score` et `Indice de recherche`, table de correspondance des libellés | ✓ ATTEINT (ÉCR-1/ÉCR-2 enregistrés) | `PAGE 1/3 — ENTREE=VALIDER` lu dans la **ligne de statut** et confronté aux attributs `data-body-page`/`data-body-total` ; diagnostics **positionnels** (après le dernier `Équipement :`, avant `Greedy: `, phrase du catalogue en position `dernier_diagnostic + 1`) ; mesurés en **page 2/3** sur l'état du module. Table de correspondance : **17 libellés** extraits par `ast` de `display_slots` (`api.py:362-380`), chacun avec son nom complet relu **sur la ligne qui le porte**. Aucune troncature promise (la page dit « libellé technique », et explique que le rendu les complète par des espaces). Mutations M6, M7, M8 : rouges. |
| 3 | La sauvegarde navigateur (20 sauvegardes maximum) et l'export Dofusbook décrits et rattachés à l'écran qui les expose | ✓ ATTEINT (ÉCR-5 dit honnêtement) | Écran `SAV-01` (`GET /saves`) : en-tête `SAV-01`, corps `CHARGEMENT DES SAUVEGARDES LOCALES…`, statut `N OUVRIR \| DEL N \| PURGE OUI`, `data-mode="saves"` ; écran de résultat : statut `ID DETAIL \| SAVE [NOM] \| SAVES \| EDIT \| DB`, `data-mode="result"`. Limite **lue dans le JS** (`terminal.js:14` clé `dofus-stuff-machine.saves`, `:15` `MAX_SAVES = 20`) et citée ; la page dit « les plus anciennes sont remplacées » (le `shift` de `:295-297` est silencieux) et **jamais** « 20 maximum ». Export : `build_dofusbook_url` appelée sur sa surface **publique pure**, charge utile décodée (`base64` + `msgpack`) → **16** emplacements comptés, `prysma` absente des `ids`, URL d'import relue sur `DOFUSBOOK_IMPORT_URL` et citée entre accents graves. Mutations M11, M12, M13 : rouges. |
| 4 | Les hypothèses (points par niveau, paliers PA/PM 40/100/150, heuristiques de classe, ni exo ni parchemins) et les limites (« indice » ≠ qualité en combat, recherche sur une sélection du catalogue) explicites | ✓ ATTEINT | Capital prouvé **par balayage** aux niveaux 1/39/40/99/100/149/150/200 : `capital_spent == total_capital_for_level == 5 * (niveau - 1)` ; paliers PA/PM prouvés **sur le comportement** de `recommendation_spec` (6/8/10/11 et 3/4/5/6, bascule exacte à 40/100/150, base PA 6→7 à 100) ; quatre ensembles de classes extraits par `ast`, **9** classes sans objectif **calculées** ; les deux lignes littérales d'`api.py` (`:316` sans exo/parchemins, `:434` sélection du catalogue) exigées **des deux côtés**, et `base+parcho` (`:429`) levé d'ambiguïté. Limites : trois modes de `score.py:8` cités, `_is_plausible_equipment` et `top_k=40` ancrés sur leurs sources, `url[:COLS]` ancré. Mutations M15 (formule) et M16 (chiffre de catalogue) : rouges. |
| 5 | Le contrôle détecte un numéro de menu associé au mauvais libellé (assertion négative dérivée du rendu réel) et la suite reste verte | ✓ ATTEINT | Les couples **viennent du rendu** (`routes.py:989` pour 19 classes, `:993` pour 4 éléments) et sont comparés **section par section** ; trois modes de constat (numéro cité deux fois, numéro absent, libellé différent) + un numéro inventé + le **compte d'occurrences** (19 + 4). Mes mutations M1/M2 rougissent en nommant « dans « ## Question 1/3 : la classe », le numero 9 est associe au libelle « Feca » ; attendu « Iop » … rendu par `dofus_stuff/web/routes.py:989` ». Suite verte, copie non mutée verte. |

## 3. Must-haves vérifiés (critères du ROADMAP fusionnés avec les vérités des plans)

| # | Vérité | Statut | Preuve |
|---|--------|--------|--------|
| 1 | Les trois questions et `AVANCE` sont rendues telles quelles et citées par la section correspondante (V1) | ✓ VERIFIED | Rendu mesuré (corps des 3 écrans) + page ; mutation M5 rouge ; `_libelle_saisie` = `CHOIX : [` et (`ESC`, `Retour`) exigés |
| 2 | Chaque entrée citée par la page est rejouée sur le rendu et classée par ce que l'outil fait réellement (V2) | ✓ VERIFIED | Table épinglée rejouée (302 / `_run_optimize_and_redirect` patché / 200 + message) ; page exigée **dans les deux sens** ; M3 rouge |
| 3 | Les trois messages de refus sont exigés au début de la ligne de statut, texte exact (V3) | ✓ VERIFIED | `routes.py` : `Saisissez le nom ou le numéro de votre classe.`, `Exemple : feu, terre air, ou multi.`, `Saisissez un niveau entre 1 et 200.` ; M4 rouge |
| 4 | La correspondance numéro ↔ libellé des deux menus est comparée section par section (V4, critère 5) | ✓ VERIFIED | Dérivée du rendu ; M1/M2 rouges avec constat attribué ; comptage 23 occurrences exigé |
| 5 | Le sommaire, le H1, la ligne de retour et l'exhaustivité bidirectionnelle restent cohérents, sans exception (V14, D-39) | ✓ VERIFIED | `docs/sommaire.md` porte `[Parcours simplifié](parcours-simplifie.md)` ; tests de la phase 1 **inchangés** verts dans les 186 |
| 6 | Le bloc « Source de vérité » cite `routes.py`/`recommend.py` et **tout** chemin entre accents graves existe sur disque | ✓ VERIFIED | 8 chemins cités, tous existants ; M10 (chemin inventé) rouge |
| 7 | Le harnais n'ouvre ni la base, ni un processus, ni un socket, ni le réseau ; ne supprime rien ; n'exécute jamais `main()` (garde `ast` + clôture) | ✓ VERIFIED (coincidental-reliance) | Garde passée en propre : clôture **ast** = 6 modules atteints, aucun interdit, aucun non résolu, aucun appel à `main`/suppression ; empreinte `.data` identique autour de la suite. **Réserve mesurée** : la clôture réelle atteint `dofus_stuff.database` et `sqlite3` par le paquet parent `dofus_stuff.web` — voir « Faux verts mesurés » n° 2 |
| 8 | Le parcours CLI ne pose pas les trois questions : la page l'affirme, aucun littéral de `profile_input.py` ne porte une invite de classe ou d'élément (D-33) | ✓ VERIFIED | Phrase épinglée exigée dans la page ; littéraux du module CLI scannés par `ast` ; M9 rouge |
| 9 | La carte de pagination est lue dans la **ligne de statut** et cohérente avec les attributs de la coquille ; la page `N/N` porte `PAGE N/N` (V5) | ✓ VERIFIED | Mesures : `PAGE 1/3` + `data-body-page="1"`/`data-body-total="3"` ; cohérence statut ↔ attributs exigée ; aucun total épinglé |
| 10 | Le résultat d'une seule page n'a ni carte de pagination ni `F7`/`F8` (affirmation de la page, jamais évaluée par le module — WR-04) | ✓ VERIFIED | Mesure propre : statut `ID DETAIL \| SAVE [NOM] \| SAVES \| EDIT \| DB — ENTREE=VALIDER` (aucun `PAGE`), touches réduites à (`ESC`, `Retour`), `data-body-total="1"` ; `routes.py:143-146` conditionne carte et touches à `total > 1` |
| 11 | Les trois diagnostics sont **positionnels** (après le dernier `Équipement :`, avant `Greedy: `), jamais `page == total` (V6, ÉCR-2) | ✓ VERIFIED | Mesure : 3 pages, diagnostics en **2/3** ; contrôle positionnel ; aucun motif `page == total` dans le module (`grep` vide) ; M7 rouge ; « dernière page » absent de toute la page |
| 12 | La table de correspondance couvre **exactement** les 17 libellés de `display_slots`, chaque nom complet relu sur sa ligne source (V7, ÉCR-1) | ✓ VERIFIED | Extraction `ast` de `display_slots` (17) ; noms relus dans les commentaires `_GROUP_SLOTS` et `solver_spec` ; M8 (ligne `belt` supprimée) rouge |
| 13 | Aucun libellé n'est présenté comme tronqué, aucun test n'asserte l'apparition de `…` (ÉCR-1) | ✓ VERIFIED | La page dit « ni raccourcis ni abrégés à l'affichage … il ne les coupe pas » ; le seul `…` de la page est le texte d'attente rendu ; aucun contrôle n'asserte `…` sur le rendu du résultat |
| 14 | La section « Lire le résultat » ne fige aucune valeur volatile et distingue la barre de touches du résultat de celle du wizard | ✓ VERIFIED | 4 motifs volatils contrôlés absents ; M6 rouge ; `F7=Page prec`/`F8=Page suiv`/`ESC=Retour` mesurés, `Precedent`/`Suivant` interdits sur le résultat |
| 15 | Les deux écrans qui exposent la sauvegarde et l'export sont rendus et leurs libellés exigés (V8) | ✓ VERIFIED | `SAV-01`, texte d'attente, `N OUVRIR \| DEL N \| PURGE OUI`, `data-mode="saves"` ; statut du résultat portant `SAVE [NOM]`, `SAVES`, `DB`, `data-mode="result"` |
| 16 | `MAX_SAVES` et la clé de stockage sont lus dans le JS et cités par la page — **contrôle de littéral**, nommé comme tel (V9) | ✓ VERIFIED | `terminal.js:14-15` relus à chaque exécution (`_litteral_js`) ; page cite `20` et `dofus-stuff-machine.saves` ; M12 rouge ; le module écrit lui-même qu'aucun moteur JS n'existe (ni `localStorage`, ni `shift`) et **ne prétend pas** avoir exécuté le JS |
| 17 | La page dit la vérité de l'éviction (silencieuse, « les plus anciennes sont remplacées ») et ne dit pas « 20 maximum » tout court (ÉCR-5) | ✓ VERIFIED | `shift()` tant que `length >= MAX_SAVES` (`terminal.js:295-297`), puis `push` : rien n'est refusé, la ligne de statut ne signale rien ; M13 rouge |
| 18 | L'export Dofusbook est prouvé sur sa surface publique pure : 16 emplacements calculés, `prysma` exclue, URL d'import relue du module et citée (V10) | ✓ VERIFIED | Charge utile décodée, `counts` = 10 groupes, `total = 16`, `id_prysmaradite ∉ ids`, URL lue par `getattr` public ; M11 rouge ; l'ordre des groupes reste couvert par `tests/test_web.py:713-750` (non redupliqué, D-12) |
| 19 | Aucun test ne poste `DB` sans patcher `webbrowser.open_new_tab`, et aucun test n'exécute le JS de sauvegarde | ✓ VERIFIED | `grep` : le seul POST `DB` de la suite est `tests/test_web.py:676`, sous `patch(...open_new_tab)` ; garde `ast` du module ; aucun `app.run`/`make_server` dans `tests/` |
| 20 | Le capital `5 * (niveau - 1)` est prouvé par balayage et cité par la page (V11) | ✓ VERIFIED | 8 niveaux balayés, `capital_spent == total_capital_for_level == 5*(n-1)` ; M15 rouge |
| 21 | Les paliers PA/PM et la base de PA sont prouvés sur le comportement, pas recopiés ; la page les cite en table (V11) | ✓ VERIFIED | `recommend.py:24,35-36` ; bascule exacte aux niveaux 39/40, 99/100, 149/150 ; table de la page confrontée aux cibles mesurées |
| 22 | Les heuristiques de classe sont présentées comme des **préférences de style de jeu**, les 4 ensembles extraits par `ast`, le nombre de classes sans objectif calculé (V12, ÉCR-3) | ✓ VERIFIED | 6 + 4 = 10 classes concernées, **9** sans objectif calculées et citées ; tournure « préférences de style de jeu » et libellé rendu `Jets moyens ; préférences de classe ajustables après calcul.` exigés |
| 23 | « Ni exo ni parchemins » et « recherche sur une sélection du catalogue » sont exigés **des deux côtés**, et `base+parcho` est levé d'ambiguïté (V13, ÉCR-4) | ✓ VERIFIED | `api.py:316` et `:434` cherchés par motif **dans la source** et exigés normalisés dans la page ; phrase « aucun parchemin » présente ; `api.py:429` relu |
| 24 | La page est complète et conforme (9 sections dans l'ordre, un H1, aucun bloc `console`, aucun lien externe ni vers une page absente, CRLF sans BOM), et l'en-tête rendu des trois écrans est cité (V14, RF-2) | ✓ VERIFIED (coincidental-reliance) | Mesures octets : 269 CRLF / 269 LF, pas de BOM, 9 sections, 1 H1 ; mutations M14/M17/M18/M19/M21/M22 rouges ; **réserve** : la clause CRLF est verte par le réglage git local — voir « Faux verts mesurés » n° 1 |

**Score :** **24/24** must-haves vérifiés (0 présent-mais-comportement-non-exercé, 0 override, 0 gap).

### Faux verts mesurés (contrôles verts pour une raison qui n'est pas celle de la page)

| # | Constat | Mesure qui l'établit | Effet |
|---|---------|----------------------|-------|
| 1 | **WR-01 confirmé et aggravé.** `test_page_complete_et_sans_derive` exige `fins == crlf` sur les octets de **l'arbre de travail**. `git ls-files --eol` répond `i/lf w/crlf attr/` : l'objet versionné est en **LF**, l'arbre n'est en CRLF que par `core.autocrlf=true` (aucun `.gitattributes`). | Sur une copie jetable, la **page correcte convertie en LF** → `ROUGE : CRLF — les octets portent 269 fin(s) de ligne pour 0 CRLF`. Les fins de ligne **mêlées** (1 LF sur 269) sont détectées de la même façon. `.claude/CLAUDE.md` §11 prescrit explicitement « ne pas asserter sur les octets de fin de ligne ». | Contrôle **rouge sur un artefact correct** dans un clone sans `autocrlf`. La vérité (« page en CRLF, sans BOM ») tient **ici** — comme pour toutes les pages de `docs/`, toutes `i/lf w/crlf` — mais vit d'une précondition non déclarée. Advisories A1 |
| 2 | **La clôture d'imports de la garde `ast` n'est pas la clôture réelle.** La vérité 03-01 exige que la clôture transitive des imports du module « ne contient aucune de ces racines ni `dofus_stuff.database` ». Or le module importe `dofus_stuff.web.dofusbook_export`, ce qui exécute `dofus_stuff/web/__init__.py`, qui importe `dofus_stuff.database` (`flask`, `catalog` en prime). La mesure de clôture du module marche sur les **arêtes `ast`** des modules atteints et ne modélise pas l'exécution du paquet parent. | `python -c "import dofus_stuff.web.dofusbook_export; ..."` → `dofus_stuff.database: True`, `sqlite3: True`, et `['sqlite3','socket','ctypes','urllib','http']` présents dans `sys.modules`. La garde du module, elle, mesure **6** modules atteints (`model.character`, `model.slots`, `model.solver_spec`, `model.stats`, `optimize.recommend`, `web.dofusbook_export`), aucun interdit, et passe. | La clause (c) de la vérité est **fausse au sens de la clôture d'exécution** ; le **risque nommé** (ouvrir la base, lancer un processus, ouvrir un socket, joindre le réseau) n'est **pas** réalisé (importer `sqlite3`/`socket` n'ouvre rien, et l'empreinte `.data` est identique autour de la suite). Advisories A2 |
| 3 | **Deux littéraux du résultat ne sont contrôlés qu'à une jambe** (WR-03). `ENTREE=VALIDER` est exigé **côté page** mais jamais relu dans le rendu, alors que la ligne de statut rendue est en main ; `Méthode : ` et `Score : ` sont exigés **côté rendu** mais pas côté page. | Lecture de `test_pagination_et_emplacement_du_calcul` (étapes 2 et 5) ; la valeur rendue est **mesurée** : `… — PAGE 1/3 — ENTREE=VALIDER` et les trois marqueurs présents dans le résultat concaténé. | Aucun must-have non soutenu aujourd'hui : les deux faits sont vrais et mesurés ; c'est la **dérive future** qui ne rougirait pas. Advisories A3 |

*Aucun de ces trois constats ne touche un critère d'acceptation : les faits visés sont vrais et mesurés, ce sont les **contrôles** qui sont faibles. Ils ne déclenchent donc pas `gaps_found` ; ils sont enregistrés, non silencieux.*

## 4. Batterie de morsures indépendante (copies jetables, arbre livré jamais muté)

Protocole : la page est copiée sous le répertoire temporaire système, mutée, puis la **fonction de test réelle du module** est appelée avec les fixtures réelles (`app` construite par `tests/conftest.py`, `section`, `normalize`). La copie **non mutée** est rejouée avant chaque mutation (`VERT` attendu) ; la copie mutée doit produire une `AssertionError` **attribuée**.

| # | Mutation appliquée à la copie de la page | Copie intacte | Mutation détectée | Constat attribué (extrait) |
|---|------------------------------------------|---------------|-------------------|----------------------------|
| M1 | `9. Iop` → `9. Feca` (libellé inversé) | VERT | ✓ ROUGE | « dans « ## Question 1/3 : la classe », le numero 9 est associe au libelle « Feca » ; attendu « Iop » … `routes.py:989` » |
| M2 | menu des éléments : `3. Eau` → `3. Terre` | VERT | ✓ ROUGE | « dans « ## Question 2/3 : les éléments », le numero 3 est associe au libelle « Terre » ; attendu « Eau » » |
| M3 | entrée acceptée inventée (`terre\|air`) | VERT | ✓ ROUGE | « la table « ### Entrées acceptées » … cite la saisie « terre\|air », absente des saisies acceptées mesurées » |
| M4 | les trois messages de refus reformulés | VERT | ✓ ROUGE | « la sous-section « ### Erreurs et refus » … ne cite pas le message « Exemple : feu, terre air, ou multi. » » |
| M5 | `AVANCE : personnaliser les réglages` renommée | VERT | ✓ ROUGE | « la section « ## Question 1/3 : la classe » ne cite pas le libelle « AVANCE : … » » |
| M6 | valeur volatile épinglée (`Score : 123`, `Indice : 88`) | VERT | ✓ ROUGE | « la section « Lire le résultat » fige la valeur « Score : 123 » (méthode, score, indice et total changent) » |
| M7 | « en fin de résultat » → « sur la dernière page » | VERT | ✓ ROUGE | « la section « ## Lire le résultat » dit « dernière page » ; attendu « en fin de résultat » » |
| M8 | ligne de table supprimée (`\| belt \| ceinture (ce) \|`) | VERT | ✓ ROUGE | « le libelle « belt » de `api.py:362-380` est absent de la table » |
| M9 | « ne pose pas ces trois questions » altérée | VERT | ✓ ROUGE | « la phrase « ne pose pas ces trois questions » est absente » |
| M10 | chemin de code inventé (`score2.py`) | VERT | ✓ ROUGE | « le chemin « dofus_stuff/optimize/score2.py » cite entre accents graves n'existe pas » |
| M11 | URL d'import modifiée dans la page | VERT | ✓ ROUGE | « ne cite pas, entre accents graves, l'URL d'import portee par `dofusbook_export` » |
| M12 | limite `20` → `50` dans la page | VERT | ✓ ROUGE | « ne cite pas la limite de sauvegarde portee par `terminal.js:15` » |
| M13 | « les plus anciennes sont remplacées » → « 20 maximum » | VERT | ✓ ROUGE | « dit « 20 maximum » ; attendu la tournure honnête … `terminal.js:294-318` » |
| M14 | `OPT-SIMPLE` → `OPT-SIMPL` (partout) | VERT | ✓ ROUGE | « la page ne cite pas « OPT-SIMPLE », le code de programme rendu par la ligne d'en-tete » |
| M15 | `5 * (niveau - 1)` → `6 * (niveau - 1)` | VERT | ✓ ROUGE | « ne cite pas la formule du capital par niveau (« 5 * (niveau - 1) ») » |
| M16 | chiffre de catalogue injecté (1219) | VERT | ✓ ROUGE | « la page cite 1 chiffre de catalogue(s) de quatre chiffres ou plus (1219) » |
| M17 | bloc ` ```console ` ajouté | VERT (octets d'origine) | ✓ ROUGE | « la page porte un bloc de commandes « ```console » ; la surface de commandes appartient à `docs/cli.md` » |
| M18 | lien vers `wizard-avance.md` (page absente) | VERT | ✓ ROUGE | « la page lie « wizard-avance.md », qui n'existe pas encore » |
| M19 | 9ᵉ section de niveau 2 renommée | VERT (octets d'origine) | ✓ ROUGE | « section 8 attendue « ## Ce que l'outil ne fait pas », section trouvée « Les limites de l'outil » » |
| M20 | titre d'en-tête `** RECOMMANDATION DE STUFF **` retiré | VERT | ✓ ROUGE | « la page ne cite pas « ** RECOMMANDATION DE STUFF ** », le titre rendu » |
| M21 | BOM UTF-8 ajouté | VERT (octets d'origine) | ✓ ROUGE | « les octets portent un BOM UTF-8 ; attendu un fichier sans BOM » |
| M22 | 9ᵉ section retirée | VERT (octets d'origine) | ✓ ROUGE | « la page porte 7 section(s) de niveau 2 au lieu de 9 » |

**22 mutations, 22 détections**, aucune page livrée modifiée (`git status --porcelain -- docs tests` vide avant et après). Les batteries de mutation déclarées par les SUMMARY (5 en 03-01, 6 en 03-02, 3 en 03-03, plus les morsures de 03-04) n'ont **pas** été rejouées ligne à ligne ; la propriété qu'elles portent est **reproduite indépendamment** par cette batterie, sur des mutations choisies par moi.

## 5. Artefacts exigés

| Artefact | Exigence | Statut | Détail |
|----------|----------|--------|--------|
| `docs/parcours-simplifie.md` | 9 sections, `## Question 1/3 : la classe`, `min_lines` 40 → 100 selon les plans | ✓ VERIFIED | **269 lignes / 20 015 octets** ; 9 sections de niveau 2 dans l'ordre épinglé, un H1, bloc « Source de vérité » (8 chemins, tous existants), ligne de retour en dernière ligne ; CRLF sans BOM ; committée en quatre vagues (`e61f4f6`, `8818460`, `f96f9bf`, `7a537f7`) et **jamais modifiée après** la dernière vague. |
| `docs/sommaire.md` | ligne `[Parcours simplifié](parcours-simplifie.md)`, `min_lines` 21 | ✓ VERIFIED | 21 lignes, tableau `Index` avec la ligne (et « Parcours simplifié » en 2ᵉ étape du parcours conseillé) ; tests de structure de la phase 1 verts. |
| `tests/test_docs_parcours.py` | helpers d'extraction, couples par section, entrées rejouées, garde sans base ; `min_lines` 150 → 330 selon les plans | ✓ VERIFIED | **2 734 lignes, 17 tests**, 0 `skip`, 0 test désactivé, 0 marqueur de dette ; contient `_lignes_du_corps`, `_statut`, `_touches`, `_client_etape`, `_couples_de_section`, `display_slots`, `MAX_SAVES`, `capital_spent`. |

Aucun artefact manquant, aucun stub : la page ne porte **aucun** marqueur `TBD`/`FIXME`/`XXX`/`TODO`/`HACK`/`placeholder` (grep vide sur la page et sur le module), et les sections que la page ne peut pas tirer d'un rendu (`base+parcho`, « sélection du catalogue ») sont **adossées à une ligne littérale du code**, pas remplies.

## 6. Key links (câblage réel)

| From | To | Via | Statut | Détail |
|------|----|-----|--------|--------|
| `tests/test_docs_parcours.py` | `dofus_stuff/web/routes.py` | `client.get/post("/optimize/quick/<etape>")` puis lecture des **lignes du corps** et de la ligne de statut | ✓ WIRED | 3 écrans de questions + résultat rendus en processus ; aucun serveur, aucun socket |
| `tests/test_docs_parcours.py` | `docs/parcours-simplifie.md` | lecture UTF-8 puis comparaison **par section** (`section(texte, TITRE_*, PAGE)`) | ✓ WIRED | Toutes les exigences de page passent par ce chemin ; une section absente devient un constat (jamais un vert sans objet) |
| `tests/test_docs_parcours.py` | `dofus_stuff/optimize/api.py` | `ast` sur `display_slots` + lecture des pages concaténées du résultat | ✓ WIRED | 17 libellés extraits ; position des diagnostics mesurée |
| `tests/test_docs_parcours.py` | `dofus_stuff/web/static/js/terminal.js` | `_litteral_js` (motifs `SAVES_KEY`, `MAX_SAVES`) puis exigence de citation | ✓ WIRED | Contrôle de **littéral** explicitement nommé (pas d'exécution JS) |
| `tests/test_docs_parcours.py` | `dofus_stuff/web/dofusbook_export.py` | appel public de `build_dofusbook_url` + décodage `base64`/`msgpack` ; `getattr` pour `DOFUSBOOK_IMPORT_URL` | ✓ WIRED | Charge utile décodée, `counts` et `ids` vérifiés, `prysma` absente |
| `tests/test_docs_parcours.py` | `dofus_stuff/optimize/recommend.py` / `model/solver_spec.py` | `recommendation_spec` (pur, 8 niveaux), `capital_spent`, `total_capital_for_level`, `ast` sur les ensembles de classes | ✓ WIRED | Aucun solveur lancé pour les hypothèses |
| `tests/test_docs_parcours.py` | `dofus_stuff/optimize/score.py` / `candidates.py` | lecture des trois modes et du nom du filtre, exigés dans la page | ✓ WIRED | Ancrage « par nom » sur la source citée |
| `tests/test_docs_parcours.py` | `tests/conftest.py` | fixtures `app`, `docs_dir`, `normalize`, `section`, `sections` consommées telles quelles | ✓ WIRED | Aucune redéfinition locale des helpers partagés (D-12) ; `grep` : aucune définition locale de `_section`/`_normalize` |
| `tests/test_web.py` | `dofus_stuff/web/dofusbook_export.py` | couverture existante de l'ordre des groupes et des `counts` (`:713-750`) | ✓ WIRED (réutilisée) | 03-03 s'y renvoie au lieu de redupliquer ; ✅ présent dans les 186 |
| `docs/sommaire.md` | `docs/parcours-simplifie.md` | ligne d'index dont le libellé normalisé égale le H1 | ✓ WIRED | Test d'exhaustivité bidirectionnelle vert |

## 7. Data-flow (niveau 4) — la page dit-elle ce que le code rend ?

| Affirmation de la page | Source réelle | Produit de la donnée | Statut |
|------------------------|---------------|----------------------|--------|
| Trois questions, `AVANCE`, `CHOIX`, `ESC=Retour`, `ENTREE=SUIVANT/CALCULER` | `routes.py:1000-1010`, `_screen`/`_statut` | Rendue par `test_client`, relue dans les lignes du corps | ✓ FLOWING |
| Menus 1→19 classes / 1→4 éléments | `routes.py:989`, `:993` (`CLASSES`, `ELEMENTS`) | Couples lus dans le rendu, comparés section par section | ✓ FLOWING |
| Messages de refus | `routes.py:964,972,976` via `flash` | Relus au début de la ligne de statut | ✓ FLOWING |
| `PAGE n/total`, `ENTREE=VALIDER`, `F8=Page suiv` | `routes.py:137-147` | Statut rendu mesuré (`PAGE 1/3`, 1 page → aucune carte) | ✓ FLOWING |
| `Méthode : `, `Score : `, `Indice de recherche : `, phrase du catalogue | `api.py:327-341`, `:432-434` | Lignes du corps des pages concaténées, mesurées en page 2/3 | ✓ FLOWING |
| 17 libellés d'emplacement + `(vide)` | `api.py:362-386` | `display_slots` extrait par `ast` ; ligne qui omet dofus/familier/prysma/bouclier quand ils sont vides, relue | ✓ FLOWING |
| `N OUVRIR \| DEL N \| PURGE OUI`, `SAVE [NOM] \| SAVES \| DB` | `routes.py:1293`, `:1380` | Statuts rendus mesurés, `data-mode` vérifié | ✓ FLOWING |
| `MAX_SAVES = 20`, clé `dofus-stuff-machine.saves`, éviction silencieuse | `terminal.js:14-15`, `:295-297` | **Littéraux** relus à chaque exécution (pas d'exécution JS) | ⚠️ STATIC (limite déclarée, cf. §12) |
| `5 * (niveau - 1)`, paliers 40/100/150, base PA 6→7 | `recommend.py:24,35-36`, `solver_spec.py:264-269` | Balayage de 8 niveaux : valeurs **calculées**, jamais recopiées | ✓ FLOWING |
| Préférences de classe (4 ensembles, 9 classes sans objectif) | `recommend.py:45-52` | Ensembles extraits par `ast`, compte **calculé**, comparé à la page | ✓ FLOWING |
| 16 emplacements exportés, `prysma` non exportée | `dofusbook_export.py:21,26-37` | Charge utile **décodée** ; nombre dérivé des `counts` | ✓ FLOWING |
| Aucun nombre de catalogue dans la page | `candidates.py`, `recommend.py:60` (`top_k=40`) | Mécanisme décrit, chiffres interdits et contrôlés absents | ✓ FLOWING (garde active) |

**Aucune affirmation de la page ne se termine dans un littéral statique ou une donnée de remplissage.** Le seul contrôle « statique » assumé porte sur le JavaScript, qui n'est pas exécutable ici (§12).

## 8. Behavioral spot-checks

| Comportement | Commande / mesure | Résultat | Statut |
|--------------|-------------------|----------|--------|
| Suite entière verte | `.venv/Scripts/python.exe -m pytest -q` | `186 passed in 5.23s` | ✓ PASS |
| Module de la phase | `… -m pytest tests/test_docs_parcours.py -q` | `17 passed in 1.10s`, aucun `skip` | ✓ PASS |
| `.data/` intact autour de la suite | empreinte taille + `mtime_ns` + SHA-256 avant/après | identique, 3 composantes | ✓ PASS |
| Carte de pagination sur un résultat multi-pages | POST étape 3 (Cra + 4 éléments, niveau 200) puis `GET /optimize/result?page=N` | `PAGE 1/3 … ENTREE=VALIDER`, diagnostics en 2/3 | ✓ PASS |
| Résultat d'une seule page | injection de session (`optimize_result_lines`), `GET /optimize/result` | aucun `PAGE`, aucune touche `F7`/`F8`, `data-body-total="1"` | ✓ PASS |
| Aucun test ne poste `DB` sans patch | `grep -rn '"cmd": "DB"' tests/` | un seul : `tests/test_web.py:676`, sous `patch(...open_new_tab)` | ✓ PASS |
| Aucun serveur lancé par la suite | `grep -rn "app.run(\|make_server" tests/` | aucune occurrence | ✓ PASS |
| Garde `ast` du module | exécution de `test_garde_ni_base_ni_processus_ni_reseau` + mesure de la clôture | garde passée ; clôture `ast` = 6 modules, 0 interdit, 0 non résolu | ✓ PASS (réserve §4.2) |
| Liens de la page dans les deux sens | `git ls-files --eol docs/` + tests de structure | page `i/lf w/crlf` comme ses 3 voisines | ✓ PASS |

**Step 7b :** aucune vérification de type « lister un test » n'était nécessaire ; les contrôles ont été **exécutés** (suite entière une seule fois, puis appels ciblés par fonction de test pour la batterie). **Step 7c :** `find scripts -path '*/tests/probe-*.sh'` → **aucun probe** dans le dépôt, et aucun plan ni SUMMARY de la phase n'en déclare : exécution de probes **sans objet**, ce qui est la déclaration honnête (aucun probe manquant).

## 9. Couverture des exigences

| Exigence | Plan propriétaire | Description (REQUIREMENTS.md) | Statut | Preuve |
|----------|-------------------|-------------------------------|--------|--------|
| **SIMP-01** | `03-01` (`requirements: [SIMP-01]`) | Ouvrir l'optimisation depuis le menu réel et dérouler les trois questions, avec les entrées acceptées et les messages d'erreur réels | ✓ SATISFAITE | Vérités 1-8 ci-dessus : rendu des trois écrans, 25 entrées rejouées, 3 messages exacts, couples numéro ↔ libellé, sommaire, Source de vérité, garde sans base, parcours CLI distingué |
| **SIMP-02** | `03-02` (`requirements: [SIMP-02]`) | Lire son résultat : pagination, emplacement réel des informations de calcul, correspondance des libellés abrégés à l'écran | ✓ SATISFAITE | Vérités 9-14 : carte dans la statut + attributs, diagnostics positionnels, table des 17 libellés techniques → noms complets, aucune valeur volatile. **Nuance assumée** : la correspondance porte sur le **libellé technique** rendu, pas sur une troncature (ÉCR-1, enregistré au ROADMAP et dans `WINDOWS.md` entrée 5) |
| **SIMP-03** | `03-03` (`requirements: [SIMP-03]`) | Sauvegarder un stuff dans son navigateur et l'exporter vers Dofusbook | ✓ SATISFAITE | Vérités 15-19 : deux écrans rendus, limite et clé lues dans le JS, éviction dite honnêtement, export prouvé pur (16 / `prysma` exclue), URL du module |
| **SIMP-04** | `03-04` (`requirements: [SIMP-04]`) | Savoir ce que l'outil suppose (répartition des points, paliers, heuristiques) et ce qu'il ne fait pas | ✓ SATISFAITE | Vérités 20-24 : capital balayé, paliers prouvés sur le comportement, préférences de classe calculées, deux lignes littérales exigées des deux côtés, indice borné, mécanisme de sélection sans chiffre de catalogue |

**Orphelines : aucune.** `REQUIREMENTS.md` mappe exactement SIMP-01…SIMP-04 à la phase 3 (`| SIMP-0x | Phase 3 | Complete |`) et le tableau « traçabilité » de la même phase liste les quatre mêmes identifiants — aucun identifiant attendu n'est resté sans plan propriétaire, aucun plan ne déclare un identifiant hors phase (vérifié sur les quatre frontmatter `requirements`).

## 10. Couverture des décisions (D-32…D-45)

| Décision | Honorée ? | Mesure |
|----------|-----------|--------|
| D-32 : écrans lus par le **client de test Flask en processus**, aucun serveur/socket/écriture `.data/` | oui | Fixture `app` de `conftest.py` (base construite sous `tmp_path/data`) ; `app.run`/`make_server` absents de `tests/` ; empreinte `.data` identique |
| D-33 : libellés du CLI lus dans leur **module source**, jamais par `main()` | oui | `test_parcours_cli_ne_pose_pas_les_trois_questions` analyse les littéraux de `profile_input.py` par `ast` |
| D-34 : assertion négative construite sur la correspondance **réellement rendue** | oui | Couples lus dans le rendu ; mutations M1/M2 rouges (constat nommant le couple rendu) |
| D-35 / D-19 : aucune sémantique inventée | oui | Chaque valeur citée relue dans sa source ; le seul apport non mesurable (mots français des emplacements) est présenté comme **correspondance de lecture**, pas comme sortie de l'outil |
| D-36 / D-37 : les écrans web sont la référence ; la surface de commandes reste à `docs/cli.md`, renvoi en prose | oui | Aucun bloc ` ```console ` ; renvoi en prose vers `cli.md` présent ; mutation M17 rouge |
| D-38 : « Lire le résultat » et « Sauvegarder et exporter » sont des sections de cette page | oui | Sections 4 et 6 de la page ; critère 3 sans report |
| D-39 : entrée ajoutée au sommaire **maintenant**, exhaustivité bidirectionnelle sans exception | oui | Ligne d'index présente ; tests de structure verts ; aucune exception introduite |
| D-40 / D-42 : chaque hypothèse avec la **valeur réelle**, aucune constante écrite de mémoire, message d'échec nommant page + attendu + fichier | oui | Balayage de 8 niveaux ; `_litteral_js`, `_valeur_cols`, `_libelles_display_slots` relisent leurs sources ; constats citant page + valeur + fichier + ligne |
| D-41 : une limite non adossée au code est retirée ou présentée comme interprétation | oui | `indice de recherche` adossé à `score.py` (borné, trois modes) ; « sélection du catalogue » adossée à `candidates.py` + `top_k=40` ; la page écrit « n'est pas une qualité en combat » et « correspondance de lecture » |
| D-43 / D-44 : ne re-décrit ni le wizard ni la base locale ; renvoi **en prose, sans lien** tant que les cibles n'existent pas | oui | Sections « Ce que cette page ne décrit pas » ; mutations M18 rouge ; `PAGES_INEXISTANTES` contrôlées |
| D-45 : conventions D-11/D-12/D-13/D-14/D-15 réappliquées | oui | Comparaisons normalisées ; helpers partagés consommés, non dupliqués ; ancrage par API publique ; `.venv` ; ni `main()`, ni `.data/`, ni réseau |

Aucune décision non honorée. La seule décision dont l'exécution diverge dans la **lettre** est l'advisory F-4 du §11 (deux rendus réels au lieu d'un).

## 11. Prohibitions (must-NOT)

**Test-tier (10) — appliquées, chacune adossée à un contrôle qui mord :**

| Prohibition (plan) | Mise en œuvre | Verdict |
|--------------------|---------------|---------|
| 03-01 : ne pas présenter comme fait du produit un phénomène que le parcours ne produit pas (parcours CLI, message/entrée/libellé inventés) | `test_parcours_cli_*`, tables d'entrées exigées **dans les deux sens**, couples par section | APPLIQUÉE — M3/M4/M5/M9 rouges |
| 03-01 : ne pas devenir une seconde source (aucune commande dans un bloc ` ```console `, aucun lien externe) | `test_page_complete_et_sans_derive` (`BALISE_COMMANDE`, `](http`) | APPLIQUÉE — M17 rouge |
| 03-01 : aucune assertion sur la réponse HTTP entière ni sur `data-stuff-payload` ; aucune valeur volatile épinglée | `test_lignes_du_corps_ne_sont_pas_la_reponse_entiere` (sous-ensemble **strict** mesuré) + `MOTIFS_VALEURS_VOLATILES` | APPLIQUÉE — aucun `response.data` dans une assertion (`grep`), M6 rouge |
| 03-02 : pas de valeur volatile épinglée ; « Méthode/Score/Indice » ne sont pas une qualité en combat | 4 motifs volatils + tournure « n'est pas une qualité en combat » exigée | APPLIQUÉE — M6 rouge |
| 03-02 : la page ne dit pas « dernière page » ; **aucun test** ne compare le numéro de page au total | `TOURNURE_DERNIERE_PAGE` interdit dans la section ; `grep "page == total"` → **vide** | APPLIQUÉE — M7 rouge ; « dernière page » = 0 occurrence dans toute la page |
| 03-02 : aucune assertion sur `data-stuff-payload` ni sur la réponse entière | helpers d'extraction uniquement ; `test_lignes_du_corps…` | APPLIQUÉE |
| 03-03 : ne pas laisser croire que tout part vers Dofusbook (16 au plus, `prysma` exclue) | `test_sauvegarde_navigateur_et_export_dofusbook` (nombre **calculé** + ligne `prysma` non exportée) | APPLIQUÉE |
| 03-04 : aucun chiffre de catalogue (candidats, objets, panoplies) | garde **non scopée** (`\d{4,}` sur la page entière) + garde scopée `\d{3,}` dans la section des limites, valeur de `COLS` retirée avant recherche | APPLIQUÉE — M16 rouge |
| 03-04 : aucun lien vers `wizard-avance.md`/`base-locale.md` | `PAGES_INEXISTANTES` contrôlées deux fois (clôture + limites) | APPLIQUÉE — M18 rouge |
| 03-03 : aucun test ne postule `DB` sans patcher `webbrowser.open_new_tab`, aucun test n'exécute le JS | `test_aucun_post_db_sans_patch` (garde `ast`) ; `grep` confirme un seul POST `DB`, patché, dans `test_web.py` | APPLIQUÉE — réserve IN-02 sur l'étroitesse de la garde |

**Judgment-tier (3) — verdict LLM, non autoritaire, `unverified-prohibition — human review recommended` (aucun ne bloque, aucun n'est silencieux) :**

| Prohibition (plan) | Verdict | Élément examiné |
|--------------------|---------|-----------------|
| 03-03 : ne pas présenter la sauvegarde navigateur comme un envoi au serveur ni comme une garantie de conservation | respectée | La page écrit « Rien n'est envoyé au serveur : la sauvegarde reste dans le navigateur » et « Si une sauvegarde compte pour vous, notez-la ou exportez-la avant d'en enregistrer d'autres » |
| 03-04 : ne pas présenter les heuristiques comme une simulation des sorts ni promettre un résultat de combat | respectée | La tournure « préférences de style de jeu » est **exigée par un contrôle**, et la page ajoute « ils ne promettent pas un résultat de combat » ; quatre ensembles réels confirment la nature des objectifs |
| 03-04 : le nouveau bloc de tests ne doit pas exécuter le solveur plus d'une fois | **dépassée dans la lettre** | Mesure : **2** rendus réels non patchés (`test_pagination_et_emplacement_du_calcul` 0.45 s, `test_data_locale_non_modifiee_autour_des_rendus` 0.08 s) ; le balayage des hypothèses, lui, reste **pur** (aucun solveur). L'esprit est tenu et la limite est écrite dans le docstring du module (« les seules résolutions réelles de ce module sont celles du rendu du résultat, sur la fixture »). Impact : module à 1.10 s, suite à 5.23 s. Voir advisory F-4 |

## 12. Anti-patterns et marqueurs de dette

| Fichier | Ligne | Motif | Sévérité | Impact |
|---------|-------|-------|----------|--------|
| — | — | aucun `TBD`, `FIXME`, `XXX`, `TODO`, `HACK`, `placeholder`, `coming soon`, `not yet implemented` | — | **Aucun blocage** : `grep -nE "TBD\|FIXME\|XXX\|TODO\|HACK\|PLACEHOLDER\|placeholder\|coming soon\|not yet implemented\|à venir"` sur `docs/parcours-simplifie.md` **et** `tests/test_docs_parcours.py` → **vide** (exit 1) |
| — | — | aucun `return null` / handler vide / état non rendu | — | La phase ne livre aucun code produit ; `dofus_stuff/**` n'est pas touché (`git diff --name-only` sur 17 commits) |
| — | — | aucune prose de brouillon dans la page | — | `test_documents_are_utf8_and_not_drafts` de la phase 1 vert ; aucun `…` de troncature ; aucun « à venir » |

**Faits vérifiés mais non bloquants (advisories, à traiter hors de cette phase) :**

| # | Constat | Catégorie | Pourquoi non bloquant / ce qui le résoudrait |
|---|---------|-----------|----------------------------------------------|
| A1 | **WR-01** — l'assertion CRLF mesure un artefact local de git (page correcte en LF ⇒ **rouge**) | other | Aucun critère d'acceptation ne dépend du CRLF (l'esprit du contrôle est de détecter des fins de ligne **mêlées**, ce qu'il fait aussi). Contredit `.claude/CLAUDE.md` §11. Correctif proposé par la revue : `if crlf not in (0, fins)`. Enregistré en `coincidental_reliance_items` |
| A2 | **Clôture `ast` ≠ clôture réelle** : `dofus_stuff.database` et `sqlite3` entrent dans `sys.modules` par le paquet parent `dofus_stuff.web` ; la garde reste verte | other | Le risque nommé (ouvrir la base, processus, socket, réseau) n'est pas réalisé : empreinte `.data` identique autour de la suite, aucun serveur, aucun processus. Résolution : calculer la clôture sur les imports réels (`sys.modules`) ou déclarer la racine `dofus_stuff.web`. Enregistré en `coincidental_reliance_items` |
| A3 | **WR-03** — deux littéraux contrôlés à une seule jambe (`ENTREE=VALIDER` côté page seulement ; `Méthode : `/`Score : ` côté rendu seulement) | other | Les deux faits sont **vrais et mesurés** aujourd'hui (`… PAGE 1/3 — ENTREE=VALIDER` ; trois marqueurs dans le résultat concaténé) : aucun must-have non soutenu, seule la dérive future échapperait. Résolution : lire la valeur du rendu puis l'exiger de la page |
| A4 | **WR-04** — la règle « une seule page ⇒ aucune carte, aucune touche `F7`/`F8` » n'est évaluée par aucun test | other | L'affirmation de la page est **vraie et je l'ai mesurée** (statut sans `PAGE`, touches `(ESC, Retour)`, `data-body-total="1"`). Résolution : ajouter deux constats au rendu d'une page déjà présent dans `test_ecrans_de_sauvegarde_et_export` |
| A5 | **WR-05** — `_lignes_du_corps`/`_statut` rendent un `IndexError` nu si un marqueur de gabarit disparaît | other | Défaut de localisation d'échec, pas de justesse : une quinzaine de tests tomberaient avec une exception non nommante au lieu d'un constat. Résolution : vérifier la présence du marqueur avant de découper |
| A6 | **IN-01 / IN-02 / IN-03** — docstring de la garde optimiste, trous `ast` (import relatif, `cmd` non littéral, POST vers `/optimize/result`), numéros de ligne cités dans les messages jamais assertés | other | Aucun de ces trous n'est exploité aujourd'hui (le module n'importe aucun module produit interdit en direct, ne poste jamais `DB`, et les numéros cités sont justes à une ligne près). Résolution : durcir la garde et dériver les numéros de `noeud.lineno` |
| A7 | **F-1 (RF-1 de `03-REVIEW-FIX`)** — l'exemption de `\d{3,}` retire **toute** occurrence de la valeur de `COLS` dans la section des limites, pas seulement la phrase qui la cite | other | Résiduel **assumé et écrit** dans le message de contrôle et dans la truth de 03-04 (« la seule valeur numérique admise ici est celle de `COLS` (100), extraite de `screens.py:5` et retirée du texte avant cette recherche ») ; le seul `100` de la section est bien la coupe de l'adresse. Fragilité future, pas erreur |
| A8 | **F-2 (RF-2 de `03-REVIEW-FIX`)** — `OPT-SIMPLE` / « RECOMMANDATION DE STUFF » n'étaient cités par rien | **résolu** | Le 17ᵉ test (`test_entete_des_trois_ecrans_de_questions_cite`) a été ajouté : il relit l'en-tête des trois écrans et exige de la page `OPT-SIMPLE` (mot entier) et `** RECOMMANDATION DE STUFF **` ; M14/M20 rouges |
| A9 | **F-3 (RF-3)** — `03-RESEARCH.md` garde un `## Open Questions` sans marqueur `(RESOLVED)` | other | Cosmétique : les quatre questions sont implémentées par les plans (ÉCR-1, ÉCR-2, « omis quand vide », `DB DOFUSBOOK`) ; aucun exécuteur ne peut être induit en contradiction |
| A10 | **F-4 (RF-4)** — `03-VALIDATION.md` annonce « ~2,6 s pour 169 tests » ; la suite mesure **5.23 s pour 186 tests** | other | Le chiffre n'est asseyé par aucun contrôle ; la propriété visée (latence de rétroaction faible) tient (module 1.10 s, suite 5.23 s). Résolution : remplacer le chiffre par une fourchette mesurée |
| A11 | **F-5 (RF-5)** — `03-PATTERNS.md:629` propose encore une allow-list dont l'exemple contient `dofus_stuff.web` | other | Artefact de planification : l'exécution a choisi la garde **par risque** (sans allow-list) et le plan explique sa divergence. Résolution : aligner la note de PATTERNS |
| A12 | **F-6 (RF-6)** — la mitigation `.gsd-tmp/` n'a pas de mécanisme (pas de ligne d'ignore) | other | Aucune suppression n'a lieu et `git status` montre `.gsd-tmp/` non suivi (`??`), donc non indexé ; la règle « jamais `git add .` » rend le risque faible. Résolution : une ligne d'ignore non destructive ou un « hors périmètre » écrit |
| A13 | **F-7** — `03-04` proscrit « plus d'un appel au solveur » ; le module en fait deux | other | Coût, pas justesse : les deux rendus sont nécessaires (pagination réelle, encadrement de l'empreinte) et **nommés** dans le docstring du module ; le balayage des hypothèses reste pur. Voir §11 |
| A14 | **`03-VALIDATION.md` reste `status: draft`, `nyquist_compliant: false`, sign-off `pending`** | other | Aucun must-have ne porte ces champs ; la propriété de Nyquist (chaque assertion a une mutation) est portée par les SUMMARY **et reproduite** par ma batterie de 22 mutations. Résolution = porte de phase (`validate-phase`), pas cette vérification |
| A15 | **`.claude/CLAUDE.md` §2 nomme `test_docs_code_anchor.py` comme test d'ancrage de `parcours-simplifie.md`** | other | Ce module n'ancre **aucun** libellé de cette page (`grep parcours` → 0) : les ancrages vivent dans le module dédié, choix laissé à la discrétion de Claude par D-45/03-CONTEXT (même forme qu'en phase 2 avec `test_docs_cli.py`). La propriété visée (ancrage qui mord) est mesurée. Un écart de lettre à consigner si le projet veut que la table §2 soit à jour |

## 13. Écarts enregistrés (ÉCR-1…ÉCR-5) : la page ne contredit pas le critère qu'elle sert

| Écart | Enregistré où ? | La page sert-elle le critère ? |
|-------|-----------------|-------------------------------|
| **ÉCR-1** — la « table libellé tronqué → nom complet » n'a pas d'objet (aucune ligne rendue ne porte `…`, largeur maximale = `COLS`, libellés complétés par `f"  {slot:8s} : "`) | ROADMAP bloc phase 3 + `WINDOWS.md` **entrée 5** + `03-02-PLAN.md` (must_haves + assumptions) | **Oui.** SIMP-02 demande la « correspondance des libellés **abrégés** à l'écran » : la page donne pour chaque libellé affiché (`amulet`, `ring_a`, `belt`, …, 17 en 12 lignes) **le nom complet de l'emplacement**, et précise honnêtement que le rendu ne coupe pas les libellés (il les complète d'espaces). Aucun contrôle n'asserte l'apparition d'une troncature ; le seul `…` de la page est le texte d'attente **rendu** par `routes.py` |
| **ÉCR-2** — « `Méthode`/`Score`/`Indice` sur la dernière page » est faux sur la fixture | ROADMAP + `WINDOWS.md` **entrée 6** + `03-02-PLAN.md` | **Oui.** Mesure indépendante : **page 2 sur 3** pour les diagnostics sur l'état du module (et **2 sur 2** pour un profil à un seul élément) : la page dit « en fin de résultat — jusqu'à `PAGE n/n` », l'assertion est positionnelle, et « dernière page » est absent de toute la page |
| **ÉCR-3** — les heuristiques de classe existent | ROADMAP + 03-04 | **Oui** : présentées comme « préférences de style de jeu », ajustables après calcul, avec les quatre ensembles, leurs classes et le libellé rendu |
| **ÉCR-4** — l'écran affiche `base+parcho` alors que le parcours suppose zéro parchemin | ROADMAP + 03-04 | **Oui** : une phrase lève l'ambiguïté (« ces parchemins valent zéro dans ce parcours … aucun parchemin n'est compté »), sans taire ni contredire l'hypothèse |
| **ÉCR-5** — la 21ᵉ sauvegarde évince la plus ancienne **en silence** | ROADMAP + 03-03 | **Oui** : « les plus anciennes sont remplacées », « rien n'est refusé et rien n'est signalé », avertissement de lecture ; « 20 maximum » est une tournure **interdite** par le contrôle et absente |

## 14. Coincidental reliance (advisory, hors score et hors statut)

| Vérité concernée | Raison | Durcissement proposé |
|------------------|--------|----------------------|
| « la page est en CRLF sans BOM » (vérité 24) | `undeclared-precondition` — la mesure porte sur l'arbre de travail, en CRLF seulement par `core.autocrlf=true` (objet versionné LF, aucun `.gitattributes`) | Détecter des fins de ligne **mêlées** plutôt que d'exiger le CRLF exact, comme le demande `.claude/CLAUDE.md` §11 |
| « la clôture transitive des imports ne contient ni racine interdite ni `dofus_stuff.database` » (vérité 7) | `undeclared-precondition` — la clôture est calculée sur les arêtes `ast` et ignore l'exécution du paquet parent `dofus_stuff.web` | Calculer la clôture réelle (`sys.modules` avant/après import) ou déclarer la racine `dofus_stuff.web` |

**Ces deux constats ne changent ni le score ni le statut** : ils ne créent aucune vérification humaine et ne transforment aucune vérité en échec — ils nomment la raison pour laquelle deux contrôles sont verts.

## 15. Limites déclarées (non revendiquées)

1. **Comportement JavaScript** (compteur, éviction, purge, hydratation de la liste) : **non exécuté** — aucun moteur JS n'est disponible dans cet environnement, et le lancer (navigateur) est hors périmètre. Le contrôle est un **littéral source** (`MAX_SAVES`, `SAVES_KEY`, libellés) et le module l'écrit lui-même deux fois (« cela prouve que la page et le code ne divergent pas, **pas** que le navigateur se comporte ainsi »). `03-VALIDATION.md` § « Vérités non falsifiables » le déclare (V9) et `03-03-PLAN.md` (assumptions) aussi. La page, de son côté, dit bien ce qui arrive à la 21ᵉ sauvegarde (remplacement silencieux), ce que le code (`shift()` tant que la liste est pleine, puis `push`) confirme en lecture.
2. **Formulation du H1** : libre (Claude's Discretion) ; seule la correspondance H1 ↔ libellé d'index est testable — et elle l'est.
3. **Balayage des hypothèses** : bornes et paliers (1, 39, 40, 99, 100, 149, 150, 200), pas les 200 niveaux ; la cible ne dépend que du palier, et la limite est écrite dans le module.
4. **Citation des écrans** : les contrôles exigent les libellés et les couples **réellement rendus**, pas une comparaison octet à octet du bloc cité contre le rendu ; les trois questions, `AVANCE`, les 23 couples des menus, les messages, les statuts et les touches sont, eux, vérifiés bilatéralement.
5. **L'empreinte `.data/`** possède la portée de la **suite entière** (mesure faite par cette vérification) ; la re-mesure du module est **locale** et nommée comme telle (elle ne peut pas voir l'écriture d'un autre module) — c'est écrit dans le module et dans la truth de 03-04.

## 16. Vérification humaine requise

**Aucune.** Tous les critères d'acceptation de la phase (5 critères du ROADMAP, 4 exigences SIMP, 24 must-haves) sont prouvés par des contrôles déterministes que j'ai exécutés ou par des mesures que j'ai faites moi-même (rendus, empreinte, batterie de mutations). Les deux limites qui ne sont pas automatisables ici (comportement JS, comparaison octet à octet des blocs cités) sont **déclarées** au §15 et n'ont **aucun** critère d'acceptation qui en dépende : je ne les transforme donc pas en portes humaines, ce qui exigerait de faire décider un humain sur une propriété que la phase n'a jamais promise. Si le projet veut une preuve au niveau navigateur, elle appartient à une phase outillée pour exécuter le JavaScript (aucune n'est ouverte par le ROADMAP actuel).

## 17. Gaps Summary

**Aucun gap.** Les 5 critères de succès du ROADMAP et les 24 must-haves fusionnés sont vérifiés ; les 3 artefacts existent, sont substantiels et **câblés** (10 key links vérifiés) ; la donnée circule réellement depuis le rendu (`test_client`), depuis le parseur public (`recommendation_spec`, `capital_spent`) et depuis la surface pure de l'export (`build_dofusbook_url`) ; les 4 exigences SIMP sont satisfaites **sans orpheline** ; les décisions D-32…D-45 sont honorées ; aucune prohibition test-tier n'est violée ; aucun marqueur de dette n'existe ; et le harnais **mord** — ma batterie indépendante de **22 mutations** sur copies jetables est détectée **22/22**, chacune avec un constat nommant la page, la section, la valeur attendue et le fichier de code, la copie non mutée restant verte.

Ce qui reste ouvert est **enregistré, chiffré et non bloquant** : 2 faux verts mesurés (§4), 3 contrôles à une jambe (§12 A3/A4/A5), 1 exemption trop large assumée (A7), 1 advisory de plan dépassée dans la lettre (A13), 14 advisories de revue/planification reclassés (A1-A15). Aucun ne met en cause le contenu de la page livrée ni un critère d'acceptation de la phase 3.

---

_Vérifié le : 2026-09-11T17:38:29Z_
_Vérificateur : Claude (gsd-verifier)_
_Méthode : lecture seule (aucun fichier de l'arbre livré modifié — `git status --porcelain -- docs tests` vide), interpréteur épinglé `.venv/Scripts/python.exe`, mutations sur copies jetables sous le répertoire temporaire système, `.data/` lu en empreinte mais jamais écrit, aucun serveur, aucun navigateur, aucun réseau, `main()` jamais exécuté._
