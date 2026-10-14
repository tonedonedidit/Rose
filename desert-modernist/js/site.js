(function () {
  'use strict';

  var FORMSPREE = 'https://formspree.io/f/mlgpprov';

  /* Nav border on scroll */
  var nav = document.getElementById('mainNav');
  if (nav) {
    var onScroll = function () { nav.classList.toggle('scrolled', window.scrollY > 20); };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  /* Portfolio viewer */
  var tiles = document.querySelectorAll('.tile');
  var lightbox = document.getElementById('lightbox');
  if (tiles.length && lightbox) {
    var photos = [];
    tiles.forEach(function (t) {
      var img = t.querySelector('img');
      photos.push({ src: img.getAttribute('src'), alt: img.getAttribute('alt') });
    });
    var total = photos.length;
    var current = 0;
    var lbImg = document.getElementById('lbImg');
    var lbCount = document.getElementById('lbCount');
    var lastFocus = null;

    var show = function (n) {
      current = ((n % total) + total) % total;
      lbImg.src = photos[current].src;
      lbImg.alt = photos[current].alt;
      lbCount.textContent = String(current + 1).padStart(2, '0') + ' / ' + String(total).padStart(2, '0');
    };
    var openBox = function (n) {
      lastFocus = document.activeElement;
      show(n);
      lightbox.classList.add('open');
      document.body.style.overflow = 'hidden';
      document.getElementById('lbClose').focus();
    };
    var closeBox = function () {
      lightbox.classList.remove('open');
      document.body.style.overflow = '';
      if (lastFocus) lastFocus.focus();
    };
    tiles.forEach(function (t, i) { t.addEventListener('click', function () { openBox(i); }); });
    document.getElementById('lbClose').addEventListener('click', closeBox);
    document.getElementById('prevBtn').addEventListener('click', function () { show(current - 1); });
    document.getElementById('nextBtn').addEventListener('click', function () { show(current + 1); });
    lightbox.addEventListener('click', function (e) { if (e.target === lightbox) closeBox(); });
    document.addEventListener('keydown', function (e) {
      if (!lightbox.classList.contains('open')) return;
      if (e.key === 'ArrowRight') show(current + 1);
      if (e.key === 'ArrowLeft') show(current - 1);
      if (e.key === 'Escape') closeBox();
    });
  }

  /* Lead forms. Posts to the Resend-backed endpoint first; if that endpoint is missing or down,
     falls back to Formspree so no lead is lost. */
  function field(form, name) {
    var el = form.elements[name];
    return el ? el.value.trim() : '';
  }

  function post(url, payload) {
    return fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
      body: JSON.stringify(payload)
    });
  }

  document.querySelectorAll('form[data-lead]').forEach(function (form) {
    var type = form.getAttribute('data-lead');
    var endpoint = form.getAttribute('data-endpoint');
    var errorEl = form.querySelector('.form-error');
    var btn = form.querySelector('.form-submit');
    var success = document.getElementById(form.getAttribute('data-success'));
    var idleText = btn.textContent;

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      errorEl.textContent = '';

      var payload = {
        type: type,
        firstName: field(form, 'firstName'),
        lastName: field(form, 'lastName'),
        company: field(form, 'company'),
        email: field(form, 'email'),
        phone: field(form, 'phone'),
        service: field(form, 'service'),
        message: field(form, 'message'),
        website: field(form, 'website'),
        page: location.href
      };

      var needService = form.elements.service && form.elements.service.required;
      if (!payload.firstName || !payload.email || (needService && !payload.service) || (type === 'partner' && !payload.company)) {
        errorEl.textContent = type === 'partner'
          ? 'Please fill in your name, company, email, and trade.'
          : 'Please fill in your name, email, and project type.';
        return;
      }
      if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(payload.email)) {
        errorEl.textContent = 'Please enter a valid email address.';
        return;
      }

      btn.textContent = 'Sending...';
      btn.disabled = true;

      var done = function () {
        form.style.display = 'none';
        if (success) { success.classList.add('show'); success.setAttribute('tabindex', '-1'); success.focus(); }
      };
      var fail = function () {
        errorEl.textContent = 'Something went wrong. Please call (480) 650-8957 or email tony@stoneandrosellc.com';
        btn.textContent = idleText;
        btn.disabled = false;
      };
      var viaFormspree = function () {
        return post(FORMSPREE, {
          name: (payload.firstName + ' ' + payload.lastName).trim(),
          email: payload.email,
          phone: payload.phone,
          company: payload.company,
          projectType: payload.service,
          leadType: type,
          message: payload.message,
          _subject: (type === 'partner' ? 'Contractor partnership inquiry: ' : 'New project inquiry: ') + payload.firstName
        }).then(function (r) { if (r.ok) done(); else fail(); });
      };

      post(endpoint, payload).then(function (r) {
        if (r.ok) { done(); return; }
        if (r.status === 400 || r.status === 422) {
          return r.json().then(function (j) { errorEl.textContent = (j && j.error) || 'Please check the form and try again.'; btn.textContent = idleText; btn.disabled = false; }, fail);
        }
        return viaFormspree();
      }).catch(function () { return viaFormspree().catch(fail); });
    });
  });
})();
