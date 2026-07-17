"""Routes Flask — écrans terminal stuff-machine."""

from __future__ import annotations

import time
from typing import Any

from flask import (
    Blueprint,
    current_app,
    flash,
    get_flashed_messages,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from dofus_stuff.catalog import format_item_summary
from dofus_stuff.cli import collect_self_test_checks
from dofus_stuff.database import Database
from dofus_stuff.optimize.api import format_optimize_result_lines, optimize_stuff
from dofus_stuff.sync import ensure_up_to_date
from dofus_stuff.web import get_catalog, reload_catalog
from dofus_stuff.web.optimize_wizard import (
    SESSION_WIZARD_EDIT,
    STEP_TITLES,
    WIZARD_STEPS,
    apply_items_input,
    apply_option_value,
    apply_options_input,
    apply_slots_input,
    apply_stat_edit,
    body_items,
    body_options,
    body_recap,
    body_slots,
    body_stat_list,
    load_wizard_spec,
    next_step,
    prev_step,
    reset_wizard,
    save_wizard_spec,
    spec_to_request,
    stat_names_for_step,
)
from dofus_stuff.web.screens import (
    BODY_LINES,
    COLS,
    format_fkey_bar,
    header_line,
    pad_lines,
    paginate,
    separator,
    table_row,
    wrap_lines,
)

bp = Blueprint("terminal", __name__)

DEFAULT_FKEYS = [
    ("F3", "Quitter"),
    ("F12", "Retour"),
]


def _clock() -> str:
    return time.strftime("%Y-%m-%d %H:%M:%S")


def _status_from_flashes() -> tuple[str, str]:
    """Récupère le dernier flash : (texte, kind) où kind in info|error."""
    pairs = get_flashed_messages(with_categories=True)
    if not pairs:
        return "", "info"
    category, message = pairs[-1]
    kind = "error" if category == "error" else "info"
    return str(message), kind


def _screen(
    *,
    pgm: str,
    title: str,
    body_lines: list[str],
    fkeys: list[tuple[str, str]] | None = None,
    input_label: str | None = None,
    input_name: str = "selection",
    input_value: str = "",
    input_maxlength: int = 40,
    status: str = "",
    status_kind: str = "info",
    form_action: str | None = None,
    form_method: str = "post",
    body_page: int = 1,
    body_total_pages: int = 1,
    nav_base: str | None = None,
    f7_url: str | None = None,
    f8_url: str | None = None,
    mode: str = "",
    stuff_payload: Any = None,
    extra: dict[str, Any] | None = None,
) -> str:
    flash_status, flash_kind = _status_from_flashes()
    if flash_status and not status:
        status = flash_status
        status_kind = flash_kind

    # Pagination automatique si le corps dépasse la zone visible
    page = max(1, body_page)
    total = max(1, body_total_pages)
    lines = list(body_lines)
    if len(lines) > BODY_LINES:
        if total <= 1:
            page = max(1, int(request.args.get("page", page)))
        lines, page, total = paginate(lines, page=page, page_size=BODY_LINES)

    resolved_nav = nav_base
    if extra and extra.get("nav_base"):
        resolved_nav = str(extra["nav_base"])
    if total > 1 and not resolved_nav:
        resolved_nav = request.path

    keys = list(fkeys or DEFAULT_FKEYS)
    if total > 1 or f7_url or f8_url:
        key_ids = {k for k, _ in keys}
        if "F7" not in key_ids:
            keys.insert(0, ("F7", "Precedent"))
        if "F8" not in key_ids:
            keys.insert(1, ("F8", "Suivant"))

    if total > 1 and not status:
        status = f"PAGE {page}/{total}"
        status_kind = "info"

    header = header_line(pgm, title, _clock())
    body = pad_lines(lines, BODY_LINES, COLS)
    extra_kwargs = dict(extra or {})
    extra_kwargs.pop("nav_base", None)
    return render_template(
        "screen.html",
        cols=COLS,
        header=header,
        separator=separator(),
        body_lines=body,
        status=status[:COLS],
        status_kind=status_kind,
        fkey_bar=format_fkey_bar(keys),
        fkeys=keys,
        input_label=input_label,
        input_name=input_name,
        input_value=input_value,
        input_maxlength=input_maxlength,
        form_action=form_action or request.path,
        form_method=form_method,
        body_page=page,
        body_total_pages=total,
        nav_base=resolved_nav or "",
        f7_url=f7_url or "",
        f8_url=f8_url or "",
        mode=mode,
        stuff_payload=stuff_payload,
        pgm=pgm,
        title=title,
        **extra_kwargs,
    )


@bp.get("/")
def menu() -> str:
    body = [
        "1. RECHERCHE D'OBJETS",
        "2. DETAIL EQUIPEMENT (PAR ID)",
        "3. LISTE DES EQUIPEMENTS",
        "4. VERSION LOCALE",
        "5. SELF-TEST",
        "6. GESTION DE LA BASE",
        "7. OPTIMISATION DE STUFF",
        "8. STUFFS SAUVEGARDES",
        "",
        "SELECTIONNEZ UNE OPTION ET APPUYEZ SUR ENTREE :",
    ]
    return _screen(
        pgm="MNU-01",
        title="** STUFF-MACHINE - MENU PRINCIPAL **",
        body_lines=body,
        input_label="",
        input_name="selection",
        input_maxlength=1,
        fkeys=[("F3", "Quitter")],
        form_action=url_for("terminal.menu_post"),
    )


@bp.post("/")
def menu_post() -> Any:
    choice = (request.form.get("selection") or "").strip()
    if choice == "7":
        reset_wizard(session)
        return redirect(url_for("terminal.optimize_wizard", step="slots"))
    if choice == "8":
        return redirect(url_for("terminal.saves"))
    routes = {
        "1": "terminal.search",
        "2": "terminal.item_form",
        "3": "terminal.list_items",
        "4": "terminal.version",
        "5": "terminal.self_test",
        "6": "terminal.db_menu",
    }
    if choice in routes:
        return redirect(url_for(routes[choice]))
    flash("OPTION INVALIDE — SAISIR 1 A 8", "error")
    return redirect(url_for("terminal.menu"))


@bp.get("/quit")
def quit_screen() -> str:
    return _screen(
        pgm="END-01",
        title="** FIN DE SESSION **",
        body_lines=[
            "SESSION TERMINEE.",
            "",
            "VOUS POUVEZ FERMER CET ONGLET",
            "OU REVENIR AU MENU (F12).",
        ],
        fkeys=[("F12", "Menu")],
        form_action=url_for("terminal.menu"),
        form_method="get",
        input_label=None,
    )


@bp.route("/search", methods=["GET", "POST"])
def search() -> Any:
    if request.method == "GET" and "q" not in request.args:
        return _screen(
            pgm="SRC-01",
            title="** RECHERCHE D'OBJETS **",
            body_lines=[
                "SAISIR UN TERME DE RECHERCHE (SENSIBLE A LA CASSE).",
                "",
                "LIMITE PAR DEFAUT : 10 RESULTATS.",
                "SYNTAXE OPTIONNELLE : terme|/limite",
                "EXEMPLE : Cape|20",
            ],
            input_label="RECHERCHE",
            input_name="query",
            input_maxlength=60,
            form_action=url_for("terminal.search"),
        )

    raw = (request.form.get("query") or request.args.get("q") or "").strip()
    if not raw:
        flash("SAISIE REQUISE", "error")
        return redirect(url_for("terminal.search"))

    limit = 10
    query = raw
    if "|" in raw:
        parts = raw.split("|", 1)
        query = parts[0].strip()
        try:
            limit = max(1, int(parts[1].strip()))
        except ValueError:
            flash("LIMITE INVALIDE", "error")
            return redirect(url_for("terminal.search"))

    catalog = get_catalog()
    results = catalog.search_items(query, limit=limit)
    page = max(1, int(request.args.get("page", 1)))

    lines: list[str] = [f"REQUETE : {query}   LIMITE : {limit}   TROUVES : {len(results)}", ""]
    if not results:
        lines.append("AUCUN RESULTAT.")
    else:
        lines.append(table_row([("ID", 8), ("NIV", 5), ("NOM", 50), ("TYPE", 30)]))
        lines.append(separator(char="."))
        for item in results:
            item_type = item.get("type")
            type_name = item_type.get("name", "?") if isinstance(item_type, dict) else "?"
            lines.append(
                table_row(
                    [
                        (str(item.get("ankama_id", "?")), 8),
                        (str(item.get("level", "?")), 5),
                        (str(item.get("name", "?")), 50),
                        (str(type_name), 30),
                    ]
                )
            )
        lines.append("")
        lines.append("POUR VOIR UN DETAIL : OPTION 2 DU MENU (ID ANKAMA).")

    slice_lines, page, total = paginate(lines, page=page, page_size=BODY_LINES)
    status = ""
    if not results:
        status = "AUCUN RESULTAT."
    return _screen(
        pgm="SRC-02",
        title="** RESULTATS DE RECHERCHE **",
        body_lines=slice_lines,
        status=status,
        body_page=page,
        body_total_pages=total,
        fkeys=[("F7", "Precedent"), ("F8", "Suivant"), ("F12", "Retour")],
        form_action=url_for("terminal.search", q=query, page=page),
        form_method="get",
        input_label=None,
        extra={"nav_base": url_for("terminal.search", q=query)},
    )


@bp.route("/item", methods=["GET", "POST"])
def item_form() -> Any:
    if request.method == "GET" and "id" not in request.args:
        return _screen(
            pgm="ITM-01",
            title="** DETAIL EQUIPEMENT **",
            body_lines=[
                "SAISIR L'IDENTIFIANT ANKAMA DE L'EQUIPEMENT.",
                "",
                "EXEMPLE : 44  (Epee de Boisaille)",
            ],
            input_label="ANKAMA_ID",
            input_name="ankama_id",
            input_maxlength=12,
            form_action=url_for("terminal.item_form"),
        )

    raw = (request.form.get("ankama_id") or request.args.get("id") or "").strip()
    try:
        ankama_id = int(raw)
    except ValueError:
        flash("ID INVALIDE — ENTIER ATTENDU", "error")
        return redirect(url_for("terminal.item_form"))

    page = max(1, int(request.args.get("page", 1)))
    catalog = get_catalog()
    try:
        item = catalog.get_equipment(ankama_id)
    except KeyError as exc:
        flash(str(exc).upper(), "error")
        return redirect(url_for("terminal.item_form"))

    text = format_item_summary(item, detailed=True, catalog=catalog)
    lines = wrap_lines(text.splitlines(), COLS)
    slice_lines, page, total = paginate(lines, page=page, page_size=BODY_LINES)
    return _screen(
        pgm="ITM-02",
        title=f"** ITEM #{ankama_id} **",
        body_lines=slice_lines,
        body_page=page,
        body_total_pages=total,
        fkeys=[("F7", "Precedent"), ("F8", "Suivant"), ("F12", "Retour")],
        form_action=url_for("terminal.item_form", id=ankama_id, page=page),
        form_method="get",
        input_label=None,
        extra={"nav_base": url_for("terminal.item_form", id=ankama_id)},
    )


@bp.route("/list", methods=["GET", "POST"])
def list_items() -> Any:
    page = max(1, int(request.args.get("page", 1)))
    size = max(1, min(18, int(request.args.get("size", 10))))

    if request.method == "POST":
        raw = (request.form.get("ankama_id") or "").strip()
        if not raw:
            flash("SAISIE REQUISE", "error")
            return redirect(url_for("terminal.list_items", page=page, size=size))
        try:
            ankama_id = int(raw)
        except ValueError:
            flash("ID INVALIDE — ENTIER ATTENDU", "error")
            return redirect(url_for("terminal.list_items", page=page, size=size))
        return redirect(url_for("terminal.item_form", id=ankama_id))

    catalog = get_catalog()
    page_data = catalog.list_equipment_page(page=page, page_size=size)
    items = page_data.get("items", [])
    total = int(page_data.get("total", 0))
    total_pages = max(1, (total + size - 1) // size) if total else 1

    lines: list[str] = [
        f"PAGE {page}/{total_pages}   TAILLE {size}   TOTAL EQUIPEMENTS {total}",
        "",
        table_row([("ID", 8), ("NIV", 5), ("NOM", 55), ("TYPE", 28)]),
        separator(char="."),
    ]
    if not isinstance(items, list) or not items:
        lines.append("AUCUN OBJET SUR CETTE PAGE.")
    else:
        for item in items:
            if not isinstance(item, dict):
                continue
            item_type = item.get("type")
            type_name = item_type.get("name", "?") if isinstance(item_type, dict) else "?"
            lines.append(
                table_row(
                    [
                        (str(item.get("ankama_id", "?")), 8),
                        (str(item.get("level", "?")), 5),
                        (str(item.get("name", "?")), 55),
                        (str(type_name), 28),
                    ]
                )
            )
        lines.append("")
        lines.append("SAISIR UN ID ANKAMA POUR AFFICHER LE DETAIL.")

    return _screen(
        pgm="LST-01",
        title="** LISTE DES EQUIPEMENTS **",
        body_lines=lines,
        body_page=page,
        body_total_pages=total_pages,
        fkeys=[("F7", "Precedent"), ("F8", "Suivant"), ("F12", "Retour")],
        form_action=url_for("terminal.list_items", page=page, size=size),
        form_method="post",
        input_label="ANKAMA_ID",
        input_name="ankama_id",
        input_maxlength=12,
        extra={"nav_base": url_for("terminal.list_items", size=size)},
    )


@bp.get("/version")
def version() -> str:
    catalog = get_catalog()
    ver = catalog.version
    if ver is None:
        body = ["ERREUR : AUCUNE VERSION EN BASE."]
        status, kind = "AUCUNE VERSION EN BASE", "error"
    else:
        body = [
            f"VERSION DOFUS (LOCALE) : {ver}",
            "",
            f"ENTREES EN MEMOIRE : {len(catalog.items)}",
            f"DATA DIR : {current_app.config['DATA_DIR']}",
        ]
        status, kind = f"VERSION {ver}", "info"
    return _screen(
        pgm="VER-01",
        title="** VERSION LOCALE **",
        body_lines=body,
        status=status,
        status_kind=kind,
        fkeys=[("F12", "Retour")],
        input_label=None,
        form_method="get",
        form_action=url_for("terminal.menu"),
    )


@bp.get("/self-test")
def self_test() -> str:
    catalog = get_catalog()
    checks = collect_self_test_checks(catalog)
    lines = ["RESULTATS SELF-TEST :", ""]
    failed = 0
    for label, ok in checks:
        mark = "OK" if ok else "ECHEC"
        lines.append(f"[{mark}] {label}")
        if not ok:
            failed += 1
    lines.append("")
    if failed:
        lines.append(f"ECHEC : {failed} CONTROLE(S)")
        status, kind = f"{failed} CONTROLE(S) EN ECHEC", "error"
    else:
        lines.append("TOUS LES CONTROLES SONT OK.")
        status, kind = "SELF-TEST OK", "info"

    page = max(1, int(request.args.get("page", 1)))
    slice_lines, page, total = paginate(lines, page=page, page_size=BODY_LINES)
    return _screen(
        pgm="TST-01",
        title="** SELF-TEST **",
        body_lines=slice_lines,
        status=status,
        status_kind=kind,
        body_page=page,
        body_total_pages=total,
        fkeys=[("F7", "Precedent"), ("F8", "Suivant"), ("F12", "Retour")],
        input_label=None,
        form_method="get",
        form_action=url_for("terminal.self_test", page=page),
        extra={"nav_base": url_for("terminal.self_test")},
    )


@bp.get("/db")
def db_menu() -> str:
    body = [
        "1. ETAT DE LA BASE (STATUS)",
        "2. SYNCHRONISATION FORCEE (SYNC)",
        "3. VIDER LA BASE (CLEAR)",
        "",
        "SELECTIONNEZ UNE OPTION ET APPUYEZ SUR ENTREE :",
    ]
    return _screen(
        pgm="DB-01",
        title="** GESTION DE LA BASE **",
        body_lines=body,
        input_label="",
        input_name="selection",
        input_maxlength=1,
        form_action=url_for("terminal.db_menu_post"),
    )


@bp.post("/db")
def db_menu_post() -> Any:
    choice = (request.form.get("selection") or "").strip()
    routes = {
        "1": "terminal.db_status",
        "2": "terminal.db_sync_confirm",
        "3": "terminal.db_clear_confirm",
    }
    if choice in routes:
        return redirect(url_for(routes[choice]))
    flash("OPTION INVALIDE — SAISIR 1 A 3", "error")
    return redirect(url_for("terminal.db_menu"))


@bp.get("/db/status")
def db_status() -> str:
    data_dir = current_app.config["DATA_DIR"]
    db = Database(data_dir=data_dir)
    db.open()
    try:
        stats = db.stats()
    finally:
        db.close()

    lines = [
        f"FICHIER : {stats['path']}",
        f"VERSION JEU : {stats['game_version'] or '(aucune)'}",
    ]
    last_checked = stats["last_checked_at"]
    if isinstance(last_checked, float):
        age_h = (time.time() - last_checked) / 3600
        lines.append(f"DERNIER CHECK : IL Y A {age_h:.1f}H")
    else:
        lines.append("DERNIER CHECK : (AUCUN)")
    lines.append(f"ENTREES : {stats['total_items']}")
    by_kind = stats["by_kind"]
    if isinstance(by_kind, dict) and by_kind:
        lines.append("PAR CATEGORIE :")
        for kind, count in by_kind.items():
            lines.append(f"  - {kind} : {count}")

    page = max(1, int(request.args.get("page", 1)))
    slice_lines, page, total = paginate(lines, page=page, page_size=BODY_LINES)
    return _screen(
        pgm="DB-02",
        title="** ETAT DE LA BASE **",
        body_lines=slice_lines,
        body_page=page,
        body_total_pages=total,
        fkeys=[("F7", "Precedent"), ("F8", "Suivant"), ("F12", "Retour")],
        input_label=None,
        form_method="get",
        form_action=url_for("terminal.db_menu"),
        extra={"nav_base": url_for("terminal.db_status")},
    )


@bp.get("/db/sync")
def db_sync_confirm() -> str:
    return _screen(
        pgm="DB-03",
        title="** SYNCHRONISATION **",
        body_lines=[
            "CETTE OPERATION CONTACTE L'API DOFUSDUDE",
            "ET PEUT PRENDRE PLUSIEURS MINUTES.",
            "",
            "CONFIRMER ? (O=OUI / N=NON)",
        ],
        input_label="CONFIRM",
        input_name="confirm",
        input_maxlength=1,
        form_action=url_for("terminal.db_sync_run"),
    )


@bp.post("/db/sync")
def db_sync_run() -> Any:
    confirm = (request.form.get("confirm") or "").strip().upper()
    if confirm not in {"O", "Y", "OUI", "YES"}:
        flash("SYNC ANNULEE", "info")
        return redirect(url_for("terminal.db_menu"))

    cfg = current_app.extensions["web_config"]
    data_dir = cfg["data_dir"]
    timeout = cfg.get("timeout")
    db = Database(data_dir=data_dir)
    db.open()
    try:
        ensure_up_to_date(
            db,
            force=True,
            offline=False,
            timeout=timeout,
            quiet=True,
        )
    except Exception as exc:
        flash(f"ERREUR SYNC : {exc}".upper()[:COLS], "error")
        return redirect(url_for("terminal.db_menu"))
    finally:
        db.close()

    try:
        reload_catalog(current_app, skip_sync=True)
    except Exception as exc:
        flash(f"SYNC OK MAIS RECHARGEMENT ECHOUE : {exc}".upper()[:COLS], "error")
        return redirect(url_for("terminal.db_menu"))

    flash("SYNCHRONISATION TERMINEE", "info")
    return redirect(url_for("terminal.db_status"))


@bp.get("/db/clear")
def db_clear_confirm() -> str:
    return _screen(
        pgm="DB-04",
        title="** VIDER LA BASE **",
        body_lines=[
            "ATTENTION : TOUTES LES ENTREES LOCALES SERONT SUPPRIMEES.",
            "",
            "CONFIRMER ? (O=OUI / N=NON)",
        ],
        input_label="CONFIRM",
        input_name="confirm",
        input_maxlength=1,
        form_action=url_for("terminal.db_clear_run"),
        status="OPERATION DESTRUCTIVE",
        status_kind="error",
    )


@bp.post("/db/clear")
def db_clear_run() -> Any:
    confirm = (request.form.get("confirm") or "").strip().upper()
    if confirm not in {"O", "Y", "OUI", "YES"}:
        flash("CLEAR ANNULE", "info")
        return redirect(url_for("terminal.db_menu"))

    data_dir = current_app.config["DATA_DIR"]
    db = Database(data_dir=data_dir)
    db.open()
    try:
        deleted = db.clear()
    except Exception as exc:
        flash(f"ERREUR CLEAR : {exc}".upper()[:COLS], "error")
        return redirect(url_for("terminal.db_menu"))
    finally:
        db.close()

    try:
        reload_catalog(current_app, skip_sync=True)
    except Exception:
        from dofus_stuff.catalog import Catalog
        from dofus_stuff.web import set_catalog

        set_catalog(current_app, Catalog(version=None, items={}))

    flash(f"BASE VIDEE : {deleted} ENTREE(S) SUPPRIMEE(S).", "info")
    return redirect(url_for("terminal.db_status"))


SESSION_OPTIMIZE_RESULT = "optimize_result_lines"


def _store_optimize_result(lines: list[str]) -> None:
    session[SESSION_OPTIMIZE_RESULT] = lines


def _run_optimize_and_redirect(req) -> Any:
    catalog = get_catalog()
    result = optimize_stuff(
        catalog,
        req.profile,
        spec=req.spec,
        top_k=req.top_k,
        time_limit_s=req.time_limit_s,
        use_cpsat=req.use_cpsat,
        classic_only=req.classic_only,
    )
    lines = format_optimize_result_lines(result, req.profile)
    _store_optimize_result(lines)
    flash("CALCUL TERMINE", "info")
    return redirect(url_for("terminal.optimize_result"))


@bp.get("/optimize")
def optimize_entry() -> Any:
    """Entrée unique : démarre le wizard Stuffer."""
    reset_wizard(session)
    return redirect(url_for("terminal.optimize_wizard", step="slots"))


def _wizard_fkeys(step: str) -> list[tuple[str, str]]:
    keys = [("F12", "Retour")]
    if prev_step(step):
        keys.insert(0, ("F7", "Precedent"))
    if next_step(step):
        keys.insert(len(keys) - 1 if keys else 0, ("F8", "Suivant"))
    return keys


def _wizard_step_urls(step: str) -> tuple[str | None, str | None]:
    """URLs F7/F8 pour navigation entre écrans du wizard."""
    prev = prev_step(step)
    nxt = next_step(step)
    f7 = url_for("terminal.optimize_wizard", step=prev) if prev else None
    f8 = url_for("terminal.optimize_wizard", step=nxt) if nxt else None
    return f7, f8


@bp.get("/optimize/wizard/<step>")
@bp.post("/optimize/wizard/<step>")
def optimize_wizard(step: str) -> Any:
    if step not in WIZARD_STEPS:
        flash("ECRAN WIZARD INCONNU", "error")
        return redirect(url_for("terminal.menu"))

    # Navigation F7/F8 via query
    nav = (request.args.get("nav") or "").strip().casefold()
    if nav == "prev":
        target = prev_step(step)
        if target:
            return redirect(url_for("terminal.optimize_wizard", step=target))
    if nav == "next":
        target = next_step(step)
        if target:
            return redirect(url_for("terminal.optimize_wizard", step=target))

    # Sous-édition d'option / stat
    edit = session.get(SESSION_WIZARD_EDIT)
    if isinstance(edit, dict) and edit.get("step") == step:
        return _wizard_edit_screen(step, edit)

    spec = load_wizard_spec(session)
    page = max(1, int(request.args.get("page", 1)))

    if request.method == "POST":
        raw = (request.form.get("cmd") or "").strip()
        try:
            if step == "slots":
                if not raw:
                    nxt = next_step(step)
                    return redirect(url_for("terminal.optimize_wizard", step=nxt or "options"))
                spec = apply_slots_input(spec, raw)
                save_wizard_spec(session, spec)
                flash("SLOT/FILTRE MIS A JOUR", "info")
                return redirect(url_for("terminal.optimize_wizard", step=step))

            if step == "options":
                if not raw:
                    return redirect(
                        url_for("terminal.optimize_wizard", step=next_step(step) or "caracs")
                    )
                spec, edit_key = apply_options_input(spec, raw)
                save_wizard_spec(session, spec)
                if edit_key:
                    session[SESSION_WIZARD_EDIT] = {
                        "step": step,
                        "kind": "option",
                        "key": edit_key,
                    }
                    return redirect(url_for("terminal.optimize_wizard", step=step))
                flash("OPTION MISE A JOUR", "info")
                return redirect(url_for("terminal.optimize_wizard", step=step))

            names = stat_names_for_step(step)
            if names is not None:
                if not raw:
                    return redirect(
                        url_for(
                            "terminal.optimize_wizard",
                            step=next_step(step) or "items",
                        )
                    )
                if not raw.isdigit():
                    raise ValueError("Saisir le numero de la ligne")
                idx = int(raw) - 1
                if idx < 0 or idx >= len(names):
                    raise ValueError("Numero invalide")
                session[SESSION_WIZARD_EDIT] = {
                    "step": step,
                    "kind": "stat",
                    "name": names[idx],
                    "with_exo": step == "papmpo",
                }
                return redirect(url_for("terminal.optimize_wizard", step=step))

            if step == "items":
                if not raw:
                    return redirect(url_for("terminal.optimize_wizard", step="recap"))
                spec = apply_items_input(spec, raw)
                save_wizard_spec(session, spec)
                flash("LISTE ITEMS MISE A JOUR", "info")
                return redirect(url_for("terminal.optimize_wizard", step=step))

            if step == "recap":
                upper = raw.casefold()
                if upper in {"", "go"}:
                    req = spec_to_request(spec)
                    return _run_optimize_and_redirect(req)
                if upper == "reset":
                    reset_wizard(session)
                    flash("WIZARD REINITIALISE", "info")
                    return redirect(url_for("terminal.optimize_wizard", step="slots"))
                if raw.isdigit():
                    n = int(raw)
                    if 1 <= n <= len(WIZARD_STEPS) - 1:
                        return redirect(
                            url_for("terminal.optimize_wizard", step=WIZARD_STEPS[n - 1])
                        )
                raise ValueError("GO | RESET | 1-8")
        except ValueError as exc:
            flash(str(exc).upper()[:COLS], "error")
            return redirect(url_for("terminal.optimize_wizard", step=step, page=page))
        except Exception as exc:
            flash(f"ERREUR : {exc}".upper()[:COLS], "error")
            return redirect(url_for("terminal.optimize_wizard", step=step, page=page))

    # GET — affichage
    f7_url, f8_url = _wizard_step_urls(step)
    nav_base = url_for("terminal.optimize_wizard", step=step)

    if step == "slots":
        body = body_slots(spec)
    elif step == "options":
        body = body_options(spec)
    elif step == "items":
        body = body_items(spec)
    elif step == "recap":
        body = body_recap(spec)
    else:
        names = stat_names_for_step(step) or ()
        body, page, total = body_stat_list(
            STEP_TITLES[step],
            names,
            spec,
            with_exo=(step == "papmpo"),
            page=page,
        )
        return _screen(
            pgm=f"OPT-W{WIZARD_STEPS.index(step) + 1}",
            title=f"** WIZARD — {STEP_TITLES[step]} **",
            body_lines=body,
            input_label="CMD",
            input_name="cmd",
            input_maxlength=40,
            form_action=url_for("terminal.optimize_wizard", step=step, page=page),
            fkeys=_wizard_fkeys(step),
            body_page=page,
            body_total_pages=total,
            nav_base=nav_base,
            f7_url=f7_url,
            f8_url=f8_url,
        )

    return _screen(
        pgm=f"OPT-W{WIZARD_STEPS.index(step) + 1}",
        title=f"** WIZARD — {STEP_TITLES[step]} **",
        body_lines=body,
        input_label="CMD",
        input_name="cmd",
        input_maxlength=40,
        form_action=url_for("terminal.optimize_wizard", step=step),
        fkeys=_wizard_fkeys(step),
        body_page=page,
        nav_base=nav_base,
        f7_url=f7_url,
        f8_url=f8_url,
    )


def _wizard_edit_screen(step: str, edit: dict[str, Any]) -> Any:
    spec = load_wizard_spec(session)
    kind = edit.get("kind")

    if request.method == "POST":
        raw = (request.form.get("value") or "").strip()
        try:
            if kind == "option":
                key = str(edit.get("key"))
                if not raw:
                    session.pop(SESSION_WIZARD_EDIT, None)
                    return redirect(url_for("terminal.optimize_wizard", step=step))
                spec = apply_option_value(spec, key, raw)
                save_wizard_spec(session, spec)
                session.pop(SESSION_WIZARD_EDIT, None)
                flash("VALEUR ENREGISTREE", "info")
                return redirect(url_for("terminal.optimize_wizard", step=step))
            if kind == "stat":
                name = str(edit.get("name"))
                with_exo = bool(edit.get("with_exo"))
                if not raw:
                    session.pop(SESSION_WIZARD_EDIT, None)
                    return redirect(url_for("terminal.optimize_wizard", step=step))
                spec = apply_stat_edit(spec, name, raw, with_exo=with_exo)
                save_wizard_spec(session, spec)
                session.pop(SESSION_WIZARD_EDIT, None)
                flash("CARAC ENREGISTREE", "info")
                return redirect(url_for("terminal.optimize_wizard", step=step))
        except ValueError as exc:
            flash(str(exc).upper()[:COLS], "error")
            return redirect(url_for("terminal.optimize_wizard", step=step))
        except Exception as exc:
            flash(f"ERREUR : {exc}".upper()[:COLS], "error")
            return redirect(url_for("terminal.optimize_wizard", step=step))

    if kind == "option":
        key = str(edit.get("key"))
        current = getattr(spec, key, "")
        body = [
            f"EDITION : {key.upper()}",
            f"VALEUR ACTUELLE : {current}",
            "",
            "NOUVELLE VALEUR (ENTREE VIDE = ANNULER) :",
        ]
        return _screen(
            pgm="OPT-WED",
            title="** WIZARD — EDITION **",
            body_lines=body,
            input_label="VAL",
            input_name="value",
            input_maxlength=20,
            form_action=url_for("terminal.optimize_wizard", step=step),
            fkeys=[("F12", "Annuler")],
        )

    name = str(edit.get("name"))
    with_exo = bool(edit.get("with_exo"))
    from dofus_stuff.model.solver_spec import StatGoal

    goal = spec.goals.get(name, StatGoal())
    if with_exo:
        hint = f"ACTUEL : B={goal.base:g} E={goal.exo:g} C={goal.target:g} W={goal.weight:g}"
        fmt = "FORMAT : BASE EXO CIBLE POIDS"
    else:
        hint = (
            f"ACTUEL : B={goal.base:g} P={goal.points:g} "
            f"C={goal.target:g} W={goal.weight:g}"
        )
        fmt = "FORMAT : BASE POINTS CIBLE POIDS"
    body = [
        f"EDITION : {name.upper()}",
        hint,
        fmt,
        "",
        "NOUVELLE VALEUR (ENTREE VIDE = ANNULER) :",
    ]
    return _screen(
        pgm="OPT-WED",
        title="** WIZARD — EDITION CARAC **",
        body_lines=body,
        input_label="VAL",
        input_name="value",
        input_maxlength=40,
        form_action=url_for("terminal.optimize_wizard", step=step),
        fkeys=[("F12", "Annuler")],
    )


@bp.get("/saves")
@bp.post("/saves")
def saves() -> Any:
    """Liste / consultation des stuffs sauvegardés (hydraté côté navigateur)."""
    return _screen(
        pgm="SAV-01",
        title="** STUFFS SAUVEGARDES **",
        body_lines=["CHARGEMENT DES SAUVEGARDES LOCALES…"],
        input_label="",
        input_name="cmd",
        input_maxlength=40,
        fkeys=[("F7", "Precedent"), ("F8", "Suivant"), ("F12", "Retour")],
        form_action=url_for("terminal.saves"),
        status="N OUVRIR | DEL N | PURGE OUI | F12 RETOUR",
        mode="saves",
    )


@bp.get("/optimize/result")
@bp.post("/optimize/result")
def optimize_result() -> Any:
    if request.method == "POST":
        raw = (
            request.form.get("cmd") or request.form.get("ankama_id") or ""
        ).strip()
        if raw.isdigit():
            return redirect(url_for("terminal.item_form", id=raw))
        flash("ID ANKAMA INVALIDE — OU SAVE [NOM] POUR SAUVEGARDER", "error")
        return redirect(url_for("terminal.optimize_result"))

    lines = session.get(SESSION_OPTIMIZE_RESULT)
    if not isinstance(lines, list) or not lines:
        flash("AUCUN RESULTAT — LANCER UN CALCUL D'ABORD", "error")
        return redirect(url_for("terminal.menu"))

    wrapped = wrap_lines(lines, COLS)
    page = max(1, int(request.args.get("page", 1)))
    slice_lines, page, total = paginate(wrapped, page=page, page_size=BODY_LINES)
    return _screen(
        pgm="OPT-03",
        title="** RESULTAT OPTIMISATION **",
        body_lines=slice_lines,
        input_label="",
        input_name="cmd",
        input_maxlength=40,
        body_page=page,
        body_total_pages=total,
        fkeys=[("F7", "Precedent"), ("F8", "Suivant"), ("F12", "Retour")],
        form_action=url_for("terminal.optimize_result"),
        status=f"PAGE {page}/{total} — ID DETAIL | SAVE [NOM] | F12 RETOUR",
        nav_base=url_for("terminal.optimize_result"),
        mode="result",
        stuff_payload={"lines": list(lines)},
    )
