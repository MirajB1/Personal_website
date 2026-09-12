/* ══════════════════════════════════════════════════════════════
   Miraj Bhattarai — portfolio
   Vanilla JS, no dependencies.
     · intro animation  · theme switch  · scroll reveal
     · project tabs     · visitor count
   Everything that can fail, fails quietly and hides itself.
   ══════════════════════════════════════════════════════════════ */
(function () {
  'use strict';

  var root    = document.documentElement;
  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function $(s, c) { return (c || document).querySelector(s); }
  function $$(s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); }
  function store(fn, fb) { try { return fn(); } catch (e) { return fb; } }

  /* ─────────────────────────── intro ───────────────────────────
     The name rises, a rule draws under it, then the panel lifts away.
     Plays on every load, skippable with any key or click, and skipped
     outright for reduced motion. A failsafe removes it regardless. */
  function boot() {
    var el = document.getElementById('boot');
    if (!el) return;

    if (reduced) { el.remove(); return; }

    var done = false, timers = [];

    function finish() {
      if (done) return;
      done = true;
      timers.forEach(clearTimeout);
      el.classList.add('out');
      timers.push(window.setTimeout(function () { if (el.parentNode) el.remove(); }, 720));
      window.removeEventListener('keydown', finish);
      window.removeEventListener('pointerdown', finish);
    }

    window.addEventListener('keydown', finish);
    window.addEventListener('pointerdown', finish);

    timers.push(window.setTimeout(finish, 1300));   // normal end of the intro
    window.setTimeout(function () {                  // failsafe, never trapped
      if (done) return;
      el.classList.add('out');
      window.setTimeout(function () { if (el.parentNode) el.remove(); }, 720);
      done = true;
    }, 3500);
  }

  /* ─────────────────────────── theme ─────────────────────────── */
  function theme() {
    var btn = $('#themeBtn');
    if (!btn) return;
    var mq = window.matchMedia('(prefers-color-scheme: light)');

    function apply(t, remember) {
      root.setAttribute('data-theme', t);
      if (remember) {
        root.removeAttribute('data-theme-auto');
        store(function () { localStorage.setItem('mb-theme', t); });
      }
      btn.setAttribute('aria-label', t === 'dark' ? 'Switch to light theme' : 'Switch to dark theme');
    }

    btn.addEventListener('click', function () {
      apply(root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark', true);
    });

    // keep following the OS until the visitor makes a choice
    var onChange = function (e) {
      if (root.getAttribute('data-theme-auto')) apply(e.matches ? 'light' : 'dark', false);
    };
    if (mq.addEventListener) mq.addEventListener('change', onChange);
    else if (mq.addListener) mq.addListener(onChange);

    apply(root.getAttribute('data-theme'), false);
  }

  /* ─────────────────────────── chrome: bar, nav, reveal ─────────────────────────── */
  function chrome() {
    var bar = $('#bar'), nav = $('#nav'), burger = $('#burger');

    var ticking = false;
    function onScroll() {
      if (bar) bar.classList.toggle('stuck', (window.scrollY || 0) > 6);
    }
    window.addEventListener('scroll', function () {
      if (ticking) return;
      ticking = true;
      requestAnimationFrame(function () { onScroll(); ticking = false; });
    }, { passive: true });
    onScroll();

    function closeNav() {
      if (!nav || !burger) return;
      nav.classList.remove('open');
      burger.setAttribute('aria-expanded', 'false');
      burger.setAttribute('aria-label', 'Open menu');
    }
    if (nav && burger) {
      burger.addEventListener('click', function () {
        var open = nav.classList.toggle('open');
        burger.setAttribute('aria-expanded', String(open));
        burger.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
      });
      nav.addEventListener('click', function (e) { if (e.target.closest('a')) closeNav(); });
      document.addEventListener('keydown', function (e) { if (e.key === 'Escape') closeNav(); });
      document.addEventListener('click', function (e) {
        if (!nav.classList.contains('open')) return;
        if (e.target.closest('#nav') || e.target.closest('#burger')) return;
        closeNav();
      });
      window.addEventListener('resize', function () { if (window.innerWidth > 900) closeNav(); });
    }

    // one-shot reveal, then the transition is dropped entirely
    var items = $$('.r');
    if (reduced || !('IntersectionObserver' in window)) {
      items.forEach(function (el) { el.classList.add('in', 'settled'); });
    } else {
      var io = new IntersectionObserver(function (entries, obs) {
        entries.forEach(function (en) {
          if (!en.isIntersecting) return;
          var el = en.target;
          el.classList.add('in');
          obs.unobserve(el);
          el.addEventListener('transitionend', function h(ev) {
            if (ev.propertyName !== 'opacity') return;
            el.classList.add('settled');
            el.removeEventListener('transitionend', h);
          });
        });
      }, { rootMargin: '0px 0px -6% 0px', threshold: 0.06 });
      items.forEach(function (el) { io.observe(el); });
    }

    // active nav link
    var secs = $$('main section[id]'), links = $$('#nav a[href^="#"]');
    if ('IntersectionObserver' in window && secs.length) {
      var vis = {};
      var spy = new IntersectionObserver(function (entries) {
        entries.forEach(function (e) { vis[e.target.id] = e.intersectionRatio; });
        var best = null, r = 0;
        Object.keys(vis).forEach(function (id) { if (vis[id] > r) { r = vis[id]; best = id; } });
        if (best && r > 0) links.forEach(function (a) { a.classList.toggle('on', a.getAttribute('href') === '#' + best); });
      }, { rootMargin: '-45% 0px -45% 0px', threshold: [0, .2, .5, .8, 1] });
      secs.forEach(function (s) { spy.observe(s); });
    }

    var y = $('#year'); if (y) y.textContent = new Date().getFullYear();
  }

  /* ─────────────────────────── project tabs ─────────────────────────── */
  function projects() {
    var tabs = $$('.pj-tab'), panes = $$('.pj-pane');
    if (!tabs.length) return;

    function show(n, focus) {
      tabs.forEach(function (t) {
        var on = t.dataset.i === String(n);
        t.classList.toggle('is-on', on);
        t.setAttribute('aria-selected', String(on));
        t.tabIndex = on ? 0 : -1;
        if (on && focus) t.focus();
      });
      panes.forEach(function (p) {
        var on = p.id === 'pj-' + n;
        p.hidden = !on;
        p.classList.toggle('is-on', on);
      });
    }

    tabs.forEach(function (t) {
      t.addEventListener('click', function () { show(t.dataset.i, false); });
      t.addEventListener('keydown', function (e) {
        var i = tabs.indexOf(t), n = null;
        if (e.key === 'ArrowRight' || e.key === 'ArrowDown') n = (i + 1) % tabs.length;
        else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') n = (i - 1 + tabs.length) % tabs.length;
        else if (e.key === 'Home') n = 0;
        else if (e.key === 'End') n = tabs.length - 1;
        if (n === null) return;
        e.preventDefault();
        show(tabs[n].dataset.i, true);
      });
    });
    show(1, false);
  }

  /* ─────────────────────────── copy to clipboard ─────────────────────────── */
  function copy() {
    $$('.copy').forEach(function (btn) {
      var label = $('span', btn), use = $('use', btn), original = label ? label.textContent : '';
      btn.addEventListener('click', function () {
        var v = btn.getAttribute('data-copy') || '';
        function done() {
          btn.classList.add('done');
          if (label) label.textContent = 'copied';
          if (use) use.setAttribute('href', '#i-check');
          setTimeout(function () {
            btn.classList.remove('done');
            if (label) label.textContent = original;
            if (use) use.setAttribute('href', '#i-copy');
          }, 1800);
        }
        function fallback() {
          var ta = document.createElement('textarea');
          ta.value = v; ta.setAttribute('readonly', ''); ta.style.cssText = 'position:fixed;opacity:0';
          document.body.appendChild(ta); ta.select();
          try { document.execCommand('copy'); done(); } catch (e) {}
          document.body.removeChild(ta);
        }
        if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(v).then(done, fallback);
        } else { fallback(); }
      });
    });
  }

  /* ─────────────────────────── visitor count ─────────────────────────── */
  function visitors() {
    var wrap = $('#visits'), out = $('#visitsCount');
    if (!wrap || !out) return;

    var NS = 'mirajbhattarai-com-np', KEY = 'site-visits';
    var counted = store(function () { return sessionStorage.getItem('mb-counted'); }, '1');
    var verb = counted ? 'get' : 'hit';

    fetch('https://abacus.jasoncameron.dev/' + verb + '/' + NS + '/' + KEY, { cache: 'no-store' })
      .then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); })
      .then(function (d) {
        var n = d && typeof d.value === 'number' ? d.value : null;
        if (n === null) throw new Error('shape');
        store(function () { sessionStorage.setItem('mb-counted', '1'); });
        out.textContent = n.toLocaleString();
        wrap.hidden = false;
      })
      .catch(function () { wrap.hidden = true; });
  }

  /* ─────────────────────────── go ─────────────────────────── */
  document.addEventListener('DOMContentLoaded', function () {
    boot(); theme(); chrome(); projects(); copy(); visitors();
  });
})();
