(function () {
  "use strict";

  var terminal = document.getElementById("terminal");
  if (!terminal) return;

  var form = document.getElementById("main-form");
  var input = document.getElementById("main-input");
  var headerRow = document.getElementById("header-row");
  var bodyEl = document.getElementById("body");
  var statusEl = document.querySelector(".row.status");

  var MODE = terminal.getAttribute("data-mode") || "";
  var SAVES_KEY = "dofus-stuff-machine.saves";
  var MAX_SAVES = 20;
  var BODY_LINES = 18;
  var COLS = 100;

  var savesState = {
    view: "list",
    index: -1,
    page: 1,
    lines: [],
  };

  function pad2(n) {
    return n < 10 ? "0" + n : String(n);
  }

  function formatClock(d) {
    return (
      d.getFullYear() +
      "-" +
      pad2(d.getMonth() + 1) +
      "-" +
      pad2(d.getDate()) +
      " " +
      pad2(d.getHours()) +
      ":" +
      pad2(d.getMinutes()) +
      ":" +
      pad2(d.getSeconds())
    );
  }

  function updateClock() {
    if (!headerRow) return;
    var text = headerRow.textContent || "";
    var clock = formatClock(new Date());
    if (text.length >= 19) {
      headerRow.textContent = text.slice(0, text.length - 19) + clock;
    }
  }

  updateClock();
  setInterval(updateClock, 1000);

  function scaleTerminal() {
    var cols = parseInt(terminal.getAttribute("data-cols") || "100", 10);
    terminal.style.transform = "scale(1)";
    var rect = terminal.getBoundingClientRect();
    var vw = window.innerWidth * 0.96;
    var vh = window.innerHeight * 0.96;
    var scale = Math.min(vw / rect.width, vh / rect.height, 1.5);
    if (!isFinite(scale) || scale <= 0) scale = 1;
    terminal.style.transform = "scale(" + scale + ")";
    var targetChar = vw / (cols + 2);
    var base = Math.max(8, Math.min(22, targetChar));
    document.documentElement.style.fontSize = base + "px";
    terminal.style.transform = "scale(1)";
    rect = terminal.getBoundingClientRect();
    scale = Math.min(vw / rect.width, vh / rect.height);
    if (!isFinite(scale) || scale <= 0) scale = 1;
    terminal.style.transform = "scale(" + scale + ")";
  }

  scaleTerminal();
  window.addEventListener("resize", scaleTerminal);

  if (input) {
    input.focus();
    document.addEventListener("mousedown", function (e) {
      if (e.target !== input) {
        e.preventDefault();
        input.focus();
      }
    });
  }

  function pageUrl(page) {
    var base = terminal.getAttribute("data-nav-base") || "";
    if (!base) return "";
    try {
      var url = new URL(base, window.location.origin);
      url.searchParams.set("page", String(page));
      return url.pathname + url.search;
    } catch (err) {
      var sep = base.indexOf("?") >= 0 ? "&" : "?";
      return base + sep + "page=" + page;
    }
  }

  function currentPage() {
    return parseInt(terminal.getAttribute("data-body-page") || "1", 10);
  }

  function totalPages() {
    return parseInt(terminal.getAttribute("data-body-total") || "1", 10);
  }

  function goPage(delta) {
    var page = currentPage();
    var total = totalPages();
    var next = page + delta;
    if (next < 1 || next > total) return false;
    var url = pageUrl(next);
    if (!url) return false;
    window.location.href = url;
    return true;
  }

  function setStatus(msg, kind) {
    if (!statusEl) return;
    statusEl.textContent = (msg || "").slice(0, COLS) || "\u00a0";
    statusEl.className = "row status " + (kind || "info");
  }

  function clipLine(text, width) {
    width = width || COLS;
    text = text == null ? "" : String(text);
    if (text.length > width) {
      if (width <= 1) return text.slice(0, width);
      return text.slice(0, width - 1) + "…";
    }
    while (text.length < width) text += " ";
    return text;
  }

  function wrapLine(text, width) {
    width = width || COLS;
    text = text == null ? "" : String(text);
    if (text.length <= width) return [text];
    var lines = [];
    var remaining = text;
    while (remaining) {
      if (remaining.length <= width) {
        lines.push(remaining);
        break;
      }
      var split = remaining.lastIndexOf(" ", width);
      if (split <= 0) {
        lines.push(remaining.slice(0, width));
        remaining = remaining.slice(width);
        continue;
      }
      lines.push(remaining.slice(0, split));
      remaining = remaining.slice(split + 1);
    }
    return lines;
  }

  function wrapLines(lines, width) {
    var out = [];
    for (var i = 0; i < lines.length; i++) {
      out = out.concat(wrapLine(lines[i], width));
    }
    return out;
  }

  function renderBodyRows(lines) {
    if (!bodyEl) return;
    var padded = [];
    var i;
    for (i = 0; i < lines.length && i < BODY_LINES; i++) {
      padded.push(clipLine(lines[i]));
    }
    while (padded.length < BODY_LINES) {
      padded.push(clipLine(""));
    }
    bodyEl.innerHTML = "";
    for (i = 0; i < padded.length; i++) {
      var row = document.createElement("div");
      row.className = "row";
      row.textContent = padded[i];
      bodyEl.appendChild(row);
    }
  }

  function loadSaves() {
    try {
      var raw = localStorage.getItem(SAVES_KEY);
      if (!raw) return [];
      var data = JSON.parse(raw);
      if (!data || !Array.isArray(data.stuffs)) return [];
      return data.stuffs;
    } catch (err) {
      return [];
    }
  }

  function writeSaves(stuffs) {
    localStorage.setItem(
      SAVES_KEY,
      JSON.stringify({ version: 1, stuffs: stuffs })
    );
  }

  function makeId() {
    return (
      Date.now().toString(36) +
      "-" +
      Math.random().toString(36).slice(2, 8)
    );
  }

  function buildSummary(lines) {
    var score = "";
    var niveau = "";
    var method = "";
    var i;
    for (i = 0; i < lines.length; i++) {
      var line = lines[i] || "";
      if (!niveau && line.indexOf("Niveau ") === 0) {
        var nivMatch = line.match(/^Niveau\s+(\d+)/);
        if (nivMatch) niveau = "niv." + nivMatch[1];
      }
      if (!method && line.indexOf("Méthode") === 0) {
        method = line.replace(/^Méthode\s*:\s*/i, "").split("(")[0].trim();
      }
      if (!score && line.indexOf("Score") === 0) {
        var scMatch = line.match(/Score\s*:\s*([0-9.]+)/);
        if (scMatch) score = "Score " + scMatch[1];
      }
    }
    var parts = [];
    if (score) parts.push(score);
    if (niveau) parts.push(niveau);
    if (method) parts.push(method);
    return parts.length ? parts.join(" — ") : "Stuff sauvegardé";
  }

  function formatSavedAt(iso) {
    try {
      var d = new Date(iso);
      if (isNaN(d.getTime())) return iso || "";
      return (
        d.getFullYear() +
        "-" +
        pad2(d.getMonth() + 1) +
        "-" +
        pad2(d.getDate()) +
        " " +
        pad2(d.getHours()) +
        ":" +
        pad2(d.getMinutes())
      );
    } catch (err) {
      return iso || "";
    }
  }

  function saveCurrentResult(label) {
    var payloadRaw = terminal.getAttribute("data-stuff-payload");
    if (!payloadRaw) {
      setStatus("AUCUN PAYLOAD A SAUVEGARDER", "error");
      return;
    }
    var payload;
    try {
      payload = JSON.parse(payloadRaw);
    } catch (err) {
      setStatus("PAYLOAD INVALIDE", "error");
      return;
    }
    var lines = payload && Array.isArray(payload.lines) ? payload.lines : null;
    if (!lines || !lines.length) {
      setStatus("RESULTAT VIDE — RIEN A SAUVEGARDER", "error");
      return;
    }
    var stuffs = loadSaves();
    while (stuffs.length >= MAX_SAVES) {
      stuffs.shift();
    }
    var entry = {
      id: makeId(),
      savedAt: new Date().toISOString(),
      label: label || "",
      summary: buildSummary(lines),
      lines: lines,
    };
    stuffs.push(entry);
    try {
      writeSaves(stuffs);
    } catch (err) {
      setStatus("ECHEC LOCALSTORAGE (QUOTA ?)", "error");
      return;
    }
    var msg = "STUFF SAUVEGARDE (" + stuffs.length + "/" + MAX_SAVES + ")";
    if (label) msg += " — " + label;
    setStatus(msg.slice(0, COLS), "info");
  }

  function listLinesFromSaves(stuffs) {
    if (!stuffs.length) {
      return [
        "AUCUNE SAUVEGARDE LOCALE.",
        "",
        "Apres un calcul, tapez SAVE [NOM] sur l'ecran resultat.",
        "Les stuffs sont stockes dans ce navigateur uniquement.",
      ];
    }
    var lines = [
      stuffs.length + " SAUVEGARDE(S) — MAX " + MAX_SAVES,
      "",
    ];
    var i;
    for (i = 0; i < stuffs.length; i++) {
      var s = stuffs[i];
      var label = s.label ? " — " + s.label : "";
      lines.push(
        i +
          1 +
          ". " +
          formatSavedAt(s.savedAt) +
          " — " +
          (s.summary || "Stuff") +
          label
      );
    }
    return lines;
  }

  function renderSavesList() {
    savesState.view = "list";
    savesState.index = -1;
    savesState.lines = [];
    var stuffs = loadSaves();
    savesState.listPages = wrapLines(listLinesFromSaves(stuffs), COLS);
    renderSavesListPage(1);
  }

  function renderSavesListPage(page) {
    var all = savesState.listPages || [];
    var total = Math.max(1, Math.ceil(all.length / BODY_LINES) || 1);
    page = Math.max(1, Math.min(page, total));
    savesState.page = page;
    var start = (page - 1) * BODY_LINES;
    renderBodyRows(all.slice(start, start + BODY_LINES));
    terminal.setAttribute("data-body-page", String(page));
    terminal.setAttribute("data-body-total", String(total));
    setStatus(
      "PAGE " + page + "/" + total + " — N OUVRIR | DEL N | PURGE OUI | F12",
      "info"
    );
  }

  function openSaveDetail(index) {
    var stuffs = loadSaves();
    if (index < 0 || index >= stuffs.length) {
      setStatus("NUMERO INVALIDE", "error");
      return;
    }
    var entry = stuffs[index];
    var wrapped = wrapLines(entry.lines || [], COLS);
    savesState.view = "detail";
    savesState.index = index;
    savesState.page = 1;
    savesState.lines = wrapped;
    renderSaveDetailPage(1);
  }

  function renderSaveDetailPage(page) {
    var wrapped = savesState.lines || [];
    var total = Math.max(1, Math.ceil(wrapped.length / BODY_LINES) || 1);
    page = Math.max(1, Math.min(page, total));
    savesState.page = page;
    var start = (page - 1) * BODY_LINES;
    renderBodyRows(wrapped.slice(start, start + BODY_LINES));
    terminal.setAttribute("data-body-page", String(page));
    terminal.setAttribute("data-body-total", String(total));
    setStatus(
      "PAGE " + page + "/" + total + " — BACK LISTE | F12 MENU",
      "info"
    );
  }

  function handleSavesCmd(raw) {
    var cmd = (raw || "").trim();
    if (!cmd) {
      if (savesState.view === "detail") {
        renderSavesList();
        return;
      }
      return;
    }
    var upper = cmd.toUpperCase();

    if (savesState.view === "detail") {
      if (upper === "BACK" || upper === "LISTE" || upper === "L") {
        renderSavesList();
        return;
      }
      setStatus("BACK POUR LA LISTE | F12 MENU", "error");
      return;
    }

    if (upper === "PURGE OUI") {
      try {
        localStorage.removeItem(SAVES_KEY);
      } catch (err) {
        /* ignore */
      }
      renderSavesList();
      setStatus("SAUVEGARDES PURGEES", "info");
      return;
    }
    if (upper === "PURGE") {
      setStatus("CONFIRMER AVEC : PURGE OUI", "error");
      return;
    }

    var delMatch = upper.match(/^DEL\s+(\d+)$/);
    if (delMatch) {
      var delIdx = parseInt(delMatch[1], 10) - 1;
      var stuffs = loadSaves();
      if (delIdx < 0 || delIdx >= stuffs.length) {
        setStatus("NUMERO INVALIDE", "error");
        return;
      }
      stuffs.splice(delIdx, 1);
      writeSaves(stuffs);
      renderSavesList();
      setStatus("SAUVEGARDE SUPPRIMEE", "info");
      return;
    }

    if (/^\d+$/.test(cmd)) {
      openSaveDetail(parseInt(cmd, 10) - 1);
      return;
    }

    setStatus("COMMANDE INVALIDE — N | DEL N | PURGE OUI", "error");
  }

  function savesHandlePageDelta(delta) {
    if (MODE !== "saves") return false;
    if (savesState.view === "detail") {
      var totalDetail = Math.max(
        1,
        Math.ceil((savesState.lines || []).length / BODY_LINES) || 1
      );
      var nextDetail = savesState.page + delta;
      if (nextDetail < 1) {
        renderSavesList();
        return true;
      }
      if (nextDetail > totalDetail) return true;
      renderSaveDetailPage(nextDetail);
      return true;
    }
    var all = savesState.listPages || [];
    var totalList = Math.max(1, Math.ceil(all.length / BODY_LINES) || 1);
    var nextList = savesState.page + delta;
    if (nextList < 1 || nextList > totalList) return true;
    renderSavesListPage(nextList);
    return true;
  }

  /**
   * F7/F8 hiérarchiques :
   * 1) d'abord pagination locale si possible
   * 2) sinon URL d'étape wizard (data-f7-url / data-f8-url)
   */
  function navigateF7() {
    if (savesHandlePageDelta(-1)) return;
    if (currentPage() > 1 && goPage(-1)) return;
    var stepUrl = terminal.getAttribute("data-f7-url") || "";
    if (stepUrl) {
      window.location.href = stepUrl;
      return;
    }
    goPage(-1);
  }

  function navigateF8() {
    if (savesHandlePageDelta(1)) return;
    if (currentPage() < totalPages() && goPage(1)) return;
    var stepUrl = terminal.getAttribute("data-f8-url") || "";
    if (stepUrl) {
      window.location.href = stepUrl;
      return;
    }
    goPage(1);
  }

  document.addEventListener("keydown", function (e) {
    var key = e.key;

    if (key === "F3") {
      e.preventDefault();
      window.location.href = terminal.getAttribute("data-f3-url") || "/quit";
      return;
    }

    if (key === "F12") {
      e.preventDefault();
      window.location.href = terminal.getAttribute("data-f12-url") || "/";
      return;
    }

    if (key === "F7") {
      e.preventDefault();
      navigateF7();
      return;
    }

    if (key === "F8") {
      e.preventDefault();
      navigateF8();
      return;
    }

    if (key === "PageUp") {
      e.preventDefault();
      if (MODE === "saves") {
        savesHandlePageDelta(-1);
        return;
      }
      if (!goPage(-1)) navigateF7();
      return;
    }

    if (key === "PageDown") {
      e.preventDefault();
      if (MODE === "saves") {
        savesHandlePageDelta(1);
        return;
      }
      if (!goPage(1)) navigateF8();
      return;
    }

    if (key === "Enter" && form && document.activeElement === input) {
      return;
    }

    if (key === " ") {
      if (document.activeElement !== input) {
        e.preventDefault();
      }
    }
  });

  if (MODE === "result" && form) {
    form.addEventListener("submit", function (e) {
      var raw = (input && input.value ? input.value : "").trim();
      var upper = raw.toUpperCase();
      if (upper === "SAVE" || upper.indexOf("SAVE ") === 0) {
        e.preventDefault();
        var label = "";
        if (upper.indexOf("SAVE ") === 0) {
          label = raw.slice(5).trim();
        }
        saveCurrentResult(label);
        if (input) input.value = "";
      }
    });
  }

  if (MODE === "saves" && form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var raw = input && input.value ? input.value : "";
      handleSavesCmd(raw);
      if (input) input.value = "";
    });
    renderSavesList();
  }
})();
