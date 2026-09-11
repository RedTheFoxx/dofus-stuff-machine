# Phase 5: Base locale, hors-ligne et resynchronisation - Context

**Gathered:** 2026-09-11
**Status:** Ready for planning
**Mode:** --auto (le porteur du projet a choisi « Run discuss-phase first » puis « Research first » ; les décisions ci-dessous retiennent l'option recommandée, consignée au journal de discussion)

<domain>
## Phase Boundary

**Goal (ROADMAP.md § Phase 5)** : un lecteur comprend la base SQLite locale, la fenêtre de
resynchronisation et les deux comportements hors-ligne, et ne lance jamais une commande destructrice
par inadvertance.

**Livrable de cette phase** : `docs/base-locale.md` (page unique du sujet), une ligne d'index dans
`docs/sommaire.md`, et le module de contrôle d'ancrage qui la garde. Aucun changement de code produit.

**Exigences** : BASE-01, BASE-02, BASE-03.

**Critères de succès (les 5 du ROADMAP, repris tels quels)** :

1. `docs/base-locale.md` décrit le fichier `.data/dofus.sqlite3`, les catégories d'objets stockées et la fenêtre de re-check de 24 heures.
2. Les deux défauts hors-ligne sont distingués explicitement (web hors-ligne par défaut, CLI en ligne par défaut donc `--offline` requis) et les champs affichés par l'état de la base sont décrits par leurs noms, sans aucune valeur volatile.
3. Les cas non évidents sont couverts : `db status` crée le fichier s'il n'existe pas, `db sync` refuse `--offline`, l'écran web de synchronisation contacte l'API même en mode hors-ligne.
4. Les commandes destructrices (`db clear`, `PURGE OUI`) sont signalées comme telles sur la même ligne et n'apparaissent dans aucun parcours ; les contrôles de la phase n'écrivent pas sous `.data/`, n'exécutent aucune synchronisation et n'ouvrent aucune connexion réseau.
5. Chaque nom de champ ou de commande cité par la page est produit par le code, et la suite reste verte avec l'interpréteur épinglé.

**Hors périmètre** : la preuve de complétude des 8 pages et la liste épinglée des pages, la page de
dépannage par message d'erreur, le glossaire (phase 6) ; toute modification de `dofus_stuff/**` ;
toute resynchronisation Dofusdude.

</domain>

<decisions>
## Implementation Decisions

### Périmètre et gabarit de `docs/base-locale.md`
- **D-68:** La page est la **source unique** du sujet « base locale » : le fichier, les catégories
  d'objets stockées, la fenêtre de re-check de 24 h, les deux défauts hors-ligne et les champs de
  l'état de la base. Aucun de ces énoncés n'est décrit deux fois ailleurs (D-17) ; les pages voisines
  y renvoient par lien.
- **D-69:** Gabarit de page hérité, sans exception (D-01) : `H1` unique `# Base locale` **égal au
  libellé d'index** après normalisation, introduction en français, sections courtes, bloc
  « Source de vérité » dont **chaque chemin entre accents graves existe sur disque**, dernière ligne
  non vide `[Retour au sommaire](sommaire.md)`. Fichier **CRLF, UTF-8 sans BOM** (D-67).
- **D-70:** `docs/sommaire.md` gagne **exactement une** ligne d'index
  `| [Base locale](base-locale.md) | … |` **à cette phase** — l'index croît au rythme des pages créées
  (D-05). L'ordre des lignes existantes et l'ordre du « Parcours conseillé » ne sont pas remaniés. La
  liste épinglée des 8 pages reste à la phase 6.

### Les deux défauts hors-ligne (critère 2)
- **D-71:** Les deux défauts sont énoncés **séparément et nommés par leur surface**, jamais fusionnés
  en une phrase générale : **le web est hors-ligne par défaut** et **la CLI est en ligne par défaut,
  donc `--offline` y est requis**. Chaque énoncé dit **où** il s'applique (lancement web / commande CLI).
- **D-72:** Les **orthographes exactes** des drapeaux et leurs textes d'aide sont **lus dans le code**
  au moment de la recherche et de la rédaction, jamais écrits de mémoire (D-19). La page ne cite un
  drapeau que si le code le porte.

### Fenêtre de re-check de 24 heures (critère 1)
- **D-73:** La fenêtre est documentée depuis le code (`dofus_stuff/sync.py`,
  `CHECK_INTERVAL_SECONDS = 24 * 60 * 60`), **constante nommée**, sans recopier aucune date, durée
  calculée ni horodatage (D-72 ci-dessus : aucune valeur volatile).

### Fichier et catégories stockées (critère 1)
- **D-74:** Le nom du fichier est documenté depuis `dofus_stuff/database.py` (`DB_NAME`), pas depuis
  la mémoire. Les **catégories d'objets réellement stockées** sont relevées dans le code (schéma,
  modules d'écriture) ; la page ne revendique aucune catégorie que le code ne stocke pas.

### Champs de l'état de la base (critères 2 et 5)
- **D-75:** Chaque **nom de champ ou de commande** cité par la page est **produit par le code** :
  lu dans une constante publique (D-14) ou au rendu, jamais recopié de mémoire. Les champs sont décrits
  **par leurs noms**, sans aucune **valeur volatile** (date, taille, compteur, version courante).
- **D-76:** Un champ dont le nom n'est produit ni par une constante publique ni par un rendu
  observable **n'est pas cité** : la page ne décrit que ce qu'un contrôle peut ancrer.

### Cas non évidents (critère 3)
- **D-77:** `db status` **crée le fichier s'il n'existe pas** : le comportement est décrit comme tel,
  et il est **prouvé sans toucher `.data/`** (répertoire temporaire, jamais la base réelle).
- **D-78:** `db sync` **refuse `--offline`** : le refus est décrit et **son message réel** est cité
  depuis le code (`dofus_stuff/cli.py`), jamais paraphrasé.
- **D-79:** L'écran web de synchronisation **contacte l'API même en mode hors-ligne** : c'est le seul
  endroit où le mode hors-ligne **ne s'applique pas**, et la page le dit explicitement.

### Commandes destructrices (critère 4)
- **D-80:** `db clear` et `PURGE OUI` sont **signalées comme destructrices sur la même ligne** que la
  commande, et n'apparaissent dans **aucun parcours recommandé**. La page ne présente jamais l'une
  d'elles comme une étape à suivre.
- **D-81:** **Aucun contrôle de la phase n'exécute une commande destructrice**, n'écrit sous `.data/`,
  n'exécute de synchronisation, ni n'ouvre de connexion réseau. La démonstration d'un comportement qui
  toucherait la base se fait **exclusivement** dans un répertoire temporaire (`tmp_path`), et
  l'intégrité de la base réelle est mesurée (empreinte) **avant et après la suite entière**.

### Contrôles d'ancrage (critère 5)
- **D-82:** Un module dédié `tests/test_docs_base_locale.py` porte l'ancrage de la page ; il **réutilise
  les fixtures partagées** de `tests/conftest.py` et ne les recopie pas (D-12).
- **D-83:** Chaque constat d'échec cite **la page, la valeur attendue et le fichier de code
  producteur** (D-13), de sorte qu'un échec dise quoi corriger sans lecture supplémentaire.
- **D-84:** Les morsures sont jouées **sur une copie verte en répertoire temporaire, avant mutation**,
  jamais sur l'arbre réel ni sur `.data/` ; chaque morsure rapportée provient d'une **sortie réellement
  obtenue**, jamais d'un résultat attendu.
- **D-85:** Le module **déclare ses limites honnêtes** : ce que la page ne revendique pas
  (couverture et précision des contrôles), sans revendiquer d'exhaustivité.

### Frontières et conventions
- **D-86:** Les renvois de la page se font **par lien uniquement là où la cible existe** (leçon D-44) :
  aucun lien mort, aucune cible citée en prose sans lien lorsqu'elle n'existe pas encore.
- **D-87:** La phase 5 porte en plus le contrôle de complétude demandé par le porteur du projet :
  **les renvois de `README.md` pointent vers des fichiers qui existent**. Le libellé « T6 » employé par
  le porteur n'a **aucune définition dans les artefacts de planification** (vérifié : aucune
  occurrence) : le critère est donc pris **à la lettre** (les renvois du README résolvent) et n'est pas
  étendu à une liste de pages que le README ne cite pas.
- **D-88:** `dofus_stuff/**` n'est **pas modifié** : le code est la référence et la page s'y conforme
  (D-19).
- **D-89:** **Aucune resynchronisation Dofusdude** n'est déclenchée par cette phase ; le travail se fait
  **hors-ligne d'abord** sur la base locale existante. Aucun `db clear`, aucun `drop`, aucune
  suppression sous `.data/` ni sous `.doc-agent/`.
- **D-90:** Conventions des phases 1 à 4 applicables **telles quelles** (D-01…D-67) : normalisation
  accents/casse/CRLF/balises (D-11), helpers partagés (D-12), constats (D-13), constantes publiques
  (D-14), interpréteur épinglé `./.venv/Scripts/python.exe` (D-15), une seule source par énoncé (D-17),
  aucune sémantique inventée (D-19), français (D-67).
- **D-91:** Commits **locaux** uniquement, indexation **par chemin explicite** (jamais `git add .`, ni
  `doc-agent.toml`, ni `.doc-agent/`, ni `gsd-auto*.toml`, ni `.planning/state.json`) ; **aucune
  publication, aucun déploiement distant** ; **aucune dépendance ajoutée**.

### Claude's Discretion
- L'ordre exact des sections à l'intérieur de la page, la formulation de l'introduction.
- Le nombre et la forme des contrôles d'ancrage, et le découpage des sections du module de test.
- Le point de savoir si les deux défauts hors-ligne ont leur propre section ou sont deux sous-blocs
  d'une même section.
- Les termes exacts employés pour signaler le caractère destructeur, tant que l'avertissement est
  **sur la même ligne** que la commande (D-80).

### Folded Todos
- Aucun todo en attente ne correspond au périmètre de cette phase.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Cadrage de la phase
- `.planning/ROADMAP.md` § `### Phase 5: Base locale, hors-ligne et resynchronisation` — goal, les 5 critères de succès, et les 3 plans 05-01 / 05-02 / 05-03 avec leur objet.
- `.planning/REQUIREMENTS.md` — BASE-01, BASE-02, BASE-03 (traçabilité exigée par la vérification de phase).
- `.planning/PROJECT.md` — valeur du produit et règles d'évolution.

### Décisions verrouillées des phases précédentes (à lire avant de planifier)
- `.planning/phases/04-wizard-avanc-et-r-sorption-de-la-dette-guide-wizard/04-CONTEXT.md` — D-46…D-67, dont le gabarit D-01/D-56, la dette de renvoi D-44/D-63 et les conventions D-65…D-67.
- `.planning/phases/03-parcours-simplifi-document-depuis-le-rendu-r-el/03-CONTEXT.md` — ancrage au rendu, valeurs volatiles interdites, limites honnêtes.
- `.planning/phases/01-socle-documentaire-installation-et-harnais-v-rifiable/01-CONTEXT.md` — gabarit de page (D-01), sommaire qui croît par phase (D-05), harnais vérifiable.

### Code — source de vérité à lire avant de rédiger
- `dofus_stuff/database.py` — `DB_NAME = "dofus.sqlite3"` : nom du fichier de base locale.
- `dofus_stuff/sync.py` — `CHECK_INTERVAL_SECONDS = 24 * 60 * 60` et la raison `within_24h` : la fenêtre de re-check.
- `dofus_stuff/cli.py` — `--offline`, les sous-commandes `db status` / `db sync` / `db clear`, et le refus « `--offline` incompatible avec `db sync` ».
- `dofus_stuff/web/__main__.py` — `--offline` côté web (le défaut hors-ligne du web).
- `dofus_stuff/web/routes.py` — l'écran d'état / de sauvegarde de la base et la barre portant `PURGE OUI`.
- `dofus_stuff/api.py` — l'accès à l'API Dofusdude que la synchronisation contacte.

### Pages de documentation (gabarit, index et voisines)
- `docs/sommaire.md` — l'index à faire croître d'une seule ligne (D-70).
- `docs/installation.md`, `docs/cli.md`, `docs/parcours-simplifie.md`, `docs/wizard-avance.md` — pages voisines : gabarit à respecter, cibles de liens autorisées (D-86).
- `README.md` — les renvois dont la résolution est contrôlée (D-87).

### Harnais de tests
- `tests/conftest.py` — fixtures partagées à réutiliser (`app`, `client`, `docs_dir`, `normalize`, `section`, `sections`, `lignes_de_code`, `lignes_exemple`), D-12.
- `tests/test_docs_structure.py` — gardes existantes d'index/`H1`/retour/encodage, inchangées.
- `tests/test_docs_wizard.py` — le modèle de l'ancrage au rendu et des morsures sur copie verte (phase 4), à imiter sans le recopier.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `tests/conftest.py` : `app`, `client` (client de test Flask en processus, base sous `tmp_path`), `docs_dir`, `normalize`, `section`, `sections`, `lignes_de_code`, `lignes_exemple` — tout l'ancrage de la page passe par là.
- `tests/test_docs_wizard.py` (phase 4) : fonction pure d'analyse + constats citant la page et le fichier producteur, et morsures sur copie verte — le patron à réutiliser.

### Established Patterns
- **Page ancrée au code** : les phases 3 et 4 ont établi qu'une page documentaire se prouve par des contrôles qui comparent ses libellés au produit, pas par une relecture.
- **Valeurs volatiles interdites** : aucune date, taille, version ou compteur recopié (phases 3 et 4).
- **Morsure discriminante** : la copie doit être verte **avant** mutation, sinon la morsure ne prouve rien.
- **Base jamais touchée par les tests** : la fixture construit sa propre base sous `tmp_path` ; l'empreinte de `.data/dofus.sqlite3` est mesurée autour de la suite entière.

### Integration Points
- `docs/sommaire.md` : une ligne d'index ajoutée (D-70) — les gardes de structure existantes vérifient l'index, le `H1`, la ligne de retour et l'encodage.
- `README.md` : les renvois sont contrôlés (D-87) sans réécrire le README au-delà du nécessaire.
- `tests/` : nouveau module d'ancrage, sans toucher aux modules existants.

</code_context>

<specifics>
## Specific Ideas

- La page ne doit **jamais** se lire comme une invitation à lancer une commande destructrice : `db clear` et `PURGE OUI` existent pour être **reconnues**, pas pour être suivies.
- Le **risque de confusion central** de cette phase est la coexistence de deux défauts hors-ligne opposés selon la surface (web / CLI) : c'est le point où une page peut être vraie « en général » et fausse en pratique.
- L'écran web de synchronisation qui contacte l'API **même hors-ligne** est un piège de lecture : il doit être dit, pas laissé deviner.

</specifics>

<deferred>
## Deferred Ideas

- Preuve de complétude des pages et liste épinglée des pages → phase 6.
- Dépannage par message d'erreur → phase 6.
- Glossaire → phase 6.
- Toute discussion sur une resynchronisation Dofusdude (hors périmètre : le travail est hors-ligne d'abord).

</deferred>

---

*Phase: 05-base-locale-hors-ligne-et-resynchronisation*
*Context gathered: 2026-09-11*
