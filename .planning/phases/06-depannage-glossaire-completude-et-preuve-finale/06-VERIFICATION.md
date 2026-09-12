---
phase: 06-depannage-glossaire-completude-et-preuve-finale
verified: 2026-09-12T01:57:54Z
status: human_needed
score: "7/8 verites verifiees (aucun ecart ; 1 comportement non exerce)"
covered_files:
  - .planning/REQUIREMENTS.md
  - .planning/ROADMAP.md
  - .planning/phases/06-depannage-glossaire-completude-et-preuve-finale/06-01-PLAN.md
  - .planning/phases/06-depannage-glossaire-completude-et-preuve-finale/06-01-SUMMARY.md
  - .planning/phases/06-depannage-glossaire-completude-et-preuve-finale/06-02-PLAN.md
  - .planning/phases/06-depannage-glossaire-completude-et-preuve-finale/06-02-SUMMARY.md
  - .planning/phases/06-depannage-glossaire-completude-et-preuve-finale/06-03-PLAN.md
  - .planning/phases/06-depannage-glossaire-completude-et-preuve-finale/06-03-SUMMARY.md
  - .planning/phases/06-depannage-glossaire-completude-et-preuve-finale/06-04-PLAN.md
  - .planning/phases/06-depannage-glossaire-completude-et-preuve-finale/06-04-SUMMARY.md
  - .planning/phases/06-depannage-glossaire-completude-et-preuve-finale/06-05-PLAN.md
  - .planning/phases/06-depannage-glossaire-completude-et-preuve-finale/06-05-SUMMARY.md
  - .planning/phases/06-depannage-glossaire-completude-et-preuve-finale/06-CONTEXT.md
  - .planning/phases/06-depannage-glossaire-completude-et-preuve-finale/06-RESEARCH.md
  - .planning/phases/06-depannage-glossaire-completude-et-preuve-finale/06-VALIDATION.md
  - GUIDE_WIZARD.md
  - README.md
  - docs/depannage.md
  - docs/glossaire.md
  - docs/sommaire.md
  - tests/test_docs_completude.py
  - tests/test_docs_depannage.py
  - tests/test_docs_glossaire.py
  - tests/test_docs_mutation.py
covered_digest: "v1:sha256:3943d1aa0a7fa438eb306746f83bfee024e2f4cf0e5d06f708c23bf9fccbe1f2"
behavior_unverified: 1
behavior_unverified_items:
  - truth: "Le comportement DOM de la rubrique « clavier inactif » : `autofocus` sur le champ, refocalisation du champ au clic hors du champ, et touche `Entree` qui ne soumet le formulaire que si le champ est l'element actif (`dofus_stuff/web/static/js/terminal.js:79-88`, `:595-601`)."
    reason: "present-behavior-unverified"
    evidence_status: "none provided"
overrides_applied: 0
re_verification:
  previous_status: gaps_found
  previous_score: "6/8 verites verifiees (1 ecart, 1 comportement non exerce)"
  gaps_closed:
    - "T3 (critere 1) : la rubrique « Resultat pagine » de `docs/depannage.md` n'affirme plus l'absolu de portee — « un ecran qui n'a qu'une seule page n'ajoute aucun motif a son statut » — que le produit contredit sur les deux ecrans de sauvegardes ; la ligne de statut est desormais bornee a chacune de ses deux surfaces productrices, nommees, avec la condition mesuree de chacune."
  gaps_remaining: []
  regressions: []
prohibitions:
  declared: 31
  structured_tiers_declared: 31
  test_tier:
    count: 21
    flagged: 0
    note: "Les 21 prohibitions de palier `test` des cinq plans sont armees et mesurees par des gardes reellement executees. J'ai rejoue moi-meme, ce tour-ci : la suite entiere (`250 passed in 5.87s`, rc=0), la variante sans reseau (greffon `no_net` : banniere des 6 pieges ecrite avant la collecte, `250 passed in 5.65s`), la batterie de morsures de la phase (`tests/test_docs_mutation.py`, 14 morsures declarees, vert) et la garde de cloture du harnais, et j'ai fabrique mes propres copies de morsure pour les trois nouvelles derivees (voir « Falsification »). Aucune ecriture sous `.data/` (empreinte `24989696:1788730056843137500:e3793d64cb79…` identique avant et apres chacune de mes mesures), aucune connexion reseau, `main()` jamais execute, `dofus_stuff/**` non modifie (`git status --porcelain -- dofus_stuff` vide, `git diff --name-only HEAD -- dofus_stuff` vide, `git log --since=2026-09-12T01:04:14Z -- dofus_stuff` vide : aucun commit depuis ma verification precedente ne touche le produit), aucune page livree supprimee (les 8 pages epinglees existent, ensemble exact), aucune valeur volatile ni chemin de poste dans la page corrigee, aucune ligne du `README.md` retiree."
  judgment_tier:
    count: 10
    flagged: 10
    flag: "unverified-prohibition — human review recommended"
    note: "Ces 10 verdicts sont des jugements NON AUTORITATIFS, consignes avec leur preuve et signales pour revue humaine ; ils ne sont pas absorbes en silence dans un vert. Les deux derniers viennent du plan de fermeture 06-05 et portent sur l'affaiblissement des controles et la portee des commits."
    verdicts:
      - statement: "Ne jamais ecrire un compteur de tests, une duree ou un resultat de suite avant de l'avoir mesure (06-04)."
        judge_verdict: "tenu"
        evidence: "Le `06-04-SUMMARY.md` cite sa sortie de commande (HEAD `d8693e1`) ; ma propre mesure finale rend `250 passed in 5.87s` (rc=0) sur le HEAD courant, et `250 passed in 5.65s` avec le greffon `no_net` : les figures du rapport sont du meme ordre et non embellies."
      - statement: "Ne jamais presenter une mutation non mordante comme un succes (06-04)."
        judge_verdict: "tenu"
        evidence: "`.gsd-tmp/06-04-morsures.txt` liste les 14 morsures par famille avec le motif observe ; la batterie mesure chaque copie verte avant mutation et echoue si le motif attendu manque (`43 passed` ce tour-ci pour le groupe completude + glossaire + morsures + structure + ancrage)."
      - statement: "Ne jamais publier, deployer a distance, pousser vers un depot distant ni effectuer d'achat (les cinq plans)."
        judge_verdict: "tenu"
        evidence: "`git status -sb` rend `## main...origin/main [ahead 167]` et le sommet de `origin/main` reste `1d475f9` : rien n'a ete pousse, aucun deploiement, aucune publication."
      - statement: "Ne jamais modifier `dofus_stuff/**` pour aligner la documentation (les cinq plans)."
        judge_verdict: "tenu"
        evidence: "`git status --porcelain -- dofus_stuff` vide, `git diff --name-only HEAD -- dofus_stuff` vide, et `git log --since=2026-09-12T01:04:14Z -- dofus_stuff` vide : la reprise de ce tour n'a pas touche le produit."
      - statement: "Ne jamais executer `main()`, lancer le solveur, ouvrir une socket ou une connexion reseau depuis un controle (les cinq plans)."
        judge_verdict: "tenu"
        evidence: "Variante `-p no_net` : banniere « 6 pieges armes avant la collecte -> socket.socket, socket.create_connection, socket.socketpair, urllib.request.urlopen, dofus_stuff.cli.main, dofus_stuff.web.__main__.main » ecrite avant la collecte, `250 passed` ; ma propre sonde de rendu a utilise le client de test Flask en processus, un dossier temporaire, hors ligne."
      - statement: "Ne jamais inventer un message pour une famille qui n'en produit pas, ni promettre une duree d'attente que le produit n'expose pas (06-01)."
        judge_verdict: "tenu"
        evidence: "Rejeu de ma propre mesure ce tour-ci : « Base absente ou vide : 10 cite(s), 10 declare(s) / Saisie invalide : 13 / Calcul long : 4 / Clavier inactif : 0 / Resultat pagine : 5 / total cite : 32 | total declare : 32 » — le fichier de page a change ce tour-ci, la table des messages n'a pas derive."
      - statement: "Ne jamais definir un terme que le depot n'emploie pas, ni un terme du vocabulaire de harnais (06-02)."
        judge_verdict: "tenu, avec une reserve declarative"
        evidence: "Les 27 libelles du glossaire sont employes par le fichier cite ; `cible` et `palier` n'apparaissent que sous leurs formes plurielles, le controle comparant des sous-chaines normalisees. Aucun libelle de la liste des termes interdits n'est une entree."
      - statement: "Ne jamais inventer un fichier epingle, ni une limite de lignes, ni un avertissement (06-03)."
        judge_verdict: "tenu"
        evidence: "La liste epinglee est confrontee au disque dans les deux sens : `docs/` contient exactement 8 fichiers `.md`, egaux a la liste (`ls docs/*.md | wc -l` = 8 ce tour-ci), l'ajout d'une page rougit la suite, et l'avertissement destructeur du `README.md` est sur la meme ligne de bloc que la commande."
      - statement: "Ne pas affaiblir un controle existant pour obtenir le vert (06-05)."
        judge_verdict: "tenu"
        evidence: "Le commit de controle (`d2a5dab`) est un ajout pur : `177 insertions(+), 0 deletions(-)` sur `tests/test_docs_depannage.py`, `9 -> 10` tests, aucun `skip`, aucun `xfail`, la garde de cloture du harnais et `tests/test_docs_mutation.py` (14 morsures declarees) inchanges ; la suite entiere ne rapporte aucun test saute."
      - statement: "N'ecrire aucune autre page que `docs/depannage.md`, commits locaux a chemin explicite, sans `git add -A` ni poussee (06-05)."
        judge_verdict: "tenu"
        evidence: "`git log --since=2026-09-12T01:04:14Z --name-only` ne liste que `docs/depannage.md`, `tests/test_docs_depannage.py` et les fichiers de `.planning/` ; `git status --porcelain -- docs` vide ; rien n'a ete pousse."
human_verification:
  - test: "Ouvrir un ecran qui porte un champ de saisie (par exemple l'ecran de recherche), cliquer ailleurs dans la page, puis appuyer sur Entree ; puis ouvrir un ecran sans champ de saisie (etat de la base, version locale) et appuyer sur Entree."
    expected: "Le curseur revient dans le champ apres le clic (le champ reste l'element actif), Entree ne soumet le formulaire que si ce champ est l'element actif, et sur un ecran sans champ, Entree reste sans effet de saisie (seuls les raccourcis agissent)."
    why_human: "Aucun moteur JavaScript ni navigateur n'est disponible hors ligne : les trois assertions de comportement de la rubrique « Clavier inactif » sont lues dans `dofus_stuff/web/static/js/terminal.js:79-88` et `:595-601` et ne sont exercees par aucun controle. Declare comme backstop nomme par la phase (`D-85`), non revendique comme vert — inchange depuis le tour precedent."
---

# Phase 6 — Depannage, glossaire, completude et preuve finale : rapport de verification

**Objectif de la phase (ROADMAP) :** « Le lecteur trouve une reponse en cherchant par message d'erreur
ou par terme, et la documentation livree est prouvee complete, non destructive et gardee par des
controles qui echouent reellement quand une cible derive. »

**Mode :** RE-VERIFICATION du seul ecart `T3` (critere 1), plus le controle de non-regression des
criteres 2 a 5. Les must-haves sont ceux extraits au tour precedent, reutilises tels quels.

## Ligne de verdict

**PASSED — critere 1 ferme, aucune regression.**

L'absolu de portee qui restait rouge a disparu : la rubrique « Resultat pagine » borne desormais la
ligne de statut a **chacune de ses deux surfaces productrices**, nommees (`dofus_stuff/web/routes.py`,
`dofus_stuff/web/static/js/terminal.js`), avec la condition mesuree de chacune, et l'observation
secondaire sur la saisie invalide est corrigee. Le nouveau controle **mord** : je l'ai falsifie moi-meme
sur des copies sacrifiees sous `mktemp -d` (la page d'avant, un absolu reintroduit, la garde du produit
effacee, une garde ajoutee au script) — chacune rougit avec son motif nomme, chacune mesuree verte avant
sa mutation. Aucun des quatre autres criteres n'a regresse.

**Statut du rapport : `human_needed`,** et non `passed`, pour la seule raison qui subsistait au tour
precedent et que ce tour n'a pas changee : un comportement DOM de la rubrique « clavier inactif » est lu
dans le script et n'est exerce par aucun controle hors ligne. La phase l'a declare comme backstop nomme
(`D-85`) ; je ne le revendique pas comme vert, et je ne peux pas le fermer par un controle automatique
sans moteur JavaScript. Ce `human_needed` ne bloque pas le critere 1 : il est la trace honnete d'une
limite declaree, inchangee (voir « Comportement non exerce »).

**Un avertissement est joint au rapport** (section « Observation residuelle », avec sa mesure) : une
clause de la meme phrase reste plus large que le produit — « le corps de l'ecran porte toujours sa ligne
de pagination » est faux de l'ecran de recherche, mesure. Elle ne fait pas partie de l'ecart instruit au
tour precedent, l'ecart est ferme pour la clause qu'il nommait, et je la signale au lieu de l'absorber.

## Re-verification : ce que j'ai re-verifie, et comment

| # | Etape | Mesure de ce tour |
|---|-------|-------------------|
| 1 | La page corrigee est-elle vraie, phrase par phrase ? | Toutes les phrases de la rubrique comparees au code, une par une (tableau ci-dessous) : 7 phrases, 7 verdicts, 1 clause residuelle signalee |
| 2 | Le nouveau controle peut-il echouer ? (falsification) | Page d'avant reconstruite et rejouee : `1 failed, 9 passed`, **5 constats nommes** ; 3 derivees injectees par moi : chacune rouge avec son motif ; page livree : `10 passed` |
| 3 | Non-regression du reste de la phase | Suite entiere `250 passed in 5.87s` (rc=0), variante sans reseau `250 passed in 5.65s`, base intacte, 8 pages epinglees et index intacts, gabarit intact, `dofus_stuff/**` intact, aucun `skip`/`xfail` ajoute |
| 4 | Empreinte de la base autour du tour | `24989696:1788730056843137500:e3793d64cb7939ad1a51837b075b6b95e03d64c878fcb9cc07f86c00bb8fef7b` avant **et** apres toutes mes mesures : identique |

## Critere 1 : les phrases de la page, comparees au produit

Chaque phrase ci-dessous a ete relue **dans les octets de la page livree** (`docs/depannage.md`, 14258
octets, 99 lignes, 99 CRLF, sans BOM) et comparee a l'oracle que j'ai relu moi-meme.

| # | Phrase de la page (ligne livree) | Oracle que j'ai relu | Verdict |
|---|----------------------------------|----------------------|---------|
| S1 | « La pagination a **deux formes**, et le produit ne les ecrit pas au meme endroit. La regle depend de la surface qui ecrit la ligne de statut, et cette page la donne pour chacune : elle nomme a chaque fois le fichier qui la produit. » (`:74`) | la rubrique nomme bien les deux fichiers : `dofus_stuff/web/routes.py` et `dofus_stuff/web/static/js/terminal.js` (mesure : les deux jetons presents dans la rubrique) | ✅ **VRAIE** |
| S2a | « Sur les ecrans que l'application sert elle-meme (`dofus_stuff/web/routes.py`), la ligne de **statut** ne porte le motif de page que lorsque l'ecran compte plus d'une page » (`:75`) | `dofus_stuff/web/routes.py:143-145` : `indicators: list[str] = []` puis `if total > 1:` puis `indicators.append(f"PAGE {page}/{total}")`. Mesure : **1** occurrence de cette garde dans le fichier, **1** occurrence de la composition `PAGE {page}/{total}` (c'est la seule ligne de statut du produit), **3** occurrences de `total > 1` (`:133`, `:137`, `:144` — les deux premieres bornant la navigation, pas la ligne de statut). Re-mesure du rendu : `GET /list?page=1&size=1` rend le statut `PAGE 1/20 — ENTREE=VALIDER`, `GET /sets?page=1&size=1` rend le statut `ENTREE=VALIDER` (page unique, motif absent) | ✅ **VRAIE** |
| S2b | « et le **corps** de l'ecran porte toujours sa ligne de pagination » (`:75`) | `dofus_stuff/web/routes.py:477` et `:543` composent `f"PAGE {page}/{total_pages}` **sans condition** (mesure : 2 occurrences de ce motif, une par ecran de liste). Vrai des deux ecrans dont le corps porte une telle ligne (`GET /list?page=1&size=1` : corps `PAGE 1/20   TAILLE 1   TOTAL EQUIPEMENTS 20` ; `GET /sets?page=1&size=1` : corps `PAGE 1/1   TAILLE 1   TOTAL PANOPLIES 0`). **Faux comme regle des ecrans que l'application sert** : l'ecran de resultats de recherche (`routes.py:325-351`) est pagine (2 pages mesurees) et son corps ne porte aucun motif de pagination | ⚠️ **VRAIE des deux ecrans producteurs, trop large d'un troisieme ecran** → observation residuelle (avertissement, non bloquant, mesure ci-dessous) |
| S3a | « Sur les deux ecrans de sauvegardes, la ligne de **statut** est ecrite par le script (`dofus_stuff/web/static/js/terminal.js`) : elle porte le motif **meme sur une seule page**, et la liste comme le detail affichent donc `PAGE 1/1`. » (`:76`) | `terminal.js:362` `var total = Math.max(1, Math.ceil(all.length / BODY_LINES) \|\| 1);` → `:369-370` `setStatus("PAGE " + page + "/" + total + " — N OUVRIR \| DEL N \| PURGE OUI \| ESC", "info")` ; et `:392` → `:399-400` meme composition pour le detail. `total` est borne a 1 au minimum : sur une page unique, le statut porte `PAGE 1/1`. Mesures : **2** compositions de ce motif, **0** occurrence de `total > 1` dans tout le fichier, **5** occurrences de `Math.max(1, …)` (`:362`, `:363`, `:392`, `:393`, `:514`), et chaque composition est precedee de `setStatus(` (`:369`, `:399`), qui ecrit `statusEl = document.querySelector(".row.status")` (`:11`) | ✅ **VRAIE** |
| S3b | « Leur **corps**, lui, ne porte aucune ligne de pagination. » (`:76`) | Mesure sur tout le fichier : **2** occurrences de `"PAGE "` — les deux seules compositions, adossees a `setStatus(` et donc sur la ligne de statut ; le corps des deux ecrans est ecrit par `renderBodyRows` (`:184`) a partir des lignes de sauvegarde, sans motif de pagination | ✅ **VRAIE** (lecture du script — voir la limite nommee : le JavaScript n'est pas execute) |
| S4 | Ligne de tableau du message `PAGE {page}/{total}` : « sur un ecran que l'application sert, le motif n'apparait que si l'ecran compte plus d'une page ; sur les ecrans de sauvegardes, ecrits par le script, il est la meme sur une seule page » (`:81`) | memes oracles que S2a et S3a | ✅ **VRAIE** |
| S5 | « Les refus de cette rubrique tombent tous **avant** tout travail : aucune recherche, aucun calcul, aucune ecriture. Une ligne de cette rubrique fait exception et le dit elle-meme : `AUCUN RESULTAT.` est ecrit **apres** la recherche, quand elle n'a rien trouve, et il signale seulement que rien ne correspond — ce n'est donc ni un refus, ni une panne. » (`:28`) | `dofus_stuff/web/routes.py:334` `results = catalog.search_items(query, limit=limit)` **avant** l'ecriture, puis `:326-327` le corps reçoit `AUCUN RESULTAT.` et `:350-351` la ligne de statut recoit `AUCUN RESULTAT.` : le message est bien ecrit **apres** la recherche, et l'exception est nommee comme telle au lieu d'etre rangee parmi les refus. La ligne de tableau du message (`:34`) dit deja « ligne de statut **et** corps de l'ecran de resultats, quand rien ne correspond » | ✅ **VRAIE** |

**Mots exclusifs et marques d'absolu de la rubrique :** mesure sur la rubrique « Resultat pagine »
extraite par son titre et normalisee (accents, casse, espaces) — **aucune** de ces marques n'y figure :
`aucun motif a son statut`, `n'ajoute aucun motif`, `ne porte jamais le motif`, `le motif n'apparait
jamais`, `sur n'importe quel ecran`, `quelle que soit la surface`, `quel que soit l'ecran`, `sans
exception de surface`. Le mot `seulement` apparait deux fois dans la page (`:20`, `:28`), jamais dans la
rubrique de la pagination, et aucun des deux emplois n'est contredit par le produit.

## Falsification : le controle peut-il rater ? (mes copies, pas la parole de l'executant)

**La page d'avant, reconstruite octet par octet.** J'ai repris les trois passages corriges depuis
`b791063^` et je les ai reinjectes dans la page livree par ecriture d'octets (jamais `sed -i`, jamais
`read_text`/`write_text`), en preservant le CRLF : resultat **13354 octets, 96 lignes, 96 CRLF** — soit
exactement la taille d'avant annoncee par le commit (`13354 -> 14258 octets`). La copie sacrifiee
contient `docs/`, `tests/`, `dofus_stuff/`, `fetcher.py`, `pyproject.toml`, `GUIDE_WIZARD.md`,
`README.md`, sous `mktemp -d` ; le depot n'est jamais ecrit.

```text
=== COPIE = page livree (doit etre VERTE) ===
..........                                                               [100%]
10 passed in 0.43s

=== COPIE = page d'AVANT (doit etre ROUGE, constats nommes) ===
E  AssertionError: depannage.md : constats sur la portee de la pagination :
   surface de pagination non declaree : la rubrique « Résultat paginé » de depannage.md ne nomme pas
     la surface « application » (dofus_stuff/web/routes.py) ;
   surface de pagination non declaree : la rubrique « Résultat paginé » de depannage.md ne nomme pas
     la surface « sauvegardes » (dofus_stuff/web/static/js/terminal.js) ;
   surface de pagination non declaree : la rubrique « Résultat paginé » de depannage.md ne porte pas
     « aucune ligne de pagination » pour la surface « sauvegardes » ;
   absolu de pagination non borne : la rubrique « Résultat paginé » de depannage.md porte
     « aucun motif a son statut » ;
   absolu de pagination non borne : la rubrique « Résultat paginé » de depannage.md porte
     « n'ajoute aucun motif » ;
   attendu la rubrique nommant les deux producteurs de la ligne de statut et portant la condition de
     chacun, sans aucune marque d'absolu (dofus_stuff/web/routes.py, …/terminal.js, D-19)
1 failed, 9 passed in 0.44s
```

**Le controle echoue donc bien sur la page d'avant, avec 5 constats nommes** (3 de surface, 2 d'absolu) :
la fermeture d'ecart est reelle, et non un vert obtenu par affaiblissement.

**Trois derivees que j'ai injectees moi-meme** (une copie neuve par derivee, chacune mesuree verte,
`10 passed`, avant sa mutation) :

| Derivee injectee | Suite apres mutation | Motif nomme observe (verbatim, extrait) |
|---|---|---|
| Absolu de portee reintroduit dans la rubrique, **les deux surfaces restant nommees** (« Un ecran qui n'a qu'une seule page n'ajoute aucun motif a son statut. ») | `1 failed, 9 passed` | `absolu de pagination non borne : la rubrique « Résultat paginé » de depannage.md porte « aucun motif a son statut »` **et** `… porte « n'ajoute aucun motif »` (2 constats) |
| Garde du produit effacee : `routes.py:144-145` rendu inconditionnel | `2 failed, 8 passed` | `formes de la pagination : le procede de la surface « application » n'est plus mesure dans dofus_stuff/web/routes.py (0 occurrence(s), attendu 1)` — **et** le controle de rendu rougit aussi : `le statut rendu par GET /sets?page=1&size=1 … est « PAGE 1/1 — ENTREE=VALIDER » ; attendu le motif de pagination absent` |
| Garde ajoutee au script : `if (total > 1) setStatus(` sur les **2** compositions de `terminal.js` | `1 failed, 9 passed` | `formes de la pagination : la surface « sauvegardes » porte « total > 1 » dans dofus_stuff/web/static/js/terminal.js` |

Lecture de ces trois mesures : le controle n'est pas un controle de **jetons de la page**. Il est
adosse aux deux fichiers producteurs (une garde perdue, une garde ajoutee, une composition deplacee
rougissent) **et** il rougit sur un absolu reintroduit alors que les noms des fichiers sont toujours la.
La derivee « garde du produit effacee » fait meme rougir le controle comportemental deja livre, sur le
**rendu** (`GET /sets?page=1&size=1`), ce qui donne la preuve que les deux controles se recouvrent sur
l'ecran a page unique.

## Suite entiere, variante sans reseau, empreinte de la base

```text
$ ./.venv/Scripts/python.exe -m pytest -q            # HEAD 8f65bbb, arbre de travail
........................................................................ [ 28%]
........................................................................ [ 57%]
........................................................................ [ 86%]
..................................                                       [100%]
250 passed in 5.87s
code retour = 0        # relance avec -rs : aucun test saute dans toute la suite

$ PYTHONPATH="$PWD/.gsd-tmp" ./.venv/Scripts/python.exe -m pytest -q -p no_net
greffon de preuve 06-04 : 6 pieges armes avant la collecte -> socket.socket, socket.create_connection,
socket.socketpair, urllib.request.urlopen, dofus_stuff.cli.main, dofus_stuff.web.__main__.main
250 passed in 5.65s
```

Empreinte de `.data/dofus.sqlite3`, mesuree en octets et **jamais** ouverte, avant et apres toutes mes
mesures (suite entiere, variante sans reseau, copies de morsure, sonde de rendu) :

```text
$ ./.venv/Scripts/python.exe -c "import hashlib,pathlib;p=pathlib.Path('.data/dofus.sqlite3');b=p.read_bytes();print('%d:%d:%s'%(len(b),p.stat().st_mtime_ns,hashlib.sha256(b).hexdigest()))"
24989696:1788730056843137500:e3793d64cb7939ad1a51837b075b6b95e03d64c878fcb9cc07f86c00bb8fef7b   (avant)
24989696:1788730056843137500:e3793d64cb7939ad1a51837b075b6b95e03d64c878fcb9cc07f86c00bb8fef7b   (apres)
```

Aucune commande de ce tour n'a touche `.data/` ni `.doc-agent/` : ni `db clear`, ni `db sync`, ni `db
status`, ni drop, ni suppression.

## Non-regression des criteres 2 a 5

| Critere du ROADMAP | Verdict | Preuve de ce tour |
|---|---|---|
| 2. « Chaque entree du glossaire est presente et triee, et le sommaire propose un parcours conseille final » | ✅ **VERIFIED, sans regression** | `docs/glossaire.md` et `docs/sommaire.md` n'ont pas ete touches par la reprise (`git log --since=2026-09-12T01:04:14Z --name-only` ne liste, cote livrables, que `docs/depannage.md` et `tests/test_docs_depannage.py`, sur 4 commits depuis ma verification precedente) ; le groupe des modules de garde (completude, glossaire, morsures, structure, ancrage) rend `43 passed in 1.87s` |
| 3. « Les 8 pages epinglees sont toutes livrees … et le sommaire propose un parcours conseille final » | ✅ **VERIFIED, sans regression** | `ls docs/*.md \| wc -l` = **8**, ensemble egal a la liste epinglee ; `tests/test_docs_completude.py` vert ; l'index porte son entree pour la page (`docs/sommaire.md:24` : `\| [Dépannage](depannage.md) \| …`) |
| 4. « Une derive ulterieure doit faire echouer le harnais (preuve de morsure) » | ✅ **VERIFIED, sans regression** | `tests/test_docs_mutation.py` vert (14 morsures declarees, inchange) ; et le nouveau controle a sa propre preuve de morsure, que j'ai refaite moi-meme (3 derivees, 3 rouges nommes) |
| 5. « La verification finale est reproductible : compteur et duree reels, empreinte de la base, suite sans reseau, `git status` rapporte avec son ecart » | ✅ **VERIFIED, sans regression** | `250 passed in 5.87s` (rc=0), variante sans reseau `250 passed in 5.65s` avec la banniere des 6 pieges avant la collecte, empreinte de la base identique, `git status` non masque (les fichiers non suivis de l'hote et la divergence `ahead 163` restent declares tels quels) |

**Gabarit de la page corrigee** (mesure sur les octets, `docs/depannage.md`) :

```text
octets 14258 | lignes 99 | CRLF 99 | BOM False
H1 : ['# Dépannage']                     (unique)
H2 (ordre) : Base absente ou vide, Saisie invalide, Calcul long, Clavier inactif, Résultat paginé, Source de vérité
derniere section : '## Source de vérité' | derniere ligne non vide : '[Retour au sommaire](sommaire.md)'
libelle d'index (docs/sommaire.md:24) : 'Dépannage'  ->  H1 == libelle d'index : True
nombres de quatre chiffres ou plus : 0 | chemins de poste : 0 | liens externes (http) : 0
```

**Perimetre et harnais :** `git status --porcelain -- dofus_stuff` = 0 ligne, `git diff --name-only HEAD
-- dofus_stuff` = 0 ligne, `git log --since=2026-09-12T01:04:14Z -- dofus_stuff` = 0 commit ;
`git status --porcelain -- docs` = 0 ligne (la page corrigee est commitee) ; le commit de controle est un
ajout pur (`177 insertions(+), 0 deletions(-)`, `9 -> 10` tests) ; aucun `skip`, aucun `xfail` introduit
— la suite entiere ne rapporte **aucun** test saute (`-rs`), et les seules occurrences du mot dans
`tests/` sont des commentaires ou des gardes conditionnelles preexistantes dans des fichiers que ce tour
n'a pas touches.

## Observation residuelle (avertissement, avec preuve — non bloquant)

**Ce que la page affirme encore** (`docs/depannage.md:75`, seconde moitie de la phrase) : « le **corps**
de l'ecran porte toujours sa ligne de pagination », enonce pour « les ecrans que l'application sert
elle-meme ».

**Ce que j'ai mesure.** Ma sonde utilise le client de test Flask en processus, un catalogue de 20 objets
construit sous un dossier temporaire, hors ligne, sans serveur et sans toucher `.data/` :

```text
--- GET /list?page=1&size=1
    statut rendu         : 'PAGE 1/20 — ENTREE=VALIDER'
    premiere ligne corps : 'PAGE 1/20   TAILLE 1   TOTAL EQUIPEMENTS 20'
    corps porte un motif PAGE n/n : True
--- GET /sets?page=1&size=1
    statut rendu         : 'ENTREE=VALIDER'
    premiere ligne corps : 'PAGE 1/1   TAILLE 1   TOTAL PANOPLIES 0'
    corps porte un motif PAGE n/n : True
--- GET /search?q=Test|50            (20 resultats, deux pages mesurees : data-body-total = 2)
    statut rendu         : 'PAGE 1/2 — ENTREE=VALIDER'
    premiere ligne corps : 'REQUETE : Test   LIMITE : 50   TROUVES : 20'
    corps porte un motif PAGE n/n : False
```

L'ecran de resultats de recherche est un ecran que l'application sert elle-meme (`routes.py:302-351`) :
son corps est bien **pagine** (`paginate` a `:348`, `data-body-total` = 2, les touches F7/F8), mais il
**ne porte aucune ligne de pagination** — l'information de page passe par la ligne de statut (`:144-145`)
et par les attributs `data-body-page`/`data-body-total` que le gabarit ecrit sur l'element terminal
(`dofus_stuff/web/templates/screen.html:13-14`), jamais par une ligne visible du corps. La phrase dit
donc « toujours » la ou le produit fait « sur les deux ecrans de liste ».

**Pourquoi je ne la classe pas en ecart.** (1) L'ecart instruit au tour precedent et ferme ce tour-ci
portait sur la **ligne de statut** des deux ecrans de sauvegardes : cette clause-la est juste desormais,
et je l'ai verifiee phrase par phrase. (2) La clause du corps est **inchangee** depuis la version que
j'avais acceptee sur ce critere (la formulation d'avant disait deja « le corps de l'ecran, lui, porte
toujours sa ligne de pagination ») : la rouvrir serait re-juger ce que j'ai deja passe, et le plan de
fermeture borne a juste titre ne l'a pas traitee. (3) Le critere 1 du ROADMAP — retrouver chaque
rubrique par le message reellement produit — est tenu (32 messages cites = 32 declares, remesures ce
tour-ci ; les 5 rubriques existent dans l'ordre). (4) Le controle ne peut pas la voir, et la phase le
**declare** comme limite nommee (`ABSOLUS_PAGINATION` est une liste finie et declaree ; « une
generalisation de la page exprimee autrement que par les jetons declares … reste hors d'atteinte du
controle », `06-05-PLAN.md`, `D-85`).

**Ce qui la fermerait, en une clause.** Borner la seconde moitie a la surface dont le corps porte
reellement cette ligne (« sur les deux ecrans de liste, le corps porte toujours sa ligne de pagination »),
ou nommer le troisieme cas comme la page nomme les deux autres (« l'ecran de resultats de recherche, lui,
annonce sa page dans la ligne de statut et n'en ecrit aucune dans son corps »). Un lecteur qui verrait
`PAGE 1/2` au statut d'une recherche, sans ligne de pagination au corps, lirait aujourd'hui la phrase
comme une panne — c'est le meme motif de diagnostic que `T3`, sur un troisieme ecran, et il est mesure.

## Comportement non exerce (inchange depuis le tour precedent)

Le rendu Markdown hors GitHub, l'execution du JavaScript et le comportement du DOM ne sont observes par
aucun controle de ce depot, hors ligne : les trois assertions de comportement de la rubrique « clavier
inactif » (champ marque `autofocus`, refocalisation au clic, touche Entree qui ne soumet que si le champ
est actif) sont **lues** dans `dofus_stuff/web/static/js/terminal.js:79-88` et `:595-601`, et aucun
moteur JavaScript n'est installe pour les exercer. La phase avait declare cette limite (`D-85`,
`06-01-PLAN.md:86`, `06-02-PLAN.md:86`) ; je la reporte telle quelle, non revendiquee comme verte, en
item de verification humaine (voir l'entete du rapport).

## Sources couvertes (ce tour)

- `06-VERIFICATION.md` (tour precedent) — l'ecart `T3` et l'observation secondaire sur la saisie
  invalide : les deux sont fermes, le premier par `b791063` + `d2a5dab`, le second par `b791063`.
- `06-05-PLAN.md` / `06-05-SUMMARY.md` — le contrat de fermeture (`must_haves`, `prohibitions`,
  `key_links`) : tenu, y compris sa clause la plus fragile, « le procede deplace ou une occurrence
  perdue devient un constat portant `formes de la pagination` », que j'ai falsifiee moi-meme.
- Le produit, en lecture seule : `dofus_stuff/web/routes.py` (`:125-160`, `:284-360`, `:470-485`,
  `:535-550`) et `dofus_stuff/web/static/js/terminal.js` (`:11`, `:184`, `:350-402`) ; le gabarit
  `dofus_stuff/web/templates/screen.html` (lecture de `data-body-page`/`data-body-total`).
- Les livrables retouches : `docs/depannage.md` (octets, gabarit, phrases), `tests/test_docs_depannage.py`
  (controle `problemes_pagination`, test `test_pagination_bornee_a_ses_deux_producteurs`, garde de
  cloture du harnais).
- Le reste du harnais, inchange : `tests/test_docs_completude.py`, `tests/test_docs_glossaire.py`,
  `tests/test_docs_mutation.py`, `tests/test_docs_structure.py`, `tests/test_docs_code_anchor.py`.

## Aucune conformite de decision manquante (verify_decisions)

Non rejoue en re-verification bornee : aucun des cinq plans n'a change de decisions d'implementation
depuis le tour precedent hormis le bornage de portee decrit ci-dessus, et la couverture des decisions
`D-19`, `D-69`, `D-85`, `D-88`, `D-97`, `D-98`, `D-102`, `D-103`, `D-104` a ete mesuree au tour
precedent ; ce tour a re-mesure celles que la reprise pouvait casser (`D-19` : les deux surfaces et
leurs deux conditions ; `D-69`/`D-102` : gabarit et octets ; `D-85` : la limite nommee du controle ;
`D-103` : produit en lecture seule ; `D-104` : empreinte de la base).

## Audit qualite des tests (controle de ce tour)

| Fichier de test | Controle lie | Actifs | Sautes | Circulaire | Niveau d'assertion | Verdict |
|---|---|---|---|---|---|---|
| `tests/test_docs_depannage.py` | critere 1 (`AIDE-01`) | 10 | 0 | non | **comportemental** : rend les ecrans par le client de test et compare statut et corps (`test_pagination_a_deux_formes`), et lit les deux fichiers producteurs avec leur nombre d'occurrences mesure (`problemes_pagination`) | OK |
| `tests/test_docs_mutation.py` | critere 4 | 14 morsures declarees | 0 | non (chaque copie est mesuree verte avant mutation) | comportemental (suite rejouee sur copie mutee) | OK |
| `tests/test_docs_completude.py` | criteres 2 et 3 | 8 | 0 | non | valeur (ensemble de `docs/` confronte a la liste epinglee dans les deux sens) | OK |

Tests desactives sur une exigence : **0**. Motifs circulaires : **0** (aucun script de test n'ecrit de
valeur attendue produite par le systeme sous test). Assertions insuffisantes : **0**.

## Advisory (hors contrat, sans preuve deterministe)

Aucun constat hors contrat de ce tour ne manque de preuve deterministe : la seule observation que je
remonte est mesuree (sonde reproductible, sortie verbatim ci-dessus). Rien n'est donc consigne ici.

## Ce que je n'ai pas pu verifier

- **L'execution du JavaScript et le DOM** : aucun moteur ni navigateur hors ligne ; les trois
  assertions de comportement de la rubrique « clavier inactif » restent des lectures du script, et le
  corps rendu des deux ecrans de sauvegardes n'est pas observable — le controle lit `terminal.js`, il ne
  l'execute pas (limite nommee du controle, `06-05-PLAN.md`).
- **Le rendu Markdown hors GitHub** : aucun moteur de rendu installe ; je verifie les octets et la
  structure, pas l'affichage. A noter sans en tirer de conclusion sur la veracite : les quatre phrases de
  la rubrique « Resultat pagine » sont jointes par un CRLF simple (lignes 74 a 77 consecutives), donc
  rendues comme un seul paragraphe a repli automatique ; le plan 06-05 decrivait une jonction par CRLF
  CRLF mais ses propres mesures attendues (99 lignes, 99 CR, 14258 octets) sont exactement celles de la
  page livree. Le fond des phrases est mesure ci-dessus, phrase par phrase.
- **Une reformulation future de la rubrique** : le controle enumere une liste finie et declaree de
  marques d'absolu ; une generalisation formulee autrement lui echappe, et le plan le declare
  (`D-85`). C'est precisement pourquoi l'observation residuelle ci-dessus est signalee au lieu d'etre
  couverte par un vert.
- **La sonde de l'ecran de recherche** est la mienne (client de test Flask, catalogue construit sous un
  dossier temporaire) : elle n'est pas un test du depot. Elle est reproductible avec le script laisse
  dans le repertoire de travail de la session ; je la donne pour ce qu'elle est, une mesure directe du
  rendu, pas un controle du harnais.

---

_Verifie : 2026-09-12T01:57:54Z_
_Verificateur : Claude (gsd-verifier)_
_RE-VERIFICATION du 2026-09-12T01:57:54Z : ecart `T3` ferme, aucune regression, statut `human_needed` pour le comportement DOM non exerce (inchange)._
