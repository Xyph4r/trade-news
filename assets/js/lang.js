// Language toggle. Runs in <head> so the page renders in the chosen language without a flash.
(function () {
  var KEY = "lang";
  var root = document.documentElement;

  function stored() {
    try { return window.localStorage.getItem(KEY); } catch (e) { return null; }
  }
  function store(lang) {
    try { window.localStorage.setItem(KEY, lang); } catch (e) { /* storage blocked: toggle still works for this page */ }
  }
  function apply(lang) {
    lang = lang === "de" ? "de" : "en";
    root.setAttribute("data-lang", lang);
    root.setAttribute("lang", lang);
    return lang;
  }

  var param = new URLSearchParams(window.location.search).get("lang");
  var current = apply(param || stored() || "en");
  if (param) { store(current); }

  document.addEventListener("DOMContentLoaded", function () {
    var btn = document.getElementById("lang-toggle");
    if (!btn) { return; }
    btn.addEventListener("click", function () {
      current = apply(current === "de" ? "en" : "de");
      store(current);
    });
  });
})();
