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


def test_optimize_result_payload_parseable(client):
    """Le data-stuff-payload doit être un JSON récupérable via getAttribute."""
    import html as html_module
    import json
    import re

    lines = [
        'Stuff avec "guillemets" et accent «è»',
        "Symboles < > & pour vérifier l'échappement",
    ]
    with client.session_transaction() as sess:
        sess["optimize_result_lines"] = lines
    rv = client.get("/optimize/result")
    assert rv.status_code == 200
    body = rv.data.decode()
    match = re.search(r"data-stuff-payload='([^']*)'", body)
    assert match is not None, "payload introuvable ou attribut mal délimité"
    payload = json.loads(html_module.unescape(match.group(1)))
    assert payload["lines"] == lines


def test_wizard_exposes_step_nav_urls(client):
    client.post("/", data={"selection": "7"}, follow_redirects=True)
    rv = client.get("/optimize/wizard/options")
    assert rv.status_code == 200
    body = rv.data.decode()
    assert "data-f7-url=" in body
    assert "/optimize/wizard/slots" in body
    assert "data-f8-url=" in body
    assert "/optimize/wizard/caracs" in body


def test_optimize_result_edit_returns_to_recap(client):
    """EDIT renvoie au recap sans réinitialiser le spec."""
    from dofus_stuff.web.optimize_wizard import SESSION_WIZARD

    with client.session_transaction() as sess:
        sess["optimize_result_lines"] = ["Niveau 50", "Score : 1"]
        sess[SESSION_WIZARD] = {"level": 50, "goals": {}}

    rv = client.post("/optimize/result", data={"cmd": "EDIT"}, follow_redirects=False)
    assert rv.status_code in (301, 302)
    assert "/optimize/wizard/recap" in (rv.headers.get("Location") or "")
    # Le spec n'a pas été réinitialisé par l'EDIT.
    with client.session_transaction() as sess:
        assert sess.get(SESSION_WIZARD, {}).get("level") == 50


def test_build_dofusbook_url_encodes_slots():
    import base64

    import msgpack

    from dofus_stuff.web.dofusbook_export import build_dofusbook_url

    url = build_dofusbook_url(
        {
            "hat": {"ankama_id": 44},
            "cape": {"ankama_id": 50},
            "ring_a": {"ankama_id": 100},
            "ring_b": {"ankama_id": 101},
            "weapon": {"ankama_id": 7},
            "pet": {"ankama_id": 999},
        },
        level=200,
    )
    assert "stuff=" in url
    token = url.split("stuff=", 1)[1]
    data = msgpack.unpackb(base64.b64decode(token), raw=False)
    caracs, points, level, flags, counts, ids = data
    assert level == 200
    assert flags == 0
    # Groupes: cape, coiffe, ceinture, bottes, amulette, anneaux, dofus,
    # bouclier, arme, familier (ca puis ch dans le schéma Dofusbook)
    assert counts == [1, 1, 0, 0, 0, 2, 0, 0, 1, 1]
    assert ids == [50, 44, 100, 101, 7, 999]


def test_optimize_result_db_opens_browser(client):
    with client.session_transaction() as sess:
        sess["optimize_result_lines"] = ["Niveau 50", "Score : 1"]
        sess["optimize_result_build"] = {
            "slots": {"hat": 44, "weapon": 7},
            "level": 50,
        }
    with patch("dofus_stuff.web.routes.webbrowser.open_new_tab") as open_mock:
        rv = client.post("/optimize/result", data={"cmd": "DB"}, follow_redirects=False)
    assert rv.status_code in (301, 302)
    open_mock.assert_called_once()
    url = open_mock.call_args[0][0]
    assert "dofusbook.net" in url
    assert "stuff=" in url


def test_dofusbook_url_route_from_saved_slots(client):
    """La route JSON génère une URL Dofusbook depuis des slots sauvegardés."""
    rv = client.post(
        "/optimize/dofusbook-url",
        json={"slots": {"hat": 44, "ring_a": 100, "ring_b": 101}, "level": 199},
    )
    assert rv.status_code == 200
    data = rv.get_json()
    assert "dofusbook.net" in data["url"]
    assert "stuff=" in data["url"]

    # Décodage pour vérifier le contenu
    import base64

    import msgpack

    token = data["url"].split("stuff=", 1)[1]
    payload = msgpack.unpackb(base64.b64decode(token), raw=False)
    assert payload[2] == 199
    # hat est le groupe 1 (ch), anneaux le groupe 5
    assert payload[4] == [0, 1, 0, 0, 0, 2, 0, 0, 0, 0]
    assert payload[5] == [44, 100, 101]


def test_dofusbook_url_route_requires_slots(client):
    rv = client.post("/optimize/dofusbook-url", json={})
    assert rv.status_code == 400


def test_build_dofusbook_url_124test_hat_cape_order():
    """Régression : cape (groupe 0) avant chapeau (groupe 1), sinon Dofusbook
    rejette les deux items pour type incompatible."""
    import base64

    import msgpack

    from dofus_stuff.web.dofusbook_export import build_dofusbook_url

    slots = {
        "amulet": 8453,
        "belt": 14582,
        "boots": 2530,
        "cape": 8452,
        "dofus_1": 13344,
        "dofus_2": 13767,
        "dofus_3": 16247,
        "dofus_4": 12715,
        "dofus_5": 13766,
        "dofus_6": 16246,
        "hat": 14583,
        "pet": 33036,
        "ring_a": 2469,
        "ring_b": 27532,
        "shield": 18683,
        "weapon": 23314,
    }
    url = build_dofusbook_url(slots, 124)
    token = url.split("stuff=", 1)[1]
    data = msgpack.unpackb(base64.b64decode(token), raw=False)
    counts, ids = data[4], data[5]
    assert data[2] == 124
    assert counts == [1, 1, 1, 1, 1, 2, 6, 1, 1, 1]
    # Ordre plat : cape, hat, belt, boots, amulet, rings, dofus×6, shield, weapon, pet
    assert ids[0] == 8452  # cape
    assert ids[1] == 14583  # hat
    assert ids[2] == 14582  # belt
    assert ids[3] == 2530  # boots
    assert ids[4] == 8453  # amulet
    assert ids[5:7] == [2469, 27532]  # rings
    assert ids[7:13] == [13344, 13767, 16247, 12715, 13766, 16246]  # dofus
    assert ids[13] == 18683  # shield
    assert ids[14] == 23314  # weapon
    assert ids[15] == 33036  # pet
    assert 8452 in ids and 14583 in ids

