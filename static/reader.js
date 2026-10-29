(function () {
  var KEY_SIZE = "vyasa.v1.fontStep";
  var KEY_THEME = "vyasa.v1.theme";
  var SIZES = [1, 1.125, 1.25, 1.5, 1.75, 2];
  var root = document.documentElement;

  function get(key) {
    try { return localStorage.getItem(key); } catch (e) { return null; }
  }
  function set(key, value) {
    try { localStorage.setItem(key, value); } catch (e) { /* storage blocked: preference lasts this page only */ }
  }

  var step = parseInt(get(KEY_SIZE), 10);
  if (!(step >= 0 && step < SIZES.length)) step = 1;
  var saved = get(KEY_THEME);
  if (saved === "light" || saved === "dark") root.setAttribute("data-theme", saved);
  root.style.setProperty("--reader-size", SIZES[step] + "rem");

  function currentTheme() {
    return root.getAttribute("data-theme") ||
      (window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light");
  }

  document.addEventListener("DOMContentLoaded", function () {
    var dec = document.getElementById("font-dec");
    var inc = document.getElementById("font-inc");
    var themeBtn = document.getElementById("theme-toggle");
    if (!dec || !inc || !themeBtn) return;

    function showSize() {
      root.style.setProperty("--reader-size", SIZES[step] + "rem");
      dec.disabled = step === 0;
      inc.disabled = step === SIZES.length - 1;
    }
    function showTheme() {
      themeBtn.textContent = currentTheme() === "dark" ? "Light mode" : "Dark mode";
    }

    dec.addEventListener("click", function () { step -= 1; set(KEY_SIZE, step); showSize(); });
    inc.addEventListener("click", function () { step += 1; set(KEY_SIZE, step); showSize(); });
    themeBtn.addEventListener("click", function () {
      var next = currentTheme() === "dark" ? "light" : "dark";
      root.setAttribute("data-theme", next);
      set(KEY_THEME, next);
      showTheme();
    });
    showSize();
    showTheme();
  });
})();
