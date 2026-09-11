---
phase: 01-socle-documentaire-installation-et-harnais-v-rifiable
fixed_at: 2026-09-11T10:54:08Z
review_path: .planning/phases/01-socle-documentaire-installation-et-harnais-v-rifiable/01-REVIEW.md
iteration: 1
findings_in_scope: 6
fixed: 6
skipped: 0
status: all_fixed
---

# Phase 01 : correction de la revue de code

**Corrige le :** 2026-09-11T10:54:08Z
**Revue source :** `.planning/phases/01-socle-documentaire-installation-et-harnais-v-rifiable/01-REVIEW.md`
(statut `issues_found` : 1 critique, 5 avertissements, 3 infos)
**Iteration :** 1

**Resume :**

- Findings dans le perimetre (`critical+warning`) : **6**
- Corriges : **6**
- Ignores : **0**
- Hors perimetre, laisses ouverts : **IN-01, IN-02, IN-03** (niveau Info, hors `fix_scope`)

## Environnement de verification

**Ou les controles ont tourne :** dans le worktree isole
`.claude/worktrees/rf-01-286-1789123760` (branche `gsd-reviewfix/01-286`), avec
l'interpreteur du depot `.venv/Scripts/python.exe -m pytest -q`, depuis la racine du
worktree. Le worktree n'embarque pas `.venv/` : l'interpreteur est celui du checkout
principal et `dofus_stuff` (gele, identique dans les deux arbres) est importe depuis
l'installation editable. Les commits de correction ont ete reportes sur `main` par
fast-forward en fin de passe, donc les comptes ci-dessous sont reproductibles depuis
l'arbre principal.

**Reference avant correctif :** `157 passed`.
**Apres chaque correctif :** `158 passed` (157 + le test d'ancrage ajoute par CR-01).

**Tier 2 (syntaxe)** : `python -c "import ast; ast.parse(...)"` sur chaque fichier
modifie avant chaque commit. **Tier 1** : relecture de chaque zone modifiee.
**Fins de ligne** : `tests/**` reste integralement CRLF (0 fin de ligne LF nue apres les
corrections, verifie octet par octet).

**Methode de preuve de morsure :** la mutation citee par la revue est injectee dans une
copie jetable de l'arbre entier (`tempfile`), puis la **suite complete** y est relancee :
elle doit basculer du vert au rouge en nommant la derive. Aucune mutation n'est appliquee
sous `docs/` du depot, `.data/` n'est ni lu en ecriture ni resynchronise, et aucune
commande destructrice n'a ete lancee.

## Corrections appliquees

### CR-01 : surface d'options web jamais verifiee de la page vers le parseur

**Fichiers modifies :** `tests/test_docs_code_anchor.py`
**Commit :** `3f221b3`
**Statut :** `fixed`
**Correctif applique :** nouveau test
`test_options_citees_par_la_page_sont_acceptees_par_le_parseur` : il derive les options
citees par la section « Lancement de l'interface web » de la page (`OPTION_CITEE`), verifie
que chacune est acceptee par le parseur public (`parse_args`, D-14) puis compare la surface
citee a la surface de `format_help()` (hors `--help`). La table de la page devient
autoritaire dans les deux sens, sans liste codee en dur dans la boucle. Perimetre limite a
la section web, car le reste de la page cite des options de la ligne de commande
(`--force-sync`) qui ne relevent pas de `dofus_stuff/web/__main__.py`.
**Preuve que le correctif mord :** ligne `| --serve | option inventee, absente du parseur |`
ajoutee au tableau des options dans une copie jetable ->
`1 failed, 157 passed` : « installation.md : option(s) citee(s) par la section
« ## Lancement de l'interface web » mais refusee(s) par le parseur : --serve ; attendu chaque
option citee acceptee par dofus_stuff/web/__main__.py::build_parser().parse_args() ».
Avant correctif, la meme mutation donnait `157 passed` (etat reproduit par la revue).

### WR-01 : chemins cites seulement en `.py`/`.toml`, et hors du bloc Source de verite

**Fichiers modifies :** `tests/test_docs_code_anchor.py`
**Commit :** `45ea250`
**Statut :** `fixed`
**Correctif applique :** `CHEMIN_CITE` couvre `.py`, `.toml`, `.js`, `.md`, `.json`, `.sql`
et `test_sources_de_verite_exist` balaie la page entiere ; l'assertion « au moins un chemin
dans le bloc Source de verite » est conservee comme garde-fou contre un motif qui cesserait
de matcher n'importe ou.
**Preuve que le correctif mord (deux mutations, copies jetables) :**
1. `terminal.js` -> `terminal-inexistant.js` dans le bloc Source de verite ->
   `1 failed, 157 passed` : « installation.md : chemin(s) cite(s) comme source mais
   absent(s) du depot : dofus_stuff/web/static/js/terminal-inexistant.js ».
2. les deux chemins de la ligne `Sources :` du pilotage clavier remplaces par
   `routes-inexistant.py` / `terminal-inexistant.js` (hors du bloc, donc invisibles avant) ->
   `1 failed, 157 passed` nommant **les deux** chemins.
Avant correctif, les deux mutations donnaient `157 passed`.

### WR-02 : regle `--debug` muette sur l'entete de la page

**Fichiers modifies :** `tests/test_docs_code_anchor.py`
**Commit :** `9e2f467`
**Statut :** `fixed`
**Correctif applique :** `_sections` expose l'entete (titre `None`) comme premiere section ;
la boucle `--debug` controle desormais ce perimetre et le nomme « l'entete de installation.md,
avant le premier titre de niveau 2 » (D-13 : page, valeur attendue, fichier de code).
**Preuve que le correctif mord :** phrase `--debug` deplacee dans l'entete et mention
« reservee au developpement » retiree, dans une copie jetable ->
`1 failed, 157 passed` : « installation.md : l'entete de installation.md, avant le premier
titre de niveau 2 cite --debug sans preciser qu'il est reserve au developpement ; attendu
« developpement » dans le meme perimetre ». Avant correctif : `157 passed`.

### WR-03 : ancre non reconnue des qu'elle suit un chemin

**Fichiers modifies :** `tests/test_docs_structure.py`
**Commit :** `e5f2be0`
**Statut :** `fixed: requires human verification` (changement de condition de controle :
la regression ne peut pas etre exclue par la seule syntaxe ; elle est ici couverte par les
mutations ci-dessous)
**Correctif applique :** `problemes_liens` et `test_no_anchor_or_absolute_links` testent la
presence de `#` n'importe ou dans la cible ; `problemes_liens` rapporte « ancre interdite »
puis passe la cible (`continue`) pour ne pas la doubler d'un faux « lien mort ». Les liens
externes restent exemptes (test sur `LIENS_EXTERNES` en premier).
**Preuve que le correctif mord :** `[Installation](installation.md#prerequis)` dans
`docs/sommaire.md` d'une copie jetable -> `6 failed, 152 passed`, dont
`test_no_anchor_or_absolute_links`, `test_sommaire_links_resolve` et
`test_all_relative_links_resolve` nommant « ancre interdite : installation.md#prerequis ;
attendu un lien de fichier a fichier vers une page de docs/ ». Avant correctif, la revue
montrait qu'aucun echec ne nommait la regle d'ancre.
Non-regression : un lien externe porteur d'une ancre (`https://exemple.tld/guide#prerequis`)
et un lien `mailto:` ajoutes a `docs/installation.md` -> `158 passed` sur copie jetable :
la regle d'ancre ne deborde pas sur les cibles externes, que la revue declare acceptees.

### WR-04 : cibles du sommaire comparees a des noms de base

**Fichiers modifies :** `tests/test_docs_structure.py`
**Commit :** `b2854f7`
**Statut :** `fixed: requires human verification` (regle de comparaison reecrite ; couverte
par les deux mutations ci-dessous)
**Correctif applique :** une entree d'index est desormais comparee au chemin de la page
**relatif a `docs/`** (`page.relative_to(docs_dir).as_posix()`), des deux cotes de l'egalite
d'ensembles de `problemes_index` ; la recherche du libelle d'index dans `problemes_h1` utilise
la meme cle, sinon la configuration « page imbriquee correctement listee » restait
contradictoire (`cible listee absente` **et** `page non listee`).
**Ecart assume par rapport a la suggestion de la revue :** le filtre `LIENS_EXTERNES` propose
dans le meme extrait de correction n'a **pas** ete applique : il releve de IN-01, hors
perimetre, et le retirer relacherait le controle d'index (une cible externe introduite dans le
sommaire serait alors silencieusement ignoree, alors que D-06 n'y autorise que des pages).
**Preuve que le correctif mord (deux mutations, copies jetables) :**
1. `docs/sub/installation.md` ajoutee et jamais listee -> `3 failed, 155 passed` :
   « sub/installation.md : page non listee dans docs/sommaire.md ; attendu une ligne d'index
   pointant vers sub/installation.md (SOMM-02, D-06) ». Avant correctif : `157 passed`
   (page imbriquee non listee invisible).
2. `docs/sub/glossaire.md` + entree d'index `sub/glossaire.md` (et `../sommaire.md` en retour)
   -> `158 passed` : la configuration est desormais satisfiable. Avant correctif la revue
   mesurait 3 echecs, dont deux exigences contradictoires.

### WR-05 : test de mutation nommant une page livree par la phase 6

**Fichiers modifies :** `tests/test_docs_structure.py`
**Commit :** `479bd1d`
**Statut :** `fixed`
**Correctif applique :** `_nom_page_injectee` derive le nom de la page injectee de l'arbre
analyse (pages presentes + cibles du sommaire) : `page-injectee-mutation.md`, suffixe
incremente en cas de collision. Le nom n'est plus code en dur, et l'assertion sur l'arbre
livre porte sur le meme nom derive : la mutation reste une derive quelle que soit la page
livree ensuite.
**Preuve que le correctif mord (dans les deux sens) :**
1. La mutation continue de mordre : le test passe en detectant la page derivee
   (`158 passed`, et il echoue si `problemes_index` cesse de la signaler).
2. Simulation de la phase 6 (`docs/glossaire.md` + son entree d'index, copie jetable) ->
   `158 passed`, la ou le test echouait avant correctif (`1 failed, 156 passed` d'apres la
   revue) pour une raison sans rapport avec une derive.

## Findings laisses ouverts (hors perimetre)

### IN-01, IN-02, IN-03

**Raison :** niveau **Info** ; `fix_scope` vaut `critical+warning`. Aucun n'a ete corrige
incidemment, ni directement ni au prix d'un avertissement. Consequences connues, assumees :
- IN-01 : une cible externe listee dans le sommaire continue d'etre signalee « cible listee
  absente sur disque » (diagnostic imprecis, mais le controle reste strict).
- IN-02 : une page enregistree avec un BOM UTF-8 est toujours rapportee « 0 titre(s) H1 ».
- IN-03 : `test_docs_code_anchor.py` leve encore un `FileNotFoundError` brut si
  `docs/installation.md` disparait, au lieu du message nomme de `test_docs_structure.py`.
- Residu lie a WR-03 : une cible portant une ancre est desormais correctement diagnostiquee
  « ancre interdite » (regle appliquee), mais reste par ailleurs comptee par
  `problemes_index` comme entree d'index sans page (message secondaire, la suite reste rouge).

## Non-regression : etats futurs legitimes (aucune suite ne devient rouge a tort)

| Etat futur legitime | Attendu | Mesure |
|---|---|---|
| `docs/sub/glossaire.md` listee `sub/glossaire.md` | vert | `158 passed` |
| phase 6 : `docs/glossaire.md` + son entree d'index | vert | `158 passed` |
| le parseur web gagne `--verbose` **et** la page le documente | vert | `158 passed` |
| lien externe porteur d'une ancre dans une page de `docs/` | vert | suite verte |

Le dernier point de contraste confirme la morsure nouvelle sans faux positif : la meme
extension d'option non documentee par la page donne `1 failed, 157 passed` en nommant
`--verbose` et les deux surfaces comparees.

## Verification par correctif

| Correctif | Commit | Suite complete apres correctif |
|---|---|---|
| CR-01 | `3f221b3` | `158 passed` |
| WR-01 | `45ea250` | `158 passed` |
| WR-02 | `9e2f467` | `158 passed` |
| WR-03 | `e5f2be0` | `158 passed` |
| WR-04 | `b2854f7` | `158 passed` |
| WR-05 | `479bd1d` | `158 passed` |

Aucun fichier de production n'a ete modifie (`dofus_stuff/**` intact ; `git status
--porcelain -- dofus_stuff` vide), aucune page de `docs/` n'a ete editee (la prose de la
revue est jugee saine), `README.md` est intact, aucune dependance ajoutee, aucun
sous-dossier cree sous `docs/`, `GUIDE_WIZARD.md` non touche.

---

_Corrige le : 2026-09-11T10:54:08Z_
_Correcteur : Claude (gsd-code-fixer)_
_Iteration : 1_
