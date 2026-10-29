(function () {
  var KEY = "vyasa.v1.state";
  var SESSION = "vyasa.v1.session";
  var ID = /^[A-Za-z0-9_-]{1,64}$/;

  function has(obj, key) { return Object.prototype.hasOwnProperty.call(obj, key); }
  function readUrl(item, block) { return "/read/" + encodeURIComponent(item) + (block ? "#" + block : ""); }

  function clean(p) {
    if (!p || typeof p !== "object" || !ID.test(p.item) || !ID.test(p.block)) return null;
    var ratio = typeof p.ratio === "number" && p.ratio >= 0 ? Math.min(p.ratio, 1) : 0;
    var text = typeof p.text === "string" ? p.text.slice(0, 80) : "";
    return { item: p.item, block: p.block, ratio: ratio, t: Number(p.t) || 0, text: text };
  }

  function load() {
    var s = null;
    try { s = JSON.parse(localStorage.getItem(KEY)); } catch (e) { s = null; }
    if (!s || typeof s !== "object" || s.v !== 1) s = {};
    return {
      v: 1,
      auto: s.auto !== false,
      last: clean(s.last),
      items: s.items && typeof s.items === "object" && !Array.isArray(s.items) ? s.items : {},
      bookmarks: Array.isArray(s.bookmarks) ? s.bookmarks.map(clean).filter(Boolean) : []
    };
  }

  function save(s) {
    var keys = Object.keys(s.items);
    if (keys.length > 100) {
      keys.sort(function (a, b) { return ((s.items[a] || {}).t || 0) - ((s.items[b] || {}).t || 0); });
      delete s.items[keys[0]];
    }
    try { localStorage.setItem(KEY, JSON.stringify(s)); return true; } catch (e) { return false; }
  }

  // A fresh launch is a new browser session not reached from another page of this site.
  var fresh = false;
  try { fresh = !sessionStorage.getItem(SESSION); sessionStorage.setItem(SESSION, "1"); } catch (e) { fresh = false; }
  if (document.referrer.indexOf(location.origin + "/") === 0) fresh = false;

  function reader(box, item) {
    var blocks = box.querySelectorAll("[id]");
    var ready = false, dirty = false, timer = null, keep = null;

    function current() {
      for (var i = 0; i < blocks.length; i++) {
        var r = blocks[i].getBoundingClientRect();
        if (r.bottom > 0) {
          var ratio = r.top < 0 && r.height ? Math.min(1, -r.top / r.height) : 0;
          return { item: item, block: blocks[i].id, ratio: ratio, t: Date.now() };
        }
      }
      return blocks.length ? { item: item, block: blocks[blocks.length - 1].id, ratio: 1, t: Date.now() } : null;
    }
    function apply(p) {
      var el = p && document.getElementById(p.block);
      if (!el || !box.contains(el) || (el === blocks[0] && p.ratio === 0)) return;
      var r = el.getBoundingClientRect();
      window.scrollTo(0, window.scrollY + r.top + r.height * p.ratio);
    }
    function flush() {
      clearTimeout(timer);
      if (!ready || !dirty) return;
      dirty = false;
      var p = current();
      if (!p) return;
      var s = load();
      s.last = p;
      s.items[item] = p;
      save(s);
    }

    window.addEventListener("scroll", function () {
      if (!ready) return;
      dirty = true;
      clearTimeout(timer);
      timer = setTimeout(flush, 600);
    }, { passive: true });
    document.addEventListener("visibilitychange", function () { if (document.visibilityState === "hidden") flush(); });
    window.addEventListener("pagehide", flush);
    document.addEventListener("click", function (e) { if (e.target.closest && e.target.closest("a")) flush(); }, true);
    document.addEventListener("vyasa:beforefont", function () { keep = current(); });
    document.addEventListener("vyasa:afterfont", function () { apply(keep); dirty = true; flush(); });

    var btn = document.getElementById("bookmark");
    if (btn) btn.addEventListener("click", function () {
      var p = current();
      if (!p) return;
      p.text = document.getElementById(p.block).textContent.trim().slice(0, 80);
      var s = load();
      s.bookmarks = s.bookmarks.filter(function (b) { return b.item !== p.item || b.block !== p.block; });
      s.bookmarks.unshift(p);
      s.bookmarks = s.bookmarks.slice(0, 50);
      btn.textContent = save(s) ? "Bookmarked" : "Could not save (storage blocked)";
    });

    if ("scrollRestoration" in history) history.scrollRestoration = "manual";
    var hash = location.hash.slice(1);
    var start = ID.test(hash) ? { block: hash, ratio: 0 } : clean(load().items[item]);
    var fonts = document.fonts && document.fonts.ready ? document.fonts.ready : Promise.resolve();
    fonts.then(function () {
      requestAnimationFrame(function () {
        apply(start);
        if (ID.test(hash)) history.replaceState(null, "", location.pathname);
        ready = true;
        dirty = true;
        flush();
      });
    });
  }

  function showBookmarks(list, empty, titles) {
    var s = load();
    list.textContent = "";
    empty.hidden = s.bookmarks.length > 0;
    s.bookmarks.forEach(function (b, i) {
      var li = document.createElement("li");
      var ok = has(titles, b.item);
      var link = document.createElement(ok ? "a" : "span");
      link.textContent = ok ? titles[b.item] : "Item no longer available";
      if (ok) link.href = readUrl(b.item, b.block);
      var small = document.createElement("small");
      small.textContent = b.text;
      var del = document.createElement("button");
      del.type = "button";
      del.textContent = "Remove";
      del.addEventListener("click", function () {
        var s2 = load();
        s2.bookmarks.splice(i, 1);
        save(s2);
        showBookmarks(list, empty, titles);
      });
      li.appendChild(link);
      li.appendChild(small);
      li.appendChild(del);
      list.appendChild(li);
    });
  }

  function home(box) {
    var titles = {};
    try { titles = JSON.parse(box.getAttribute("data-items")) || {}; } catch (e) { titles = {}; }
    var s = load();
    var last = s.last && has(titles, s.last.item) ? s.last : null;
    if (last && s.auto && fresh) { location.replace(readUrl(last.item)); return; }

    if (last) {
      var go = document.getElementById("resume-go");
      go.querySelector("a").href = readUrl(last.item);
      go.querySelector("span").textContent = titles[last.item];
      go.hidden = false;
      document.getElementById("resume-empty").hidden = true;
    }
    var auto = document.getElementById("auto-resume");
    auto.checked = s.auto;
    auto.addEventListener("change", function () {
      var s2 = load();
      s2.auto = auto.checked;
      save(s2);
    });
    showBookmarks(document.getElementById("bookmarks"), document.getElementById("bookmarks-empty"), titles);
  }

  function offerUpdate(worker) {
    var bar = document.createElement("div");
    bar.className = "update";
    bar.textContent = "A new version is available. ";
    var btn = document.createElement("button");
    btn.type = "button";
    btn.textContent = "Reload";
    btn.addEventListener("click", function () { worker.postMessage("skipWaiting"); });
    bar.appendChild(btn);
    document.body.appendChild(bar);
  }

  if ("serviceWorker" in navigator) {
    window.addEventListener("load", function () {
      navigator.serviceWorker.register("/sw.js", { scope: "/" }).then(function (reg) {
        if (reg.waiting && navigator.serviceWorker.controller) offerUpdate(reg.waiting);
        reg.addEventListener("updatefound", function () {
          var w = reg.installing;
          if (w) w.addEventListener("statechange", function () {
            if (w.state === "installed" && navigator.serviceWorker.controller) offerUpdate(w);
          });
        });
      }).catch(function () {});
    });
    var hadController = !!navigator.serviceWorker.controller;
    navigator.serviceWorker.addEventListener("controllerchange", function () { if (hadController) location.reload(); });
  }

  var box = document.querySelector(".reader[data-item]");
  if (box && ID.test(box.getAttribute("data-item"))) reader(box, box.getAttribute("data-item"));
  var resume = document.getElementById("resume");
  if (resume) home(resume);
})();
