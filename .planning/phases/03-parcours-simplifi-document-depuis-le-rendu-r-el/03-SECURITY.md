---
phase: "3"
slug: "parcours-simplifi-document-depuis-le-rendu-r-el"
status: verified
# threats_open = count of OPEN threats at or above workflow.security_block_on severity (the blocking gate)
threats_open: 0
asvs_level: 1
created: "2026-09-11"
---

# Phase 3 — Security

> Per-phase security contract: threat register, accepted risks, and audit trail.
>
> **Surface réelle de cette phase** : des fichiers Markdown sous `docs/`, un module de test sous `tests/`, aucune dépendance ajoutée, aucun secret, aucun réseau, aucun serveur lancé. Les menaces de cette phase ne sont donc pas des menaces réseau : ce sont des menaces de **fausseté** (un document qui affirme sans mesure, un contrôle qui approuve sans rien prouver) et d'**effet de bord** (une écriture sous `.data/`, un navigateur lancé, une resynchronisation déclenchée).

---

## Trust Boundaries

| Boundary | Description | Data Crossing |
|----------|-------------|---------------|
| Page `docs/` ↔ code produit | La page affirme ce que le lecteur voit ; le code est la seule source de vérité | Libellés, messages d'erreur, valeurs numériques (non sensibles, mais faux silencieusement) |
| Module de test ↔ base locale `.data/dofus.sqlite3` | La fixture `app` **lit** la base ; aucun test ne doit écrire, ni la supprimer | Données de jeu (reconstructibles ; la valeur est le coût de resynchronisation, pas la confidentialité) |
| Module de test ↔ processus hôte | `webbrowser.open_new_tab`, `subprocess`, `socket`, réseau sont hors périmètre | Effets de bord système (ouverture de navigateur, accès réseau) |
| Harnais ↔ arbre produit `dofus_stuff/**` | Lecture seule stricte ; les batteries de morsure mutent une **copie** `mktemp -d` | Code produit (aucune donnée sensible) |
| Livraison ↔ dépôt distant | Aucune publication, aucun déploiement, aucun `git push` | Commits locaux uniquement |

---

## Threat Register

Registre construit depuis les blocs `<threat_model>` des quatre plans (T-1…T-21), croisé avec les sections `## Threat Flags` des quatre `SUMMARY.md` et re-mesuré par la vérification de phase. `register_authored_at_plan_time: true`.

| Threat ID | Category | Component | Severity | Disposition | Mitigation | Status |
|-----------|----------|-----------|----------|-------------|------------|--------|
| T-1 | Fausseté (Repudiation) | `tests/test_docs_parcours.py` | high | mitigate | Assertions limitées à `_lignes_du_corps` / `_statut` ; test dédié exigeant que le corps soit un sous-ensemble **strict** de la réponse — la charge utile `data-stuff-payload` porte tout le résultat sur chaque page (`screen.html:21`) | closed |
| T-2 | Fausseté (Tampering) | `docs/parcours-simplifie.md` | high | mitigate | Chaque entrée acceptée/refusée rejouée sur le rendu réel via le client Flask ; listes épinglées dérivées de la mesure, jamais écrites de mémoire | closed |
| T-3 | Élévation (EoP) | `.data/dofus.sqlite3` | high | mitigate | Garde `ast` sur les racines interdites **et** sur la clôture des imports produit ; `mtime_ns` + taille + SHA-256 comparés avant/après la **suite entière** — voir « Limites connues » L-1 | closed |
| T-4 | Fuite d'information | `docs/parcours-simplifie.md` | medium | mitigate | Aucun chemin absolu du développeur dans la page ; les chemins cités sont relatifs au dépôt et contrôlés **existants sur disque** | closed |
| T-5 | Fausseté (Repudiation) | `tests/test_docs_parcours.py` | medium | mitigate | Aucune introspection d'attribut privé hors le `patch` de court-circuit déjà employé par l'analog (`tests/test_recommend.py:75`) | closed |
| T-6 | Élévation (EoP) | environnement | low | accept | Aucune installation, aucune dépendance nouvelle ; risque accepté et documenté ici | closed |
| T-7 | Fausseté (Repudiation) | `tests/test_docs_parcours.py` | high | mitigate | Aucune valeur volatile épinglée (`Méthode`, score, total de pages) : la base réelle a rendu **deux méthodes** et **six puis sept** pages. Toute lecture passe par la fixture déterministe (charge utile identique par SHA-256 sur trois exécutions) ; la position des diagnostics est exigée par **ordre relatif** | closed |
| T-8 | Faux négatif (Repudiation) | `tests/test_docs_parcours.py` | high | mitigate | Interdiction explicite d'asserter sur `response.data` (accents échappés `\u00e9`) ; assertions limitées aux lignes du corps et à la ligne de statut | closed |
| T-9 | Fausseté (Tampering) | `docs/parcours-simplifie.md` | medium | mitigate | Chaque nom complet recopié de sa source **et** re-vérifié sur la ligne qui le porte (`dofusbook_export.py:27-36`, `solver_spec.py:53`) | closed |
| T-10 | Fausse garantie (Repudiation) | `docs/parcours-simplifie.md` | medium | mitigate | Ni « libellé tronqué » ni `…` dans la page ; le module n'asserte jamais l'apparition de points de suspension sur un rendu (mesure : aucune ligne rendue n'en porte) | closed |
| T-11 | Élévation (EoP) | `.data/dofus.sqlite3` | high | mitigate | Aucun test n'écrit ; `mtime_ns` et taille comparés après chaque tâche. Vérifié indépendamment : empreinte identique avant/après la suite entière | closed |
| T-12 | Effet de bord (EoP) | processus hôte | high | mitigate | Aucun POST `DB` dans le module (il appelle `webbrowser.open_new_tab` côté serveur) ; garde `ast` interdisant `webbrowser` et le POST littéral ; le comportement reste couvert, patché, par `tests/test_web.py:668` | closed |
| T-13 | Fausse garantie (Repudiation) | `docs/parcours-simplifie.md` | medium | mitigate | Le module ne revendique **pas** avoir exécuté le JavaScript : il contrôle des **littéraux** (`SAVES_KEY`, `MAX_SAVES`) et le dit dans son docstring et dans ses constats | closed |
| T-14 | Fausseté (Tampering) | export Dofusbook | medium | mitigate | Contrôle comportemental sur la surface publique pure (`build_dofusbook_url`, charge utile décodée) : `sum(counts) == 16` et identifiant de `prysma` absent des identifiants exportés | closed |
| T-15 | Fausseté (Tampering) | `docs/parcours-simplifie.md` | medium | mitigate | La valeur affichée est comparée à celle **extraite du JS** à chaque exécution : changer `MAX_SAVES` rougit | closed |
| T-16 | Élévation (EoP) | `.data/dofus.sqlite3` | high | mitigate | Aucun test n'écrit ; les rendus `/saves` et résultat n'écrivent rien ; empreinte comparée après la tâche | closed |
| T-17 | Destruction de données (Tampering) | `.data/dofus.sqlite3` | critical | mitigate | Interdiction explicite d'écrire dans la base pour démontrer une morsure : la démonstration se fait sur une **copie** dans `mktemp -d`. Aucune commande destructive employée (`db clear`, `drop`, suppression) | closed |
| T-18 | Faux vert (Repudiation) | `.data/dofus.sqlite3` | high | mitigate | Le rendu réel a lieu entre les deux empreintes de la mesure locale, et la mesure large entoure la **suite entière** ; une base absente produit un `skip` explicite, jamais un faux vert — voir « Limites connues » L-2 | closed |
| T-19 | Limite inventée (Repudiation) | `docs/parcours-simplifie.md` | medium | mitigate | Chaque limite est adossée à un fichier cité (`score.py`, `candidates.py`, `recommend.py:60`, `routes.py:1336`) ; ce qui n'était adossé à rien est retiré ou présenté comme une interprétation (D-41) | closed |
| T-20 | Valeurs volatiles (Tampering) | `docs/parcours-simplifie.md` | medium | mitigate | La section des limites n'accepte aucun nombre à trois chiffres ou plus (une seule exception nommée : la valeur de `COLS` extraite du code, qui est strippée du texte avant la recherche) | closed |
| T-21 | Dérive de format (Tampering) | `docs/parcours-simplifie.md` | low | mitigate | Contrôle de format (CRLF, UTF-8 sans BOM, neuf sections dans l'ordre, H1 unique, aucun bloc `console`, aucun lien externe) — voir « Limites connues » L-1 | closed |

*Status: open · closed · open — below high threshold (non-blocking)*
*Severity: critical > high > medium > low — only open threats at or above `workflow.security_block_on` (`high`) count toward `threats_open`*
*Disposition: mitigate (implementation required) · accept (documented risk) · transfer (third-party)*

Aucune menace n'est ouverte. `threats_open: 0`.

---

## Limites connues — portées explicitement, jamais masquées

Ces deux points ont été mesurés par la vérification de phase et par la revue de code. Ils ne créent **aucune menace ouverte** (la propriété visée est tenue, mesurée) mais la **force** d'un contrôle était surestimée ; elle est donc corrigée ici plutôt que laissée implicite.

**L-1 — La garde `ast` n'est pas la clôture d'exécution réelle (T-3, T-21).**
La garde vérifie statiquement la clôture des imports **produit** du module. Or importer `dofus_stuff.web.dofusbook_export` exécute `dofus_stuff/web/__init__.py`, ce qui charge `dofus_stuff.database` et `sqlite3` dans `sys.modules` **pendant que la garde reste verte**. Le risque nommé (ouvrir la base en écriture, processus, socket, réseau) **n'est pas réalisé** : l'empreinte de `.data/dofus.sqlite3` est identique avant/après la suite entière (`24989696` / `1788730056843137500` / SHA-256 `e3793d64…`), aucun serveur n'est lancé et aucun POST `DB` n'est émis. La preuve directe est donc la **mesure d'empreinte**, pas la garde ; la revendication de la garde dans les plans est ramenée à ce qu'elle vaut — un contrôle **statique et indirect**.

**L-2 — Le contrôle d'empreinte ne peut pas voir l'écriture d'un autre module (T-18).**
`tests/conftest.py` construit sa propre base sous `tmp_path/data` et passe `data_dir=tmp_path/"data"` à `create_app` : le test local mesure donc un fichier que rien d'autre ne touche, et un « avant == après » y est vrai par construction. La preuve directe est la mesure **au périmètre de la suite** (avant/après `pytest -q`), que la vérification a exécutée. Le test local a été renommé (`test_data_locale_non_modifiee_autour_des_rendus`) pour ne revendiquer que ce qu'il mesure.

**L-3 — L'assertion de fin de ligne mesure un artefact de l'arbre de travail (T-21).**
Le blob est stocké en LF et converti en CRLF au checkout (`core.autocrlf=true`, aucun `.gitattributes`) : sur une copie sans cette conversion, une page **correcte** rédigée en LF rougirait. La convention CRLF du projet est bien une décision verrouillée (D-45) et la page la respecte dans cet arbre, mais l'assertion n'est pas portable hors de cette configuration. Signalé à la revue de code (WR-01) ; non corrigé dans cette phase, car corriger reviendrait à modifier un contrôle que le plan prescrit explicitement — la décision revient au porteur du projet.

---

## Accepted Risks Log

| Risk ID | Threat Ref | Rationale | Accepted By | Date |
|---------|------------|-----------|-------------|------|
| AR-1 | T-6 | Aucune dépendance nouvelle, aucune installation : le projet reste exécutable avec l'environnement existant (`pytest`, `flask`, `ortools`, `msgpack`). Accepter plutôt qu'ajouter une dépendance de contrôle. | porteur du projet (règles du run) | 2026-09-11 |
| AR-2 | T-13 | Le comportement réel du JavaScript de sauvegarde (éviction au 21ᵉ enregistrement) n'est pas exécutable dans cet environnement : il est décrit depuis la source lue et contrôlé comme **littéraux**, limite écrite noir sur blanc dans la page et dans le module. | porteur du projet (règles du run) | 2026-09-11 |
| AR-3 | T-9 | L'équivalence « libellé technique ↔ mot affiché dans le jeu » reste une lecture de joueur, annoncée comme telle dans la page ; elle n'est pas prouvable depuis le dépôt. | porteur du projet (règles du run) | 2026-09-11 |
| AR-4 | T-19 | L'intérêt pratique de l'« indice de recherche » pour un joueur reste une interprétation, présentée comme telle (D-41). | porteur du projet (règles du run) | 2026-09-11 |
| AR-5 | T-21 / L-3 | L'assertion de fin de ligne n'est pas portable hors `core.autocrlf=true`. Accepté pour cette phase : la convention CRLF est une décision verrouillée (D-45) et le contrôle est conservé tel que le plan le prescrit. | porteur du projet (règles du run) | 2026-09-11 |

*Accepted risks do not resurface in future audit runs.*

---

## Security Audit Trail

| Audit Date | Threats Total | Closed | Open | Run By |
|------------|---------------|--------|------|--------|
| 2026-09-11 | 21 | 21 | 0 | orchestrateur GSD (registre des plans 03-01…03-04 + `## Threat Flags` des SUMMARY + `03-VERIFICATION.md` + `03-REVIEW.md`) |

### Évidences mesurées à l'appui de ce registre

- `./.venv/Scripts/python.exe -m pytest -q` → **186 passed** ; module de la phase → **17 passed**, aucun `skip`.
- `.data/dofus.sqlite3` → `24989696` octets / `mtime_ns 1788730056843137500` / SHA-256 `e3793d64cb7939ad…`, **identique avant et après la suite entière** (mesuré par la vérification de phase, indépendamment du module).
- Batterie de morsures de la vérification : **22 mutations sur copies jetables → 22/22 détectées**, constat attribué (page + section + valeur attendue + fichier de code), copie non mutée verte avant chaque mutation.
- Aucun fichier de `dofus_stuff/**`, `README.md`, `GUIDE_WIZARD.md` ni `.data/` modifié sur l'ensemble de la phase (`git status --porcelain` vide sur ces chemins ; aucun `--diff-filter=D`).
- Aucune resynchronisation Dofusdude, aucun accès réseau, aucune commande destructive, aucune publication, aucun déploiement, aucune dépendance ajoutée.

---

## Sign-Off

- [x] All threats have a disposition (mitigate / accept / transfer)
- [x] Accepted risks documented in Accepted Risks Log
- [x] `threats_open: 0` confirmed
- [x] `status: verified` set in frontmatter

**Approval:** verified 2026-09-11
