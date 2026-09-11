---
phase: "3"
slug: "parcours-simplifi-document-depuis-le-rendu-r-el"
status: open
kind: review-fix
source: plan-checker iteration 2 (0 blocker, 0 warning, 7 info)
blocker: 0
warning: 0
info: 7
created: "2026-09-11"
---

# 03 — REVIEW-FIX (advisories du plan-checker, itération 2)

Le plan-checker iteration 2 a rendu **VERIFICATION PASSED** : `0 blocker`, `0 warning`, `7 info`.
Les deux blockers et les quatre warnings de l'itération 1 sont **resolved**, chacun re-mesuré
indépendamment (le checker a rejoué la route réelle : 12/12 entrées acceptées, 9/9 refus,
`AVANCE` → `/optimize/wizard/recap`). **Aucune révision n'est requise.**

Ce fichier n'est pas une porte : il consigne les sept advisories pour qu'elles ne soient pas perdues.
Deux d'entre elles ont été corrigées immédiatement (texte seulement, aucun contenu de tâche touché) —
voir « Déjà traité ». Les cinq autres sont des cibles d'hygiène à traiter pendant l'exécution ou à
assumer comme hors périmètre, avec la raison écrite.

## Déjà traité (texte seulement — aucune tâche, aucun `<verify>`, aucun `must_haves` modifié)

| # | Advisory | Action |
|---|----------|--------|
| 1 | `03-01-PLAN.md` — fragment final dupliqué | Clause en trop retirée ; la phrase se termine maintenant sur « …seraient alors faux sur une implémentation correcte. » |
| 2 | `03-01-PLAN.md` — ligne de couverture `SIMP-02` portant aussi la correspondance `SIMP-03` | Ligne ramenée à `03-02 \`requirements\` (SIMP-02)` ; la ligne `SIMP-03` correcte existait déjà |

## À traiter pendant l'exécution

### RF-1 — `\d{3,}` : exempter la phrase qui cite `COLS`, pas toute occurrence de sa valeur
- **Plan :** 03-04, tâche 2
- **Property :** l'exception nommée à l'interdiction `\d{3,}` n'exempte pas un autre numéro.
- **État actuel :** le contrôle retire du texte **toutes** les occurrences en mot entier de la valeur
  extraite de `dofus_stuff/web/screens.py:5` (`COLS = 100`), puis cherche `\d{3,}`. Un autre nombre à
  trois chiffres (`1219`, `1000`) est bien attrapé — la retombée est bornée à un nombre **égal à la
  valeur extraite** dans cette seule section.
- **Résiduel assumé :** si `COLS` prenait un jour une valeur apparaissant légitimement dans la prose de
  la section, une page correcte pourrait rougir. La mesure suit le code, donc le contrôle resterait
  *juste* mais deviendrait *fragile*.
- **Cible :** exempter la **phrase** qui cite `COLS` (ou annoter l'occurrence admise) au lieu de toute
  occurrence de la valeur. Si l'exécution choisit de garder la forme actuelle, l'écrire dans le message
  de contrôle et dans la truth concernée.

### RF-2 — `OPT-SIMPLE` / « RECOMMANDATION DE STUFF » : citer l'en-tête rendu ou enregistrer l'omission
- **Portée :** phase entière (plan le plus proche : 03-01)
- **Property :** tout ce que `.claude/CLAUDE.md` prescrit pour `docs/parcours-simplifie.md` est porté
  par la page **et** un contrôle, ou son omission est enregistrée.
- **Mesure :** `0` occurrence de `OPT-SIMPLE`, `RECOMMANDATION DE STUFF` et `.claude/CLAUDE.md` dans les
  quatre plans ; l'extracteur d'en-tête `_entete` n'est introduit qu'en 03-03 T1 et n'est utilisé que
  pour `SAV-01`. L'en-tête est bien rendu (`PGM: OPT-SIMPLE … ** RECOMMANDATION DE STUFF ** …`).
- **Atténuation :** ni `PROJECT.md` DOCS-04 (« le flux … est décrit tel qu'il existe réellement dans le
  code ») ni les critères 1–5 du ROADMAP ne nomment ces identifiants, et les plans montrent bien les
  trois corps rendus.
- **Cible :** soit la page cite l'en-tête rendu des trois écrans de questions et le contrôle l'asserte
  via `_entete`, soit l'omission est **enregistrée** (même traitement que l'écart DOCS-06, déjà en
  `WINDOWS.md` entrée 2). Ne pas laisser l'omission implicite.

## À assumer comme hors périmètre (avec raison écrite)

### RF-3 — `03-RESEARCH.md` : `## Open Questions` sans marqueur `(RESOLVED)`
Les quatre questions portent une « Recommandation » et **chacune est implémentée** par les plans
(ÉCR-1 → ROADMAP + `WINDOWS.md` entrée 5 + 03-02 ; assertion positionnelle → 03-02 T1 (ÉCR-2,
`WINDOWS.md` entrée 6) ; phrase « omis quand vide » → 03-02 T2 ; `DB DOFUSBOOK` sur les deux écrans →
03-03 T1/T2). Rien n'est substantiellement ouvert ; c'est le **marqueur** qui manque. Aucun exécuteur ne
peut être induit en contradiction. Corriger coûte une ligne, mais touche un artefact déjà vérifié.

### RF-4 — `03-VALIDATION.md` : les durées de la porte de validation ne sont pas reproductibles
`03-VALIDATION.md` cite ~2,6 s pour 169 tests et un budget « < 5 s » ; le checker a mesuré **4,73 s**
sur cette machine pour la même base, et le module de la phase ajoute deux vrais appels au solveur (03-02
T1 et 03-04 T3). **Aucun contrôle n'assoit ces chiffres.** La cible est de les exprimer comme
**cibles avec provenance de mesure**, ou de cesser de s'appuyer sur la case de latence. Ne pas réécrire
le chiffre pour qu'il « passe » : le remplacer par une fourchette mesurée.

### RF-5 — `03-PATTERNS.md:629` : l'exemple d'allow-list du garde est devenu faux
`PATTERNS.md` suggérait encore une allow-list dont l'exemple contient `dofus_stuff.web` ; mesure faite :
la fermeture transitive de `dofus_stuff.web` **contient `dofus_stuff.database`**, donc implémenter cet
exemple littéralement serait rouge sous le garde révisé. Le plan est cohérent et explique sa divergence
volontaire ; l'exécuteur lit le plan, pas PATTERNS. Cible : aligner la note de PATTERNS sur la forme
« par risque » pour que les deux artefacts concordent.

### RF-6 — `.gsd-tmp/` : la mitigation de l'hypothèse A1 n'a pas de mécanisme
03-01 `must_haves.assumptions` A1 écarte — à juste titre — la « suppression des sondes » de RESEARCH A1
(le projet interdit la suppression) et la remplace par « ne rien indexer sous `.gsd-tmp/` ». Mesure :
`git check-ignore -v .gsd-tmp/` est vide, `.gitignore` n'a gagné que `.gsd-auto/`, et aucun plan ne
liste `.gitignore` dans `files_modified`. **Aucune suppression n'est faite, c'est bien le point
essentiel.** Cible : soit ajouter une ligne d'ignore non destructive pour `.gsd-tmp/`, soit écrire que
l'hygiène d'index est hors périmètre de cette phase. La règle « jamais `git add .` ni `git add -A` »
rend le risque concret faible, mais la mitigation doit être vraie.

## Non négociable

Aucun de ces points n'autorise : une écriture ou une suppression sous `.data/`, une resynchronisation
Dofusdude, une exécution de `main()`, la modification d'un chemin `dofus_stuff/**`, une nouvelle
dépendance, une publication ou un déploiement distant. La suite doit rester verte
(`169 passed` à la base) et l'empreinte de `.data/dofus.sqlite3` identique.

**Approval:** pending
