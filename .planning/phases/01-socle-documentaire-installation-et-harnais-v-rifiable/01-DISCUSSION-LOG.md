# Phase 1: Socle documentaire, installation et harnais vérifiable - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-09-11
**Phase:** 1-Socle documentaire, installation et harnais vérifiable
**Areas discussed:** Gabarit de page, Parcours & sommaire, Détail install, Tests : ancrage

---

## Gabarit de page

| Option | Description | Selected |
|--------|-------------|----------|
| Gabarit léger avec bloc « Source de vérité » | H1 + intro + sections courtes + chemins réels du code + retour au sommaire | ✓ |
| Page nue | Texte seul, sans bloc de provenance ni lien de retour | |
| Fiche produit avec métadonnées | Front-matter et en-tête structuré par page | |

**User's choice:** Gabarit léger, bloc « Source de vérité » obligatoire, encadrés d'erreur seulement là où l'erreur est réellement rencontrée.
**Notes:** Le bloc « Source de vérité » est ce qui rend l'ancrage vérifiable : chaque chemin `.py` cité doit exister.

---

## Parcours & sommaire

| Option | Description | Selected |
|--------|-------------|----------|
| Parcours guidé ordonné + index en fin de page | Ordre de lecture puis tableau thématique, un seul fichier | ✓ |
| Index thématique plat | Entrées classées par thème, sans ordre de lecture | |

**User's choice:** Parcours guidé ordonné (Installation → Parcours simplifié → Wizard avancé → CLI → Base locale → Dépannage → Glossaire) + index thématique sur la même page.

| Option | Description | Selected |
|--------|-------------|----------|
| Croît par phase (Recommandé) | Le sommaire ne liste que les pages livrées ; une entrée par phase ; liste épinglée en phase 6 | ✓ |
| Les 8 pages tout de suite | Le sommaire annonce les 8 pages dès la phase 1 | |

**User's choice:** Croît par phase.
**Notes:** Motif explicité — un sommaire annonçant des pages inexistantes serait une doc qui « a l'air juste » ; la liste épinglée des 8 pages arrive en phase 6, comme le recommande la recherche. Le contrôle d'exhaustivité bidirectionnelle reste vert sans exception.

---

## Détail install

| Option | Description | Selected |
|--------|-------------|----------|
| Chemin minimal + section « erreurs fréquentes » | Pas-à-pas court puis erreurs réellement rencontrées | ✓ |
| Référence complète pip/uv Windows/Linux | Tous les gestionnaires et systèmes documentés | |

**User's choice:** Chemin minimal d'abord + erreurs fréquentes.
**Notes:** Ni `uv` ni autre gestionnaire : `pyproject.toml` n'utilise que `setuptools`/`pip` — documenter un outil non utilisé serait inventer une procédure. Le pilotage clavier (champ de saisie, `F7`, `F8`, `ESC`, `PageUp`, `PageDown`) est décrit avant le lancement.

| Option | Description | Selected |
|--------|-------------|----------|
| Lien vers le sommaire (Recommandé) | Section « Documentation utilisateur » → un seul lien vers `docs/sommaire.md` | ✓ |
| Sommaire + liens directs | Liens directs vers chaque page en plus du sommaire | |

**User's choice:** Lien unique vers le sommaire.
**Notes:** Motif explicité — une seule source par énoncé ; la duplication README + sommaire reproduirait le mode de défaillance mesuré sur `GUIDE_WIZARD.md`. La redirection actuelle vers `GUIDE_WIZARD.md` (ligne 59) est traitée totalement en phase 4.

---

## Tests : ancrage

| Option | Description | Selected |
|--------|-------------|----------|
| Comparaison normalisée + helpers dans `tests/conftest.py` | Accents/casse/espaces/CRLF/HTML neutralisés ; helpers dans le conftest existant | ✓ |
| Comparaison littérale + module d'aide dédié | Correspondance exacte des chaînes, helpers dans un nouveau module | |

**User's choice:** Comparaison normalisée, helpers dans le `conftest.py` existant, messages d'échec localisants (page + libellé attendu + fichier de code), pas d'API privée `argparse`, aucune introspection.
**Notes:** La normalisation est un choix assumé avec son risque : elle ne doit pas devenir un test affaibli « parce qu'il est trop fragile » — d'où l'exigence que chaque échec dise où est la divergence. Verdict : cette décision est marquée coûteuse à défaire, car les phases 2 à 6 s'appuient dessus.

---

## Claude's Discretion

- Noms des fixtures et helpers dans `tests/conftest.py` (le comportement de normalisation reste testé).
- Découpage interne de `tests/test_docs_structure.py` (classes ou fonctions).
- Formulation exacte du parcours guidé et de l'index dans `docs/sommaire.md`.
- Libellé et forme du lien de retour au sommaire sur chaque page.

## Deferred Ideas

- Pages séparées « lire le résultat » / « sauvegardes & export » → `DOC2-04`, hors roadmap.
- Captures d'écran du terminal → `DOC2-03`.
- Site statique MkDocs/Sphinx → `OUT2-01`, explicitement rejeté pour ce milestone.
- Vérificateur de liens externes → `OUT2-02`.
- Intégration continue → `OUT2-03` (aucune plateforme distante autorisée).
- Guide de contribution / doc d'architecture interne → hors périmètre du milestone.
