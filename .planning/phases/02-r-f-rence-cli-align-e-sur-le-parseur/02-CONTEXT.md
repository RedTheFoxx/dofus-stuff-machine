# Phase 2: Référence CLI alignée sur le parseur - Context

**Gathered:** 2026-09-11
**Status:** Ready for planning

<domain>
## Phase Boundary

Livrer `docs/cli.md` : une page de référence où **chaque sous-commande, chaque option et chaque exemple est réellement analysable** par le parseur d'arguments de `fetcher.py`, plus son entrée dans `docs/sommaire.md` et les contrôles d'ancrage qui gardent la page vraie.

Délimitation : cette phase **documente** la surface CLI existante (`version`, `self-test`, `search`, `item`, `list`, `optimize`, `db`/`cache`). Elle ne modifie **aucune** ligne de `dofus_stuff/**`, n'ajoute aucune option, ne documente ni le dépannage par message d'erreur (phase 6), ni le glossaire (phase 6), ni le parcours simplifié (phase 3), ni le wizard avancé (phase 4), ni la base locale hors-ligne et la resynchronisation (phase 5).

</domain>

<decisions>
## Implementation Decisions

### Profondeur & structure par sous-commande
- **D-16:** Une section par sous-commande, **dans l'ordre réel du parseur** (`version`, `self-test`, `search`, `item`, `list`, `optimize`, `db`), chacune avec : synopsis, options propres et leurs **valeurs par défaut réellement lues dans le parseur**, un exemple.
- **D-17:** **Pas de table récapitulative en fin de page.** Une table unique dupliquerait le parseur et deviendrait un second référentiel à maintenir — contraire au principe « une seule source par énoncé » (même raison que D-10 pour le lien unique `README.md` → `docs/sommaire.md`). La source de vérité est le parseur ; la page le décrit.

### Surface des options d'`optimize`
- **D-18:** **Toutes** les options d'`optimize` sont documentées, en **tables groupées par thème** (profil/poids, contraintes, caractéristiques de base & scrolls, RNG/perf), avec synopsis et défaut issus du code réel (~30 options : `--base-*`, `--scroll-*`, `--level`, `--top-k` défaut 30, `--seed` défaut `None`, options de contraintes et de perf).
  — **Reversibility:** costly — Si un groupe thématique est mal découpé, le corriger impose de réécrire les tables de la page et de re-valider les contrôles d'ancrage des options déjà écrits en phase 2, ainsi que la section de `docs/cli.md` que les phases 3 et 6 citeront comme référence.
- **D-19:** **Aucune sémantique inventée.** Une option dont le sens n'est pas lisible dans le code est décrite par son synopsis et son défaut, sans interprétation ajoutée. Le critère 2 du ROADMAP n'exige que « chaque option **documentée** » soit acceptée par le parseur ; la complétude retenue ici vient de l'utilité pour le lecteur, pas d'une obligation de tout documenter, et la page reste honnête sur ce qu'elle ne dit pas.

### Alias `cache` et commandes destructrices
- **D-20:** `cache` est présenté **comme alias de `db`**, sans description dupliquée. Les sous-commandes masquées du help (`stats`, `fill`, `argparse.SUPPRESS`) sont signalées **comme telles** et rattachées à leur nom canonique.
- **D-21:** Le lien d'alias est prouvé **par le parseur public**, sans recopier de texte : `cache <sous-commande>` et `db <sous-commande>` doivent produire un espace de noms équivalent. Aucune API privée d'`argparse` (D-14).
- **D-22:** `db clear` est mentionné **hors parcours recommandé**, avec l'**avertissement destructif sur la même ligne**, et jamais proposé comme étape. Le nom exact du drapeau est **lu dans le parseur** au moment de rédiger, pas inventé. Aucun `db clear` n'est exécuté, à aucun moment.
- **D-23:** La liste des sous-commandes réellement destructrices (`db clear`, et `db sync` / `cache fill` qui réécrivent la base) est dérivée du code, pas supposée ; toute commande retenue comme destructrice doit apparaître **avec** son avertissement et **en dehors** de tout parcours conseillé.

### Ancrage des exemples et limite du contrôle
- **D-24:** Seules comptent comme « exemples » les lignes situées dans des **blocs de code balisés comme tels** (marqueur explicite), pas les commandes citées en prose — sinon le contrôle devient fragile.
- **D-25:** Vérification d'un exemple : présence **verbatim** dans la page **et** analyse par `shlex.split(...)` → `build_parser().parse_args(...)`, parseur public uniquement (D-14).
- **D-26:** **Limite honnête consignée dans le test lui-même** : une sous-commande ou une option ajoutée plus tard au parseur et **non documentée ne fera pas échouer la suite** (le contrôle est page → parseur plus une liste explicite). Aucune exhaustivité totale n'est revendiquée.
- **D-27:** L'**ordre réel** est illustré : au moins un exemple hors-ligne place l'option globale **avant** la sous-commande (`--offline optimize …`), conformément au comportement mesuré en phase 1.

### Sommaire et README
- **D-28:** `docs/sommaire.md` gagne **l'entrée `cli.md` maintenant** (le sommaire croît par phase, D-05) ; la liste épinglée des 8 pages reste en phase 6 (D-05). Le test d'exhaustivité bidirectionnelle (D-06) doit rester vert sans exception.
- **D-29:** `README.md` garde son **lien unique** vers `docs/sommaire.md` — aucun lien direct vers `cli.md` (D-10).

### Gabarit et ancrage au code
- **D-30:** `docs/cli.md` suit le gabarit de D-01 : H1 unique, phrase d'introduction, sections courtes, bloc **« Source de vérité »** pointant vers `dofus_stuff/cli.py` § `build_parser()` et `fetcher.py` (point d'entrée), et ligne de retour vers `docs/sommaire.md`. Chaque chemin `.py` du bloc doit exister sur disque (D-03).
- **D-31:** Les conventions de test de la phase 1 s'appliquent sans modification : comparaisons après normalisation (D-11), helpers dans le `tests/conftest.py` existant (D-12), message d'échec citant **la page, la valeur attendue et le fichier de code** (D-13), exécution de référence `.venv/Scripts/python.exe -m pytest -q` sans exécuter `main()`, sans écrire sous `.data/`, sans connexion réseau (D-15).

### Claude's Discretion
- Découpage exact des groupes thématiques des tables d'`optimize` (D-18 fixe le principe, pas le nombre de groupes).
- Forme du marqueur qui identifie une ligne comme « exemple » (D-24), tant qu'il reste détectable par test sans ambiguïté.
- Formulation du synopsis de chaque sous-commande et de la phrase d'introduction de la page.
- Ordre des groupes à l'intérieur des tables, dès lors que les options et leurs défauts sont exacts.
- Découpage interne des nouveaux tests (module dédié `tests/test_docs_cli.py` ou extension d'un module existant) — seule contrainte : ne pas dupliquer les helpers de `tests/conftest.py` (D-12).

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Cadrage de la phase
- `.planning/ROADMAP.md` § « Phase 2: Référence CLI alignée sur le parseur » — objectif et les 5 critères de succès opposables, plus la liste des 3 plans (02-01, 02-02, 02-03)
- `.planning/REQUIREMENTS.md` — `CLI-01`, `CLI-02`, `CLI-03` (lignes 41-43) et la table de traçabilité (lignes 122-124)
- `.planning/PROJECT.md` — valeur centrale du milestone : « chaque commande/menu cité dans le code réel », « sans rencontrer de documentation périmée »
- `.planning/phases/01-socle-documentaire-installation-et-harnais-v-rifiable/01-CONTEXT.md` — décisions **D-01…D-15** verrouillées en phase 1, toutes applicables ici (gabarit, sommaire croissant, normalisation, helpers, messages d'échec, API publique, exécution de référence)

### Source de vérité du code (frozen pour cette phase)
- `dofus_stuff/cli.py` — `build_parser()` : surface réelle des sous-commandes, options et défauts ; `db`/`cache` et `argparse.SUPPRESS` sur `stats`/`fill` ; drapeau de `db clear`
- `fetcher.py` — point d'entrée CLI (`from dofus_stuff.cli import main`)
- `pyproject.toml` — interpréteur/livrable attendus (`python_requires` 3.11+), extra `dev`

### Pages livrées et gabarit à respecter
- `docs/installation.md` — page livrée en phase 1, modèle de gabarit (H1, sections, bloc « Source de vérité », ligne de retour)
- `docs/sommaire.md` — index unique à faire croître avec l'entrée `cli.md` (D-05/D-28)
- `README.md` — lien unique vers le sommaire, à ne pas modifier au-delà (D-10/D-29)

### Harnais de tests existant (à étendre, pas à dupliquer)
- `tests/conftest.py` — fixture `docs_dir` et helper de normalisation partagés (D-11/D-12)
- `tests/test_docs_structure.py` — invariants de structure et d'exhaustivité bidirectionnelle du sommaire (D-06)
- `tests/test_docs_code_anchor.py` — ancrage chemins/options/libellés, y compris le contrôle bidirectionnel de la surface web (modèle du contrôle page ↔ parseur de cette phase)

### Politique de dépendances
- `pyproject.toml` — aucune dépendance ne doit être ajoutée par cette phase (aucun parseur de Markdown tiers : le format est contraint et déjà traité à la main par le harnais existant)

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `tests/conftest.py` : fixture `docs_dir` + helper de normalisation (minuscules, accents, CRLF/LF, balises HTML) — réutilisés tels quels, jamais recopiés (D-12).
- `tests/test_docs_code_anchor.py` : contient déjà le patron « dériver une surface depuis le parseur public, comparer dans les deux sens, nommer la dérive » — c'est le modèle direct des contrôles d'options de cette phase.
- `tests/test_docs_structure.py` : contient déjà les helpers purs `pages_listees` / `problemes_index` / `problemes_h1` et le test de mutation sur copie jetable — le contrôle de l'entrée `cli.md` dans le sommaire passe par là, sans nouveau mécanisme.

### Established Patterns
- **Ancrage par surface publique** (D-14) : `build_parser().parse_args(...)` et `format_help()`, jamais d'attribut privé d'`argparse`.
- **Contrôle bidirectionnel** : une surface documentée et une surface du parseur doivent s'égaliser, sinon échec nommant les deux côtés.
- **Message d'échec localisant** (D-13) : page + valeur attendue + fichier de code.
- **Mutation sur copie jetable** (`tmp_path` / `tempfile`) : jamais d'écriture dans `docs/` du dépôt.
- **Exécution de référence** `./.venv/Scripts/python.exe -m pytest -q`, sans `main()`, sans réseau, sans écriture sous `.data/`.
- **Prose en français**, code/chemins/identifiants/frontmatter inchangés.

### Integration Points
- `docs/sommaire.md` : ajouter l'entrée `cli.md` fait basculer le test d'exhaustivité (D-06) — l'ajout de la page et de l'entrée doit se faire dans le même plan.
- `tests/conftest.py` : tout nouveau helper partagé y va (D-12), les helpers spécifiques à la CLI restent dans le module de tests CLI.
- `dofus_stuff/cli.py` : lecture seule, source d'information — aucune écriture, aucune importation qui exécuterait `main()`.
- Phase 3 puis phase 6 : `docs/cli.md` deviendra une cible de lien et une référence citée ; son H1 doit donc rester stable et égal à son libellé d'index (D-06).

</code_context>

<specifics>
## Specific Ideas

- Le contrôle de l'alias est explicitement requis comme **équivalence d'espace de noms** via le parseur, pas comme comparaison de texte : c'est la seule formulation qui ne se périme pas si les descriptions changent.
- L'avertissement destructif doit tenir **sur la même ligne** que la mention de `db clear`, pour qu'un test puisse exiger leur co-présence sans analyse sémantique.
- La limite du contrôle (D-26) doit être écrite **dans le test lui-même**, pas seulement dans le plan : un futur lecteur du harnais doit voir ce que le contrôle ne garantit pas.
- Le bloc « Source de vérité » doit nommer `build_parser()` comme la fonction précise, pas seulement `dofus_stuff/cli.py` : c'est ce qui rend le contrat vérifiable au-delà de l'existence du fichier.

</specifics>

<deferred>
## Deferred Ideas

- **Table récapitulative unique de toute la surface CLI** — écartée (D-17) : second référentiel à maintenir, contraire à « une seule source par énoncé ».
- **Documenter une sémantique non lisible dans le code** (intention d'une option, valeur recommandée) — hors périmètre (D-19) ; relèverait d'un guide d'usage, pas d'une référence.
- **Complétude prouvée dans les deux sens pour toute la surface CLI** (toute sous-commande/option du parseur doit être documentée) — non retenue (D-26) : rendrait toute évolution future du parseur bloquante. Reste un contrôle page → parseur plus une liste explicite.
- **Dépannage par message d'erreur, glossaire, liste épinglée des 8 pages** — phases 5 et 6.
- **Parcours simplifié du rendu réel** — phase 3.

None — la discussion est restée dans le périmètre de la phase, à l'exception des points ci-dessus, explicitement écartés ou renvoyés à une phase ultérieure.

</deferred>

---

*Phase: 2-Référence CLI alignée sur le parseur*
*Context gathered: 2026-09-11*
