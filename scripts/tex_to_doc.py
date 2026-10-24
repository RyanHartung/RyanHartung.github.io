#!/usr/bin/env python3
"""Convert LaTeX cv/resume to .docx or .odt.

The Word file is built directly with python-docx so it keeps the same layout:
centered name and contact lines, ruled small-caps section headings, right-aligned
locations and dates, bullet lists, and clickable links. For .odt output the .docx
is converted with LibreOffice (or pandoc if LibreOffice isn't installed).
"""
import argparse, re, shutil, subprocess, sys, tempfile
from pathlib import Path

from docx import Document
from docx.enum.section import WD_ORIENT
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.opc.constants import RELATIONSHIP_TYPE
from docx.shared import Inches, Pt, RGBColor

COL = "\x01"          # column separator inside intermediate records
LINK_COLOR = RGBColor(0, 51, 128)   # matches \definecolor{linkblue}{RGB}{0, 51, 128}


# --------------------------------------------------------------------------- #
#  LaTeX helpers
# --------------------------------------------------------------------------- #
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


def read_optional(s, i):
    """If s[i:] (after whitespace) starts with [...], return (inner, end); else (None, i)."""
    k = i
    while k < len(s) and s[k].isspace():
        k += 1
    if k >= len(s) or s[k] != "[":
        return None, i
    depth, j = 0, k + 1
    while j < len(s):
        c = s[j]
        if c == "\\":
            j += 2
            continue
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
        elif c == "]" and depth == 0:
            return s[k + 1 : j], j + 1
        j += 1
    raise ValueError("unbalanced [ ]")


def expand(s, name, nargs, render):
    """Replace every \\name{arg1}...{argN} with render(arg1, ..., argN)."""
    pat = re.compile(r"\\" + name + r"(?![A-Za-z])")
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


def unwrap(s, name):
    r"""\name{X} -> X, but only where \name is followed by a brace group."""
    pat = re.compile(r"\\" + name + r"(?![A-Za-z])\s*(?=\{)")
    while m := pat.search(s):
        inner, j = read_group(s, m.end())
        s = s[: m.start()] + inner + s[j:]
    return s


def split_top(s, sep):
    """Split s on the regex sep, but only at brace depth 0."""
    parts, depth, last, i = [], 0, 0, 0
    rx = re.compile(sep)
    while i < len(s):
        c = s[i]
        if c == "\\" and not rx.match(s, i):
            i += 2
            continue
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
        elif depth == 0 and (m := rx.match(s, i)):
            parts.append(s[last:i])
            last = i = m.end()
            continue
        i += 1
    parts.append(s[last:])
    return parts


def oneline(s):
    return re.sub(r"\s+", " ", s).strip()


# --------------------------------------------------------------------------- #
#  Parse the document into records
# --------------------------------------------------------------------------- #
def tabulars_to_rows(s, env, tag):
    r"""\begin{tabular*}...\end{tabular*} (or tabularx) -> '@@<tag> left COL right' lines."""
    begin, end_tok = "\\begin{" + env + "}", "\\end{" + env + "}"
    while (start := s.find(begin)) != -1:
        _, j = read_group(s, start + len(begin))        # width
        _, j = read_optional(s, j)                      # [t]
        _, j = read_group(s, j)                         # column spec
        end = s.index(end_tok, j)
        out = []
        for row in split_top(s[j:end], r"\\\\"):
            cells = split_top(row, r"(?<!\\)&")
            if len(cells) >= 2:
                out.append(f"\n@@{tag} " + COL.join(oneline(c) for c in cells) + "\n")
            elif row.strip():
                out.append("\n" + row + "\n")            # e.g. a bullet list from \multicolumn
        s = s[:start] + "".join(out) + s[end + len(end_tok):]
    return s


def lists_to_records(s):
    """Innermost itemize/enumerate first -> @@BULLET / @@PUB / @@LINE records."""
    rx = re.compile(r"\\begin\{(itemize|enumerate)\}(?:\[[^\]]*\])?((?:(?!\\begin\{(?:itemize|enumerate)\}).)*?)\\end\{\1\}", re.S)
    while m := rx.search(s):
        body, out = m.group(2), []
        for piece in split_top(body, r"\\item(?![A-Za-z])")[1:]:
            label, j = read_optional(piece, 0)
            rest = piece[j:].strip()
            if rest.startswith("{") and label is None:   # \item{ line \\ line \\ }
                inner, _ = read_group(rest, 0)
                out += ["@@LINE " + oneline(l) for l in split_top(inner, r"\\\\") if l.strip()]
                continue
            text = oneline(rest)
            if not text:
                continue
            lab = (label or "").strip().strip("{}").strip()
            if re.fullmatch(r"\[.*\]", lab):              # \item[{[2026]}] -> publication
                out.append(f"@@PUB {lab}{COL}{text}")
            else:
                out.append(f"@@BULLET {text}")
        s = s[: m.start()] + "\n" + "\n".join(out) + "\n" + s[m.end():]
    return s


def parse(tex):
    body = tex.split(r"\begin{document}", 1)[1].split(r"\end{document}", 1)[0]
    body = re.sub(r"(?<!\\)%.*", "", body)

    # ---- header ------------------------------------------------------------
    start = body.index(r"\begin{center}")
    end = body.index(r"\end{center}", start)
    header = body[start + len(r"\begin{center}") : end]
    body = body[end + len(r"\end{center}"):]
    header = re.sub(r"\\[hv]space\*?\{[^}]*\}", "", header)
    lines = [l for l in split_top(header, r"\\\\") if l.strip()]
    name = oneline(lines[0])
    contact = [[oneline(x) for x in re.split(r"\\:\s*\\big\|\s*\\:|\\:\s*\$\|\$\s*\\:", l)]
               for l in lines[1:]]

    # ---- sections ----------------------------------------------------------
    sections = []
    for chunk in re.split(r"(?=\\section\*?\{)", body):
        if not chunk.strip().startswith("\\section"):
            continue
        title, j = read_group(chunk, chunk.index("{"))
        s = chunk[j:]
        s = expand(s, "docSubheading", 4,
                   lambda a, b, c, d: f"\n@@HEAD \\textbf{{{oneline(a)}}}{COL}{oneline(b)}\n"
                                      f"@@SUB \\textit{{{oneline(c)}}}{COL}\\textit{{{oneline(d)}}}\n")
        s = expand(s, "docItem", 1, lambda x: f"\\item {x}\n")
        s = expand(s, "docItemListStart", 0, lambda: "\\begin{itemize}")
        s = expand(s, "docItemListEnd", 0, lambda: "\\end{itemize}")
        s = expand(s, "docSubHeadingListStart", 0, lambda: "")
        s = expand(s, "docSubHeadingListEnd", 0, lambda: "")
        s = expand(s, "multicolumn", 3, lambda n, spec, x: "\n" + x + "\n")
        s = tabulars_to_rows(s, "tabularx", "WIDE")
        s = tabulars_to_rows(s, "tabular*", "ROW")
        s = re.sub(r"\\[hv]space\*?\{[^}]*\}", "", s)
        s = re.sub(r"\\(begin|end)\{small\}", "", s)
        s = unwrap(s, "small")
        s = lists_to_records(s)

        records = []
        for line in s.split("\n"):
            line = line.strip()
            if not line:
                continue
            if line.startswith("@@"):
                kind, _, payload = line[2:].partition(" ")
                records.append((kind, payload.split(COL)))
            else:
                leftover = re.sub(r"\\(small|footnotesize)(?![A-Za-z])", "", line).strip(" {}")
                if leftover:
                    print(f"warning: unparsed text in '{oneline(title)}': {leftover[:60]!r}", file=sys.stderr)
                    records.append(("PARA", [leftover]))
        sections.append((oneline(title), records))
    return name, contact, sections


# --------------------------------------------------------------------------- #
#  Inline LaTeX -> styled runs
# --------------------------------------------------------------------------- #
MATH = {r"\times": "×", r"\sim": "~", r"\approx": "≈", r"\pm": "±", r"\cdot": "·",
        r"\leq": "≤", r"\geq": "≥", r"\rightarrow": "→", r"\to": "→", "|": "|"}
SIMPLE = {"&": "&", "%": "%", "$": "$", "_": "_", "#": "#", "{": "{", "}": "}", " ": " ", ",": "\u2009"}
STYLE_CMDS = {"textbf": "bold", "textit": "italic", "emph": "italic", "textsl": "italic",
              "texttt": "mono", "textsc": "caps", "underline": "underline"}


def inline(s, style=None, out=None):
    """Return a list of (text, style dict) for a LaTeX fragment."""
    style = dict(style or {})
    out = [] if out is None else out
    i = 0

    def emit(t, st=style):
        if out and out[-1][1] == st:
            out[-1] = (out[-1][0] + t, st)
        else:
            out.append((t, dict(st)))

    while i < len(s):
        c = s[i]
        if c == "\\":
            m = re.match(r"\\([A-Za-z]+)\s*", s[i:])
            if not m:                                    # \& \% \\ etc.
                ch = s[i + 1] if i + 1 < len(s) else ""
                if ch in SIMPLE:
                    emit(SIMPLE[ch])
                i += 2
                continue
            cmd, i = m.group(1), i + m.end()
            if cmd in STYLE_CMDS:
                arg, i = read_group(s, i)
                inline(arg, {**style, STYLE_CMDS[cmd]: True}, out)
            elif cmd == "href":
                url, i = read_group(s, i)
                arg, i = read_group(s, i)
                inline(arg, {**style, "link": url}, out)
            elif cmd == "url":
                url, i = read_group(s, i)
                inline(url.replace("\\", ""), {**style, "link": url}, out)
            elif cmd in ("ldots", "dots"):
                emit("…")
            elif cmd == "LaTeX":
                emit("LaTeX")
            # anything else (\LARGE, \scshape, \small, ...) is layout only: drop it
        elif c == "$":
            j = s.index("$", i + 1)
            math = s[i + 1 : j]
            for k, v in MATH.items():
                math = math.replace(k, v)
            emit(re.sub(r"\\[A-Za-z]+|[{}^_]", "", math))
            i = j + 1
        elif c == "{":
            arg, i = read_group(s, i)
            inline(arg, style, out)
        elif c == "}":
            i += 1
        elif s.startswith("---", i):
            emit("—"); i += 3
        elif s.startswith("--", i):
            emit("–"); i += 2
        elif s.startswith("``", i):
            emit("“"); i += 2
        elif s.startswith("''", i):
            emit("”"); i += 2
        elif c == "`":
            emit("‘"); i += 1
        elif c == "'":
            emit("’"); i += 1
        elif c == "~":
            emit("\u00a0"); i += 1
        elif c.isspace():
            if not (out and out[-1][0].endswith(" ")):
                emit(" ")
            i += 1
        else:
            emit(c); i += 1
    return out


# --------------------------------------------------------------------------- #
#  docx building
# --------------------------------------------------------------------------- #
def add_hyperlink(paragraph, url, text, style, size):
    part = paragraph.part
    r_id = part.relate_to(url, RELATIONSHIP_TYPE.HYPERLINK, is_external=True)
    link = OxmlElement("w:hyperlink")
    link.set(qn("r:id"), r_id)
    run = paragraph.add_run(text)           # build a normal run, then move it inside the link
    format_run(run, style, size)
    run.font.color.rgb = LINK_COLOR
    link.append(run._r)
    paragraph._p.append(link)


def format_run(run, style, size):
    run.bold = style.get("bold") or None
    run.italic = style.get("italic") or None
    run.underline = style.get("underline") or None
    run.font.small_caps = style.get("caps") or None
    if style.get("mono"):
        run.font.name = "Consolas"
        run.font.size = Pt(size * 0.92)
    elif size:
        run.font.size = Pt(size)


def add_rich(paragraph, tex, size=None, base=None):
    runs = inline(tex, base)
    if runs:                                             # trim outer whitespace
        runs[0] = (runs[0][0].lstrip(), runs[0][1])
        runs[-1] = (runs[-1][0].rstrip(), runs[-1][1])
    for text, st in runs:
        if not text:
            continue
        if st.get("link"):
            add_hyperlink(paragraph, st["link"], text, st, size)
        else:
            format_run(paragraph.add_run(text), st, size)


def para(doc, space_before=0, space_after=0, left=0, first=0, align=None, keep=False):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.space_before, pf.space_after = Pt(space_before), Pt(space_after)
    pf.left_indent, pf.first_line_indent = Inches(left), Inches(first)
    pf.keep_with_next = keep
    if align is not None:
        p.alignment = align
    return p


def bottom_rule(paragraph):
    pPr = paragraph._p.get_or_add_pPr()
    bdr = OxmlElement("w:pBdr")
    bottom = OxmlElement("w:bottom")
    for k, v in (("val", "single"), ("sz", "6"), ("space", "1"), ("color", "000000")):
        bottom.set(qn("w:" + k), v)
    bdr.append(bottom)
    pPr.append(bdr)


def no_borders(table):
    tblPr = table._tbl.tblPr
    borders = OxmlElement("w:tblBorders")
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        el = OxmlElement("w:" + edge)
        el.set(qn("w:val"), "nil")
        borders.append(el)
    tblPr.append(borders)
    mar = OxmlElement("w:tblCellMar")                   # zero cell padding
    for edge in ("left", "right"):
        el = OxmlElement("w:" + edge)
        el.set(qn("w:w"), "0"); el.set(qn("w:type"), "dxa")
        mar.append(el)
    tblPr.append(mar)


def build_docx(name, contact, sections, path, font, size, margin):
    doc = Document()
    sec = doc.sections[0]
    sec.orientation = WD_ORIENT.PORTRAIT
    sec.page_width, sec.page_height = Inches(8.5), Inches(11)
    for side in ("left_margin", "right_margin", "top_margin", "bottom_margin"):
        setattr(sec, side, Inches(margin))
    width = 8.5 - 2 * margin

    normal = doc.styles["Normal"]
    normal.font.name, normal.font.size = font, Pt(size)
    normal.element.rPr.rFonts.set(qn("w:eastAsia"), font)
    normal.paragraph_format.space_after = Pt(0)
    normal.paragraph_format.line_spacing = 1.0
    doc.core_properties.title = re.sub(r"\\[A-Za-z]+\s*|[{}]", "", name).strip()
    doc.core_properties.author = doc.core_properties.title

    def right_tab(p):
        p.paragraph_format.tab_stops.add_tab_stop(Inches(width), WD_TAB_ALIGNMENT.RIGHT)

    # Header
    p = para(doc, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=3)
    add_rich(p, name, size * 2.0, {"bold": True, "caps": True})
    for items in contact:
        p = para(doc, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=1)
        for k, item in enumerate(items):
            if k:
                format_run(p.add_run("  |  "), {}, size - 0.5)
            add_rich(p, item, size - 0.5)

    small = size - 0.5
    for title, records in sections:
        p = para(doc, space_before=9, space_after=3, keep=True)
        add_rich(p, title, size * 1.2, {"caps": True})
        bottom_rule(p)

        prev = None
        for kind, cols in records:
            if kind in ("HEAD", "ROW", "SUB"):
                is_sub = kind == "SUB" or (kind == "ROW" and prev in ("HEAD", "SUB", "BULLET")
                                            and all(c.startswith("\\textit") for c in cols))
                before = 0 if kind == "SUB" else (1 if is_sub else 5)
                if prev is None:
                    before = 0
                p = para(doc, space_before=before, keep=True)
                right_tab(p)
                add_rich(p, cols[0], small if is_sub else size)
                if len(cols) > 1:
                    p.add_run("\t")
                    add_rich(p, cols[1], small if is_sub else size)
            elif kind == "BULLET":
                p = doc.add_paragraph(style="List Bullet")
                pf = p.paragraph_format
                pf.left_indent, pf.first_line_indent = Inches(0.4), Inches(-0.18)
                pf.space_before = Pt(1.5 if prev == "BULLET" else 1)
                pf.space_after = Pt(0)
                add_rich(p, cols[0], small)
            elif kind == "PUB":
                p = para(doc, space_before=2 if prev else 0, left=0.6, first=-0.6)
                p.paragraph_format.tab_stops.add_tab_stop(Inches(0.6))
                add_rich(p, cols[0], small)
                p.add_run("\t")
                add_rich(p, cols[1], small)
            elif kind == "LINE":
                p = para(doc, left=0.15, space_after=1)
                add_rich(p, cols[0], small)
            elif kind == "WIDE":                         # wrapping text + date: borderless table
                t = doc.add_table(rows=1, cols=2)
                t.alignment = WD_TABLE_ALIGNMENT.LEFT
                t.autofit = False
                no_borders(t)
                widths = (width - 1.75, 1.75)
                for col, w in zip(t.columns, widths):    # grid widths (LibreOffice reads these)
                    col.width = Inches(w)
                for cell, text, w in zip(t.rows[0].cells, cols + [""], widths):
                    cell.width = Inches(w)
                    cp = cell.paragraphs[0]
                    cp.paragraph_format.space_after = Pt(2)
                    add_rich(cp, text, small)
                t.rows[0].cells[1].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
            else:                                        # PARA (unrecognised leftovers)
                add_rich(para(doc), cols[0], small)
            prev = kind
    doc.save(path)


# --------------------------------------------------------------------------- #
def to_odt(docx_path, odt_path):
    soffice = shutil.which("soffice") or shutil.which("libreoffice")
    if soffice:
        with tempfile.TemporaryDirectory() as tmp:
            subprocess.run([soffice, "--headless", "--convert-to", "odt", "--outdir", tmp, str(docx_path)],
                           check=True, capture_output=True)
            shutil.move(str(Path(tmp) / (docx_path.stem + ".odt")), odt_path)
    elif shutil.which("pandoc"):
        print("note: LibreOffice not found; using pandoc (some layout is lost)", file=sys.stderr)
        subprocess.run(["pandoc", str(docx_path), "-o", str(odt_path)], check=True)
    else:
        sys.exit("error: .odt output needs LibreOffice (soffice) or pandoc installed")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--input", nargs="?", help="LaTeX source")
    ap.add_argument("-o", "--output", help="output .docx or .odt (default: input name with .docx)")
    ap.add_argument("--font", default="Palatino Linotype", help="body font (default: Palatino Linotype)")
    ap.add_argument("--size", type=float, default=10, help="body font size in pt (default: 10.5)")
    ap.add_argument("--margin", type=float, default=0.5, help="page margins in inches (default: 0.5)")
    args = ap.parse_args()

    src = Path(args.input)
    out = Path(args.output) if args.output else src.with_suffix(".docx")
    fmt = out.suffix.lower()
    if fmt not in (".docx", ".odt"):
        ap.error("output file must end in .docx or .odt")

    name, contact, sections = parse(src.read_text(encoding="utf-8"))
    out.parent.mkdir(parents=True, exist_ok=True)
    if fmt == ".docx":
        build_docx(name, contact, sections, out, args.font, args.size, args.margin)
    else:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_docx = Path(tmp) / (out.stem + ".docx")
            build_docx(name, contact, sections, tmp_docx, args.font, args.size, args.margin)
            to_odt(tmp_docx, out)
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()