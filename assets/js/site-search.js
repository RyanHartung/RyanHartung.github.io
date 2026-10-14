import { highlightSearchTerm } from "./highlight-search-term.js";

document.addEventListener("DOMContentLoaded", async () => {
  const searchModal = document.getElementById("site-search-modal");
  const searchButton = document.getElementById("site-search-open");
  const searchableContent = "#main .page__content, #main .archive, #main .page__title";

  const injectHighlightStyles = () => {
    if (document.getElementById("site-search-highlight-styles")) return;
    const style = document.createElement("style");
    style.id = "site-search-highlight-styles";
    style.textContent = `
      mark.site-search-highlight {
        background: #ffe066;
        color: #1a1a1a;
        padding: 0.08em 0.25em;
        margin: 0 -0.05em;
        border-radius: 0.3em;
        box-shadow: 0 0 0 2px rgba(255, 196, 0, 0.45), 0 2px 8px rgba(0, 0, 0, 0.18);
        -webkit-box-decoration-break: clone;
        box-decoration-break: clone;
        transition: background-color 0.6s ease, box-shadow 0.6s ease, color 0.6s ease;
        animation: site-search-pop 0.6s ease-out both;
      }

      mark.site-search-highlight.is-current {
        background: #ffd43b;
        box-shadow: 0 0 0 3px rgba(255, 170, 0, 0.7), 0 4px 14px rgba(0, 0, 0, 0.25);
        animation: site-search-pop 0.6s ease-out both, site-search-pulse 1.2s ease-in-out 0.6s 3;
      }

      [data-theme="dark"] mark.site-search-highlight {
        background: #f5c542;
        color: #111;
        box-shadow: 0 0 0 2px rgba(245, 197, 66, 0.5), 0 2px 10px rgba(0, 0, 0, 0.5);
      }

      mark.site-search-highlight.is-fading {
        background: transparent;
        color: inherit;
        box-shadow: none;
        animation: none;
      }

      @keyframes site-search-pop {
        0%   { box-shadow: 0 0 0 0 rgba(255, 196, 0, 0.9); }
        50%  { box-shadow: 0 0 0 8px rgba(255, 196, 0, 0.25), 0 4px 14px rgba(0, 0, 0, 0.2); }
        100% { box-shadow: 0 0 0 2px rgba(255, 196, 0, 0.45), 0 2px 8px rgba(0, 0, 0, 0.18); }
      }

      @keyframes site-search-pulse {
        0%, 100% { box-shadow: 0 0 0 3px rgba(255, 170, 0, 0.7), 0 4px 14px rgba(0, 0, 0, 0.25); }
        50%      { box-shadow: 0 0 0 9px rgba(255, 170, 0, 0.2), 0 4px 14px rgba(0, 0, 0, 0.25); }
      }

      @media (prefers-reduced-motion: reduce) {
        mark.site-search-highlight,
        mark.site-search-highlight.is-current {
          animation: none;
          transition: none;
        }
      }
    `;
    document.head.append(style);
  };

  const applyIncomingSearch = () => {
    const search = new URLSearchParams(window.location.search).get("search")?.trim();
    if (!search) return;

    const normalizedSearch = search.toLocaleLowerCase();
    const elements = document.querySelectorAll(searchableContent);
    const matchingNodes = new Set();

    elements.forEach((element) => {
      const walker = document.createTreeWalker(element, NodeFilter.SHOW_TEXT);
      let node;
      while ((node = walker.nextNode())) {
        if (node.textContent?.toLocaleLowerCase().includes(normalizedSearch)) {
          matchingNodes.add(node);
        }
      }
    });

    if (!matchingNodes.size) return;
    injectHighlightStyles();

    const marks = [];
    matchingNodes.forEach((node) => {
      const lowerText = (node.textContent || "").toLocaleLowerCase();
      const starts = [];
      let offset = 0;
      let index;
      while ((index = lowerText.indexOf(normalizedSearch, offset)) >= 0) {
        starts.push(index);
        offset = index + normalizedSearch.length;
      }

      // Wrap from the end so earlier offsets stay valid
      const nodeMarks = [];
      starts.reverse().forEach((start) => {
        const range = new Range();
        range.setStart(node, start);
        range.setEnd(node, start + normalizedSearch.length);
        const mark = document.createElement("mark");
        mark.className = "site-search-highlight";
        range.surroundContents(mark);
        nodeMarks.unshift(mark);
      });
      marks.push(...nodeMarks);
    });

    const firstMark = marks[0];
    firstMark?.classList.add("is-current");
    firstMark?.scrollIntoView({ behavior: "smooth", block: "center" });

    window.setTimeout(() => {
      marks.forEach((mark) => mark.classList.add("is-fading"));

      // Unwrap once the fade transition has finished
      window.setTimeout(() => {
        marks.forEach((mark) => {
          const parent = mark.parentNode;
          if (!parent) return;
          mark.replaceWith(...mark.childNodes);
          parent.normalize();
        });
      }, 700);
    }, 5000);
  };
  applyIncomingSearch();
  if (!searchModal || !searchButton) return;

  const markSearchUnavailable = () => {
    searchButton.disabled = true;
    searchButton.textContent = "Search unavailable";
  };

  const escapeHtml = (text) =>
    text.replace(/[&<>"']/g, (character) => ({
      "&": "&amp;",
      "<": "&lt;",
      ">": "&gt;",
      '"': "&quot;",
      "'": "&#39;",
    })[character]);

  const snippetStyles = `<style>
  div.ninja-action {
    flex-wrap: wrap;
    row-gap: 0.2em;
    padding: 0.7em 1em;
  }

  div.ninja-title {
    order: 1;
    flex: 1 1 100%;
    margin-right: 0;
    font-size: 0.9em;
    font-weight: 600;
  }

  .ninja-icon.site-search-snippet {
    order: 2;
    flex: 0 0 100%;
    display: -webkit-box;
    -webkit-box-orient: vertical;
    -webkit-line-clamp: 2;
    max-width: none;
    max-height: none;
    margin: 0;
    overflow: hidden;
    color: var(--ninja-secondary-text-color);
    font-size: 0.78em;
    font-weight: 400;
    line-height: 1.45;
    white-space: normal;
  }

  .site-search-snippet mark {
    padding: 0 0.15em;
    border-radius: 3px;
    background: color-mix(in srgb, var(--ninja-accent-color) 30%, transparent);
    color: inherit;
    font-weight: 600;
  }
</style>`;

  const makeSnippet = (doc, query) => {
    const source = doc.content || "";
    if (!source) return snippetStyles;

    const wrap = (html) =>
      `${snippetStyles}<span class="ninja-icon site-search-snippet" aria-hidden="true">${html}</span>`;

    const index = query
      ? source.toLocaleLowerCase().indexOf(query.toLocaleLowerCase())
      : -1;

    /* no match in the body (or no query yet): show the start of the page */
    if (index < 0) {
      return wrap(escapeHtml(source.slice(0, 180)) + (source.length > 180 ? "…" : ""));
    }

    const start = Math.max(0, index - 60);
    const end = Math.min(source.length, index + query.length + 140);
    const matchEnd = index + query.length;

    return wrap(
      (start > 0 ? "…" : "") +
      escapeHtml(source.slice(start, index)) +
      `<mark>${escapeHtml(source.slice(index, matchEnd))}</mark>` +
      escapeHtml(source.slice(matchEnd, end)) +
      (end < source.length ? "…" : "")
    );
  };

  const applyTheme = () => {
    searchModal.classList.toggle("dark", document.documentElement.dataset.theme === "dark");
  };
  applyTheme();
  new MutationObserver(applyTheme).observe(document.documentElement, {
    attributes: true,
    attributeFilter: ["data-theme"],
  });

  try {
    await import("https://unpkg.com/ninja-keys@1.2.2?module");
    await customElements.whenDefined("ninja-keys");
    searchModal.openHotkey = "/";
    searchModal._unregisterInternalHotkeys?.();
    searchModal._registerInternalHotkeys?.();
    searchModal.placeholder = "Search this site…";
    searchModal.hideBreadcrumbs = true;
    searchButton.disabled = false;
    searchButton.addEventListener("click", () => searchModal.open());

    const response = await fetch(searchButton.dataset.index);
    if (!response.ok) throw new Error(`Search index request failed: ${response.status}`);
    const documents = await response.json();

    const documentsByUrl = new Map(documents.map((document) => [document.url, document]));
    let searchTerm = "";
    let actions = documents.map((document) => ({
      id: document.url,
      title: document.title,
      icon: makeSnippet(document, ""),
      keywords: document.content,
      section: "Pages",
      handler: () => {
        const target = new URL(document.url, window.location.href);
        if (searchTerm) target.searchParams.set("search", searchTerm);
        window.location.href = target.href;
      },
    }));
    searchModal.addEventListener("change", (event) => {
      const query = event.detail.search.trim();
      searchTerm = query;
      actions = actions.map((action) => {
        const document = documentsByUrl.get(action.id);
        return {
          ...action,
          icon: document ? makeSnippet(document, query) : undefined,
        };
      });
      searchModal.data = actions;
    });
    searchModal.data = actions;
  } catch (error) {
    console.error("Site search failed to load:", error);
    if (customElements.get("ninja-keys")) {
      searchModal.data = [{
        id: "search-unavailable",
        title: "Search is temporarily unavailable. Please try again later.",
        section: "Search",
      }];
    } else {
      markSearchUnavailable();
    }
  }
});
