---
phase: 01-socle-documentaire-installation-et-harnais-v-rifiable
reviewed: 2026-09-11T10:46:14Z
depth: standard
files_reviewed: 6
files_reviewed_list:
  - README.md
  - docs/installation.md
  - docs/sommaire.md
  - tests/conftest.py
  - tests/test_docs_code_anchor.py
  - tests/test_docs_structure.py
findings:
  critical: 1
  warning: 5
  info: 3
  total: 9
status: issues_found
---

# Phase 01: Code Review Report

**Reviewed:** 2026-09-11T10:46:14Z
**Depth:** standard
**Files Reviewed:** 6
**Status:** issues_found

## Summary

Reviewed the delivered documentation chain (`README.md` → `docs/sommaire.md` → `docs/installation.md`) and the harness that is supposed to keep it true (`tests/conftest.py`, `tests/test_docs_structure.py`, `tests/test_docs_code_anchor.py`), at standard depth.

**The prose is sound.** Every executable claim I could test is true against the real code (see "Claims verified against the product" below) — I found no documentation statement that the code contradicts, no invented default, no wrong option surface in the delivered text. `tests/conftest.py` has no findings.

**The harness bites in the directions it implements, but nine claims it makes are either partial or not falsifiable at all.** The single Critical finding is the one that matters most for this phase's purpose: the web option surface is verified only *parser → page*, never *page → parser*, so an option invented in the documentation keeps the whole suite green — proven by mutation, not asserted. Four Warnings name further mutations that should break a named invariant but do not (unvalidated source-of-truth paths, the `--debug` caveat, fragment anchors, the index equality), and one Warning is a *scheduled* self-inflicted failure: the mutation test hardcodes `glossaire.md`, a filename the roadmap delivers in phase 6.

All mutation experiments ran on `tempfile` copies of the repo tree. `docs/`, `.data/`, and every source file under `dofus_stuff/**` are unchanged (`git status --porcelain -- dofus_stuff` empty; `docs/` untouched). Reference suite on the delivered tree: **157 passed**.

## Narrative Findings (AI reviewer)

### Claims verified against the product (no findings — recorded so they are not re-litigated)

All checks were run with `.venv/Scripts/python.exe`, never with the ambient interpreter, and never writing under `.data/` (a temp `--data-dir` was used for every CLI probe):

- `python fetcher.py --data-dir <tmp> --offline version` on a fresh directory → exit **1**, stderr `Erreur : Base locale vide et --offline : impossible de synchroniser`; the exact string and the `if offline:` guard exist at `dofus_stuff/sync.py:43`. Matches `docs/installation.md` § "Erreurs fréquentes" literally, including the exit code and the `Erreur : ` prefix from `dofus_stuff/cli.py`.
- `python fetcher.py --offline db status` → exit **0**, creates `dofus.sqlite3`, prints `Fichier` / `Version jeu` / `Dernier check` / `Entrées` — exactly the four characteristics the page promises for the "chemin minimal".
- `python fetcher.py db status --offline` → exit **2**, stderr line `fetcher.py: error: unrecognized arguments: --offline`. The page quotes this line and this exit code correctly.
- `dofus_stuff/web/__main__.py::build_parser().parse_args([])` yields `host=127.0.0.1`, `port=5000`; the page's `http://127.0.0.1:5000` is therefore the parser's own default. The page's options table lists exactly the parser's surface (`--offline` + auto `--no-offline`, `--online`, `--data-dir`, `--timeout`, `--host`, `--port`) plus `--debug`; `--online` ≡ `--no-offline` matches `offline = False if args.online else args.offline`.
- Keyboard table: `dofus_stuff/web/static/js/terminal.js` binds `F3`, `Escape`, `F7`, `F8`, `PageUp`, `PageDown` (lines 551–592) and refocuses the input on any click (lines 82–89); the labels `Quitter`/`Retour`/`Precedent`/`Page prec`/`Suivant`/`Page suiv` exist in `dofus_stuff/web/routes.py` (lines 67–68, 138–139) and the main menu carries only `fkeys=[("F3", "Quitter")]` (line 208) — the page's "construite dynamiquement" paragraph is accurate.
- All seven paths in the page's `## Source de vérité` block, `README.md`'s `[Sommaire de la documentation](docs/sommaire.md)` link, and the seven-theme plain-text "Parcours conseillé" (mandated by `01-01-PLAN.md:132`, so not drift) check out. `docs/sommaire.md` carries no link other than its single index entry, as D-05/D-06 require.

### Method note

Each mutation below was applied to a `tempfile` copy of the whole working tree (`README.md docs tests pyproject.toml fetcher.py dofus_stuff`), and then the *entire* suite was run in that copy, so "the suite stays green" means all 157 tests, not a subset. Where only the pure invariant functions were needed, they were imported directly and called on mutated copies of `docs/`.

## Critical Issues

### CR-01: The web option surface is never checked in the page → parser direction; two tests are named as if it were

**File:** `tests/test_docs_code_anchor.py:173` (`test_documented_entry_options_parse`), `tests/test_docs_code_anchor.py:186` (`test_documented_entry_options_appear_in_help`), constants at `tests/test_docs_code_anchor.py:30` and `:42`

**Issue:** `test_documented_entry_options_parse`'s docstring claims *"Chaque option d'entrée web **de la page** est acceptée par le parseur réel (D-14)"*, and `01-04-SUMMARY.md:20` claims the seven options are *"verifiees dans les deux sens"*. Neither test takes the `docs_dir` fixture, never opens `docs/installation.md`, and iterates a hardcoded list (`SONDES_WEB`). Only the opposite direction exists: `test_documented_entry_options_are_documented` (`:197`) checks that the parser's seven options appear somewhere in the page. So an option that the page documents but the parser does not have is invisible to the suite — no page mutation can turn these two tests red.

**Concrete failure scenario:** a maintainer rewrites the options table in `docs/installation.md:87-95` and adds a row `| `--serve` | sert la racine statique |`, or changes `--timeout`'s documented default to `30`. The reader then runs `python -m dofus_stuff.web --serve` and gets argparse exit 2. This is exactly the "invented option surface / invented default" drift class success criterion 4 exists to refuse, and the module named "ancrage ... sur le code réel" does not see it.

**Proof (mutation that should break it but does not):** add `| `--serve` | option inventee, absente du parseur |` to the options table of `docs/installation.md` in the throwaway tree → **157 passed**, no failure. (The `01-04-SUMMARY.md:144` mutation battery lists "option web inconnue" as refused, but that drift was injected by rebinding `SONDES_WEB` in-process — the parser direction, not the page direction.)

**Fix:** derive the page's own option list and assert set equality in both directions, so the table becomes authoritative:

```python
OPTION_PAGE = re.compile(r"`(--[a-z][a-z-]*)`")
OPTIONS_A_VALEUR = ("--data-dir", "--timeout", "--host", "--port")

def test_documented_entry_options_are_accepted_by_parser(docs_dir: Path) -> None:
    """Chaque option citee par le tableau de la page est acceptee par le parseur reel (D-14)."""
    texte = (docs_dir / PAGE).read_text(encoding="utf-8")
    corps = _section(texte, "## Lancement de l'interface web")
    citees = set(OPTION_PAGE.findall(corps)) | {OPTION_PAGE.findall(texte)[0]}  # + --debug si hors section
    parser = build_parser()
    for option in sorted(citees):
        argv = [option, "x"] if option in OPTIONS_A_VALEUR else [option]
        try:
            parser.parse_args(argv)
        except SystemExit:
            raise AssertionError(
                f"{PAGE} : option « {option} » citee par la page mais refusee par "
                f"{SOURCE_WEB}::build_parser().parse_args() ; attendu une option reelle"
            ) from None
    assert citees == set(OPTIONS_WEB) | {JETON_DEBUG}, (
        f"{PAGE} : surface citee {sorted(citees)} differente de la surface reelle "
        f"{sorted(set(OPTIONS_WEB) | {JETON_DEBUG})} ; attendu egalite des deux surfaces"
    )
```

## Warnings

### WR-01: The "Source de vérité" path invariant ignores `.js` paths, and the page's second source block is not scanned at all

**File:** `tests/test_docs_code_anchor.py:23` (`CHEMIN_CITE`), applied at `tests/test_docs_code_anchor.py:106-110`

**Issue:** `CHEMIN_CITE = re.compile(r"`(?P<chemin>[\w./-]+\.(?:py|toml))`")` only matches `.py` and `.toml`, and `test_sources_de_verite_exist` applies it to the `## Source de vérité` section body only. Two of the page's nine source citations therefore fall outside the invariant while the docstring still claims *"Chaque chemin cité par le bloc « Source de vérité » de la page existe sur disque"*: the `.js` entry at `docs/installation.md:139` (one of that block's seven entries), and both paths of the `Sources :` line in the keyboard section at `docs/installation.md:71` (that line is outside `TITRE_SOURCE`, so even its `.py` path is unchecked).

**Concrete failure scenario:** a refactor moves the key handling to `dofus_stuff/web/static/js/clavier.js`; the page's block keeps pointing at `static/js/terminal.js` and the reader follows a citation to a file that no longer exists. The suite stays green.

**Proof (mutations that should break it but do not, run separately):**
1. `- `dofus_stuff/web/static/js/terminal.js` : …` → `terminal-inexistant.js` in `## Source de vérité` → **157 passed**.
2. `Sources : `dofus_stuff/web/routes.py` … et `dofus_stuff/web/static/js/terminal.js`` (`docs/installation.md:71`) → both replaced by `routes-inexistant.py` / `terminal-inexistant.js` → **157 passed**.

**Fix:** widen the pattern and scan the whole page (the non-empty guard at `:111` still protects against a regex that stops matching):

```python
CHEMIN_CITE = re.compile(r"`(?P<chemin>[\w./-]+\.(?:py|toml|js|md|json|sql))`")
# dans test_sources_de_verite_exist : analyser `texte` entier, et garder
# l'assertion chemins non vide sur le bloc « Source de vérité » comme garde-fou.
```

### WR-02: The `--debug` caveat rule does not cover text before the first `##`, so `--debug` can be cited with no development caveat at all

**File:** `tests/test_docs_code_anchor.py:207-214` (loop over `_sections`, defined at `:71`)

**Issue:** the rule "a section citing `--debug` must also say `developpement`" is evaluated per `## ` section. `_sections` starts at the first `## ` match, so the H1 preamble is in no section and is never inspected. The rule is stated as a global safety rule (T-01-03, "`--debug` n'est accepté comme documenté que s'il est qualifié de réservé au développement"), but its scope is only the post-heading body.

**Concrete failure scenario:** a maintainer promotes the `--debug` sentence (`docs/installation.md:97`) into the page intro ("Passer `--debug` pour déboguer") and drops the "réservée au développement" wording. A reader enables Flask's debug server — the exact elevation-of-privilege surface T-01-03 is about — with the suite green.

**Proof (mutation that should break it but does not):** delete `docs/installation.md:97`, and insert `L'option `--debug` active le serveur de debogage Flask.` immediately before the first `## ` (the preamble), in a throwaway tree → **157 passed**; `test_documented_entry_options_are_documented` called directly on the mutated copy also passes.

**Fix:** parse the preamble as its own section and report it by name:

```python
def _sections(texte: str) -> list[tuple[str, str]]:
    premier = TITRE_H2.search(texte)
    entete = [(None, texte[: premier.start()] if premier else texte)]
    ...  # puis les sections existantes
# dans la boucle : titre_affiche = titre or "preambule"
```

### WR-03: The anchor ban only recognises targets that *start* with `#`; `page.md#ancre` is misdiagnosed as a dead link

**File:** `tests/test_docs_structure.py:155` (inside `test_no_anchor_or_absolute_links`), same defect at `tests/test_docs_structure.py:51` (inside `problemes_liens`)

**Issue:** the invariant is documented as *"Aucune cible ne porte d'ancre, de chemin absolu, d'antislash ni de schéma file:// (D-01, T-01-04)"*, but the code only tests `cible.startswith("#")`. A target that carries a fragment after a path — the common Markdown form `installation.md#prerequis` — is not recognised as an anchor and falls through to path resolution, where it fails as a missing file. The anchor rule is therefore never the reported cause.

**Concrete failure scenario:** someone links to a subsection from the sommaire. The maintainer sees three failures saying `lien mort vers installation.md#prerequis` / `cible listee absente sur disque : installation.md#prerequis` / `page non listee` and concludes the page is missing, not that anchors are forbidden by D-01.

**Proof (mutation that should break it but does not):** `docs/sommaire.md`: `[Installation](installation.md)` → `[Installation](installation.md#prerequis)`.
- `test_no_anchor_or_absolute_links` (the test whose docstring is the anchor rule) → **1 passed**.
- Full suite → 5 failed, none of them for the anchor rule: `test_sommaire_lists_every_document`, `test_sommaire_links_resolve`, `test_all_relative_links_resolve` (`lien mort` / `cible listee absente`), `test_h1_matches_sommaire_entry` and `test_mutation_detecte_les_trois_derives` (knock-on).

**Fix:** test for `#` anywhere in a local target, and `continue` after reporting so the same target is not also reported as a dead link; apply the same change at `:51`:

```python
elif "#" in cible:
    problemes.append(
        f"{nom} : ancre interdite : {cible} ; attendu un lien de fichier a "
        f"fichier vers une page de {docs_dir.name}/ (T-01-04)"
    )
    continue
```

### WR-04: `problemes_index` compares index *target strings* with page *basenames* while page discovery is recursive — a nested page passes silently, and listing it correctly is impossible

**File:** `tests/test_docs_structure.py:92-93` (comparison), `tests/test_docs_structure.py:28` (`docs_dir.rglob("*.md")`)

**Issue:** `_pages` recurses (`rglob`), but `problemes_index` builds `pages = {page.name …}`, so it compares a flat set of basenames against the raw targets found in `sommaire.md`. The declared invariant is set equality between the sommaire's targets and the pages present under `docs/` (SOMM-02, D-06). Two consequences, both proven below: a nested page whose basename is already listed is invisible, and a nested page with a new basename can never be made green — `problemes_index` demands the target string equals the basename, `problemes_liens` demands the target resolve from the sommaire, and the two demands are contradictory.

**Concrete failure scenarios:**
- *False pass:* `docs/sub/installation.md` is added (e.g. an English mirror or a per-version copy) and never listed in the sommaire → all five invariant functions report nothing; the full suite is green.
- *Unsatisfiable:* `docs/sub/glossaire.md` is added and the sommaire gains its real, correct entry `| [Glossaire](sub/glossaire.md) | … |` → 3 failures, including `docs/sommaire.md : cible listee absente sur disque : sub/glossaire.md` **and** `glossaire.md : page non listee dans docs/sommaire.md ; attendu une ligne d'index pointant vers glossaire.md`. The suggested repair (point at `glossaire.md`) would create a dead link, and `problemes_liens` would reject it.

**Proof (full-suite runs on throwaway trees):**
- `docs/sub/installation.md` with H1 `# Installation` and `[Retour au sommaire](../sommaire.md)` → **157 passed**.
- `docs/sub/glossaire.md` (H1 `# Glossaire`, back link `../sommaire.md`) listed as `sub/glossaire.md` → **3 failed, 154 passed**, messages quoted above.

Note this is latent rather than active: `01-RESEARCH.md:202` fixes the convention "aucun sous-dossier sous `docs/`", which is why the delivered tree is green. The defect is that the module's own discovery is recursive while its comparison is flat, so the two invariants in the same file disagree about what a valid layout is.

**Fix:** compare the page's path relative to `docs/`, and ignore external targets (see IN-01), which makes the three functions coherent:

```python
cibles = {c for c in LINK.findall(sommaire.read_text(encoding="utf-8"))
          if not c.startswith(LIENS_EXTERNES)}
pages = {page.relative_to(docs_dir).as_posix()
         for page in _pages(docs_dir) if page.name != "sommaire.md"}
```

### WR-05: The mutation test hardcodes `glossaire.md`, a filename the roadmap delivers in phase 6 — a guaranteed self-inflicted red

**File:** `tests/test_docs_structure.py:536` (injected copy page), `tests/test_docs_structure.py:540` (assertion), `tests/test_docs_structure.py:570` (delivered-tree assertion)

**Issue:** the drift-(b) fixture injects `(copie / "glossaire.md")` and asserts that `problemes_index` names it, then asserts `not (docs_dir / "glossaire.md").exists()` on the delivered tree. `docs/glossaire.md` is a *planned deliverable*: `ROADMAP.md:184` ("`docs/glossaire.md` définit le vocabulaire…"), `ROADMAP.md:195` ("Rédiger `docs/glossaire.md`, son entrée d'index…"), and `ARCHITECTURE.md:112/148` all pin that exact path. When phase 6 lands, the copy inherits a real `glossaire.md` that *is* listed in the sommaire, so the injected page is no longer unlisted and the drift-(b) assertion fails; the run stops before `:570`, whose assertion has the same problem (it asserts a delivered file must not exist).

**Concrete failure scenario:** phase 6 adds `docs/glossaire.md` + its index entry. `test_mutation_detecte_les_trois_derives` fails with *"la page glossaire.md non listee dans sommaire.md n'est pas detectee par problemes_index()"* — a message that is now false, since the page is listed — and the harness's proof-of-bite test is red for a reason unrelated to any drift. A future maintainer either deletes the page name or the test's credibility, and the harness loses its demonstration.

**Proof (phase 6 simulated in a throwaway tree):** add `docs/glossaire.md` (H1 `# Glossaire`, ≥300 chars, `[Retour au sommaire](sommaire.md)`) plus its index row `| [Glossaire](glossaire.md) | … |` → **1 failed, 156 passed**: `FAILED tests/test_docs_structure.py::test_mutation_detecte_les_trois_derives - AssertionError: copie de docs/ : la page glossaire.md non listee dans sommaire.md n'est pas detectee par problemes_index()`. The later assertion at `:570` fails on the same tree (the file exists), it is simply not reached.

**Fix:** inject a page name that cannot collide with a planned deliverable, and derive both messages from one constant:

```python
PAGE_INJECTEE = "page-injectee-mutation.md"
...
(copie / PAGE_INJECTEE).write_text(f"# Page injectee\r\n\r\n{texte_court}\r\n", encoding="utf-8")
assert any(PAGE_INJECTEE in probleme for probleme in index), (...)
...
assert not (docs_dir / PAGE_INJECTEE).exists(), (...)
```

## Info

### IN-01: An external link placed in the sommaire is reported as a missing page

**File:** `tests/test_docs_structure.py:92-100`

**Issue:** `cibles` is built from *all* link targets of `sommaire.md`, including the external ones that `problemes_liens` (`:51`) and `test_no_anchor_or_absolute_links` (`:153`) explicitly bless. An external citation added to the index page therefore produces `docs/sommaire.md : cible listee absente sur disque : https://dofusdu.de/ ; attendu une page presente sous docs/` — a wrong diagnosis (D-06 forbids extra targets there, but nothing is missing from disk — verified on a mutated copy). `pages_listees` (`:314`) has the same blind spot: an external link's label joins the duplicate-label check of `test_sommaire_index_labels_are_unique`.

**Fix:** filter `LIENS_EXTERNES` when building `cibles` (see the WR-04 snippet), and keep the message for genuinely absent internal pages only.

### IN-02: A UTF-8 BOM produces a misleading "0 titre(s) H1" failure

**File:** `tests/test_docs_structure.py:309` (`_lire_page`), consumed by `problemes_h1` (`:325`)

**Issue:** `read_text(encoding="utf-8")` does not strip a BOM, so a page saved by a Windows editor with a UTF-8 BOM decodes successfully (the "UTF-8 strict" guard is satisfied) but its first line reads `\ufeff# Installation`, which `H1 = re.compile(r"^#\s+…", re.MULTILINE)` does not match. Verified on a copy with a BOM prepended to `docs/installation.md`: `problemes_h1` reports `docs/installation.md : 0 titre(s) H1 dans …` while `test_pages_have_back_link` and `test_documents_are_utf8_and_not_drafts` still pass. The failure is real (so the harness does bite) but it names a symptom the file does not have and points the maintainer at the wrong section.

**Fix:** read pages with `encoding="utf-8-sig"` (or strip `"\ufeff"` right after reading) and, when a BOM is present, say so in the message.

### IN-03: `test_docs_code_anchor.py` raises raw `FileNotFoundError` instead of the named failure used by its sibling module

**File:** `tests/test_docs_code_anchor.py:106`, `:123`, `:155`, `:197`, `:217` (all `(docs_dir / PAGE).read_text(encoding="utf-8")`)

**Issue:** `test_docs_structure.py` implements D-13 explicitly — `_page` (`:203`) and `_sommaire_absent` (`:31`) turn a missing page into a readable, named expectation. The anchor module does not: with `docs/installation.md` deleted, five tests fail with a bare `FileNotFoundError: [Errno 2] No such file or directory: …docs\installation.md` traceback while the structure module reports `docs/sommaire.md : lien mort vers installation.md ; cible attendue sur disque sous …` (verified: 11 failed, 146 passed over the full suite; the five tracebacks come from this module).

**Fix:** reuse the same pattern — a `_page_ou_absent(docs_dir)` helper returning the path plus a named problem, asserted before any `read_text`, so every failure cites `installation.md` and the expectation.
