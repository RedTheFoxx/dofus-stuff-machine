# Phase 1: Socle documentaire, installation et harnais vérifiable - Context

**Gathered:** 2026-09-11
**Status:** Ready for planning

<domain>
## Phase Boundary

Cette phase livre le **socle de la documentation utilisateur** et le **harnais qui la garde** :

**Livré :**
- Une section « Documentation utilisateur » dans `README.md` qui pointe vers `docs/sommaire.md`
- `docs/sommaire.md` : point d'entrée unique, parcours guidé ordonné + index thématique, ne listant que les pages réellement livrées
- `docs/installation.md` : de Python 3.11+ au premier lancement CLI **et** web, pilotage clavier compris
- `tests/test_docs_structure.py` : invariants internes de la doc (liens relatifs résolus, exhaustivité bidirectionnelle sommaire ↔ `docs/**/*.md`, un seul H1 égal au libellé d'index, ligne de retour, UTF-8 strict)
- `tests/test_docs_code_anchor.py` (première moitié) : chemins des blocs « Source de vérité » existants, options d'entrée web acceptées par le parseur réel

**Non livré par cette phase (phases suivantes) :**
- `docs/cli.md` (phase 2), `docs/parcours-simplifie.md` (phase 3), `docs/wizard-avance.md` + résorption de `GUIDE_WIZARD.md` (phase 4), `docs/base-locale.md` (phase 5), `docs/depannage.md` + `docs/glossaire.md` + liste épinglée des 8 pages (phase 6)
- Le contrôle des renvois obsolètes (phase 4), la complétude épinglée et le test de mutation (phase 6)

**Hors périmètre, sans exception :** toute modification de `dofus_stuff/**`, tout générateur de site statique, toute nouvelle dépendance, toute écriture sous `.data/`, tout réseau, toute publication.

</domain>

<decisions>
## Implementation Decisions

### Gabarit de page
- **D-01:** Gabarit **léger** pour chaque page `docs/` : un `H1` unique, une phrase d'introduction, des sections courtes, un bloc **« Source de vérité »** listant les chemins réels du code (ex. `dofus_stuff/cli.py`, `dofus_stuff/web/routes.py`, `pyproject.toml`), et une ligne de retour vers le sommaire. Pas de front-matter, pas de bloc de métadonnées d'en-tête.
- **D-02:** Les encadrés « erreur fréquente » ne sont ajoutés que là où l'erreur est **réellement rencontrée** (attendu dans `installation.md`), jamais systématiquement sur toutes les pages.
- **D-03:** Le bloc « Source de vérité » crée un contrat vérifiable : chaque chemin `.py` qui y figure doit exister sur disque — c'est le premier ancrage au code que `tests/test_docs_code_anchor.py` vérifie.

### Parcours & sommaire
- **D-04:** `docs/sommaire.md` est le **point d'entrée unique** : un parcours guidé ordonné (Installation → Parcours simplifié → Wizard avancé → CLI → Base locale → Dépannage → Glossaire) suivi d'un tableau d'index thématique, **sur la même page**. Pas de sommaire secondaire, pas de page annexe.
- **D-05:** Le sommaire **croît par phase** : il ne liste que les pages réellement livrées (donc uniquement `installation.md` en phase 1) et gagne une entrée à chaque phase. La liste épinglée des 8 pages n'arrive qu'en phase 6, quand toutes les cibles existent.
- **D-06:** Conséquence directe : le test d'exhaustivité bidirectionnelle (toute page listée existe / aucune page non listée) reste **vert à tout moment**, sans exception ni tolérance pour cible absente.

### Détail installation
- **D-07:** `docs/installation.md` suit un **chemin minimal pas-à-pas d'abord** : Python 3.11+, environnement virtuel, `pip install -e ".[dev]"`, vérification, lancement CLI (`python fetcher.py version`) et web (`python -m dofus_stuff.web`, adresse par défaut), puis une courte section « erreurs fréquentes ».
- **D-08:** **Ni `uv` ni aucun autre gestionnaire de paquets ne sera documenté.** `pyproject.toml` déclare `setuptools` + `pip` et l'extra `dev` ; documenter un outil non utilisé serait inventer une procédure.
- **D-09:** Le pilotage clavier de l'interface web (champ de saisie, `F7`, `F8`, `ESC`, `PageUp`, `PageDown`) est décrit **avant** de lancer l'interface, pas après.
- **D-10:** La section « Documentation utilisateur » du `README.md` contient un **lien unique** vers `docs/sommaire.md`. Aucun lien direct vers les pages individuelles : la même information ne vit qu'à un endroit.

### Tests : ancrage
- **D-11:** Les comparaisons de libellés, de touches et de chemins se font **après normalisation** : minuscules, accents insensibles, espaces et fins de ligne CRLF/LF unifiés, balises HTML retirées.
  — **Reversibility:** costly — Si la normalisation s'avère trop permissive (un test qui passe alors que la doc diverge), la corriger impose de reprendre les helpers de `tests/conftest.py` et de re-valider chaque assertion déjà écrite dans les phases 2 à 6, qui s'appuient dessus.
- **D-12:** Les helpers de test vivent dans le `tests/conftest.py` **existant** (fixtures `docs_dir`, fonction de normalisation testée), pas dans un module d'aide dédié.
- **D-13:** Chaque échec de test doit citer la page concernée, le libellé attendu et le fichier de code où il n'a pas été trouvé — un échec sans ces trois éléments est considéré comme un défaut du harnais.
- **D-14:** Interdits d'introspection acquis du cadrage : pas d'API privée d'`argparse`, pas de lecture d'attributs internes ; l'ancrage passe par le parseur public (`build_parser().parse_args`) et par le client de test Flask.
- **D-15:** Exécution de référence du harnais : `.venv/Scripts/python.exe -m pytest -q`, **sans** exécuter `main()`, **sans** écrire sous `.data/`, **sans** ouvrir de connexion réseau.

### Claude's Discretion
- Nom exact des fixtures et des fonctions de helper dans `tests/conftest.py` (seule contrainte : le comportement de normalisation de D-11 est testé).
- Découpage interne de `tests/test_docs_structure.py` en classes ou en fonctions.
- Formulation exacte du parcours guidé et de l'index dans `docs/sommaire.md` (seule contrainte : ordre de lecture et exhaustivité vérifiables).
- Choix de la ligne de retour au sommaire (libellé et forme du lien relatif), tant qu'un H1 unique et un lien résolu restent vérifiables par test.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Cadrage produit
- `.planning/PROJECT.md` — contexte, valeur centrale, périmètre validé du milestone, décisions déjà actées (dont « sauter la cartographie de codebase » et « livrable `docs/` multi-fichiers »)
- `.planning/REQUIREMENTS.md` — les 25 exigences v1 et leur traçabilité ; cette phase couvre SOMM-01, SOMM-02, SOMM-03, INST-01, INST-02, INST-03, GARD-01, GARD-02
- `.planning/ROADMAP.md` § Phase 1 — objectif, dépendances et les 5 critères de succès opposables

### Recherche (source des contraintes de conception)
- `.planning/research/SUMMARY.md` — synthèse : Markdown nu + stdlib + `pytest` existant, zéro dépendance nouvelle ; recommandation explicite de garder la liste épinglée des 8 pages en **dernière** phase
- `.planning/research/ARCHITECTURE.md` — structure à plat sous `docs/`, contrat « le code est la source de vérité, la doc est le reflet, le test est le juge »
- `.planning/research/PITFALLS.md` — pièges mesurés (136 tests verts dont aucun ne lit un fichier de doc ; `GUIDE_WIZARD.md` contredit le code depuis `1d475f9`)
- `.planning/research/FEATURES.md` — périmètre des 8 pages attendues
- `.planning/research/STACK.md` — justification de l'absence de générateur de site statique et de vérificateur de liens tiers

### Code réel à refléter (le produit est figé)
- `pyproject.toml` — `requires-python >= 3.11`, extra `dev` avec `pytest>=8.0`, `[tool.pytest.ini_options]` (`testpaths = ["tests"]`, `pythonpath = ["."]`)
- `dofus_stuff/cli.py` § `build_parser()` — parseur réel des sous-commandes et options (source d'ancrage pour la phase 2, déjà utilisé par la phase 1 pour les options d'entrée web)
- `dofus_stuff/web/routes.py`, `dofus_stuff/web/screens.py` — routes et écrans réellement rendus, libellés visibles par le lecteur
- `tests/conftest.py` — fixtures existantes et fabrique de catalogue d'exemple ; point d'accueil des helpers de cette phase
- `README.md` — état actuel (français, orienté technique) et section « Documentation utilisateur » à ajouter
- `tests/test_web.py`, `tests/test_screens.py` — précédents de test du rendu web réellement affiché (modèle à suivre pour l'ancrage)

### Hors dépôt
- Aucun document externe, aucun ADR, aucune spécification tierce. Toutes les contraintes sont capturées par les décisions ci-dessus et le cadrage `.planning/`.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `tests/conftest.py` : propose déjà une fixture complète de client Flask alimentée par une fabrique de catalogue d'exemple (`_sample_items()`) — l'ancrage des libellés web s'appuie dessus au lieu de créer un second harnais.
- `pyproject.toml` `[tool.pytest.ini_options]` : `testpaths = ["tests"]` et `pythonpath = ["."]` sont déjà configurés — les nouveaux modules de test sont détectés sans configuration supplémentaire ; `pytest>=8.0` est déjà dans l'extra `dev`.
- `.venv/Scripts/python.exe` : interpréteur épinglé du dépôt, base de l'exécution de référence de D-15.
- `tests/test_screens.py` / `tests/test_web.py` : montrent comment le rendu réel est obtenu via le client de test — patron à réutiliser pour l'ancrage de libellés.

### Established Patterns
- **Français partout** dans le contenu produit et les libellés d'interface ; identifiants et chemins de code restent en anglais.
- **Aucune dépendance nouvelle** : le mode de vérification du projet est `pytest` + bibliothèque standard, jamais un vérificateur tiers.
- **Pas d'exécution destructive** : les tests observent (parseur, rendu, disque) ; ils n'exécutent ni `main()`, ni commande d'écriture, ni accès réseau.
- **Fins de ligne CRLF** dans les fichiers déjà présents sous Windows, et contenu français accentué en UTF-8 — d'où la normalisation de D-11 ; toute lecture de fichier doit fixer l'encodage explicitement.
- Fichiers de documentation produits par commit dédié (`docs:` / `docs(0N):`), staging par chemin explicite, jamais `git add .`.

### Integration Points
- `README.md` : la nouvelle section « Documentation utilisateur » remplace la redirection actuelle vers `GUIDE_WIZARD.md` (ligne 59) comme point d'entrée documentaire — la correction complète de cette redirection appartient à la phase 4.
- `docs/sommaire.md` : point d'ancrage de toutes les entrées ajoutées par les phases 2 à 6 ; le contrôle d'exhaustivité bidirectionnelle de cette phase devient le garde-fou de ces ajouts.
- `tests/test_docs_code_anchor.py` : module ouvert en phase 1, complété par les phases 2, 3, 4, 5 puis conclus par le test de mutation de la phase 6.
- `dofus_stuff/cli.py` § `build_parser()` : surface publique du parseur, utilisée par l'ancrage CLI sans toucher au module.

</code_context>

<specifics>
## Specific Ideas

- Le harnais est le **produit** de cette phase autant que la doc : la recherche a mesuré que 136 tests verts ne lisaient aucun fichier de documentation alors que `ab1eb38` avait modifié le menu web sans mettre à jour un seul document. La valeur de la phase se juge sur ce que les deux modules de test refusent de laisser passer.
- Formulation de référence du milestone, à reprendre telle quelle : « le code est la source de vérité, la doc est le reflet, le test est le juge ».
- L'échec doit être **lisible et localisant** (D-13) : c'est la contrepartie de la normalisation de D-11 — un test permissif qui ne dit pas où est la divergence est pire qu'un test strict.
- Le choix « croît par phase » (D-05) signifie que le sommaire de la phase 1 contient **une seule entrée** ; ce n'est pas un défaut de complétude mais la condition pour que le contrôle bidirectionnelle reste un vrai signal pendant cinq phases.
- `docs/installation.md` documente un lancement **hors-ligne** : l'installation ne doit déclencher aucune resynchronisation Dofusdude.

</specifics>

<deferred>
## Deferred Ideas

- Page dédiée « lire le résultat » et « sauvegardes / export » → déjà prévu en phase 3 (SIMP-02, SIMP-03) ; noté en v2 (`DOC2-04`) comme pages séparées, hors roadmap actuel.
- Captures d'écran / illustrations du terminal → `DOC2-03`, hors roadmap.
- Génération d'un site statique depuis `docs/` (MkDocs/Sphinx) → `OUT2-01`, explicitement hors périmètre : la recherche recommande le Markdown nu.
- Vérificateur de liens **externes** → `OUT2-02`, hors roadmap ; cette phase ne contrôle que les liens internes.
- Intégration continue exécutant pytest à chaque changement → `OUT2-03`, hors roadmap (aucune plateforme distante autorisée).
- Guide de contribution et documentation d'architecture interne → hors périmètre du milestone (public « Utilisateur + dev », pas « Développeur »).

</deferred>

---

*Phase: 1-Socle documentaire, installation et harnais vérifiable*
*Context gathered: 2026-09-11*
