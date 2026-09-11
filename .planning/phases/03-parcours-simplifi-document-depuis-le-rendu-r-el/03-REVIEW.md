---
phase: 03-parcours-simplifie-documente
reviewed: 2026-09-11T17:31:03Z
depth: standard
files_reviewed: 3
files_reviewed_list:
  - docs/parcours-simplifie.md
  - docs/sommaire.md
  - tests/test_docs_parcours.py
findings:
  critical: 0
  warning: 5
  info: 3
  total: 8
status: issues_found
---

# Phase 3 : revue de code — « Parcours simplifié documenté depuis le rendu réel »

**Revu :** 2026-09-11T17:31:03Z
**Profondeur :** standard (3 fichiers en périmètre, aucun code produit)
**Statut :** issues_found (0 critique, 5 avertissements, 3 informations)

## Résumé

Périmètre : `docs/parcours-simplifie.md` (269 lignes, 9 sections de niveau 2),
`docs/sommaire.md` (21 lignes, une ligne d'index ajoutée), `tests/test_docs_parcours.py`
(2 734 lignes, 17 tests). `dofus_stuff/**` est en lecture seule et n'a pas été modifié.
Aucun **Critical** : la page ne promet rien de faux, et aucune donnée n'est en jeu.

Ce que la revue a vérifié **et trouvé conforme**, sur mesure et non sur lecture :

- **Suite complète** : `./.venv/Scripts/python.exe -m pytest -q` → **186 passed** (référence de
  la phase). Module seul : **17 passed en 0,88 s** — aucun `skip`, donc
  `test_data_locale_non_modifiee_autour_des_rendus` a bien encadré une résolution réelle.
- **Hygiène des octets** : les trois fichiers sont UTF-8 **sans BOM** et CRLF dans l'arbre de
  travail ; aucun mojibake relevé, 100 lignes accentuées intactes dans la page.
- **Honnêteté des affirmations mesurées** : la page dit « en fin de résultat — jusqu'à
  `PAGE n/n` » et ne dit jamais « dernière page » ; elle ne promet aucune troncature (aucun `…`
  dans « Correspondance des libellés ») ; le plafond de sauvegardes est présenté comme un
  **littéral** `MAX_SAVES = 20` lu dans `terminal.js:15`, jamais comme un JavaScript exécuté.
  Mesures refaites : avec la fixture du résultat, `Méthode : ` et `Score : ` tombent en **page 2
  sur 3**, `Greedy:` et la phrase du catalogue en page 3 — donc ni page fixe, ni dernière page.
  La ligne de statut mesurée vaut `ID DETAIL | SAVE [NOM] | SAVES | EDIT | DB — PAGE 1/3 —
  ENTREE=VALIDER`, et le résultat d'une page vaut la même ligne **sans** `PAGE n/total`, avec la
  seule touche (`ESC`, `Retour`).
- **Exactitude de la page vis-à-vis du code** : vérifiés un par un contre leur porteur réel →
  `5 * (niveau - 1)` (`recommend.py:24`) ; capital 5 / 40 / 995 et consommation totale
  (`solver_spec.py:264-282`) ; paliers de coût 99/199/299/399
  (`solver_spec.py:251-261`) ; paliers PA/PM et base de PA 6→7 au niveau 100
  (`recommend.py:35-36`) ; `Portée` cible 2 puis 4, `Invocation` base 1 cible 3
  (`recommend.py:51-54`) ; objectifs de classe (`recommend.py:45-48`) ; les 9 emplacements omis
  quand ils sont vides (`api.py:384-385`) ; 16 emplacements exportés, `prysma` exclue
  (`dofusbook_export.py`) ; URL d'import Dofusbook (`dofusbook_export.py:21`) ; libellés de la
  barre des sauvegardes et du détail (`terminal.js:370`, `:400`) ; éviction silencieuse
  (`terminal.js:295-297`) ; `N` / `DEL N` numérotés à partir de 1 (`terminal.js:475-490`) ;
  ouverture navigateur et coupe de l'adresse (`routes.py:1332-1336`). **Aucune affirmation
  fausse trouvée dans la page.**
- **Les pièges nommés dans le contexte de phase sont effectivement évités** : lecture par lignes
  du corps et jamais sur `data-stuff-payload` (`_lignes_du_corps`, ligne 282), comparaison
  **par section** des couples numéro → libellé (`_couples_de_section`, ligne 331), aucune valeur
  volatile figée (`MOTIFS_VALEURS_VOLATILES`, ligne 221), rendu réel du résultat passé par la
  fixture déterministe et jamais par la base du dépôt.

Ce qui reste : cinq **contrôles à une jambe** (verts dans le sens qui ne prouve rien, silencieux
sur la dérive réelle) et trois **notes de solidité** sur les gardes `ast`. Aucun n'exige de
toucher la page ; tous portent sur le harnais.

## Narrative Findings (AI reviewer)

### Warnings

#### WR-01 : l'assertion CRLF mesure un artefact local de git, pas la page

**Fichier :** `tests/test_docs_parcours.py:2533-2547` (la page, `docs/parcours-simplifie.md`)
**Constat :** `if fins != crlf:` exige que les octets de **l'arbre de travail** soient tous en
CRLF. Or `git ls-files --eol docs/parcours-simplifie.md` répond
`i/lf  w/crlf  attr/` : l'objet versionné est en **LF**, l'arbre de travail n'est en CRLF que
parce que `core.autocrlf=true` est un réglage **local** (`git check-attr -a` ne rend aucun
attribut : pas de `.gitattributes`). L'assertion est donc verte ici pour une raison qui n'a rien
à voir avec la page : sur un clone où `core.autocrlf` vaut `false` ou `input` (poste Linux,
`git clone` non configuré), la **même page commitée** arrive en LF et ce test rougit alors que la
page est correcte. C'est le défaut dominant déjà rencontré deux fois dans le projet — un contrôle
vert pour la mauvaise raison, et rouge sur un artefact correct — et il contredit la note de la
pile projet (`.claude/CLAUDE.md`, « Version Compatibility » : « ne pas asserter sur les octets de
fin de ligne »), le dépôt n'ayant pas les moyens de versionner ces octets.
Le fichier lui-même est **conforme** (CRLF, sans BOM) : le constat porte sur l'assertion, pas sur
la page.
**Correction :** garder le contrôle du BOM et remplacer l'égalité stricte par la détection du
vrai piège (des fins de ligne **mêlées** dans un même fichier), qui ne dépend d'aucune config git :

```python
if crlf not in (0, fins):
    constats.append(
        f"{PAGE} : {MOTIF_CRLF} — les octets portent {fins} fin(s) de ligne pour {crlf} CRLF, "
        f"soit des fins de ligne melees ; attendu un fichier homogene, le CRLF n'etant pas "
        f"versionne (aucun .gitattributes, core.autocrlf local)"
    )
```

#### WR-02 : un commentaire affirme le contraire de la mesure enregistrée (ÉCR-2)

**Fichier :** `tests/test_docs_parcours.py:2597-2600` (commentaire du test d'empreinte)
**Constat :** « Les diagnostics tombent sur la derniere page du resultat, donc les pages sont
concatenees… » — la mesure contredit cette phrase : avec la fixture, `Méthode : ` et `Score : `
sont en **page 2 sur 3**, et `test_pagination_et_emplacement_du_calcul` n'est positionnel que
précisément parce qu'ils **ne** sont **pas** sur la dernière page. C'est le tour (« dernière
page ») que le plan 03-02 a explicitement écarté et que `TOURNURE_DERNIERE_PAGE` (ligne 217)
interdit à la page : un lecteur du module prendrait ce commentaire pour la règle attendue, et la
justification de la concaténation des pages deviendrait fausse dès qu'on la recopie.
Le comportement du test, lui, est correct (comparaison sur les pages concaténées).
**Correction :** reformuler, par exemple : « La position des diagnostics est relative à la fin du
résultat, pas à la dernière page (mesure : page 2/3 sur la fixture, ECR-2) : les pages sont
concaténées avant la recherche, jamais indexées sur un numéro fixe. »

#### WR-03 : ancrage à une seule jambe pour les libellés du résultat

**Fichier :** `tests/test_docs_parcours.py:920-928` et `:203` — la page, lignes 140 et 142
**Constat :** deux dérives silencieuses, symétriques :

1. `ENTREE=VALIDER` (page:140) est exigé **côté page** (ligne 921) mais **jamais relu dans le
   rendu**, alors que la ligne de statut rendue est déjà en main (`statut = _statut(premiere)`,
   ligne 787) et la porte : mesure `ID DETAIL | SAVE [NOM] | SAVES | EDIT | DB — PAGE 1/3 —
   ENTREE=VALIDER`, produite par `routes.py:147`. Si le code renommait cet indice, aucun test ne
   rougirait et la page continuerait d'annoncer un libellé que l'écran n'affiche plus.
2. `Méthode : ` et `Score : ` (page:142) sont exigés **côté rendu** (`MARQUEURS_DIAGNOSTICS`,
   ligne 203, vérifié à l'étape 4) mais **pas côté page**, alors que le module pratique le
   contrôle bidirectionnel pour d'autres littéraux (cf. « Controle bidirectionnel », étape 5 de
   `test_hypotheses_prouvees_par_balayage`, ligne 2170). Une réécriture du paragraphe de la page
   qui perdrait `Score : ` ne rougirait pas.

**Correction :** fermer les deux jambes dans `test_pagination_et_emplacement_du_calcul`, en
lisant la valeur **du rendu** pour l'exiger ensuite de la page :

```python
# étape 2, apres `statut = _statut(premiere)`
hint = re.search(r"ENTREE=[A-Z]+", statut)
if hint is None:
    constats.append(f"{PAGE} : la ligne de statut « {statut} » ne porte aucun indice "
                    f"« ENTREE=... » ; attendu « ENTREE=VALIDER », pose par {SOURCE_ROUTES}:147")
# étape 5, cote page : exiger les trois marqueurs, et `hint.group(0)` plutot qu'un litteral
```

#### WR-04 : la règle « une seule page ⇒ aucune carte, aucune touche F7/F8 » n'est jamais évaluée

**Fichier :** `tests/test_docs_parcours.py:1415-1500` (page:138, section « Lire le résultat »)
**Constat :** la page affirme (ligne 138) que « tant que le résultat tient sur une seule page, il
n'y a **aucune carte de pagination et aucune touche F7 ni F8** ». Aucun test n'évalue ce cas :
`test_pagination_et_emplacement_du_calcul` **exige** au moins deux pages (constat si
`total_lu < 2`, lignes 804-809), et `test_ecrans_de_sauvegarde_et_export` rend justement le cas
d'une page (deux lignes injectées → `data-body-total="1"`) mais n'asserte que le préfixe de la
ligne de statut (ligne 1492). Mesuré sur ce rendu d'une page : statut
`ID DETAIL | SAVE [NOM] | SAVES | EDIT | DB — ENTREE=VALIDER` — **pas** de `PAGE n/total` — et
barre de touches réduite à (`ESC`, `Retour`) — **pas** de F7 ni F8. La règle est donc vraie
aujourd'hui, mais `routes.py:136-146` pourrait se mettre à poser la carte et les deux touches
dès la première page sans qu'aucun test ne rougisse, la page continuant d'affirmer le contraire.
**Correction :** le rendu d'une page est déjà dans le test — y ajouter l'absence, et exiger de la
page qu'elle cite le fragment :

```python
if "PAGE " in statut_resultat:
    constats.append(
        f"{PAGE} : le resultat d'une seule page porte deja « {statut_resultat} » ; attendu "
        f"aucune carte de pagination tant que le resultat tient sur une page ({SOURCE_ROUTES}:145)"
    )
for touche in TOUCHES_RESULTAT[:2]:  # ("F7", "Page prec"), ("F8", "Page suiv")
    if touche in _touches(resultat):
        constats.append(
            f"{PAGE} : la touche (« {touche[0]} », « {touche[1]} ») est rendue sur un resultat "
            f"d'une seule page ; attendu ces deux touches seulement au-dela d'une page "
            f"({SOURCE_ROUTES}:136-141)"
        )
```

#### WR-05 : deux helpers rendent un `IndexError` nu au lieu d'un échec localisant

**Fichier :** `tests/test_docs_parcours.py:282-289` et `:293-296`
**Constat :** `texte.split(MARQUEUR_CORPS, 1)[1]` (ligne 288) et
`texte.split(MARQUEUR_STATUT, 1)[1]` (ligne 295) indexent directement le résultat du découpage.
Si le gabarit déplace ses marqueurs (`templates/screen.html:24` `id="body">`, `:49`
`class="row status`), l'échec est `IndexError: list index out of range` — vérifié en passant un
texte sans marqueur aux deux helpers — donc un message qui ne nomme **ni la page, ni la section,
ni le fichier** qui a changé. Ces deux helpers sont utilisés par presque tous les tests du module :
un seul déplacement de marqueur fait tomber une quinzaine de tests avec une exception
inexpliquée, alors que le module s'impose l'inverse (« Jamais de `FileNotFoundError` brut (lecon
IN-03) », lignes 267-273, D-13) et que `_entete` (ligne 1396) et `_champ_saisie` (ligne 1404)
renvoient déjà une valeur sentinelle dans le même cas.
**Correction :** nommer le marqueur et son porteur avant de découper :

```python
if MARQUEUR_CORPS not in texte:
    raise AssertionError(
        f"{PAGE} : marqueur de corps {MARQUEUR_CORPS!r} absent du rendu ; attendu le gabarit "
        f"dofus_stuff/web/templates/screen.html:24, qui l'encadre"
    )
```

### Info

#### IN-01 : la limite annoncée par la garde « ni base, ni processus, ni réseau » est plus étroite que sa formulation

**Fichier :** `tests/test_docs_parcours.py:1287-1295` (limite annoncée ligne 1294)
**Constat :** mesuré avec les helpers du module, la clôture transitive atteint **6** modules
(`model.solver_spec`, `model.character`, `model.slots`, `model.stats`, `optimize.recommend`,
`web.dofusbook_export`) et **jamais** `dofus_stuff.web`, `dofus_stuff.web.routes` ni
`dofus_stuff.database`. La garde est donc réelle et non vacuitaire (le seuil « au moins 3 »
est franchi), mais sa docstring est optimiste : « un import public pur ajoute plus tard passe
sans revision ». Or `dofus_stuff/web/__init__.py:12` importe `dofus_stuff.database` et
`routes.py:6` importe `webbrowser` : un futur `from dofus_stuff.web import create_app` (import
public pur, celui que `tests/conftest.py:12` fait déjà) produirait **deux constats** sans aucun
risque réel.
**Correction :** soit nommer dans la docstring les racines publiques volontairement interdites
(`dofus_stuff.web`, `…web.routes`, `dofus_stuff.database`), soit restreindre le contrôle aux
modules réellement **appelés** par le module plutôt qu'aux modules atteints par import.

#### IN-02 : deux trous prouvés dans les deux gardes `ast`

**Fichier :** `tests/test_docs_parcours.py:1224-1236`, `:1281`, `:1840-1885`
**Constat :**

1. `_imports_du_module` enregistre `noeud.module` **sans** le niveau d'import relatif : un
   `from ..database import X` rend le nom `database`, qui échappe aux deux filets — la clôture
   (`importe.split(".")[0]` hors `RACINES_INTERDITES`, et non préfixé par `dofus_stuff.`) comme
   l'égalité stricte `importe == MODULE_BASE_INTERDIT` (ligne 1281). Latent et non vivant :
   `grep -rn "^from \." dofus_stuff/` ne rend rien aujourd'hui.
2. `test_aucun_post_db_sans_patch` n'inspecte que les dictionnaires dont la clé **et** la valeur
   sont des constantes de chaîne (ligne 1878) : un `cmd` venu d'une table
   (`data={"cmd": valeur}`, exactement la forme employée par
   `test_entrees_citees_acceptees_et_refusees`) est invisible, et rien n'interdit un POST vers
   `/optimize/result`, seul chemin qui atteint `webbrowser.open_new_tab` côté serveur
   (`routes.py:1309-1310`, `:1333`).

**Correction :** (1) résoudre le nom de module avec le niveau d'import
(`importlib.util.resolve_name` sur le paquet importateur) et comparer par préfixes ; (2) signaler
aussi tout POST visant `/optimize/result` et tout `cmd` non littéral, ou asserter qu'aucune table
épinglée (`ENTREES_MESUREES`, `VALEURS_*`) ne porte la valeur `db`.

#### IN-03 : les numéros de ligne cités dans les messages d'échec dériveront sans rien faire rougir

**Fichier :** `tests/test_docs_parcours.py:915-916`, `:1546-1547`, `:1567-1571`, `:2207-2213`
**Constat :** les messages portent des références de ligne littérales, jamais assertées : par
exemple `{SOURCE_API}:436` pour la ligne `Greedy:` — qui est en `api.py:435` — et
`{SOURCE_API}:384-385` pour la ligne `(vide)` — qui est en `api.py:386`. `LIGNE_MAX_SAVES = 15`
et `LIGNE_MENU_CLASSE = 989` ne servent, eux aussi, que dans des messages. Ces nombres sont
justes à une ou deux lignes près aujourd'hui, mais ils se périmeront au premier ajout de ligne et
le message censé localiser la faute pointera à côté.
**Correction :** dériver le numéro du nœud `ast` quand le message nomme une ligne
(`noeud.lineno`), ou retirer les numéros et ne nommer que le fichier et le fragment cherché.

---

_Revu : 2026-09-11T17:31:03Z_
_Relecteur : Claude (gsd-code-reviewer)_
_Profondeur : standard_
