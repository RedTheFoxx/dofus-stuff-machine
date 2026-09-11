---
phase: 05-base-locale-hors-ligne-et-resynchronisation
verified: 2026-09-11T22:37:42Z
status: passed
score: 5/5 must-haves verified (0 present-behavior-unverified, 0 override, 0 gap)
covered_files:
  - .planning/REQUIREMENTS.md
  - .planning/ROADMAP.md
  - .planning/phases/05-base-locale-hors-ligne-et-resynchronisation/05-01-PLAN.md
  - .planning/phases/05-base-locale-hors-ligne-et-resynchronisation/05-01-SUMMARY.md
  - .planning/phases/05-base-locale-hors-ligne-et-resynchronisation/05-02-PLAN.md
  - .planning/phases/05-base-locale-hors-ligne-et-resynchronisation/05-02-SUMMARY.md
  - .planning/phases/05-base-locale-hors-ligne-et-resynchronisation/05-03-PLAN.md
  - .planning/phases/05-base-locale-hors-ligne-et-resynchronisation/05-03-SUMMARY.md
  - .planning/phases/05-base-locale-hors-ligne-et-resynchronisation/05-04-PLAN.md
  - .planning/phases/05-base-locale-hors-ligne-et-resynchronisation/05-04-SUMMARY.md
  - .planning/phases/05-base-locale-hors-ligne-et-resynchronisation/05-CONTEXT.md
  - .planning/phases/05-base-locale-hors-ligne-et-resynchronisation/05-VALIDATION.md
  - docs/base-locale.md
  - docs/sommaire.md
  - tests/test_docs_base_locale.py
  - tests/test_docs_parcours.py
covered_digest: "v1:sha256:63e4a798dfe174036b06acd60664f7a13c25711fb6555fa9165be08f29b8df7e"
behavior_unverified: 0
overrides_applied: 0
re_verification:
  previous_status: gaps_found
  previous_score: 4/5
  gaps_closed:
    - "La fenêtre de re-check de 24 heures est décrite conformément au comportement réel du code — critère de succès 1 du ROADMAP, BASE-01 : les quatre conditions du déclencheur sont énumérées telles que `sync.py:32` les implémente, les absolus « et seulement dans ce cas » et « la seule situation » ont disparu de la page, l'affirmation de la base absente est bornée des deux côtés (ligne 9 et section de la ligne de commande), et le module mesure désormais les six cas du déclencheur avant d'exiger que la page les nomme."
  gaps_remaining: []
  regressions: []
deferred:
  - truth: "La liste « Parcours conseillé » du sommaire ne renvoie qu'à des pages livrées (elle annonce encore « Dépannage » et « Glossaire »)"
    addressed_in: "Phase 6"
    evidence: "Phase 6, nom « Dépannage, glossaire, complétude et preuve finale », critère de succès 3 : « les 8 pages épinglées sont toutes livrées … et le sommaire propose un parcours conseillé final »"
advisory:
  - finding: "05-03-SUMMARY.md annonce la copie verte des batteries de la vague 3 à « 212 passed, 2 skipped » ; je n'ai pas reproduit cette figure"
    category: other
    reason: "Mesure propre, deux tours de suite : la copie du même contenu sans `.data/` rend 215 passed, 3 skipped (218 − 3 `skip` nommés). Le fichier n'est pas touché par le tour de fermeture de gap et la figure ne porte aucun critère de la phase ; aucune preuve déterministe d'un défaut, donc consultatif."
    evidence_status: "none provided"
coincidental_reliance_items:
  - truth: "Les octets de docs/base-locale.md sont en CRLF sur toutes les lignes, UTF-8 sans BOM (must-have du plan 05-03, reconduit par 05-04)."
    reason: undeclared-precondition
    harden: "L'assertion `retours != fins` lit les octets de l'arbre de travail, mais `git ls-files --eol docs/base-locale.md` rend `i/lf w/crlf attr/` : le blob versionné est en LF et la conversion vient de `core.autocrlf=true` (mesuré sur ce poste), aucun `.gitattributes` n'existe. Sur un clone où `core.autocrlf` vaut `false` ou `input`, la même page versionnée arrive en LF et le contrôle rougit pour une raison étrangère au fichier (limite AR-5 déclarée par le module et par 05-04, `verification: backstop`). Durcissement : exiger des fins de ligne homogènes (`if retours not in (0, fins)`) au lieu du CRLF strict."
prohibitions:
  declared: 24
  structured_tiers_declared: 24
  test_tier:
    count: 10
    flagged: 0
    note: "Les dix prohibitions de palier `test` sont armées et mesurées par des contrôles réellement exécutés, et je les ai rejouées dans ce tour : aucune écriture sous `.data/` (empreinte `24989696:1788730056843137500:e3793d64cb79…` identique avant/après la suite entière, avant/après la variante sans réseau et avant/après ma session), aucune connexion réseau (suite entière verte — 219 passed — avec `socket.socket`, `socket.create_connection`, `socket.socketpair` et `urllib.request.urlopen` neutralisés par un greffon de mon cru), aucune synchronisation (les deux points d'entrée de `dofus_stuff/sync.py` sont doublés avant tout appel ; `APPELS_SYNCHRO_PRODUIT` refuse `ensure_up_to_date` et `pull_all` par leur nom), aucune valeur volatile dans la page, avertissement destructeur sur la même ligne que chaque commande, `skip` nommé quand `.data/` est absent. `dispositionForProhibition` n'a rien à signaler ici."
  judgment_tier:
    count: 14
    flagged: 14
    flag: "unverified-prohibition — human review recommended"
    note: "Vérification autonome : les verdicts ci-dessous sont des jugements LLM NON AUTORITATIFS, consignés avec leur preuve, et signalés pour revue humaine. Aucun n'est absorbé en silence dans un vert. Les quatre derniers viennent du plan 05-04."
    verdicts:
      - statement: "Ne jamais modifier dofus_stuff/** pour aligner la documentation (05-01, D-88)."
        judge_verdict: "tenu"
        evidence: "`git diff --name-only HEAD -- dofus_stuff` vide et `git status --porcelain -- dofus_stuff` vide, mesurés dans ce tour."
      - statement: "Ne jamais présenter une commande destructrice comme une étape d'un parcours recommandé ni l'exécuter (05-01, D-80/D-81)."
        judge_verdict: "tenu"
        evidence: "docs/base-locale.md:129 et :131 portent chacune l'avertissement sur sa ligne ; 0 bloc de code dans la page ; ligne 133 dit « ne sont l'étape d'aucun parcours de cette page »."
      - statement: "Ne jamais publier, déployer à distance, pousser vers un dépôt distant ni effectuer d'achat (05-01, D-91)."
        judge_verdict: "tenu"
        evidence: "Aucun commit de la phase n'est un ancêtre de `origin/main` ; tous les commits de la phase (02ff41c, b6bc832, e17308a) sont locaux."
      - statement: "Ne jamais faire rougir un contrôle à cause de README.md, hors mandat de la phase (05-02, D-87)."
        judge_verdict: "tenu"
        evidence: "README.md absente de `git diff --name-only 6a063ff..HEAD` ; suite entière verte."
      - statement: "Ne jamais modifier dofus_stuff/** pour faire passer la page (05-02, D-88)."
        judge_verdict: "tenu"
        evidence: "Idem ci-dessus, mesure de ce tour."
      - statement: "Ne jamais publier, déployer à distance, pousser ni acheter (05-02, D-91)."
        judge_verdict: "tenu"
        evidence: "Historique des commits sans poussée postérieure au 2026-09-07."
      - statement: "Ne jamais réécrire README.md au-delà de la résolution de ses renvois (05-03, D-87)."
        judge_verdict: "tenu"
        evidence: "README.md absente du diff du tour de fermeture, dont sa ligne 80."
      - statement: "Ne jamais présenter l'assertion des fins de ligne comme portable (05-03, AR-5)."
        judge_verdict: "tenu"
        evidence: "Limite écrite dans la docstring du module et reprise en `backstop` par 05-04 ; voir `coincidental_reliance_items`."
      - statement: "Ne jamais revendiquer une exhaustivité de rédaction (05-03, D-85)."
        judge_verdict: "tenu"
        evidence: "Docstring de module : « le module ne revendique aucune exhaustivité de la redaction » ; limites nommées à chaque contrôle."
      - statement: "Ne jamais publier, déployer à distance, pousser ni acheter (05-03, D-91)."
        judge_verdict: "tenu"
        evidence: "Aucune poussée postérieure au 2026-09-07."
      - statement: "Ne jamais modifier dofus_stuff/** pour faire dire a la page ce qu'elle veut (05-04, D-88/D-19)."
        judge_verdict: "tenu"
        evidence: "La page a été conformée au code lu (`sync.py:32`), jamais l'inverse : `git diff --name-only HEAD -- dofus_stuff` vide."
      - statement: "Ne jamais affaiblir un controle existant pour obtenir le vert (05-04)."
        judge_verdict: "tenu"
        evidence: "Seule modification d'un jeu de garde : `CIBLES_DATA_DIR = (\"Database\", \"create_app\")` → `(\"Database\", \"create_app\", \"load\")`. Aucune entrée de `RACINES_INTERDITES`, `APPELS_SUPPRESSION`, `APPEL_PRODUIT`, `APPELS_SYNCHRO_PRODUIT`, `CONFIRMATIONS_INTERDITES`, `REPERTOIRES_ISOLES` ni aucun motif des vagues 1 à 3 n'est retirée (filtre indépendant sur le diff de `b6bc832`)."
      - statement: "Ne jamais presenter comme prouvee une phrase dont l'ancrage n'existe pas (05-04, D-85)."
        judge_verdict: "tenu"
        evidence: "Trois `verification: backstop` déclarés dans les truths du plan (prose au-delà des marques, contact réel de l'API jamais exercé, portabilité CRLF), et repris tels quels dans la docstring du nouveau contrôle."
      - statement: "Ne jamais publier, deployer a distance, pousser vers un depot distant ni effectuer d'achat (05-04, D-91)."
        judge_verdict: "tenu"
        evidence: "Aucune poussée ; aucun `git add .` ; les fichiers non suivis (`gsd-auto*.toml`, `.gsd-tmp/`, `.gsd/`, `.doc-agent/`, `doc-agent.toml`, `.planning/state.json`) restent hors des commits."
---

# Phase 5 : Base locale, hors-ligne et resynchronisation — Rapport de vérification

**But de la phase (ROADMAP § Phase 5) :** un lecteur comprend la base SQLite locale, la fenêtre de
resynchronisation et les deux comportements hors-ligne, et ne lance jamais une commande destructrice
par inadvertance.
**Vérifié :** 2026-09-11T22:37:42Z
**Statut :** passed — 5 critères sur 5 vérifiés ; le gap du critère 1 est fermé et aucun critère 2 à 5
n'a régressé.
**Re-vérification :** oui — fermeture du gap (vérification initiale : `gaps_found`, 4/5, gap unique sur
le critère 1).

## VERDICT DE LA RE-VÉRIFICATION : **PASSED**

Le gap du critère 1 est fermé. Les trois phrases fautives que j'avais relevées (`docs/base-locale.md`
lignes 39, 41 et la nuance de la ligne 9) sont vraies ou bornées, et le contrôle neuf **mesure** le
déclencheur réel avant de juger la page : je l'ai falsifié indépendamment — remise en place de la page
d'avant correction sur une copie → **ROUGE avec les trois constats attendus**, page livrée → **VERT**.
Aucune régression : suite entière `219 passed`, `dofus_stuff/**` intact, gabarit de la page intact.

**Environnement mesuré.** `HEAD = e17308a` ; interpréteur épinglé `./.venv/Scripts/python.exe` (D-15) →
**Python 3.14.7**. Le mode `mvp` de la phase 5 a été vérifié en *goal-backward* sur le but et les cinq
critères de succès, comme les rapports 03 et 04 l'ont fait pour ce milestone documentaire ; le but
n'étant pas une *user story* au sens de `user-story.validate`, je ne l'ai pas traité comme telle.

## Goal Achievement

### Observable Truths (les cinq critères de succès du ROADMAP)

| # | Vérité (critère du ROADMAP) | Statut | Preuve |
|---|------------------------------|--------|--------|
| 1 | `docs/base-locale.md` décrit le fichier `.data/dofus.sqlite3`, les catégories stockées et la fenêtre de re-check de 24 h | ✓ VERIFIED | Fichier, dossier, sept catégories, constante et expression : exacts (mesurés). Fenêtre : les **quatre** conditions réelles du déclencheur sont énumérées et mesurées sur le code (voir § Re-check, phrase W2) ; les deux absolus faux ont disparu, et le contrôle neuf les refuse en s'appuyant sur une mesure. |
| 2 | Les deux défauts hors-ligne sont distingués explicitement et les champs d'état décrits par leurs noms, sans valeur volatile | ✓ VERIFIED (non rouvert) | Mesures du tour initial (parseurs, aides rendues, champs rendus). Fichiers touchés par ce tour : `docs/base-locale.md` (3 phrases dans deux sections hors de ce critère) et le module de test (un contrôle ajouté, aucun contrôle existant affaibli). 0 valeur volatile re-mesurée dans la page. |
| 3 | Les cas non évidents sont couverts : `db status` crée le fichier, `db sync` refuse `--offline`, l'écran web de synchro contacte l'API même hors-ligne | ✓ VERIFIED (non rouvert) | Sections correspondantes de la page **inchangées** (diff `02ff41c` = 3 remplacements, 0 dans ces sections) ; leurs contrôles `test_le_premier_contact_cree_la_base`, `test_le_refus_de_la_synchronisation`, `test_la_synchronisation_web_contacte_l_api`, `test_champs_de_la_ligne_de_commande`, `test_champs_de_la_surface_web` : **PASSED** dans ce tour. |
| 4 | `db clear` et `PURGE OUI` signalées destructrices sur la même ligne et hors de tout parcours ; les contrôles n'écrivent pas sous `.data/`, ne synchronisent pas, n'ouvrent aucune connexion | ✓ VERIFIED (non rouvert) | `test_commandes_destructrices` **PASSED** ; empreinte `.data/` identique avant/après la suite entière ; suite entière verte (219 passed) avec les points d'entrée réseau neutralisés — la phrase de l'écran de synchro est inchangée. |
| 5 | Chaque nom de champ ou de commande cité par la page est produit par le code, et la suite reste verte avec l'interpréteur épinglé | ✓ VERIFIED | Gabarit et noms re-mesurés sur la page livrée : 1 H1 = libellé d'index, 12 titres de niveau 2, `## Source de vérité` en dernier titre, lien de retour en dernière ligne non vide, 141 lignes CRLF, aucun BOM, 0 bloc de code, 0 lien externe, aucune valeur volatile, aucun marqueur de dette. Suite entière `219 passed in 7.49s` ; module seul `14 passed` (dont le contrôle neuf). |

**Score :** 5/5 vérités vérifiées (0 présente-mais-comportement-non-exercé, 0 override, 0 gap).

## Re-check du critère 1 : chaque phrase comparée à l'oracle

L'oracle, relu par moi dans `dofus_stuff/sync.py` :

- `sync.py:32` — `needs_check = force or empty or last_checked is None or (now - last_checked) >= CHECK_INTERVAL_SECONDS`
- `sync.py:33-39` — `if not needs_check: return {"action": "skip", "reason": "within_24h", …}` (avant tout contact)
- `sync.py:41-43` — `if offline:` puis, sur base vide, `raise RuntimeError("Base locale vide et --offline : impossible de synchroniser")`
- `sync.py:51` — `remote_version = fetch_version(timeout=timeout)` (premier contact)
- `sync.py:53-69` — `if (not force and not empty and local_version == remote_version): touch_checked_at(now)` sinon `pull_all(...)`

| # | Phrase de la page (section « La fenêtre de re-check de 24 heures ») | Code qui doit la porter | Verdict |
|---|--------------------------------------------------------------------|-------------------------|---------|
| W1 | « Il note l'instant de son dernier contrôle dans la clé `last_checked_at` de la table `meta` … cette fenêtre est la constante `CHECK_INTERVAL_SECONDS`, déclarée dans `dofus_stuff/sync.py` par l'expression `24 * 60 * 60`. » | `sync.py:11`, `:27-29`, `:57` (`touch_checked_at`) | ✓ **VRAIE** (inchangée, était déjà exacte) |
| W2 | « En ligne, l'outil compare la version du jeu distante à la version locale **dans quatre situations** : la fenêtre de 24 heures est écoulée, la base locale ne porte encore aucun objet, aucun dernier contrôle n'a été enregistré, ou l'option `--force-sync` a été passée. » | `sync.py:32` — les quatre disjonctions, puis `:51` | ✓ **VRAIE** — mes quatre conditions égales à celles du code, et **mesurées** par moi (§ mesure propre) |
| W3 | « En dehors de ces quatre situations — une base remplie, un dernier contrôle enregistré et une fenêtre non écoulée —, le chargement du catalogue s'arrête là : aucune requête réseau n'est émise. » | `sync.py:33-39` | ✓ **VRAIE** — la négation exacte des quatre disjonctions, et 0 contact mesuré sur ce cas |
| W4 | « Quand la comparaison a lieu, l'outil regarde ce qu'elle rend : si les deux versions sont identiques, si la base locale n'est pas vide et si `--force-sync` n'a pas été passée, il se contente de noter le nouvel instant du contrôle ; si les versions diffèrent, ou si la base locale est vide, ou si `--force-sync` a été passée, il récupère tout le catalogue à nouveau. » | `sync.py:53-69` | ✓ **VRAIE** — disjonctions exactes ; mesuré : fenêtre écoulée → `pull_all` 0 fois (simple note), base vide et `--force-sync` → `pull_all` 1 fois |
| W5 | « L'option `--force-sync` court-circuite cette fenêtre » | `sync.py:32` (`force` en tête de `needs_check`) | ✓ **VRAIE** (inchangée) |
| W6 | ~~« Tant que la fenêtre n'est pas écoulée, le chargement du catalogue s'arrête là : aucune requête réseau n'est émise, **et c'est la seule situation où une commande en ligne ne contacte pas l'API**. »~~ | contredit par `sync.py:32` | ✓ **DISPARUE** — remplacée par W2+W3. `grep` des cinq marques d'exclusivité (`seulement dans ce cas`, `uniquement dans ce cas`, `dans ce cas seulement`, `la seule situation`, `la seule condition`) sur toute la page : **aucune occurrence**. |
| W7 | ~~« Quand la fenêtre est écoulée — **et seulement dans ce cas** — l'outil compare la version du jeu distante à la version locale. »~~ | contredit par `sync.py:32` | ✓ **DISPARUE** — remplacée par W4. |
| F1 | « Une base absente n'est donc pas une erreur : c'est une base vide, que l'outil remplit à la première synchronisation, et l'écran web s'ouvre dessus sans se plaindre. » | création par `Database.open` ; web hors-ligne (`skip_sync`) | ✓ **VRAIE pour ces deux parcours** (mesures du tour initial), et **désormais bornée dans la même phrase** |
| F2 | « La ligne de commande y ajoute une limite, décrite plus bas : charger le catalogue en mode hors-ligne sur une base vide l'arrête sur une erreur. » | `sync.py:43` (`RuntimeError`), `cli.py` | ✓ **VRAIE** — mes propre essai : `Catalog.load(data_dir=<vide>, offline=True)` lève exactement « Base locale vide et --offline : impossible de synchroniser » avec 0 contact |
| F3 | Section « Le mode hors-ligne de la ligne de commande » : « Une base locale **vide** … la commande s'arrête alors sur une erreur » | `sync.py:43`, `cli.py` | ✓ **VRAIE** (inchangée) — la contradiction interne lignes 9/61 est donc fermée **des deux côtés**, comme demandé |

Une seule occurrence du mot « seul » subsiste dans la page : ligne 119, « C'est le seul endroit où le
mode hors-ligne ne s'applique pas », sur l'écran `/db/sync`. Elle est **vraie** et hors du gap
(`dofus_stuff/web/routes.py:820` est le seul chemin web qui appelle `ensure_up_to_date`, et il le fait
avec `offline=False` en dur, contrôlé par le module) ; elle est inchangée par ce tour.

## Le contrôle neuf peut-il réellement échouer ? (falsification indépendante)

Je n'ai pas cru l'exécuteur sur parole : j'ai remis la page **d'avant correction** sur une copie, puis
mesuré. Mutations et copies sous `mktemp -d` uniquement, page réécrite au niveau des octets (préserveur
de CR, jamais `sed -i`), jamais l'arbre de travail.

### 1. Copie verte (page livrée) — sinon rien ne serait discriminant

| Mesure | Commande | Résultat réel |
|---|---|---|
| Module seul, copie de la page livrée, sans `.data/` | `python -m pytest tests/test_docs_base_locale.py -q` (cwd = copie) | `13 passed, 1 skipped in 0.82s` — le `skip` est **nommé** (`base locale du depot absente`) |
| Module seul, arbre réel (avec `.data/`) | `python -m pytest tests/test_docs_base_locale.py -v` | **`14 passed in 0.51s`**, dont `test_declencheur_du_controle_de_version PASSED` |
| Suite entière, arbre réel | `python -m pytest -q` | **`219 passed in 7.49s`** (exit 0) |

### 2. Page d'avant correction remise en place (`git show 02ff41c^:docs/base-locale.md`, converti en CRLF : 13 213 octets, 141 lignes, 141 CRLF)

```text
tests\test_docs_base_locale.py:2555: AssertionError
E  AssertionError: base-locale.md : constats sur les conditions du declencheur et sur l'affirmation de la
   base absente : declencheur du controle de version : la condition « base_remplie_jamais_controlee » a ete
   mesuree a 1 contact(s) de `fetch_version` et la section « ## La fenêtre de re-check de 24 heures » ne la
   nomme pas ; … ; absolu sur le declencheur : la section « ## La fenêtre de re-check de 24 heures » porte
   « seulement dans ce cas » ; … ; absolu sur le declencheur : … porte « la seule situation » ; … ; base
   absente presentee comme sans erreur : la section « Le fichier de la base » affirme qu'une base absente
   n'est pas une erreur sans nommer la limite de la ligne de commande ; …
FAILED tests/test_docs_base_locale.py::test_declencheur_du_controle_de_version
1 failed, 12 passed, 1 skipped in 1.03s
```

Trois constats indépendants, avec leurs trois motifs nommés, et **le seul test rouge est celui du
contrôle neuf** — le test des fins de ligne passe, donc la copie n'a pas rougi pour une raison étrangère
au libellé. Le contrôle n'est donc pas aveugle sur le défaut d'origine.

### 3. Morsures de la batterie de 05-04 rejouées par moi, chacune sur une copie **verte avant mutation**

| Morsure | Ce qu'elle casse | Copie verte avant? | Résultat réel | Motif exigé / trouvé |
|---|---|---|---|---|
| `declencheur_omis` | `aucun dernier contrôle` → `un contrôle ancien` (marque du déclencheur « jamais contrôlée » retirée) | oui — `13 passed, 1 skipped in 0.87s` | **suite entière** : `1 failed, 215 passed, 3 skipped in 7.75s` ; `FAILED tests/test_docs_base_locale.py::test_declencheur_du_controle_de_version` ; 4 occurrences du motif | `declencheur du controle de version` ✓ |
| `absolu_reintroduit` | clause d'exclusivité réintroduite dans la section de la fenêtre | oui — `13 passed, 1 skipped in 0.81s` | `1 failed, 12 passed, 1 skipped in 0.85s` | `absolu sur le declencheur` ✓ |
| `erreur_sans_borne` | `La ligne de commande y ajoute une limite` → `La commande y ajoute une limite` | oui — `13 passed, 1 skipped in 0.83s` | `1 failed, 12 passed, 1 skipped in 0.76s` | `base absente presentee comme sans erreur` ✓ |

`3/3` morsures détectées, aucune `MUTATION NON DETECTEE`, aucune copie rouge avant mutation. Le contrôle
mord sur les trois formes exactes du défaut mesuré, et il mord **aussi** quand une clause est simplement
*retirée* (le cas `declencheur_omis`), pas seulement quand une chaîne interdite est ajoutée.

## Mesure propre du déclencheur (hors du harnais de la phase)

J'ai re-dérivé le déclencheur moi-même, avec mon propre script (6 bases sous `tmp_path`, `fetch_version`
et `pull_all` doublés avant l'appel, `Catalog.load`) :

| Cas (ma construction) | `fetch_version` | `pull_all` | Exception | Conditions correspondantes de la page |
|---|---|---|---|---|
| base remplie, fenêtre fraîche | **0** | 0 | — | « En dehors de ces quatre situations … aucune requête réseau » (W3) |
| base remplie, fenêtre écoulée | **1** | 0 | — | « la fenêtre de 24 heures est écoulée » (W2) + note du contrôle (W4) |
| base **vide**, fenêtre fraîche | **1** | 1 | — | « la base locale ne porte encore aucun objet » (W2) |
| base remplie, **jamais contrôlée** | **1** | 0 | — | « aucun dernier contrôle n'a été enregistré » (W2) |
| base remplie, fenêtre fraîche + `force_sync` | **1** | 1 | — | « l'option `--force-sync` a été passée » (W2) |
| base **vide** + `offline=True` | **0** | 0 | `Base locale vide et --offline : impossible de synchroniser` | borne F2/Critère 2 |

Les quatre situations de contact de la page sont exactement les quatre que le code produit, et aucune
cinquième n'existe dans ce chemin : les seuls appelants de `fetch_version`/`ensure_up_to_date` du produit
sont `catalog.py:46` (chargement du catalogue), `cli.py:348` (`db sync`, `force=True`) et
`routes.py:820` (confirmation web, `force=True`).

## Required Artifacts

| Artefact | Attendu | Statut | Détails |
|---|---|---|---|
| `docs/base-locale.md` | La page du sujet, gabarit verrouillé, phrases rendues vraies | ✓ VERIFIED | 13 755 octets, **141 lignes / 141 CRLF**, aucun BOM ; H1 unique `# Base locale` = libellé de l'index ; 12 titres de niveau 2 ; `## Source de vérité` en dernier titre ; `[Retour au sommaire](sommaire.md)` en dernière ligne non vide ; 0 bloc de code, 0 lien externe, 0 valeur volatile, 0 marqueur de dette ; marques d'exclusivité du déclencheur : **0**. |
| `tests/test_docs_base_locale.py` | Module d'ancrage + contrôle du déclencheur mesuré | ✓ VERIFIED | **2 561 lignes / 2 561 CRLF**, aucun BOM ; **14 tests, 14 passed** ; helper `_contacts_mesures` (6 cas, bases `tmp_path`, doubles installés avant l'appel) et `test_declencheur_du_controle_de_version` (5 blocs, constats accumulés, 1 assertion finale) ; seul `skip` : conditionnel et nommé (ligne 2323, `MOTIF_BASE_ABSENTE`). |
| `docs/sommaire.md` | Une seule ligne d'index ajoutée | ✓ VERIFIED (inchangé par ce tour) | Ligne d'index de `base-locale.md` toujours présente ; absente du diff `6a063ff..HEAD`. |
| `tests/test_docs_parcours.py` | Réserve de dette vidée | ✓ VERIFIED (inchangé) | `PAGES_INEXISTANTES = ()` ; fichier absent du diff du tour de fermeture. |
| `.data/dofus.sqlite3` | Non touché | ✓ VERIFIED | `24989696:1788730056843137500:e3793d64cb7939ad1a51837b075b6b95e03d64c878fcb9cc07f86c00bb8fef7b` — **identique** au début, après la suite entière, après la variante sans réseau et à la fin de ma session. |

## Key Link Verification

| From | To | Via | Statut | Détails |
|---|---|---|---|---|
| `docs/base-locale.md` | `dofus_stuff/sync.py` | Enumération des conditions du déclencheur ⟷ `needs_check` (`:32`), `skip` (`:33-39`), garde hors-ligne (`:41-43`), comparaison (`:53-69`) | ✓ WIRED | Ce lien, **sémantique** et non plus seulement nominal, est désormais tenu par une mesure (6 cas) et par une prohibition conditionnée à cette mesure. C'est exactement le chaînon qui manquait au tour initial. |
| `tests/test_docs_base_locale.py` | `dofus_stuff/sync.py` | `fetch_version` / `pull_all` doublés dans le module `dofus_stuff.sync`, puis `Catalog.load` | ✓ WIRED | Les deux points d'entrée réseau sont remplacés avant tout appel ; `APPELS_SYNCHRO_PRODUIT` refuse `ensure_up_to_date` et `pull_all` par leur nom. Aucun socket ouvert. |
| `tests/test_docs_base_locale.py` | `docs/base-locale.md` | Sections `## La fenêtre de re-check de 24 heures` et `## Le mode hors-ligne de la ligne de commande`, marques normalisées | ✓ WIRED | La correspondance va de la mesure vers la page, jamais d'une constante vers la page. |
| `docs/base-locale.md` | `dofus_stuff/database.py`, `api.py`, `cli.py`, `web/routes.py`, `web/static/js/terminal.js` | Constante, libellés rendus, message de refus, phrase d'écran | ✓ WIRED (non rouvert) | Contrôles correspondants PASSED dans ce tour ; section du fichier et section du web inchangées par `02ff41c`. |

## Data-Flow Trace (Level 4)

| Artefact | Variable de données | Source | Produit de la donnée réelle | Statut |
|---|---|---|---|---|
| Page — conditions du déclencheur | `needs_check` et ses quatre disjonctions | `sync.py:32` via `Database.is_empty()` / `last_checked_at()` sur base SQLite `tmp_path` | Oui — 6 cas mesurés, valeurs attendues 0/1/1/1/1/0 exactement reproduites | ✓ FLOWING (était ✗ GAP au tour initial) |
| Page — cas de non-contact | retour `skip` / `reason=within_24h` | `sync.py:33-39` | Oui — 0 contact mesuré, et la page le dit | ✓ FLOWING |
| Page — borne de la base absente | `RuntimeError` de la garde hors-ligne | `sync.py:41-43` | Oui — message réel comparé à la chaîne du produit | ✓ FLOWING |
| Page — libellés CLI et web, catégories, phrase `/db/sync` | rendus de production | `cli.py`, `routes.py`, `ITEM_KINDS`, `SYNC_SOURCES` | Oui (mesures du tour initial, contrôles PASSED ici) | ✓ FLOWING |
| Module — compteurs de contacts | `requetes` des deux doubles | doubles installés dans `dofus_stuff.sync` | Oui — mesure de la décision de production, jamais de la prose | ✓ FLOWING |

## Behavioral Spot-Checks

| Comportement | Commande | Résultat | Statut |
|---|---|---|---|
| Contrôle neuf, arbre réel | `python -m pytest tests/test_docs_base_locale.py -v` | `14 passed in 0.51s` | ✓ PASS |
| Contrôle neuf, page d'avant correction | copie `mktemp -d`, page `02ff41c^` en CRLF, module seul | `1 failed, 12 passed, 1 skipped` + 3 motifs | ✓ PASS (rouge attendu) |
| Morsure `declencheur_omis` | copie verte puis mutation, suite entière | `1 failed, 215 passed, 3 skipped`, motif présent | ✓ PASS |
| Morsures `absolu_reintroduit`, `erreur_sans_borne` | copies vertes puis mutation, module seul | `1 failed` chacune, motifs présents | ✓ PASS |
| Déclencheur mesuré hors du harnais | mon script, 6 cas, `Catalog.load` | 0/1/1/1/1/0 + message hors-ligne exact | ✓ PASS |
| Suite entière, interpréteur épinglé | `python -m pytest -q` | `219 passed in 7.49s`, exit 0 | ✓ PASS |
| Suite entière sans réseau | greffon `no_net` (`socket.socket`, `create_connection`, `socketpair`, `urlopen` neutralisés) | `219 passed in 4.18s` | ✓ PASS |
| Intégrité `.data/` | empreinte `(taille, mtime_ns, sha256)` avant/après chaque étape | identique à la référence de la phase | ✓ PASS |
| `dofus_stuff/**` non modifié | `git diff --name-only HEAD -- dofus_stuff` et `git status --porcelain -- dofus_stuff` | les deux vides | ✓ PASS |
| Garde de clôture renforcée, jamais affaiblie | filtre du diff `b6bc832^..b6bc832` sur les noms des jeux de la garde | seule ligne retirée : l'ancienne `CIBLES_DATA_DIR` (elle gagne `load`), 313 insertions / 1 suppression | ✓ PASS |

## Probe Execution

Aucune sonde `scripts/*/tests/probe-*.sh` n'est déclarée par les plans ou résumés de la phase, et aucune
n'existe dans le dépôt (`find scripts -path '*/tests/probe-*.sh'` → rien). Étape sans objet.

### Decision Coverage

`gsd_run query check.decision-coverage-verify` → `{skipped: false, blocking: false, total: 24, honored: 24, not_honored: []}` — « All trackable CONTEXT.md decisions are honored by shipped artifacts. » (Porte non bloquante ; elle n'influence pas le statut.)

## Requirements Coverage

| Exigence | Plan source | Description | Statut | Preuve |
|---|---|---|---|---|
| BASE-01 | 05-01, **05-04** | Le fichier, les catégories stockées et la fenêtre de resynchronisation | ✓ SATISFAIT | Fichier et catégories exacts (tour initial) ; fenêtre : quatre conditions énumérées, mesurées et contrôlées ; absolus d'exclusivité absents ; base absente bornée des deux côtés. |
| BASE-02 | 05-01 | Les deux comportements hors-ligne et les champs de l'état de la base | ✓ SATISFAIT | Non rouvert ; contrôles correspondants PASSED ; 0 valeur volatile. |
| BASE-03 | 05-02 / 05-03 | Commandes destructrices signalées, jamais présentées comme une étape | ✓ SATISFAIT | Non rouvert ; `test_commandes_destructrices` PASSED ; page inchangée dans ces sections. |

Aucune exigence orpheline : `REQUIREMENTS.md` ne mappe à la phase 5 que BASE-01, BASE-02 et BASE-03,
toutes revendiquées par les plans. `AIDE-01`/`AIDE-02` et `GARD-03`/`GARD-04` appartiennent à la phase 6.

## Anti-Patterns Found

| Fichier | Ligne | Motif | Sévérité | Impact |
|---|---|---|---|---|
| `docs/base-locale.md` | — | Marqueurs `TBD`/`FIXME`/`XXX`/`TODO`/`HACK`/`PLACEHOLDER` | — | **Aucun** — porte des marqueurs de dette franchie proprement. |
| `docs/base-locale.md`, `tests/test_docs_base_locale.py` | — | Stubs, implémentations creuses, valeurs volatiles, liens externes, blocs de code | — | **Aucun** : 0 valeur volatile, 0 lien externe, 0 bloc de code, aucun `return {}` ni libellé de remplacement ; le seul `skip` du module est conditionnel, nommé et vérifié comme tel. |
| `tests/test_docs_base_locale.py` | 2323 | `pytest.skip(MOTIF_BASE_ABSENTE)` | ℹ️ Info | Saute **uniquement** si `.data/dofus.sqlite3` est absent, en portant un motif nommé ; sur ce poste la suite ne saute aucun test (`219 passed`, 0 skipped). Ce n'est pas un test désactivé au sens de la porte de qualité des tests. |

Les absolus faux qui constituaient le 🛑 BLOCKER du tour initial (lignes 39 et 41) et l'avertissement de
la ligne 9 sont **corrigés** : plus aucun blocker, plus aucun avertissement ouvert.

## Advisory (nouveau périmètre, sans preuve déterministe)

| # | Constat | Catégorie | Pourquoi consultatif |
|---|---|---|---|
| 1 | `05-03-SUMMARY.md` annonce la copie verte des batteries de la vague 3 à « 212 passed, 2 skipped » | exactitude de rapport | Figure que je n'ai pas reproduite (la même copie sans `.data/` rend `215 passed, 3 skipped`) ; le fichier n'est pas touché par le tour de fermeture et la ligne ne porte aucun critère. Aucune preuve déterministe d'un défaut → consultatif, jamais bloquant. |

## Human Verification Required

**Aucun.** Les cinq critères de cette phase sont des critères de documentation et de harnais, tous
mesurables automatiquement, et je les ai tous mesurés ; je ne revendique **aucune** validation humaine.
La phase ne présente aucun élément d'interface utilisateur à juger visuellement : la vérification
humaine de parcours y est sans objet. Les points que je n'ai **pas** pu vérifier sont listés ci-dessous
et ne sont comptés ni verts ni comme des éléments de vérification humaine.

## Ce que je n'ai PAS pu vérifier (énoncé franchement)

1. **`main()` jamais exécuté** (règle du run) : l'état `db status` a été observé par la fonction de
   production `_print_db_status` et le refus `db sync` lu par `ast` + `parse_args` lors du tour initial,
   jamais sur un `stderr` réel. Je n'ai rien ajouté à ce point dans ce tour.
2. **Exécution JavaScript de `PURGE OUI` dans un navigateur réel** — non vérifiée (aucun navigateur).
   Vérifié à la place : le libellé rendu par `GET /saves` et le texte de `terminal.js:459-466`.
3. **Portabilité de l'assertion CRLF** hors d'un poste où `core.autocrlf=true` — non vérifiée
   (`core.autocrlf=true` mesuré ici, `git ls-files --eol` rend `i/lf w/crlf attr/`, aucun
   `.gitattributes`). Voir `coincidental_reliance_items`.
4. **Contact réel de l'API Dofusdude** — jamais exercé, par construction : les deux points d'entrée de
   `dofus_stuff/sync.py` sont doublés. Le contrôle prouve la **décision** du produit, pas qu'un appel
   réel réussirait. Déclaré en `backstop` par le plan 05-04 et par la docstring du test.
5. **Absence de réseau prouvée en processus**, pas par une sandbox au niveau de l'OS : la variante verte
   à 219 tests neutralise `socket`/`urllib` dans le processus de test. C'est la même méthode que le tour
   initial ; je la reporte pour ce qu'elle est.
6. **Morsures des vagues 1 à 3 non rejouées dans ce tour** : je les avais rejouées (6/6) au tour initial
   et je n'ai constaté aucune régression (mêmes contrôles, tous PASSED, diff de `dofus_stuff/**` vide).

## Gaps Summary

**Aucun gap.** Le gap unique du tour initial — le critère de succès 1, sur la description de la fenêtre
de re-check — est fermé, et il est fermé en profondeur :

- la page énonce les **quatre** conditions réelles lues dans `dofus_stuff/sync.py:32`, dit le cas de
  non-contact pour ce qu'il est, et ne porte plus aucune marque d'exclusivité du déclencheur ;
- l'affirmation « une base absente n'est pas une erreur » est bornée dans la même phrase par la limite
  mesurée de la ligne de commande, et la section de la ligne de commande continue de dire ce cas — la
  contradiction interne est fermée des deux côtés ;
- la cause profonde est traitée : le harnais **mesure** désormais les six cas du déclencheur sur des
  bases temporaires avant d'exiger que la page les nomme, et la prohibition des absolus est conditionnée
  à la mesure qui la contredit (elle crie parce qu'un contact a été mesuré sur une base vide, jamais à
  vide) ;
- la garde de clôture est renforcée (`CIBLES_DATA_DIR` gagne `load`), aucune autre entrée de garde n'est
  retirée, et aucun contrôle existant n'a été affaibli pour obtenir le vert.

Je l'ai **falsifié moi-même** plutôt que de croire le résumé : page d'avant correction → ROUGE avec ses
trois constats nommés ; page livrée → VERT ; trois morsures rejouées → 3/3 détectées sur copie verte au
préalable. Aucune régression sur les critères 2 à 5 (fichiers inchangés, contrôles PASSED, suite entière
`219 passed`, `dofus_stuff/**` intact, empreinte `.data/` identique).

**Verdict : PASSED.** Le besoin initial de cette phase est livré et vérifié.

---

_Vérifié : 2026-09-11T22:37:42Z_
_Vérificateur : Claude (gsd-verifier)_
