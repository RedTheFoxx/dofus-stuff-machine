---
phase: 03-parcours-simplifi-document-depuis-le-rendu-r-el
plan: 02
subsystem: documentation
tags: [markdown, pytest, flask-test-client, ast, pagination, resultat, documentation-francaise]

# Dependency graph
requires:
  - phase: 03-parcours-simplifi-document-depuis-le-rendu-r-el
    provides: "docs/parcours-simplifie.md (les trois sections de questions, le bloc Source de vérité, la ligne de retour) et tests/test_docs_parcours.py (helpers _lignes_du_corps, _statut, _touches, _client_etape, _couples_du_rendu, _couples_de_section, constantes de titres TITRE_RESULTAT et TITRE_SUPPOSE), suite verte à 176 tests"
  - phase: 01-socle-documentaire-installation-et-harnais-v-rifiable
    provides: "harnais documentaire partagé (docs_dir, normalize, section, lignes_de_code) et invariants de docs/ (liens, sommaire, H1, encodage)"
provides:
  - "docs/parcours-simplifie.md : la section « Lire le résultat » (carte de pagination lue dans la ligne de statut, absence de carte sur un résultat d'une page, barre F7=Page prec / F8=Page suiv / ESC=Retour, et emplacement des trois diagnostics en fin de résultat) et la section « Correspondance des libellés » (la table des 17 emplacements réellement rendus)"
  - "tests/test_docs_parcours.py : _libelles_display_slots (extraction par ast de display_slots), SLOTS_MESURE (17 paires libellé / nom complet / source / aiguille), _attribut, et les tests test_pagination_et_emplacement_du_calcul (V5, V6) et test_correspondance_libelles_slots (V7)"
affects: [03-03, 03-04]

# Actuals (#2632) — mesurés sur la même échelle que l'estimate du plan (chars/4 du diff réalisé).
actuals:
  tokens: 6978     # chars/4 sur le diff réalisé (27 914 caractères ajoutés, 0 retiré)
  tasks: 2
  commits: 2       # MESURE : git rev-list --count 55ec185be077c5585a7606096ae890aa675f3a9a..HEAD
  plan_head_before: 55ec185be077c5585a7606096ae890aa675f3a9a

# Tech tracking
tech-stack:
  added: []          # aucune dépendance ajoutée (contrainte projet C1)
  patterns:
    - "Rendu Flask en processus pour la lecture du résultat : la carte de pagination et la position des diagnostics sont lues sur les pages réellement rendues, jamais déduites du code (D-32)"
    - "Assertion POSITIONNELLE des diagnostics sur les pages concaténées dans l'ordre : jamais un indice de page, jamais une comparaison page == total (reformulation enregistrée ÉCR-2)"
    - "Table de correspondance adossée au code : les libellés viennent d'une extraction ast de display_slots, et chaque nom complet est re-vérifié sur la ligne de la source qui le porte (patron LIBELLES_SOURCE, D-42)"
    - "Constat accumulés joints à une seule assertion, message citant la page, la section, le libellé attendu et le fichier de code (D-13)"

key-files:
  created: []
  modified:
    - docs/parcours-simplifie.md
    - tests/test_docs_parcours.py

key-decisions:
  - "La carte de pagination est lue dans la ligne de statut et confrontée aux attributs data-body-page / data-body-total de la coquille : la cohérence statut <-> attributs est exigée sans épingler aucun total, le total dépendant du catalogue (mesure M6)."
  - "La position des diagnostics est exigée sur la concaténation des pages de résultat, après le dernier « Équipement : » et avant « Greedy: », la phrase du catalogue devant suivre immédiatement le dernier diagnostic — aucune comparaison entre un numéro de page et le total n'existe dans le module (ÉCR-2)."
  - "La section « Lire le résultat » ne fige aucune valeur volatile : les quatre motifs interdits (Score : \\d, Indice de recherche : \\d, Greedy: \\d, Méthode : [a-z]) sont contrôlés sur le texte de la section, et la page écrit « en fin de résultat » plutôt que « dernière page »."
  - "SLOTS_MESURE porte l'aiguille de ligne qui porte le nom complet dans sa source (par exemple \"amulet\", dans dofus_stuff/web/dofusbook_export.py, ou \"prysmaradite\", dans dofus_stuff/model/solver_spec.py) : le contrôle ne vérifie pas seulement que le nom existe quelque part dans le fichier, mais qu'il est lisible sur la même ligne que le libellé."
  - "Le tableau de la page est lu ligne de tableau, jamais en prose : une même ligne peut porter plusieurs libellés, comme les six dofus_1 à dofus_6, et chaque libellé de display_slots doit y apparaître exactement une fois."
  - "Aucune troncature n'est promette ni assertee : la section « Correspondance des libellés » ne contient ni « libellé tronqué » ni le caractère de points de suspension, et le module n'asserte nulle part l'apparition de ce caractère sur un rendu (reformulation enregistrée ÉCR-1, mesure M7)."
  - "Le solveur tourne une seule fois dans ce plan, sur la fixture minimale déterministe (niveau 200, quatre éléments) : trois pages mesurées, diagnostics en page 2/3, module sous 0,8 s."

patterns-established:
  - "Pattern 1 : lecture d'un résultat paginé sans jamais épingler un total — le total est capturé dans la ligne de statut puis réutilisé pour parcourir les pages et confronter les attributs"
  - "Pattern 2 : vérité extraite du code par ast, avec garde qui nomme le fichier, la table et la plage de lignes plutôt qu'un AttributeError brut"
  - "Pattern 3 : table épinglée (libellé, nom complet, source, aiguille) re-vérifiée dans les deux sens — la page ne peut ni inventer ni oublier un emplacement"

requirements-completed: [SIMP-02]

coverage:
  - id: D1
    description: "docs/parcours-simplifie.md : la section « Lire le résultat » décrit la carte de pagination de la ligne de statut, l'absence de carte sur un résultat d'une page, la barre F7=Page prec / F8=Page suiv / ESC=Retour du résultat et l'emplacement des trois diagnostics en fin de résultat"
    requirement: "SIMP-02"
    verification:
      - kind: integration
        ref: "tests/test_docs_parcours.py#test_pagination_et_emplacement_du_calcul"
        status: pass
    human_judgment: false
  - id: D2
    description: "Le résultat est réellement rendu sur la fixture : la ligne de statut porte PAGE 1/<total>, les attributs de la coquille s'accordent avec elle, la page <total>/<total> est atteinte, et les diagnostics sont exigés par leur position sur les pages concaténées"
    requirement: "SIMP-02"
    verification:
      - kind: integration
        ref: "tests/test_docs_parcours.py#test_pagination_et_emplacement_du_calcul"
        status: pass
      - kind: other
        ref: "batterie de morsures tâche 1 : 2/2 détectées (carte de pagination renommée, diagnostics retirés du flux simplifié), copie verte vérifiée avant chaque mutation"
        status: pass
    human_judgment: false
  - id: D3
    description: "docs/parcours-simplifie.md : la section « Correspondance des libellés » porte la table des 17 emplacements rendus, chaque nom complet recopié de la source qui le porte"
    requirement: "SIMP-02"
    verification:
      - kind: integration
        ref: "tests/test_docs_parcours.py#test_correspondance_libelles_slots"
        status: pass
    human_judgment: false
  - id: D4
    description: "La table de la page couvre exactement les libellés de display_slots (aucun inventé, aucun manquant, chacun une seule fois et sur la même ligne que son nom complet), et quatre dérives rougissent le module"
    requirement: "SIMP-02"
    verification:
      - kind: integration
        ref: "tests/test_docs_parcours.py#test_correspondance_libelles_slots"
        status: pass
      - kind: other
        ref: "batterie de morsures tâche 2 : 4/4 détectées (ligne de tableau supprimée, nom complet renommé dans la source, libellé du tableau altéré, libellé retiré de display_slots), copie verte vérifiée avant chaque mutation"
        status: pass
    human_judgment: false
  - id: D5
    description: "Aucune troncature n'est promise ni assertee, aucune valeur volatile n'est figée par la page, et .data/dofus.sqlite3 reste intact"
    requirement: "SIMP-02"
    verification:
      - kind: unit
        ref: "tests/test_docs_parcours.py#test_correspondance_libelles_slots"
        status: pass
      - kind: other
        ref: "mesure locale : .data/dofus.sqlite3 inchangé après chaque tâche (24 989 696 octets, mtime_ns 1788730056843137500) ; suite complète verte à 178 tests"
        status: pass
    human_judgment: false
  - id: D6
    description: "Le lecteur doit reconnaître un mot du jeu (« coiffe » pour hat) : la correspondance est adossée au code, mais son adéquation au vocabulaire du joueur reste une lecture humaine — annoncée comme telle dans la page"
    requirement: "SIMP-02"
    verification:
      - kind: manual_procedural
        ref: "relecture humaine de la table de la page ; la page écrit elle-même qu'il s'agit d'une correspondance de lecture, pas d'une sortie de l'outil"
        status: unknown
    human_judgment: true

duration: 6 min
completed: 2026-09-11
status: complete
---

# Phase 3 Plan 02: Pagination, emplacement du calcul et correspondance des libellés Summary

**Le critère 2 est tenu dans ses deux moitiés mesurées : la carte de pagination est lue dans la ligne de statut du résultat réel et confrontée aux attributs de la coquille, les trois diagnostics sont exigés par leur position sur les pages concaténées (jamais « sur la dernière page »), et la table des 17 emplacements est adossée à une extraction `ast` de `display_slots` dont chaque nom complet est re-vérifié sur la ligne de sa source.**

## Performance

- **Duration:** 319 s ≈ 6 min pour les deux tâches (mesuré : `date +%s` 1789145098 → 1789145417, du premier garde de racine au vert de la tâche 2 ; la clôture SUMMARY puis STATE/ROADMAP suit)
- **Started:** 2026-09-11T16:44:58Z
- **Completed:** 2026-09-11T16:50:17Z (fin de la vérification de la tâche 2)
- **Tasks:** 2
- **Files modified:** 2 (0 créé, 2 modifiés)

## Accomplishments

- `docs/parcours-simplifie.md` gagne les deux sections du critère 2, insérées **avant** `## Source de vérité` : « Lire le résultat » (absence de carte sur un résultat d'une page, carte `PAGE n/total` dans la ligne de statut suivie de `ENTREE=VALIDER`, barre `F7=Page prec` / `F8=Page suiv` / `ESC=Retour` distinguée de celle du wizard avancé, trois diagnostics **en fin de résultat — jusqu'à `PAGE n/n`** suivis de la phrase du catalogue, valeurs annoncées comme changeant d'une exécution à l'autre, `(vide)` et la règle des emplacements omis) et « Correspondance des libellés » (table de 17 libellés techniques → nom complet).
- `tests/test_docs_parcours.py` gagne `_attribut`, `_libelles_display_slots` (extraction `ast` de `display_slots`, garde nommant fichier, table et lignes), la table épinglée `SLOTS_MESURE` (17 entrées, aiguille de ligne par entrée), et les deux tests `test_pagination_et_emplacement_du_calcul` (V5, V6) et `test_correspondance_libelles_slots` (V7).
- Le résultat est **réellement rendu** par le client de test Flask : un `POST /optimize/quick/niveau` avec `cmd=200` sous `recommendation_input` (classe `Cra`, les quatre éléments) redirige en `302` vers `/optimize/result`, puis les pages sont lues une à une. Mesures locales : **3 pages**, ligne de statut `ID DETAIL | SAVE [NOM] | SAVES | EDIT | DB — PAGE 1/3 — ENTREE=VALIDER`, diagnostics sur la ligne 34 (`Méthode : cpsat (OPTIMAL)`) et 35 (`Score : … | Indice de recherche : …`), phrase du catalogue en 36, `Greedy:` en 37 — donc **page 2/3** pour les diagnostics, jamais la dernière page.
- Les six dérives épinglées par le plan sont détectées sur une copie vérifiée verte avant mutation : carte de pagination renommée et diagnostics retirés du flux simplifié (tâche 1, 2/2) ; ligne de tableau supprimée, nom complet renommé dans le commentaire d'export, libellé du tableau altéré, libellé retiré de `display_slots` (tâche 2, 4/4) — chacune nommant la page, le libellé ou le marqueur attendu et le fichier de code.
- Suite complète verte : **178 passed** (176 après la vague 1 + 2 nouveaux). `.data/dofus.sqlite3` intact après chaque tâche.

## Task Commits

Each task was committed atomically:

1. **Tâche 1 : la carte de pagination et l'emplacement des diagnostics lus sur le rendu** - `8818460` (feat)
2. **Tâche 2 : la table libellé technique → nom complet ancrée sur display_slots et les commentaires d'export** - `0d24f68` (feat)

**Plan metadata:** `HEAD` après le commit de clôture de ce plan (docs: complete plan).

_Note: `TDD_MODE=false` pour cette phase — aucun cycle RED/GREEN/REFACTOR n'était requis._

## Files Created/Modified

- `docs/parcours-simplifie.md` (modifié, +30 lignes, 177 lignes au total, CRLF, UTF-8 sans BOM) — les sections `## Lire le résultat` et `## Correspondance des libellés`, insérées avant `## Source de vérité`, qui reste la dernière section avant la ligne de retour au sommaire.
- `tests/test_docs_parcours.py` (modifié, +479 lignes, 1 323 lignes au total, CRLF, UTF-8 sans BOM) — les constantes du résultat (`ETAT_RESULTAT`, `NIVEAU_RESULTAT`, `MOTIF_PAGE_STATUT`, `ATTRIBUTS_COQUILLE`, `MARQUEURS_DIAGNOSTICS`, `PHRASE_CATALOGUE`, `PREFIXE_EQUIPEMENT`, `PREFIXE_GREEDY`, `EMPLACEMENT_VIDE`, `TOUCHES_RESULTAT`, `TOUCHES_WIZARD`, `TOURNURE_DERNIERE_PAGE`, `MOTIFS_VALEURS_VOLATILES`, `TABLE_SLOTS`, `NOMBRE_SLOTS`, `SLOTS_MESURE`, `LIBELLE_ENTRE_ACCENTS`, `TITRE_CORRESPONDANCE`, `TRONCATURE_PAGE`, `POINTS_DE_SUSPENSION`, `SOURCE_SCREENS`), les helpers `_attribut` et `_libelles_display_slots`, et les deux tests.

## Decisions Made

- **Total de pages jamais épinglé.** La ligne de statut est lue par un motif, le total est capturé puis réutilisé pour parcourir les pages et confronter `data-body-page` / `data-body-total` / `data-mode`. Aucune constante de page n'existe dans le module : le total dépend du catalogue (mesure M6 : 3 pages sur la fixture, 6 puis 7 sur la base réelle).
- **Assertion positionnelle, jamais un indice de page.** Les diagnostics sont cherchés sur la **concaténation** des pages du résultat, après le dernier `Équipement :` et avant `Greedy:`, la phrase du catalogue devant suivre immédiatement le dernier diagnostic. Aucune comparaison page == total n'existe : ce serait faux sur une implémentation correcte (ÉCR-2).
- **Vérité des libellés extraite du code.** `_libelles_display_slots()` parcourt les `Assign` / `AnnAssign` dont la cible s'appelle `display_slots` et lit un `ast.Tuple` de constantes de type `str` ; si la table disparaît ou change de forme, l'échec nomme `dofus_stuff/optimize/api.py:362-380` et dit que la table a peut-être été renommée, plutôt que de lever un `AttributeError` brut.
- **La table du module est vérifiée dans les deux sens.** Chaque libellé de `display_slots` doit apparaître **exactement une fois** dans les lignes de tableau de la section (les six `dofus_1` à `dofus_6` partageant une ligne), tout libellé du tableau absent du code est signalé comme inventé, et tout libellé du code absent du tableau est signalé comme manquant — l'absence ne passe pas en silence.
- **Chaque nom complet est re-vérifié sur la ligne de sa source.** `SLOTS_MESURE` porte une aiguille (le fragment qui porte le nom dans sa ligne) : les noms viennent des commentaires de `_GROUP_SLOTS` (`dofus_stuff/web/dofusbook_export.py:26-37`) pour les seize emplacements exportés, et de `dofus_stuff/model/solver_spec.py` (`"prysmaradite",`) pour `prysma`, le seul emplacement absent de cet export.
- **Aucune troncature promise ni assertee.** La section ne contient ni « libellé tronqué » ni le caractère de points de suspension, et le module n'asserte nulle part ce caractère sur un rendu : la règle `clip` existe mais ne se déclenche pas dans ce flux (mesure M7, reconstatée localement : 0 ligne rendue du résultat ne porte de points de suspension, longueur maximale mesurée 79 sur la fixture).
- **Aucune valeur volatile figée.** Les quatre motifs interdits sont contrôlés sur le texte de la section, et la page écrit « en fin de résultat — jusqu'à `PAGE n/n` » là où la version antérieure du critère disait « dernière page » (la tournure `dernière page` est contrôlée absente, comparaison après normalisation).
- **La page ne dit pas ce qui appartient à la phase 4.** La barre du **résultat** (`Page prec` / `Page suiv`) est exigée présente et les libellés du **wizard** (`Precedent` / `Suivant`) exigés absents du rendu du résultat, avec le renvoi en prose — sans lien — vers le wizard non encore livré (D-43, D-44).

## Deviations from Plan

### Auto-fixed Issues

None — le plan a été exécuté comme écrit. Aucune règle 1, 2, 3 ou 4 n'a été déclenchée : aucune écriture sous `.data/`, aucun solveur hors de la fixture, aucune dépendance, aucun chemin `dofus_stuff/**` modifié.

### Non-deviations worth recording

- **Le helper `_touches` n'a pas été redéfini.** Le plan le liste dans la sortie du plan ; il a été posé par la tâche 1 du plan 03-01 (il y sert déjà à exiger `ESC=Retour`) et il est ici **seulement réutilisé**, conformément à D-12.
- **`SOURCE_SCREENS`, `TITRE_CORRESPONDANCE` et `_attribut` sont ajoutés au module.** Les deux premières suivent la convention des constantes existantes (`SOURCE_*`, `TITRE_*`) et sont consommées par les messages de contrôle ; `_attribut` évite de répéter trois fois le même `re.search` sur les attributs `data-*` de la coquille.
- **Une ligne de tableau peut porter six libellés.** Les six emplacements Dofus sont cités ensemble sur une ligne, comme le plan le prévoit explicitement ; le contrôle compte les libellés, pas les lignes.

### Reformulations enregistrées honorées (ROADMAP § Phase 3)

- **ÉCR-1** : la table porte sur le **libellé technique → nom complet**, jamais sur une troncature ; aucun contrôle n'asserte l'apparition d'un caractère de points de suspension, et la page n'invoque aucune troncature inexistante.
- **ÉCR-2** : « `Méthode` / `Score` / `Indice de recherche` » ne sont **pas** décrits comme étant sur la dernière page. La page écrit « en fin de résultat — jusqu'à `PAGE n/n` » et le contrôle est positionnel ; le paragraphe de déviation du ROADMAP n'a pas été touché.

## Issues Encountered

- **Le rendu de la fixture place les diagnostics en page 2/3**, pas sur la dernière page — ce qui est exactement le piège qu'ÉCR-2 documente. Mesuré avant écriture du contrôle (sonde `.gsd-tmp/plan-p3/probe_pagination.py`), puis reconstaté par le test lui-même. Un contrôle qui aurait exigé la dernière page aurait été faux sur une implémentation correcte.
- **`data-stuff-payload` porte tout le résultat sur chaque page** (accents échappés par `tojson`) : aucune assertion du module ne porte sur la réponse entière, tout passe par `_lignes_du_corps` et `_statut` — vérifié en lisant la charge utile pendant la sonde.
- **Fins de ligne.** Les deux fichiers modifiés sont restés 100 % CRLF, UTF-8 sans BOM (mesuré octet par octet après chaque écriture).
- Aucun blocage : ce plan n'exige ni geste humain, ni secret, ni accès réseau. `.data/dofus.sqlite3` n'a jamais été ouvert (24 989 696 octets et `mtime_ns` 1788730056843137500 avant et après chaque tâche), la fixture `app` construisant sa propre base sous `tmp_path`.

## Known Stubs

None — aucun stub, aucun `TODO`, aucun test en `skip`, aucune `<verify>` non exécutée. Les quatre blocs `<verify>` du plan (module seul, batterie de morsures de la tâche 1, module seul, batterie de morsures de la tâche 2, plus la suite complète) ont été exécutés et leurs sorties sont citées ci-dessus.

## Threat Flags

Aucune surface nouvelle : ce plan n'ajoute aucun endpoint, aucune route, aucune dépendance et aucun secret ; il étend une page `docs/` et un module de test qui lisent le dépôt. Les menaces du `<threat_model>` du plan sont couvertes : T-7 (aucune valeur volatile, aucune total épinglé, fixture déterministe), T-8 (assertions limitées aux lignes du corps et à la ligne de statut), T-9 (noms complets recopiés de la source **et** re-vérifiés sur la ligne qui les porte), T-10 (aucune promesse de troncature, aucun contrôle sur les points de suspension), T-11 (`mtime_ns` et taille de `.data/dofus.sqlite3` identiques avant et après chaque tâche).

## Next Phase Readiness

- **Prêt pour 03-03** : la page et le module sont en place ; les sections du plan 03-03 (`## Sauvegarder et exporter`) s'insèrent **avant** `## Source de vérité`, et le module offre désormais `_attribut`, `_libelles_display_slots` et `SLOTS_MESURE` en plus des helpers de la vague 1.
- **Contraintes à honorer par les plans suivants** : insérer les sections **avant** `## Source de vérité`, laisser `[Retour au sommaire](sommaire.md)` en dernière ligne, ne pas ajouter de second exemplaire des couples des deux menus (le contrôle de la vague 1 en compte 23 exactement) et ne pas ajouter de ligne de tableau portant un libellé de slot hors de la section « Correspondance des libellés » sans mettre à jour `SLOTS_MESURE`.
- **Aucun blocage.** `03-VALIDATION.md` reste à mettre à jour par `/gsd:validate-phase`, pas par cet exécuteur.

## Self-Check: PASSED

- `docs/parcours-simplifie.md` : FOUND (177 lignes, CRLF, UTF-8 sans BOM, H1 unique, `## Lire le résultat` avant `## Source de vérité`, dernière ligne `[Retour au sommaire](sommaire.md)`)
- `tests/test_docs_parcours.py` : FOUND (1 323 lignes, CRLF, UTF-8 sans BOM, 9 tests verts)
- Commit `8818460` : FOUND — feat(03-02) lit la pagination et l'emplacement du calcul sur le rendu du resultat
- Commit `0d24f68` : FOUND — feat(03-02) correspondance libelle technique -> nom complet des emplacements
- `./.venv/Scripts/python.exe -m pytest tests/test_docs_parcours.py -q` : 8 passed après la tâche 1, 9 passed après la tâche 2 (0,78 s)
- `./.venv/Scripts/python.exe -m pytest -q` : 177 passed après la tâche 1, 178 passed après la tâche 2
- Batterie de morsures de la tâche 1 : 2/2 détectées, copie verte avant chaque mutation
- Batterie de morsures de la tâche 2 : 4/4 détectées, copie verte avant chaque mutation
- `.data/dofus.sqlite3` : 24 989 696 octets, `mtime_ns` 1788730056843137500 — identique aux valeurs mesurées avant la tâche 1
- Commits mesurés : `git rev-list --count 55ec185be077c5585a7606096ae890aa675f3a9a..HEAD` = 2

---

*Phase: 03-parcours-simplifi-document-depuis-le-rendu-r-el*
*Completed: 2026-09-11*
