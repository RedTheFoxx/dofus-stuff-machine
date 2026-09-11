---
phase: 04-wizard-avanc-et-r-sorption-de-la-dette-guide-wizard
reviewed: 2026-09-11T19:29:26Z
depth: standard
files_reviewed: 8
files_reviewed_list:
  - GUIDE_WIZARD.md
  - README.md
  - docs/parcours-simplifie.md
  - docs/sommaire.md
  - docs/wizard-avance.md
  - tests/fixtures/guide-wizard-obsolete.md
  - tests/test_docs_parcours.py
  - tests/test_docs_wizard.py
findings:
  critical: 2
  warning: 5
  info: 4
  total: 11
status: issues_found
---

# Phase 4 : revue de code — « Wizard avancé et résorption de la dette `GUIDE_WIZARD` »

**Revu :** 2026-09-11T19:29:26Z
**Profondeur :** standard (8 fichiers en périmètre, aucun fichier de `dofus_stuff/**` — le code est resté le référentiel, D-66)
**Statut :** issues_found (2 critiques, 5 avertissements, 4 informations)

## Résumé

Périmètre mesuré, pas lu : `GUIDE_WIZARD.md` (18 lignes, 321 supprimées),
`docs/wizard-avance.md` (224 lignes, nouveau), `docs/sommaire.md` (+1 ligne d'index),
`docs/parcours-simplifie.md` (2 lignes converties en liens), `README.md` (−2 lignes),
`tests/fixtures/guide-wizard-obsolete.md` (39 lignes, nouveau),
`tests/test_docs_wizard.py` (2 569 lignes, nouveau), `tests/test_docs_parcours.py` (+165/−2).

Ce que la revue a vérifié **sur mesure** et trouvé conforme :

- **Suite complète** : `./.venv/Scripts/python.exe -m pytest -q` → **203 passed, 0 skipped**.
  Les neuf écrans du wizard et les trois questions ont été rendus par le client de test Flask
  **en processus** (aucun serveur, aucun socket), et `.data/dofus.sqlite3` garde son `mtime` du
  6 septembre — la suite n'écrit rien sous `.data/`.
- **Aucun contrôle affaibli** : `git diff --numstat c2afc42..HEAD` donne `2569 0` pour
  `tests/test_docs_wizard.py` et `165 2` pour `tests/test_docs_parcours.py`. Les **deux** lignes
  retirées de ce dernier sont la déclaration remplacée de la réserve `PAGES_INEXISTANTES`
  (`wizard-avance.md` en sort, parce que sa cible existe désormais) ; cette réduction est
  **compensée et inversible** : l'invariant 2 du nouveau `test_lien_wizard_avance_legitime`
  (lignes 2837-2852) refuse qu'une entrée de la réserve désigne une page existante, donc remettre
  `wizard-avance.md` dans la réserve rougit la suite. Ce n'est pas un affaiblissement.
- **Fixture fidèle** : comparaison octet à octet des trois extraits déclarés « verbatim » de
  `tests/fixtures/guide-wizard-obsolete.md` contre `git show c2afc42:GUIDE_WIZARD.md` → segments
  l. 35-45, l. 50-51 et l. 151-156 **identiques** (apostrophes typographiques comprises) ; les
  plages citées (35-45, 50-51, 153-157) sont exactes. La copie porte bien les trois formes, et le
  détecteur la signale (16 tests du module verts).
- **Forme des octets** : les huit fichiers sont UTF-8 **sans BOM** et CRLF dans l'arbre de travail
  (18/18, 123/123, 269/269, 224/224, 39/39, 2569/2569 retours chariot).
- **Exactitude de la page vis-à-vis du rendu réel** : vérifiés un par un contre leur porteur →
  les 9 titres, les 11 emplacements, les 10 couples `F<n>`/libellé (dont `F6` = `ARMES DISTANCE`,
  `F7` = `ARMES MELEE`), les invites (`SLOTS (N=TOGGLE) :`, `FILTRES TYPES (F+N) :`,
  `N=TOGGLE SLOT  FN=TOGGLE FILTRE`, `OPTIONS (N=EDIT) :`, `N=CHOISIR OPTION`, `N=EDIT`), les
  11 options, le sous-écran `OPT-WED` (libellé `VAL`, `maxlength=20`, `VALEUR ENREGISTREE`),
  `OPTION MISE A JOUR`, `OPTION INVALIDE`, `SAISIR UN NUMERO D'OPTION`, `JET = MIN|AVERAGE|MAX`,
  `SEED` vide/`-`/`none`/`aucun` → `(aucun)`, plancher `TOP-K`, les deux formes
  `FORMAT : BASE POINTS CIBLE POIDS` / `FORMAT : BASE EXO CIBLE POIDS` (routes.py:1254 et :1260,
  lignes citées justes), `SAISIR LE NUMERO DE LA LIGNE`, `NUMERO INVALIDE`, `CARAC ENREGISTREE`,
  les quatre lignes de syntaxe d'items et leur seul refus (`optimize_wizard.py:424`, ligne citée
  juste), l'état vide `(aucun)`, la troncature `… +N` au-delà de 8 entrées, les codes d'écran
  `OPT-W1`…`OPT-W9` et `OPT-WED`, `ECRAN WIZARD INCONNU`, les trois questions, la ligne
  `AVANCE : personnaliser les réglages`, l'arrivée sur le **récapitulatif**, les couples
  `F7`/`F8`/`ESC` des neuf étapes, les quatre commandes du récapitulatif et les chiffres
  `1`-`8` (`WIZARD_STEPS[n-1]`). **Aucune de ces affirmations n'est fausse.**
- **Le procédé honnête de la page sur la touche sans destination** : « le récapitulatif rend
  `Page suiv` … se comporte comme un `Suivant` sans destination » est exact — mesuré dans
  `terminal.js` (`navigateF8`, l. 538-547) : sans `data-f8-url` et avec `totalPages() == 1`,
  `goPage(1)` sort en `false` et rien ne se passe.
- **Aucune commande destructrice, aucun `GO` posté** : `COMMANDE_DESTRUCTRICE = \bdb\s+clear\b` est
  armé sur la section de l'exemple, et la garde `ast` du module refuse la paire `cmd` = `GO`
  (qui exécute le solveur via `routes.py:1114-1116`). Aucun `db clear`, aucun `drop`, aucune
  suppression sous `.data/` ni `.doc-agent/` dans le diff de la phase.
- **Aucun artefact généré commité** : `git status --porcelain` ne montre que des éléments **non
  suivis** du hôte de planification (`.gsd/`, `.gsd-tmp/`, `.doc-agent/`, `doc-agent.toml`,
  `gsd-auto*.toml`, `.planning/state.json`, `.planning/milestone.lock`) et deux modifications non
  indexées de l'hôte (`.gitignore`, `.planning/config.json`) ; rien de tout cela n'est dans un
  commit de la phase.
- **Les assertions ne sont pas vacuitaires** : aucune assertion du nouveau module ne compare une
  valeur calculée par le chemin qu'elle prétend garder ; les refus sont postés et lus dans la ligne
  de statut rendue, les libellés sont lus dans le corps rendu, et les comptes (11 emplacements,
  10 filtres, 11 options, 2 pages de l'écran `slots`) sont dérivés du rendu, jamais d'une table
  locale. Les deux seuls contrôles à une jambe que la phase laisse sont nommés ci-dessous en
  avertissement (enumeration des refus de l'écran `slots`) et en information (`VAL`).

Ce qui reste : **deux affirmations fausses ou contradictoires** — l'arborescence de l'aiguillage
(dont les libellés ne sont pas ceux que le produit rend) et la phrase de
`docs/parcours-simplifie.md:140` que cette phase devait garder vraie — plus cinq constats de
solidité, tous portant sur la page ou le harnais, aucun n'exigeant de toucher `dofus_stuff/**`.

## Narrative Findings (AI reviewer)

### Critical Issues

#### CR-01 : l'arborescence de l'aiguillage n'est pas celle que le produit rend, et la phase écrit la vraie deux fichiers plus loin

**Fichier :** `GUIDE_WIZARD.md:5` (l'affirmation), `:10` et `:12` (les deux lignes qui la démentent)
**Constat :** le fichier annonce « Le menu principal du produit, lui, garde son **arborescence
réelle** : » puis affiche

```
3. PANOPLIES        (ligne 10)
4. OPTIMISATION     (ligne 12)
```

Le rendu de `GET /` **mesuré** avec le client de test Flask (fixture `app`, en processus,
hors-ligne) porte, lui, exactement :

```
1. RECHERCHE D&#39;OBJETS
2. LISTE DES EQUIPEMENTS
3. LISTE DES PANOPLIES
4. OPTIMISATION DE STUFF
5. SYSTEME
```

(`dofus_stuff/web/routes.py:191-198`, corps du menu). Deux des cinq lignes de l'aiguillage ne sont
donc pas les libellés du produit, alors que la phrase les présente comme tels **et** que la même
phase les écrit correctement ailleurs : `docs/wizard-avance.md:9` cite « la ligne
`4. OPTIMISATION DE STUFF` ouvre l'optimisation » — le libellé **rendu** — et la page cite
`4. OPTIMISATION DE STUFF` une seconde fois à l'étape 1 de l'exemple (l. 204). Deux documents du
même jeu se contredisent donc sur le libellé de la même ligne de menu, et l'un des deux
(`GUIDE_WIZARD.md`) **contredit toujours le produit** : c'est précisément le critère que la phase
existe pour satisfaire (WIZ-02/WIZ-03, « `GUIDE_WIZARD.md` ne contredit plus le produit »), et
c'est la **forme (a)** du détecteur (« un menu associé au mauvais libellé », D-58).

Rien ne garde cette dérive : le détecteur juge les jetons `N. LIBELLE` par **appartenance de mots**
(`_mots_significatifs`, `tests/test_docs_wizard.py:440-449`, avec `MOTS_OUTILS`), donc
`3. PANOPLIES` est accepté parce qu'il partage le mot `PANOPLIES` avec `3. LISTE DES PANOPLIES`, et
`4. OPTIMISATION` parce qu'il partage `OPTIMISATION` avec `4. OPTIMISATION DE STUFF`. La tolérance
est **voulue** (D-47 fixe ces formes abrégées, et `test_renvois_legitimes_non_signales` l'exige :
« sans cette tolérance, l'aiguillage corrigé serait déclaré fautif »). Le défaut n'est donc pas la
tolérance, c'est le **choix de la valeur attendue** : D-47 a été écrite depuis le **routage**
(`menu_post`, `routes.py:217-222`), qui donne les numéros — et les numéros sont justes —, jamais
depuis le **corps rendu**, qui donne les libellés ; or la méthode de la phase est que le rendu est
la référence (D-36). Résultat : le nombre est corrigé, l'étiquette est restée approximative, et la
phrase « arborescence réelle » la transforme en affirmation fausse.

**Correction :** écrire les libellés **rendus** — le détecteur les accepte sans modification, sa
règle d'appartenance étant une intersection non vide :

```
3. LISTE DES PANOPLIES

4. OPTIMISATION DE STUFF
5. SYSTEME
```

(`_mots_significatifs("LISTE DES PANOPLIES")` = `{PANOPLIES}` ∩ `{PANOPLIES}` ≠ ∅, et
`_mots_significatifs("OPTIMISATION DE STUFF")` ∩ `{OPTIMISATION, STUFF}` ≠ ∅ ; le jeton reste capté
par `MOTIF_JETON_MENU`.) Variante si D-47 doit rester lettre pour lettre : ne plus présenter le
bloc comme « l'arborescence réelle » mais comme le **rappel des numéros** du menu, et laisser
`docs/wizard-avance.md` seule source des libellés. Les deux voies sont locales et n'exigent aucun
fichier de `dofus_stuff/**`.

#### CR-02 : l'affirmation que la phase devait garder vraie (D-64) est fausse, et la nouvelle page la rend visiblement fausse

**Fichier :** `docs/parcours-simplifie.md:140` — la page, lignes 173, 181 et 183
**Constat :** la phrase en jeu est : « Ces libellés sont ceux du résultat : le wizard avancé, qui
n'est pas décrit ici, affiche `Precedent` et `Suivant` à la place. » Or le rendu **mesuré** des neuf
écrans rend `Page prec` sur l'étape 1 (`routes.py:138` : `f7_label = "Precedent" if f7_url else
"Page prec"`, et `_wizard_step_urls` ne fournit pas de précédent à `slots`) et `Page suiv` sur
l'étape 9 (`f8_label = "Suivant" if f8_url else "Page suiv"`). La mesure confirme la barre de
l'étape 1 : `[('F7', 'Page prec'), ('F8', 'Suivant'), ('ESC', 'Retour')]`, et celle du
récapitulatif : `[('F7', 'Precedent'), ('F8', 'Page suiv'), ('ESC', 'Retour')]`.

L'affirmation de `parcours-simplifie.md:140` était donc déjà trop générale ; cette phase la rend
**contradictoire avec un document livré** en publiant la table exacte
(`docs/wizard-avance.md:173` et `:181`, plus la phrase de synthèse `:183` : « l'étape 1 n'a pas de
précédent et rend `Page prec`, l'étape 9 n'a pas de suivant et rend `Page suiv` »). D-64 est
explicite : « Cette affirmation **doit rester vraie après cette phase** […] en aucun cas elle ne
les contredit », et D-63 interdisait de modifier un autre énoncé de cette page — les deux décisions
se contredisent, et la phase a tranché en faveur de D-63, laissant une phrase fausse dans le jeu
documentaire. Le harnais le sait : la docstring du module d'ancrage écrit noir sur blanc qu'une
assertion exigeant `Precedent`/`Suivant` « contredirait le rendu des extrémités et l'affirmation de
`docs/parcours-simplifie.md:140` » (`tests/test_docs_wizard.py:2116-2117`). Aucun contrôle ne
compare cette phrase au rendu : la dérive est donc **non gardée**.

**Correction :** qualifier la phrase de `parcours-simplifie.md:140`, par exemple : « […] le wizard
avancé, qui n'est pas décrit ici, affiche `Precedent` et `Suivant` **aux écrans intermédiaires** et
`Page prec` / `Page suiv` à ses deux extrémités. » Si D-63 interdit réellement cette retouche, la
contradiction doit être signalée comme limite assumée dans le module (au même titre que
`LIMITE_HONNETE`) plutôt que laissée implicite — mais en l'état, le critère D-64 est faux, et un
lecteur qui compare les deux pages trouve deux libellés incompatibles pour le même écran.

### Warnings

#### WR-01 : l'énumération des refus de l'écran `slots` est fausse pour un numéro hors liste

**Fichier :** `docs/wizard-avance.md:94` et `:95` (section « Erreurs et refus »)
**Constat :** la page écrit « Une saisie qui n'est ni un numéro de `1` à `11` ni une touche `F<n>`
rend `SAISIE INVALIDE` ». Mesuré sur le rendu, c'est faux dès qu'on tape un **nombre hors liste** :

```
slots 'abc' -> SAISIE INVALIDE
slots '0'   -> SLOT INVALIDE
slots '12'  -> SLOT INVALIDE
slots '13'  -> SLOT INVALIDE
slots 'F11' -> FILTRE INVALIDE
slots 'F0'  -> FILTRE INVALIDE
```

`apply_slots_input` (`dofus_stuff/web/optimize_wizard.py:281-309`) distingue trois refus :
`Saisie invalide` (ni chiffres ni `F<n>`), `Slot invalide` (chiffres hors `1`-`11`) et
`Filtre invalide` (`F` suivi de chiffres hors `1`-`10`). Le message `SLOT INVALIDE` n'est cité
**nulle part** dans la page, et la phrase `:95` (« une touche au-delà de `F10` ») laisse croire que
`F0` rend autre chose que `FILTRE INVALIDE`. Le contrôle du module ne mesure que `abc` → `SAISIE
INVALIDE` et `F11` → `FILTRE INVALIDE` (`tests/test_docs_wizard.py:1174-1177`), donc la dérive
passe : c'est exactement le trou que la phase dit vouloir fermer (`F7` mal étiqueté, même nature).
**Correction :** ajouter le refus manquant et borner la règle, en gardant les libellés lus au
rendu :

```markdown
- Une saisie qui n'est ni des chiffres ni une touche `F<n>` rend `SAISIE INVALIDE`.
- Des chiffres hors de `1` à `11` rendent `SLOT INVALIDE`.
- Une touche `F<n>` avec `n` hors de `1` à `10`, par exemple `F11` ou `F0`, rend `FILTRE INVALIDE`.
```

et poster `12` et `F0` dans `test_slots_et_filtres_ancres_au_rendu` (le corpus de refus de la
ligne 1172 est déjà un tuple extensible).

#### WR-02 : l'assertion CRLF mesure un artefact local de git, pas la page

**Fichier :** `tests/test_docs_wizard.py:1781-1789` (la page, `docs/wizard-avance.md`)
**Constat :** `if retours != fins` exige que **toutes** les fins de ligne des octets de l'arbre de
travail soient des CRLF. Or `git ls-files --eol docs/wizard-avance.md` répond
`i/lf  w/crlf  attr/` : l'objet **versionné** est en LF, l'arbre de travail n'est en CRLF que parce
que `core.autocrlf=true` est un réglage **local** (aucun `.gitattributes`). Sur un clone où
`core.autocrlf` vaut `false` ou `input` (poste Linux, clone non configuré), la **même page
commitée** arrive en LF : `retours = 0`, `fins = 224`, la suite rougit avec le message « attendu des
fins de ligne CRLF sur toutes les lignes, comme les autres pages de docs/ ». C'est la forme dure du
défaut déjà relevé en `WR-01` de la revue de la phase 3 : un contrôle vert pour une raison qui
n'appartient pas au fichier, et rouge sur un artefact correct. Le fichier lui-même est conforme
(CRLF, sans BOM).
**Correction :** garder le contrôle du BOM et accepter tout fichier **homogène**, ce qui n'élimine
pas le vrai piège (des fins de ligne **mêlées** dans un même fichier) et ne dépend d'aucune config
git :

```python
if retours not in (0, fins):
    constats.append(
        f"{PAGE} : la page porte {fins} fin(s) de ligne pour {retours} retour(s) chariot ; attendu "
        f"des fins de ligne homogenes, le CRLF n'etant pas versionne (aucun .gitattributes, "
        f"core.autocrlf local)"
    )
```

#### WR-03 : le harnais de rendu est recopié d'un module de test à l'autre, contre la leçon du dépôt

**Fichier :** `tests/test_docs_wizard.py:91-101,348-357,372-386,390-407,834-849` et
`tests/test_docs_parcours.py:100-106,282-289,293-296,356-375,743-750`
**Constat :** comparaison `ast` des deux modules : **six fonctions sont octet pour octet
identiques** (`_lignes_du_corps`, `_statut`, `_touches`, `_champ_saisie`, `_imports_du_module`,
`_appels_du_module`), six constantes sont recopiées à l'identique (`MARQUEUR_CORPS`,
`MARQUEUR_STATUT`, `MARQUEUR_ENTETE`, `LIGNE_CORPS`, `LIBELLE_SAISIE`, `TOUCHE_BARRE`), et
`_empreinte` / `_entete` / `_texte_page` / `_libelle_saisie` / `_sous_section` sont des copies où
**la divergence a déjà commencé** (docstrings et messages d'échec différents, `_empreinte` renvoie
sur `RACINE_DEPOT` d'un côté et `docs_dir.parent` de l'autre). Le `tests/conftest.py` du dépôt
porte pourtant la règle en clair (l. 126-128) : « Un helper dupliqué finit par diverger
(leçon WR-04) : ces fonctions ne sont donc jamais recopiées dans un module de test, elles y sont
exposées comme l'est déjà la normalisation. » Ici les marqueurs de `templates/screen.html` vivent
donc en deux exemplaires : un déplacement de marqueur devra être corrigé deux fois, et rien ne
signale qu'un seul des deux a été mis à jour.
**Correction :** promouvoir les marqueurs et les lecteurs du rendu en fixtures de
`tests/conftest.py` (`marqueurs`, `lignes_du_corps`, `statut`, `touches`, `entete`, `champ_saisie`,
`empreinte`), comme l'ont été `section`, `sections`, `normalize` et `docs_dir` — le module ne garde
alors que ses lecteurs propres au wizard (`_emplacements_du_rendu`, `_options_du_rendu`, etc.).

#### WR-04 : deux lecteurs rendent un `IndexError` nu, contre la règle D-13 du module

**Fichier :** `tests/test_docs_wizard.py:354` et `:376`
**Constat :** `texte.split(MARQUEUR_CORPS, 1)[1]` et `texte.split(MARQUEUR_STATUT, 1)[1]` indexent
directement le résultat du découpage. Si `dofus_stuff/web/templates/screen.html` déplace ses
marqueurs (`id="body">` l. 24, `class="row status` l. 49), l'échec est
`IndexError: list index out of range` — un message qui ne nomme **ni la page, ni le marqueur, ni le
fichier** qui a changé, alors que le module s'impose l'inverse (« Jamais de `FileNotFoundError`
brut », `_texte_page` l. 341-346, D-13) et que `_entete` (l. 359-370) renvoie déjà `""` dans le
même cas. Ces deux lecteurs sont appelés par la quasi-totalité des seize tests : un seul
déplacement de marqueur fait tomber le module entier avec une exception inexplicable au lieu d'un
constat localisant. C'est la répétition, dans un second module, de `WR-05` de la revue de la
phase 3 (même code, même défaut), ce qui rend la correction d'autant plus utile.
**Correction :** nommer le marqueur et son porteur avant de découper, sur le patron de `_entete` :

```python
if MARQUEUR_CORPS not in texte or MARQUEUR_STATUT not in texte:
    raise AssertionError(
        f"{PAGE} : marqueur de corps {MARQUEUR_CORPS!r} ou de statut {MARQUEUR_STATUT!r} absent du "
        f"rendu ; attendu le gabarit dofus_stuff/web/templates/screen.html, qui les pose"
    )
```

#### WR-05 : deux sections du guide supprimé n'ont reçu aucun propriétaire, et le fait produit qu'elles portaient n'est nulle part

**Fichier :** `GUIDE_WIZARD.md` (état antérieur : sections 9 « Conseils pour de bons résultats » et
12 « Aller plus loin ») — la page livrée
**Constat :** D-49 pose que « Le contenu retiré est **migré, jamais perdu** » et désigne deux
destinations : l'exemple guidé (`docs/wizard-avance.md`, D-55) et « lire le résultat » /
« sauvegarder et exporter » (`docs/parcours-simplifie.md`, D-38). Les sections §10 (problèmes
fréquents) et §11 (lexique) ont bien des cibles **déclarées** au sommaire mais non livrées
(`docs/depannage.md`, `docs/glossaire.md`, phases ultérieures — acceptable). En revanche §9 et §12
**n'ont aucun propriétaire**, ni dans D-46/D-49, ni dans les idées différées : leur contenu a
disparu avec le fichier. Le seul fait **produit** qu'elles portaient et qui est encore vérifiable
au rendu est le repli par défaut du calcul : sans aucun poids, le récapitulatif affiche
`POIDS : (aucun — defaut INT)` (`dofus_stuff/web/optimize_wizard.py:265`), et
`grep -ril "défaut INT\|défaut Intelligence\|au moins un poids" docs/ GUIDE_WIZARD.md README.md`
ne rend **rien** : la connaissance n'est atteignable qu'en lisant le code du solveur, ce qui est
précisément ce que la documentation existe pour éviter. (§12 renvoyait aussi à
« menu `4. SYSTEME` » — référence obsolète heureusement supprimée, et sa partie CLI/base locale a
bien ses pages.)
**Correction :** ajouter au périmètre livré la phrase la plus utile de §9, adossée au rendu — par
exemple dans `docs/wizard-avance.md` § « Les 9 étapes du wizard », à côté de l'étape
`RECAPITULATIF` : « Sans aucun poids, le calcul retombe sur un défaut Intelligence ; le
récapitulatif l'affiche alors sous la forme `POIDS : (aucun — defaut INT)`. » Le reste des conseils
(§9) et de « aller plus loin » (§12) peut rester abandonné **s'il est déclaré** comme tel dans la
page, au lieu de disparaître sans trace.

### Info

#### IN-01 : « le message du convertisseur tel quel » est en réalité mis en majuscules et tronqué

**Fichier :** `docs/wizard-avance.md:139`
**Constat :** la page écrit « Une valeur qui n'est pas un nombre fait remonter le message du
convertisseur **tel quel**. » Mesuré : le sous-écran d'édition rend
`INVALID LITERAL FOR INT() WITH BASE 10: 'ABC'` pour `abc` sur `NIVEAU`, et
`COULD NOT CONVERT STRING TO FLOAT: 'A'` pour `a b c d` sur une caractéristique — le routeur
applique `flash(str(exc).upper()[:COLS], "error")` (`dofus_stuff/web/routes.py:1221`), donc le
message est **mis en capitales** et coupé à `COLS`. « Tel quel » est donc inexact, alors que la page
est précise partout ailleurs sur la casse des libellés.
**Correction :** « fait remonter le message du convertisseur, en capitales, tel que la ligne de
statut l'affiche (`COULD NOT CONVERT STRING TO FLOAT: …`) ».

#### IN-02 : le contrôle « aucun énoncé de contenu » de l'aiguillage ne mord que la forme `N. LIBELLE = VALEUR`

**Fichier :** `tests/test_docs_wizard.py:2509-2535` (motif `MOTIF_OPTION_RENDUE`, l. 126-128)
**Constat :** l'assertion du contrôle annonce « un aiguillage … **sans aucun énoncé de contenu** »,
et sa docstring comme son message nomment cinq marqueurs plus les lignes d'options. Mais la
détection des lignes d'options passe par `MOTIF_OPTION_RENDUE`, qui **exige un `=`** :
`^(?P<numero>\d{1,2})\.\s+(?P<libelle>.+?)\s*=\s*(?P<valeur>.*)$`. Une ligne réintroduite sous une
autre forme — `1. NIVEAU`, `| 1 | NIVEAU |`, ou `Niveau — le niveau de votre personnage` — n'entre
pas dans le motif et passe inaperçue, alors que c'est exactement le contenu que D-48 veut bannir.
**Correction :** élargir le contrôle aux jetons `^\s*\d+\.\s+[A-ZÀ-Ý][^=]*$` et aux lignes de
tableau dont les mots significatifs recoupent un libellé d'option rendu (le helper
`_mots_significatifs` est déjà là), ou reformuler l'assertion pour ce qu'elle vérifie réellement.

#### IN-03 : l'assertion sur le libellé `VAL` ne peut pas mordre

**Fichier :** `tests/test_docs_wizard.py:1324` (et, même forme, `:1336`, `:1475`)
**Constat :** `if "VAL" not in texte` cherche `VAL` **n'importe où** dans la page. Or la page cite
aussi `VALEUR ENREGISTREE` (exigé juste au-dessus, l. 1330 et 1321) : la sous-chaîne `VAL` est donc
présente même si le libellé du champ disparaissait de la phrase correspondante. Le contrôle est vert
pour la mauvaise raison, alors que le module dispose déjà d'un helper de citation en mot entier
(`tests/test_docs_parcours.py:2661`, `_cite_en_mot_entier`).
**Correction :** exiger le fragment réellement cité par la page, entre accents graves
(`` `VAL` ``), ou comparer avec le libellé lu au rendu (`_libelle_saisie`, déjà en main) au lieu
d'un littéral.

#### IN-04 : la docstring du module décrit encore l'état rouge comme l'état attendu

**Fichier :** `tests/test_docs_wizard.py:20-26`
**Constat :** « **Etat attendu pendant la phase** : `test_aiguillage_sans_renvoi_obsolete` est
**ROUGE** tant que l'aiguillage livre `GUIDE_WIZARD.md` n'a pas ete corrige (plan 04-03, vague 4).
C'est la preuve du critere 5 dans son etat rouge (D-59a) […]. » La phase est terminée : le
contrôle est **vert** (mesuré, 16 passed) et le fichier qu'il garde est corrigé, mais la docstring
reste au présent de l'état intermédiaire ; `test_aiguillage_et_readme` porte encore, lui aussi, des
renvois « appartient au plan 04-03 ». Un lecteur du module — c'est la première chose qu'il lit —
croit que le fichier gardé est encore obsolète. C'est la même famille que `WR-02` de la revue de la
phase 3 (un commentaire qui contredit la mesure enregistrée), en plus bénin.
**Correction :** passer ces phrases au passé (« le détecteur **a été** écrit et lancé alors que le
fichier était encore obsolète ; depuis le plan 04-03 il est vert, et la copie figée garde la
morsure ») et supprimer les renvois de plan devenus caducs.

---

_Revu : 2026-09-11T19:29:26Z_
_Relecteur : Claude (gsd-code-reviewer)_
_Profondeur : standard_
