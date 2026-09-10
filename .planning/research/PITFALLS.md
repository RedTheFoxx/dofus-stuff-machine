# Pitfalls Research

**Domain :** ajouter une documentation utilisateur **française, vérifiée par `pytest`** à un produit
**déjà livré et toujours mouvant** (`dofus-stuff-machine` : package Python 3.11+, CLI `fetcher.py`,
web Flask « terminal rétro », solveur ortools, base SQLite Dofusdude sous `.data/`).
**Researched :** 2026-09-10 (HEAD `19b5c96`, dernier commit fonctionnel `1d475f9`)
**Confidence :** **HIGH** sur les pièges *observés dans ce dépôt* (chaque affirmation cite un chemin +
numéro de ligne, un commit, ou une exécution locale rejouable) ; **MEDIUM** sur l'arbitrage
« quel piège est le plus grave / quelle phase le traite » (jugement d'ingénierie) ; **LOW** pour tout
énoncé qui viendrait d'Internet — **aucune source web n'était joignable sur cet hôte**.

## Note de méthode (seam de recherche, résultat réel)

`gsd_run query research-plan` (entrée : 2 questions, `config` tous drapeaux `false`) a retourné deux
items et deux clés : `websearch` / clé
`2ecbf79c7daba75d721599a3d51ae7931a289a779fb91d158e940aaf0e9332b3` et `context7` / clé
`678060c4faf1d28eff2ca1186218f0712c83ce535f9d7fac1555ed4ac63a96cb`.

Aucun des deux n'a pu être exécuté, et c'est **vérifié**, pas supposé :

| Fournisseur imposé par le seam | Tentative | Réponse réelle |
|---|---|---|
| `websearch` | `gsd_run query websearch "<question>"` | `{"available": false, "reason": "BRAVE_API_KEY not set"}` |
| `context7` | aucun outil `mcp__context7__*` exposé à cet agent | non invocable |

`gsd_run query classify-confidence --provider websearch` → **LOW** ;
`--provider context7` → **MEDIUM** (mais inutilisable, cf. ci-dessus).

**Conséquence assumée :** aucune trouvaille web n'a été inventée et **aucun digest n'a été mis en
cache** (`research-store put` n'a rien à stocker : il n'y a pas eu de fetch externe ; enregistrer un
digest sous `--source web --provider …` aurait falsifié la provenance). La source de vérité de ce
milestone étant le **code du dépôt**, c'est aussi la source la plus fiable : tous les constats
ci-dessous viennent de fichiers **lus ou exécutés localement**.

**Observations rejouables utilisées comme preuves** (aucune écriture sous `.data/`, aucune
resynchronisation Dofusdude, aucun `db clear` exécuté sur la vraie base) :

- `./.venv/Scripts/python.exe -m pytest -q` → **`136 passed in 1.69s`** (état actuel : suite verte,
  **zéro test** sur la documentation).
- `python -m pytest -q` (interpréteur par défaut de l'hôte) → `No module named pytest` : le projet a
  son propre `.venv/Scripts/python.exe` (voir Pitfall 10).
- Rendu réel des écrans via le client de test Flask, catalogue **synthétique** de
  `tests/conftest.py`, `offline=True`, `load_catalog=False` (aucun accès réseau, aucun accès `.data/`).
- Introspection du parseur : `build_parser().parse_args(shlex.split(cmd)[1:])` sur les commandes
  documentées.
- Le seul `db clear` de cette recherche est celui du **test existant** `tests/test_web.py:411`, qui
  s'exécute sur la base temporaire de la fixture `tmp_path`.

---

## Critical Pitfalls

### Pitfall 1: Documenter le produit d'avant — le numéro de menu que la doc donne n'ouvre pas l'écran promis

**What goes wrong:**
Un lecteur suit la doc et n'arrive pas où elle dit. C'est **déjà cassé** aujourd'hui, et pas de
façon marginale :

- `GUIDE_WIZARD.md:35` : « Tapez `3` puis **Entrée** pour ouvrir l'optimisation. » — or
  `dofus_stuff/web/routes.py:214-224` route `"3"` vers `terminal.list_sets` et `"4"` vers
  `terminal.optimize_entry`. Le lecteur qui tape `3` atterrit sur **LISTE DES PANOPLIES**.
- `GUIDE_WIZARD.md:38-42` reproduit un menu à 4 entrées (`3. OPTIMISATION DE STUFF`, `4. SYSTEME`)
  alors que le menu réel (`routes.py:189-200`) en compte **5** : `1. RECHERCHE D'OBJETS`,
  `2. LISTE DES EQUIPEMENTS`, `3. LISTE DES PANOPLIES`, `4. OPTIMISATION DE STUFF`, `5. SYSTEME`.
- Même erreur `SYSTEME` en `GUIDE_WIZARD.md:50` et `GUIDE_WIZARD.md:328` (« menu `4. SYSTEME` ») ;
  le menu réel est `5. SYSTEME` (`routes.py:197`).
- `GUIDE_WIZARD.md:45` : « Vous arrivez **directement** dans le wizard (premier écran : slots et
  filtres) » — faux depuis `1d475f9` : `optimize_entry()` redirige vers le flux en trois questions
  (`routes.py:930-934`), le wizard n'est atteignable que par `AVANCE` (`routes.py:944-951`).

**Why it happens:**
Le numéro d'un menu est un **littéral de code** dans une liste (`routes.py:189-200`) que **seuls les
tests de code** épinglent (`tests/test_web.py:10-21`). Rien ne relie ce littéral à la prose.
L'historique le prouve :

- `ab1eb38` (« Add set management features », 29/07) modifie le menu (`3. PANOPLIES` ajouté,
  `OPTIMISATION` 3 → 4, `SYSTEME` → 5) et met à jour `tests/test_web.py` — **aucun fichier de
  documentation n'est touché** (`--stat` : `catalog.py`, `routes.py`, `conftest.py`, `test_web.py`).
- `1d475f9` corrige la phrase devenue fausse **dans `README.md`** (`4. Optimisation de stuff`) mais,
  pour `GUIDE_WIZARD.md`, se contente d'**ajouter une note de 6 lignes en tête** — les sections 2, 5
  et 12 restent périmées.
- Inversement, `b3aa6f2` (F12 → ESC) fait évoluer **code + tests + doc dans le même commit** : la
  dérive n'est donc **pas** une fatalité, c'est l'absence de lien doc ↔ code qui la produit.

**How to avoid:**
Le contrôle doit **dériver la valeur attendue du runtime** et la comparer au fichier de doc :

```python
# côté runtime (source 1) — jamais recopié à la main dans le test
html = client.get("/").data.decode("utf-8")
lignes_menu = [l.strip() for l in re.findall(r'<div class="row">(.*?)</div>', html)
               if re.match(r"\d+\. ", l.strip())]

# côté doc (source 2) — le fichier sur disque
doc = (docs_dir / "parcours-simplifie.md").read_text(encoding="utf-8")
for ligne in lignes_menu:
    assert normalise(ligne) in normalise(doc)
```

Et la moitié **négative**, sans laquelle la dérive survit (voir Pitfall 4) : aucun document ne doit
présenter un numéro associé au mauvais libellé (`3. OPTIMISATION`, `4. SYSTEME`). Interdit : écrire
`assert "5. SYSTEME" in doc` (constante recopiée = test mort au prochain changement de menu).

**Warning signs:**
Un document cite un **numéro** d'entrée ; `git log --stat` montre un commit touchant `routes.py` /
`templates/` **sans** `docs/`, `README.md`, `GUIDE_WIZARD.md` ; la date du dernier commit touchant
`GUIDE_WIZARD.md` est antérieure à celle de `routes.py` (c'est le cas aujourd'hui).

**Phase to address:** **Phase 1** (harnais + `docs/sommaire.md` : la fixture et le test d'ancrage
existent avant les pages) puis **Phase 3** (parcours simplifié, propriétaire de la page qui cite le
menu) ; **Phase 4** pour la même vérification sur `GUIDE_WIZARD.md`.

---

### Pitfall 2: Le pansement en tête de fichier au lieu de corriger le corps

**What goes wrong:**
`GUIDE_WIZARD.md` contient **aujourd'hui deux vérités contradictoires** : une note ajoutée par
`1d475f9` en `GUIDE_WIZARD.md:1-6` (« Entrée simplifiée : le menu Optimisation demande désormais
classe, éléments et niveau ») et, 30 lignes plus bas, `:35` (« Tapez `3` »), `:45` (« vous arrivez
directement dans le wizard »), `:328`. Un lecteur scrolle la note d'encadré, applique la consigne
numérotée, et se perd. Pire pour la vérification : un test de **présence** passe, puisque la note
existe — donc le garde-fou peut être vert sur une doc fausse.

**Why it happens:**
Ajouter une note en tête est le geste le moins coûteux quand on modifie un comportement : il évite de
relire 330 lignes. C'est « réparé » du point de vue de l'auteur du commit (`1d475f9`), pas du point de
vue du lecteur.

**How to avoid:**
Une seule source par énoncé, et pour les doublons un test **de structure**, pas de contenu :
`GUIDE_WIZARD.md` ne décrit plus écran par écran (Phase 4 : contenu migré vers
`docs/wizard-avance.md`, `GUIDE_WIZARD.md` réduit à un aiguillage) ; le test de structure vérifie
qu'il pointe vers `docs/wizard-avance.md` **et** qu'il ne contient plus de section « détail de chaque
écran ». Interdire explicitement le motif « note d'avertissement en tête + corps périmé » : la
correction se fait **dans** la phrase fausse, ou la phrase est supprimée.

**Warning signs :**
Un fichier contient à la fois « désormais » et l'ancien parcours ; deux énoncés du même fait à deux
endroits ; un `git show` de correction qui n'ajoute qu'un `>` en tête de fichier (`git show 1d475f9 --
GUIDE_WIZARD.md` = 6 lignes ajoutées, 0 ligne du corps modifiée).

**Phase to address:** **Phase 4** (wizard avancé + résorption de la dette `GUIDE_WIZARD`), avec le
contrôle de renvois obsolètes qui doit être **vu rouge sur l'état d'avant** puis vert.

---

### Pitfall 3: Les tests ne mordent que sur le code — rien ne relie la doc au produit (cause racine)

**What goes wrong:**
Le projet a 136 tests verts et **aucun** ne lit un fichier de documentation. Conséquence mesurée dans
l'historique : la doc peut mentir indéfiniment sans qu'aucune barrière ne le signale (`ab1eb38` →
`1d475f9` : deux commits de dérive non détectée). Le milestone reproduirait exactement ce défaut en
livrant des pages validées par relecture humaine — précisément ce que `PROJECT.md` (Key Decisions)
refuse, et ce que les règles du projet interdisent (aucune validation manuelle, aucun résultat
inventé).

**Why it happens:**
Écrire un test qui lit un fichier Markdown n'est pas naturel : on teste des fonctions. Et le lien
doc ↔ code traverse deux artefacts de nature différente (texte / littéraux de rendu), ce qui n'a pas
de place évidente dans une suite organisée par module.

**How to avoid:**
Chaque affirmation « ancrable » doit avoir **deux côtés** dans un même test : le runtime (client Flask
/ `build_parser()` / constantes importées) et le fichier sur disque. Un test qui n'a qu'un côté n'est
pas un contrôle d'ancrage. Et appliquer la règle d'`ARCHITECTURE.md` §8.3 : **un garde-fou introduit
en même temps que la correction doit avoir été observé rouge sur l'état antérieur** — sinon rien ne
prouve qu'il mord (pratique concrète : copier le `GUIDE_WIZARD.md` d'avant `1d475f9` dans un
`tmp_path` et vérifier que le test échoue).

**Warning signs:**
Un plan de phase dont la section « Vérification » ne cite que `pytest` sans nommer le test qui relie
doc et code ; un fichier `tests/test_docs_*.py` dont les littéraux attendus ont manifestement été
recopiés depuis la doc qu'il contrôle (voir Pitfall 4).

**Phase to address:** **Phase 1** (le harnais est le pivot de tout le milestone) ; renforcement
Phase 2 (CLI), Phase 3 (parcours), Phase 4 (dette), Phases 5-6 (pages restantes), **Phase 7**
(consolidation : suite complète verte).

---

### Pitfall 4: Le test tautologique — les deux côtés du contrôle partagent la même source

**What goes wrong:**
Le garde-fou est vert à vie et ne détecte rien. Trois formes plausibles ici :

1. **Constante recopiée.** Le test écrit `assert "5. SYSTEME" in doc` : si le menu passe à 6 entrées,
   le test reste vert et la doc re-dérive.
2. **Liste de renvois obsolètes recopiée depuis la doc fautive.** Le test « interdit les renvois
   périmés » reçoit à la main la liste des phrases de `GUIDE_WIZARD.md` — il décrit le défaut, pas la
   règle. Quand une nouvelle dérive apparaît, elle n'est pas dans la liste.
3. **Doc produite par un outil, test contre ce même outil.** Voir Pitfall 9 : générer `docs/` puis
   vérifier `docs/` contre le générateur ne prouve que la cohérence du générateur avec lui-même — pas
   que le produit existe.

**Why it happens:**
C'est la pente naturelle : recopier ce qu'on vient d'écrire est plus rapide que d'aller chercher la
vérité dans `routes.py` / `build_parser()`. Le test vert donne un sentiment de sécurité immérité.

**How to avoid:**
- Interdire toute valeur attendue recopiée à la main : elle doit provenir d'un appel de code
  (`client.get(...)`, `build_parser().parse_args(...)`, `CLASSES`, `WIZARD_STEPS`, `TYPE_FILTER_KEYS`).
- Le contrôle des renvois obsolètes doit être **dérivé** : extraire de la doc toutes les lignes qui
  associent un numéro à un libellé de navigation, et comparer le couple `(numéro, libellé)` au menu
  rendu par le runtime. Une règle, pas une liste.
- **Test de mutation** (le seul moyen de prouver que le garde-fou mord) : copier `docs/` dans
  `tmp_path`, injecter une dérive connue (remplacer « 5. SYSTEME » par « 4. SYSTEME »), et asserter
  que le contrôle échoue. Sans ce test, « c'est vérifié » n'est pas démontré.

**Warning signs :**
Un test dont les chaînes attendues ne se retrouvent nulle part dans le code ; une liste de chaînes
« interdites » maintenue à la main dans le fichier de test ; un test qui passe alors qu'on vient de
casser volontairement le fichier de doc.

**Phase to address:** **Phase 7** (le test de mutation s'ajoute quand les contrôles sont stabilisés),
mais la règle s'applique dès **Phase 1**.

---

### Pitfall 5: Vérifier la doc en exécutant ce qu'elle décrit — dont des commandes destructrices

**What goes wrong:**
Le réflexe « je vérifie que la commande documentée fait bien ça » est **interdit ici** :

| Ce que la doc décrit | Réalité du code | Effet si exécuté |
|---|---|---|
| `python fetcher.py db clear` (`README.md:78`) | `dofus_stuff/cli.py:357-360` : `deleted = db.clear()` **immédiat, sans confirmation** | vide `.data/dofus.sqlite3` ; hors-ligne, **aucun retour en arrière** |
| `4. GESTION DE LA BASE` → `VIDER LA BASE` (web) | `routes.py:844-861` : écran « **OPERATION DESTRUCTIVE** », confirmation `O` obligatoire | idem, mais **derrière un garde-fou** |
| `PURGE OUI` (`GUIDE_WIZARD.md:249`) | `terminal.js:461` : `localStorage.removeItem(SAVES_KEY)` | efface **toutes** les sauvegardes navigateur (max 20, `terminal.js:14-15`), sans copie serveur |
| `db sync` / `--force-sync` (`README.md:77`, `cli.py:344-353`) | `ensure_up_to_date(..., force=True, offline=False)` | déclenche une **vraie** resynchronisation Dofusdude |

Le CLI `db clear` est donc **plus dangereux que l'équivalent web** : la version web demande « O=OUI /
N=NON », la version CLI non. Une doc utilisateur qui place `db clear` dans la liste des commandes
courantes (`README.md:76-78`, bloc « Base locale ») enseigne une perte de données sans avertissement.

**Why it happens:**
Les commandes destructrices sont documentées au même endroit et au même niveau de détail que les
commandes de lecture ; et la petite taille du projet donne l'illusion qu'exécuter une commande est un
contrôle (« je l'ai vue marcher »). Les règles du projet bannissent pourtant explicitement `db clear`,
le drop SQLite et toute destruction sous `.data/`.

**How to avoid:**
- La surface **CLI** se vérifie par **introspection** (lecture seule) : `build_parser()` +
  `parse_args` — jamais en exécutant `main()`.
- La surface **web** se vérifie via le **client de test Flask** avec catalogue synthétique injecté
  (`tests/conftest.py`) — le motif existe déjà : `tests/test_web.py:411` exerce `/db/clear` sur la
  base **temporaire** de `tmp_path`, ce qui prouve le geste sans toucher `.data/`.
- Dans `docs/`, toute mention d'une commande destructrice est (a) absente des parcours
  (`installation.md`, `parcours-simplifie.md`, `wizard-avance.md`), (b) accompagnée d'un avertissement
  explicite là où elle est mentionnée (`base-locale.md`).
- Contrôle mécanique possible : rechercher `db clear` dans `docs/` et exiger, sur la **même ligne ou
  la suivante**, un marqueur d'avertissement (`⚠`, `ATTENTION`, `destruct`, `sauvegarde`) ; et
  interdire le motif dans `docs/installation.md` et `docs/parcours-simplifie.md`. Ne jamais exécuter
  la commande pour « vérifier la sortie ».
- Attention : `git status` **ne peut pas** montrer une destruction — `.data/` est ignoré
  (`.gitignore`). Un contrôle « la base n'a pas bougé » doit passer par l'empreinte / le mtime de
  `.data/dofus.sqlite3`.

**Warning signs:**
Une tâche de plan du type « lancer les commandes pour vérifier la sortie » ; une phase qui « nettoie
la base pour repartir d'un état propre » ; `.data/` dont la date de modification bouge pendant le
milestone.

**Phase to address:** **Phase 5** (base locale : la page qui parle de `db status|sync|clear`) ; la
règle « on ne lance pas » s'applique à **toutes** les phases et doit figurer dans les critères de
sortie de la Phase 1.

---

### Pitfall 6: Test documentaire qui ouvre la vraie base ou le réseau (non hermétique)

**What goes wrong:**
Un contrôle d'ancrage web qui construit l'application **sans injecter de catalogue** tombe sur
`web/__init__.py:46` → `DEFAULT_DATA_DIR` (`database.py:13`) → `.data/dofus.sqlite3`, et peut passer
par `ensure_up_to_date` (fenêtre de 24 h, `sync.py:11`). Résultat : test dépendant de la machine,
**faux négatif sur un clone frais** (pas de `.data/`), risque d'appel réseau et de resynchronisation —
explicitement interdit par les règles du projet. Effet secondaire : la suite passe de 1,7 s à plusieurs
secondes et devient instable, donc on finit par l'ignorer.

**Why it happens:**
`create_app()` paraît inoffensif et donne accès à des écrans « réels ». Le motif sûr existe pourtant
déjà dans le dépôt, mais il faut aller le lire.

**How to avoid:**
- Les tests d'**intégrité documentaire** n'ouvrent ni application ni base : ils lisent des fichiers
  (`Path.read_text(encoding="utf-8")`). C'est aussi ce qui les rend rapides et déterministes.
- Quand une valeur attendue doit venir d'un **écran**, réutiliser la fixture `client` de
  `tests/conftest.py` (`create_app(data_dir=tmp_path, offline=True, catalog=…, load_catalog=False)`) ;
  patcher le réseau comme le fait déjà `tests/test_web.py:380`
  (`patch("dofus_stuff.web.routes.ensure_up_to_date")`) et utiliser `skip_sync=True` comme
  `tests/test_web.py:403`.
- N'asserter aucune valeur issue de la vraie base (nombre d'objets, version Dofus réelle).

**Warning signs :**
Un test qui appelle `Catalog.load()` sans `data_dir` explicite ; un test qui échoue seulement quand
`.data/` est absent ; une durée de suite qui s'allonge anormalement.

**Phase to address:** **Phase 1** (la fixture est un pivot : écrite une fois, jamais après —
`ARCHITECTURE.md` §8.1).

---

### Pitfall 7: Comparer des chaînes brutes au rendu HTML — faux négatifs qui poussent à affaiblir les contrôles

**What goes wrong:**
Le contrôle échoue sur une doc **correcte**, l'auteur « répare » le test en relâchant l'assertion, et
la dérive revient. Cinq pièges de comparaison, tous **observés** :

| Piège | Preuve observée |
|---|---|
| Échappement HTML de l'apostrophe | Le rendu réel de `/` donne `1. RECHERCHE D&#39;OBJETS` (Jinja `autoescape`), pas `1. RECHERCHE D'OBJETS`. Le test existant contourne déjà le problème : `assert b"1. RECHERCHE" in rv.data` (`tests/test_web.py:14`). |
| Padding à 100 colonnes | Chaque ligne est `clip()`/`ljust` à exactement `COLS = 100` (`dofus_stuff/web/screens.py:14-21`) : la ligne rendue est suivie de ~79 espaces. |
| Apostrophes typographiques et accents | La prose de `GUIDE_WIZARD.md` utilise `’` (« l’optimisation », `:35`) et des accents ; les littéraux du code utilisent `'` ASCII (`routes.py:191`). Comparaison stricte = échec. |
| Casse des messages d'erreur | Le flux simplifié conserve la casse de phrase (`routes.py:964` → « Saisissez le nom ou le numéro de votre classe. »), le wizard passe tout en majuscules (`routes.py:1131` → `flash(str(exc).upper()[:COLS])`). |
| Encodage du terminal d'observation | Pendant cette recherche, la console Windows a affiché `num?ro` pour `numéro` : la sortie de shell **n'est pas** une source fiable de texte accentué. Lire les fichiers et le HTML **en Python** avec `encoding="utf-8"`. |

**Why it happens:**
La couche d'affichage du produit (padding, clipping, échappement, majuscules) est invisible quand on
lit la doc, et les tests d'écran existants ont contourné le problème plutôt que de le traiter.

**How to avoid:**
Un **seul** helper de normalisation, utilisé par tous les tests doc, documenté et testé lui-même :
`html.unescape` → repli des apostrophes (`’ ‘ ´` → `'`) → `unicodedata.normalize` pour retirer les
diacritiques **si** la comparaison est insensible aux accents → `.strip()` par ligne → espaces
multiples ramenés à un seul. Règle de rédaction : **la doc affiche verbatim** (accents, apostrophes
françaises), **le test compare normalisé**. Un test dédié (`test_normalisation_*`) prouve que le
helper traite bien `D&#39;OBJETS` ≡ `D'objets` ≡ `D’OBJETS`.

**Warning signs :**
Un `assert … in …` sur du HTML brut (`rv.data`) pour du texte accentué ou apostrophé ; un test dont
l'assertion a été raccourcie à un préfixe (`"1. RECHERCHE"`) ; une assertion retirée avec un
commentaire du type « trop fragile ».

**Phase to address:** **Phase 1** (le helper fait partie du harnais), réutilisé Phases 2 (CLI),
3 (parcours), 4 (wizard), 5 (base locale), 6 (dépannage/glossaire).

---

### Pitfall 8: Le garde-fou jamais vu rouge, et la liste de pages épinglée trop tôt

**What goes wrong:**
Deux façons de fabriquer une suite verte qui ne prouve rien :

1. **Jamais vu rouge.** Un test d'anti-dérive introduit *après* la correction, et jamais observé en
   échec, est un test non validé. La Phase 4 corrige la dérive de `GUIDE_WIZARD.md` : le contrôle doit
   être démontré rouge sur l'état d'avant (une copie du fichier d'avant dans `tmp_path` suffit — rien
   de cassé n'a besoin d'être commité).
2. **Liste de pages épinglée trop tôt.** Exiger dès la Phase 1 « les 8 pages existent » rend la suite
   rouge pendant cinq phases pour une raison *normale*. Une suite durablement rouge perd sa valeur de
   signal, on cesse de la lire, et la dérive revient — anti-pattern identifié par `ARCHITECTURE.md`
   §8.2 (point 3, « Pattern 2 »).

**Why it happens:**
Le désir de « tout verrouiller d'entrée » et la confusion entre *écrire le contrôle* et *prouver le
contrôle*.

**How to avoid:**
- Chaque phase doit voir **au moins un** de ses contrôles passer du rouge au vert lorsqu'elle corrige
  quelque chose (critère de sortie repris d'`ARCHITECTURE.md` §8.3).
- La complétude (`test_pages_requises_livrees`) arrive en **Phase 6**, pas avant ; les contrôles
  transversaux introduits en Phase 1 ne portent que sur les invariants déjà vrais (liens résolus, index
  exhaustif **auto-ajustant**, UTF-8, absence de renvois périmés sur les pages livrées).
- Convention de preuve : citer le **nom du test** dans la section « Vérification » de chaque phase, pas
  seulement « pytest ».

**Warning signs :**
Une phase dont la sortie est « la suite passe, sauf les tests de la phase suivante » ; un plan qui dit
« le test sera affiné plus tard » ; un test ajouté dans le même commit que le contenu qu'il contrôle,
sans trace de son exécution rouge.

**Phase to address:** **Phase 4** (démonstration rouge→vert) et **Phase 6** (complétude) ; règle
générale sur les 7 phases.

---

### Pitfall 9: Deux producteurs concurrents de `docs/` (un générateur LLM vise déjà le même dossier)

**What goes wrong:**
Le dépôt contient un outillage documentaire **antérieur et inactif** qui vise exactement la cible du
milestone :

- `doc-agent.toml` (racine, **non suivi**) : `output = "docs"`, `language = "fr"`,
  `base_url = "http://localhost:11434/v1"`, `model = "qwen3.8:27b"`, `max_revision_cycles = 2`.
- `.doc-agent/state.json` : `status: "running"`, `stage: "PLAN"`, `commit: 1d475f98…`,
  `documents_modified: []` — run **abandonné** ; plus `.doc-agent/lock`.
- `.gitignore` ignore `.gsd-auto/` mais **pas** `.doc-agent/` : `git status --porcelain` affiche
  `?? .doc-agent/`.

Risques concrets :

1. **Deux écrivains sur `docs/`** : une relance du générateur (ou d'un automatisme) écrase des pages
   rédigées à la main, de façon non déterministe.
2. **Doc fabriquée** : une page LLM peut décrire des commandes ou des écrans qui n'existent pas —
   exactement le risque que `PROJECT.md` nomme (« le risque dominant est de documenter un produit
   imaginaire ») et que ce document cartographie (Pitfalls 1 et 3).
3. **Débris commité** : `.doc-agent/state.json`, `.doc-agent/lock` et `runs/` peuvent partir dans un
   commit de documentation (`git add .` ou `git add -A` depuis la racine).
4. **Contrôle instable** : un test qui fige la liste des pages de `docs/` échouera de façon
   incompréhensible si le générateur ajoute un fichier.

**Why it happens:**
Un outil a été branché puis abandonné en cours de route (état `running`/`PLAN` figé sur le commit
`1d475f9`) ; personne n'a décidé si `docs/` lui appartenait.

**How to avoid:**
- `docs/` appartient **exclusivement** à ce milestone. Ne pas lancer `doc-agent`, ne pas l'utiliser
  comme source, ne pas « compléter » ses sorties.
- Le contrôle d'intégrité **épingle l'ensemble des fichiers attendus** dans `docs/` (page
  supplémentaire = échec) : c'est aussi une détection d'écriture parasite.
- Considérer `.doc-agent/` comme des débris non suivis : ne jamais faire `git add .` ; si le bruit
  persiste, ajouter `.doc-agent/` à `.gitignore` dans un commit d'hygiène local (petit, sans rapport
  avec le contenu de la doc).
- Ne pas documenter `doc-agent.toml` ni l'endpoint Ollama `localhost:11434` dans la doc utilisateur :
  ce n'est pas une fonctionnalité du produit.

**Warning signs :**
`updated_at` de `.doc-agent/state.json` qui augmente pendant le milestone ; nombre de fichiers dans
`docs/` qui change sans commit correspondant ; une page dont le style tranche avec les autres ;
`git status` annonçant des fichiers `doc-agent` en attente d'ajout.

**Phase to address:** **Phase 1** (contrôle « liste de pages » posé en mode auto-ajustant puis encadré
en Phase 6 ; la décision « pas de générateur » appartient au plan de la Phase 1).

---

### Pitfall 10: Vérification faite dans le mauvais interpréteur (ou dans une session sans `pytest`)

**What goes wrong:**
`python -m pytest -q` **échoue** sur cet hôte (`No module named pytest`) : le `python` du PATH n'est pas
celui du projet. Le projet a son propre environnement :
`./.venv/Scripts/python.exe -m pytest -q` → `136 passed in 1.69s`. Sans épingler l'interpréteur, une
phase peut (a) déclarer « tests non exécutables » et improviser, (b) conclure « vert » sans rien avoir
exécuté, (c) inventer un résultat — trois échecs de vérification invisibles dans le rapport.

**Why it happens:**
Deux environnements coexistent (celui de l'hôte GSD et celui du dépôt), et `pip install -e ".[dev]"`
n'est pas rejoué à chaque session.

**How to avoid:**
La commande de vérification du milestone est **littéralement** :
`cd <repo> && ./.venv/Scripts/python.exe -m pytest -q` (adapter le séparateur au shell actif). Elle doit
figurer dans les critères de sortie de chaque phase, et toute citation de résultat doit inclure le
**nombre de tests** et la **durée** observés, pas seulement « pytest OK ». Aucun résultat de test ne
doit être écrit sans exécution réelle.

**Warning signs :**
`ModuleNotFoundError: No module named 'pytest'` dans un log de phase ; un rapport de vérification qui
ne cite ni compteur ni durée ; `pytest` lancé via `python`/`uv run` sans mention du `.venv` du dépôt.

**Phase to address:** **Phase 1** (rappelé dans toutes les phases ; **Phase 7** pour la clôture).

---

## Technical Debt Patterns

| Shortcut | Immediate Benefit | Long-term Cost | When Acceptable |
|---|---|---|---|
| Garder `GUIDE_WIZARD.md` **et** `docs/wizard-avance.md` complets tous les deux | Aucune réécriture, contenu déjà là | Deux sources qui divergent : toute correction peut être appliquée au mauvais endroit (cause directe du Pitfall 2) | **Uniquement** comme état transitoire *à l'intérieur* de la Phase 4, jamais commité avec deux versions divergentes |
| Vérifier le sommaire dans un seul sens (index → fichiers) | Moins de code de test | Pages orphelines invisibles ; un fichier supprimé laisse une entrée morte | Jamais : les deux sens coûtent ~5 lignes (`rglob` vs entrées de l'index) |
| Liste « renvois obsolètes » écrite à la main dans le test | Très rapide à écrire | Vieillit : ne couvre que la dérive connue aujourd'hui (Pitfall 4) | Jamais pour la navigation : la règle se dérive du rendu du menu |
| Recopier dans la doc des valeurs du runtime (nombre d'objets, `%`, `version 0.2.0`, seuils PA/PM de `recommend.py`) | Exemples concrets et rassurants | Chaque copie devient fausse au prochain changement, et aucune n'est vérifiable | Acceptable **si** explicitement étiqueté « exemple indicatif » et jamais utilisé comme assertion |
| Ajouter `docs/` à `[tool.setuptools.package-data]` | Doc présente dans le wheel | Deuxième copie à garder fraîche, sdist plus gros, aucun besoin (la doc se lit dans le dépôt) | Jamais dans ce milestone (publication hors périmètre) |
| Introduire MkDocs/Sphinx « pour la navigation » | Sommaire automatique, jolie sortie | Outillage + build à maintenir ; publication hors périmètre ; `pytest` ne vérifie plus la source unique | Jamais (tranché hors périmètre dans `PROJECT.md`) |
| Pinner la liste des 8 pages dès la Phase 1 | Sentiment d'exhaustivité | Suite rouge 5 phases → signal détruit (Pitfall 8) | Jamais avant la Phase 6 |

---

## Integration Gotchas

| Integration | Common Mistake | Correct Approach |
|---|---|---|
| Base locale Dofusdude / fenêtre 24 h (`sync.py:11`, `CHECK_INTERVAL_SECONDS = 24*60*60`) | Écrire « la base se synchronise au lancement » | Écrire : la version API n'est **re-testée** que si le dernier contrôle date de **plus de 24 h** (`sync.py:23,32`), et la base n'est resynchronisée **que si la version a changé** |
| Mode hors-ligne : deux défauts **différents** | Un seul énoncé « hors-ligne par défaut » | Le **web** est hors-ligne par défaut (`web/__init__.py:49`, `web/__main__.py:22-32`, `--online` pour l'inverse) ; la **CLI** est en ligne par défaut (`cli.py:47-50`, `--offline` requis) → documenter les deux explicitement |
| `--offline db sync` | Exemple « hors-ligne » sur la synchro | Impossible : refusé par le code (`cli.py:344-348`, « `--offline` incompatible avec db sync ») |
| Options globales CLI | `fetcher.py optimize --offline …` | Les options globales se placent **avant** la sous-commande : `fetcher.py --offline optimize …` (vérifié : la forme inversée provoque `unrecognized arguments: --offline`, `SystemExit 2`) |
| Images d'objets | Croire que « hors-ligne » veut dire « aucune connexion » | L'aperçu `[ APERCU ]` charge une URL `api.dofusdu.de` (`routes.py:387-395`, bloc `item-visual` de `screen.html`) : mode hors-ligne ≠ icônes disponibles hors connexion |
| Export Dofusbook | Le présenter comme une fonctionnalité interne | Ouvre un **site externe** `https://www.dofusbook.net/fr/equipement/dofus-stuffer/objets` (`dofusbook_export.py:21`, `routes.py:1326-1338`) : navigateur + Internet requis |
| Ambiguïté `DB` | Confondre la commande `DB` (résultat) et la gestion de base | Sur l'écran résultat, `DB` = **Dofusbook** (`routes.py:1315-1316`), alors que le menu `5. SYSTEME` → `4. GESTION DE LA BASE` parle de la base SQLite : la doc doit lever l'ambiguïté explicitement |
| Sauvegardes navigateur (`terminal.js:14-15`) | Les présenter comme des données du projet | Elles vivent dans `localStorage` (`dofus-stuff-machine.saves`), **20 max**, liées au navigateur, aucune copie côté serveur ; `PURGE OUI` est irréversible |
| `README.md` aussi rendu sur PyPI (`pyproject.toml:9`, `readme = "README.md"`) | Liens relatifs vers `docs/…` / `GUIDE_WIZARD.md` | Sur PyPI, un lien relatif ne résout pas : garder une formulation explicite (« dans le dépôt : `docs/sommaire.md` ») et ne pas faire dépendre l'entrée de la doc du rendu README |

---

## Performance Traps

| Trap | Symptoms | Prevention | When It Breaks |
|---|---|---|---|
| Faire passer les tests d'intégrité doc par un rendu d'écran (ou pire, par la chaîne d'optimisation complète) | Suite qui passe de ~2 s à plusieurs secondes ; exécution d'un solveur CP-SAT à chaque test | Contrôles d'intégrité = **lecture de fichiers** ; un ou deux tests d'écran séparés, avec catalogue synthétique | Dès que `docs/` dépasse ~8 pages avec un contrôle par page |
| Relire tous les fichiers de `docs/` dans chaque test | I/O répétée, suite qui s'allonge linéairement | Une lecture par module (`docs_dir` + fixture, cf. `ARCHITECTURE.md` §8.1) | ~15–25 pages (`ARCHITECTURE.md` §9) |
| Indicateurs d'ancrage web dispersés dans plusieurs fichiers de test | Ajouter un écran demande de retrouver où sont les sondes ; on en oublie | Un seul tableau de sondes par famille (parcours / wizard / CLI / base) | Dès le 3e module de tests de doc |
| Sondes CLI figées (liste d'options recopiée) | Le test reste vert alors qu'une option n'est pas documentée | Choisir explicitement : introspection `argparse` (`build_parser()`) plutôt que sondes statiques, ou assumer la limite par écrit | Dès qu'une option est ajoutée au parseur |
| Suite durablement rouge (page listée avant d'exister) | On cesse de lire les échecs, la dérive revient | Complétude en Phase 6 (Pitfall 8) | Dès la 2e phase |

---

## Security Mistakes

| Mistake | Risk | Prevention |
|---|---|---|
| Documenter `--host 0.0.0.0` / exposer le serveur Flask de dev | Le serveur Flask de développement n'a **aucune** authentification et une clé de session par défaut (`web/__init__.py:41`, `DOFUS_SECRET_KEY` → `stuff-machine-dev-secret`) ; l'exposer sur un réseau donne un accès complet aux écrans et à la gestion de base | Garder le défaut `127.0.0.1` (`web/__main__.py:33`) et le dire ; ne mentionner `--host` que dans la section technique, avec l'avertissement « dev only, aucun contrôle d'accès » |
| Recommander `--online` / `--force-sync` « pour être à jour » | Connexion réseau non nécessaire, resynchronisation Dofusdude déclenchée alors que le mode hors-ligne est la règle ; échecs silencieux hors connexion | Ne présenter `--online` et `db sync` que dans la page « base locale », comme actions **explicites et ponctuelles** |
| Placer une clé/secret d'exemple dans `docs/` (même factice) | Invite à copier-coller un secret dans un dépôt ; brouille la frontière « ce qui se configure » | Aucun secret dans `docs/` ; si une variable d'environnement est citée, n'indiquer que son **nom** |
| Documenter `db clear` comme une étape de dépannage | Perte de la base locale, sans confirmation côté CLI (`cli.py:357-360`) ; hors-ligne, non récupérable | Pitfall 5 : retirer des parcours, avertir là où c'est cité, ne jamais l'exécuter pour vérifier |
| Documenter `PURGE OUI` sans conséquence | Les sauvegardes navigateur (jusqu'à 20) disparaissent sans copie de secours | Mention explicite « irréversible, sauvegardes locales uniquement » (`terminal.js:459-461`) |

---

## UX Pitfalls

| Pitfall | User Impact | Better Approach |
|---|---|---|
| Généraliser « Entrée à vide = écran suivant » (`GUIDE_WIZARD.md:70`) | Sur le **premier écran du flux simplifié**, Entrée à vide **échoue** : vérifié sur le rendu réel, le statut affiche « Saisissez le nom ou le numéro de votre classe. » **en même temps** que `ENTREE=SUIVANT` (messages `routes.py:964` et `:976`, pied d'écran `routes.py:1010`). Le lecteur conclut que l'outil est cassé | Décrire le contrat **par écran** : flux simplifié = saisie obligatoire (nom ou numéro) ; écrans du wizard = Entrée vide = étape suivante (`routes.py:1057-1090` pour slots/options/stats, `:1105-1107` pour items) ; récapitulatif = Entrée vide = `GO` (`routes.py:1114-1116`) |
| Présenter une barre de raccourcis unique (« F7, F8, ESC… », `GUIDE_WIZARD.md:63`) | Les barres varient : menu = `F3=Quitter` seulement (`routes.py:206-208`, pas de pagination) ; flux simplifié = `ESC=Retour` seulement (rendu réel : `fkeys ['Retour']`) ; écrans de stats du wizard = `F7`/`F8` + `ESC` (`routes.py:137-140`) | Décrire la barre **écran par écran**, ou énoncer la règle (« les flèches n'apparaissent que si l'écran peut paginer ou changer d'étape ») |
| Laisser croire que `F7`/`F8` sont inactifs quand « le clavier ne répond pas » | `F7`/`F8` sont des gestionnaires **globaux** avec `preventDefault()` (`terminal.js:548-593`) : ils fonctionnent **même pendant une saisie** et changent d'écran en abandonnant le texte tapé. Le vrai cas « inactif » est un `focus` hors du champ jaune (`terminal.js:81-85`) | Dépannage distinct : (a) cliquer dans le champ jaune si le curseur n'y est pas ; (b) avertir que `F7`/`F8` quittent l'écran et perdent la saisie non validée ; (c) ne jamais écrire « F7/F8 désactivés pendant la saisie » |
| Envoyer vers `/optimize/result` par lien | Sans calcul en session, la route redirige vers le menu avec « AUCUN RESULTAT — LANCER UN CALCUL D'ABORD » (`routes.py:1300-1324`) | Documenter le **chemin** (menu → `4` → 3 questions → calcul), jamais une URL directe |
| Décrire l'écran `STUFFS SAUVEGARDES` seulement depuis Flask | Les commandes (`N`, `BACK`, `DEL N`, `PURGE OUI`) et la pagination vivent dans `terminal.js` (`:295-494`) ; `routes.py:1282-1296` ne porte que le squelette et le libellé de statut | Rédiger cette section **depuis `terminal.js`**, en citant les commandes telles qu'affichées |
| Propager un libellé inventé pour le score | `GUIDE_WIZARD.md:224` annonce un « **% de compatibilité** » ; le code affiche « **Indice de recherche** : x % [mode] » (`optimize/api.py:339`), et `README.md:65` utilise déjà ce bon libellé | Un seul vocabulaire : « indice de recherche », repris de `optimize/api.py:339` ; le glossaire (DOCS-09) est l'endroit où ce terme est défini |
| Citer une liste figée de classes ou d'éléments | `CLASSES` contient 19 classes (`optimize/recommend.py:5-9`) affichées 3 par ligne (`routes.py:1006-1010`), et `ELEMENTS` mappe `terre→Force`, `feu→Intelligence`, `eau→Chance`, `air→Agilité` (`:10`) : une liste recopiée devient fausse au prochain ajout | Décrire la **règle** (nom ou numéro, accents tolérés, `multi`) et, si la liste apparaît, la dériver du rendu réel dans le test |
| Laisser un faux exemple de menu dans la doc | Un lecteur qui tape `3` obtient `3. LISTE DES PANOPLIES` (`routes.py:218-224`) : il perd confiance dans **tout** le reste de la doc | Pitfall 1 : le menu documenté est celui du rendu réel, contrôlé par test |
| Laisser croire que la doc « wizard » couvre le parcours d'un débutant | `GUIDE_WIZARD.md` décrit 9 écrans et des poids/cibles, alors que le parcours par défaut est 3 questions sans configuration (`routes.py:936-1010`) | Séparer explicitement deux pages (DOCS-04 vs DOCS-05) et le dire dans l'intro : « débutant → parcours simplifié ; réglages fins → wizard » |

---

## "Looks Done But Isn't" Checklist

- [ ] **Sommaire (DOCS-01) :** chaque page livrée est listée **et** chaque ligne pointe vers un fichier existant — vérifier les **deux** sens.
- [ ] **`README.md` (DOCS-02) :** renvoie vers `docs/sommaire.md`, le lien résout sur disque, et `README.md:59` ne renvoie plus vers `GUIDE_WIZARD.md` pour l'usage produit.
- [ ] **`GUIDE_WIZARD.md` (DOCS-10) :** plus de `3. OPTIMISATION` / `4. SYSTEME` / « vous arrivez directement dans le wizard » (`:35,38-42,45,50,328`), plus de « % de compatibilité » (`:224`), plus de « F7 = armes à distance » (`:157`, alors que `TYPE_FILTER_KEYS` place `arme_distance` en **F6** et `arme_melee` en **F7**, `model/solver_spec.py:43-53`), plus de détail écran par écran dupliqué.
- [ ] **CLI (DOCS-06) :** chaque commande et option citée existe dans `build_parser()` **et** chaque exemple documenté s'analyse sans erreur (options globales avant la sous-commande).
- [ ] **Flux simplifié (DOCS-04) :** les 3 étapes (`classe`, `elements`, `niveau`, `routes.py:936-1010`), la tolérance aux accents et aux numéros, `multi`, et le fait que `AVANCE` ouvre le wizard, sont décrits tels que le rendu les montre.
- [ ] **Wizard (DOCS-05) :** les 9 étapes et leurs titres viennent de `WIZARD_STEPS` / `STEP_TITLES` (`optimize_wizard.py:23-45`) ; la syntaxe des items (`+ID` interdit, `-ID` forcé, `!ID`, `CLEAR`, `:399-436`) est exacte ; le format des lignes de stats (`B=… P=… C=… W=…`, `:167-177`) est exact.
- [ ] **Base locale (DOCS-07) :** fenêtre 24 h (`sync.py:11`), **défauts différents** CLI (en ligne) / web (hors-ligne), emplacement réel de la base (« à la racine du dépôt », `database.py:13`), commandes destructrices encadrées.
- [ ] **Dépannage (DOCS-08) :** le cas « clavier » distingue `focus` hors champ et `F7`/`F8` qui changent d'écran ; « calcul long » renvoie aux vrais leviers (`top_k`, `time_limit_s`, `stop_when_satisfied`, `optimize_wizard.py:198-213`).
- [ ] **Glossaire (DOCS-09) :** chaque terme (slot, panoplie, jet, exo, indice de recherche, PA/PM/PO) a une définition cohérente avec le code.
- [ ] **Aucune valeur périssable présentée comme une vérité** (nombre d'objets, version Dofus, `version = "0.2.0"`, seuils PA/PM).
- [ ] **Garde-fou prouvé :** au moins un contrôle a été **vu rouge** sur l'état antérieur (Phase 4), et un test de mutation prouve que les contrôles mordent.
- [ ] **Interpréteur épinglé :** la vérification a été exécutée en tant que `./.venv/Scripts/python.exe -m pytest -q`, avec compteur et durée réels.
- [ ] **`.data/` intact :** vérifié par empreinte/mtime (et non par `git status`, qui ne voit pas `.data/`, ignoré).

---

## Recovery Strategies

| Pitfall | Recovery Cost | Recovery Steps |
|---|---|---|
| Numéro de menu faux découvert après rédaction (Pitfall 1) | LOW | Corriger la phrase, vérifier que le contrôle dérivé du rendu passe, relancer `pytest -q` |
| Deux sources divergentes `GUIDE_WIZARD.md` / `docs/` (Pitfall 2) | MEDIUM | Choisir `docs/wizard-avance.md` comme canon, migrer le contenu unique, réduire `GUIDE_WIZARD.md` à l'aiguillage, relancer le contrôle de structure |
| Contrôle découvert tautologique (Pitfall 4) | MEDIUM | Réécrire l'attendu depuis le runtime (client Flask / `build_parser()`), ajouter le test de mutation, revérifier qu'il est rouge sur une dérive injectée |
| `docs/` écrasé par le générateur (Pitfall 9) | MEDIUM | Restaurer depuis git (`docs/` est suivi), vérifier le contenu contre le code, figer la liste des pages, ne plus lancer l'outil |
| Contrôle affaibli pour faire passer une doc correcte (Pitfall 7) | MEDIUM | Restaurer l'assertion stricte, introduire le helper de normalisation, ajouter `test_normalisation_*`, revérifier |
| Tests non hermétiques (Pitfall 6) | LOW | Réinjecter le catalogue synthétique / patcher le réseau, revérifier qu'aucun accès `.data/` ni réseau n'a lieu |
| Base locale vidée par un `db clear` « de vérification » (Pitfall 5) | **HIGH** | Aucune restauration hors-ligne possible : recréer la base exige la resynchronisation Dofusdude (hors règle « hors-ligne par défaut »). Traiter comme un blocage à signaler, pas comme un incident mineur — la seule vraie parade est préventive |
| Vérification faite sans `pytest` disponible (Pitfall 10) | LOW | Relancer avec `./.venv/Scripts/python.exe -m pytest -q` et **citer le résultat réel** ; ne jamais reporter une vérification non exécutée |

---

## Pitfall-to-Phase Mapping

Phases alignées sur l'ordre de construction d'`ARCHITECTURE.md` §8.2 (1 socle/harnais, 2 CLI,
3 parcours simplifié, 4 wizard + résorption `GUIDE_WIZARD`, 5 base locale, 6 dépannage/glossaire/
complétude, 7 clôture).

| Pitfall | Prevention Phase | Vérification (pytest) |
|---|---|---|
| 1 — numéro de menu / écran faux | Phase 1 (harnais) + Phase 3 ; re-joué Phase 4 | Menu et titres **dérivés** du rendu `client.get("/")` ; assertion positive sur `docs/parcours-simplifie.md` **et** absence des couples obsolètes (`3. OPTIMISATION`, `4. SYSTEME`). Nommage cohérent avec `test_menu_labels_documented` / `test_libelles_parcours_simplifie` (`ARCHITECTURE.md` §6) |
| 2 — note de tête + corps périmé | Phase 4 | `GUIDE_WIZARD.md` pointe vers `docs/wizard-avance.md`, ne contient plus de section écran par écran ; le contrôle de renvois obsolètes passe **rouge → vert** dans la phase |
| 3 — rien ne relie la doc au code | Phase 1 | Les deux modules de tests doc lisent des fichiers et comparent à un appel de code (aucun contrôle « unilatéral ») |
| 4 — test tautologique | Phase 1 (règle) + Phase 7 (preuve) | Test de mutation : copie de `docs/` dans `tmp_path` avec dérive injectée → le contrôle doit échouer |
| 5 — exécution de commandes destructrices | Phase 5 (page base locale) ; règle en Phase 1 | Contrôle de sécurité documentaire : `db clear` absent de `installation.md`/`parcours-simplifie.md`, et accompagné d'un avertissement partout ailleurs ; **aucune** exécution réelle (`build_parser()` + client de test avec `tmp_path` uniquement) |
| 6 — test non hermétique | Phase 1 | La suite doc n'utilise ni `.data/` ni réseau : exécutable sur un clone sans `.data/`, sans resynchronisation |
| 7 — comparaison de chaînes brute | Phase 1 (helper), réutilisé Phases 2-6 | `test_normalisation_*` prouve `D&#39;OBJETS` ≡ `D'objets` ≡ `D’OBJETS`, padding/espaces multiples ignorés, lecture `encoding="utf-8"` |
| 8 — garde-fou jamais rouge / complétude trop tôt | Phase 4 (rouge→vert) et Phase 6 (complétude) | Trace d'un échec observé avant correction ; `test_pages_requises_livrees` introduit en Phase 6 seulement |
| 9 — deux écrivains sur `docs/` | Phase 1 (décision) + Phase 6 (complétude) | Contrôle de l'ensemble des fichiers de `docs/` : tout fichier hors liste échoue ; aucun artefact de générateur dans le dépôt suivi |
| 10 — mauvais interpréteur | Phase 1 + Phase 7 | Chaque phase cite `./.venv/Scripts/python.exe -m pytest -q` avec compteur et durée ; aucune vérification déclarée sans exécution |

### Limites honnêtes de ce harnais (à écrire dans la doc de vérification, pas à masquer)

- **Le comportement JavaScript n'est pas exécuté par `pytest`** : la saisie clavier (`F7`/`F8`/`ESC`/
  `PageUp`/`PageDown`, `Enter` pendant la saisie, `SAVE`/`PURGE OUI`) vit dans `terminal.js:548-631` et
  `:295-494`. Un test peut affirmer que les **littéraux** cités par la doc existent dans le fichier JS
  et dans les attributs `data-*` rendus (`screen.html:12-20`), mais pas qu'un appui touche produit
  l'effet décrit. Le dire, plutôt que d'écrire un test qui prétend le contraire.
- **La sortie réelle des commandes** (`db status`, `self-test`, `version`) dépend de la base locale : la
  doc ne peut l'exemplifier qu'à titre indicatif, et aucun test ne doit figer des chiffres.
- **`GUIDE_WIZARD.md` n'est pas entièrement faux** (l'ordre des 9 étapes, la syntaxe `+ID`/`-ID`, la
  table des touches restent exacts) : le risque est de « tout réécrire » et de perdre du contenu juste.
  La Phase 4 migre, elle ne réinvente pas.
- **Aucune validation humaine n'est requise ni invoquée** : tout ce qui suit est prouvable hors ligne.
  Si un critère du milestone ne pouvait pas l'être, ce serait un **blocage à signaler**, pas un
  contrôle à déclarer « validé manuellement ».

---

## Sources

Toutes les sources sont locales (aucune source web joignable : cf. note de méthode). Elles ont été
**lues** ou **exécutées** dans ce dépôt.

**Code du produit (sources de vérité)**

- `dofus_stuff/web/routes.py` — `:66-69` `DEFAULT_FKEYS`, `:137-140` injection `F7`/`F8`,
  `:189-200` menu réel, `:214-224` routage du menu (`3`→panoplies, `4`→optimisation), `:231-249` menu
  SYSTEME, `:387-395` `_item_image_url` (URL distante), `:844-880` `db_clear_confirm`/`db_clear_run`
  (confirmation `O`), `:930-1010` entrée + flux simplifié (casse du message, `fkeys`, `enter_hint`),
  `:1029-1190` wizard (Entrée vide → étape suivante, `upper()` sur les erreurs), `:1282-1296` `saves`,
  `:1300-1338` résultat / Dofusbook.
- `dofus_stuff/web/optimize_wizard.py` — `:23-45` `WIZARD_STEPS`/`STEP_TITLES`, `:167-177` format des
  lignes de stats, `:198-213` libellés d'options, `:240-260` syntaxe items, `:399-436`
  `apply_items_input`.
- `dofus_stuff/web/screens.py` — `:14-21` `clip` (padding/troncature à 100 colonnes), `:54-58`
  `pad_lines`.
- `dofus_stuff/web/static/js/terminal.js` — `:14-15` clé et limite de sauvegardes, `:295-494`
  commandes `SAVE`/`DEL`/`PURGE`, `:548-597` clavier global (`F3`, `Escape`, `F7`, `F8`, `PageUp`,
  `PageDown`, `Enter`).
- `dofus_stuff/web/templates/screen.html` — `:12-20` attributs `data-*` de navigation, bloc
  `item-visual` (aperçu distant).
- `dofus_stuff/cli.py` — `:34-50` options globales (`--offline` = `store_true`, défaut **en ligne**),
  `:52-176` commandes/options, `:180-193` boucle `db`/`cache`, `:344-360` `db sync` (refus avec
  `--offline`) et `db clear` (suppression immédiate).
- `dofus_stuff/database.py:13` — `DEFAULT_DATA_DIR` = racine du dépôt + `.data`.
- `dofus_stuff/sync.py:11,23,32` — fenêtre de 24 h.
- `dofus_stuff/web/__init__.py:41,46,49` — `DOFUS_SECRET_KEY` par défaut, `DOFUS_DATA_DIR`,
  `DOFUS_OFFLINE` par défaut `True` ; `dofus_stuff/web/__main__.py:22-41` `--offline`/`--online`.
- `dofus_stuff/optimize/api.py:339` — libellé réel « Indice de recherche ».
- `dofus_stuff/optimize/recommend.py:5-10` — `CLASSES` (19), `ELEMENTS`.
- `dofus_stuff/model/solver_spec.py:15-53` — `SLOT_GROUPS`, `TYPE_FILTER_KEYS` (F6 `arme_distance`,
  F7 `arme_melee`).
- `dofus_stuff/web/dofusbook_export.py:21` — URL externe Dofusbook.
- `pyproject.toml` — `readme = "README.md"` (`:9`), `requires-python`, extra `dev`,
  `[tool.pytest.ini_options]` (`testpaths`, `pythonpath`), `package-data`.
- `.gitignore` — `.data/` et `.gsd-auto/` ignorés ; `.doc-agent/` **non** ignoré.

**Documentation existante (cible des corrections)**

- `README.md` — `:9` base locale/fenêtre 24 h, `:44` menu web, `:59` renvoi vers `GUIDE_WIZARD.md`,
  `:65` « indice de recherche », `:76-78` bloc `db status|sync|clear`, `:102` menu 1→5.
- `GUIDE_WIZARD.md` — `:1-6` note ajoutée par `1d475f9`, `:35` « Tapez `3` », `:38-42` menu faux,
  `:45` entrée directe dans le wizard, `:50`/`:328` `4. SYSTEME`, `:63` barre de touches générique,
  `:70` « Entrée à vide = écran suivant », `:157` « F7 = armes à distance », `:224`
  « % de compatibilité », `:249` `PURGE OUI`.

**Historique git (dérive observée)**

- `ab1eb38` — menu 3→4 (`OPTIMISATION`), ajout de `3. LISTE DES PANOPLIES`, `SYSTEME` 4→5 ; tests mis
  à jour, **aucun** fichier de doc touché.
- `b3aa6f2` — F12 → ESC : code + tests + doc dans le même commit (contre-exemple : la synchro est
  possible).
- `692736b` — « Update GUIDE_WIZARD and README for menu changes » (correction manuelle d'un changement
  de menu).
- `1d475f9` — flux simplifié ; `README.md` corrigé, `GUIDE_WIZARD.md` seulement préfixé de 6 lignes.

**Tests existants (état de référence)**

- `tests/conftest.py` — catalogue synthétique + `create_app(..., load_catalog=False)` sur `tmp_path`.
- `tests/test_web.py:10-21` — le menu est épinglé **côté code** (seule protection actuelle) ; `:380`
  `patch` de `ensure_up_to_date` ; `:403` `skip_sync=True` ; `:411` `db clear` sur base temporaire.
- Exécutions : `./.venv/Scripts/python.exe -m pytest -q` → **136 passed in 1.69s** ;
  `python -m pytest -q` → `No module named pytest`.

**Outillage de recherche (résultats réels, aucun résultat inventé)**

- `gsd_run query research-plan --input …` → items `websearch` (clé `2ecbf79c…`) et `context7`
  (clé `678060c4…`).
- `gsd_run query websearch "…"` → `{"available": false, "reason": "BRAVE_API_KEY not set"}`.
- `gsd_run query classify-confidence --provider websearch` → `LOW` ; `--provider context7` → `MEDIUM`,
  mais aucun outil `mcp__context7__*` n'est exposé à cet agent : **aucun digest mis en cache**, la
  provenance d'un digest externe n'ayant pas existé.

---
*Pitfalls research for: documentation utilisateur FR d'un produit brownfield, vérifiée par pytest*
*Researched: 2026-09-10*
