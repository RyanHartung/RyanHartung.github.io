import { highlightSearchTerm } from "./highlight-search-term.js";

document.addEventListener("DOMContentLoaded", function () {
  const input = document.getElementById("bibsearch");
  const CARD = ".pub-list .pub-card";

  const filterItems = (rawTerm) => {
    const searchTerm = rawTerm.trim().toLowerCase();
    const cards = document.querySelectorAll(CARD);

    // reset
    document
      .querySelectorAll(".pub-list .unloaded")
      .forEach((el) => el.classList.remove("unloaded"));

    // highlight matches where the browser supports it
    if (CSS.highlights) {
      highlightSearchTerm({ search: searchTerm, selector: CARD });
    }

    if (!searchTerm) return;

    // hide non-matching cards
    cards.forEach((card) => {
      if (!card.textContent.toLowerCase().includes(searchTerm)) {
        card.classList.add("unloaded");
      }
    });

    // hide category headers with no visible cards left
    document.querySelectorAll(".pub-category-header").forEach((header) => {
      let el = header.nextElementSibling;
      let hasVisible = false;
      while (el && !el.classList.contains("pub-category-header")) {
        if (el.classList.contains("pub-card") && !el.classList.contains("unloaded")) {
          hasVisible = true;
          break;
        }
        el = el.nextElementSibling;
      }
      if (!hasVisible) header.classList.add("unloaded");
    });
  };

  // debounce: wait 200 ms after the last keystroke
  let timeoutId;
  input.addEventListener("input", function () {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => filterItems(this.value), 200);
  });

  // support links like /publications/#keyword
  const updateFromHash = () => {
    const hashValue = decodeURIComponent(window.location.hash.substring(1));
    input.value = hashValue;
    filterItems(hashValue);
  };
  window.addEventListener("hashchange", updateFromHash);
  updateFromHash();
});