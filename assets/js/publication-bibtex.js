const normalizeBibId = (bibID) => bibID.trim().toLowerCase();

const extractEntries = (bibtex) => {
  const entries = [];
  const entryStart = /@\s*[a-z]+\s*[{(]/gi;
  let match;

  while ((match = entryStart.exec(bibtex)) !== null) {
    const openingIndex = entryStart.lastIndex - 1;
    const opening = bibtex[openingIndex];
    const closing = opening === "{" ? "}" : ")";
    let depth = 1;
    let braceDepth = 0;
    let quoted = false;
    let escaped = false;
    let end = openingIndex + 1;

    for (; end < bibtex.length; end += 1) {
      const character = bibtex[end];
      if (escaped) {
        escaped = false;
        continue;
      }
      if (character === "\\") {
        escaped = true;
        continue;
      }
      if (character === '"' && braceDepth === 0) {
        quoted = !quoted;
        continue;
      }
      if (quoted) continue;
      if (character === "{") {
        braceDepth += 1;
      } else if (character === "}" && braceDepth > 0) {
        braceDepth -= 1;
      } else if (braceDepth === 0 && character === opening) {
        depth += 1;
      } else if (braceDepth === 0 && character === closing) {
        depth -= 1;
        if (depth === 0) break;
      }
    }

    if (depth !== 0) {
      throw new Error(`Unclosed BibTeX entry starting at character ${match.index}`);
    }

    entries.push(bibtex.slice(match.index, end + 1));
    entryStart.lastIndex = end + 1;
  }
  return entries;
};

const bibIdForEntry = (entry) =>
  entry.match(/^@\s*[a-z]+\s*[{(]\s*([^,\s]+)\s*,/i)?.[1] || null;

const bibtexPunctuation = "@!$&.\\:;<>?[]^`|~*/+-";
const isBibtexNameStart = (character) =>
  /[a-z_]/i.test(character) || bibtexPunctuation.includes(character);
const isBibtexNameCharacter = (character) =>
  /\w/.test(character) || bibtexPunctuation.includes(character);

const highlightBibtex = (code, source) => {
  const tokens = [];
  const states = ["root"];
  let index = 0;

  const addToken = (text, tokenClass = null) => {
    const lastToken = tokens[tokens.length - 1];
    if (lastToken && lastToken.tokenClass === tokenClass) {
      lastToken.text += text;
    } else {
      tokens.push({ text, tokenClass });
    }
  };

  const nameEnd = (start) => {
    let end = start + 1;
    while (end < source.length && isBibtexNameCharacter(source[end])) end += 1;
    return end;
  };

  while (index < source.length) {
    const state = states[states.length - 1];
    const character = source[index];
    const inString = state === "quoted_string" || state === "braced_string";

    if (!inString && /\s/.test(character)) {
      const start = index;
      while (index < source.length && /\s/.test(source[index])) index += 1;
      addToken(source.slice(start, index));
      continue;
    }

    if (state === "root") {
      if (character === "@" && index + 1 < source.length && isBibtexNameStart(source[index + 1])) {
        const end = nameEnd(index + 1);
        const entryType = source.slice(index + 1, end).toLowerCase();
        addToken(source.slice(index, end), entryType === "comment" ? "c" : "nc");
        index = end;
        if (entryType === "comment") continue;
        states.push("closing_brace");
        states.push(entryType === "preamble" ? "value" : entryType === "string" ? "field" : "command_body");
        states.push("opening_brace");
        continue;
      }

      let end = source.indexOf("\n", index);
      if (end === -1) end = source.length;
      if (end === index) end += 1;
      addToken(source.slice(index, end), "c");
      index = end;
      continue;
    }

    if (state === "opening_brace" || state === "closing_brace") {
      const expected = state === "opening_brace" ? "{(" : "})";
      if (expected.includes(character)) {
        addToken(character, "p");
        states.pop();
      } else {
        addToken(character, "err");
      }
      index += 1;
      continue;
    }

    if (state === "command_body") {
      if (character === "," || character === "}") {
        states.pop();
        continue;
      }
      let end = index + 1;
      while (end < source.length && !/[\s,}]/.test(source[end])) end += 1;
      addToken(source.slice(index, end), "nl");
      index = end;
      states.pop();
      states.push("fields");
      continue;
    }

    if (state === "fields") {
      if (character === ",") {
        addToken(character, "p");
        index += 1;
        states.push("field");
      } else {
        states.pop();
      }
      continue;
    }

    if (state === "field") {
      if (!isBibtexNameStart(character)) {
        states.pop();
        continue;
      }
      const end = nameEnd(index);
      addToken(source.slice(index, end), "na");
      index = end;
      states.push("value");
      states.push("equal_sign");
      continue;
    }

    if (state === "equal_sign") {
      if (character === "=") {
        addToken(character, "p");
        index += 1;
      }
      states.pop();
      continue;
    }

    if (state === "value") {
      if (isBibtexNameStart(character)) {
        const end = nameEnd(index);
        addToken(source.slice(index, end), "nv");
        index = end;
      } else if (character === '"' || character === "{") {
        addToken(character, "s");
        index += 1;
        states.push(character === '"' ? "quoted_string" : "braced_string");
      } else if (/\d/.test(character)) {
        let end = index + 1;
        while (end < source.length && /\d/.test(source[end])) end += 1;
        addToken(source.slice(index, end), "m");
        index = end;
      } else if (character === "#") {
        addToken(character, "p");
        index += 1;
      } else {
        states.pop();
      }
      continue;
    }

    if (inString) {
      if (character === "{") {
        addToken(character, "s");
        index += 1;
        states.push("braced_string");
      } else if (character === "}" && state === "braced_string") {
        addToken(character, "s");
        index += 1;
        states.pop();
      } else if (character === '"' && state === "quoted_string") {
        addToken(character, "s");
        index += 1;
        states.pop();
      } else {
        let end = index + 1;
        while (end < source.length && !/[{}"]/.test(source[end])) end += 1;
        addToken(source.slice(index, end), "s");
        index = end;
      }
    }
  }

  code.replaceChildren(
    ...tokens.map(({ text, tokenClass }) => {
      if (!tokenClass) return document.createTextNode(text);
      const token = document.createElement("span");
      token.className = tokenClass;
      token.textContent = text;
      return token;
    })
  );
};

document.addEventListener("DOMContentLoaded", async () => {
  const panels = [...document.querySelectorAll("[data-bibtex-id]")];
  if (!panels.length) return;

  try {
    const response = await fetch(panels[0].dataset.bibtexUrl);
    if (!response.ok) {
      throw new Error(`BibTeX file request failed: ${response.status}`);
    }

    const entriesByBibID = new Map(
      extractEntries(await response.text())
        .map((entry) => [bibIdForEntry(entry), entry])
        .filter(([bibID]) => bibID)
        .map(([bibID, entry]) => [normalizeBibId(bibID), entry])
    );

    panels.forEach((panel) => {
      const bibID = panel.dataset.bibtexId;
      const entry = entriesByBibID.get(normalizeBibId(bibID));
      if (!entry) {
        console.error(`No BibTeX entry found for ID ${bibID}`);
        panel.querySelector(".js-bibtex-copy").hidden = true;
        panel.insertAdjacentText("beforeend", `No BibTeX entry found for ID ${bibID}.`);
        return;
      }
      highlightBibtex(panel.querySelector("code"), entry);
    });
  } catch (error) {
    console.error("Failed to load publication BibTeX:", error);
    panels.forEach((panel) => {
      panel.querySelector(".js-bibtex-copy").hidden = true;
      panel.insertAdjacentText("beforeend", "BibTeX could not be loaded.");
    });
  }
});
