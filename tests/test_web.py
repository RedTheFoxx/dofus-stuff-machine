"""Tests d'intégration Flask — parité CLI."""

from __future__ import annotations

from unittest.mock import patch

from dofus_stuff.catalog import Catalog


def test_menu_get(client):
    rv = client.get("/")
    assert rv.status_code == 200
    assert b"MENU PRINCIPAL" in rv.data
    assert b"1. RECHERCHE" in rv.data
    assert b"8. STUFFS SAUVEGARDES" in rv.data
    assert b"F3" in rv.data


def test_menu_post_valid(client):
    rv = client.post("/", data={"selection": "4"}, follow_redirects=True)
    assert rv.status_code == 200
    assert b"VERSION DOFUS" in rv.data
    assert b"9.9.9.9" in rv.data


def test_menu_post_invalid(client):
    rv = client.post("/", data={"selection": "9"}, follow_redirects=True)
    assert rv.status_code == 200
    assert b"OPTION INVALIDE" in rv.data
    assert b"1 A 8" in rv.data
    assert b"error" in rv.data


def test_menu_option_8_saves(client):
    rv = client.post("/", data={"selection": "8"}, follow_redirects=True)
    assert rv.status_code == 200
    assert b"STUFFS SAUVEGARDES" in rv.data
    assert b'data-mode="saves"' in rv.data


def test_saves_screen(client):
    rv = client.get("/saves")
    assert rv.status_code == 200
    assert b"SAV-01" in rv.data or b"STUFFS SAUVEGARDES" in rv.data
    assert b'data-mode="saves"' in rv.data
    assert b"PURGE OUI" in rv.data


def test_search_form_and_results(client):
    rv = client.get("/search")
    assert rv.status_code == 200
    assert b"RECHERCHE" in rv.data

    rv = client.post("/search", data={"query": "Cape"}, follow_redirects=True)
    assert rv.status_code == 200
    assert b"Atcham" in rv.data or b"Cape" in rv.data
    assert b"TROUVES" in rv.data


def test_search_empty(client):
    rv = client.post("/search", data={"query": "ZZZNOMATCH"}, follow_redirects=True)
    assert rv.status_code == 200
    assert b"AUCUN RESULTAT" in rv.data


def test_search_with_limit(client):
    rv = client.post("/search", data={"query": "Cape|1"}, follow_redirects=True)
    assert rv.status_code == 200
    assert b"LIMITE : 1" in rv.data


def test_item_detail(client):
    rv = client.post("/item", data={"ankama_id": "44"}, follow_redirects=True)
    assert rv.status_code == 200
    assert b"Boisaille" in rv.data or "Boisaille".encode() in rv.data
    assert b"Effets" in rv.data or b"dommages" in rv.data


def test_item_long_description_wraps(client, catalog):
    long_desc = (
        "Une description volontairement tres longue pour verifier que le texte "
        "nest pas tronque par des points de suspension et peut etre lu en entier "
        "grace aux retours a la ligne automatiques sur plusieurs lignes."
    )
    catalog.items[("equipment", 44)]["description"] = long_desc
    rv = client.get("/item?id=44")
    assert rv.status_code == 200
    body = rv.data.decode()
    assert "volontairement tres longue" in body
    assert "retours a la ligne" in body
    # Pas de troncature ellipsis sur la description elle-même
    assert "Description : Une description volontairement tres longue…" not in body


def test_item_not_found(client):
    rv = client.post("/item", data={"ankama_id": "99999"}, follow_redirects=True)
    assert rv.status_code == 200
    assert b"introuvable" in rv.data.lower() or b"INTROUVABLE" in rv.data


def test_item_invalid_id(client):
    rv = client.post("/item", data={"ankama_id": "abc"}, follow_redirects=True)
    assert rv.status_code == 200
    assert b"INVALIDE" in rv.data


def test_list_page(client):
    rv = client.get("/list?page=1&size=2")
    assert rv.status_code == 200
    assert b"LISTE DES EQUIPEMENTS" in rv.data
    assert b"PAGE 1" in rv.data
    assert b"ANKAMA_ID" in rv.data
    assert b"SAISIR UN ID ANKAMA" in rv.data


def test_list_pagination(client):
    rv = client.get("/list?page=2&size=2")
    assert rv.status_code == 200
    assert b"PAGE 2" in rv.data


def test_list_open_item_detail(client):
    rv = client.post("/list?page=1&size=2", data={"ankama_id": "44"}, follow_redirects=True)
    assert rv.status_code == 200
    assert b"ITEM #44" in rv.data
    assert b"Boisaille" in rv.data or "Boisaille".encode() in rv.data


def test_list_open_item_invalid_id(client):
    rv = client.post("/list?page=1&size=2", data={"ankama_id": "abc"}, follow_redirects=True)
    assert rv.status_code == 200
    assert b"LISTE DES EQUIPEMENTS" in rv.data
    assert b"INVALIDE" in rv.data


def test_version(client):
    rv = client.get("/version")
    assert rv.status_code == 200
    assert b"9.9.9.9" in rv.data


def test_self_test(client):
    rv = client.get("/self-test")
    assert rv.status_code == 200
    assert b"SELF-TEST" in rv.data
    assert b"[OK]" in rv.data or b"OK" in rv.data


def test_db_menu_and_status(client):
    rv = client.get("/db")
    assert rv.status_code == 200
    assert b"GESTION DE LA BASE" in rv.data

    rv = client.post("/db", data={"selection": "1"}, follow_redirects=True)
    assert rv.status_code == 200
    assert b"ETAT DE LA BASE" in rv.data or b"ENTREES" in rv.data
    assert b"9.9.9.9" in rv.data


def test_db_sync_cancelled(client):
    rv = client.post("/db/sync", data={"confirm": "N"}, follow_redirects=True)
    assert rv.status_code == 200
    assert b"ANNULEE" in rv.data or b"GESTION" in rv.data


def test_db_sync_reload_after_sync(client, app):
    """Le reload post-sync ne doit pas planter (threads SQLite)."""
    with patch("dofus_stuff.web.routes.ensure_up_to_date") as sync_mock:
        sync_mock.return_value = None
        rv = client.post("/db/sync", data={"confirm": "O"}, follow_redirects=True)
    assert rv.status_code == 200
    assert b"RECHARGEMENT ECHOUE" not in rv.data
    assert b"SYNCHRONISATION TERMINEE" in rv.data or b"ETAT" in rv.data
    assert app.extensions["catalog"] is not None


def test_catalog_load_releases_db(tmp_path):
    """Catalog.load ne conserve pas de connexion SQLite ouverte."""
    from dofus_stuff.database import Database

    data_dir = tmp_path / "data"
    db = Database(data_dir=data_dir)
    db.open()
    db.set_meta("game_version", "1.0.0")
    db.replace_kind(
        "equipment",
        [{"ankama_id": 1, "name": "Test", "level": 1}],
    )
    db.close()

    catalog = Catalog.load(data_dir=data_dir, offline=True, quiet=True, skip_sync=True)
    assert catalog.db is None
    assert catalog.version == "1.0.0"
    assert len(catalog.items) == 1
    catalog.close()



def test_db_clear(client, app, tmp_path):
    rv = client.post("/db/clear", data={"confirm": "O"}, follow_redirects=True)
    assert rv.status_code == 200
    assert b"VIDEE" in rv.data or b"SUPPRIMEE" in rv.data or b"ENTREES" in rv.data
    # Catalogue rechargé depuis la base vide
    catalog = app.extensions["catalog"]
    assert isinstance(catalog, Catalog)


def test_quit(client):
    rv = client.get("/quit")
    assert rv.status_code == 200
    assert b"FIN DE SESSION" in rv.data


def test_static_assets(client):
    css = client.get("/static/css/terminal.css")
    assert css.status_code == 200
    assert b"#000000" in css.data
    js = client.get("/static/js/terminal.js")
    assert js.status_code == 200
    assert b"F3" in js.data


def _fake_optimize_result():
    from dofus_stuff.model.build import Build, BuildEvaluation
    from dofus_stuff.model.stats import Stats
    from dofus_stuff.optimize.api import OptimizeResult
    from dofus_stuff.optimize.score import Compatibility

    evaluation = BuildEvaluation(
        total_stats=Stats({"Intelligence": 500.0}),
        item_stats=Stats({"Intelligence": 200.0}),
        set_stats=Stats(),
        base_stats=Stats({"Intelligence": 300.0}),
        score=500.0,
        set_bonuses=[],
        valid=True,
    )
    return OptimizeResult(
        build=Build(
            slots={
                "hat": {
                    "ankama_id": 44,
                    "name": "Épée de Boisaille",
                    "level": 7,
                    "type": {"name": "Chapeau"},
                }
            }
        ),
        evaluation=evaluation,
        compatibility=Compatibility(
            percent=100.0,
            mode="optimal_prouve",
            score=500.0,
            reference=500.0,
        ),
        method="cpsat",
        greedy_score=490.0,
        ub0=600.0,
        cpsat_status="OPTIMAL",
    )


def test_menu_option_7_optimize(client):
    rv = client.post("/", data={"selection": "7"}, follow_redirects=True)
    assert rv.status_code == 200
    assert b"WIZARD" in rv.data
    assert b"SLOTS" in rv.data


def test_optimize_entry_redirects_to_wizard(client):
    rv = client.get("/optimize", follow_redirects=True)
    assert rv.status_code == 200
    assert b"WIZARD" in rv.data
    assert b"SLOTS" in rv.data


def test_optimize_wizard_go_mocked(client):
    with patch(
        "dofus_stuff.web.routes.optimize_stuff",
        return_value=_fake_optimize_result(),
    ):
        client.post("/", data={"selection": "7"}, follow_redirects=True)
        with client.session_transaction() as sess:
            from dofus_stuff.web.optimize_wizard import SESSION_WIZARD
            from dofus_stuff.model.solver_spec import SolverSpec, StatGoal

            spec = SolverSpec(
                level=50,
                goals={"Intelligence": StatGoal(base=100, weight=1.0)},
                enabled_slot_groups=(
                    "amulet",
                    "rings",
                    "belt",
                    "boots",
                    "hat",
                    "cape",
                    "weapon",
                ),
            )
            sess[SESSION_WIZARD] = spec.to_dict()
        rv = client.post(
            "/optimize/wizard/recap",
            data={"cmd": "GO"},
            follow_redirects=True,
        )
    assert rv.status_code == 200
    assert b"RESULTAT" in rv.data


def test_optimize_result_pagination(client):
    """Le résultat long doit exposer la pagination F7/F8 (dofus 5-6 en page 2)."""
    lines = [
        "Niveau 200 — objectif {'Intelligence': 1.0}",
        "Méthode : cpsat",
        "Score : 100",
        "",
        "Équipement :",
    ]
    for i, slot in enumerate(
        [
            "amulet",
            "ring_a",
            "ring_b",
            "belt",
            "boots",
            "hat",
            "cape",
            "weapon",
            "dofus_1",
            "dofus_2",
            "dofus_3",
            "dofus_4",
            "dofus_5",
            "dofus_6",
            "pet",
            "prysma",
        ]
    ):
        lines.append(f"  {slot:8s} : Item{i} (#100{i}, niv. 200)")
    lines.extend(["", "Stats totales :", "  Intelligence: 999"])
    with client.session_transaction() as sess:
        sess["optimize_result_lines"] = lines

    rv = client.get("/optimize/result")
    assert rv.status_code == 200
    body = rv.data.decode()
    assert 'data-body-total="' in body
    # Plus d'une page
    assert 'data-body-total="1"' not in body or "dofus_5" in body
    assert "data-nav-base=" in body
    assert "/optimize/result" in body
    assert 'data-mode="result"' in body
    assert "data-stuff-payload=" in body
    assert "SAVE" in body

    # Page 2 doit contenir les dofus restants ou la suite
    total_attr = None
    for part in body.split("data-body-total=\"")[1:]:
        total_attr = part.split('"', 1)[0]
        break
    assert total_attr is not None
    assert int(total_attr) >= 2

    rv2 = client.get("/optimize/result?page=2")
    assert rv2.status_code == 200
    page2 = rv2.data.decode()
    assert "dofus_5" in page2 or "dofus_6" in page2 or "Intelligence" in page2


def test_optimize_result_cmd_id(client):
    with client.session_transaction() as sess:
        sess["optimize_result_lines"] = ["Niveau 50", "Score : 1"]
    rv = client.post("/optimize/result", data={"cmd": "12345"}, follow_redirects=False)
    assert rv.status_code in (301, 302)
    assert "/item" in (rv.headers.get("Location") or "")


def test_wizard_exposes_step_nav_urls(client):
    client.post("/", data={"selection": "7"}, follow_redirects=True)
    rv = client.get("/optimize/wizard/options")
    assert rv.status_code == 200
    body = rv.data.decode()
    assert "data-f7-url=" in body
    assert "/optimize/wizard/slots" in body
    assert "data-f8-url=" in body
    assert "/optimize/wizard/caracs" in body
