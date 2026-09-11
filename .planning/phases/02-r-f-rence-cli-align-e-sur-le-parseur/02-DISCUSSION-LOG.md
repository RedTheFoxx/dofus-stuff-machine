# Phase 2: Référence CLI alignée sur le parseur - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-09-11
**Phase:** 2-référence-cli-alignée-sur-le-parseur
**Areas discussed:** Profondeur & structure par sous-commande, Surface des options d'optimize, Alias `cache` et commandes destructrices, Ancrage des exemples et limite du contrôle

---

## Amont : fallait-il discuter avant de planifier ?

| Option | Description | Selected |
|--------|-------------|----------|
| Continue without context | Planifier depuis le ROADMAP + REQUIREMENTS seuls (plus rapide) | |
| Run discuss-phase first | Verrouiller les décisions de rédaction avant planification | ✓ |

**User's choice:** Run discuss-phase first.
**Notes:** Justifié par la cohérence avec les choix déjà actés (recherche d'abord, plan-check activé, verifier activé, zone « Tests : ancrage » ouverte) et par le risque central du projet — la désynchronisation doc/code, défaut mesuré sur `GUIDE_WIZARD.md`. Les points non tranchés par le ROADMAP (structure de page, alias `cache`, formulation de l'avertissement destructif, niveau d'ancrage des exemples) sont précisément ceux qui dérivent silencieusement. Décisions dérivables des acquis de la phase 1, pas inventables.

---

## Profondeur & structure par sous-commande

| Option | Description | Selected |
|--------|-------------|----------|
| Une section par sous-commande + table récapitulative en fin de page | Synthèse unique en plus des sections | |
| Une section par sous-commande, dans l'ordre du parseur, sans table | Synopsis + options/défauts + un exemple par sous-commande | ✓ |

**User's choice:** Une section par sous-commande, dans l'ordre réel du parseur, sans table récapitulative.
**Notes:** Une table unique dupliquerait le parseur et deviendrait un second référentiel à maintenir — même raison que le lien unique `README.md` → `docs/sommaire.md` (D-10). La source de vérité est le parseur. → D-16, D-17.

---

## Surface des options d'optimize

| Option | Description | Selected |
|--------|-------------|----------|
| Documenter un sous-ensemble suffisant | Plus court, risque de page peu utile | |
| Documenter toutes les options, tables groupées par thème, défauts réels | Page réellement utile au public utilisateur + dev | ✓ |
| Documenter toutes les options dans une seule table plate | Complet mais peu lisible (~30 options) | |

**User's choice:** Toutes les options documentées, en tables groupées par thème, avec les défauts réels lus dans le code.
**Notes:** Le critère 2 du ROADMAP n'exige que « chaque option documentée » soit acceptée par le parseur — il n'oblige pas à tout documenter ; la complétude retenue vient de l'utilité. Aucune sémantique inventée : une option dont le sens n'est pas lisible dans le code est décrite par son synopsis et son défaut seulement. → D-18 (Reversibility: costly), D-19.

---

## Alias `cache` et commandes destructrices

| Option | Description | Selected |
|--------|-------------|----------|
| Décrire `cache` en dupliquant la description de `db` | Autonome mais crée deux référentiels | |
| `cache` déclaré comme alias renvoyant à `db`, lien prouvé par le parseur | Une seule description ; sous-commandes masquées signalées comme telles | ✓ |
| `db clear` dans un parcours d'usage | Simple mais présente une commande destructrice comme une étape | |
| `db clear` hors parcours, avertissement destructif sur la même ligne | Co-présence exigible par test | ✓ |

**User's choice:** `cache` déclaré comme alias, lien prouvé par équivalence d'espace de noms via le parseur public ; `db clear` mentionné hors parcours avec l'avertissement destructif sur la même ligne.
**Notes:** Le nom exact du drapeau de `db clear` sera lu dans le parseur au moment de rédiger, pas inventé. La liste des commandes destructrices est dérivée du code, pas supposée. Aucun `db clear` n'est exécuté, à aucun moment. Les sous-commandes masquées du help (`stats`, `fill`, `argparse.SUPPRESS`) sont signalées comme telles. → D-20, D-21, D-22, D-23.

---

## Ancrage des exemples et limite du contrôle

| Option | Description | Selected |
|--------|-------------|----------|
| Toute ligne de commande de la page compte comme exemple (blocs + prose) | Couverture maximale, contrôle fragile | |
| Seules les lignes de blocs de code balisés comptent comme exemple | Détection non ambiguë par test | ✓ |
| Exhaustivité prouvée dans les deux sens pour toute la surface CLI | Garantie maximale, mais bloque toute évolution du parseur | |
| Contrôle page → parseur + liste explicite, limite écrite dans le test | Honnête sur ce qui n'est pas garanti | ✓ |

**User's choice:** Seuls les blocs de code balisés comptent comme exemples ; vérification verbatim + `shlex.split` → `build_parser().parse_args` ; limite consignée dans le test lui-même.
**Notes:** Une sous-commande ou option ajoutée plus tard au parseur et non documentée ne fera pas échouer la suite — aucune exhaustivité totale n'est revendiquée. Parseur public uniquement, jamais d'API privée `argparse`. → D-24, D-25, D-26, D-27.

---

## Claude's Discretion

- Découpage exact des groupes thématiques des tables d'`optimize` (principe fixé, nombre de groupes libre).
- Forme du marqueur identifiant une ligne comme « exemple », tant qu'il reste détectable sans ambiguïté.
- Formulation du synopsis de chaque sous-commande et de la phrase d'introduction de la page.
- Ordre des groupes à l'intérieur des tables, dès lors que les options et leurs défauts sont exacts.
- Découpage interne des nouveaux tests (module dédié ou extension d'un module existant), sans dupliquer les helpers de `tests/conftest.py`.

## Deferred Ideas

- Table récapitulative unique de toute la surface CLI — écartée : second référentiel à maintenir.
- Documenter une sémantique non lisible dans le code — hors périmètre d'une référence.
- Complétude prouvée dans les deux sens pour toute la surface CLI — non retenue : bloquerait toute évolution du parseur.
- Dépannage par message d'erreur, glossaire, liste épinglée des 8 pages — phases 5 et 6.
- Parcours simplifié du rendu réel — phase 3.
