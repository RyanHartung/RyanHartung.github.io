---
layout: archive
title: "Background"
permalink: /background/
author_profile: true
redirect_from:
  - /cv
  - /resume
---

{% include base_path %}

<style>
  /* ---------- Theme tokens (tweak these to match your site) ---------- */
  .bg-docs {
    --doc-accent: #3a7ca5;
    --doc-accent-soft: rgba(58, 124, 165, 0.12);
    --doc-border: rgba(128, 128, 128, 0.22);
    --doc-surface: rgba(128, 128, 128, 0.04);
    --doc-muted: rgba(128, 128, 128, 0.95);
    --doc-radius: 12px;
    --doc-shadow: 0 1px 2px rgba(0, 0, 0, 0.05), 0 4px 14px rgba(0, 0, 0, 0.06);
    --doc-shadow-hover: 0 2px 4px rgba(0, 0, 0, 0.06), 0 10px 28px rgba(0, 0, 0, 0.1);
  }

  /* ---------- Cards ---------- */
  .doc-card {
    position: relative;
    margin-bottom: 2em;
    padding: 1.6em 1.75em 1.4em;
    border: 1px solid var(--doc-border);
    border-radius: var(--doc-radius);
    background: var(--doc-surface);
    box-shadow: var(--doc-shadow);
    overflow: hidden;
    scroll-margin-top: 5em; /* keeps anchors clear of the sticky masthead */
    transition: transform 0.25s ease, box-shadow 0.25s ease, border-color 0.25s ease;
  }
  .doc-card::before {
    content: "";
    position: absolute;
    inset: 0 0 auto 0;
    height: 4px;
    background: linear-gradient(90deg, var(--doc-accent), rgba(58, 124, 165, 0.35));
  }
  .doc-card:hover {
    transform: translateY(-2px);
    box-shadow: var(--doc-shadow-hover);
    border-color: rgba(58, 124, 165, 0.35);
  }

  .doc-header {
    display: flex;
    align-items: center;
    gap: 0.9em;
    margin-bottom: 0.6em;
  }
  .doc-icon {
    flex: 0 0 auto;
    display: grid;
    place-items: center;
    width: 2.6em;
    height: 2.6em;
    border-radius: 10px;
    background: var(--doc-accent-soft);
    color: var(--doc-accent);
  }
  .doc-icon svg { width: 1.3em; height: 1.3em; }

  .doc-card h2 {
    margin: 0;
    padding: 0;
    border-bottom: none; /* overrides the theme's h2 underline */
    font-size: 1.35em;
    line-height: 1.25;
  }

  .doc-blurb {
    margin: 0 0 1.1em;
    font-size: 0.95em;
    line-height: 1.6;
    color: inherit;
    opacity: 0.85;
  }

  /* ---------- Buttons ---------- */
  .doc-controls {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5em;
    margin-bottom: 1em;
  }
  .doc-controls .btn {
    display: inline-flex;
    align-items: center;
    gap: 0.4em;
    margin: 0;
    border-radius: 8px;
    transition: transform 0.15s ease, background 0.2s, color 0.2s;
  }
  .doc-controls .btn:hover { transform: translateY(-1px); }
  .doc-controls .btn svg { width: 1em; height: 1em; }

  /* ---------- Download chips ---------- */
  .doc-downloads {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 0.45em;
    margin: 0;
    padding-top: 0.9em;
    border-top: 1px dashed var(--doc-border);
    font-size: 0.8em;
  }
  .doc-downloads-label {
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: var(--doc-muted);
    margin-right: 0.3em;
  }
  .doc-downloads a {
    display: inline-flex;
    align-items: center;
    gap: 0.35em;
    padding: 0.25em 0.75em;
    border: 1px solid var(--doc-border);
    border-radius: 999px;
    text-decoration: none;
    color: inherit;
    transition: border-color 0.2s, background 0.2s, color 0.2s;
  }
  .doc-downloads a::before {
    content: "↓";
    font-weight: 700;
    color: var(--doc-accent);
    transition: color 0.2s;
  }
  .doc-downloads a:hover,
  .doc-downloads a:focus-visible {
    border-color: var(--doc-accent);
    background: var(--doc-accent);
    color: #fff;
  }
  .doc-downloads a:hover::before,
  .doc-downloads a:focus-visible::before { color: #fff; }

  /* ---------- PDF panel ---------- */
  .doc-panel { margin-top: 1.25em; }
  .doc-panel[hidden] { display: none !important; }
  .doc-panel:not([hidden]) { animation: doc-reveal 0.3s ease; }

  @keyframes doc-reveal {
    from { opacity: 0; transform: translateY(-6px); }
    to   { opacity: 1; transform: translateY(0); }
  }

  .doc-pdf-frame {
    display: block;
    width: 100%;
    height: 85vh;
    min-height: 600px;
    border: 1px solid var(--doc-border);
    border-radius: 10px;
    background: rgba(128, 128, 128, 0.08);
    box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.06);
  }

  .doc-pdf-fallback {
    margin: 0.6em 0 0;
    font-size: 0.8em;
    color: var(--doc-muted);
    text-align: right;
  }

  /* ---------- Responsive & accessibility ---------- */
  @media (max-width: 600px) {
    .doc-card { padding: 1.3em 1.1em 1.1em; }
    .doc-controls .btn { flex: 1 1 100%; justify-content: center; }
    .doc-pdf-frame { height: 70vh; min-height: 400px; }
  }

  @media (prefers-reduced-motion: reduce) {
    .doc-card,
    .doc-controls .btn,
    .doc-panel:not([hidden]) { transition: none; animation: none; }
    .doc-card:hover,
    .doc-controls .btn:hover { transform: none; }
  }
</style>

<div class="bg-docs">

  {% for doc in site.data.background_docs %}
  {% capture path %}{{ base_path }}/assets/{{ doc.id }}/{{ doc.id }}{% endcapture %}
  <section class="doc-card" id="{{ doc.id }}">
    <div class="doc-header">
      <span class="doc-icon" aria-hidden="true">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
             stroke-linecap="round" stroke-linejoin="round">
          <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
          <polyline points="14 2 14 8 20 8"/>
          <line x1="8" y1="13" x2="16" y2="13"/>
          <line x1="8" y1="17" x2="13" y2="17"/>
        </svg>
      </span>
      <h2>{{ doc.title }}</h2>
    </div>

    <p class="doc-blurb">{{ doc.blurb }}</p>

    <div class="doc-controls">
      <button type="button" class="btn btn--inverse"
              data-pdf-target="{{ doc.id }}-pdf"
              aria-expanded="false" aria-controls="{{ doc.id }}-pdf">View PDF</button>
      <a class="btn btn--inverse" href="{{ path }}.pdf" target="_blank" rel="noopener">Open PDF in New Tab</a>
      <a class="btn btn--inverse" href="{{ base_path }}/background/{{ doc.id }}"
         data-pagination-title="{{ doc.title | escape }}">View Text Version</a>
    </div>

    <p class="doc-downloads">
      <span class="doc-downloads-label">Download</span>
      <a href="{{ path }}.pdf" download>PDF</a>
      <a href="{{ path }}.docx" download>Microsoft Word</a>
      <a href="{{ path }}.odt" download>OpenDocument</a>
      <a href="{{ path }}.md" download>Markdown</a>
    </p>

    <div id="{{ doc.id }}-pdf" class="doc-panel" hidden>
      <iframe class="doc-pdf-frame" title="Ryan Hartung {{ doc.title | escape }} (PDF)"
              data-src="{{ path }}.pdf#view=FitH"></iframe>
      <p class="doc-pdf-fallback">
        PDF not showing up? <a href="{{ path }}.pdf" target="_blank" rel="noopener">Open it directly</a>.
      </p>
    </div>
  </section>
  {% endfor %}

</div>

<script>
  (() => {
    const buttons = document.querySelectorAll("[data-pdf-target]");
    const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

    const show = (targetId) => {
      buttons.forEach((button) => {
        const panel = document.getElementById(button.dataset.pdfTarget);
        if (!panel) return;
        const isOpen = button.dataset.pdfTarget === targetId;

        panel.hidden = !isOpen;
        button.setAttribute("aria-expanded", String(isOpen));
        button.textContent = isOpen ? "Hide PDF" : "View PDF";
        button.classList.toggle("btn--primary", isOpen);
        button.classList.toggle("btn--inverse", !isOpen);

        /* Only load each PDF the first time it's opened */
        const frame = panel.querySelector("iframe[data-src]");
        if (isOpen && frame && !frame.getAttribute("src")) {
          frame.src = frame.dataset.src;
        }

        /* Bring the opened card into view */
        if (isOpen) {
          button.closest(".doc-card").scrollIntoView({
            behavior: reduceMotion ? "auto" : "smooth",
            block: "start"
          });
        }
      });
    };

    buttons.forEach((button) => {
      button.addEventListener("click", () => {
        const alreadyOpen = button.getAttribute("aria-expanded") === "true";
        show(alreadyOpen ? null : button.dataset.pdfTarget);
      });
    });
  })();
</script>