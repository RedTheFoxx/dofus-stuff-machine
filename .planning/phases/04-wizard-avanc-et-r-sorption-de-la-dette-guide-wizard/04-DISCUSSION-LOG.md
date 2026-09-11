# Phase 4: Wizard avancé et résorption de la dette `GUIDE_WIZARD` - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-09-11
**Phase:** 4-wizard-avanc-et-r-sorption-de-la-dette-guide-wizard
**Areas discussed:** Périmètre de l'aiguillage, Découpage de `docs/wizard-avance.md`, Preuve rouge du critère 5, Redirection de `README.md`

---

## Porte d'entrée — contexte de phase manquant

| Option | Description | Selected |
|--------|-------------|----------|
| Run discuss-phase first | Capturer les décisions de conception avant la planification — mode employé par les phases 1 à 3, dont les `CONTEXT.md` portent les décisions verrouillées (`D-01`…`D-45`) que le planificateur traite comme non négociables | ✓ |
| Continue without context | Planifier à partir de la recherche et des exigences seules ; aucun arbitrage verrouillé sur la source unique, le périmètre de `GUIDE_WIZARD.md` et la forme du contrôle rouge-puis-vert | |

**User's choice:** Run discuss-phase first
**Notes:** Écarté pour rupture de fil : les phases 1 à 3 se sont toutes appuyées sur un `CONTEXT.md` verrouillé, et la phase 2 avait déjà retenu « Run discuss-phase first » face au même cas. La phase 4 est la plus design-heavy du projet (source unique, périmètre de l'aiguillage, forme du contrôle à deux états).

---

## Zones ouvertes à la discussion

| Option | Description | Selected |
|--------|-------------|----------|
| Périmètre de l'aiguillage | Que garde `GUIDE_WIZARD.md` : titre + avis de migration + arborescence corrigée + lien (~15 lignes), ou aussi des sections (ex. « Lire le résultat », l'exemple guidé) ? | ✓ |
| Découpage de `docs/wizard-avance.md` | Une section par étape (9 écrans, ordre du code) ou sections groupées par thème ? Place du chemin d'arrivée réel, des formats d'édition, de la syntaxe d'items, des touches ? | ✓ |
| Preuve rouge du critère 5 | Comment le rouge est réellement observé sur l'état antérieur : ordre TDD (preuve transitoire), copie figée signalée par le même détecteur (preuve durable), ou les deux ? | ✓ |
| Redirection de `README.md` | Ligne 63 : supprimée, cible remplacée par `docs/sommaire.md`, ou renvoi en prose sans lien ? | ✓ |

**User's choice:** les quatre zones sélectionnées.
**Notes:** Les quatre correspondent aux livrables réels du ROADMAP et aux deux critiques : désynchronisation doc/code, et preuve à deux états.

---

## Périmètre de l'aiguillage

| Option | Description | Selected |
|--------|-------------|----------|
| Les deux liens | L'aiguillage porte le lien vers `docs/wizard-avance.md` **et** celui vers `docs/sommaire.md` ; `GUIDE_WIZARD.md` étant à la racine, le lecteur qui y tombe garde un chemin vers le reste de la doc | ✓ |
| Source unique seulement | Uniquement vers `docs/wizard-avance.md` ; un seul lien à vérifier dans l'aiguillage | |

**User's choice:** Les deux liens
**Notes:** D-17 interdit de **décrire** deux fois le wizard, pas de le **référencer** deux fois : un aiguillage ne porte aucun énoncé de contenu. D-10/D-29 ne sont pas contredits — ces règles encadrent le lien du `README.md` vers le sommaire, et les deux liens de l'aiguillage mènent au même ensemble documentaire. Le coût de vérification reste d'un lien, pas d'un mécanisme. Bornes : aiguillage court (~15 lignes), sans « Lire le résultat », sans exemple guidé, sans table des touches ; arborescence lue dans le code.

---

## Découpage de `docs/wizard-avance.md`

| Option | Description | Selected |
|--------|-------------|----------|
| Web seulement | Les 9 étapes vivent dans `dofus_stuff/web/optimize_wizard.py` et sont rendues par l'app Flask ; libellés, titres et touches dérivés du client de test Flask, comme D-32 en phase 3 | ✓ |
| Web + parcours CLI | Le rendu web reste la référence et une section décrit en plus le parcours CLI (`AVANCE`, `EDIT`) ; risque : la surface de commandes appartient à `docs/cli.md` (D-37) et aucune correspondance de wizard n'existe dans `cli.py` / `fetcher.py` | |

**User's choice:** Web seulement
**Notes:** La recherche de `avance|wizard` dans `dofus_stuff/cli.py` et `fetcher.py` ne renvoie **aucune correspondance** : l'option CLI décrirait une surface qui n'existe pas — exactement le travers à corriger. Une seule source de rendu, un seul type de contrôle, donc un contrôle qui garde son sens. Contenu attribué : chemin d'arrivée (menu `4` → `optimize_entry` → `optimize_quick` → `AVANCE`), les 9 étapes de `WIZARD_STEPS` avec les titres de `STEP_TITLES`, formats d'édition des 4 nombres, syntaxe d'items, touches `GO`/`RESET`/`SAVES`/`1`–`8`, filtres `F1`–`F10` adossés à `TYPE_FILTER_KEYS`/`TYPE_FILTER_LABELS`, renvoi par lien vers « lire le résultat » / « sauvegarder et exporter ».

---

## Exemple guidé (§ 8 de `GUIDE_WIZARD.md`)

| Option | Description | Selected |
|--------|-------------|----------|
| Migrer l'exemple guidé | La section « Premier stuff en 5 minutes » (avec sa variante cible PA) est reprise dans `docs/wizard-avance.md` | ✓ |
| Ne pas le reprendre | La page se limite à la description des écrans, formats et touches | |

**User's choice:** Migrer l'exemple guidé
**Notes:** « Migrer, pas réinventer » est le principe même de la décision prise pour `GUIDE_WIZARD.md` ; le § 8 est la seule partie du fichier qui n'existe nulle part ailleurs. Conditions fixées : réancrage obligatoire au rendu réel, passage par le chemin d'arrivée réel (pas d'entrée directe dans le wizard), la variante « cible PA » ne survit que si le code la porte (sinon retirée et signalée, D-19), renvoi par lien aux sections propriétaires (`parcours-simplifie.md` pour la lecture du résultat et la sauvegarde, `cli.md` pour toute ligne de commande), et jamais `db clear` dans un parcours recommandé.

---

## Contrôle des renvois obsolètes (critère 5) — forme du détecteur

| Option | Description | Selected |
|--------|-------------|----------|
| Ciblé sur les trois renvois | Le détecteur signale les trois formes nommées par le ROADMAP : menu associé au mauvais libellé, `F7` présenté comme armes distance, arrivée « directe » dans le wizard | ✓ |
| Générique, ancré au rendu | Confronte l'arborescence du texte au rendu réel (numéro ↔ libellé) et les filtres à `TYPE_FILTER_KEYS`/`TYPE_FILTER_LABELS`, au lieu de coder les trois cas en dur | |

**User's choice:** Ciblé sur les trois renvois
**Notes:** Le ROADMAP nomme les trois formes et la dette est **mesurée**, pas hypothétique — les trois ont été reconfirmées au code pendant la discussion. Même arbitrage que les « Sondes » de la phase 2 : ciblé + limite honnête écrite dans le test, plutôt qu'un contrôle général plus lourd. Un détecteur générique devrait extraire de la prose des paires *numéro ↔ libellé*, ce qui produirait des faux positifs sur de la prose légitime (le fichier cible en contient précisément) pour un gain non réclamé. Contraintes : attentes ancrées au code/rendu (jamais de mémoire), limite honnête consignée, et le détecteur ne doit pas signaler un renvoi légitime — notamment le lien D-44 ajouté.

---

## Preuve du critère 5 (deux états exigés)

| Option | Description | Selected |
|--------|-------------|----------|
| Ordre TDD seul | Détecteur écrit et lancé avant correction (rouge réellement observé), puis correction (vert) — preuve transitoire | |
| Copie figée seule | Texte obsolète conservé comme fixture, signalé par le même détecteur — preuve durable | |
| **Les deux** | Ordre TDD **et** copie figée : preuve littérale *et* relançable, qui protège le détecteur d'une régression | ✓ |

**User's choice:** Les deux
**Notes:** Le critère exige « rouge sur l'état antérieur puis vert après correction, dans la même phase », donc l'observation littérale est requise ; la fixture rend en plus la preuve relançable et vérifie le détecteur lui-même. La fixture est un artefact de `tests/` (helpers du `tests/conftest.py` existant, D-12), pas une page de documentation. Engagement explicite : le rouge et le vert ne seront cités que **réellement obtenus** ; si le test échoue, il est signalé et corrigé.

---

## Redirection de `README.md`

| Option | Description | Selected |
|--------|-------------|----------|
| Supprimer la ligne | La ligne `**Guide détaillé :** [GUIDE_WIZARD.md](GUIDE_WIZARD.md)` disparaît ; la section « Documentation utilisateur » garde son lien unique vers `docs/sommaire.md` | ✓ |
| Rediriger vers le sommaire | La ligne reste mais sa cible devient `docs/sommaire.md` ; risque d'un second lien vers le sommaire dans le même fichier | |

**User's choice:** Supprimer la ligne
**Notes:** Après la phase 4, `GUIDE_WIZARD.md` n'est plus la source du wizard : continuer à le présenter comme « le guide détaillé » entretiendrait le mode de défaillance mesuré. Rediriger ferait vivre **deux liens vers le sommaire dans le même fichier**, ce qui affaiblit le contrôle de structure et crée une seconde formulation du même renvoi (D-17 appliqué à la navigation). Le lecteur ne perd rien : le sommaire porte l'entrée « Wizard avancé » et le parcours ordonné. Emplacement exact vérifié au fichier réel avant édition.

---

## Dette de renvoi D-44 (soulevée pendant la discussion)

| Option | Description | Selected |
|--------|-------------|----------|
| Ajouter le lien maintenant | Les renvois en prose des lignes ~5 et ~256 de `docs/parcours-simplifie.md` deviennent de vrais liens, dans le même commit que la cible — D-44 attribue le lien à la phase qui crée la page cible | ✓ |
| Laisser la prose | Le lien est ajouté plus tard ; la dette reste ouverte alors que sa condition de levée est la création de la cible | |

**User's choice:** Ajouter le lien maintenant
**Notes:** D-44 tranche déjà ; la question ne fait que l'appliquer. Reporter en phase 6 ferait porter à une phase de complétude une écriture qui appartient à la phase propriétaire. Seules les lignes ~5 et ~256 sont touchées ; la ligne ~140 (`Precedent`/`Suivant` du wizard) reste intacte, sa véracité devant simplement être confirmée par le contrôle d'ancrage. Coût assumé et signalé : `docs/parcours-simplifie.md` s'ajoute aux fichiers de la phase.

---

## Claude's Discretion

- Libellé exact du `H1` de l'aiguillage `GUIDE_WIZARD.md` et texte de l'avis de déplacement.
- Découpage interne des nouveaux tests (`tests/test_docs_wizard.py` dédié ou extension d'un module existant), sans dupliquer les helpers de `tests/conftest.py` (D-12).
- Forme concrète de la fixture portant la copie figée du texte obsolète.
- Regroupement éventuel des 9 étapes en sous-sections, tant que l'ordre du code et les titres réellement rendus restent vérifiables.
- Formulation exacte de la limite honnête du détecteur dans le test.

## Deferred Ideas

- Renvoi en prose vers la base locale dans `docs/parcours-simplifie.md` — sa cible est la **phase 5**, le lien sera ajouté par la phase qui crée `docs/base-locale.md` (règle D-44).
- Liste épinglée des 8 pages du sommaire — reste en **phase 6**.
- `docs/glossaire.md` et `docs/depannage.md` — pages listées au sommaire mais non livrées ; phases suivantes.
- Aucun élargissement de périmètre pendant la discussion.
