/* Interface translation for faktickapoznamka.sk (EN, DE, HU, PL).
   Loaded only when a foreign language is chosen. Replaces known Slovak interface strings
   in text and attributes, formats Slovak dates in the chosen language, and keeps watching
   the page for content added later. Parliamentary content (bill titles, transcripts, names)
   has no dictionary entry and stays in Slovak. */
(function () {
  "use strict";
  var root = document.documentElement;
  var lang = root.getAttribute("data-lang");
  if (!lang || lang === "sk") return;
  var LOCALE = { en: "en-GB", de: "de-DE", hu: "hu-HU", pl: "pl-PL" }[lang] || lang;
  var NUM = /\d+(?:[   ]\d{3})*(?:[,.]\d+)?/g;
  var MONTHS = ["januára", "februára", "marca", "apríla", "mája", "júna", "júla", "augusta", "septembra", "októbra", "novembra", "decembra"];
  var MONTHS_NOM = ["január", "február", "marec", "apríl", "máj", "jún", "júl", "august", "september", "október", "november", "december"];
  var MONTHS_SHORT = ["jan", "feb", "mar", "apr", "máj", "jún", "júl", "aug", "sep", "okt", "nov", "dec"];
  var DAYS = "pondelok|utorok|streda|štvrtok|piatok|sobota|nedeľa";
  var DATE = new RegExp("(?:(" + DAYS + ")\\s+)?(\\d{1,2})\\.\\s+(" + MONTHS.join("|") + ")(?:\\s+(\\d{4}))?(?:,?\\s+(?:o\\s+)?(\\d{1,2}):(\\d{2}))?", "gi");
  var MONTH_YEAR = new RegExp("^(" + MONTHS_NOM.join("|") + ")(?:\\s+(\\d{4}))?$", "i");
  var SHORT_MONTH = new RegExp("^(" + MONTHS_SHORT.join("|") + ")\\s+(\\d{2})(:.*)?$", "i");
  var D = null, plural = new Intl.PluralRules(LOCALE);
  var done = new WeakMap(), ATTRS = ["placeholder", "aria-label", "title", "alt"];

  function fmtDate(m, wd, d, mon, y, hh, mm) {
    var mi = MONTHS.indexOf(mon.toLowerCase());
    var year = y ? +y : new Date().getFullYear();
    var dt = new Date(year, mi, +d, hh ? +hh : 12, mm ? +mm : 0);
    var o = { day: "numeric", month: "long" };
    if (wd) o.weekday = "long";
    if (y) o.year = "numeric";
    if (hh) { o.hour = "2-digit"; o.minute = "2-digit"; }
    var s = dt.toLocaleString(LOCALE, o);
    return /^[A-ZÁÄČĎÉÍĽŇÓÔŔŠŤÚÝŽ]/.test(m) ? s.charAt(0).toUpperCase() + s.slice(1) : s;
  }
  function pick(v, nums) {
    if (v.indexOf("|") < 0) return v;
    var forms = v.split("|"), n = nums.length ? parseFloat(nums[0].replace(/[   ]/g, "").replace(",", ".")) : 2;
    var cat = plural.select(n);
    if (forms.length === 2) return cat === "one" ? forms[0] : forms[1];
    return cat === "one" ? forms[0] : cat === "few" ? forms[1] : forms[2];
  }
  function fill(v, nums, dates) {
    var i = 0, j = 0;
    v = pick(v, nums).replace(/\{n\}/g, function () { return nums[i++] || ""; });
    return v.replace(/\{d\}/g, function () { return dates[j++] || ""; });
  }
  // exact lookup with numbers and dates as placeholders
  function look(t) {
    var dates = [];
    var k = t.replace(DATE, function () { dates.push(fmtDate.apply(null, arguments)); return "{d}"; });
    var nums = k.match(NUM) || [];
    var key = k.replace(NUM, "{n}");
    var v = D[key];
    if (v != null) return fill(v, nums, dates);
    if (dates.length && k === "{d}") return dates[0];
    return null;
  }
  var SEPS = [" · ", ": ", " – ", " — ", ", "];
  function tr(t, depth) {
    var r = look(t);
    if (r != null) return r;
    var mY = t.match(MONTH_YEAR);
    if (mY) { var d0 = new Date(mY[2] ? +mY[2] : 2026, MONTHS_NOM.indexOf(mY[1].toLowerCase()), 1); return d0.toLocaleString(LOCALE, mY[2] ? { month: "long", year: "numeric" } : { month: "long" }); }
    var sm = t.match(SHORT_MONTH);
    if (sm) { var d1 = new Date(2000 + +sm[2], MONTHS_SHORT.indexOf(sm[1].toLowerCase()), 1); return d1.toLocaleString(LOCALE, { month: "short", year: "2-digit" }) + (sm[3] ? tr(sm[3].replace(/^:\s*/, ""), 1) != null ? ": " + tr(sm[3].replace(/^:\s*/, ""), 1) : sm[3] : ""); }
    if ((depth || 0) > 3) return null;
    // "Label (details)" and "(note)": translate the known part, keep the rest
    var par = t.match(/^\((.+)\)([.,]?)$/);
    if (par) { var inner = tr(par[1], (depth || 0) + 1); if (inner != null) return "(" + inner + ")" + par[2]; }
    var lab = t.match(/^(.+?) \((.+)\)$/);
    if (lab) { var head = look(lab[1]); if (head != null) return head + " (" + lab[2] + ")"; }
    for (var i = 0; i < SEPS.length; i++) {
      var sep = SEPS[i];
      if (t.indexOf(sep) < 0) continue;
      var parts = t.split(sep), changed = false;
      for (var p = 0; p < parts.length; p++) { var x = tr(parts[p], (depth || 0) + 1); if (x != null) { parts[p] = x; changed = true; } }
      if (changed) return parts.join(sep);
    }
    // dates inside otherwise unknown text
    if (DATE.test(t)) { DATE.lastIndex = 0; return t.replace(DATE, function () { return fmtDate.apply(null, arguments); }); }
    DATE.lastIndex = 0;
    return null;
  }
  function translateString(s) {
    if (!s || s.length > 900) return null;
    var lead = s.match(/^\s*/)[0], trail = s.match(/\s*$/)[0];
    var t = s.replace(/\s+/g, " ").trim();
    if (!t || !/[a-záäčďéíĺľňóôŕšťúýž]/i.test(t)) return null;
    var r = tr(t, 0);
    return r == null || r === t ? null : lead + r + trail;
  }
  function skip(el) { return !el || el.closest("script,style,noscript,[translate=no],.notranslate,code,pre"); }
  function textNode(n) {
    if (done.get(n) === n.nodeValue) return;
    var p = n.parentElement; if (skip(p)) return;
    var r = translateString(n.nodeValue);
    if (r != null) n.nodeValue = r;
    done.set(n, n.nodeValue);
  }
  function element(el) {
    if (skip(el)) return;
    for (var i = 0; i < ATTRS.length; i++) {
      var a = ATTRS[i], v = el.getAttribute(a);
      if (!v || el.getAttribute("data-i18n-" + a) === v) continue;
      var r = translateString(v);
      if (r != null) el.setAttribute(a, r);
      el.setAttribute("data-i18n-" + a, el.getAttribute(a));
    }
  }
  function walk(node) {
    if (node.nodeType === 3) return textNode(node);
    if (node.nodeType !== 1) return;
    element(node);
    var w = document.createTreeWalker(node, NodeFilter.SHOW_TEXT | NodeFilter.SHOW_ELEMENT);
    var n; while ((n = w.nextNode())) { if (n.nodeType === 3) textNode(n); else element(n); }
  }
  function meta() {
    var t = translateString(document.title); if (t) document.title = t;
    var md = document.querySelector('meta[name="description"]');
    if (md) { var r = translateString(md.content); if (r) md.content = r; }
  }
  function notice() {
    if (document.getElementById("i18n-bar")) return;
    var txt = {
      en: ["Interface in English. Bill titles, transcripts and other parliamentary content remain in Slovak.", "Slovenčina", "Content stays in Slovak"],
      de: ["Oberfläche auf Deutsch. Gesetzestitel, Protokolle und andere parlamentarische Inhalte bleiben auf Slowakisch.", "Slovenčina", "Inhalte bleiben auf Slowakisch"],
      hu: ["Felület magyarul. A törvények címe, a jegyzőkönyvek és más parlamenti tartalmak szlovákul maradnak.", "Slovenčina", "A tartalom szlovákul marad"],
      pl: ["Interfejs po polsku. Tytuły ustaw, stenogramy i inne treści parlamentarne pozostają po słowacku.", "Slovenčina", "Treści pozostają po słowacku"],
    }[lang];
    var bar = document.createElement("div"); bar.id = "i18n-bar"; bar.className = "i18n-bar"; bar.setAttribute("translate", "no");
    var s = document.createElement("span"); var sl = document.createElement("span"); sl.className = "i18n-long"; sl.textContent = txt[0];
    var ss = document.createElement("span"); ss.className = "i18n-short"; ss.textContent = txt[2]; s.append(sl, ss);
    var b = document.createElement("button"); b.type = "button"; b.textContent = "↩ " + txt[1]; b.lang = "sk";
    b.addEventListener("click", function () { try { localStorage.removeItem("fp-lang"); } catch (e) {} location.reload(); });
    bar.append(s, b); document.body.prepend(bar);
  }
  function run() {
    meta(); notice(); walk(document.body);
    new MutationObserver(function (ms) {
      for (var i = 0; i < ms.length; i++) {
        var m = ms[i];
        if (m.type === "characterData") textNode(m.target);
        else if (m.type === "attributes") element(m.target);
        else for (var j = 0; j < m.addedNodes.length; j++) walk(m.addedNodes[j]);
      }
      meta();
    }).observe(document.body, { childList: true, subtree: true, characterData: true, attributes: true, attributeFilter: ATTRS });
    root.classList.remove("i18n-wait");
  }
  var safety = setTimeout(function () { root.classList.remove("i18n-wait"); }, 2500);
  (window.__fpDict || fetch("/i18n/" + lang + ".json").then(function (r) { return r.json(); }))
    .then(function (d) {
      D = d;
      if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", run); else run();
      clearTimeout(safety);
    })
    .catch(function () { root.classList.remove("i18n-wait"); });
})();
