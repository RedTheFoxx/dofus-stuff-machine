---
phase: 05-base-locale-hors-ligne-et-resynchronisation
plan: 03
subsystem: documentation
tags: [markdown, pytest, resolution-de-renvois, dette-denouee, cloture-de-page, crlf, valeurs-volatiles, empreinte-de-base, skip-nomme, morsures, copie-verte-avant-mutation, documentation-francaise]

# Dependency graph
requires: [05-01, 05-02]
provides:
  - "tests/test_docs_base_locale.py : les quatre controles de cloture de la phase — test_renvois_du_readme_resolus (detecteur pur `renvois_morts`, temoin vert et morsure sur copie en memoire), test_renvoi_base_locale_legitime (la dette D-44 denouee par deux renvois), test_page_close_et_sans_valeur_volatile (sections dans les deux sens, octets CRLF sans BOM, valeurs volatiles, liens externes, chemins du bloc Source de verite) et test_data_locale_non_modifiee_autour_des_rendus (empreinte de `.data/dofus.sqlite3` autour des rendus, skip nomme si la base est absente) — le module passe de 9 a 13 tests"
  - "les sept motifs du plan (MOTIF_README, MOTIF_LIEN_D63, MOTIF_SECTION, MOTIF_SOURCE, MOTIF_LIEN_EXTERNE, MOTIF_BASE_ABSENTE, MOTIF_EMPREINTE_CHANGEE) et les constantes de contenu MOTIF_LIEN_MARKDOWN, CIBLES_EXTERNES, TITRE_SECTION_RENVOI, PAGE_PARCOURS, LIEN_RETOUR, TITRE_H1, BASE_LOCALE, RENVOIS_PAGE_VOISINE, MOTIF_JETON_ACCENTS, SUFFIXES_CHEMIN, ECRANS_RENDUS"
  - "la mesure d'integrite de la phase : `.data/dofus.sqlite3` garde taille, mtime_ns et SHA-256 autour des rendus du module ET autour de la suite complete (critere 4, volet integrite)"
  - "la fin de la phase 5 : la page est close, la dette D-44 est denouee et non supprimee, et les trois exigences BASE-01 a BASE-03 sont couvertes (BASE-01/BASE-02 par 05-01, BASE-03 par 05-02 et 05-03)"
affects: [verification-phase-5, phase-6-completude]

# Actuals (#2632) — mesures sur la meme echelle que l'estimate du plan (chars/4 du diff realise).
# L'ecart avec l'estimate (84 000) est consigne tel quel : il mesure le pessimisme de l'estimate,
# pas un travail non fait (les trois taches sont livrees, 9/9 morsures detectees).
actuals:
  tokens: 6842      # chars/4 sur le diff realise (27 370 caracteres ajoutes, 1 fichier, 3 commits)
  tasks: 3
  commits: 3        # MESURE : git rev-list --count 1e2996eb492c7e96d83bc11685db3e78d0a44206..HEAD
  plan_head_before: 1e2996eb492c7e96d83bc11685db3e78d0a44206

# Tech tracking
tech-stack:
  added: []          # aucune dependance ajoutee (pyproject.toml inchange) ; stdlib seulement (re, hashlib, pathlib)
  patterns:
    - "Morsure sur copie verte avant mutation (D-84) : chaque derivee est jouee dans un repertoire temporaire (`mktemp -d`), la copie est mesuree VERTE sur `tests/test_docs_base_locale.py` avant la mutation, et la suite complete est rejouee apres — la copie sans `.data/` n'est jamais rouge pour une raison etrangere (mesure : 212 passed, 2 skipped)"
    - "Motif de morsure porte par une constante ASCII du module, jamais ecrit en clair dans une ligne d'assertion : pytest reproduit la ligne source du `assert`, une valeur en clair y serait trouvee meme sans constat produit"
    - "Une morsure est mesuree DEUX fois : par la batterie du plan (suite complete, tollerante a ce qu'un autre module rougisse pour la meme derive) et sur le module seul, en verifiant que le test vise figure nommément dans les echecs — les deux morsures qui recouvrent un controle de la vague 1 (CRLF, valeur volatile) ont ete verifiees ainsi, aucun bite sterile"
    - "Une mutation qui ajoute un import en tete d'un module de test est un piege : le module de ce plan n'ouvre volontairement pas par `from __future__ import annotations`, et la mutation `data_dir_reel` du plan ajoute une fonction, jamais un import (lecon de la vague 1)"
    - "Un fait d'integrite se mesure par lecture d'octets (`taille`, `mtime_ns`, `sha256`) sur deux instants, jamais par une ouverture SQLite du chemin reel : la mesure est locale et vraie par construction (L-2), et la limite est ecrite dans la docstring du test"

key-files:
  created: []
  modified:
    - tests/test_docs_base_locale.py

key-decisions:
  - "`renvois_morts(texte, racine, fichier=\"\")` porte un troisieme parametre nomme, faute de quoi le constat ne pouvait pas nommer « le fichier controle » exige par l'action : la fonction reste **pure** (elle ne lit aucun fichier, ne fait qu'un test d'existence sous `racine`) et les cibles interdites (ancre, chemin absolu, antislash, `file://`) sont ecartees de la resolution, la prohibition restant au module de structure de `docs/` (D-12, aucune duplication de helper)."
  - "`LIEN_RETOUR = LIGNE_RETOUR` : le litteral de la ligne de retour n'est ecrit qu'une fois dans le module, sous le nom que la vague 1 a epingle ; le nom du plan 05-03 est un alias, jamais une seconde copie de la chaine."
  - "La cloture des sections est comparee **en trois constats** (titre attendu manquant, ordre des titres presents, titre hors de la liste) plutot qu'en un seul : chaque derive dit alors ce qu'elle est, et le controle reste juste quel que soit le nombre d'entrees de `TITRES_SECTION_ATTENDUS` a ce stade."
  - "Le titre de niveau 1 est compare **au caractere pres** (`# Base locale`) ; la normalisation (D-11) ne sert qu'au diagnostic, pour dire qu'un ecart ne tient qu'a la casse ou aux accents. Les titres de niveau 2 restent compares exactement, comme la vague 1 les a epingles."
  - "Les octets de la page sont lus par `read_bytes()` et le texte vient du decode strict de ces octets ; le lecteur local `_texte_page` est utilise quand le decodage reussit, et quand il echoue le constat est produit au lieu de laisser `read_text` lever avant tout constat. Un `read_text` strict aurait transforme une derive d'encodage en erreur, pas en constat localisant."
  - "`ECRANS_RENDUS = (\"/db/status\", \"/db/sync\", \"/db/clear\", \"/saves\")` : chacun doit etre declare par un decorateur `get`/`post` de `routes.py` avant d'etre rendu, sans quoi une empreinte serait comparee autour d'un rendu qui n'a pas eu lieu ; aucun POST n'est emis par ce module (D-81)."
  - "`MOTIF_BASE_ABSENTE = \"base locale du depot absente\"` et `MOTIF_EMPREINTE_CHANGEE = \"empreinte de la base locale modifiee\"` sont les deux motifs du plan 05-03, distincts de ceux de `tests/test_docs_parcours.py` : la chaine du `skip` est celle que la batterie du plan cherche (`-rs`), et le constat d'ecart d'empreinte est celui du module de cette phase."

patterns-established:
  - "Pattern 14 : un renvoi se controle par une fonction **pure** `renvois_morts(texte, racine, fichier)` — les cibles externes et les formes interdites sont ecartees, un constat par cible interne introuvable — et sa morsure vit sur une **copie en memoire** du texte : aucun fichier du depot n'est ecrit pour prouver que le detecteur mord (D-84, D-87)"
  - "Pattern 15 : une dette documentaire est **denouee**, pas supprimee — le renvoi en prose devenu lien est controle des deux cotes (le lien dans la section, le sens conserve), la dette D-44 ne disparait que parce que sa cible existe"
  - "Pattern 16 : une mesure d'integrite locale declare son angle mort (L-2) et nomme le controle qui possede le pouvoir complementaire (la mesure avant/apres autour de la suite complete) ; un `skip` d'une mesure est toujours **nomme**, jamais un vert silencieux"

requirements-completed: [BASE-03]

coverage:
  - id: D1
    description: "Chaque renvoi interne du `README.md` resout depuis la racine du depot (critere 5, D-87) : la fonction pure `renvois_morts` ne rend aucun constat sur le fichier livre, la mesure a un objet (au moins un renvoi interne vu), et la meme fonction signale une copie en memoire du fichier ou la cible du renvoi interne est remplacee par un chemin absent — aucun fichier du depot n'est ecrit"
    requirement: "BASE-03"
    verification:
      - kind: unit
        ref: "tests/test_docs_base_locale.py#test_renvois_du_readme_resolus (temoin vert, mesure avec un objet, morsure sur chaine)"
        status: pass
      - kind: integration
        ref: "batterie de morsures 05-03 tache 1 : 2/2 detectees (`lien_readme_retire`, `renvoi_base_locale_retire`), copie verte avant chaque mutation, et chaque morsure retrouvee sur le module seul"
        status: pass
    human_judgment: false
  - id: D2
    description: "La dette D-44/D-63 est denouee : `docs/parcours-simplifie.md` porte au moins deux renvois vers `base-locale.md`, dont un dans la section « Ce que cette page ne decrit pas », cette section continuant de nommer la base locale en clair, et la cible existant sur disque"
    requirement: "BASE-03"
    verification:
      - kind: unit
        ref: "tests/test_docs_base_locale.py#test_renvoi_base_locale_legitime (deux cibles lues dans le texte : `base locale` et `**base locale**`, lien present dans la section, sens conserve, cible sur disque)"
        status: pass
      - kind: integration
        ref: "batterie de morsures 05-03 tache 1 : `renvoi_base_locale_retire` detectee (2 renvois retires, motif « renvoi en prose sans lien vers la page de la base locale »)"
        status: pass
    human_judgment: false
  - id: D3
    description: "La page est close : les douze titres de `TITRES_SECTION_ATTENDUS` se suivent dans l'ordre, aucun titre de niveau 2 n'est hors de cette liste, `## Source de verite` reste le dernier titre epingle et la derniere ligne non vide reste la ligne de retour ; les octets sont lus en binaire (aucun BOM, UTF-8 strict, CRLF sur toutes les lignes), la page ne porte aucune valeur volatile ni aucun lien externe, et chaque chemin du bloc « Source de verite » existe depuis la racine du depot"
    requirement: "BASE-03"
    verification:
      - kind: unit
        ref: "tests/test_docs_base_locale.py#test_page_close_et_sans_valeur_volatile (controle de cloture, trois constats de structure, octets binaires, valeurs, liens, chemins)"
        status: pass
      - kind: integration
        ref: "batterie de morsures 05-03 tache 2 : 5/5 detectees (`valeur_volatile_ajoutee`, `section_retiree`, `chemin_source_invente`, `lien_externe_ajoute`, `page_en_lf`), copie verte avant chaque mutation ; `section_retiree` et `chemin_source_invente` rejouees SANS perte des CR (le `sed -i` de la batterie convertit le fichier en LF) et le test de cloture rougit sur sa seule mutation"
        status: pass
    human_judgment: false
  - id: D4
    description: "Les controles de la phase n'ecrivent pas sous `.data/` : l'empreinte `(taille, mtime_ns, sha256)` de `.data/dofus.sqlite3` est identique avant et apres les rendus des ecrans `/db/status`, `/db/sync`, `/db/clear` et `/saves` (tous en lecture, aucun POST), la seule operation sur le chemin reel est une lecture d'octets, et la base absente fait **sauter** le controle sur un motif nomme"
    requirement: "BASE-03"
    verification:
      - kind: unit
        ref: "tests/test_docs_base_locale.py#test_data_locale_non_modifiee_autour_des_rendus (empreinte avant/apres, ecrans declares et rendus 200, skip nomme si la base du depot est absente)"
        status: pass
      - kind: integration
        ref: "batterie 05-03 tache 3 : skip nomme verifie sur une copie sans `.data/` (`1 skipped`, motif « base locale du depot absente », exit 0) ; morsure `data_dir_reel` detectee avec la chaine epinglee « repertoire de donnees non isole » ; empreinte identique autour de la suite complete (`24989696:1788730056843137500:e3793d64cb79…`)"
        status: pass
    human_judgment: false
  - id: D5
    description: "La suite entiere est verte avec l'interpreteur epingle et son compteur est releve tel qu'observe : `.venv/Scripts/python.exe -m pytest -q` rend **218 passed** (214 avant ce plan, 13 tests dans le module contre 9), et `.data/dofus.sqlite3` garde taille, mtime_ns et SHA-256 avant et apres elle"
    requirement: "BASE-03"
    verification:
      - kind: integration
        ref: "`.venv/Scripts/python.exe -m pytest -q` -> `218 passed in 6.10s` ; `.venv/Scripts/python.exe -m pytest tests/test_docs_base_locale.py -q` -> `13 passed`"
        status: pass
      - kind: integration
        ref: "empreinte `.data/dofus.sqlite3` mesuree avant et apres la suite complete par la verification du plan : identique (24989696:1788730056843137500:e3793d64cb7939ad1a51837b075b6b95e03d64c878fcb9cc07f86c00bb8fef7b)"
        status: pass
    human_judgment: false

# Metrics
duration: 9min
completed: 2026-09-11
status: complete
---

# Phase 5 : Base locale, hors-ligne et resynchronisation — Plan 05-03 Summary

**La phase 5 est close : la page de la base locale est fermee sur ses sections et sur ses octets, chaque renvoi interne du `README.md` resout depuis la racine du depot, la dette D-44 est denouee par deux renvois legitimes vers `docs/base-locale.md`, et les quatre controles ajoutes sont prouves mordants — neuf derives epinglees font rougir la suite sur une copie verte avant mutation. La base du depot n'est jamais touchee : son empreinte est identique autour des rendus du module comme autour de la suite complete (218 passed avec l'interpreteur epingle).**

## Performance

- **Duration:** 9 min entre le debut de session (21:53:47 UTC) et la fin du plan (~22:02 UTC) ; 3 min 21 s entre le premier et le dernier commit de tache (mesure `git log --format=%cI` : 23:57:26 +02:00 -> 00:00:47 +02:00)
- **Started:** 2026-09-11T21:53:47Z
- **Completed:** 2026-09-11T22:02:00Z
- **Tasks:** 3
- **Files modified:** 1 (511 insertions, **0 suppression**) — `tests/test_docs_base_locale.py` (253/107/151 lignes par tache, **2 249 lignes** au total, contre 1 738 avant ce plan)
- **Commits:** 3, zero fichier supprime (`git diff --diff-filter=D --name-only` sur les trois commits : vide)
- **README.md : aucun octet modifie.** Il figure dans `files_modified` du plan pour pouvoir corriger un renvoi qui ne resoudrait pas ; mesure : ses 6 liens comptent **1 seul renvoi interne** (`docs/sommaire.md`), il resout, et le fichier n'entre donc dans aucun commit (D-87, indexation par chemin explicite).
- **Duree des batteries de morsures :** tache 1 : ~11 s · tache 2 : ~24 s · tache 3 : ~14 s (skip nomme) et ~15 s (morsure `data_dir_reel`) — ordres de grandeur conformes aux 10-20 s / 25-35 s / 5-15 s annonces par le plan (cout assume par D-84).

## Accomplishments

- **Chaque renvoi interne du `README.md` resout, et le detecteur est prouve mordant.** La fonction **pure** `renvois_morts(texte, racine, fichier)` ne lit aucun fichier : elle ecarte les cibles externes (`http://`, `https://`, `mailto:`) et les formes interdites (ancre, chemin absolu, antislash, `file://`, que la garde de `docs/` possede deja), puis rend un constat par cible interne absente sous `racine`. Sur le fichier livre : aucun constat, et la mesure **a un objet** (1 renvoi interne vu, 5 cibles externes ecartees — exactement la mesure de la recherche). La morsure vit sur une **chaine** : la copie en memoire ou `(docs/sommaire.md)` devient `(docs/sommaire.md.absent)` rend un constat — aucun fichier du depot n'est ecrit (D-84, D-87).
- **La dette D-44/D-63 est denouee, pas seulement supprimee.** `docs/parcours-simplifie.md` porte deux renvois vers `base-locale.md` (lignes 5 et 256, cibles lues dans le texte), dont un dans la section `### Ce que cette page ne décrit pas`, et cette section continue de nommer la base locale en clair apres normalisation. Le controle exige les deux faits ensemble et la cible sur disque : le renvoi en prose devenu lien est verifiable parce que sa cible existe desormais.
- **La page est close dans les deux sens.** `test_page_close_et_sans_valeur_volatile` compare la suite des titres de niveau 2 a `TITRES_SECTION_ATTENDUS` **telle qu'elle est a ce stade** (12 titres) : aucun titre attendu manquant, aucun titre de la page hors de la liste, et ceux qui y appartiennent dans l'ordre — trois constats distincts, donc une derive qui dit ce qu'elle est. `## Source de vérité` reste le dernier titre epingle et `[Retour au sommaire](sommaire.md)` la derniere ligne non vide.
- **Les octets sont lus en binaire, jamais sur un texte re-encode** (D-67, D-69, AR-5) : aucun BOM, decodage UTF-8 strict, 141 fins de ligne pour 141 retours chariot. La docstring ecrit que cette assertion depend de `core.autocrlf=true` sur ce poste (**aucun `.gitattributes` dans le depot**) et **n'est pas presentee comme portable** (Pitfall 11, backstop declare).
- **La page n'ouvre aucune porte de sortie et ne fige aucune valeur** : aucun nombre de quatre chiffres ou plus, aucun lien externe ni adresse en clair, et les trois chemins cites entre accents graves du bloc « Source de vérité » (`dofus_stuff/database.py`, `dofus_stuff/sync.py`, `dofus_stuff/api.py`) existent tous depuis la racine du depot — au moins un chemin est exige, chacun est resolu.
- **Les controles de la phase n'ecrivent pas sous `.data/`, et cela est mesure deux fois.** `test_data_locale_non_modifiee_autour_des_rendus` prend l'empreinte `(taille, mtime_ns, sha256)` de `.data/dofus.sqlite3`, rend `/db/status`, `/db/sync`, `/db/clear` et `/saves` par le client de test — tous en **lecture**, aucun POST, chacun devant etre declare par un decorateur `get`/`post` de `routes.py` et rendre 200 — puis reprend l'empreinte et exige l'egalite. Quand la base du depot est absente, le controle **saute** sur le motif nomme `base locale du depot absente` (verifie sur une copie sans `.data/` : `1 skipped`, exit 0), jamais un vert silencieux.
- **`_empreinte` est la troisieme copie assumee du helper** (`tests/test_docs_parcours.py:2557+`, `tests/test_docs_wizard.py:2289+`) : reprise verbatim, jamais factorisee (Pitfall 10), et sa docstring declare la limite **L-2** de `04-SECURITY.md` — c'est une mesure locale, vraie par construction, et le module ne pretend pas prouver autre chose que l'absence d'ecriture pendant ses propres rendus. Le controle qui possede le pouvoir complementaire est la mesure avant/apres la suite entiere, jouee par la porte de fin de phase.
- **Neuf derives epinglees, neuf detectees**, chacune avec le motif exact que la batterie cherche — voir § Verification. Aucune n'a eu besoin d'etre corrigee pour mordre.

## Task Commits

Each task was committed atomically:

1. **Tache 1 : tranche verticale « chaque renvoi du README resout, et la dette D-44 est denouee » (`type="tracer"`)** — `ed69925` (feat)
2. **Tache 2 : la page est close (sections dans les deux sens, octets CRLF sans BOM, valeurs, liens, chemins)** — `baa367c` (feat)
3. **Tache 3 : la base du depot n'est pas touchee par les controles** — `703f2ed` (feat)

**Plan metadata:** `docs(05-03): complete [plan-name] plan` (voir le commit de metadonnees du plan, qui porte ce SUMMARY et la mise a jour de STATE/ROADMAP/REQUIREMENTS).

## Files Created/Modified

- `tests/test_docs_base_locale.py` — **modifie** (253/107/151 lignes, **2 249 lignes** au total, 2 249 fins de ligne pour 2 249 retours chariot, BOM absent). Quatre tests de plus (**13 au total**) — `test_renvois_du_readme_resolus`, `test_renvoi_base_locale_legitime`, `test_page_close_et_sans_valeur_volatile`, `test_data_locale_non_modifiee_autour_des_rendus` ; constantes de motif `MOTIF_README`, `MOTIF_LIEN_D63`, `MOTIF_SECTION`, `MOTIF_SOURCE`, `MOTIF_LIEN_EXTERNE`, `MOTIF_BASE_ABSENTE`, `MOTIF_EMPREINTE_CHANGEE` (les sept du plan) ; constantes de contenu `MOTIF_LIEN_MARKDOWN`, `CIBLES_EXTERNES`, `TITRE_SECTION_RENVOI`, `PAGE_PARCOURS`, `LIEN_RETOUR`, `TITRE_H1`, `BASE_LOCALE`, `RENVOIS_PAGE_VOISINE`, `MOTIF_JETON_ACCENTS`, `SUFFIXES_CHEMIN`, `ECRANS_RENDUS` ; lecteurs et mesures `_cibles_de_liens`, `_cible_interne`, `_corps_du_titre`, `renvois_morts`, `_empreinte`. Les gardes de la vague 1 (`RACINES_INTERDITES`, `APPELS_SUPPRESSION`, `APPEL_PRODUIT`, `APPELS_SYNCHRO_PRODUIT`, `CONFIRMATIONS_INTERDITES`, `CIBLES_DATA_DIR`, `REPERTOIRES_ISOLES`, `MOTIF_DATA_DIR`) et les motifs des vagues 1-2 (`MOTIF_CRLF`, `MOTIF_VOLATILES`, `MOTIF_H1`, `MOTIF_INDEX`, `_texte_page`, `_routes_declarees`) sont **reutilises tels quels**, jamais recopies ni adoucis.
- `README.md` — **inchange** (verifie : `git diff --stat 1e2996e..HEAD` ne montre que le module de test). Aucun octet du bloc de commandes (lignes 77-81, dont la ligne portant la commande destructrice) n'a ete touche : ce bloc est hors du mandat de la phase (D-87) et reste consigne pour la phase 6.

## Verification

Toutes les commandes ont ete executees avec l'interpreteur epingle `./.venv/Scripts/python.exe` (D-15), jamais un `python` nu.

### Tache 1 — `ed69925`

| Commande | Resultat observe |
|---|---|
| `python -m pytest tests/test_docs_base_locale.py -q` | `11 passed in 0.45s` (9 avant ce plan) |
| `python -m pytest tests/test_docs_structure.py tests/test_docs_parcours.py -q` | `32 passed in 0.99s` — gardes existantes inchangees |
| `python -m pytest -q` | `216 passed in 4.83s` |
| batterie `lien_readme_retire` | copie verte avant mutation, puis `mutation detectee (lien_readme_retire), motif "renvoi du README"` |
| batterie `renvoi_base_locale_retire` | copie verte avant mutation, puis `mutation detectee (renvoi_base_locale_retire), motif "renvoi en prose sans lien vers la page de la base locale"` |
| **batterie du plan (tache 1)** | **`morsures 05-03 tache 1 : 2/2 detectees (copie verte avant chaque mutation)`** |
| contre-mesure (module seul, apres mutation) | `1 failed, 10 passed` — `FAILED ...::test_renvois_du_readme_resolus` ; `1 failed, 10 passed` — `FAILED ...::test_renvoi_base_locale_legitime`. Les deux morsures sont portees par le test vise, jamais par un autre. |

**Porte de retroaction du `type="tracer"`** (mode interactif, `HUMAN_VERIFY_MODE=end-of-phase`, `<verify>` entierement automatise) : les trois commandes de verification de la tache ont ete **rejouees de bout en bout** apres la tache 1 — module vert (`11 passed`), gardes existantes vertes (`32 passed`), 2/2 morsures detectees — puis l'execution s'est poursuivie sans point d'arret, aucun echec n'ayant ete observe.

### Tache 2 — `baa367c`

| Commande | Resultat observe |
|---|---|
| `python -m pytest tests/test_docs_base_locale.py -q` | `12 passed in 0.54s` |
| batterie `valeur_volatile_ajoutee` | `mutation detectee (valeur_volatile_ajoutee), motif "valeur volatile"` |
| batterie `section_retiree` | `mutation detectee (section_retiree), motif "section attendue de la page"` |
| batterie `chemin_source_invente` | `mutation detectee (chemin_source_invente), motif "chemin du bloc source de verite"` |
| batterie `lien_externe_ajoute` | `mutation detectee (lien_externe_ajoute), motif "lien externe"` |
| batterie `page_en_lf` | `mutation detectee (page_en_lf), motif "fins de ligne"` |
| **batterie du plan (tache 2)** | **`morsures 05-03 tache 2 : 5/5 detectees (copie verte avant chaque mutation)`** |
| `python -m pytest -q` | `217 passed in 5.82s` |
| contre-mesure (module seul, apres mutation) | `test_page_close_et_sans_valeur_volatile` figure dans les echecs des **cinq** mutations, et pour `section_retiree` comme pour `chemin_source_invente` son constat porte le motif **de sa seule mutation** (« 1 section(s) attendue(s) absente(s) de la page : ## Les commandes destructrices », « la section « ## Source de vérité » cite « dofus_stuff/inexistant.py » et ce chemin n'existe pas ») |
| contre-mesure supplementaire **sans perte des CR** (`.gsd-tmp/suppl_02.py`, hors du depot) | `section_retiree_sans_perte_cr : copie verte avant mutation=True \| rouge=True \| motif present=True \| test de cloture en echec=True` ; `chemin_source_invente_sans_perte_cr : ... True` ; `supplementaires 05-03 tache 2 : OK` |

### Tache 3 — `703f2ed`

| Commande | Resultat observe |
|---|---|
| `python -m pytest -q` | `218 passed in 6.18s` |
| `python -m pytest tests/test_docs_base_locale.py -q` (copie sans `.data/`) | `13 passed`, puis avec `-rs` : `1 skipped` et `SKIPPED [1] tests\test_docs_base_locale.py:2216: base locale du depot absente` — `skip nomme present quand .data/ est absent : 1 skipped`, exit 0 |
| batterie `data_dir_reel` | copie verte avant mutation, puis `mutation detectee (data_dir_reel), motif "repertoire de donnees non isole"` ; sortie : `FAILED ...::test_garde_de_cloture_du_harnais ... repertoire de donnees non isole : la ligne 2253 construit une base avec data_dir = « RACINE_DEPOT »`, `1 failed, 214 passed, 3 skipped` |
| **porte de fin de phase** (`pytest -q` encadre par deux mesures d'empreinte) | `218 passed in 6.10s` et `empreinte .data/ identique autour de la suite complete : 24989696:1788730056843137500:e3793d64cb7939ad1a51837b075b6b95e03d64c878fcb9cc07f86c00bb8fef7b` |

**Bilan des morsures : 9 jouees, 9 detectees, 0 corrigee pour mordre** — 2 (tache 1) + 5 (tache 2) + 1 `skip` nomme + 1 `data_dir_reel`. Les neuf batteries ont d'abord mesure la copie **verte** (copie sans `.data/`, `212 passed, 2 skipped` : aucune copie n'est rouge pour une raison etrangere a sa mutation), et chaque morsure a ete retrouvee sur le **module seul** — le fait que la copie verte avant mutation soit mesuree sur le module tandis que la suite complete est rejouee apres ne rend donc aucune morsure sterile : le test vise figure nommement dans les echecs des huit morsures de mutation.

**Aucun verrou ni coupee de securite** : aucun `git add .`, aucun fichier de `dofus_stuff/**`, `doc-agent.toml`, `.doc-agent/`, `gsd-auto*.toml`, `.planning/state.json` ni `.gsd-tmp/` n'est entre dans un commit ; aucun `push` ; aucun `db clear`, `db sync`, `db status`, `drop` ou suppression sous `.data/` ou `.doc-agent/`.

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 3 — Blocage : le constat ne pouvait pas « nommer le fichier controle »] troisieme parametre `fichier` sur `renvois_morts`**

- **Found during:** Tache 1 (lecture de l'action avant ecriture)
- **Issue:** l'action exige que « chaque constat nomme le fichier controle, la cible fautive et la racine », mais la signature epinglee `renvois_morts(texte: str, racine: Path)` ne porte pas le nom du fichier : un constat ne peut pas nommer ce qu'il ne recoit pas.
- **Fix:** un troisieme parametre **nomme et optionnel** `fichier: str = ""` est ajoute ; la fonction reste **pure** (aucune lecture de fichier, aucun fichier ouvert : seul un test d'existence sous `racine`), et le controle passe `fichier=README`. La docstring declare la limite (seules les cibles de liens Markdown sont vues).
- **Files modified:** `tests/test_docs_base_locale.py` (meme commit que la tache 1)
- **Verification:** `python -m pytest tests/test_docs_base_locale.py -q` -> `11 passed` ; morsures 2/2 detectees.
- **Committed in:** `ed69925`

### Ecarts d'interpretation (documentes, jamais des affaiblissements)

- **Les cibles interdites sont ecartees de la resolution, pas signalees.** L'action dit que `renvois_morts` « rejette » les cibles portant une ancre, un chemin absolu, un antislash ou `file://`. Elles sont **ecartees** (aucun constat de cible morte pour elles) : les signaler dupliquerait la prohibition que `tests/test_docs_structure.py` possede sur `docs/` (D-12), et ce module ne revendique que la resolution des renvois de fichier. La raison est ecrite dans la docstring de `_cible_interne`. Aucune cible interdite n'existe dans le `README.md` mesure : le choix n'adoucit aucun constat sur le fichier livre, et la morsure `lien_readme_retire` reste detectee.
- **Le texte de la page vient du decodage strict des octets, et `_texte_page` sert quand ce decodage reussit.** L'action demande a la fois de lire la page par `_texte_page(docs_dir)` et d'exiger le « decodage UTF-8 strict » comme constat. Or `_texte_page` passe par `read_text(encoding="utf-8")`, qui **leve** avant tout constat : les deux exigences ne peuvent pas tenir ensemble sur des octets non-UTF-8. Le controle produit donc d'abord le constat `MOTIF_CRLF` sur un decodage refuse, puis appelle `_texte_page` quand le decodage reussit (page absente : `AssertionError` localisante, comme le reste du module). Le controle est plus strict, jamais plus permissif.
- **La cloture des sections est ecrite en trois constats distincts** (titre attendu manquant, ordre des titres presents, titre hors de la liste) au lieu d'un seul : chaque derive dit alors ce qu'elle est. Les trois portent `MOTIF_SECTION`, la batterie du plan reste donc servie par n'importe lequel des trois.
- **Le titre de niveau 1 est compare au caractere pres** (`# Base locale`, egalite exacte) ; la fixture `normalize` (D-11) n'intervient que dans le **diagnostic** (« ecart de casse ou d'accent seulement ») et dans le constat « la mesure n'a aucun objet ». Les titres de niveau 2 restent compares exactement, comme la vague 1 les a epingles, et la mesure montre que l'egalite exacte tient sur la page livree.
- **`LIEN_RETOUR = LIGNE_RETOUR`** : le nom du plan 05-03 est un alias du litteral deja epingle par la vague 1, pour que la chaine ne soit pas ecrite deux fois dans le module.

---

**Total deviations:** 1 auto-fixed (Rule 3, un parametre manquant a la signature pour ecrire le constat exige par l'action) et 5 ecarts d'interpretation documents, tous plus stricts ou plus lisibles, aucun plus permissif. Aucun ecart de perimetre : un seul fichier modifie (`git diff --stat 1e2996e..HEAD` : `tests/test_docs_base_locale.py`, 511 insertions, 0 suppression), `README.md` et `pyproject.toml` inchanges, rien de publie, deploye, achete ou supprime.
**Impact on plan:** aucun affaiblissement d'un controle pour obtenir le vert ; la couverture de la phase (critere 5, critere 4 volet integrite, BASE-03) est atteinte telle que le plan la decrit.

## Issues Encountered

- **Le `sed -i` de la batterie du plan convertit tout le fichier en LF.** Sur ce poste (Windows / Git-for-Windows), `sed -i` reecrit le fichier entier sans les CR : dans les copies mutees par `sed`, le controle des fins de ligne rougit **aussi**, pour une raison etrangere a la mutation visee. La batterie du plan reste valide (elle exige `[0-9]+ (failed|error)` **et** le motif nomme), mais elle est **tolerante** sur ce point ; les deux morsures concernees (`section_retiree`, `chemin_source_invente`) ont donc ete **rejouees avec des mutations qui preservent les CR** (`.gsd-tmp/suppl_02.py`, hors du depot) : `motif present=True` et `test de cloture en echec=True` dans les deux cas. Les constats obtenus portent bien le motif de la seule mutation visee, ce qui est la preuve qui compte.
- **Un message de commit a d'abord ete mutile** : les accents graves du corps du message ont ete interpretes par bash (`command substitution`), et le commit `facfda6` ne portait qu'un message tronque. Il a ete **amende immediatement** avec un message ecrit dans un fichier (`git commit --amend -F`), sans changement d'arbre ; le hash de la tache 1 est `ed69925`.
- **Fins de ligne du module** : les ajouts de code sont ecrits en LF ; `tests/test_docs_base_locale.py` a ete ramene en CRLF apres chaque tache, controle a l'appui (2 249 fins de ligne pour 2 249 retours chariot, BOM absent) avant chaque commit.
- **Aucune morsure n'a eu besoin d'etre corrigee pour mordre** : les neuf batteries de cette vague ont ete discriminantes a la premiere execution, et les huit morsures de mutation ont ete contre-mesurees une par une sur le module seul.
- **Registre des fenetres cassees (`.planning/WINDOWS.md`) : ecriture refusee, defaut preexistant.** `gsd-tools windows append` repond `windows_ledger_table_drift` (la table rendue et le bloc JSON du registre divergent deja sur la ligne `id=5`, enregistree par la phase 3, avant cette vague). Aucune entree n'a donc pu etre ajoutee pour l'ecart d'interpretation sur la lecture des octets ; le registre n'a **pas** ete edite a la main, et le defaut preexistant n'a pas ete corrige (hors perimetre de ce plan). Il est signale ici plutot que passe sous silence.
- **Aucun fichier hors perimetre touche** : `git status --short` ne montre, pour les trois commits, que `tests/test_docs_base_locale.py` ; `.gsd-tmp/` (messages de commit, script de contre-mesure) est reste non indexe.

## Limites declarees, jamais revendiquees (D-85)

- **La prose libre de la page n'est pas verifiee** : les controles portent sur les valeurs, les libelles et les structures **cites** ; l'appreciation de redaction, l'invitation ou non a lancer une commande et la lisibilite des avertissements restent hors de portee d'un test (`verification: backstop` du plan).
- **La portabilite de l'assertion CRLF hors d'un poste dont `core.autocrlf` vaut `true` reste non prouvee** (aucun `.gitattributes` dans le depot, AR-5). L'assertion est ecrite la ou la limite vit, et presentee comme telle (`verification: backstop` du plan).
- **Que la suite entiere n'ecrive pas sous `.data/` est mesure par la porte de fin de phase**, pas par le controle du module : `test_data_locale_non_modifiee_autour_des_rendus` est une mesure locale, vraie par construction (L-2 de `04-SECURITY.md`), et il le dit dans sa docstring.
- **L'execution du JavaScript de l'ecran des sauvegardes reste hors d'atteinte** : aucun navigateur n'est lance, la lecture du fichier `terminal.js` par la vague 2 s'arrete au libelle et au traitement du texte.

## Known Stubs

Aucun. Ce plan n'ajoute que des controles de test : aucun chemin de code produit, aucune valeur vide, aucun libelle de remplacement, aucun `TODO`/`FIXME`, aucun test desactive. Le seul `skip` est **conditionnel et nomme** (`base locale du depot absente` quand `.data/dofus.sqlite3` est absent), il est exerce par la batterie de la tache 3, et la suite du poste ne compte aucun test saute (`218 passed`, 0 skipped).

## Threat Flags

Aucun. Les fichiers touches n'introduisent aucune surface nouvelle : pas d'endpoint, pas de chemin d'authentification, pas d'acces fichier nouveau (la lecture d'octets de `.data/dofus.sqlite3` pour l'empreinte est celle du registre de menaces `T-05-13`/`T-05-17`, mitagee par la garde de cloture de la vague 1 et par la mesure avant/apres), aucune dependance ajoutee (`T-05-SC` : sans objet).

## Self-Check

- **Fichiers modifies** : `tests/test_docs_base_locale.py` — `FOUND` (2 249 lignes, 13 tests) ; `README.md` — `inchange`, verifie par `git diff --stat 1e2996e..HEAD` (aucune entree).
- **Commits** : `ed69925` — `FOUND` ; `baa367c` — `FOUND` ; `703f2ed` — `FOUND` (`git log --oneline -3`).
- **Compteur mesure, jamais narre** : `git rev-list --count 1e2996e..HEAD` = **3**, identique au nombre de taches, et le registre de plan (`.git/gsd-plan-head-before-05-03`) porte bien `1e2996eb492c7e96d83bc11685db3e78d0a44206` comme base.
- **Empreinte `.data/dofus.sqlite3`** : `24989696:1788730056843137500:e3793d64cb7939ad1a51837b075b6b95e03d64c878fcb9cc07f86c00bb8fef7b` — identique a la valeur de reference de la vague 2, mesuree avant la session, apres chaque tache et avant/apres la suite complete.

## Self-Check: PASSED


