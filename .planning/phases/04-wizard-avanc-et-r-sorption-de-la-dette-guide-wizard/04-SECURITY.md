---
phase: "4"
slug: "wizard-avanc-et-r-sorption-de-la-dette-guide-wizard"
status: verified
# threats_open = count of OPEN threats at or above workflow.security_block_on severity (the blocking gate)
threats_open: 0
asvs_level: 1
created: "2026-09-11"
---

# Phase 4 — Security

> Per-phase security contract: threat register, accepted risks, and audit trail.
>
> **Surface réelle de cette phase** : deux pages Markdown dans `docs/`, un aiguillage à la racine, un module de test, une fixture Markdown et le client de test Flask **en processus**. Aucune dépendance ajoutée, aucun secret, aucun réseau, aucun serveur lancé, aucun fichier de `dofus_stuff/**` modifié. Les menaces de cette phase ne sont donc pas des menaces réseau : ce sont des menaces de **fausseté** (un document qui affirme ce que le rendu ne dit plus) et d'**effet de bord de harnais** (un test qui exécute le produit, le solveur, ou écrit dans la base locale).

---

## Trust Boundaries

| Boundary | Description | Data Crossing |
|----------|-------------|---------------|
| Page `docs/` et aiguillage racine ↔ code produit | Le document affirme ce que le lecteur voit ; le rendu est la seule source de vérité | Libellés de menus, de touches et de filtres (non sensibles, mais faux silencieusement) |
| Module de test ↔ base locale `.data/dofus.sqlite3` | La fixture `app` construit sa **propre** base sous `tmp_path` ; aucune écriture, aucune suppression, aucune resynchronisation | Données de jeu (reconstructibles ; le coût est la resynchronisation, pas la confidentialité) |
| Harnais ↔ processus hôte et solveur | `main()`, `subprocess`, `socket`, réseau et le POST `GO` (qui **lance le solveur**) sont hors périmètre | Effets de bord système et calcul |
| Harnais ↔ arbre produit `dofus_stuff/**` | Lecture seule stricte ; les batteries de morsure mutent une **copie** hors dépôt ou en mémoire | Code produit (aucune donnée sensible) |
| Livraison ↔ dépôt distant | Aucune publication, aucun `git push` : `origin/main` reste figé à `1d475f9` pendant que la branche locale avance | Commits locaux uniquement |

---

## Threat Register

Registre construit depuis les blocs `<threat_model>` des quatre plans (T-04-01…T-04-SC), croisé avec les sections `## Threat Flags` des `SUMMARY.md`, puis re-mesuré par la vérification de phase et la revue de code. `register_authored_at_plan_time: true`.

| Threat ID | Category | Component | Severity | Disposition | Mitigation | Status |
|-----------|----------|-----------|----------|-------------|------------|--------|
| T-04-01 | Fausseté (Spoofing documentaire) | `docs/wizard-avance.md` : titres d'étapes, slots, filtres, options, formats, syntaxe d'items | high | mitigate | Chaque libellé cité est lu au rendu (client Flask en processus) ou dans une constante publique ; morsures du plan prouvant que la page rougit quand le code change. La vérification a re-dérivé la mesure indépendamment (mutations sur copie hors dépôt) | closed |
| T-04-02 | Falsification (Tampering) | `.data/dofus.sqlite3` | medium | mitigate | La fixture `app` construit sa base sous `tmp_path/data` ; empreinte `taille:mtime_ns:SHA-256` mesurée avant/après la suite entière — identique. Voir L‑2 | closed |
| T-04-03 | Élévation de privilège (EoP) | Le harnais : exécution du produit ou du solveur | high | mitigate | Garde `ast` sur le module d'ancrage (racines interdites, `MODULE_BASE_INTERDIT`, `APPEL_PRODUIT`, refus d'un appel dont l'argument `data` porte la paire `"cmd": "GO"`) ; aucun `GO` posté par le harnais committé. **Portée limitée, mesurée : voir L‑1** | closed |
| T-04-04 | Divulgation d'information | Liens et chemins cités par la page | low | mitigate | Aucun lien externe dans les pages livrées (mesure) ; le contrôle exige que chaque chemin entre accents graves existe depuis la racine du dépôt | closed |
| T-04-05 | Répudiation | Traçabilité des décisions et des morsures | low | mitigate | Les constats citent la page, la valeur fautive, la valeur attendue lue au rendu et le fichier de code producteur ; chaque plan consigne ses morsures dans son `SUMMARY.md` | closed |
| T-04-SC | Falsification (Tampering) | Installations de paquets | low | accept | Aucune dépendance ajoutée : `pyproject.toml` **inchangé** sur toute la phase (mesure). Risque accepté et documenté ici (AR‑1) | closed |

*Status: open · closed · open — below high threshold (non-blocking)*
*Severity: critical > high > medium > low — only open threats at or above `workflow.security_block_on` (`high`) count toward `threats_open`*
*Disposition: mitigate (implementation required) · accept (documented risk) · transfer (third-party)*

Aucune menace n'est ouverte. `threats_open: 0`.

---

## Limites connues — portées explicitement, jamais masquées

Ces points ont été mesurés par la revue de code et par la vérification de phase. Aucun ne crée de **menace ouverte** (la propriété visée est tenue et mesurée), mais chacun borne la **force réelle** d'un contrôle : ils sont donc écrits ici plutôt que laissés implicites.

**L-1 — La garde `ast` ne contraint que le harnais committé, pas un script hors dépôt (T-04-03).**
La garde interdit statiquement l'appel produit portant la paire `"cmd": "GO"`. La vérification de phase a néanmoins observé qu'une **sonde hors dépôt** postant `cmd=go` (minuscules) est acceptée par le produit comme `GO`, donc le solveur a tourné. Le fait est consigné tel quel : **aucun effet de bord n'a eu lieu** — exécution en processus, hors ligne, sur la base temporaire du harnais, sans écriture sous `.data/`, sans réseau, sans `main()`. La preuve directe reste la mesure d'empreinte (identique avant/après la suite entière), pas la garde. Portée corrigée : la garde protège le **module du dépôt** ; elle ne se revendique pas comme une clôture d'exécution du produit.

**L-2 — La mesure d'empreinte locale est vraie par construction, et un `skip` est explicite (T-04-02).**
`tests/conftest.py` construit sa base sous `tmp_path/data`, donc le test local mesure un fichier que rien d'autre ne touche. La preuve directe est la mesure **au périmètre de la suite** (avant/après `pytest -q`), que cet orchestrateur a exécutée plusieurs fois. Sur une copie sans base, le test d'empreinte saute en nommant la raison, jamais en faux vert.

**L-3 — Le détecteur de renvois obsolètes tolère volontairement les libellés abrégés (T-04-01).**
Le prédicat (a) du détecteur utilise une règle d'**appartenance de mots** : c'est une décision verrouillée (D-47) pour que l'aiguillage corrigé ne soit pas déclaré fautif par ses formes abrégées. Cette tolérance a un coût mesuré : c'est **exactement** ce qui a laissé passer le constat CR-01 (`3. PANOPLIES` / `4. OPTIMISATION` dans un bloc présenté comme « l'arborescence réelle ») sous une suite verte. Le prédicat n'a **pas** été resserré (le resserrer casserait l'état corrigé) ; un contrôle **distinct** d'égalité exacte entre chaque ligne `N. LIBELLE` et le libellé rendu a été ajouté, avec sa morsure. La règle d'appartenance reste donc non stricte **par conception** — la couverture déclarée demeure celle des trois formes nommées, sans revendication d'exhaustivité.

**L-4 — Deux réserves d'exactitude du livrable restent ouvertes, nommées et non masquées (T-04-01).**
La revue de code a relevé deux défauts d'exactitude réels dans `docs/wizard-avance.md` (hors du périmètre autorisé de la passe de clôture, qui ne portait que sur les deux constats critiques) : **WR-01** la règle des refus de l'écran `slots` est plus générale que le rendu (mesure : `0`/`12`/`13` rendent `SLOT INVALIDE`, message que la page ne cite pas) et **WR-05** le fait `POIDS : (aucun — defaut INT)` rendu par le récapitulatif n'est atteignable par aucune page. Aucun des cinq critères de succès de la phase n'en dépend (ils ne portent pas sur cette énumération), donc ils ne sont pas des menaces ouvertes ; ils sont **dus** et rattachés à la phase 6 (dépannage, complétude, preuve finale) qui en est le propriétaire naturel. Remèdes nommés par la revue : trois puces bornées et deux saisies à poster (WR-01) ; une phrase adossée au rendu (WR-05).

**L-5 — Les assertions de fin de ligne dépendent de `core.autocrlf` (format).**
Blobs stockés en LF et convertis en CRLF au checkout : sur un clone sans cette conversion, une page correcte rédigée en LF rougirait. La convention CRLF est une décision verrouillée et les quatre fichiers édités la respectent dans cet arbre (mesure : 18/18, 269/269, 2721/2721, 2990/2990 lignes en CRLF, UTF-8 sans BOM). Non corrigé : corriger reviendrait à modifier un contrôle prescrit par le plan. Reportée depuis la phase 3 (AR‑5) ; signalée à la revue comme WR‑02.

---

## Accepted Risks Log

| Risk ID | Threat Ref | Rationale | Accepted By | Date |
|---------|------------|-----------|-------------|------|
| AR-1 | T-04-SC | Aucune dépendance nouvelle, aucune installation : `pyproject.toml` est inchangé sur toute la phase. Accepter plutôt qu'ajouter une dépendance de contrôle. | porteur du projet (règles du run) | 2026-09-11 |
| AR-2 | T-04-03 / L-1 | La garde `ast` ne peut pas contraindre un script hors dépôt ; la revendication a été ramenée à la portée réelle (le harnais committé). Le risque nommé (exécuter le solveur, ouvrir la base en écriture) ne s'est pas réalisé : empreinte `.data/dofus.sqlite3` identique avant/après la suite entière. | porteur du projet (règles du run) | 2026-09-11 |
| AR-3 | T-04-01 / L-3 | La règle d'appartenance de mots du détecteur est volontairement non stricte (D-47). Compensée par un contrôle d'égalité distinct ajouté dans cette phase ; l'exhaustivité n'est pas revendiquée et la limite est écrite dans le module. | porteur du projet (règles du run) | 2026-09-11 |
| AR-4 | T-04-01 / L-4 | WR-01 et WR-05 sont deux inexactitudes réelles du livrable qui ne portent sur aucun critère de succès de la phase 4 ; elles sont dues et rattachées à la phase 6, propriétaire naturel de la complétude. | porteur du projet (règles du run) | 2026-09-11 |
| AR-5 | format / L-5 | L'assertion de fin de ligne n'est pas portable hors `core.autocrlf=true`. Report de la phase 3 (AR-5) : la convention CRLF est verrouillée et le contrôle est conservé tel que le plan le prescrit. | porteur du projet (règles du run) | 2026-09-11 |

*Accepted risks do not resurface in future audit runs.*

---

## Security Audit Trail

| Audit Date | Threats Total | Closed | Open | Run By |
|------------|---------------|--------|------|--------|
| 2026-09-11 | 6 | 6 | 0 | orchestrateur GSD (registre des plans 04-01…04-04 + `## Threat Flags` des SUMMARY + `04-VERIFICATION.md` + `04-REVIEW.md` + `04-GAP-SUMMARY.md`) |

### Évidences mesurées à l'appui de ce registre

- `./.venv/Scripts/python.exe -m pytest -q` → **205 passed**, `0 failed`, `0 skipped` (suite de référence à la clôture de la phase, exécutée par l'orchestrateur).
- Vérification de phase : **19/19 must-haves** vérifiés, score `passed`, aucune vérification humaine requise.
- Critère 5 re-dérivé **indépendamment** par la vérification sur copies extraites hors dépôt : rouge `1 failed, 198 passed, 2 skipped` avec l'unique échec nommé `test_aiguillage_sans_renvoi_obsolete` portant les trois formes, puis vert `205 passed`. Le détecteur appliqué à l'état antérieur rend **8 constats**, contre **0** sur le fichier livré.
- `.data/dofus.sqlite3` → `24989696` octets / `mtime_ns 1788730056843137500` / SHA-256 `e3793d64cb79…`, **identique avant et après** la suite entière, mesuré par l'orchestrateur à plusieurs reprises.
- Revue de code : 2 constats critiques, 5 avertissements, 4 informations ; les deux critiques (**CR-01**, **CR-02**) ont été **clos** dans la phase par une passe de clôture dédiée, avec morsures re-mesurées par la vérification (6/6 sur les mutations d'arborescence ; 2/1/0 sur l'ancre des touches).
- Aucun fichier de `dofus_stuff/**` ni `pyproject.toml` modifié sur toute la phase (`git diff --stat` vide) ; aucun lien externe et aucune commande destructrice dans les pages livrées ; `origin/main` reste figé à `1d475f9` (publication exclue par les règles du run).
- Aucune resynchronisation Dofusdude, aucun accès réseau, aucune commande destructive (`db clear` jamais exécuté, aucune suppression sous `.data/`), aucune publication, aucun déploiement.

---

## Sign-Off

- [x] All threats have a disposition (mitigate / accept / transfer)
- [x] Accepted risks documented in Accepted Risks Log
- [x] `threats_open: 0` confirmed
- [x] `status: verified` set in frontmatter

**Approval:** verified 2026-09-11
