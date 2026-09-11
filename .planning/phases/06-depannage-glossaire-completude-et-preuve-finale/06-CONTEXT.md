# Phase 6: Dépannage, glossaire, complétude et preuve finale - Context

**Gathered:** 2026-09-11
**Status:** Ready for planning
**Mode:** `--auto` — le porteur du projet a demandé que les libellés proposés soient retenus ; les choix ci-dessous sont la sélection recommandée, consignée au journal de discussion.

<domain>
## Phase Boundary

**Goal (ROADMAP.md § Phase 6)** : le lecteur trouve une réponse en cherchant par message d'erreur ou par
terme, et la documentation livrée est prouvée complète, non destructive et gardée par des contrôles qui
échouent réellement quand une cible dérive.

**Exigences** : AIDE-01, AIDE-02, GARD-03, GARD-04.

**Critères de succès (les 5 du ROADMAP, repris tels quels)** :

1. `docs/depannage.md` permet de retrouver chaque rubrique par le message réellement produit (base absente ou vide, saisie invalide, calcul long, clavier inactif, résultat paginé) — contrôle message → rubrique.
2. `docs/glossaire.md` définit le vocabulaire du produit et de la documentation, chaque entrée citée étant réellement présente et triée.
3. Les 8 pages épinglées sont toutes livrées, l'ensemble des fichiers de `docs/` est exactement celui attendu (toute page en trop fait échouer la suite) et le sommaire propose un parcours conseillé final.
4. Un test de mutation (copie de `docs/` sous `tmp_path` avec dérive injectée) prouve que le harnais échoue réellement : complétude, ancrage de libellé et renvois obsolètes sont détectés.
5. La vérification finale s'exécute par `.venv/Scripts/python.exe -m pytest -q` (compteur et durée réels cités), `.data/` est inchangée (empreinte ou mtime), aucune connexion réseau n'est ouverte, `main()` n'est jamais exécuté, et `git status` ne montre que `docs/`, `README.md`, `GUIDE_WIZARD.md` et `tests/`.

**Décomposition imposée par le ROADMAP** : 06-01 dépannage + index + contrôle message → rubrique ;
06-02 glossaire + index + contrôle d'entrées + parcours conseillé final ; 06-03 complétude (liste
épinglée des 8 pages + ensemble exact des fichiers de `docs/`) ; 06-04 preuve du harnais (mutation),
intégrité de `.data/`, audit de périmètre `git status`, exécution finale verte.

**Hors périmètre** : toute modification de `dofus_stuff/**` ; toute nouvelle page au-delà des 8 épinglées ;
toute resynchronisation Dofusdude ; toute publication.

</domain>

<decisions>
## Implementation Decisions

### Découpage et vagues
- **D-92:** Les 4 plans du ROADMAP sont conservés (06-01…06-04). **Les vagues sont séquentielles** : les
  quatre plans touchent `docs/` et/ou `tests/`, et 06-03/06-04 dépendent des pages livrées par 06-01 et
  06-02 (la complétude ne peut être prouvée qu'une fois les pages existantes). Aucun parallélisme n'est
  revendiqué.

### Dépannage indexé par le message réel
- **D-93:** `docs/depannage.md` est organisé **par message réellement produit**, pas par symptôme
  imaginé : chaque rubrique s'adosse à une chaîne **lue dans le code** au moment de la rédaction (D-19),
  et les cinq familles du critère 1 sont couvertes : base absente ou vide, saisie invalide, calcul long,
  clavier inactif, résultat paginé. Un message non produit par le code ne crée pas de rubrique (D-76).

### Glossaire
- **D-94:** `docs/glossaire.md` définit le vocabulaire du produit et de la documentation ; **chaque entrée
  citée est réellement présente** dans la page et **les entrées sont triées**. Le contrôle porte sur
  l'existence et l'ordre, pas sur la prose des définitions (limite déclarée, D-85).

### Complétude et ensemble exact des fichiers
- **D-95:** La **liste épinglée des 8 pages** devient une constante de test, et l'**ensemble exact des
  fichiers de `docs/`** est vérifié : **toute page en trop fait échouer la suite** (critère 3). Le
  `docs/sommaire.md` reçoit son **parcours conseillé final**, cohérent avec les pages livrées.
- **D-96:** Le contrôle de complétude vit dans `tests/`, **réutilise les fixtures partagées** (D-12) et
  suit le patron d'ancrage des phases 3 à 5 (constats citant page, valeur attendue, fichier producteur).

### Preuve du harnais
- **D-97:** Le critère 4 est prouvé par un **test de mutation** : une **copie de `docs/` sous `tmp_path`**
  reçoit une **dérive injectée**, et le harnais doit **échouer réellement** — complétude, ancrage de
  libellé et renvois obsolètes détectés. La copie doit être **verte avant mutation**, sinon la morsure ne
  prouve rien (leçon des phases 3 à 5). Chaque morsure exige un **motif nommé** dans la sortie d'échec.

### Vérification finale
- **D-98:** Le critère 5 est exécuté et **rapporté avec le compteur et la durée réellement obtenus** par
  `.venv/Scripts/python.exe -m pytest -q` — jamais une valeur attendue ou reconstituée. `.data/` est
  mesurée (empreinte) avant et après, **identique** ; aucune connexion réseau ; `main()` jamais exécuté.
  L'audit de périmètre `git status` est consigné : seuls `docs/`, `README.md`, `GUIDE_WIZARD.md` et
  `tests/` peuvent apparaître comme modifiés.
- **D-99:** Les fichiers de planification (`GUIDE_WIZARD.md`, `README.md`) ne sont touchés **que** si un
  contrôle prouve une incohérence ; sinon ils restent tels quels.

### Points hérités de la phase 5, à trancher ici
- **D-100:** L'occurrence de `db clear` dans `README.md:80` (bloc `bash`) est **explicitement transmise à
  cette phase** : elle doit être **tranchée** — soit couverte par un contrôle (le README ne présente
  alors plus une commande destructrice comme une étape), soit **conservée et déclarée** comme limite du
  périmètre, avec sa raison. Elle ne peut pas rester dans un entre-deux non écrit.
- **D-101:** La dérive préexistante de `.planning/WINDOWS.md` (`windows_ledger_table_drift`, ligne `id=5`,
  héritée de la phase 3) est **un défaut de registre connu, hors périmètre** : elle n'est **pas corrigée à
  la main** et reste déclarée. Elle n'a jamais été causée par une phase de ce run.

### Conventions et frontières
- **D-102:** Conventions des phases 1 à 5 applicables **telles quelles** : gabarit de page D-01/D-69
  (H1 = libellé d'index, `## Source de vérité`, ligne de retour en dernière ligne non vide, CRLF, UTF-8
  sans BOM), normalisation D-11, helpers partagés D-12, constats D-13, constantes publiques D-14,
  interpréteur épinglé D-15, une seule source par énoncé D-17, aucune sémantique inventée D-19, limites
  honnêtes D-85, français D-67.
- **D-103:** `dofus_stuff/**` est **lecture seule** (D-88) : la documentation se conforme au code.
- **D-104:** **Aucune action destructive sur les données** : pas de `db clear`, pas de `drop`, aucune
  suppression sous `.data/` ni sous `.doc-agent/` ; `.data/dofus.sqlite3` peut être **lue en octets**
  pour une empreinte, jamais ouverte par SQLite dans un contrôle d'intégrité. Aucune resynchronisation.
- **D-105:** Commits **locaux** uniquement, indexation **par chemin explicite** (jamais `git add .`, ni
  `doc-agent.toml`, ni `.doc-agent/`, ni `gsd-auto*.toml`, ni `.planning/state.json`) ; **aucune
  publication, aucun déploiement distant** ; **aucune dépendance ajoutée**.

### Claude's Discretion
- L'ordre des rubriques de dépannage, la formulation des entrées de glossaire, le nombre et la forme des
  morsures du critère 4, le découpage exact des contrôleurs entre 06-03 et 06-04, et le libellé du
  parcours conseillé final.

### Folded Todos
- Aucun todo en attente ne correspond au périmètre de cette phase.

</decisions>

<canonical_refs>
## Canonical References

### Cadrage
- `.planning/ROADMAP.md` § `### Phase 6` — goal, les 5 critères, les 4 plans 06-01…06-04.
- `.planning/REQUIREMENTS.md` — AIDE-01, AIDE-02, GARD-03, GARD-04.
- `.planning/PROJECT.md` — hypothèses DOCS-01…DOCS-12.

### Décisions verrouillées antérieures
- `.planning/phases/05-base-locale-hors-ligne-et-resynchronisation/05-CONTEXT.md` (D-68…D-91) et
  `05-VERIFICATION.md` (le critère 1 fermé, les deux points transmis).
- `.planning/phases/04-…/04-CONTEXT.md` (D-46…D-67), `03-…`, `01-…` (gabarit D-01, sommaire D-05).

### Code — source de vérité des messages et du vocabulaire
- `dofus_stuff/cli.py` — messages d'erreur et de refus des commandes.
- `dofus_stuff/database.py`, `dofus_stuff/sync.py` — base absente ou vide, messages de la synchronisation.
- `dofus_stuff/catalog.py`, `dofus_stuff/api.py` — messages de saisie invalide et d'accès API.
- `dofus_stuff/web/routes.py`, `dofus_stuff/web/screens.py` — écrans, pagination, clavier inactif, calcul long.

### Documentation livrée (à compléter, jamais réécrire)
- `docs/sommaire.md` — reçoit le parcours conseillé final (D-95).
- Les pages existantes : `installation.md`, `parcours-simplifie.md`, `wizard-avance.md`, `cli.md`,
  `base-locale.md` — cibles des renvois ; gabarit à respecter.
- `README.md` — occurrence `db clear` à trancher (D-100).

### Harnais
- `tests/conftest.py` — fixtures partagées (D-12).
- `tests/test_docs_structure.py`, `test_docs_parcours.py`, `test_docs_wizard.py`, `test_docs_cli.py`,
  `test_docs_base_locale.py` — gardes existantes à ne pas affaiblir ni dupliquer.

</canonical_refs>

<code_context>
### Reusable Assets
- Fixtures partagées : `app`, `client`, `docs_dir`, `normalize`, `section`, `sections`, `lignes_de_code`, `lignes_exemple`.
- Patron d'ancrage et de morsures des phases 3 à 5, dont `tests/test_docs_base_locale.py` (le plus récent, 13 → 14 tests).

### Established Patterns
- Une page = des libellés/renvois prouvés par comparaison au produit, jamais par relecture.
- Une morsure ne vaut que si la copie est verte **avant** mutation et si le motif nommé apparaît dans l'échec.
- Limites déclarées plutôt qu'exhaustivité revendiquée.

### Integration Points
- `docs/sommaire.md` : index + parcours conseillé final.
- `tests/` : nouveaux contrôleurs de complétude et de mutation, sans affaiblir les gardes existantes.
- `.planning/STATE.md`, `.planning/ROADMAP.md`, `.planning/REQUIREMENTS.md` : clôture de la phase et du jalon.

</code_context>

<specifics>
## Specific Ideas

- Le critère 4 est le **seul** du jalon qui prouve le harnais lui-même : il doit échouer sur une dérive
  injectée, pas seulement passer sur l'état livré.
- Le critère 3 interdit une page **en trop** autant qu'une page manquante : la liste épinglée est
  l'invariant, pas le décompte.
- Le rapport final doit citer un **compteur et une durée réellement observés** ; toute valeur non mesurée
  serait exactement le défaut que ce jalon a corrigé deux fois.

</specifics>

<deferred>
## Deferred Ideas

- Aucune : cette phase clôt le jalon. Les deux points transmis par la phase 5 (occurrence `db clear` du
  README, registre `.planning/WINDOWS.md`) sont traités ici ou déclarés (D-100, D-101).

</deferred>

---

*Phase: 06-depannage-glossaire-completude-et-preuve-finale*
*Context gathered: 2026-09-11*
