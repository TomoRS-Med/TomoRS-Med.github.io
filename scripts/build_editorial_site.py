#!/usr/bin/env python3
"""Generate the bilingual static portfolio using only Python's standard library."""
from pathlib import Path
from html import escape
import json
import re

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / "content/editorial.json").read_text())
ORIGIN = "https://tomors-med.github.io"
LINKS = DATA["links"]
ORDER = ("about", "research", "publications", "piano", "lecture", "contact")
TEXT = {
    "en": {
        "about": "About", "research": "Research", "publications": "Publications",
        "piano": "Piano", "lecture": "Lecture", "contact": "Contact",
        "skip": "Skip to content", "menu": "Menu", "switch": "日本語",
        "statement": "Read the full research statement", "article": "Article",
        "press": "Press release (Japanese)", "code": "Code",
        "conferences": "Academic presentations", "watch": "Watch the performance",
        "performance": "22nd Chopin International Piano Competition in Asia · Chopinist B · Gold Prize",
        "read_lecture": "Read the lecture", "cv": "View career history", "cv_nav": "Background",
        "cv_note": "Education, research experience, clinical activities, and professional services.",
        "cv_view": "View CV", "cv_download": "Download CV", "cv_open": "Open PDF in a new tab",
        "cv_file_note": "Curriculum vitae · PDF", "cv_viewer_title": "Tomohide R. Sato’s curriculum vitae",
        "back": "Back to the profile",
        "lecture_date": "July 2026 · Fukuoka International College of Music",
        "top": "Back to top", "full_cv": "Background", "cv_subtitle": "Academic & clinical background",
        "address": "For research, clinical, and music-related enquiries.",
    },
    "ja": {
        "about": "プロフィール", "research": "研究", "publications": "論文",
        "piano": "ピアノ", "lecture": "講演", "contact": "お問い合わせ",
        "skip": "本文へ移動", "menu": "メニュー", "switch": "English",
        "statement": "研究についての全文を読む", "article": "論文",
        "press": "プレスリリース", "code": "コード",
        "conferences": "学会発表一覧", "watch": "演奏動画を見る",
        "performance": "第22回ショパン国際ピアノコンクール in Asia · ショパニストB部門 · アジア大会金賞",
        "read_lecture": "講演を読む", "cv": "詳しい経歴を見る", "cv_nav": "経歴",
        "cv_note": "学歴・研究経験・臨床経験・資格・受賞歴・奨学金・専門的貢献活動。",
        "cv_view": "CVを閲覧", "cv_download": "CVをダウンロード", "cv_open": "PDFを別タブで開く",
        "cv_file_note": "CV（英語・PDF）", "cv_viewer_title": "佐藤智英のCV",
        "back": "プロフィールに戻る",
        "lecture_date": "2026年7月 · 福岡国際音楽大学",
        "top": "ページの先頭へ", "full_cv": "経歴", "cv_subtitle": "Academic & clinical background",
        "address": "研究・医療・音楽に関するご連絡はこちらへ。",
    },
}


def home_path(lang):
    return "/japanese/" if lang == "ja" else "/"


def cv_path(lang):
    return "/japanese/cv/" if lang == "ja" else "/cv/"


def lecture_path(lang):
    return "/lecture_brainmusic/" if lang == "ja" else "/lecture_brainmusic_en/"


def link(url, label, cls="", external=False):
    attrs = f' class="{cls}"' if cls else ""
    if external:
        attrs += ' target="_blank" rel="noopener noreferrer"'
    return f'<a href="{escape(url, quote=True)}"{attrs}>{label}</a>'


def timeline(entries):
    rows = "".join(f'<div class="timeline-row"><dt>{escape(e["date"])}</dt><dd>{e["html"]}</dd></div>' for e in entries)
    return f'<dl class="timeline">{rows}</dl>'


def shell(lang, kind, title, body):
    t = TEXT[lang]
    other = "ja" if lang == "en" else "en"
    path_for = {"home": home_path, "cv": cv_path, "lecture": lecture_path}
    path = path_for[kind](lang)
    alternate = path_for[kind](other)
    current_home = kind == "home"
    navigation = "".join(link(("" if current_home else home_path(lang)) + "#" + key, escape(t[key])) for key in ORDER)
    navigation += link(cv_path(lang), t["cv_nav"], "cv-nav" + (" is-active" if kind == "cv" else ""))
    identity = DATA["locales"][lang]
    description = "佐藤智英の公式サイト。睡眠・神経ダイナミクスの研究、臨床、ピアノ、講演。" if lang == "ja" else "Tomohide R. Sato. Physician-scientist studying sleep, brain-state transitions, and biological dynamics. Research, clinical work, piano, and lectures."
    lang_switch = f'<a class="language-switch" href="{alternate}" lang="{other}" hreflang="{other}" data-language-switch>{t["switch"]}</a>'
    socials = "".join(link(LINKS[k], name, external=True) for k, name in [("researchmap", "researchmap"), ("google_scholar", "Google Scholar"), ("orcid", "ORCID"), ("researchgate", "ResearchGate"), ("github", "GitHub"), ("linkedin", "LinkedIn"), ("x", "X"), ("facebook", "Facebook")])
    return f'''<!doctype html>
<html lang="{lang}" data-page="{kind}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(title)} · Tomohide R. Sato</title>
  <meta name="description" content="{escape(description, quote=True)}">
  <meta name="theme-color" content="#ffffff">
  <link rel="canonical" href="{ORIGIN}{path}">
  <link rel="alternate" hreflang="en" href="{ORIGIN}{path_for[kind]('en')}">
  <link rel="alternate" hreflang="ja" href="{ORIGIN}{path_for[kind]('ja')}">
  <link rel="alternate" hreflang="x-default" href="{ORIGIN}{path_for[kind]('en')}">
  <meta property="og:type" content="website">
  <meta property="og:title" content="{escape(title, quote=True)} · Tomohide R. Sato">
  <meta property="og:description" content="{escape(description, quote=True)}">
  <meta property="og:url" content="{ORIGIN}{path}">
  <meta property="og:image" content="{ORIGIN}/assets/img/IMG_2824.jpeg">
  <meta property="og:locale" content="{'ja_JP' if lang == 'ja' else 'en_US'}">
  <link rel="stylesheet" href="/assets/css/editorial.css?v=20261011">
  <script src="/assets/js/editorial.js?v=20261011" defer></script>
</head>
<body id="top">
  <a class="skip-link" href="#main">{t['skip']}</a>
  <header class="site-header">
    <div class="header-inner">
      {link(home_path(lang), 'Tomohide R. Sato', 'wordmark')}
      <div class="header-actions">
        <button class="menu-toggle" type="button" aria-controls="site-navigation" aria-expanded="false">{t['menu']} <span aria-hidden="true">+</span></button>
        <nav id="site-navigation" aria-label="{'メインメニュー' if lang == 'ja' else 'Main navigation'}">{navigation}</nav>
        {lang_switch}
      </div>
    </div>
  </header>
  <main id="main" tabindex="-1">{body}</main>
  <footer class="site-footer wrap">
    <div class="footer-upper">
      <p class="footer-name">Tomohide R. Sato<span>{escape(identity['role'])}</span></p>
      <div class="social-links">{socials}</div>
    </div>
    <div class="footer-lower"><small>© 2026 Tomohide R. Sato</small>{link('#top', t['top'] + ' ↑')}</div>
  </footer>
</body>
</html>
'''


def section(lang, key, content, cls=""):
    return f'<section id="{key}" class="editorial-section {cls}" aria-labelledby="heading-{key}"><div class="section-label"><h2 id="heading-{key}">{TEXT[lang][key]}</h2></div><div class="section-content">{content}</div></section>'


def home(lang):
    d, t = DATA["locales"][lang], TEXT[lang]
    role = d['role']
    body = f'''<div class="hero-title wrap"><h1>Tomohide R. Sato</h1><p>{escape(role)}</p></div>
    <figure class="hero-photo"><img src="/assets/img/IMG_2824.jpeg" alt="{'ピアノを演奏する佐藤智英' if lang == 'ja' else 'Tomohide R. Sato playing the piano'}" width="2048" height="2115" fetchpriority="high" decoding="async"></figure>
    <div class="wrap home-content">'''
    bio = "".join(f'<p>{p}</p>' for p in d["bio"])
    about_links = link(cv_path(lang), t["cv"] + ' →', 'text-link') + link(LINKS['orcid'], 'ORCID ↗', 'text-link', True) + link(LINKS['researchmap'], 'researchmap ↗', 'text-link', True)
    body += section(lang, 'about', f'<p class="identity-name">{escape(d["name"])}</p>{bio}<div class="inline-links">{about_links}</div>')
    topics = "".join(f'<div class="research-topic"><h3>{escape(x["title"])}</h3><p>{escape(x["text"])}</p></div>' for x in d['topics'])
    full = "".join(f'<p>{p}</p>' for p in d['research_full'])
    body += section(lang, 'research', f'<p class="lead">{escape(d["research_intro"])}</p><div class="research-topics">{topics}</div><details class="reading-details"><summary>{t["statement"]}<span aria-hidden="true">+</span></summary><div class="full-statement">{full}</div></details>')
    publications = []
    for p in DATA["publications"]:
        title, authors, journal = [p.get(k + '_ja', p[k]) if lang == 'ja' else p[k] for k in ['title', 'authors', 'journal']]
        actions = [link(p['url'], t['article'] + ' ↗', 'text-link', True)]
        for k in ['press', 'code']:
            if k in p:
                actions.append(link(p[k], t[k] + ' ↗', 'text-link', True))
        publications.append(f'<li class="publication"><time datetime="{p["year"]}">{p["year"]}</time><div><h3>{escape(title)}</h3><p class="publication-authors">{escape(authors.rstrip("."))}†.</p><p class="publication-journal">{escape(journal)} · {p["year"]}</p><div class="inline-links">{"".join(actions)}</div></div></li>')
    correspondence = '† 責任著者' if lang == 'ja' else '† Corresponding author'
    pub_links = link(LINKS['google_scholar'], 'Google Scholar ↗', 'text-link', True) + link(cv_path(lang) + '#cv-3' if lang == 'en' else cv_path(lang) + '#cv-1', t['conferences'] + ' →', 'text-link')
    body += section(lang, 'publications', '<ol class="publication-list">' + ''.join(publications) + f'</ol><p class="correspondence">{correspondence}</p><div class="inline-links">{pub_links}</div>')
    performances, awards, courses = d['piano_sections']
    photo_alt = 'ホールでグランドピアノを演奏する佐藤智英' if lang == 'ja' else 'Tomohide R. Sato playing a grand piano in a concert hall'
    piano = f'<p class="lead piano-intro">{escape(d["piano_intro"])}</p><figure class="piano-photo"><img src="/assets/img/IMG_8331.jpeg" alt="{photo_alt}" width="1512" height="2048" loading="lazy" decoding="async"></figure><h3 class="small-heading">{escape(performances["title"])}</h3>{timeline(performances["entries"])}'
    for s in [awards, courses]:
        piano += f'<details class="reading-details"><summary>{escape(s["title"])}<span aria-hidden="true">+</span></summary>{timeline(s["entries"])}</details>'
    piano += f'<div class="performance-link">{link(LINKS["youtube"], t["watch"] + " ↗", "text-link", True)}<p>{escape(t["performance"])}</p></div>'
    body += section(lang, 'piano', piano)
    lecture_image = '1a.jpeg' if lang == 'ja' else '1a_en.jpeg'
    lecture = f'<a class="lecture-image" href="{lecture_path(lang)}" aria-label="{t["read_lecture"]}"><img src="/assets/img/{lecture_image}" alt="From Brain Whisper to Human Experience" width="1920" height="1080" loading="lazy" decoding="async"></a><p class="eyebrow">{escape(t["lecture_date"])}</p><h3 class="lecture-title">From Brain Whisper<br>to Human Experience</h3><p>{escape(d["lecture_intro"])}</p>{link(lecture_path(lang), t["read_lecture"] + " →", "text-link")}'
    body += section(lang, 'lecture', lecture)
    body += f'<aside class="cv-banner"><p><span>{t["cv_nav"]}</span>{escape(t["cv_note"])}</p>{link(cv_path(lang), t["cv"] + " →", "text-link")}</aside>'
    contact = f'<p>{escape(t["address"])}</p><div class="email-links">{link("mailto:chopinist@g.ecc.u-tokyo.ac.jp", "chopinist@g.ecc.u-tokyo.ac.jp")}{link("mailto:amadeusk31025@gmail.com", "amadeusk31025@gmail.com")}</div>'
    body += section(lang, 'contact', contact)
    body += '</div>'
    return shell(lang, 'home', '佐藤智英' if lang == 'ja' else 'Physician-scientist & Pianist', body)


def cv(lang):
    d, t = DATA['locales'][lang], TEXT[lang]
    pdf = escape(LINKS['cv'], quote=True)
    document = f'''<div class="cv-file">
      <p class="cv-file-note">{t['cv_file_note']}</p>
      <div class="cv-file-actions">
        <a class="document-button cv-view-button" href="{pdf}" data-cv-view><span>{t['cv_view']}</span><span class="document-toggle" aria-hidden="true">+</span></a>
        <a class="document-button" href="{pdf}" download="Tomohide_R_Sato.pdf">{t['cv_download']} <span aria-hidden="true">↓</span></a>
      </div>
      <div id="cv-document" class="cv-viewer" hidden>
        <iframe data-src="{pdf}" title="{t['cv_viewer_title']}"></iframe>
        <p>{link(LINKS['cv'], t['cv_open'] + ' ↗', 'text-link', True)}</p>
      </div>
    </div>'''
    toc = ''.join(link('#cv-' + str(i), escape(s['title'])) for i, s in enumerate(d['cv']))
    body = f'<div class="wrap cv-page"><div class="page-heading"><p class="eyebrow">Tomohide R. Sato / 佐藤智英</p><h1>{t["full_cv"]}</h1><p class="page-subtitle">{t["cv_subtitle"]}</p>{document}</div><nav class="cv-toc" aria-label="{"経歴の目次" if lang == "ja" else "Background contents"}">{toc}</nav>'
    for i, s in enumerate(d['cv']):
        body += f'<section id="cv-{i}" class="cv-section" aria-labelledby="cv-heading-{i}"><h2 id="cv-heading-{i}">{escape(s["title"])}</h2>{timeline(s["entries"])}</section>'
    body += f'<div class="return-link">{link(home_path(lang), t["back"] + " →", "text-link")}</div></div>'
    return shell(lang, 'cv', t['full_cv'], body)


def lecture(lang):
    t = TEXT[lang]
    content = (ROOT / f'content/lecture-{lang}.html').read_text()
    # Keep all original slide copy and illustrations while deferring offscreen images.
    content = re.sub(r'<img\s', '<img loading="lazy" decoding="async" ', content)
    body = f'<article class="wrap lecture-page"><div class="page-heading"><p class="eyebrow">{escape(t["lecture_date"])}</p><h1>From Brain Whisper<br>to Human Experience</h1></div><div class="lecture-reading">{content}</div><div class="return-link">{link(home_path(lang) + "#lecture", t["back"] + " →", "text-link")}</div></article>'
    return shell(lang, 'lecture', '音楽と医学' if lang == 'ja' else 'Music & Medicine', body)


def redirect(target):
    """Old bookmarked routes remain usable even with JavaScript disabled."""
    escaped = escape(target, quote=True)
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Tomohide R. Sato</title><meta http-equiv="refresh" content="0;url={escaped}"><link rel="canonical" href="{ORIGIN}{escaped}"></head><body><p><a href="{escaped}">Continue to Tomohide R. Sato’s website</a></p><script>window.location.replace({json.dumps(target)});</script></body></html>\n'''


def write(path, text):
    destination = ROOT / path
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(text)


def main():
    for lang in ('en', 'ja'):
        for path, html in [(home_path(lang), home(lang)), (cv_path(lang), cv(lang)), (lecture_path(lang), lecture(lang))]:
            write(path.strip('/') + '/index.html' if path != '/' else 'index.html', html)
    aliases = {'index/index.html': '/', 'research/index.html': '/#research', 'publications/index.html': '/#publications', 'contacts/index.html': '/#contact', 'Piano/index.html': '/#piano', 'profile/index.html': '/cv/', 'en/index.html': '/', 'ja/index.html': '/japanese/'}
    for path, target in aliases.items():
        write(path, redirect(target))
    print('Generated 6 bilingual pages and 8 legacy route redirects.')


if __name__ == '__main__':
    main()
