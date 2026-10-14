#!/usr/bin/env python3
import re, os, subprocess, sys
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


def tabularx_to_list(s):
    """Two-column tabularx (left & right) -> itemize list of 'left --- right'."""
    while (start := s.find(r"\begin{tabularx}")) != -1:
        _, j = read_group(s, start + len(r"\begin{tabularx}"))   # width
        _, j = read_group(s, j)                                   # column spec
        end = s.index(r"\end{tabularx}", j)
        items = []
        for row in re.split(r"\\\\", s[j:end]):
            row = row.strip()
            if not row:
                continue
            cells = [c.strip() for c in re.split(r"(?<!\\)&", row)]
            if len(cells) == 1 and items:        # wrapped continuation line
                items[-1][0] += " " + cells[0]
            else:
                items.append(cells)
        body = "\n".join(r"\item " + " --- ".join(c) for c in items)
        s = s[:start] + "\\begin{itemize}\n" + body + "\n\\end{itemize}" + s[end + len(r"\end{tabularx}"):]
    return s


def preprocess(tex):
    # Keep only the body; the preamble's layout code is irrelevant to Markdown
    body = tex.split(r"\begin{document}", 1)[1].split(r"\end{document}", 1)[0]
    body = re.sub(r"(?<!\\)%.*", "", body)                       # comments

    # Pull the name out of the centered header so it can become the H1
    start = body.index(r"\begin{center}")
    idx = body.index(r"\textbf", start)
    name_tex, j = read_group(body, idx + len(r"\textbf"))
    name = re.sub(r"\\[A-Za-z]+\s*", "", name_tex).strip()
    body = body[:idx] + re.sub(r"^\s*\\\\", "", body[j:])
    body = re.sub(r"\\(begin|end)\{center\}", "", body)
    body = re.sub(r"\s*\\:\\big\|\\:\s*", " · ", body)            # contact-line separators

    # Layout-only commands
    body = dash_lines_to_list(body)                               # must run before \hspace is stripped
    body = re.sub(r"\\[hv]space\*?\{[^}]*\}", "", body)
    body = re.sub(r"\s*\\hfill\s*", " --- ", body)
    body = re.sub(r"\\(begin|end)\{small\}", "", body)
    body = re.sub(r"\\(small|footnotesize|large|LARGE|scshape|justifying)(?![A-Za-z])\s*", "", body)
    body = tabularx_to_list(body)

    # Publications: enumerate with custom [YYYY-MM] labels
    body = re.sub(r"\\begin\{enumerate\}(\[[^\]]*\])?", r"\\begin{itemize}", body)
    body = body.replace(r"\end{enumerate}", r"\end{itemize}")
    body = re.sub(r"\\item\[\{\[([^\]]*)\]\}\]", r"\\item \\textbf{\1} ---", body)

    # The template's own macros
    body = expand(body, "cvheadingstart", 0, lambda: "")
    body = expand(body, "cvheadingend", 0, lambda: "")
    body = expand(body, "cvitemstart", 0, lambda: "\\begin{itemize}")
    body = expand(body, "cvitemend", 0, lambda: "\\end{itemize}")
    body = expand(body, "cvheading", 4,
                  lambda org, place, role, date:
                  f"\n\\subsection{{{org} --- {place}}}\n\\textbf{{{role}}} --- {date}\n\n")
    body = expand(body, "cvitem", 1, lambda text: f"\\item {text}\n")
    return name, body

def append_to_page():
    if not os.path.exists("cv/output.md"):
        print("Error: Failed to convert cv.tex to output.md")
        sys.exit(1)

    cv_page = "_pages/cv.md"
    cv_output = "cv/output.md"
    keep_lines = []

    with open(cv_page, "r") as file:
        cv_page_lines = file.readlines()

    with open(cv_output, "r") as file:
        cv_output_lines = file.readlines()
    
    in_cv = False
    for line in cv_page_lines:
        if line.strip() == "<!-- Begin CV -->":
            keep_lines.append(line)
            in_cv = True
            for cv_line in cv_output_lines:
                keep_lines.append(cv_line)
        if line.strip() == "<!-- End CV -->":
            in_cv = False
        if not in_cv:
            keep_lines.append(line)



    with open(cv_page, "w") as file:
        file.writelines(keep_lines)


    os.remove("cv/output.md")


def main():
    src = Path("cv/cv.tex")
    dst = Path("cv/output.md")
    name, body = preprocess(src.read_text(encoding="utf-8"))
    latex = "\\documentclass{article}\n\\begin{document}\n" + body + "\n\\end{document}\n"
    md = subprocess.run(
        ["pandoc", "-f", "latex", "-t", "gfm", "--wrap=none", "--shift-heading-level-by=1"],
        input=latex, capture_output=True, encoding="utf-8", check=True,
    ).stdout
    md = re.sub(r"\n{3,}", "\n\n", md)
    dst.write_text(f"# {name}\n\n{md}", encoding="utf-8")

    append_to_page()


if __name__ == "__main__":
    main()