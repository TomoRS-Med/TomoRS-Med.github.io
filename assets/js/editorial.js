(() => {
  'use strict';
  document.documentElement.classList.add('js');
  const navigation = document.getElementById('site-navigation');
  const toggle = document.querySelector('.menu-toggle');
  function closeMenu() {
    navigation.classList.remove('is-open');
    toggle.setAttribute('aria-expanded', 'false');
  }
  toggle.addEventListener('click', () => {
    const open = toggle.getAttribute('aria-expanded') !== 'true';
    toggle.setAttribute('aria-expanded', String(open));
    navigation.classList.toggle('is-open', open);
  });
  navigation.addEventListener('click', (event) => {
    if (event.target.closest('a')) closeMenu();
  });
  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && toggle.getAttribute('aria-expanded') === 'true') {
      closeMenu();
      toggle.focus();
    }
  });
  document.addEventListener('click', (event) => {
    if (!event.target.closest('.header-actions')) closeMenu();
  });
  window.addEventListener('resize', () => {
    if (window.innerWidth > 900) closeMenu();
  });
  const cvView = document.querySelector('[data-cv-view]');
  const cvDocument = document.getElementById('cv-document');
  if (cvView && cvDocument) {
    cvView.setAttribute('role', 'button');
    cvView.setAttribute('aria-controls', cvDocument.id);
    cvView.setAttribute('aria-expanded', 'false');
    cvView.addEventListener('click', (event) => {
      if (event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
      event.preventDefault();
      const open = cvView.getAttribute('aria-expanded') !== 'true';
      if (open) {
        const frame = cvDocument.querySelector('iframe');
        if (!frame.hasAttribute('src')) frame.setAttribute('src', frame.dataset.src);
      }
      cvDocument.hidden = !open;
      cvView.setAttribute('aria-expanded', String(open));
    });
    cvView.addEventListener('keydown', (event) => {
      if (event.key === ' ') {
        event.preventDefault();
        cvView.click();
      }
    });
  }
  const switcher = document.querySelector('[data-language-switch]');
  const alternate = switcher.getAttribute('href');
  const homeAnchors = ['about', 'research', 'publications', 'piano', 'lecture', 'contact'];
  function syncLanguageLink() {
    const anchor = window.location.hash.slice(1);
    const page = document.documentElement.dataset.page;
    const preserve = (page === 'home' && homeAnchors.includes(anchor)) ||
      (page === 'lecture' && /^slide-\d+$/.test(anchor) && document.getElementById(anchor));
    switcher.setAttribute('href', alternate + (preserve ? '#' + anchor : ''));
  }
  if (document.documentElement.lang === 'ja' && document.documentElement.dataset.page === 'home') {
    const legacy = {
      '研究': '/japanese/#research', '論文': '/japanese/#publications',
      'ピアノについて': '/japanese/#piano', '演奏活動': '/japanese/#piano',
      'ピアノの受賞歴': '/japanese/#piano', 'マスターコース': '/japanese/#piano',
      '演奏動画': '/japanese/#piano', 'email': '/japanese/#contact',
      '経歴': '/japanese/cv/#cv-0', '学会発表': '/japanese/cv/#cv-1',
      '資格': '/japanese/cv/#cv-2', '受賞歴表彰歴': '/japanese/cv/#cv-3',
      '臨床経験': '/japanese/cv/#cv-4', '研究経験': '/japanese/cv/#cv-5',
      '奨学金': '/japanese/cv/#cv-6', '専門的貢献活動-professional-services': '/japanese/cv/#cv-7'
    };
    let anchor;
    try { anchor = decodeURIComponent(window.location.hash.slice(1)); } catch (_) { anchor = ''; }
    if (legacy[anchor]) window.location.replace(legacy[anchor]);
  }
  syncLanguageLink();
  window.addEventListener('hashchange', syncLanguageLink);
  switcher.addEventListener('click', () => {
    const page = document.documentElement.dataset.page;
    if (page === 'cv') return;
    const nodes = page === 'home'
      ? homeAnchors.map((id) => document.getElementById(id))
      : [...document.querySelectorAll('.lecture-slide[id]')];
    const threshold = Math.max(120, window.innerHeight * 0.2);
    const current = nodes.filter((node) => node && node.getBoundingClientRect().top <= threshold).pop();
    switcher.setAttribute('href', alternate + (current ? '#' + current.id : ''));
  });
})();
