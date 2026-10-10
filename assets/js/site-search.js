document.addEventListener("DOMContentLoaded", async () => {
  const searchModal = document.getElementById("site-search-modal");
  const searchButton = document.getElementById("site-search-open");
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

    // no match in the body (or no query yet): show the start of the page
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
    searchModal.placeholder = "Search this site…";
    searchModal.hideBreadcrumbs = true;
    searchButton.disabled = false;
    searchButton.addEventListener("click", () => searchModal.open());

    const response = await fetch(searchButton.dataset.index);
    if (!response.ok) throw new Error(`Search index request failed: ${response.status}`);
    const documents = await response.json();

    const documentsByUrl = new Map(documents.map((document) => [document.url, document]));
    let actions = documents.map((document) => ({
      id: document.url,
      title: document.title,
      icon: makeSnippet(document, ""),
      keywords: document.content,
      section: "Pages",
      handler: () => {
        window.location.href = document.url;
      },
    }));
    searchModal.addEventListener("change", (event) => {
      const query = event.detail.search.trim();
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
