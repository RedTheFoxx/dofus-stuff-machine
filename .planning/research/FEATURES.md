# Feature Research — Documentation utilisateur (FR) de dofus-stuff-machine

**Domain:** Documentation utilisateur en français d'un produit **déjà livré** (package Python 3.11+,
CLI `fetcher.py`, interface web Flask « terminal rétro », solveur ortools, base SQLite Dofusdude).
Milestone brownfield : le produit fonctionne, ce qui manque est la doc.
**Researched:** 2026-09-10 (HEAD `19b5c96`, dernier commit fonctionnel `1d475f9`)
**Confidence:** **HIGH** sur l'inventaire des capacités, des écrans et des libellés (lecture
directe du code + **rendu réel de chaque écran** en mode hors-ligne via le client de test Flask) ;
**MEDIUM** sur l'arbitrage des parcours lecteur et des priorités (jugement éditorial, pas un fait
de code). Aucun outil web n'est configuré sur cet hôte : toutes les affirmations sont ancrées dans
des fichiers du dépôt, lus ou exécutés ici.

**Périmètre.** Ce document répond à une seule question : *quels documents, quels parcours lecteur et
quelles sections faut-il pour aller de l'installation à un stuff terminé sans quitter la doc — et à
quel artefact de code chaque affirmation documentée doit-elle être ancrée ?* Il ne re-décide pas le
layout (arbitré dans `.planning/research/STACK.md` §2 : `docs/` + `docs/sommaire.md` +
`installation.md`, `parcours-simplifie.md`, `wizard-avance.md`, `cli.md`, `base-locale.md`,
`depannage.md`, `glossaire.md`) : les noms de fichiers utilisés ci-dessous sont **ceux-là**, pour
que le roadmap puisse composer les deux recherches sans arbitrage supplémentaire.

**Méthode de vérification employée** (reproductible, sans réseau, sans écriture sous `.data/`) :

- lecture intégrale de `dofus_stuff/web/routes.py`, `dofus_stuff/web/optimize_wizard.py`,
  `dofus_stuff/web/static/js/terminal.js`, `dofus_stuff/web/templates/screen.html`,
  `dofus_stuff/cli.py`, `dofus_stuff/database.py`, `dofus_stuff/sync.py`,
  `dofus_stuff/optimize/recommend.py`, `dofus_stuff/optimize/api.py`,
  `dofus_stuff/optimize/profile_input.py`, `dofus_stuff/model/solver_spec.py`,
  `dofus_stuff/model/slots.py`, `dofus_stuff/web/__init__.py`, `dofus_stuff/web/__main__.py`,
  `dofus_stuff/web/dofusbook_export.py`, `README.md`, `GUIDE_WIZARD.md`, `pyproject.toml`, `tests/` ;
- **rendu des écrans réels** : `create_app(offline=True)` + client de test Flask
  (`GET /`, `/system`, `/version`, `/db`, `/search?q=Cape`, `/item?id=44`, `/list`, `/sets`,
  `/saves`, `/quit`, `/optimize/wizard/<step>` pour les 9 étapes, `POST /optimize/quick/*`,
  chaîne complète jusqu'à `OPT-03`) — mode hors-ligne, `skip_sync`, **aucune** requête Dofusdude ;
- **lecture seule** de `.data/dofus.sqlite3` (`sqlite3 connect('file:…?mode=ro')`) pour connaître la
  forme des données (pas pour figer des valeurs dans la doc : cf. §5) ;
- `pytest` non modifié ; aucun fichier du dépôt n'a été écrit hormis ce document.

---

## 0. Ce qu'est une « feature » dans ce projet

Ici une feature n'est pas un écran du produit (le produit est fait) : c'est **un document, une
section ou un parcours lecteur qui rend une capacité existante utilisable par un lecteur**. Trois
règles de recevabilité, appliquées à chaque ligne des tableaux ci-dessous :

1. **Une feature documentaire existe seulement si elle ferme un trou de parcours.** « Le lecteur
   doit pouvoir faire X sans ouvrir le code » — sinon ce n'est pas une feature, c'est du remplissage.
2. **Toute affirmation est ancrée** : un fichier du dépôt (idéalement un symbole ou un libellé
   littéral) prouve ce que la doc raconte. Les libellés d'écran sont **recopiés verbatim** ; la
   prose qui les entoure est rédigée.
3. **Une feature documentaire est vérifiable ou elle n'est pas livrable.** Chaque item porte la
   manière dont `pytest` peut le prouver (structure, ancrage code) — cohérent avec DOCS-11/12 et
   avec la décision projet « remplacer la relecture humaine par un contrôle automatique ».

---

## 1. Inventaire vérifié de ce qui est réellement documentable

Tout ce qui suit a été **observé** (rendu des écrans ou lecture du code), pas déduit.

### 1.1 Écrans web : codes PGM, routes et titres réels

Le code affiche un identifiant d'écran dans l'en-tête (`PGM: <code>`), posé par `_screen(...)`.
Ces codes sont un excellent ancrage documentaire : ils sont stables, uniques et littéraux.

| PGM | Route | Titre réel (en-tête) | Contenu réel | Artefact |
|-----|-------|----------------------|--------------|----------|
| `MNU-01` | `GET /` | `** STUFF-MACHINE - MENU PRINCIPAL **` | 5 entrées : `1. RECHERCHE D'OBJETS`, `2. LISTE DES EQUIPEMENTS`, `3. LISTE DES PANOPLIES`, `4. OPTIMISATION DE STUFF`, `5. SYSTEME`, puis `SELECTIONNEZ UNE OPTION ET APPUYEZ SUR ENTREE :` | `routes.py:188-210` |
| — | `POST /` | — | `4` → `/optimize` (flux simplifié) ; `1/2/3/5` → écrans ; sinon erreur `OPTION INVALIDE — SAISIR 1 A 5` | `routes.py:213-228` |
| `SYS-01` | `GET /system` | `** SYSTEME **` | `1. DETAIL EQUIPEMENT (PAR ID)`, `2. VERSION LOCALE`, `3. SELF-TEST`, `4. GESTION DE LA BASE` | `routes.py:230-248` |
| `END-01` | `GET /quit` | `** FIN DE SESSION **` | `SESSION TERMINEE.` / `VOUS POUVEZ FERMER CET ONGLET` / `OU REVENIR AU MENU (ESC).` | `routes.py:266-282` |
| `SRC-01` | `GET /search` | `** RECHERCHE D'OBJETS **` | `SAISIR UN TERME DE RECHERCHE (SENSIBLE A LA CASSE).`, `LIMITE PAR DEFAUT : 10 RESULTATS.`, `SYNTAXE OPTIONNELLE : terme\|/limite` (sic), `EXEMPLE : Cape\|20` | `routes.py:290-307` |
| `SRC-02` | `POST /search` | `** RESULTATS DE RECHERCHE **` | ligne `REQUETE : … LIMITE : … TROUVES : …`, table `ID / NIV / NOM / TYPE`, `SAISIR UN ID ANKAMA POUR AFFICHER LE DETAIL.` | `routes.py:322-368` |
| `ITM-01` | `GET /item` | `** DETAIL EQUIPEMENT **` | `SAISIR L'IDENTIFIANT ANKAMA DE L'EQUIPEMENT.`, `EXEMPLE : 44  (Epee de Boisaille)` | `routes.py:397-413` |
| `ITM-02` | `GET /item?id=44` | `** ITEM #44 **` | `ID … — nom`, `Niveau :`, `Type :`, `Description :`, `Effets :`, `Recette :` en noms d'ingrédients résolus ; panneau `[ APERCU ]` avec l'illustration Dofusdude à droite (masqué si l'image ne charge pas) | `routes.py:396-452`, `catalog.py:194-243`, `screen.html:38-47`, `terminal.js:101-115` |
| `LST-01` | `GET /list` | `** LISTE DES EQUIPEMENTS **` | `PAGE 1/872   TAILLE 5   TOTAL EQUIPEMENTS 4356` (observé) ; table `ID/NIV/NOM/TYPE` | `routes.py:453-518` |
| `PAN-01` | `GET /sets` | `** LISTE DES PANOPLIES **` | `PAGE 1/186  TAILLE 5  TOTAL PANOPLIES 929` (observé) ; `ID/NIV/OBJ/NOM` | `routes.py:519-582` |
| `PAN-02` | `GET /set?id=…` | `** PANOPLIE #… **` | `ID … — nom`, `Niveau :`, `Nombre d'objets :`, `Objets :` (par ID), `Bonus de panoplie :` par palier ; champ de saisie `ANKAMA_ID` avec `ENTREE=DETAIL OBJET` | `routes.py:583-641`, `catalog.py:246-295` |
| `VER-01` | `GET /version` | `** VERSION LOCALE **` | `VERSION DOFUS (LOCALE) : <version>`, `ENTREES EN MEMOIRE : <n>`, `DATA DIR : <chemin>` | `routes.py:642-670` |
| `TST-01` | `GET /self-test` | `** SELF-TEST **` | `RESULTATS SELF-TEST :` puis `[OK]`/`[ECHEC]` par contrôle, `TOUS LES CONTROLES SONT OK.` ou `ECHEC : N CONTROLE(S)` | `routes.py:671-708`, `cli.py:230-290` |
| `DB-01` | `GET /db` | `** GESTION DE LA BASE **` | `1. ETAT DE LA BASE (STATUS)`, `2. SYNCHRONISATION FORCEE (SYNC)`, `3. VIDER LA BASE (CLEAR)` | `routes.py:709-728` |
| `DB-02` | `GET /db/status` | `** ETAT DE LA BASE **` | `FICHIER :`, `VERSION JEU :`, `DERNIER CHECK : IL Y A XH` ou `(AUCUN)`, `ENTREES :`, `PAR CATEGORIE :` | `routes.py:744-786` |
| `DB-03` | `GET /db/sync` | `** SYNCHRONISATION **` | `CETTE OPERATION CONTACTE L'API DOFUSDUDE` / `ET PEUT PRENDRE PLUSIEURS MINUTES.` / `CONFIRMER ? (O=OUI / N=NON)` | `routes.py:788-805` |
| `DB-04` | `GET /db/clear` | `** VIDER LA BASE **` | `ATTENTION : TOUTES LES ENTREES LOCALES SERONT SUPPRIMEES.` + statut rouge `OPERATION DESTRUCTIVE` | `routes.py:843-861` |
| `OPT-SIMPLE` | `GET/POST /optimize/quick/<classe\|elements\|niveau>` | `** RECOMMANDATION DE STUFF **` | `VOTRE STUFF EN 3 CHOIX`, `1/3 - Quelle est votre classe ?`, `2/3 - Quels éléments privilégier ?`, `3/3 - Quel est votre niveau ? (1 à 200)`, `AVANCE : personnaliser les réglages` | `routes.py:929-1025` |
| `OPT-W1` … `OPT-W9` | `GET/POST /optimize/wizard/<step>` | `** WIZARD — <STEP_TITLES[step]> **` | 9 étapes (cf. §1.3) | `routes.py:1027-1195`, `optimize_wizard.py:21-44` |
| `OPT-WED` | même route, sous-écran d'édition | `** WIZARD — EDITION **` / `** WIZARD — EDITION CARAC **` | `VALEUR ACTUELLE :`, `FORMAT : BASE POINTS CIBLE POIDS` (ou `BASE EXO CIBLE POIDS`), `NOUVELLE VALEUR (ENTREE VIDE = ANNULER) :` | `routes.py:1198-1277` |
| `SAV-01` | `GET/POST /saves` | `** STUFFS SAUVEGARDES **` | `CHARGEMENT DES SAUVEGARDES LOCALES…` puis rendu **côté navigateur** ; statut `N OUVRIR \| DEL N \| PURGE OUI` | `routes.py:1280-1296`, `terminal.js:344-518` |
| `OPT-03` | `GET/POST /optimize/result` | `** RESULTAT OPTIMISATION **` | voir §1.6 ; statut `ID DETAIL \| SAVE [NOM] \| SAVES \| EDIT \| DB` ; `PAGE 1/6` observé sur le flux simplifié | `routes.py:1298-1383` |

### 1.2 Flux simplifié (la nouveauté `1d475f9`, la partie la moins documentée)

| Élément | Valeur réellement produite | Artefact |
|---------|---------------------------|----------|
| Redirection d'entrée | `GET /optimize` → `302` vers `/optimize/quick/classe` | `routes.py:929-934` |
| Ordre des étapes | `steps = ("classe", "elements", "niveau")` | `routes.py:936-937` |
| Garde de profondeur | accès direct à `/optimize/quick/niveau` sans profil → retour à `1/3` (observé) | `routes.py:939-944` |
| Classes | `CLASSES` = 19 noms, **dans cet ordre** : Cra, Ecaflip, Eliotrope, Eniripsa, Enutrof, Feca, Forgelance, Huppermage, Iop, Osamodas, Ouginak, Pandawa, Roublard, Sacrieur, Sadida, Sram, Steamer, Xelor, Zobal — affichées en 3 colonnes numérotées `1.` … `19.` | `recommend.py:4-8`, `routes.py:990-995` |
| Saisie classe | **nom ou numéro** ; accents et casse ignorés (normalisation NFD) : `Crâ`, `cra`, `9` valent `Cra` / `Iop` (vérifié : `test_recommend.py::test_quick_flow_and_advanced` poste `Crâ`) | `routes.py:961-974` |
| Saisie éléments | libres, séparés par espace, `,` ou `+` ; alias `1`=terre `2`=feu `3`=eau `4`=air ; `multi` = les quatre | `routes.py:975-982`, écran `2/3` |
| Message d'écran 2/3 | `Classe : <classe>`, `1. Terre    2. Feu    3. Eau    4. Air`, `Un ou plusieurs : feu / terre air / 1 3 / multi`, `Le multi valorise aussi votre élément le plus faible.` | `routes.py:997-1000` |
| Saisie niveau | entier `1`–`200` uniquement | `routes.py:983-989` |
| Message d'écran 3/3 | `PA/PM et vitalité sont pris en compte selon le niveau.`, `Points répartis automatiquement, sans exo ni parchemins.`, `Jets moyens ; préférences de classe ajustables après calcul.` | `routes.py:1001-1007` |
| Erreurs réelles (flash, en rouge) | `Saisissez le nom ou le numéro de votre classe.` / `Exemple : feu, terre air, ou multi.` / `Saisissez un niveau entre 1 et 200.` | `routes.py:965-989` |
| Indices d'entrée | statut `ENTREE=SUIVANT` aux étapes 1–2, `ENTREE=CALCULER` à l'étape 3 | `routes.py:1019-1025` |
| Raccourci avancé | `AVANCE` : si classe **et** éléments connus → construit la spec de recommandation et ouvre `OPT-W9` (récap) ; sinon réinitialise le wizard (`default_player_spec(level=200)`) puis ouvre le récap — **observé : `AVANCE` depuis 3/3 non répondu donne `NIVEAU 200 … DUREE=8s … TOP-K` issu de la reco** | `routes.py:945-957`, `optimize_wizard.py:92-96` |
| Règles déterministes du profil recommandé | capital = `5 × (niveau − 1)` points répartis à coût réel croissant ; poids `1/len(elements)` par carac ; `Dommage <élément>` poids `3/len` ; PA cible 6/8/10/11 et PM cible 3/4/5/6 selon les seuils **40 / 100 / 150** ; `PA.base = 6 + (niveau ≥ 100)` ; `Vitalité` cible `niveau × 12`, poids `0.15` ; `% Dommages aux sorts` poids 12 ; `% Critique` cible 35 poids 2 ; résistances élémentaires cible 25 poids 2 ; `exo = scroll = 0` ; `top_k = 40`, `time_limit_s = 8` | `recommend.py:11-61`, prouvé par `tests/test_recommend.py::test_recommendation_investment` (paramétré sur 8 niveaux × 3 combinaisons d'éléments) |
| Heuristiques de classe (à documenter comme telles : « préférences larges, pas une simulation de sorts ») | distance : Cra, Enutrof, Sadida, Eniripsa, Steamer, Osamodas ; mêlée : Iop, Sacrieur, Ouginak, Zobal ; `Portée` visée 2 (< 100) ou 4 (≥ 100) pour Cra, Enutrof, Sadida ; `Invocation` base 1 cible 3 poids 35 pour Osamodas et Sadida | `recommend.py:52-61` |

### 1.3 Wizard avancé : 9 étapes, libellés et commandes exactes

`WIZARD_STEPS = ("slots", "options", "caracs", "papmpo", "resistances", "damages", "misc",
"items", "recap")` et `STEP_TITLES` associés (`optimize_wizard.py:21-44`). Libellés observés :

| # | PGM | Titre | Libellés / commandes réels | Artefact |
|---|-----|-------|----------------------------|----------|
| 1 | `OPT-W1` | `SLOTS ET FILTRES` | `SLOTS (N=TOGGLE) :` + `1. AMULETTE` … `11. PRYSMARADITE` avec `[ON ]`/`[OFF]` ; `FILTRES TYPES (F+N) :` `F1. FAMILIER` … `F10. PRYSMARADITE` ; rappel `N=TOGGLE SLOT  FN=TOGGLE FILTRE` | `optimize_wizard.py:78-98`, `110-130` |
| 2 | `OPT-W2` | `OPTIONS SOLVEUR` | `OPTIONS (N=EDIT) :` + 11 lignes : `1. NIVEAU`, `2. JET`, `3. DUREE (S)`, `4. SEED`, `5. TOP-K`, `6. CP-SAT`, `7. STOP SI CIBLES`, `8. AUTO POINTS`, `9. ALLOW POWER`, `10. ALLOW DOMMAGES`, `11. ALLOW DOM CRIT` | `optimize_wizard.py:133-152`, `265-297` |
| 3 | `OPT-W3` | `CARACTERISTIQUES` | 6 lignes dans l'ordre `Vitalité, Sagesse, Force, Intelligence, Chance, Agilité`, format `B= P= C= W=` | `solver_spec.py:71-78`, `optimize_wizard.py:154-176` |
| 4 | `OPT-W4` | `PA / PM / PO` | `1. PA`, `2. PM`, `3. Portée`, format `B= E= C= W=` | `solver_spec.py:80`, `optimize_wizard.py:154-176` |
| 5 | `OPT-W5` | `RESISTANCES` | 14 lignes, **page 1/2 observée** (`% Résistance Neutr…`, `Résistance Critiques`, `Résistance Poussée`, `% Résistance distance`, `% Résistance mêlée`) ; noms tronqués à 18 caractères à l'affichage | `optimize_wizard.py:46-61`, `128-133` |
| 6 | `OPT-W6` | `DOMMAGES` | 15 lignes, page 1/2 (`Dommage`, `Puissance`, `% Dommages aux sor…` tronqué) | `optimize_wizard.py:63-78` |
| 7 | `OPT-W7` | `DIVERS` | 12 lignes (Initiative, Prospection, Invocation, Retrait/Esquive PA-PM, `% Critique`, Soin, Tacle, Fuite, Pod) | `optimize_wizard.py:80-93` |
| 8 | `OPT-W8` | `ITEMS INTERDITS / FORCES` | `ITEMS — SYNTAXE :` `+ID AJOUTER INTERDIT`, `-ID AJOUTER FORCE`, `!ID RETIRER (BAN OU FORCE)`, `CLEAR VIDER LISTES`, puis compteurs `INTERDITS (n)` / `FORCES (n)` (8 premiers IDs, `… +k` au-delà) | `optimize_wizard.py:240-263` |
| 9 | `OPT-W9` | `RECAPITULATIF` | `NIVEAU … JET=… DUREE=…s`, `SLOTS :`, `POIDS :`, `CIBLES :`, `BAN=… FORCE=…`, `STOP=… AUTO=…`, `POWER=… DMG=… CRIT=…`, `GO = LANCER  RESET = REINITIALISER  1-8 = RETOUR ECRAN`, `SAVES = STUFFS SAUVEGARDES` | `optimize_wizard.py:266-282`, `routes.py:1129-1143` |

Comportements de saisie vérifiés (à documenter ; ce sont les pièges réels) :

- **Entrée vide avance** d'une étape (slots, options, listes de stats, items) ; au récap, Entrée vide = `GO` ; en **édition**, Entrée vide = **annuler** — `routes.py:1058-1066`, `1081`, `1097`, `1129-1133`, `1215-1217`, `1231-1233`.
- **Numéros de ligne** : une liste de stats attend le **numéro** de ligne puis ouvre `OPT-WED` ; texte non numérique → `Saisir le numero de la ligne` ; hors bornes → `Numero invalide` — `routes.py:1085-1095`.
- **Format d'édition** exactement **4 nombres** (`,` acceptés comme séparateurs) : `BASE POINTS CIBLE POIDS` (stat normale) ou `BASE EXO CIBLE POIDS` (PA/PM/PO) ; sinon `Format : BASE POINTS CIBLE POIDS` — `optimize_wizard.py:325-352`.
- **Les parchemins (`scroll`) ne sont pas saisissables dans le wizard** : `apply_stat_edit` conserve `prev.scroll` sans jamais le modifier ; seul le CLI les expose (`--scroll-int`, …). Conséquence documentaire : `GUIDE_WIZARD.md:256-266` (« base 200 + parchemins 100 ») décrit une valeur à **plier dans BASE**, pas un champ.
- **Au moins un slot actif** : sinon `Au moins un slot requis` — `optimize_wizard.py:288-289`.
- Filtres : `FN` bascule ; `F0`/`F11` → `Filtre invalide` ; slot hors bornes → `Slot invalide` ; autre texte → `Saisie invalide` — `optimize_wizard.py:264-298`.
- Items : `+ID` = **interdit**, `-ID` = **forcé** (contre-intuitif, à expliciter) ; un ID ne peut pas être dans les deux (l'ajout retire de l'autre liste) ; `!ID` retire des deux ; `CLEAR` vide les deux ; sinon `Syntaxe : +ID | -ID | !ID | CLEAR` — `optimize_wizard.py:354-381`.
- Options 6 à 11 : le numéro **bascule immédiatement** ; options 1 à 5 : ouvre l'édition (`level`, `jet` ∈ min/average/max, `time_limit_s`, `seed` — `-`/`none`/`aucun` pour effacer, `top_k` ≥ 1) — `optimize_wizard.py:300-323`.
- **Défauts différents selon le chemin d'entrée** : wizard « vierge » (menu → `AVANCE` sans profil, ou `RESET`) = `niveau 200, JET=average, DUREE=5s, TOP-K=30, CP-SAT=ON` (`SolverSpec` par défaut, `slots.py`/`solver_spec.py:145-159`) ; wizard atteint **via `AVANCE` avec classe+éléments** = `DUREE=8s`, `TOP-K=40`, poids/cibles du profil recommandé — observé deux fois (§1.2 et rendu `OPT-W9`).
- Défaut **BOUCLIER `[OFF]`** dans `DEFAULT_SLOT_GROUPS` (le shield est activable mais n'est pas dans les défauts) — `solver_spec.py:29-40`, observé `8. [OFF] BOUCLIER`.
- La page 1 de l'écran 1 ne montre que `F1`–`F3` : 22 lignes de corps pour 18 lignes visibles ⇒ **2 pages** (statut `PAGE 1/2`, `F7`/`F8` pour feuilleter) — `screens.py:8-16`, `routes.py:120-131`, observé.

### 1.4 Clavier et navigation (source de vérité : le JS + les attributs du template)

| Touche | Effet réel | Artefact |
|--------|-----------|----------|
| `Entrée` | soumet le champ de saisie quand il a le focus | `terminal.js:551-553` |
| `F3` | quitte : charge `data-f3-url` = `/quit` (`END-01`) — **absent de `GUIDE_WIZARD.md`** | `terminal.js:528-532`, `screen.html:20`, `tests/test_web.py::test_quit` |
| `ESC` | charge `data-esc-url` = `back_url` de l'écran, **menu principal par défaut** (et `SYS-01` pour les écrans Système, `PAN-01` depuis une panoplie) | `terminal.js:534-538`, `screen.html:21`, `tests/test_web.py::test_system_screens_return_to_system` |
| `F7` / `F8` | **hiérarchique** : d'abord page locale (`?page=`), sinon URL d'étape du wizard (`data-f7-url`/`data-f8-url`) | `terminal.js:500-526`, `routes.py:1017-1025`, `tests/test_web.py::test_wizard_exposes_step_nav_urls` |
| `PageUp` / `PageDown` | même logique que F7/F8 (local puis étape) | `terminal.js:541-559` |
| Focus | le champ est `autofocus` ; **clic n'importe où** dans l'écran recharge le focus (le JS fait `preventDefault` + `focus()`), et le focus est repris au chargement | `terminal.js:88-98`, `screen.html:56-68` |
| Barre de statut | concatène message + `PAGE x/y` + `ENTREE=<hint>` (sinon `ENTREE=VALIDER`) | `routes.py:143-150` |
| Barre de touches | recalculée selon l'écran : `F3=Quitter` au menu, `F7=Page prec`/`F8=Page suiv` ou `Precedent`/`Suivant`, `ESC=Retour` | `routes.py:139-141`, `screens.py:100-108` |

### 1.5 Sauvegardes locales et export Dofusbook

| Élément | Réalité | Artefact |
|---------|---------|----------|
| Stockage | `localStorage`, clé **`dofus-stuff-machine.saves`**, structure `{version: 1, stuffs: [...]}` | `terminal.js:12-14`, `201-207` |
| Plafond | **20 entrées** ; au-delà, la plus ancienne est supprimée (`shift`) | `terminal.js:14`, `307-310` |
| Création | tape `SAVE` ou `SAVE <label>` **sur l'écran de résultat uniquement** (`data-mode="result"`, formulaire intercepté) | `terminal.js:594-608`, `routes.py:1310-1325` |
| Résumé auto | extrait `Niveau …`, `Méthode …`, `Score …` des lignes du résultat ; repli `Stuff sauvegardé` | `terminal.js:236-260` |
| Liste | `SAV-01` : raison sociale `N OUVRIR \| DEL N \| PURGE OUI \| ESC` ; `N` ouvre, `DEL N` supprime, `PURGE OUI` efface tout (`PURGE` seul demande confirmation), `BACK` (ou `LISTE`, `L`) revient de la fiche | `terminal.js:440-518` |
| Export Dofusbook | sur une fiche : `DB` → `POST /optimize/dofusbook-url` puis ouverture d'un onglet ; `POST /optimize/result` avec `DB` utilise `webbrowser.open_new_tab` (URL affichée dans le statut si l'ouverture échoue) ; URL = `https://www.dofusbook.net/fr/equipement/dofus-stuffer/objets?stuff=<base64 msgpack>` | `terminal.js:428-438`, `routes.py:1327-1373`, `dofusbook_export.py:20-77` |
| Limite honnête | une sauvegarde faite **avant** l'ajout des slots (entrées anciennes) ne peut pas être exportée : message `AUCUN SLOT SAUVEGARDE — RE-SAUVEGARDER DEPUIS UN RESULTAT` | `terminal.js:428-434` |

### 1.6 Écran de résultat (`OPT-03`) : ce qui s'affiche, dans quel ordre

Observé sur le flux simplifié (Iop / terre / niveau 123, hors-ligne, CP-SAT) : **6 pages** de 18
lignes, statut `ID DETAIL | SAVE [NOM] | SAVES | EDIT | DB`.

- **En tête (mode simplifié)** : `Niveau <n> — <Élément>`, puis `PA x | PM y | Portée z`,
  `Éléments : <carac> <valeur>`, `Puissance … | Vitalité ajoutée …`, `Points inclus ; sans
  exo/parchemins. Jets moyens sauf réglage avancé.`, `Build valide : oui|non` — `optimize/api.py:305-316`, `344`.
- **Puis** `Équipement :` avec 17 emplacements affichés dans un ordre fixe (`amulet, ring_a, ring_b,
  belt, boots, hat, cape, weapon, shield, dofus_1…dofus_6, pet, prysma`), chaque ligne
  `<slot> : <Nom> [<Type>] (#<ID Ankama>, niv. <n>)` ; les slots optionnels vides sont omis,
  les autres affichent `(vide)` — `optimize/api.py:347-395`.
- **Puis** `Panoplies actives : N`, `Stats totales (avec équipement) :`, `Stats gagnées (équipement +
  panoplies) :`, `Bonus de panoplie :` (`<nom> — <n> pièces (palier k)`), `Détail <carac> — base+parcho
  | items | sets`, et **en fin de document** `Méthode :`, `Score : … | Indice de recherche : …% [mode]`,
  l'avertissement `Recherche sur une sélection du catalogue ; optimalité globale non garantie.`,
  `Objectif à vérifier : …`, `Build incomplet — emplacements vides : …`, `Greedy: … | UB0: …` —
  `optimize/api.py:327-346`, `353-357`, `396-436`.
- **Conséquence documentaire importante** : le **score** et l'**indice de recherche** ne sont pas en
  haut de l'écran : dans le flux simplifié ils arrivent **en dernière page** (les diagnostics sont
  volontairement déplacés en fin de sortie quand un profil « simplifié » est détecté) —
  `optimize/api.py:308-309`, `342-346`, `428-431`. Toute doc qui promet « l'écran résultat montre le
  score » sans dire *où* est inexacte en pratique.
- Les en-têtes de slots et les noms de stats sont **tronqués à 18 caractères** (`% Dommages aux sor…`) :
  la doc doit fournir la correspondance libellé tronqué → libellé complet, sinon le lecteur ne sait
  pas à quoi il tape — `optimize_wizard.py:128-133`.

### 1.7 CLI (`python fetcher.py …` / `dofus-stuff …`)

Sous-commandes et options réellement parsées (`cli.build_parser`, ré-exporté « pour tests /
scripts ») :

| Sous-commande | Rôle | Options | Artefact |
|---------------|------|---------|----------|
| `version` | version Dofus de la base locale (`Version Dofus (locale) : 3.6.10.11` observé) | — | `cli.py:60-61`, `cli.py:363-369` |
| `self-test` | contrôles base + objets connus, sortie `[OK]`/`[ÉCHEC]` | — | `cli.py:62`, `230-290` |
| `search` | recherche locale par sous-chaîne, **sensible à la casse** | `query`, `--limit` (défaut 10) | `cli.py:64-66`, `catalog.py:119-142` |
| `item` | détail d'un équipement par ID Ankama | `ankama_id` | `cli.py:68-69` |
| `list` | page d'équipements | `--page` (1), `--size` (5) | `cli.py:71-74` |
| `optimize` | optimiseur (démo, flags, ou **interactif** si aucun profil) | cf. tableau ci-dessous | `cli.py:76-215` |
| `db` / `cache` | `status`, `sync`, `clear` (+ alias muets `stats`→`status`, `fill`→`sync`) | — | `cli.py:217-235`, `cli.py:295-299` |

Options globales : `--timeout` (15), `--data-dir` (`.data/`), `--force-sync`, `--offline`.
Options d'`optimize` : `--level`, `--max`, `--base-int/vit/str/cha/agi/wis`, `--scroll-*`, `--jet`
(min|average|max), `--top-k` (30), `--time-limit` (5.0), `--no-cpsat`, `--classic-only`, `--demo`,
`--target STAT=valeur`, `--weight STAT=valeur`, `--ban`, `--force`, `--seed`,
`--stop-when-satisfied`, `--auto-points`, `--allow-power`, `--allow-damages`,
`--allow-crit-damages`.

Mode interactif (aucun `--level`, `--max` ni `--demo`) : prompts `Niveau [demo] :`,
`Classique seul (sans dofus/familier) [n] :`, `Jets (min|average|max) [average] :`,
`Caractéristique(s) à maxer (ex: intelligence) :`, `Base hors stuff (<carac>) [0] :`,
`Parchemin (<carac>) [0] :` — `profile_input.py:324-403`. Le parseur d'« ligne compacte »
(`123 int,vit 200,50 100,0 classic jet=max`) existe et est testé, mais **n'est branché sur aucune
sous-commande ni option** : ne pas le documenter comme une commande utilisateur sans le dire
explicitement (`profile_input.py:223-317`, `tests/test_profile_input.py`).

Messages d'erreur CLI observés : `Erreur : Base locale vide et --offline : impossible de
synchroniser` (exit 1), `Erreur : 'Équipement introuvable : #999999'` (exit 1),
`Erreur : --offline incompatible avec db sync` — `sync.py:55-59`, `catalog.py:74-78`, `cli.py:322-325`.

### 1.8 Base locale et hors-ligne

| Élément | Réalité | Artefact |
|---------|---------|----------|
| Fichier | `.data/dofus.sqlite3` (répertoire par défaut = `.data/` du dépôt), tables `meta` + `items (kind, ankama_id, payload JSON)` | `database.py:12-13`, `36-70` |
| Catégories | `equipment, resources, consumables, quest, cosmetics, mounts, sets` | `database.py:20-28` |
| Fenêtre de re-check | `CHECK_INTERVAL_SECONDS = 24 * 60 * 60` ; au-delà (ou base vide, ou `--force-sync`) : re-test de version et resync si la version a changé | `sync.py:14`, `29-36` |
| Hors-ligne | `--offline` / `DOFUS_OFFLINE=1` : aucune requête API ; base vide ⇒ échec explicite | `sync.py:52-59`, `web/__init__.py:39-42` |
| Asymétrie CLI/web (à documenter telle quelle) | `db sync` **refuse** avec `--offline` ; dans le web, `DB-03`/`DB-04` appelle `ensure_up_to_date(..., offline=False)` **quel que soit** `--offline` (le menu prévient `CETTE OPERATION CONTACTE L'API DOFUSDUDE`) | `cli.py:322-325` vs `routes.py:807-840` |
| `db status` | sortie `Fichier :`, `Version jeu :`, `Dernier check : il y a Xh` / `(aucun)`, `Entrées :`, `Par catégorie :` — mêmes champs dans `DB-02` (en majuscules) | `cli.py:257-270`, `routes.py:744-786` |
| Effet de bord | `db status` **crée** le fichier (et le dossier) s'ils n'existent pas : observé sur un `--data-dir` vide → `Entrées : 0`, exit 0 | `database.py:38-42`, vérifié en répertoire temporaire |
| Web, variables | `DOFUS_DATA_DIR`, `DOFUS_OFFLINE`, `DOFUS_TIMEOUT`, `DOFUS_SECRET_KEY` ; options `--data-dir`, `--offline/--no-offline`, `--online`, `--timeout`, `--host` (127.0.0.1), `--port` (5000), `--debug` | `web/__init__.py:16-60`, `web/__main__.py:13-32` |
| Base vide côté web | l'app **démarre** : `VER-01` affiche `ERREUR : AUCUNE VERSION EN BASE.` et `SRC-02` `AUCUN RESULTAT.` (observé) | `routes.py:642-670`, `332-334` |

### 1.9 Recherche : le piège de la casse (et une coquille d'écran)

`Catalog.search_items` fait un `query in name` **sensible à la casse** (`catalog.py:119-142`) —
vérifié sur la base réelle : `Cape` → 10 résultats, `cape` → `Abracape`, `Gelocape`, `Vegacape`,
`Caracape`, … (sous-chaîne), `CAPE` → **0**. L'écran `SRC-01` l'annonce (`SENSIBLE A LA CASSE`) mais
affiche une coquille de syntaxe : `SYNTAXE OPTIONNELLE : terme|/limite` alors que le parseur attend
`terme|<entier>` (le `/` provoque `LIMITE INVALIDE`) — `routes.py:290-320`. La doc utilisateur doit
donner la **syntaxe qui marche** (`Cape|20`) **et** signaler l'écart avec le texte de l'écran.

---

## 2. Parcours lecteur (reader journeys) — le critère « sans quitter la doc »

Un parcours est la seule unité qui prouve la valeur de la doc : chaque étape doit être couverte par
une page, et **la page doit dire où l'on clique/tape ensuite**. Les 7 parcours ci-dessous couvrent
tout ce que le produit sait faire ; J1→J4 sont le cœur (« de l'installation à un stuff terminé »),
J5→J7 sont les parcours d'appoint qui existent déjà dans le produit et qu'aucune doc ne couvre.

| # | Parcours | Étapes réelles | Pages qui doivent le couvrir | Trou actuel |
|---|----------|----------------|------------------------------|-------------|
| **J1** | Installer et prouver que ça marche (CLI) | `pip install -e ".[dev]"` → `python fetcher.py version` → `python fetcher.py self-test` → `pytest` | `installation.md` | `README.md` liste les commandes mais n'explique ni `self-test` ni ce qu'un échec signifie ; `pytest` est mentionné sans dire ce qu'il prouve |
| **J2** | Premier stuff par le flux simplifié (web) | `python -m dofus_stuff.web` → `http://127.0.0.1:5000` → `4` → classe → élément(s) → niveau → résultats | `installation.md` (§ interface) + `parcours-simplifie.md` | **aucune doc** : `GUIDE_WIZARD.md` envoie au wizard, le `README.md` s'arrête à 4 lignes de prose |
| **J3** | Lire et interpréter le résultat | page 1 (résumé + équipement) → pages suivantes (stats, panoplies) → dernière page (méthode, score, indice) → ouvrir un item par son ID | `parcours-simplifie.md` (§ lire le résultat), renvoi depuis `wizard-avance.md` | partiel et trompeur : `GUIDE_WIZARD.md:218-236` annonce « le score et un % de compatibilité » **sur l'écran** sans dire qu'ils sont en dernière page |
| **J4** | Personnaliser puis relancer (wizard avancé) | `AVANCE` (ou menu → wizard via restauration de session) → 9 étapes → `GO` → `EDIT` → récap modifié → `GO` | `wizard-avance.md` | `GUIDE_WIZARD.md` décrit le wizard mais se trompe d'entrée (menu `3`) et ignore `EDIT`/`AVANCE` en tant qu'entrée |
| **J5** | Consulter le catalogue (annuaire) | `1` recherche (`Cape`, `Cape\|20`) → ouvrir un ID → `5` Système → détail par ID ; `2` liste paginée ; `3` panoplies → détail → objet | `installation.md` (§ interface) + `depannage.md` (casse, ID invalide) ; une section « consulter un objet » dans `parcours-simplifie.md` ou `base-locale.md` | `README.md` cite seulement les entrées de menu ; **jamais** la syntaxe `terme\|limite`, la casse, la pagination ni le panneau `[ APERCU ]` |
| **J6** | Garder et réutiliser un stuff | `SAVE [nom]` → `SAVES` → ouvrir `N` → `DB` (Dofusbook) → `DEL N` / `PURGE OUI` | `parcours-simplifie.md` (§ sauvegardes) | `README.md` : **rien**. `GUIDE_WIZARD.md:237-250` : liste incomplète (pas de `DB`, pas des alias, pas du mode résultat/navigateur) |
| **J7** | Base locale, hors-ligne, et quand resynchroniser | `db status` → lire les champs → `db sync` (réseau) ou `DB-01 → 2` → comprendre la fenêtre 24 h et l'échec « base vide + `--offline` » | `base-locale.md` (+ `depannage.md`) | `README.md` décrit `.data/dofus.sqlite3` et la fenêtre 24 h en 1 paragraphe (exact) mais pas les champs de `db status`, pas l'asymétrie CLI/web de la sync, pas les messages d'échec |

**Critère d'acceptation transversal (proposé pour les PR)** : pour J2 et J4, un lecteur qui suit la
page **dans l'ordre** doit voir à l'écran chaque libellé cité par la doc, sans ouvrir un fichier
`.py`. C'est exactement ce qu'un test d'ancrage (`DOCS-12`) peut vérifier mécaniquement.

---

## 3. Table Stakes (le lecteur les exige ; sinon il ouvre le code)

| Document / section | Pourquoi c'est exigible | Complexité | Artefact d'ancrage | Exigence |
|--------------------|-------------------------|-----------|--------------------|----------|
| `docs/sommaire.md` : index des 7 pages + parcours conseillé (installation → parcours simplifié → glossaire) | Sinon le lecteur ne sait pas par où commencer ; c'est aussi le point d'entrée que `README.md` doit citer | LOW | les 7 fichiers `docs/` (test d'exhaustivité bidirectionnelle) | DOCS-01, DOCS-02 |
| `README.md` : section « Documentation utilisateur » + renvoi depuis l'ancienne ligne `GUIDE_WIZARD.md` | `README.md` est la première page lue (et le `readme` du paquet) ; il ne doit plus envoyer vers une page périmée | LOW | `README.md:59`, `pyproject.toml:readme` | DOCS-02 |
| `docs/installation.md` : prérequis, installation, premier lancement CLI **et** web, `pytest`, URL `http://127.0.0.1:5000` | J1 et J2 : sans ça rien ne démarre ; « Python 3.11+ » et `pip install -e ".[dev]"` sont les seules vraies préconditions | LOW | `pyproject.toml` (`requires-python`, `dependencies`, `[project.scripts]`), `web/__main__.py:13-34` | DOCS-03 |
| `docs/installation.md` § « l'interface terminal : ce qu'il faut savoir avant de taper » (champ, ligne de statut, barre de touches, `F3`/`ESC`/`F7`/`F8`, `PAGE x/y`, `ENTREE=…`) | Sans cette section, le lecteur ne peut pas *taper* : l'UI n'est pas un site web | MEDIUM | `screen.html` (attributs `data-*`), `terminal.js:528-559`, `routes.py:143-150` | DOCS-03 (+ socle de DOCS-05) |
| `docs/parcours-simplifie.md` : les 3 questions avec leurs libellés verbatim, les entrées acceptées, les 3 messages d'erreur, `AVANCE` | C'est le cœur de la valeur produit depuis `1d475f9` ; la doc actuelle ne le décrit pas du tout dans son corps | MEDIUM | `routes.py:929-1025`, `recommend.py:4-8` | DOCS-04 |
| `docs/parcours-simplifie.md` § « lire le résultat » : ordre réel du contenu, pagination, où sont `Méthode`/`Score`/`Indice de recherche`, table de correspondance des libellés de slots (`amulet`, `ring_a`, `dofus_3`…) et des stats tronquées | J3 : un stuff affiché sans mode d'emploi du résultat n'est pas un stuff obtenu | MEDIUM | `optimize/api.py:305-436`, `solver_spec.py:15-27`, `optimize_wizard.py:128-133` | DOCS-04 |
| `docs/parcours-simplifie.md` § « ce que l'outil suppose » (5 points par niveau, ni exo ni parchemins, jets moyens, cibles PA/PM par palier 40/100/150, heuristiques de classe) | Le lecteur doit pouvoir expliquer le résultat ; ces règles sont déterministes et déjà testées | MEDIUM | `recommend.py:11-61`, `tests/test_recommend.py::test_recommendation_investment` | DOCS-04 |
| `docs/wizard-avance.md` : les **9** étapes dans l'ordre de `WIZARD_STEPS`, avec les titres de `STEP_TITLES`, les commandes de chaque étape et les 2 formats d'édition | J4 ; l'exigence dit « écran par écran, aligné sur les libellés réels » | HIGH | `optimize_wizard.py:21-44`, `154-176`, `240-352`, `routes.py:1027-1277` | DOCS-05 |
| `docs/wizard-avance.md` : slots 1→11 (dont `BOUCLIER` OFF par défaut), filtres `F1`→`F10` avec leur intitulé exact, options 1→11, syntaxe items `+`/`-`/`!`/`CLEAR`, récap `GO`/`RESET`/`SAVES`/`1-8` | Ce sont les points où l'on se trompe (`-ID` = **forcé** ; `F6` = armes distance) | MEDIUM | `solver_spec.py:15-54`, `optimize_wizard.py:78-98`, `133-152`, `240-282` | DOCS-05 |
| `docs/cli.md` : tableau de **toutes** les sous-commandes + **toutes** les options globales + exemples exécutables, avec avertissement sur `db clear` | J1 et usage « dev » ; `README.md` n'en montre qu'une fraction (aucun `--target`, `--ban`, `--no-cpsat`, …) | MEDIUM | `cli.py:41-235`, `tests/test_profile_input.py` pour la syntaxe | DOCS-06 |
| `docs/base-locale.md` : fichier, catégories, mode hors-ligne par défaut, fenêtre **24 h**, `db status` décrit par ses **champs** (jamais par des valeurs), `--force-sync`, asymétrie CLI/web, échec « base vide + `--offline` » | J7 ; c'est le point qui explique les 90 % de « ça ne marche pas » | MEDIUM | `database.py:12-28`, `sync.py:14-59`, `cli.py:257-270`, `routes.py:744-840` | DOCS-07 |
| `docs/depannage.md` : 5 rubriques (base absente/vide, saisie invalide, calcul long, clavier inactif, résultat paginé) **avec le message réel** à l'appui | Le lecteur cherche par message, pas par concept ; exiger le libellé rend la page grep-able | MEDIUM | messages listés en §1.2/1.3/1.7/1.8, `terminal.js:88-98`, `routes.py:143-150` | DOCS-08 |
| `docs/glossaire.md` : vocabulaire jeu **et** vocabulaire outil, trié, chaque entrée reliée à un libellé du produit | Sans glossaire, « PA/PM/PO », « exo », « jet », « poids », « cible », « slot », « prysmaradite » restent opaques | LOW | `solver_spec.py:71-80`, `EXO_STATS`, `STEP_TITLES["papmpo"]`, `TYPE_FILTER_LABELS`, `model/slots.py:8-30` | DOCS-09 |
| Correction de `GUIDE_WIZARD.md` (arborescence de menus) + renvoi unique vers `docs/wizard-avance.md` | Deux descriptions concurrentes sont la **cause** de la désynchronisation constatée | LOW | §8 de ce document (audit cité) | DOCS-10 |

---

## 4. Differentiators (ce qui rend la doc réellement utile plutôt que « générée »)

| Feature documentaire | Valeur pour le lecteur | Complexité | Ancrage |
|----------------------|------------------------|-----------|---------|
| **Bloc « Source de vérité » en tête de chaque page** (chemins `.py` + symboles en backticks) | Le lecteur sait *sur quoi* la page s'engage, et le dépôt peut le vérifier : un fichier renommé casse un test | LOW | convention proposée par `STACK.md` §3.1 ; fichiers cibles listés en §9 |
| **Encadré « ce que vous devez voir à l'écran »** (copie verbatim du rendu) dans J2/J4/J5 | Transforme la doc en procédure vérifiable ; supprime la question « est-ce que j'ai fait pareil ? » | LOW | sorties relevées §1.1–1.3 (reproductibles hors-ligne) |
| **Table de correspondance libellé affiché → nom complet** pour les slots (`dofus_3`), les stats tronquées (`% Dommages aux sor…`) et les abréviations (`B/P/C/W`, `E` pour exo) | Sans elle, le lecteur ne peut pas interpréter la page 2+ du résultat ni les listes du wizard | LOW | `optimize/api.py:347-395`, `optimize_wizard.py:128-133` |
| **Carte de pagination du résultat** (page 1 = résumé + équipement ; pages intermédiaires = stats/panoplies ; dernière page = `Méthode`, `Score`, `Indice de recherche`) | Répond à la question « où est passé le score ? » que la doc actuelle crée | LOW | `optimize/api.py:308-309`, `342-346`, `428-431` ; observé `PAGE 1/6` |
| **Section « défauts différents selon l'entrée »** (wizard vierge = `DUREE 5s`/`TOP-K 30` ; wizard via `AVANCE` = profil de reco, `8s`/`TOP-K 40`) | Explique pourquoi deux utilisateurs voient deux valeurs différentes — sinon la doc paraît fausse | MEDIUM | `solver_spec.py:145-159`, `routes.py:945-957`, observé sur `OPT-W9` |
| **Section « règles du profil recommandé »** (5 points/niveau, cibles PA/PM par palier, heuristiques distance/mêlée/portée/invocation par classe) | Le lecteur comprend *pourquoi* son Iop reçoit +mêlée et son Cra +portée ; c'est du contenu que personne ne peut deviner | MEDIUM | `recommend.py:11-61`, `tests/test_recommend.py` |
| **Transparence sur les limites** (« indice de recherche » ≠ qualité en combat, CP-SAT sur un sous-ensemble de candidats, prix/kamas/effets déclenchés/rotations non simulés, conditions non numériques à vérifier en jeu, vitalité affichée = vitalité ajoutée) | Évite la déception et les rapports de bug ; le texte existe déjà dans `README.md`, il doit être consolidé dans une section stable | LOW | `README.md` (paragraphe solveur), `optimize/api.py:327-346`, `recommend.py:52` |
| **« Consulter le catalogue » documenté** : syntaxe `terme\|limite` qui marche, casse significative avec contre-exemples réels (`Cape` vs `cape` vs `CAPE`), pagination `PAGE x/y`, panneau `[ APERCU ]` masqué hors-ligne | C'est un usage légitime (vérifier un objet, récupérer un ID à bannir/forcer) absent de toute doc | MEDIUM | `catalog.py:119-142`, `routes.py:284-320`, `terminal.js:101-115` |
| **Dépannage rédigé à partir des messages réels** (chaque ligne cite la chaîne affichée, y compris les bizarreries : `'ÉQUIPEMENT INTROUVABLE : #999999'` avec apostrophes issues de `str(KeyError)`) | Le lecteur trouve sa ligne en collant ce qu'il voit ; exploitable par un test qui cherche ces chaînes | MEDIUM | §1.2/1.7/1.8 ; `routes.py:415-419` |
| **Sauvegardes et export Dofusbook documentés** (localStorage navigateur, 20 max, `SAVE [nom]` seulement depuis le résultat, `DB` seulement depuis une fiche, URL Dofusbook) | Ferme J6 : c'est ce qui transforme « un résultat affiché » en « un stuff réutilisable » ; aujourd'hui seul `GUIDE_WIZARD.md:237-250` en parle, partiellement | MEDIUM | `terminal.js:12-14`, `201-438`, `routes.py:1327-1373`, `dofusbook_export.py:20-77` |
| **Section « ce que l'outil ne fait pas » dans `installation.md` ou `base-locale.md`** (pas de budget kamas, pas de simulation de sorts, pas d'exo/parchemins en simplifié, pas de prix) | Cadre les attentes dès l'installation ; évite que le lecteur croie à un simulateur de combat | LOW | `README.md`, `recommend.py:41-48`, `optimize/api.py:344-346` |
| **Table « message affiché → ce qu'il faut faire »** y compris les cas non évidents : `db status` **crée** un fichier vide ; `DB-01 → 2` contacte l'API **même** en `--offline` ; `db sync` CLI **refuse** `--offline` | Débloque les situations où le lecteur croit à un bug alors que le comportement est voulu | MEDIUM | `database.py:38-42`, `routes.py:807-840`, `cli.py:322-325` |
| **Parcours d'installation vérifiable de bout en bout hors-ligne** (les exemples de la doc sont exécutables sans réseau, avec la base locale fournie) | Respecte la contrainte projet « hors-ligne par défaut » et rend la doc testable sans effet de bord | LOW | `sync.py:52-59` ; exemples choisis dans §1 (aucun `db sync`) |

---

## 5. Anti-Features (contenu à ne **pas** produire)

| Anti-feature | Pourquoi elle semble bonne | Pourquoi elle est problématique | À faire à la place |
|--------------|---------------------------|--------------------------------|--------------------|
| Documenter l'architecture interne, les heuristiques de `candidates.py`/`cpsat.py`, le mapping `SLOT_GROUPS` → instances, le format msgpack Dofusbook | « Ça aide à comprendre » | Hors périmètre explicite de `PROJECT.md` (public « Utilisateur + dev », pas « Développeur ») ; les seuils de préfiltrage et le format reverse-engineered bougent, la doc devient fausse sans qu'aucun test d'ancrage ne puisse suivre la sémantique | Une phrase de limite dans `parcours-simplifie.md` (« recherche sur une sélection du catalogue ») + le renvoi au code pour l'implémentation |
| Générer une référence d'API automatique (Sphinx/autodoc, docstrings extraites) | « C'est gratuit » | Ajoute un outillage et une dépendance, cible du public développeur, et produit des pages non rédigées en français | Rédiger la doc utilisateur à la main (décision `STACK.md` §4) |
| Documenter **la ligne compacte** de l'optimiseur (`123 int,vit 200,50 100,0 classic jet=max`) comme une forme d'appel CLI | Elle existe, elle est testée | Elle n'est **branchée sur aucune sous-commande ni option** (vérifié : seul `optimize` avec flags, ou le mode interactif) ; la documenter promet une interface inexistante | Ne pas la documenter ; si l'équipe y tient, l'annoncer explicitement comme « non exposée en CLI » dans `cli.md` |
| Décrire `db clear` / `DB-01 → 3` comme une procédure de dépannage (« repartir de zéro ») | « Réinitialiser règle 80 % des problèmes » | Les règles du projet interdisent `db clear`, le drop SQLite et toute destruction sous `.data/` ; conseiller la destruction de la base locale contredit la contrainte et la remise en état exige un réseau | Documenter l'existence de l'entrée **comme destructive** (statut `OPERATION DESTRUCTIVE`), et orienter vers `db status` puis `db sync` |
| Recopier des **valeurs volatiles** de la base dans la doc (`18288` entrées, `3.6.10.11`, `il y a 96.0h`, `PAGE 1/872`) | Cela rend la doc concrète | La base se resynchronise : ces chiffres seront faux et aucun test d'ancrage ne peut les protéger (et un test ne doit pas lire `.data/`) | Décrire les **formats** (`Fichier :`, `Version jeu :`, `Dernier check : il y a Xh`, `Entrées :`, `Par catégorie :`) et laisser la commande produire les chiffres |
| Dupliquer la description du wizard dans `README.md` **et** `docs/wizard-avance.md` (et/ou laisser `GUIDE_WIZARD.md` complet) | « C'est plus pratique d'avoir tout dans le README » | C'est **exactement** la cause de la désynchronisation constatée (deux descriptions concurrentes depuis `692736b`/`1d475f9`) | Une source unique (`docs/wizard-avance.md`), `README.md` aiguille, `GUIDE_WIZARD.md` réduit à un aiguillage corrigé |
| Ajouter des captures d'écran / images | « Une image vaut mille mots » | L'UI est du **texte** collable ; des images ne sont pas vérifiables par un test, ajoutent des binaires et vieillissent silencieusement (le rendu terminal change à chaque commit de `routes.py`) | Blocs de code avec le texte exact de l'écran, encadrés « ce que vous devez voir » |
| Documenter la gestion du paquet, la CI, les migrations de base, le `.doc-agent/` (run local `status: "running"`, `stage: "PLAN"`, sortie `docs` configurée dans `doc-agent.toml`) | Ces fichiers existent dans le dépôt | Aucun rapport avec le besoin « utilisateur, en français » ; `.doc-agent/` n'est pas suivi par git et son run est inachevé — le présenter reviendrait à raconter un outil en panne | Ignorer ces fichiers dans la doc utilisateur (ne rien supprimer) |
| Écrire la doc en anglais ou prévoir `docs/en/` | « Ça élargit l'audience » | Besoin explicitement « en Français » ; toute infra i18n est du surdimensionnement | Doc française unique |
| Publier la doc (site statique, GitHub Pages, PyPI) | « Une doc qu'on ne lit pas en ligne n'existe pas » | Publication et déploiement distant sont interdits par les règles du projet ; le rendu GitHub du Markdown suffit | Markdown nu dans `docs/`, liens relatifs, commit local |
| Recopier ligne à ligne la prose de `GUIDE_WIZARD.md` vers `docs/wizard-avance.md` sans correction | « Migrer est plus sûr que réécrire » | Migre les 8 erreurs factuelles auditées en §8 ; la valeur ajoutée disparaît | Migrer la **structure utile** (les 9 écrans, les 4 nombres, les filtres) et corriger chaque libellé contre le code |
| Ajouter une page de « notes de développement » / « bugs connus » | « Transparence » | Crée un artefact non testable, non destiné au lecteur, et un second endroit où l'information peut périmer | Les limites fonctionnelles vont dans une section « limites » des pages concernées |

---

## 6. Dépendances entre features documentaires

```
docs/sommaire.md ──requires──> les 7 pages existent (exhaustivité bidirectionnelle)
README.md (## Documentation utilisateur) ──requires──> docs/sommaire.md
docs/installation.md ──requires──> README.md (point d'entrée)          [§ interface terminal]
docs/parcours-simplifie.md ──requires──> installation.md (avoir lancé l'interface)
docs/wizard-avance.md ──requires──> parcours-simplifie.md (AVANCE est le chemin d'entrée)
docs/wizard-avance.md ──enhances──> parcours-simplifie.md (EDIT ↩ récap, mêmes formats de saisie)
docs/depannage.md ──requires──> installation.md + base-locale.md + parcours-simplifie.md (messages cités)
docs/cli.md ──requires──> base-locale.md (--offline, --data-dir, db status/sync)
docs/glossaire.md ──enhances──> toutes les pages (liens sortants vers le terme défini)
GUIDE_WIZARD.md (aiguillage) ──requires──> docs/wizard-avance.md (source unique)
tests d'ancrage (DOCS-11/12) ──requires──> libellés figés dans les pages, existants dans le code
```

Notes de dépendance utiles au séquencement des phases :

- **`parcours-simplifie.md` avant `wizard-avance.md`** : `AVANCE` et `EDIT` ne se comprennent qu'à
  partir du flux simplifié ; inverser produit une page wizard qui commence par une redirection
  inexpliquée.
- **`base-locale.md` avant les exemples CLI exécutables** : sinon le lecteur lance des commandes qui
  échouent hors-ligne avec `Base locale vide et --offline : impossible de synchroniser`.
- **Le glossaire ne dépend de rien mais tout le monde y renvoie** : le produire tôt coûte peu et
  débloque la rédaction des autres pages (termes déjà stabilisés par ce document, §1).
- **Conflit à éviter dans une même phase** : réécrire `GUIDE_WIZARD.md` et rédiger
  `docs/wizard-avance.md` dans deux tâches parallèles sans arbitrer la source unique — c'est le
  scénario exact qui a produit la désynchronisation actuelle.
- **Les tests d'ancrage dépendent des pages, pas l'inverse** : écrire d'abord les pages (libellés
  corrects), puis les tests qui les relisent, sinon les tests figent les erreurs existantes.

---

## 7. MVP documentaire (ce qui doit être livré pour valider le besoin)

### Livré avec (v1) — indissociable du besoin

- [ ] `docs/sommaire.md` + `README.md` (section Documentation utilisateur) — sinon rien n'est trouvable (DOCS-01/02)
- [ ] `docs/installation.md` (prérequis, CLI, web, `pytest`, § interface terminal) — J1/J2 (DOCS-03)
- [ ] `docs/parcours-simplifie.md` (3 questions + erreurs + `AVANCE`, § lire le résultat, § ce que l'outil suppose, § sauvegardes/export) — J2/J3/J6, cœur de la valeur (DOCS-04)
- [ ] `docs/depannage.md` (5 rubriques, messages réels) — le filet qui évite l'abandon (DOCS-08)
- [ ] `docs/glossaire.md` — lève l'opacité du vocabulaire avant la fin de la rédaction (DOCS-09)
- [ ] `docs/wizard-avance.md` (9 écrans, slots/filtres/options, formats d'édition, récap) — J4 (DOCS-05)
- [ ] `docs/cli.md` (toutes sous-commandes et options, avertissement `db clear`) — usage dev (DOCS-06)
- [ ] `docs/base-locale.md` (fichier, 24 h, hors-ligne, champs de `db status`, asymétrie sync) — J7 (DOCS-07)
- [ ] `GUIDE_WIZARD.md` corrigé + aiguillage — supprime la source de désynchronisation (DOCS-10)
- [ ] Tests de structure/liens/sommaire et tests d'ancrage code — la preuve (DOCS-11/12)

### Ajouté après validation (v1.x)

- [ ] Section « limites de l'outil » consolidée (aujourd'hui éparpillée dans le `README.md`) — dès que la page `parcours-simplifie.md` dépasse ~250 lignes
- [ ] Table « message affiché → action » pour les 5 cas non évidents (§1.2, §1.7, §1.8) — si l'ancrage par message se révèle fragile en rédaction
- [ ] « Exemples exécutables » supplémentaires dans `cli.md` (chaque exemple prouvé analysable par `build_parser`) — quand les tests d'ancrage CLI existent

### Considéré plus tard (v2+ — hors besoin initial)

- [ ] Éclatement de `wizard-avance.md` en sous-pages si elle dépasse ~400 lignes (décision `STACK.md` §7 : réévaluer un sous-dossier **dans** `docs/`)
- [ ] Page dédiée « rechercher et consulter le catalogue » (aujourd'hui une section) si J5 devient un parcours principal
- [ ] Diagramme texte du flux menu → simplifié → avancé (utile, mais non nécessaire et non testable) — seulement si des lecteurs se perdent

---

## 8. Audit de péremption — `GUIDE_WIZARD.md` vs le code (constat demandé)

Le fichier porte un encadré d'avertissement ajouté par `1d475f9` (lignes 1-5) mais **son corps n'a pas
suivi** : ce commit n'a touché que 6 lignes du guide (`git show 1d475f9 --stat` : `GUIDE_WIZARD.md |
6 +++`) alors qu'il changeait le parcours d'entrée. Résultat : le guide se contredit lui-même
(l'encadré dit « le menu Optimisation demande classe, éléments et niveau », le §2 dit qu'on arrive
directement dans le wizard).

| `GUIDE_WIZARD.md` | Ce que dit le guide | Réalité du code (ancrage) | Verdict |
|-------------------|---------------------|---------------------------|---------|
| L33-43 (menu principal en bloc de code) | `1. RECHERCHE D'OBJETS` / `2. LISTE DES EQUIPEMENTS` / `3. OPTIMISATION DE STUFF` / `4. SYSTEME` | `routes.py:190-205` : `1. RECHERCHE D'OBJETS` / `2. LISTE DES EQUIPEMENTS` / `3. LISTE DES PANOPLIES` / `4. OPTIMISATION DE STUFF` / `5. SYSTEME` ; prouvé par `tests/test_web.py::test_menu_get` | **FAUX** — panoplies manquante, deux numéros décalés |
| L35 | « Tapez `3` puis **Entrée** pour ouvrir l'optimisation. » | `routes.py:213-228` : `3` → `terminal.list_sets` ; `4` → `terminal.optimize_entry` | **FAUX** — `3` ouvre les panoplies |
| L45 | « Vous arrivez **directement** dans le wizard (premier écran : slots et filtres). » | `routes.py:929-934` : `/optimize` redirige vers `/optimize/quick/classe` ; écran `OPT-SIMPLE` = `VOTRE STUFF EN 3 CHOIX` / `1/3 - Quelle est votre classe ?` (observé) | **FAUX** — le wizard est atteint par `AVANCE` |
| L50 | « L'option **4. SYSTEME** regroupe le reste… » | `routes.py:198-205` : Système = entrée `5` | **FAUX** (numéro) |
| L70 | « Sur la plupart des écrans, **Entrée à vide** = passer à l'écran suivant » | Vrai dans le wizard (`routes.py:1058-1066`, `1081`, `1097`, `1129-1133`) ; **faux dans le flux simplifié** : Entrée vide produit `Saisissez le nom ou le numéro de votre classe.` / `Exemple : feu, terre air, ou multi.` / `Saisissez un niveau entre 1 et 200.` (`routes.py:965-989`) | **TROMPEUR** depuis `1d475f9` |
| L63-74 (touches) | Cite `Entrée`, `F7`, `F8`, `ESC`, `PageUp/PageDown` ; présente `ESC` comme « retour à l'écran **parent** » | `F3` = `Quitter` → `END-01` (`terminal.js:528-532`, `screen.html:20`) est **absent du tableau** ; `ESC` charge `back_url`, qui est **le menu principal** par défaut (`screen.html:21`, `routes.py:177`), `SYS-01` seulement pour les écrans Système | **INCOMPLET / imprécis** |
| L142-157 (écran 1) | `F1` familiers, `F2` montiliers, « `F3`… Dragodindes, muldos, volkornes, armes distance/mêlée, dofus, trophées, prysmaradite » | `TYPE_FILTER_KEYS` (`solver_spec.py:43-54`) : `F3` = DRAGODINDE, `F4` = MULDO, `F5` = VOLKORNE, `F6` = ARMES DISTANCE, `F7` = ARMES MELEE, `F8` = DOFUS, `F9` = TROPHEE, `F10` = PRYSMARADITE ; **écran sur 2 pages** (observé `PAGE 1/2`) | **INCOMPLET** |
| L157 | « pour interdire les armes à distance, tapez `F7` » | Armes distance = `F6` ; `F7` = armes mêlée (`solver_spec.py:49-50`) | **FAUX** — l'exemple fait basculer le mauvais filtre |
| L142-147 | Ne liste pas les 11 slots ni leurs numéros ; « laissez les défauts » | `SLOT_GROUP_LABELS` / `SLOT_GROUPS` (`optimize_wizard.py:96-108`, `solver_spec.py:15-40`) : 1 AMULETTE … 7 ARME, 8 BOUCLIER, 9 DOFUS/TROPHEES, 10 FAMILIER/MONTURE, 11 PRYSMARADITE ; **BOUCLIER `[OFF]` par défaut** (absent de `DEFAULT_SLOT_GROUPS`) | **TROU** — le défaut change le résultat |
| L161-180 (écran 2) | « 5 Top-K … (défaut `30`) », « 3 Durée … ex. `5` ou `10` » | Vrai pour le wizard vierge (`solver_spec.py:157-159`) ; **faux quand on arrive par `AVANCE`** : `recommend.py:56-58` impose `top_k=40`, `time_limit_s=8` (observé sur `OPT-W9`) | **TROMPEUR** — dépend du chemin d'entrée |
| L82-98 | « Le wizard comporte **9 écrans** dans cet ordre » | `WIZARD_STEPS` (9 tuples) et `STEP_TITLES` — conforme | **CORRECT** (à conserver tel quel) |
| L192-204 (écran 8) | `+12345` interdit, `-12345` force, `!12345` retire, `CLEAR` vide | `optimize_wizard.py:354-381` — conforme (et le caractère contre-intuitif de `-ID` = forcé mérite d'être explicité) | **CORRECT** |
| L205-218 (écran 9) | `GO`, `RESET`, `SAVES`, `1`…`8` | `routes.py:1129-1143` — conforme | **CORRECT** |
| L220-227 | « L'écran résultat montre notamment : le score et un % de compatibilité » | `optimize/api.py:337-341` produit `Méthode : …`, `Score : … | Indice de recherche : …% [mode]` **mais** en mode simplifié ces lignes sont déplacées **en fin de sortie** (`api.py:308-309`, `342-346`, `428-431`) : observé en **page 1/6** du résultat, donc invisibles sans paginer | **TROMPEUR** — position non dite |
| L237-250 | Écran `STUFFS SAUVEGARDES` : `N`, `BACK`, `DEL N`, `PURGE OUI`, `ESC` ; « jusqu'à 20 entrées » | Conforme (`terminal.js:14`, `440-518`) mais **incomplet** : `DB` (export Dofusbook) existe dans la fiche, alias `LISTE`/`L`, et `PURGE` seul demande `CONFIRMER AVEC : PURGE OUI` ; la commande n'existe que si le stuff a des `slots` sauvegardés (`terminal.js:428-434`) | **INCOMPLET** |
| L254-266 (exemple guidé) | « base 200 + parchemins 100 déjà inclus dans la base » puis saisie `300 0 0 1` | Le wizard **n'a pas de champ parchemins** : `apply_stat_edit` ne modifie jamais `scroll` (`optimize_wizard.py:325-352`) ; seuls le CLI (`--scroll-*`) et la spec de recommandation (qui force `scroll=0`, `recommend.py:34` via `StatGoal`) les portent ; `README.md` précise « sans supposer de parchemins ni d'exos » | **TROMPEUR** — le guide suggère un champ inexistant |
| L300-308 (problèmes fréquents) | « Je ne vois que **4** dofus → appuyer sur F8 » | Le solveur affiche **6** emplacements de dofus/trophées (`slots.py:22` `dofus_1..dofus_6`, `api.py:372-377`) et le résultat est paginé (observé `PAGE 1/6`) | **DATÉ** (le conseil F8 reste juste) |
| L325-328 | « base locale (menu `4. SYSTEME` → `4. GESTION DE LA BASE` / sync) » | `5. SYSTEME` (`routes.py:198-205`) → `4. GESTION DE LA BASE` (`routes.py:710-714`) | **FAUX** (numéro du menu) |
| L1-5 (encadré) | « le menu Optimisation demande désormais classe, éléments et niveau » | Conforme à `routes.py:936-1025`, mais **contredit le corps du fichier** (§2) | **À réconcilier** |

Conclusion à porter au roadmap : `GUIDE_WIZARD.md` **ne peut pas être « corrigé » par retouches** — six
affirmations fausses et cinq trous structurels dans un seul fichier de 330 lignes. La solution la plus
simple est celle de `STACK.md` §2.4 : contenu migré et corrigé dans `docs/wizard-avance.md`, racine
réduite à un aiguillage de ~15 lignes avec l'arborescence **corrigée**, et un test
(`test_no_obsolete_menu_references`) qui interdit le retour de `3. OPTIMISATION DE STUFF`.

---

## 9. Ancrage obligatoire : affirmation documentée → artefact de code

Table de correspondance à utiliser telle quelle par les tests `DOCS-12` (et qui sert de checklist de
relecture) : chaque ligne dit *ce que la doc affirme* et *ce qui le prouve mécaniquement*.

| Affirmation à porter dans la doc | Artefact qui la prouve | Plus petit test possible |
|----------------------------------|------------------------|--------------------------|
| Le menu compte exactement 5 entrées, dans cet ordre (`1` recherche … `4` optimisation, `5` système) | `routes.menu()` | comparer le corps de `GET /` aux littéraux |
| L'entrée `4` ouvre le flux simplifié ; l'entrée `3` ouvre les panoplies | `routes.menu_post()` | `POST / {"selection": "4"}` → corps de `OPT-SIMPLE` |
| Le flux simplifié pose 3 questions, dans l'ordre classe → éléments → niveau, écran `OPT-SIMPLE`, titre `RECOMMANDATION DE STUFF` | `routes.optimize_quick` (`steps`, `pgm="OPT-SIMPLE"`) | `POST /optimize/quick/classe` → `1/3` ; etc. |
| Les classes acceptées sont les 19 de `CLASSES`, saisissables par nom (accents/casse ignorés) ou numéro | `recommend.CLASSES` + normalisation NFD dans `routes.optimize_quick` | `POST {"cmd": "Crâ"}` puis `{"cmd": "9"}` → même classe |
| Éléments : `terre/feu/eau/air`, alias `1`–`4`, séparateurs espace/`,`/`+`, `multi` = 4 éléments | `recommend.ELEMENTS` + parsing de `routes.optimize_quick` | `POST {"cmd": "terre + air"}` → `balanced_elements == ("Force","Agilité")` (déjà testé) |
| Niveau : entier 1–200, sinon message exact | bornes de `routes.optimize_quick` | `POST {"cmd": "201"}` → message présent |
| Les objectifs PA/PM du profil recommandé suivent les paliers 40/100/150 | `recommend.recommendation_spec` | réutiliser `tests/test_recommend.py::test_recommendation_investment` |
| `AVANCE` ouvre le récapitulatif du wizard (`RECAPITULATIF`), avec le profil de reco si classe+éléments connus | `routes.optimize_quick` (branche `AVANCE`) + `save_wizard_spec` | `POST {"cmd":"AVANCE"}` → `OPT-W9` |
| Le wizard compte 9 écrans, titres = `STEP_TITLES`, dans l'ordre de `WIZARD_STEPS` | `optimize_wizard.WIZARD_STEPS`, `STEP_TITLES` | comparaison normalisée des titres dans la page |
| Écran 1 : 11 slots nommés (dont BOUCLIER OFF par défaut) et filtres `F1`–`F10` avec leurs libellés | `optimize_wizard.SLOT_GROUP_LABELS`, `TYPE_FILTER_LABELS`, `solver_spec.DEFAULT_SLOT_GROUPS` | comparer le rendu de la page 1 **et** 2 |
| Écran 2 : 11 options numérotées (`NIVEAU` … `ALLOW DOM CRIT`) | `optimize_wizard.body_options` | appartenance des 11 libellés au rendu de `OPT-W2` |
| Écrans 3, 4, 5, 6, 7 : listes de stats exactes (`MAIN_CARACS`, `EXO_STATS`, `RESISTANCE_STATS`, `DAMAGE_STATS`, `MISC_STATS`) | `solver_spec` + `optimize_wizard` | appartenance des libellés |
| Formats d'édition `BASE POINTS CIBLE POIDS` / `BASE EXO CIBLE POIDS` (4 nombres) | `optimize_wizard.apply_stat_edit` | `apply_stat_edit` sur 3 et 5 nombres → erreurs |
| Syntaxe items `+ID` interdit / `-ID` forcé / `!ID` retire / `CLEAR` | `optimize_wizard.apply_items_input` | assert sur les ensembles `blacklist_ids`/`forced_ids` |
| Récap : `GO`, `RESET`, `SAVES`, `1`–`8` | `routes.optimize_wizard` (branche `recap`) | `POST` de chaque commande |
| Écran résultat : statut `ID DETAIL \| SAVE [NOM] \| SAVES \| EDIT \| DB` ; `EDIT` revient au récap ; un ID ouvre la fiche | `routes.optimize_result`, `_result_screen` | `POST {"cmd":"EDIT"}` → `/optimize/wizard/recap` (déjà testé) |
| `SAVE`/`SAVE <label>` n'agit que sur l'écran de résultat (mode `result`) | `terminal.js` (submit interceptor) | test d'ancrage textuel sur `js` |
| Sauvegardes : localStorage, clé exacte, 20 entrées max, commandes `N`/`DEL N`/`PURGE OUI`/`BACK`/`DB` | `terminal.js` | recherche des littéraux |
| Export Dofusbook : URL `dofusbook.net/fr/equipement/dofus-stuffer/objets?stuff=` + pas de slots → message d'erreur | `dofusbook_export.build_dofusbook_url`, `terminal.js` | `tests/test_web.py::test_build_dofusbook_url_*` existe déjà |
| Touches : `F3` quitte, `ESC` revient (`back_url`), `F7`/`F8` paginent puis changent d'étape | `terminal.js`, `screen.html` (`data-f3-url`, `data-esc-url`, `data-f7-url`, `data-f8-url`) | présence des attributs dans le rendu |
| CLI : chaque sous-commande et chaque option citée existe | `dofus_stuff.cli.build_parser` (ré-exporté « pour tests / scripts ») | `build_parser().parse_args(argv)` sans exception + présence du nom dans `cli.md` |
| Base locale : fichier, catégories, fenêtre 24 h, champs de `db status` | `database.py` (`DB_NAME`, `ITEM_KINDS`, `stats`), `sync.CHECK_INTERVAL_SECONDS`, `cli._print_db_status` | présence des libellés de champs |
| Hors-ligne : base vide échoue avec le message exact | `sync.ensure_up_to_date` | présence de la chaîne |
| Recherche sensible à la casse + syntaxe `terme\|limite` | `catalog.search_items`, `routes.search` | présence des exemples documentés (`Cape\|20`) |
| `db clear` est destructif (avertissement) et n'est pas une procédure conseillée | `database.Database.clear`, `routes.db_clear_confirm` (`OPERATION DESTRUCTIVE`) | présence du mot-clé d'avertissement dans `cli.md` |
| Aucune valeur volatile (nombre d'entrées, version, horodatage) dans `docs/**` | — | test négatif sur les motifs de valeurs (cf. `STACK.md` §3.5) |

---

## 10. Matrice de priorisation

| Feature documentaire | Valeur lecteur | Coût | Priorité |
|----------------------|----------------|------|----------|
| `installation.md` (J1/J2, dont § interface terminal) | HIGH | LOW | **P1** |
| `parcours-simplifie.md` (3 questions + erreurs + `AVANCE`) | HIGH | MEDIUM | **P1** |
| § « lire le résultat » (pagination, score en fin, libellés tronqués) | HIGH | LOW | **P1** |
| Corriger `GUIDE_WIZARD.md` + aiguillage + renvoi README | HIGH (supprime la désinformation) | LOW | **P1** |
| `sommaire.md` + entrée `README.md` | HIGH | LOW | **P1** |
| `depannage.md` (5 rubriques, messages réels) | HIGH | MEDIUM | **P1** |
| `glossaire.md` | MEDIUM | LOW | **P1** |
| `wizard-avance.md` (9 écrans, slots/filtres/options/défauts) | HIGH | HIGH | **P1** |
| `cli.md` (toutes commandes et options) | MEDIUM | MEDIUM | **P2** |
| `base-locale.md` (24 h, hors-ligne, asymétrie sync) | MEDIUM | MEDIUM | **P2** |
| § « règles du profil recommandé » (5 pts/niveau, paliers PA/PM, heuristiques de classe) | HIGH | MEDIUM | **P2** |
| § sauvegardes + export Dofusbook | MEDIUM | MEDIUM | **P2** |
| § « ce que l'outil suppose / ne fait pas » | MEDIUM | LOW | **P2** |
| Table libellé tronqué → nom complet (slots et stats) | MEDIUM | LOW | **P2** |
| Table « message → action » (cas non évidents : `db status` crée le fichier, sync web en `--offline`, sync CLI refusée) | MEDIUM | MEDIUM | **P3** |
| Parcours J5 « consulter le catalogue » en section dédiée | LOW | MEDIUM | **P3** |
| Diagramme du flux menu → simplifié → avancé | LOW | LOW | **P3** |

---

## 11. Base documentaire existante (à ne pas dupliquer, à corriger)

| Artefact | État vérifié | Ce qu'on en garde |
|----------|--------------|-------------------|
| `README.md` (121 lignes, français, orienté technique) | **Plutôt à jour** : les 5 entrées de menu (L101-104), le flux simplifié en 3 choix (L44-45), `--offline`/`--force-sync`/`--data-dir`/`--timeout`, l'asymétrie « sans parchemins ni exos », les limites du solveur | Sert de base aux sections techniques ; devient le point d'entrée vers `docs/` ; garde son avertissement implicite (il cite `db clear`, L78) |
| `GUIDE_WIZARD.md` (330 lignes, français, pédagogique) | **Périmé** (§8) : 6 affirmations fausses, 5 trous ; l'encadré L1-5 contredit le corps | Son plan (à quoi sert / démarrer / touches / parcours / B-P-C-W / écran par écran / lire le résultat / exemple / conseils / problèmes / lexique) est bon : c'est la **structure** à migrer dans `docs/wizard-avance.md` + `docs/depannage.md` + `docs/glossaire.md` |
| `docs/` | **N'existe pas** | — |
| `.doc-agent/runs/20260909T145903Z-fc7a7e36` + `doc-agent.toml` (`output = "docs"`, `language = "fr"`, modèle local) | Run **inachevé** (`status: "running"`, `stage: "PLAN"`), fichiers non suivis par git, aucun fichier livré | Rien à réutiliser ; ne pas s'en servir comme source (contenu non vérifié) et ne rien supprimer |
| `tests/` (6 modules, 1691 lignes) | Vert et **exploitable comme ancrage** : `test_web.py` contient déjà les assertions de libellés (`MENU PRINCIPAL`, `1. RECHERCHE`, `4. OPTIMISATION DE STUFF`, `5. SYSTEME`, `RECOMMANDATION`, `1/3`, `STUFFS SAUVEGARDES`, `data-mode="saves"`, pagination du résultat, `EDIT` → récap) | Les tests de doc s'ajoutent à côté sans modifier `pyproject.toml` ; les littéraux existants disent quels libellés sont déjà « officiels » |
| `pyproject.toml` | 3 dépendances runtime, extra `dev` = `pytest`, `testpaths`/`pythonpath` configurés, `[project.scripts]` = `dofus-stuff` et `dofus-stuff-web` | Aucune dépendance à ajouter ; ne pas oublier de documenter les deux points d'entrée (le README ne cite que `dofus-stuff-web`) |

---

## 12. Sources (toutes locales, aucune recherche web configurée)

- `C:/Users/Red/Documents/Projets/dofus-stuff-machine/.planning/PROJECT.md` (périmètre, DOCS-01..12, contraintes, hors-périmètre)
- `.planning/research/STACK.md` (layout `docs/`, conventions, design pytest — aligné ici)
- `dofus_stuff/web/routes.py` (toutes les routes et tous les libellés d'écran ; §1.1, §1.2, §1.6, §8)
- `dofus_stuff/web/optimize_wizard.py` (`WIZARD_STEPS`, `STEP_TITLES`, `body_*`, `apply_*` ; §1.3)
- `dofus_stuff/web/static/js/terminal.js` (touches, pagination, sauvegardes, export ; §1.4, §1.5)
- `dofus_stuff/web/templates/screen.html` (attributs `data-f3-url`, `data-esc-url`, `data-f7-url`, `data-f8-url`, `data-nav-base`, `data-mode`, `data-stuff-payload` ; §1.4)
- `dofus_stuff/optimize/recommend.py` + `tests/test_recommend.py` (règles du profil recommandé ; §1.2)
- `dofus_stuff/optimize/api.py` (`format_optimize_result` / `format_optimize_result_lines` ; §1.6)
- `dofus_stuff/optimize/profile_input.py` (parseur CLI, mode interactif, ligne compacte non branchée ; §1.7)
- `dofus_stuff/cli.py`, `dofus_stuff/database.py`, `dofus_stuff/sync.py`, `dofus_stuff/catalog.py`, `dofus_stuff/model/solver_spec.py`, `dofus_stuff/model/slots.py` (§1.3, §1.7, §1.8, §1.9)
- `dofus_stuff/web/__init__.py`, `dofus_stuff/web/__main__.py`, `dofus_stuff/web/dofusbook_export.py`
- `README.md`, `GUIDE_WIZARD.md`, `pyproject.toml` ; `git log` / `git show 1d475f9 --stat` (historique de la dérive du guide)
- Rendus d'écrans obtenus localement (mode hors-ligne, sans réseau) : `GET /`, `/system`, `/version`, `/db`, `/search?q=Cape`, `/item?id=44`, `/list`, `/sets`, `/saves`, `/quit`, `/optimize/wizard/<les 9 étapes>` (+ `?page=2`), `POST /optimize/quick/*`, chaîne complète jusqu'à `OPT-03` (6 pages) ; `fetcher.py db status`, `fetcher.py --offline version`, `fetcher.py --offline item 999999` ; lecture seule de `.data/dofus.sqlite3`.

---

## 13. Zones d'incertitude et questions ouvertes (pour la phase de rédaction)

1. **`GUIDE_WIZARD.md` : migrer ou corriger sur place ?** Ce document recommande la migration
   (source unique `docs/wizard-avance.md`, racine réduite en aiguillage) — décision de goût, déjà
   arbitrée avec confiance MEDIUM dans `STACK.md` §2.4. Si le roadmap choisit l'option alternative
   (« page complète corrigée »), alors **les tests d'ancrage doivent viser `GUIDE_WIZARD.md`** et
   `docs/sommaire.md` doit le référencer par un lien relatif `../GUIDE_WIZARD.md`.
2. **Page dédiée à la lecture du résultat ou section ?** Ce document recommande une **section** dans
   `docs/parcours-simplifie.md` (pas de 8ᵉ fichier) : cela garde le test d'exhaustivité du sommaire
   trivial et évite un nouveau fichier pour un contenu de ~60 lignes. À confirmer au plan.
3. **Nombre de pages de `docs/`** : le besoin DOCS-04/05 nomme deux flux, pas deux fichiers ; toute
   page supplémentaire doit être ajoutée à la liste du test d'exhaustivité, donc arbitrée une fois.
4. **Faut-il documenter la ligne compacte de l'optimiseur ?** Elle est testée mais non exposée ;
   la seule manière honnête est de la présenter comme « fonction interne, non disponible en CLI ».
   Incertitude assumée : l'équipe peut préférer l'exposer plus tard — la doc ne doit alors pas avoir
   à être démentie, d'où la recommandation de ne pas la traiter comme une commande.
5. **Durées de calcul** : les seules valeurs citables sont les **défauts du code** (`DUREE` 5 s / 8 s,
   `TOP-K` 30 / 40, palier 40/100/150). Ne pas citer de temps mesuré (4,3 s observé ici) : machine,
   base et solveur dépendants.
6. **Coquille de l'écran `SRC-01`** (`terme|/limite` alors que le parseur attend `terme|20`) : la doc
   doit-elle corriger le code ou signaler l'écart ? Le périmètre est documentaire et le code ne doit
   pas changer (`PROJECT.md` : « le code reste inchangé ») → documenter la syntaxe qui marche et
   signaler l'écart textuel en note.
7. **Échec d'un self-test** : les contrôles (`cli.collect_self_test_checks`) renvoient des libellés
   comme `objet 44 nom`, `lecture mémoire stable` ; la doc peut-elle expliquer chaque échec ? Les
   libellés sont stables mais techniques — incertitude éditoriale, à trancher en rédigeant
   `depannage.md`.

---

*Feature research for: documentation utilisateur (FR) d'un outil Dofus existant — dofus-stuff-machine*
*Researched: 2026-09-10 — HEAD `19b5c96`, code lu et écrans rendus hors-ligne (aucune recherche web, aucune écriture sous `.data/`)*


