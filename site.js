(function () {
  var nav = document.getElementById('mainNav');
  if (nav) {
    var onScroll = function () { nav.classList.toggle('scrolled', window.scrollY > 80); };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  // Portfolio slideshow
  var stage = document.getElementById('portfolioStage');
  if (stage) {
    var slides = stage.querySelectorAll('.portfolio-slide');
    var dots = stage.querySelectorAll('.portfolio-dot');
    var counter = document.getElementById('currentNum');
    var progressBar = document.getElementById('progressBar');
    var total = slides.length;
    var current = 0;
    var DURATION = 5500;
    var autoTimer = null;
    var paused = false;
    var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    var startProgress = function () {
      clearTimeout(autoTimer);
      progressBar.style.transition = 'none';
      progressBar.style.width = '0%';
      if (paused || reduceMotion) return;
      setTimeout(function () {
        progressBar.style.transition = 'width ' + DURATION + 'ms linear';
        progressBar.style.width = '100%';
      }, 30);
      autoTimer = setTimeout(function () { goToSlide(current + 1); }, DURATION);
    };

    var goToSlide = function (n) {
      slides[current].classList.remove('active');
      slides[current].setAttribute('aria-hidden', 'true');
      dots[current].classList.remove('active');
      dots[current].removeAttribute('aria-current');
      current = ((n % total) + total) % total;
      slides[current].classList.add('active');
      slides[current].removeAttribute('aria-hidden');
      dots[current].classList.add('active');
      dots[current].setAttribute('aria-current', 'true');
      counter.textContent = String(current + 1).padStart(2, '0');
      startProgress();
    };

    document.getElementById('prevBtn').addEventListener('click', function () { goToSlide(current - 1); });
    document.getElementById('nextBtn').addEventListener('click', function () { goToSlide(current + 1); });
    dots.forEach(function (dot, i) { dot.addEventListener('click', function () { goToSlide(i); }); });

    stage.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowRight') goToSlide(current + 1);
      if (e.key === 'ArrowLeft') goToSlide(current - 1);
    });
    var pause = function () { paused = true; startProgress(); };
    var resume = function () { paused = false; startProgress(); };
    stage.addEventListener('mouseenter', pause);
    stage.addEventListener('mouseleave', resume);
    stage.addEventListener('focusin', pause);
    stage.addEventListener('focusout', resume);

    // Only run the timer while the slideshow is on screen
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (entries) {
        entries.forEach(function (en) { if (en.isIntersecting) { resume(); } else { pause(); } });
      }, { threshold: 0.25 }).observe(stage);
    } else {
      startProgress();
    }
  }

  // Forms (Formspree)
  document.querySelectorAll('form[data-formspree]').forEach(function (form) {
    var btn = form.querySelector('.form-submit');
    var errorBox = form.querySelector('.form-error');
    var success = document.getElementById(form.getAttribute('data-success'));
    var label = btn.textContent;

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      errorBox.classList.remove('show');
      var firstBad = null;
      form.querySelectorAll('[required]').forEach(function (el) {
        var bad = !el.checkValidity();
        el.setAttribute('aria-invalid', bad ? 'true' : 'false');
        if (bad && !firstBad) firstBad = el;
      });
      if (firstBad) {
        errorBox.textContent = 'Please fill in the highlighted fields.';
        errorBox.classList.add('show');
        firstBad.focus();
        return;
      }
      btn.textContent = 'Sending...';
      btn.disabled = true;
      fetch(form.action, { method: 'POST', body: new FormData(form), headers: { 'Accept': 'application/json' } })
        .then(function (res) {
          if (!res.ok) throw new Error('bad status');
          form.style.display = 'none';
          success.classList.add('show');
          success.focus();
        })
        .catch(function () {
          errorBox.innerHTML = 'That didn’t go through. Call or text <a href="tel:+14809735166">(480) 973-5166</a> or email <a href="mailto:Stoneandrose@gmail.com">Stoneandrose@gmail.com</a>.';
          errorBox.classList.add('show');
          btn.textContent = label;
          btn.disabled = false;
        });
    });
  });

  var year = document.getElementById('year');
  if (year) year.textContent = new Date().getFullYear();
})();
