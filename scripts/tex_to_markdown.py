#!/usr/bin/env python3
import argparse, re, os, subprocess, sys
from pathlib import Path

def read_group(s, i):
    """Skip whitespace from s[i], read one {...} group. Return (inner text, index after it)."""
    while s[i].isspace():
        i += 1
    if s[i] != "{":
        raise ValueError(f"expected '{{' at position {i}: {s[i:i+40]!r}")
    depth, j = 0, i
    while j < len(s):
        c = s[j]
        if c == "\\":
            j += 2
            continue
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return s[i + 1 : j], j + 1
        j += 1
    raise ValueError("unbalanced braces")


def expand(s, name, nargs, render):
    """Replace every \\name{arg1}...{argN} with render(arg1, ..., argN), handling nested braces."""
    pat = re.compile(r"\\" + name + r"(?![A-Za-z])")   # so \cvitem doesn't match \cvitemstart
    out, pos = [], 0
    while m := pat.search(s, pos):
        out.append(s[pos : m.start()])
        args, j = [], m.end()
        for _ in range(nargs):
            arg, j = read_group(s, j)
            args.append(arg)
        out.append(render(*args))
        pos = j
    out.append(s[pos:])
    return "".join(out)


def dash_lines_to_list(s):
    r"""Manual bullets like '\hspace*{2em} - Grading' -> a real itemize list."""
    block = re.compile(r"(?:[ \t]*\\hspace\*?\{[^}]*\}\s*-\s*[^\n]+\n\s*)+")

    def repl(m):
        items = re.findall(r"\\hspace\*?\{[^}]*\}\s*-\s*([^\n]+)", m.group(0))
        return "\\begin{itemize}\n" + "\n".join(r"\item " + i.strip() for i in items) + "\n\\end{itemize}\n"

    return block.sub(repl, s)


def read_optional(s, i):
    """Skip an optional [...] argument starting at s[i], if there is one."""
    k = i
    while k < len(s) and s[k].isspace():
        k += 1
    if k < len(s) and s[k] == "[":
        return s.index("]", k) + 1
    return i


def split_table(body):
    r"""Split table body into rows (on \\) and cells (on &), ignoring anything inside braces."""
    rows, cells, buf, depth, i = [], [], [], 0, 0
    while i < len(body):
        c = body[i]
        if c == "\\":
            if depth == 0 and body.startswith("\\\\", i):     # row break
                cells.append("".join(buf))
                rows.append(cells)
                cells, buf = [], []
            else:                                               # \&, \{, \textbf, ...
                buf.append(body[i : i + 2])
            i += 2
            continue
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
        elif c == "&" and depth == 0:                           # cell break
            cells.append("".join(buf))
            buf = []
            i += 1
            continue
        buf.append(c)
        i += 1
    cells.append("".join(buf))
    rows.append(cells)
    return rows


def tables_to_paragraphs(s):
    """Layout-only tables (tabular, tabular*, tabularx) -> one paragraph per row: 'left --- right'."""
    TABLE_ENV = re.compile(r"\\begin\{(tabularx|tabular\*?)\}")
    while m := TABLE_ENV.search(s):
        env, j = m.group(1), m.end()
        if env != "tabular":
            _, j = read_group(s, j)          # width
        j = read_optional(s, j)              # [t]
        _, j = read_group(s, j)              # column spec
        end_tag = "\\end{" + env + "}"
        end = s.index(end_tag, j)

        rows = []
        for cells in split_table(s[j:end]):
            cells = [expand(c, "multicolumn", 3, lambda n, spec, content: content).strip()
                     for c in cells]
            cells = [c for c in cells if c]
            if cells:
                rows.append(" --- ".join(cells))

        s = s[: m.start()] + "\n\n" + "\n\n".join(rows) + "\n\n" + s[end + len(end_tag):]
    return s


def simple_math_to_unicode(s):
    """Replace short math spans like $\\times$ or $\\sim$ with Unicode; leave real math alone."""
    MATH_SYMBOLS = {
        r"\times": "×",
        r"\sim": "\uE000",
        r"\approx": "≈",
        r"\leq": "≤",
        r"\geq": "≥",
        r"\pm": "±",
        r"\cdot": "·",
        r"\rightarrow": "→",
        r"\to": "→",
    }
    def repl(m):
        out = m.group(1)
        for cmd in sorted(MATH_SYMBOLS, key=len, reverse=True):
            out = re.sub(re.escape(cmd) + r"(?![A-Za-z])", MATH_SYMBOLS[cmd], out)
        out = out.replace("{", "").replace("}", "").strip()
        return m.group(0) if "\\" in out else out
    return re.sub(r"(?<!\\)\$([^$]+?)(?<!\\)\$", repl, s)


def preprocess(tex):
    # Keep only the body; the preamble's layout code is irrelevant to Markdown
    body = tex.split(r"\begin{document}", 1)[1].split(r"\end{document}", 1)[0]
    body = re.sub(r"(?<!\\)%.*", "", body) # comments

    # Pull the name out of the centered header so it can become the H1
    start = body.index(r"\begin{center}")
    idx = body.index(r"\textbf", start)
    name_tex, j = read_group(body, idx + len(r"\textbf"))
    name = re.sub(r"\\[A-Za-z]+\s*", "", name_tex).strip()
    body = body[:idx] + re.sub(r"^\s*\\\\", "", body[j:])
    body = re.sub(r"\\(begin|end)\{center\}", "", body)
    body = re.sub(r"\s*\\:\\big\|\\:\s*", " · ", body)

    # Math symbols
    body = simple_math_to_unicode(body)

    # Layout-only commands
    body = dash_lines_to_list(body)
    body = re.sub(r"\\[hv]space\*?\{[^}]*\}", "", body)
    body = re.sub(r"\s*\\hfill\s*", " --- ", body)
    body = re.sub(r"\\(begin|end)\{small\}", "", body)
    body = re.sub(r"\\(small|footnotesize|large|LARGE|scshape|justifying)(?![A-Za-z])\s*", "", body)
    body = tables_to_paragraphs(body)
    body = re.sub(r"\\begin\{itemize\}\[[^\]]*\]", r"\\begin{itemize}", body)   # drop enumitem options
    body = re.sub(r"\\item\[(?:--|-|\\textbullet)\]", r"\\item", body)

    # Publications: enumerate with custom [YYYY-MM] labels
    body = re.sub(r"\\begin\{enumerate\}(\[[^\]]*\])?", r"\\begin{itemize}", body)
    body = body.replace(r"\end{enumerate}", r"\end{itemize}")
    body = re.sub(r"\\item\[\{\[([^\]]*)\]\}\]", r"\\item \\textbf{\1} ---", body)

    # The template's own macros
    body = expand(body, "docSubHeadingListStart", 0, lambda: "")
    body = expand(body, "docSubHeadingListEnd", 0, lambda: "")
    body = expand(body, "docItemListStart", 0, lambda: "\\begin{itemize}")
    body = expand(body, "docItemListEnd", 0, lambda: "\\end{itemize}")
    body = expand(body, "docSubheading", 4,
                  lambda org, place, role, date:
                  f"\n\\subsection{{{org} --- {place}}}\n\\textbf{{{role}}} --- {date}\n\n")
    body = expand(body, "docItem", 1, lambda text: f"\\item {text}\n")
    return name, body


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--input", nargs="?", help="LaTeX source")
    ap.add_argument("-o", "--output", help="output .md")
    args = ap.parse_args()

    src = Path(args.input)
    dst = Path(args.output)
    name, body = preprocess(src.read_text(encoding="utf-8"))
    latex = "\\documentclass{article}\n\\begin{document}\n" + body + "\n\\end{document}\n"
    md = subprocess.run(
        ["pandoc", "-f", "latex", "-t", "gfm", "--wrap=none", "--shift-heading-level-by=1"],
        input=latex, capture_output=True, encoding="utf-8", check=True,
    ).stdout
    md = re.sub(r"\n{3,}", "\n\n", md)
    md = md.replace("\uE000", "~")
    md = re.sub(r"\n{3,}", "\n\n", md)
    dst.write_text(f"# {name}\n\n{md}", encoding="utf-8")


if __name__ == "__main__":
    main()