# Phase 4: Wizard avancé et résorption de la dette `GUIDE_WIZARD` - Context

**Gathered:** 2026-09-11
**Status:** Ready for planning

<domain>
## Phase Boundary

Cette phase livre **une seule source de vérité pour le flux avancé** et **résorbe la dette de
`GUIDE_WIZARD.md`**.

Ce qu'elle délivre :

1. `docs/wizard-avance.md` — nouvelle page, adossée au **rendu réel** : le chemin d'arrivée, les
   **9 étapes** dans l'ordre du code avec leurs titres réellement rendus, les slots et filtres
   (`F1`–`F10`), les formats d'édition des quatre nombres, la syntaxe d'items
   (`+ID` interdit, `-ID` forcé, `!ID`, `CLEAR`) et les touches actives (`GO`, `RESET`, `SAVES`,
   `1`–`8` au récapitulatif), plus l'exemple guidé migré.
2. `GUIDE_WIZARD.md` — réduit à un **aiguillage corrigé** : il ne décrit plus le wizard.
3. `README.md` — le pointeur produit vers `GUIDE_WIZARD.md` est retiré.
4. `docs/sommaire.md` — entrée d'index « Wizard avancé » ajoutée.
5. `docs/parcours-simplifie.md` — les deux renvois en prose vers le wizard deviennent des liens
   (dette D-44 levée par la phase qui crée la cible).
6. Un **contrôle des renvois obsolètes**, observé **rouge** sur l'état antérieur puis **vert** après
   correction, dans la même phase.

Ce qu'elle ne fait **pas** : décrire la base locale (phase 5), figer la liste des 8 pages du sommaire
(phase 6), ajouter une capacité produit, modifier `dofus_stuff/**`.

</domain>

<decisions>
## Implementation Decisions

Conventions héritées : la numérotation reprend après la phase 3 (`D-01`…`D-15` phase 1,
`D-16`…`D-31` phase 2, `D-32`…`D-45` phase 3). Les décisions des phases précédentes restent
verrouillées et s'appliquent sans être rediscutées.

### Périmètre de l'aiguillage `GUIDE_WIZARD.md`

- **D-46:** `GUIDE_WIZARD.md` est réduit à un **aiguillage court** (~15 lignes) : `H1`, avis de
  déplacement, **arborescence de menus corrigée**, lien vers `docs/wizard-avance.md` **et** lien vers
  `docs/sommaire.md`. Tout le reste est supprimé : ni section « Lire le résultat », ni exemple guidé,
  ni table des touches rédupliquée.
- **D-47:** L'arborescence de l'aiguillage est **lue dans le code**, jamais écrite de mémoire :
  `4. OPTIMISATION` (et non `3`), `3. PANOPLIES`, `5. SYSTEME`, conformément à
  `dofus_stuff/web/routes.py` (`menu_post`, lignes ~217-222). L'affirmation « tapez `3` puis Entrée
  pour ouvrir l'optimisation » disparaît : c'est la première référence obsolète à résorber.
- **D-48:** L'aiguillage ne porte **aucun énoncé de contenu**. Deux **liens de navigation** ne sont pas
  deux descriptions : D-17 interdit de décrire le wizard deux fois, pas de le référencer deux fois.
  Les deux liens mènent au même ensemble documentaire, donc D-10/D-29 (lien unique du `README.md`
  vers le sommaire) restent intacts.
- **D-49:** Le contenu retiré est **migré, jamais perdu** : l'exemple guidé va dans
  `docs/wizard-avance.md` (D-55) ; « lire le résultat » et « sauvegarder et exporter » restent
  propriété de `docs/parcours-simplifie.md` (D-38, phase 3) — renvoi, pas recopie.

### Découpage de `docs/wizard-avance.md`

- **D-50:** La page suit **`WIZARD_STEPS`** — les 9 étapes **dans l'ordre exact du code** —
  `slots`, `options`, `caracs`, `papmpo`, `resistances`, `damages`, `misc`, `items`, `recap` — avec
  les **titres réellement rendus** lus dans `STEP_TITLES` de `dofus_stuff/web/optimize_wizard.py`
  (`SLOTS ET FILTRES`, `OPTIONS SOLVEUR`, `CARACTERISTIQUES`, `PA / PM / PO`, `RESISTANCES`,
  `DOMMAGES`, `DIVERS`, `ITEMS INTERDITS / FORCES`, `RECAPITULATIF`).
- **D-51:** La page contient une section **« Arriver au wizard »** décrivant le **chemin réel** :
  menu `4` → `optimize_entry` → `optimize_quick` (les 3 questions) → `AVANCE`. C'est précisément
  l'affirmation fausse à résorber : `GUIDE_WIZARD.md` annonce une arrivée « **directement** dans le
  wizard », alors que `optimize_entry` (`routes.py` ~930-932) redirige vers le parcours des
  3 questions.
- **D-52:** Le **périmètre de rendu est le web seulement** — le client de test Flask, en processus,
  hors-ligne, sans serveur ni réseau (méthode **D-32/D-36** de la phase 3). Le wizard vit dans
  `dofus_stuff/web/optimize_wizard.py` ; **aucune correspondance `AVANCE`/`wizard` n'existe dans
  `dofus_stuff/cli.py` ni `fetcher.py`**. Aucune section « parcours CLI du wizard » n'est écrite :
  la surface de commandes appartient à `docs/cli.md` (**D-37**).
- **D-53:** Les filtres de type `F1`–`F10` sont adossés à **`TYPE_FILTER_KEYS`**
  (`dofus_stuff/model/solver_spec.py:43`) et **`TYPE_FILTER_LABELS`**
  (`dofus_stuff/web/optimize_wizard.py:111`). Vérifié au code : index 6 = `arme_distance` → `F6` =
  `ARMES DISTANCE`, index 7 = `arme_melee` → `F7` = `ARMES MELEE`. **C'est la troisième référence
  obsolète à résorber** : `GUIDE_WIZARD.md` présente `F7` comme les armes distance.
- **D-54:** La page documente les **formats d'édition des quatre nombres** (`B` / `P` / `C` / `W`) et
  la **syntaxe d'items** telle que le code l'applique (`+ID` interdit, `-ID` forcé, `!ID`, `CLEAR`),
  dont le message d'erreur est lu au code (`optimize_wizard.py` : `+ID | -ID | !ID | CLEAR`). Les
  **touches actives** réellement vues au rendu sont citées : `GO`, `RESET`, `SAVES`, et `1`–`8` au
  récapitulatif.
- **D-55:** L'**exemple guidé** de `GUIDE_WIZARD.md` (§ 8 « Premier stuff en 5 minutes », avec sa
  variante « cible PA ») est **migré** dans `docs/wizard-avance.md`, et **réancré au rendu réel** :
  chaque écran, libellé, titre, touche et format qu'il cite est confronté au rendu. Un passage
  contredit par le code est **corrigé**, jamais conservé au motif qu'il figurait dans le guide. Il
  passe par le chemin d'arrivée réel (D-51) et ne met jamais `db clear` dans un parcours recommandé.
  La variante « cible PA » ne survit que si le code la porte ; sinon elle est **retirée et signalée**
  (D-19).
- **D-56:** La page suit le **gabarit D-01** : `H1` unique, phrase d'introduction, sections courtes,
  bloc **« Source de vérité »** pointant vers des chemins qui **existent réellement** sur disque
  (D-03), et ligne de retour vers `docs/sommaire.md`. Les renvois vers « lire le résultat » /
  « sauvegarder et exporter » sont des **liens** vers `docs/parcours-simplifie.md`, **sans recopie**
  (D-38/D-43).
- **D-57:** `docs/sommaire.md` gagne **l'entrée d'index « Wizard avancé » à cette phase** (le
  sommaire croît par phase, **D-05**). La page y figure déjà dans « Parcours conseillé » (position 3)
  mais **pas dans la table d'index** — c'est le trou à combler. Le test d'exhaustivité
  bidirectionnelle (**D-06**) doit rester vert sans exception ; la liste épinglée des 8 pages reste en
  phase 6.

### Contrôle des renvois obsolètes (critère 5)

- **D-58:** Le détecteur est **ciblé sur les trois formes obsolètes nommées par le ROADMAP** : (a) un
  menu associé au mauvais libellé, (b) `F7` présenté comme armes distance, (c) l'arrivée
  « directe » dans le wizard. Les attentes du détecteur sont **ancrées** — arborescence et filtres lus
  au code et au rendu réel, chemin d'arrivée lu au flux réellement rendu — jamais écrites de mémoire.
  Limite honnête consignée **dans le test lui-même** : une *autre* inversion, non couverte par ces
  trois formes, ne fera pas échouer la suite ; aucune exhaustivité n'est revendiquée (même arbitrage
  que la limite de **D-26**, phase 2).
- **D-59:** La preuve du critère 5 est **double**, pour être à la fois littérale et relançable :
  **(a)** *ordre TDD* — le détecteur est écrit et **lancé alors que `GUIDE_WIZARD.md` est encore
  obsolète** : le **rouge est réellement observé et consigné**, puis la correction est appliquée et le
  **vert** est réellement obtenu, dans la même phase ; **(b)** *copie figée* — le texte obsolète est
  conservé comme **fixture de test**, et le **même détecteur doit le signaler**, ce qui rend la preuve
  durable et protège le détecteur d'une régression. La fixture est un artefact de `tests/`, avec les
  helpers du `tests/conftest.py` **existant** (**D-12**) ; ce n'est pas une page de documentation.
- **D-60:** Le détecteur **ne doit pas signaler un renvoi légitime** — en particulier le lien vers
  `docs/wizard-avance.md` que cette phase ajoute (D-63) ni les liens vers `docs/parcours-simplifie.md`
  (D-56).
- **D-61:** Le détecteur ne classe jamais `db clear` dans un parcours recommandé, et aucun `db clear`
  n'est exécuté, à aucun moment (**D-22/D-23**, phase 2).

### Redirection `README.md` et dette de renvoi D-44

- **D-62:** Dans `README.md`, la ligne `**Guide détaillé :** [GUIDE_WIZARD.md](GUIDE_WIZARD.md)`
  (~ligne 63) est **supprimée** — sans texte de remplacement. La section « Documentation utilisateur »
  garde son **lien unique** vers `docs/sommaire.md` (**D-10/D-29**). Aucun renvoi en prose vers
  `GUIDE_WIZARD.md` ni vers `docs/wizard-avance.md` n'est ajouté : rediriger la ligne ferait vivre
  **deux liens vers le sommaire dans le même fichier**, ce qui affaiblit le contrôle de structure et
  crée une seconde formulation du même renvoi (D-17). L'emplacement exact est **vérifié au fichier
  réel** avant édition (D-19).
- **D-63:** La **dette de renvoi D-44 est levée maintenant** : les deux renvois **en prose sans lien**
  de `docs/parcours-simplifie.md` (~lignes 5 et 256) deviennent de **vrais liens** vers
  `docs/wizard-avance.md`, **dans le même commit que la cible**. D-44 attribue explicitement le lien à
  la phase qui crée la page cible ; reporter laisserait la dette ouverte alors que sa condition de
  levée est précisément la création de la cible. **Aucun autre énoncé** de cette page n'est modifié.
- **D-64:** La ligne ~140 de `docs/parcours-simplifie.md` affirme que le wizard affiche `Precedent` /
  `Suivant` là où le résultat affiche `Page prec` / `Page suiv`. Cette affirmation **doit rester vraie
  après cette phase** : la page du wizard cite les libellés **effectivement rendus**, ou le contrôle
  les ancre ; en aucun cas elle ne les contredit.

### Conventions applicables (héritées, sans modification)

- **D-65:** Les conventions des phases 1 à 3 s'appliquent telles quelles : comparaisons **après
  normalisation** accents/casse/CRLF/balises HTML (**D-11**), helpers dans le `tests/conftest.py`
  **existant** (**D-12**), message d'échec citant **la page, la valeur attendue et le fichier de
  code** (**D-13**), ancrage par **API publique** — client de test Flask et lectures de constantes
  publiques, jamais d'introspection privée (**D-14**) — et exécution de référence
  `.venv/Scripts/python.exe -m pytest -q`, **sans** exécuter `main()`, **sans** écrire sous `.data/`,
  **sans** connexion réseau (**D-15**).
- **D-66:** Aucune modification de `dofus_stuff/**` n'est faite **pour aligner la documentation** : le
  code est le référentiel, la page s'y conforme. Aucun `db clear`, aucune suppression sous `.data/` ni
  `.doc-agent/`. Commits **locaux** uniquement, `git add` **par chemin explicite** (jamais
  `git add .`). Aucune publication, aucun déploiement distant.
- **D-67 [informational]:** La documentation est **en français**, comme les phases précédentes.

### Claude's Discretion

- Le libellé exact du `H1` de l'aiguillage `GUIDE_WIZARD.md` et le texte de l'avis de déplacement,
  tant que le fichier reste un aiguillage court et ne décrit plus le wizard.
- Le découpage interne des nouveaux tests (module `tests/test_docs_wizard.py` dédié ou extension d'un
  module existant) — seule contrainte : ne pas dupliquer les helpers de `tests/conftest.py` (D-12) et
  conserver le passage `.venv/Scripts/python.exe -m pytest -q` vert.
- La forme concrète de la **fixture** portant la copie figée du texte obsolète (chaîne dans le test,
  donnée structurée, ou fichier de fixture sous `tests/`), tant que le détecteur la signale et que la
  preuve reste relançable.
- Le regroupement des 9 étapes en sous-sections si la page y gagne en lisibilité, tant que **l'ordre
  du code** et les **titres réellement rendus** sont respectés et vérifiables.
- La formulation exacte de la limite honnête de D-58 dans le test.

### Folded Todos

Aucun — `todo.match-phase` a renvoyé `todo_count: 0` pour la phase 4.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Cadrage de la phase
- `.planning/ROADMAP.md` § « Phase 4: Wizard avancé et résorption de la dette `GUIDE_WIZARD` » —
  objectif et les 5 critères de succès (dont le critère 5, rouge puis vert).
- `.planning/REQUIREMENTS.md` — `WIZ-01`, `WIZ-02`, `WIZ-03` (dérivés de `DOCS-05`, `DOCS-10`) ;
  phase 4, statut Pending au moment de la discussion.
- `.planning/STATE.md` — état du projet.

### Décisions verrouillées des phases précédentes (à lire avant de planifier)
- `.planning/phases/01-socle-documentaire-installation-et-harnais-v-rifiable/01-CONTEXT.md` —
  **D-01** gabarit de page, **D-03** chemins réellement existants, **D-05** sommaire croissant par
  phase, **D-06** exhaustivité bidirectionnelle, **D-10** lien unique du README, **D-11** à **D-15**
  conventions de test.
- `.planning/phases/02-r-f-rence-cli-align-e-sur-le-parseur/02-CONTEXT.md` — **D-17** une seule
  source par énoncé, **D-19** aucune sémantique inventée, **D-22/D-23** commandes destructrices,
  **D-26** limite honnête consignée dans le test, **D-29** README à un seul lien.
- `.planning/phases/03-parcours-simplifi-document-depuis-le-rendu-r-el/03-CONTEXT.md` — **D-32**
  écrans web lus par le client de test Flask en processus, **D-36** le rendu web est la référence,
  **D-37** la surface de commandes appartient à `docs/cli.md`, **D-38** « lire le résultat » et
  « sauvegarder et exporter » sont des sections de `parcours-simplifie.md`, **D-43** ne pas
  re-décrire le wizard avancé dans cette page, **D-44** renvoi en prose sans lien jusqu'à la création
  de la cible, **D-45** conventions de test.

### Pages de documentation touchées
- `GUIDE_WIZARD.md` — 330 lignes, à réduire à l'aiguillage corrigé. Sections à migrer : § 5 (quatre
  nombres), § 6 (détail de chaque écran), § 8 (exemple guidé + variante cible PA). Sections à
  abandonner au profit des propriétaires déjà désignés : § 7 (« Lire le résultat », « Stuffs
  sauvegardés ») appartient à `docs/parcours-simplifie.md`.
- `docs/sommaire.md` — index à faire croître avec l'entrée « Wizard avancé » (D-57) ; porte déjà
  « 3. Wizard avancé » dans *Parcours conseillé* mais pas dans la table.
- `README.md` — lignes ~50-65 : prose produit, et la ligne `**Guide détaillé :**
  [GUIDE_WIZARD.md](GUIDE_WIZARD.md)` à supprimer (D-62).
- `docs/parcours-simplifie.md` — renvois en prose vers le wizard aux lignes ~5 et ~256 à convertir en
  liens (D-63) ; ligne ~140 (`Precedent`/`Suivant`) à ne pas contredire (D-64).
- `docs/installation.md` § ~69 — mentionne que `F7`/`F8` n'apparaissent dans la barre de raccourcis
  que sur un écran paginé ou à une étape du wizard : cohérence à préserver.

### Code — source de vérité à lire avant de rédiger
- `dofus_stuff/web/optimize_wizard.py` — `WIZARD_STEPS` (l. ~23), `STEP_TITLES` (l. ~35),
  `TYPE_FILTER_LABELS` (l. ~111), corps d'écran des slots (l. ~189), lecture des touches de filtre
  (l. ~288), syntaxe d'items et son message d'erreur (l. ~406, ~424), `CLEAR` (l. ~248).
- `dofus_stuff/model/solver_spec.py` — `TYPE_FILTER_KEYS` (l. 43), `default_player_spec`.
- `dofus_stuff/web/routes.py` — `menu_post` (l. ~217-222, arborescence `3`/`4`/`5`),
  `optimize_entry` (l. ~930-932), `optimize_quick` (l. ~935+), `optimize_wizard` (l. ~1027+),
  `_wizard_fkeys` / `_wizard_step_urls` (l. ~1014-1023).
- `dofus_stuff/web/templates/screen.html` — gabarit d'écran réellement rendu.

### Harnais de tests
- `tests/conftest.py` — fixture `docs_dir` et helper de normalisation partagés (**D-11/D-12**), à
  réutiliser sans les recopier.
- `tests/test_docs_structure.py` — invariants de structure et exhaustivité bidirectionnelle du
  sommaire (**D-06**), à garder vert.
- `tests/test_docs_parcours.py` — module de la phase 3 (17 tests) : patron d'ancrage au rendu réel à
  suivre, et page dont l'ancrage ne doit pas se dégrader.

### Modèle de fixture
- `.planning/phases/03-parcours-simplifi-document-depuis-le-rendu-r-el/03-CONTEXT.md` — **D-32**
  décrit le patron exact du client de test Flask à réutiliser pour dériver les libellés du wizard.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- **Client de test Flask en processus** (patron `tests/test_recommend.py` et
  `tests/test_docs_parcours.py`) : `client.post("/optimize/quick/niveau", ...)` etc. À réutiliser tel
  quel pour rendre `/optimize/wizard/<step>` et en dériver titres, libellés et touches — aucun
  serveur, aucun socket, aucune écriture sous `.data/`.
- **`tests/conftest.py`** : fixture `docs_dir` + helper de normalisation (minuscules, accents,
  CRLF/LF, balises HTML). Toute comparaison de libellé passe par lui (D-11/D-12).
- **`WIZARD_STEPS` / `STEP_TITLES`** : la liste ordonnée et les titres des 9 étapes sont déjà des
  constantes publiques — la page les cite, le test les lit, aucune liste n'est recopiée en dur.
- **`TYPE_FILTER_KEYS` / `TYPE_FILTER_LABELS`** : les 10 filtres et leurs libellés sont déjà
  appariés par index dans le code ; le couple `F6`/`F7` se vérifie sans hypothèse.
- **Message d'erreur d'items** (`+ID | -ID | !ID | CLEAR`) : la syntaxe documentée a déjà sa
  formulation exacte dans le code, à citer telle quelle.

### Established Patterns
- **Une seule source par énoncé (D-17)** : la page décrit, elle ne recopie pas la surface d'une autre
  page ; les renvois sont des liens, pas des copies.
- **Ancrage au rendu réel (D-32/D-36)** : tout libellé affirmé est lu au rendu ou au module source,
  jamais écrit de mémoire ; le message d'échec cite page + valeur attendue + fichier de code (D-13).
- **Sommaire croissant (D-05)** : chaque phase ajoute sa page à l'index ; le test d'exhaustivité
  bidirectionnelle reste vert sans exception (D-06).
- **Limite honnête dans le test (D-26)** : ce qu'un contrôle ne couvre pas est écrit dans le test,
  pas passé sous silence.

### Integration Points
- `docs/wizard-avance.md` ↔ `docs/sommaire.md` : nouvelle entrée d'index (D-57).
- `docs/wizard-avance.md` ↔ `docs/parcours-simplifie.md` : liens entrants (D-63) et sortants (D-56).
- `GUIDE_WIZARD.md` ↔ `docs/wizard-avance.md` : l'aiguillage pointe la source unique (D-46).
- `GUIDE_WIZARD.md` ↔ `docs/sommaire.md` : second lien de navigation, même point d'entrée (D-48).
- `README.md` : retrait du pointeur produit, lien unique vers le sommaire conservé (D-62).
- `tests/` : le détecteur de renvois obsolètes et sa fixture (D-58/D-59) s'ajoutent au harnais
  existant sans le dupliquer.

</code_context>

<specifics>
## Specific Ideas

**Les trois références obsolètes, adossées au code (à résorber et à détecter).**

1. **Menu inversé.** `GUIDE_WIZARD.md` écrit « Tapez `3` puis **Entrée** pour ouvrir
   l'optimisation » et dessine `3. OPTIMISATION DE STUFF` / `4. SYSTEME`. Le code
   (`routes.py`, `menu_post`) route `4 → optimize_entry`, `3 → list_sets`, `5 → system_menu`. La
   valeur attendue de l'arborescence corrigée est donc `4. OPTIMISATION`, `3. PANOPLIES`,
   `5. SYSTEME`.
2. **`F7` présenté comme armes distance.** `TYPE_FILTER_KEYS` donne, dans l'ordre,
   `familier`, `montilier`, `dragodinde`, `muldo`, `volkorne`, `arme_distance`, `arme_melee`,
   `dofus`, `trophee`, `prysmaradite` — donc `F6` = `ARMES DISTANCE`, `F7` = `ARMES MELEE`. Le
   ROADMAP a raison, `GUIDE_WIZARD.md` a tort.
3. **Arrivée « directe » dans le wizard.** `GUIDE_WIZARD.md` écrit « Vous arrivez **directement**
   dans le wizard (premier écran : slots et filtres) ». Or `optimize_entry` redirige vers
   `optimize_quick` (`classe` → `elements` → `niveau`), le wizard n'étant atteint qu'ensuite par
   `AVANCE`.

**Le trou du sommaire.** `docs/sommaire.md` liste « 3. Wizard avancé » dans *Parcours conseillé*
mais sa table d'index ne contient que trois lignes (`installation.md`, `parcours-simplifie.md`,
`cli.md`). L'entrée manquante est ajoutée par cette phase (D-57).

**Nature du critère 5.** C'est le seul critère du ROADMAP qui exige **deux états observés** — rouge
sur l'état antérieur, vert après correction, dans la même phase. La preuve retenue est double
(D-59) : observation réelle en ordre TDD *et* copie figée relançable.

**Ton et public.** Documentation **en français**, pour l'utilisateur comme pour le développeur
(public « Utilisateur + dev » retenu au cadrage projet) : page lisible par un non-technicien, adossée
au code pour rester maintenable.

</specifics>

<deferred>
## Deferred Ideas

- **`docs/base-locale.md` et son renvoi en prose** : `docs/parcours-simplifie.md` renvoie aussi à la
  base locale en prose sans lien. Sa cible est la **phase 5** ; le lien sera ajouté par la phase qui
  crée cette page, selon la règle D-44.
- **Liste épinglée des 8 pages du sommaire** : reste en **phase 6** (D-05/D-57). Cette phase ajoute
  seulement l'entrée d'index de sa propre page.
- **`docs/glossaire.md` et `docs/depannage.md`** : pages listées au sommaire mais non livrées ;
  elles relèvent des phases suivantes, pas de celle-ci.
- Aucune extension de périmètre : le périmètre de la phase est fixé par le ROADMAP et n'a pas été
  élargi pendant la discussion.

</deferred>

---

*Phase: 4-Wizard avancé et résorption de la dette `GUIDE_WIZARD`*
*Context gathered: 2026-09-11*
