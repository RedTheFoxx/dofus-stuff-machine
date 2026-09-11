---
phase: 05-base-locale-hors-ligne-et-resynchronisation
plan: 04
subsystem: documentation
tags: [markdown, pytest, mesure-du-declencheur, conditions-reelles, morsures-sur-copie-verte, crlf, code-non-modifie, empreinte-de-base, gap-closure, backstops, documentation-francaise]

# Dependency graph
requires: [05-03]
provides:
  - "docs/base-locale.md : les trois phrases du gap rendues vraies — les quatre conditions reelles du declencheur enumerees dans la section de la fenetre (fenetre ecoulee, base vide, aucun dernier controle enregistre, `--force-sync`), le cas de non-contact dit pour ce qu'il est, et l'affirmation de la base absente bornee par la limite de la ligne de commande mesuree (`sync.py:43`) — la page reste a 141 lignes, sans section ajoutee"
  - "tests/test_docs_base_locale.py : le controle `test_declencheur_du_controle_de_version` et le helper de mesure `_contacts_mesures` (six cas sur bases construites sous `tmp_path`, `dofus_stuff.sync.fetch_version` et `dofus_stuff.sync.pull_all` remplaces par des doubles compteurs avant l'appel), les motifs `MOTIF_DECLENCHEUR`, `MOTIF_ABSOLU_DECLENCHEUR`, `MOTIF_SANS_ERREUR`, les constantes de mesure (`VERSION_DISTANTE`, `MESSAGE_BASE_VIDE`, six noms de cas, `CONTACTS_ATTENDUS`) et de contenu (`MARQUES_DECLENCHEURS`, `MARQUES_NON_CONTACT`, `ABSOLUS_DECLENCHEUR`, `MARQUES_ABSENTE_SANS_ERREUR`, `MARQUES_LIMITE_CLI`, `MARQUES_VIDE_HORS_LIGNE`, `MARQUES_ERREUR_HORS_LIGNE`) — le module passe de 13 a 14 controles"
  - "la garde de cloture RENFORCEE : `CIBLES_DATA_DIR = (\"Database\", \"create_app\", \"load\")` — le `data_dir` du nouvel appel `Catalog.load` est verifie comme les autres, aucune autre entree de la garde n'est retiree"
  - "la fermeture du seul gap de la phase 5 (critere 1 du ROADMAP, BASE-01), harnais compris : la semantique du declencheur n'etait couverte par aucun test, une phrase fausse y restait verte — elle ne peut plus"
affects: [verification-phase-5]

# Actuals (#2632) — mesures sur la meme echelle que l'estimate du plan (chars/4 du diff realise).
# L'ecart avec l'estimate (34 000) est consigne tel quel : il mesure le pessimisme de l'estimate, pas un
# travail non fait (les deux taches sont livrees, 3/3 morsures detectees du premier coup).
actuals:
  tokens: 4800      # chars/4 sur le diff realise (19 198 caracteres ajoutes, 2 fichiers, 2 commits)
  tasks: 2
  commits: 2        # MESURE : git rev-list --count 55e4a3c6435fd1c5bdc04946d56fd0e133967c6d..HEAD
  plan_head_before: 55e4a3c6435fd1c5bdc04946d56fd0e133967c6d

# Tech tracking
tech-stack:
  added: []          # aucune dependance ajoutee (pyproject.toml inchange) ; `time` est la bibliotheque standard, `dofus_stuff.catalog` un module du depot
  patterns:
    - "Mesure avant prohibition (T-05-19) : la liste des formes d'exclusivite de la fenetre n'est **pas** une liste de chaines interdites en dur — elle est appliquee **seulement parce qu'un contact a ete mesure** sur une base vide a fenetre fraiche. Retirer la mesure eteindrait la prohibition au lieu de la laisser crier a vide"
    - "Correspondance mesure -> page, jamais page -> mesure : pour chaque cas dont le compteur rend au moins un contact, la section doit porter une marque de son jeu ; la page est donc jugee sur ce que le code **fait**, pas sur ce que la page raconte du code"
    - "Doubles des deux points d'entree reseau importes dans `dofus_stuff.sync`, installes AVANT l'appel, et mesure prise a travers `Catalog.load` (jamais `ensure_up_to_date`, refuse nommement par la garde `APPELS_SYNCHRO_PRODUIT`) : aucune socket ouverte, aucune synchronisation du produit executee"
    - "Motif de morsure porte par une constante ASCII du module et jamais ecrit en clair dans le message de l'assertion finale : une morsure doit trouver le motif de **son** constat, pas un motif que le message d'accueil porterait de toute facon (lecon T-05-20)"
    - "Page et module edites au niveau des octets par un script du depot (`.gsd-tmp/apply_05_04_*.py`), jamais par `sed -i` : le `sed` de Git-for-Windows convertit le fichier entier en LF et ferait rougir le controle des fins de ligne pour une raison etrangere a la correction"

key-files:
  created: []
  modified:
    - docs/base-locale.md
    - tests/test_docs_base_locale.py

key-decisions:
  - "Les quatre conditions du declencheur sont **lues dans `dofus_stuff/sync.py:32`** (`needs_check = force or empty or last_checked is None or (now - last_checked) >= CHECK_INTERVAL_SECONDS`) et ecrites en clair dans la page comme quatre situations : la page se conforme au code, jamais l'inverse (D-88, D-19). `dofus_stuff/**` n'est jamais modifie — mesure : `git diff --name-only HEAD -- dofus_stuff` vide apres chaque tache."
  - "Le paragraphe de la consequence ne fait plus dependre la comparaison de la seule fenetre : il dit ce que rend la comparaison (versions identiques **et** base non vide **et** pas de `--force-sync` -> l'instant du controle est note ; versions differentes, **ou** base vide, **ou** `--force-sync` -> tout le catalogue est recupere), ce qui est exactement la decision de `sync.py:53-69`."
  - "L'affirmation « une base absente n'est pas une erreur » est bornee dans la section du fichier par la limite mesuree de la ligne de commande (`sync.py:43`) et l'ecran web est nomme comme surface qui s'en accommode : les deux extremites de la contradiction interne relevee par `05-VERIFICATION.md` (lignes 9 et 61) sont donc tenues ensemble, et la section de la ligne de commande reste inchangee."
  - "`_contacts_mesures` rend `(dict[str, int], str)` : le dictionnaire porte les **contacts** mesures (appels a `fetch_version`, seule mesure comparable aux valeurs attendues 0/1/1/1/1/0) et la chaine porte le message du cas hors-ligne, lu sur l'exception reelle. Le double de `pull_all` est installe et compteur lui aussi, mais son compte n'entre pas dans la valeur comparee : sur une base vide le produit appelle les **deux** points d'entree, et additionner les deux compte 2 la ou la mesure attendue est 1."
  - "Le message de l'assertion finale ne contient **aucun** des trois motifs (ils vivent dans les constats et sont interpoles par leur constante) : sans cette precaution, une morsure chercherait son motif dans un message qui le porterait meme si aucun constat n'avait ete produit, et passerait sur une implementation aveugle (T-05-20)."
  - "Le controle est ecrit avec cinq blocs numerotes et **une seule** assertion finale, constats accumules : c'est la regle du depot (phase 2), sans quoi les motifs des blocs 2 a 5 seraient inatteignables des qu'un bloc anterieur produit un constat."
  - "La garde de cloture est renforcee, jamais adoucie : `CIBLES_DATA_DIR` gagne `load` et son commentaire dit pourquoi (`Catalog.load` ouvre la base par `Database`, son `data_dir` est donc verifie comme les deux autres). Aucune entree de `APPELS_SYNCHRO_PRODUIT`, `RACINES_INTERDITES`, `APPEL_PRODUIT`, `CONFIRMATIONS_INTERDITES`, `APPELS_SUPPRESSION` ni aucun jeu de marques ou de motifs des vagues 1 a 3 n'est retiree — mesure : le module garde ses treize controles verts en plus du nouveau."

patterns-established:
  - "Pattern 17 : une prohibition de prose est **conditionnee a la mesure qui la justifie** — la liste des formes d'exclusivite n'est appliquee que si le compteur du cas « base vide a fenetre fraiche » rend au moins un contact ; une liste de chaines interdites en dur vieillirait en interdisant sans preuve"
  - "Pattern 18 : un controle de documentation peut **mesurer le code** avant de juger la page — six cas sur des bases temporaires, deux doubles de reseau, un compteur par cas, puis correspondance condition par condition ; le controle prouve la **decision** du produit et declare honnetement qu'il ne prouve pas qu'un appel reel a l'API reussirait (D-85, D-89)"

requirements-completed: [BASE-01]

coverage:
  - id: D1
    description: "La section « La fenetre de re-check de 24 heures » enonce les **quatre** conditions reelles du declencheur lues dans `dofus_stuff/sync.py:32` (fenetre ecoulee, base vide, aucun dernier controle enregistre, `--force-sync`), dit le cas de non-contact avec sa bonne portee (base remplie, fenetre fraiche, sans `--force-sync` : le chargement s'arrete la, aucune requete reseau n'est emise) et ne porte plus aucune marque d'exclusivite de la fenetre (critere 1 du ROADMAP, BASE-01 ; `05-VERIFICATION.md` lignes 39 et 41)"
    requirement: "BASE-01"
    verification:
      - kind: unit
        ref: "batterie du plan 05-04, tache 1 : section de la fenetre lue en binaire (six fragments exiges, dont « dans quatre situations », « la base locale ne porte encore aucun objet », « aucun dernier contrôle n'a été enregistré » et « En dehors de ces quatre situations ») — exit 0"
        status: pass
      - kind: unit
        ref: "batterie du plan 05-04, tache 1 : octets de la page — 141 lignes, 141 retours chariot, aucun BOM, exit 0"
        status: pass
      - kind: integration
        ref: "morsure `absolu_reintroduit` (clause d'exclusivite reintroduite dans la section) : detection avec le motif « absolu sur le declencheur » sur une copie verte avant mutation ; morsure `declencheur_omis` (marque « aucun dernier contrôle » retiree) : detection avec le motif « declencheur du controle de version »"
        status: pass
    human_judgment: false
  - id: D2
    description: "L'affirmation de la base absente est bornee des deux cotes : la section « Le fichier de la base » nomme la limite de la ligne de commande (« La ligne de commande y ajoute une limite, décrite plus bas : charger le catalogue en mode hors-ligne sur une base vide l'arrête sur une erreur. ») sans contredire la section « Le mode hors-ligne de la ligne de commande », qui continue de dire qu'une base vide arrete la commande sur une erreur (`sync.py:43`, `dofus_stuff/cli.py`)"
    requirement: "BASE-01"
    verification:
      - kind: unit
        ref: "batterie du plan 05-04, tache 1 : fragment « La ligne de commande y ajoute une limite » exige de la section du fichier — exit 0"
        status: pass
      - kind: unit
        ref: "tests/test_docs_base_locale.py#test_declencheur_du_controle_de_version, bloc 5 : toute section portant une marque de `MARQUES_ABSENTE_SANS_ERREUR` doit nommer la limite de la ligne de commande, et la section de la ligne de commande doit dire le cas « vide » et l'arret sur erreur"
        status: pass
      - kind: integration
        ref: "morsure `erreur_sans_borne` (bornage retire de la section du fichier) : detection avec le motif « base absente presentee comme sans erreur » sur une copie verte avant mutation"
        status: pass
    human_judgment: false
  - id: D3
    description: "Le controle **mesure** le declencheur avant de se prononcer, et il **mord** : les six cas (fenetre fraiche sur base remplie, fenetre ecoulee, base vide a fenetre fraiche, base jamais controlee, `--force-sync`, base vide en `--offline`) rendent exactement 0, 1, 1, 1, 1, 0 contacts sur des bases construites sous `tmp_path` avec les deux points d'entree reseau remplaces ; le cas hors-ligne leve en portant le message reel de `sync.py:43` ; chaque condition mesuree est exigee de la page, les marques d'exclusivite sont refusees parce que la mesure les contredit, et les trois derives epinglees font rougir la suite avec leur motif nomme"
    requirement: "BASE-01"
    verification:
      - kind: unit
        ref: "tests/test_docs_base_locale.py#test_declencheur_du_controle_de_version — `14 passed in 0.55s` avec l'interpreteur epingle ; la correspondance est mesuree vers page (bloc 2), le cas de non-contact est exige (bloc 3), la prohibition est conditionnee (bloc 4)"
        status: pass
      - kind: integration
        ref: "**preuve que le controle voit le defaut d'origine** : sur une copie de l'arbre porteuse de la page livree par 05-03 (page d'avant la tache 1), le controle est ROUGE pour trois constats independants — marque « aucun dernier controle » absente, deux marques d'exclusivite presentes (« seulement dans ce cas », « la seule situation ») et affirmation de la base absente non bornee. Mesure : `1 failed, 12 passed, 1 skipped`"
        status: pass
      - kind: integration
        ref: "batterie de morsures 05-04 tache 2 : 3/3 detectees (motifs « absolu sur le declencheur », « declencheur du controle de version », « base absente presentee comme sans erreur »), copie verte avant chaque mutation, 20,4 s ; aucune corrigee pour mordre"
        status: pass
      - kind: integration
        ref: "porte non-regression : `git diff --name-only HEAD -- dofus_stuff` vide apres les deux taches, `219 passed` sur la suite entiere avec l'interpreteur epingle, et l'empreinte `.data/dofus.sqlite3` identique avant et apres la suite complete (24989696:1788730056843137500:e3793d64cb7939ad1a51837b075b6b95e03d64c878fcb9cc07f86c00bb8fef7b)"
        status: pass
    human_judgment: false

# Metrics
duration: 6min
completed: 2026-09-11
status: complete
---

# Phase 5 : Base locale, hors-ligne et resynchronisation — Plan 05-04 Summary

**Le seul gap de la phase 5 est ferme, et il est ferme des deux cotes : la page dit les quatre conditions reelles du declencheur lues dans `dofus_stuff/sync.py:32` au lieu d'affirmer que la fenetre ecoulee en est la seule, et un controle qui **mesure** ces conditions sur six bases temporaires avant de juger la page est desormais arme — il est vert sur la page corrigee, rouge sur la page livree par 05-03, et les trois derives epinglees font rougir la suite avec le motif nomme de leur constat. `dofus_stuff/**` n'est pas touche d'un octet (D-88), aucune synchronisation Dofusdude n'est lancee (D-89), et `.data/dofus.sqlite3` garde son empreinte exacte avant et apres la suite entiere (219 passed avec l'interpreteur epingle).**

## Performance

- **Duration:** ~6 min entre le debut de session (22:26 UTC) et la fin du plan (~22:34 UTC) ; 2 min 30 s entre le premier et le dernier commit de tache (mesure `git log --format=%cI` : 00:29:12 +02:00 -> 00:31:42 +02:00)
- **Started:** 2026-09-11T22:26:00Z
- **Completed:** 2026-09-11T22:34:00Z
- **Tasks:** 2 (tache 1 `type="tracer"`, tache 2 `type="auto"`)
- **Files modified:** 2 (`docs/base-locale.md` 3 insertions / 3 suppressions, `tests/test_docs_base_locale.py` 313 insertions / 1 suppression) — **19 198 caracteres ajoutes** au total
- **Commits:** 2, zero fichier supprime (`git diff --diff-filter=D --name-only 55e4a3c..HEAD` : vide)
- **Duree de la batterie de morsures :** 20,4 s pour trois copies completes et six suites pytest (copie verte + suite complete par mutation) — conforme aux 20-30 s annonces par le plan (cout assume par D-84), et le module seul reste a 0,55 s (`T-05-24` : six cas sur des bases d'une ligne, `pull_all` double, `quiet=True`)

## Accomplishments

- **La page enonce les quatre conditions reelles du declencheur, lues dans le code et non resumees.** `needs_check = force or empty or last_checked is None or (now - last_checked) >= CHECK_INTERVAL_SECONDS` (`sync.py:32`) precede le premier contact `remote_version = fetch_version(timeout=timeout)` (`sync.py:51`) : la section de la fenetre enumere donc les quatre situations — fenetre de 24 heures ecoulee, base locale sans aucun objet, aucun dernier controle enregistre, `--force-sync` — et le seul cas de non-contact est dit pour ce qu'il est (base remplie, dernier controle enregistre, fenetre non ecoulee : le chargement s'arrete la, aucune requete reseau n'est emise, `sync.py:33-39`). Les deux absolus faux de `05-VERIFICATION.md` (lignes 39 et 41) ont disparu, et une marque d'exclusivite formulee autrement reste hors d'atteinte du controle — declare en backstop (D-85).
- **Le paragraphe de la consequence suit la decision reelle de `sync.py:53-69`** : versions identiques **et** base non vide **et** pas de `--force-sync` -> l'instant du controle est note ; versions differentes, **ou** base vide, **ou** `--force-sync` -> tout le catalogue est recupere. La comparaison ne depend plus de la fenetre ecoulee, et le premier paragraphe (cle `last_checked_at`, constante `CHECK_INTERVAL_SECONDS`, expression `24 * 60 * 60`) comme le paragraphe `--force-sync` sont restes inchanges parce qu'ils etaient exacts.
- **L'affirmation de la base absente est bornee, et la contradiction interne est fermee des deux cotes.** La section du fichier affirme l'absence d'erreur pour le premier contact **et** pour l'ecran web, puis nomme exactement la limite mesuree : « La ligne de commande y ajoute une limite, décrite plus bas : charger le catalogue en mode hors-ligne sur une base vide l'arrête sur une erreur. » (`sync.py:43`). La section de la ligne de commande, qui portait deja cette limite (ligne 61 de la verification), reste inchangee : les deux extremites tiennent ensemble.
- **Le nouveau controle mesure avant de juger, et c'est le point du plan (T-05-20).** `_contacts_mesures` construit six bases neuves sous `tmp_path` (`Database(data_dir=tmp_path / <cas>)`), pose l'horodatage du cas (`last_checked_at` absent, frais ou ecoule), remplace `dofus_stuff.sync.fetch_version` et `dofus_stuff.sync.pull_all` par des doubles compteurs **avant** tout appel, puis charge par `Catalog.load(data_dir=..., offline=..., force_sync=..., quiet=True)`. Mesure : 0 contact (base remplie, fenetre fraiche), 1 (fenetre ecoulee), 1 (base vide a fenetre fraiche), 1 (base jamais controlee), 1 (`--force-sync`), 0 (base vide en `--offline`, garde `sync.py:41-43` qui leve avant tout contact en portant « Base locale vide et --offline : impossible de synchroniser »). Aucune socket ouverte, aucune synchronisation du produit executee.
- **La prohibition des marques d'exclusivite est conditionnee a la mesure qui la justifie** : c'est parce qu'un contact a ete mesure sur une base vide a fenetre fraiche que « seulement dans ce cas », « uniquement dans ce cas », « dans ce cas seulement », « la seule situation » et « la seule condition » sont refusees dans cette section — jamais une liste de chaines interdites en dur (pattern 17).
- **Le controle est prouve mordant, et il est prouve voyant.** Trois derives epinglees rejouees sur une copie verte avant mutation, chacune detectee avec le motif nomme de son constat : `absolu_reintroduit` (motif « absolu sur le declencheur »), `declencheur_omis` (motif « declencheur du controle de version »), `erreur_sans_borne` (motif « base absente presentee comme sans erreur »). **Aucune n'a eu besoin d'etre corrigee pour mordre** — et la preuve complementaire, hors du plan, a ete faite : sur une copie portant la page livree par 05-03, le controle est **rouge pour les trois constats independants** annonces par la verification (marque « aucun dernier controle » absente, deux marques d'exclusivite presentes, affirmation non bornee), mesure `1 failed, 12 passed, 1 skipped`.
- **La garde de cloture est renforcee, jamais adoucie** : `CIBLES_DATA_DIR` gagne `load` (le `data_dir` du nouvel appel `Catalog.load` est verifie comme ceux de `Database` et de `create_app`), et aucune autre entree de la garde n'est retiree — les treize controles des vagues 1 a 3 restent verts, le module passe a quatorze.
## Task Commits

Each task was committed atomically:

1. **Tache 1 : la page dit les quatre conditions reelles du declencheur, et borne la base absente (`type="tracer"`)** — `02ff41c` (docs)
2. **Tache 2 : le controle mesure le declencheur reel, exige que la page l'enumere, et mord** — `b6bc832` (test)

**Plan metadata:** `docs(05-04): complete ...` (voir le commit de metadonnees du plan, qui porte ce SUMMARY et la mise a jour de STATE/ROADMAP/REQUIREMENTS).

**Registre de plan** : `.git/gsd-plan-head-before-05-04` porte `55e4a3c6435fd1c5bdc04946d56fd0e133967c6d` (tete avant la premiere tache), et `git rev-list --count 55e4a3c..HEAD` rend **2** — le compte de commits du frontmatter est **mesure**, jamais narre.

## Files Created/Modified

- `docs/base-locale.md` — **modifie** (3 insertions, 3 suppressions, **141 lignes** apres comme avant, 141 retours chariot pour 141 fins de ligne, aucun BOM, 13 213 -> 13 755 octets) :
  - section `## La fenêtre de re-check de 24 heures` : le paragraphe « Tant que la fenêtre n'est pas écoulée … c'est la seule situation où … » est remplace par les deux phrases des quatre conditions et du cas de non-contact ; le paragraphe « Quand la fenêtre est écoulée — et seulement dans ce cas — … » est remplace par la consequence reelle de la comparaison. Le premier paragraphe (constante, expression `24 * 60 * 60`) et le paragraphe `--force-sync` sont **inchanges** ;
  - section `## Le fichier de la base` : la phrase de la base absente gagne l'ecran web et la limite de la ligne de commande (« La ligne de commande y ajoute une limite, décrite plus bas : … »).
  - **Aucun titre de niveau 2 ajoute ni retire** (`TITRES_SECTION_ATTENDUS` reste exactement la liste des douze titres), aucun saut de ligne ajoute, aucun lien externe, aucun nombre de quatre chiffres ou plus, et `[Retour au sommaire](sommaire.md)` reste la derniere ligne non vide.
- `tests/test_docs_base_locale.py` — **modifie** (313 insertions, 1 suppression, **2 561 lignes** contre 2 249, 2 561 retours chariot pour 2 561 fins de ligne, aucun BOM) :
  - imports ajoutes : `time` et `from dofus_stuff.catalog import Catalog` (aucun module de `RACINES_INTERDITES`, aucun `from __future__ import annotations` — le piege de la vague 1 est evite) ;
  - constantes ajoutees : les trois motifs (`MOTIF_DECLENCHEUR`, `MOTIF_ABSOLU_DECLENCHEUR`, `MOTIF_SANS_ERREUR`), `VERSION_DISTANTE`, `MESSAGE_BASE_VIDE`, les six noms de cas (`CAS_*`), `CONTACTS_ATTENDUS`, `MARQUES_DECLENCHEURS`, `MARQUES_NON_CONTACT`, `ABSOLUS_DECLENCHEUR`, `MARQUES_ABSENTE_SANS_ERREUR`, `MARQUES_LIMITE_CLI`, `MARQUES_VIDE_HORS_LIGNE`, `MARQUES_ERREUR_HORS_LIGNE` ;
  - helper `_contacts_mesures(tmp_path, monkeypatch)` et le quatorzieme controle `test_declencheur_du_controle_de_version` (cinq blocs numerotes, constats accumules, une seule assertion finale) ;
  - garde renforcee : `CIBLES_DATA_DIR = ("Database", "create_app", "load")`.
- `dofus_stuff/**` — **jamais touche** : `git diff --name-only HEAD -- dofus_stuff` est vide, mesure apres la tache 1 (batterie 4) et apres la tache 2 (batteries 7 et 8). Aucun fichier supprime, `pyproject.toml` inchange, aucune dependance ajoutee, rien de publie ni de pousse.

## Verification

Toutes les commandes ont ete executees avec l'interpreteur epingle `./.venv/Scripts/python.exe` (D-15), jamais un `python` nu. Les commandes des batteries sont celles du plan, extraites **au caractere pres** du fichier `05-04-PLAN.md` (huit blocs `<automated>`, ecrits en scripts sous `.gsd-tmp/verif-NN.sh`) : aucune n'a ete retapee de memoire.

### Tache 1 — `02ff41c`

| Commande | Resultat observe |
|---|---|
| `python -m pytest tests/test_docs_base_locale.py -q` | `13 passed in 0.45s` (13 avant le plan : le nouveau controle arrive en tache 2) |
| section de la fenetre et section du fichier, fragments exiges | `page : les quatre conditions mesurees du declencheur sont enumerees, le cas de non-contact est dit, et la base absente est bornee par la limite de la ligne de commande` |
| octets de la page (CRLF, BOM) | `page : 141 lignes, 141 CR, aucun BOM` |
| `python -m pytest -q` + `git diff --name-only HEAD -- dofus_stuff` | `218 passed in 4.63s` puis `suite complete verte et code de production inchange (D-88)` |

**Porte de retroaction du `type="tracer"`** (mode interactif, `HUMAN_VERIFY_MODE=end-of-phase`, `<verify>` entierement automatise) : les quatre commandes de verification de la tache ont ete rejouees de bout en bout apres la tache 1 — module vert, fragments presents, octets CRLF sans BOM, suite entiere verte et `dofus_stuff/**` inchange — puis l'execution s'est poursuivie sans point d'arret, aucun echec n'ayant ete observe.

### Tache 2 — `b6bc832`

| Commande | Resultat observe |
|---|---|
| `python -m pytest tests/test_docs_base_locale.py -q` | `14 passed in 0.55s` (13 + 1, aucune erreur) |
| batterie de morsures (trois copies, copie verte mesuree avant chaque mutation) | `mutation detectee (absolu_reintroduit), motif "absolu sur le declencheur"` · `mutation detectee (declencheur_omis), motif "declencheur du controle de version"` · `mutation detectee (erreur_sans_borne), motif "base absente presentee comme sans erreur"` puis `morsures 05-04 tache 2 : 3/3 detectees (copie verte avant chaque mutation)` — 20,4 s |
| `python -m pytest -q` encadre par deux mesures d'empreinte + `git diff --name-only HEAD -- dofus_stuff` | `219 passed in 4.86s` et `empreinte .data/ identique autour de la suite complete : 24989696:1788730056843137500:e3793d64cb7939ad1a51837b075b6b95e03d64c878fcb9cc07f86c00bb8fef7b` — l'etat vide de `git diff --name-only HEAD -- dofus_stuff` est verifie avant **et** apres la suite |
| lecture `ast` du module (appels interdits, `CIBLES_DATA_DIR`) | `module : aucun appel interdit (ni ensure_up_to_date, ni pull_all, ni main, ni suppression) et CIBLES_DATA_DIR porte load` |
| **controle supplementaire, hors du plan** : module seul contre une copie de l'arbre portant la page livree par 05-03 | `1 failed, 12 passed, 1 skipped` — le controle est **ROUGE** sur la page d'avant la tache 1, pour les trois constats independants annonces par `05-VERIFICATION.md` (marque « aucun dernier controle » absente ; deux marques d'exclusivite presentes, « seulement dans ce cas » et « la seule situation » ; affirmation de la base absente non bornee). Le `skip` est **nomme** (`base locale du depot absente`), la copie n'embarque pas `.data/` |

**Empreinte `.data/dofus.sqlite3`** — les trois valeurs reelles, mesurees a trois instants :

| Instant | `taille:mtime_ns:sha256` |
|---|---|
| Avant toute modification (debut de session) | `24989696:1788730056843137500:e3793d64cb7939ad1a51837b075b6b95e03d64c878fcb9cc07f86c00bb8fef7b` |
| Apres la suite complete de la tache 1 | identique |
| Avant et apres la suite complete de la tache 2 (batterie 7) | identique — `empreinte .data/ identique autour de la suite complete : 24989696:1788730056843137500:e3793d64cb7939ad1a51837b075b6b95e03d64c878fcb9cc07f86c00bb8fef7b` |

**Aucun verrou ni coupee de securite** : aucun `git add .` ; indexation par chemin explicite (`docs/base-locale.md`, `tests/test_docs_base_locale.py`) ; `doc-agent.toml`, `.doc-agent/`, `gsd-auto*.toml`, `.planning/state.json` et `.gsd-tmp/` restent non indexes ; aucun `push` ; aucun `db clear`, `db sync`, `db status`, `drop` ni suppression sous `.data/` ou `.doc-agent/`. La base du depot n'a jamais ete ouverte par SQLite : la seule operation sur son chemin reel a ete la lecture d'octets de l'empreinte.

**Bilan des morsures : 3 jouees, 3 detectees, 0 corrigee pour mordre.** Les trois copies ont d'abord ete mesurees **vertes** sur le module (14 passed) et aucune n'a rougi pour une raison etrangere a sa mutation — le `sed -i` du piege d'environnement n'est jamais employe : les trois mutations ecrivent la page par `pathlib` en **preservant les CR**.
## Deviations from Plan

### Auto-fixed Issues

Aucun. Le plan a ete execute tel qu'ecrit : les deux taches, leurs `<action>`, leurs `<verify>` et leurs `<acceptance_criteria>` sont couverts sans correction de cause. Aucune morsure n'a eu besoin d'etre corrigee pour mordre.

### Ecarts d'interpretation (documentes, jamais des affaiblissements)

- **Le controle prend une sixieme fixture (`sections`) au-dela de la signature declaree.** L'action epingle `test_declencheur_du_controle_de_version(docs_dir, section, normalize, tmp_path, monkeypatch)` et demande, dans son bloc 5, d'itérer « pour chaque section de la page qui porte une marque de `MARQUES_ABSENTE_SANS_ERREUR` ». Les deux exigences ne tiennent pas ensemble avec cinq parametres : la fixture `section` rend **un** corps a partir d'un titre connu, et l'en-tete de la page (ce qui precede le premier titre de niveau 2, de titre `None`) n'est atteignable que par la fixture `sections`, seule projection du helper partage (D-12, aucune duplication de helper). Le controle prend donc `sections` en sixieme parametre et parcourt `sections(texte)`, en-tete compris — l'alternative (boucler sur les douze titres de `TITRES_SECTION_ATTENDUS` par `section(...)`) aurait laisse l'en-tete hors du controle. Le controle est **plus large** que la signature ne le suggerait, jamais plus etroit, et aucune assertion n'est affaiblie. `TITRES_SECTION_ATTENDUS` reste par ailleurs comparee dans les deux sens par `test_page_close_et_sans_valeur_volatile`, inchange.
- **Le message de l'assertion finale ne porte aucun des trois motifs.** Les motifs vivent dans les constats, sous forme de constantes interpolees. Ce n'est pas une omission : écrire un motif en clair dans le message d'accueil du controle ferait matcher la morsure de ce motif sur une implementation **aveugle** (le message accompagnerait n'importe quel echec), et la morsure perdrait tout pouvoir de discrimination — précisément le defaut que T-05-20 mitige. Le message final nomme la page, les sections fautives, la valeur mesuree, la valeur attendue et les fichiers producteurs (`SOURCE_SYNC`, `SOURCE_CLI`, D-83), ce que l'action demande ; il ne recite pas les trois motifs.
- **`_contacts_mesures` rend `(contacts, messages.get(CAS_HORS_LIGNE, ""))`** et non une variable `message` unique : chaque cas qui leverait est enregistre sous son propre nom, et le message du cas hors-ligne est lu a la cle qui le concerne. Une variable unique aurait ete ecrasee par l'exception de n'importe quel autre cas, et le constat du bloc 1 aurait alors decrit la mauvaise situation.
- **Les contacts compares sont les appels a `fetch_version`**, pas la somme des deux points d'entree : sur une base vide a fenetre fraiche le produit appelle `fetch_version` **et** `pull_all` (`sync.py:51` puis `:66`), une somme compterait 2 la ou la mesure attendue est 1. Le double de `pull_all` est installe et compteur lui aussi — s'il n'etait pas en place, le vrai `pull_all` tenterait un `api_get` — mais son compte n'entre pas dans la valeur comparee ; la mesure des deux points d'entree est celle du verificateur (`fetch_version` 1, `pull_all` 1).

---

**Total deviations:** 0 auto-fixed et 4 ecarts d'interpretation documentes, tous plus larges ou plus discriminants, aucun plus permissif.
**Impact on plan:** aucun affaiblissement d'un controle pour obtenir le vert ; le gap du critere 1 est couvert ligne par ligne (les trois `missing` du rapport : remplacer l'exclusivite par les conditions reelles, rattacher l'absence de requete a sa vraie condition, borner la phrase de la ligne 9), et le controle « recommande » par la verification est livre avec trois cas de plus qu'elle ne l'exigeait.

## Issues Encountered

- **Le registre des fenetres cassees (`.planning/WINDOWS.md`) reste non alimente.** Aucun stub, aucun test desactive, aucune `verify` non jouee et aucun ecart de perimetre ne sont a consigner pour ce plan : les quatre ecarts ci-dessus sont des choix d'ecriture documentes ici, pas des defauts. Une tentative d'enregistrement de l'ecart de signature a ete faite avec `gsd_run windows append` (kind `deviation`) et son resultat est reporte tel quel dans la reponse d'execution ; le registre n'a **pas** ete edite a la main et le defaut preexistant de la table n'a pas ete corrige (hors perimetre de ce plan).
- **Le `sed -i` de la batterie du plan n'est pas employe pour muter la page** : sur ce poste, `sed -i` reecrit tout le fichier sans les CR, et le controle des fins de ligne rougirait alors pour une raison etrangere a la mutation. Les trois mutations du plan ecrivent la page par `pathlib` (lecture et ecriture d'octets) et **preservent les CR** ; les trois copies sont mesurees vertes avant mutation, ce qui prouve que la discriminance tient.
- **Aucune commande interactive, aucun serveur, aucun reseau** : le module ne poste rien, ne lance pas le produit (`main`), n'appelle ni `ensure_up_to_date` ni les deux points d'entree de synchronisation, et la garde `ast` de la vague 1 le verifie — le controle du declencheur passe par `Catalog.load`, la surface que la page decrit, avec ses deux points d'entree reseau remplaces avant tout appel.
- **Fins de ligne** : la page et le module sont restes en CRLF (141/141 et 2 561/2 561), sans BOM, verifie avant chaque commit — les editions passent par des scripts en `.gsd-tmp/` qui lisent et ecrivent les octets, jamais `sed`.
- **Aucun fichier hors perimetre touche** : `git status --short` ne montre, pour les deux commits, que `docs/base-locale.md` et `tests/test_docs_base_locale.py` ; les modifications preexistantes (`.gitignore`, `.planning/config.json`, `05-01-PLAN.md`) et les fichiers non suivis (`.doc-agent/`, `.gsd-tmp/`, `.gsd/`, `doc-agent.toml`, `gsd-auto*.toml`, `.planning/state.json`) restent hors des commits.

## Limites declarees, jamais revendiquees (D-85)

- **La prose au-dela des marques epinglees reste un jugement** : le controle exige la presence des conditions **mesurees** et l'absence des marques d'exclusivite de la famille epinglee, il ne lit pas le sens des phrases. Une exclusivite formulee autrement que par les cinq chaines de `ABSOLUS_DECLENCHEUR` reste hors d'atteinte — c'est ecrit dans la docstring du test et dans le constat lui-meme (`verification: backstop` du plan).
- **Le contact reel de l'API Dofusdude n'est jamais exerce** : les deux points d'entree de `dofus_stuff/sync.py` sont remplaces par des doubles avant tout appel et la garde de cloture refuse les racines `socket`, `urllib`, `http` et `requests`. Le controle prouve la **decision** de `sync.py`, pas qu'un appel Dofusdude reussirait (`verification: backstop` du plan, D-89).
- **La portabilite de l'assertion CRLF hors d'un poste dont `core.autocrlf` vaut `true` reste non prouvee** (aucun `.gitattributes` dans le depot, limite AR-5) : elle n'est ni revendiquee ni rouverte par ce plan (`verification: backstop`).
- **Les criteres 2 a 5 de la phase, verifies par `05-VERIFICATION.md`, ne sont pas rouverts** : ce plan ne touche ni `docs/sommaire.md`, ni `docs/parcours-simplifie.md`, ni `README.md`, n'ajoute aucune section a la page et ne modifie aucun fichier de `dofus_stuff/**`.

## Known Stubs

Aucun. Ce plan ne touche que trois phrases d'une page et un module de test : aucun chemin de code produit, aucune valeur vide qui remonterait a un rendu, aucun libelle de remplacement, aucun `TODO`/`FIXME`, aucun test desactive. Le seul `skip` du module reste **conditionnel et nomme** (`base locale du depot absente`, quand `.data/dofus.sqlite3` est absent — la copie de morsure ne l'embarque pas : `1 skipped`), et la suite du poste ne compte aucun test saute (`219 passed`, 0 skipped).

## Threat Flags

Aucun. Les fichiers touches n'introduisent aucune surface nouvelle : pas d'endpoint, pas de chemin d'authentification, aucun acces fichier nouveau (les six bases mesurees sont construites sous `tmp_path`, `DEFAULT_DATA_DIR` n'est jamais passe a `Database`, a `create_app` ni a `Catalog.load`), aucune dependance ajoutee (`T-05-SC` : sans objet). Les quatre menaces `high` du registre du plan sont mitigees et mesurees : `T-05-19` (page qui ment) par l'enumeration des conditions lues dans `sync.py:32` et la prohibition conditionnee a la mesure ; `T-05-20` (faux vert) par trois morsures discriminantes sur copie verte avant mutation **et** par la mesure que le controle est rouge sur la page d'avant la correction ; `T-05-21` (base du depot) par l'empreinte identique avant/apres la suite et par `CIBLES_DATA_DIR` renforce ; `T-05-22` (contact reseau d'un controle) par les deux doubles installes avant l'appel et par `APPELS_SYNCHRO_PRODUIT` toujours arme.

## Self-Check

- **Fichiers modifies** : `docs/base-locale.md` — `FOUND` (141 lignes, 141 CR, aucun BOM) ; `tests/test_docs_base_locale.py` — `FOUND` (2 561 lignes, 14 tests) ; `dofus_stuff/**` — `inchange`, verifie par `git diff --name-only HEAD -- dofus_stuff` (aucune entree) et par `git diff --diff-filter=D --name-only 55e4a3c..HEAD` (aucune suppression).
- **Commits** : `02ff41c` — `FOUND` ; `b6bc832` — `FOUND` (`git log --oneline -3`).
- **Compteur mesure, jamais narre** : `git rev-list --count 55e4a3c6435fd1c5bdc04946d56fd0e133967c6d..HEAD` = **2**, identique au nombre de taches, et le registre de plan (`.git/gsd-plan-head-before-05-04`) porte bien cette base.
- **Empreinte `.data/dofus.sqlite3`** : `24989696:1788730056843137500:e3793d64cb7939ad1a51837b075b6b95e03d64c878fcb9cc07f86c00bb8fef7b` — identique a la valeur de reference de la phase, mesuree avant la session, apres la suite de la tache 1 et avant/apres la suite complete de la tache 2.
- **Controle mordant** : 3/3 morsures detectees avec leur motif nomme, copie verte avant chaque mutation ; et sur la page d'avant la correction, le controle est ROUGE pour trois constats independants (mesure reelle : `1 failed, 12 passed, 1 skipped`).

## Self-Check: PASSED
