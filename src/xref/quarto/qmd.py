
from typing import Union, Optional
import polars

from ..utils import *
from .code import *

# ------------------------------------

# anything else?
ORDER_ENRICH = 0
ORDER_FORMAT = 1
ORDER_EMBED = 2

class QmdMarkup(NamedTupleBase):
    
    def sort_key(self):
        raise ValueError(type(self), self)

# ------------------------------------

class QmdLoc(NamedTupleBase):
    i: Optional[tuple[int, int]]

    def is_empty(self):
        return self.i is None

    def sort_key(self):
        res = (
            -1 if self.is_empty()
            else self.i[-1]
        )
        if res is None:
            raise ValueError(self)
        return res

# ------------------------------------

class QmdLocUpdate(NamedTupleBase):
    offsets: dict[int, int]
    more: list[dict[int, int]]

def update_qmd_loc(
    loc: QmdLoc,
    updates: list[Optional[QmdLocUpdate]],
):
    if loc.is_empty():
        # sure?
        return loc
    start, end = loc.i
    for u in updates:
        if u is None:
            continue
        for o in [u.offsets] + u.more:
            for i, offset in o.items():
                if i >= start:
                    start += offset
                if i >= end:
                    end += offset
    return QmdLoc((start, end))

# ------------------------------------

class QmdFormat(QmdMarkup):
    loc: QmdLoc

    def sort_key(self):
        return ORDER_FORMAT, self.loc.sort_key()

class QmdHeader(QmdFormat):
    loc: QmdLoc
    depth: int

class QmdItalics(QmdFormat):
    pass

class QmdBold(QmdFormat):
    pass

class QmdBoldItalics(QmdFormat):
    pass

class QmdStrikeThrough(QmdFormat):
    pass

class QmdCodeVerbatim(QmdFormat):
    pass

class QmdBlockQuote(QmdFormat):
    pass

class QmdMathInline(QmdFormat):
    pass

class QmdMathDisplay(QmdFormat):
    pass

class QmdCrossReference(QmdFormat):
    pass

class QmdList(QmdFormat):
    pass

class QmdListOrdered(QmdList):
    pass

class QmdListUnordered(QmdList):
    pass

# ^ these get spicy, need to add tabs? or no, just need to do string replace dpeendnet on depth (assume tabbed?)

def qmd_surround_string(
    s: str,
    loc: QmdLoc,
    prefix: str,
    postfix: str,
):
    if loc.is_empty():
        start = 0
        end = len(s)
    else:
        start, end = loc.i
    return (
        s[:start]
        + prefix
        + 
        s[start:end]
        + postfix
        + s[end:]
    ), QmdLocUpdate({
        start: len(prefix),
        end: len(prefix) + len(postfix)
    }, [])

def qmd_update_string(
    s: str,
    loc: QmdLoc,
    rep: str,
):
    if loc.is_empty():
        start = 0
        end = len(s)
    else:
        start, end = loc.i
    return (
        s[:start]
        + rep
        + s[end:]
    ), QmdLocUpdate({
        end: len(rep) - len(s[start:end])
    }, [])
def qmd_format(
    s: str,
    m: QmdFormat,
    updates: list[Optional[QmdLocUpdate]],
):
    loc=update_qmd_loc(
        m.loc, updates
    )
    prefix = None
    postfix = None
    if isinstance(m, QmdHeader):
        prefix = ("#" * m.depth) + " "
        postfix = "\n"
    if isinstance(m, QmdItalics):
        prefix = postfix = "*"
    elif isinstance(m, QmdBold):
        prefix = postfix = "**"
    elif isinstance(m, QmdBoldItalics):
        prefix = postfix = "***"
    elif isinstance(m, QmdStrikeThrough):
        prefix = postfix = "~~"
    elif isinstance(m, QmdCodeVerbatim):
        prefix = postfix = "`"
    elif isinstance(m, QmdMathInline):
        prefix = postfix = "$"
    elif isinstance(m, QmdMathDisplay):
        prefix = postfix = "$$"
    elif isinstance(m, QmdCrossReference):
        prefix = "@"
        postfix = ""
    elif isinstance(m, QmdBlockQuote):
        prefix = "> "
        postfix = ""
    else:
        raise ValueError(m)
    return qmd_surround_string(
        s, loc, prefix, postfix
    )

# ------------------------------------

class QmdEnrich(QmdMarkup):
    loc: QmdLoc

    def sort_key(self):
        return ORDER_ENRICH, self.loc.sort_key()

class QmdSubScript(QmdFormat):
    loc: QmdLoc
    v: str

class QmdSupScript(QmdFormat):
    loc: QmdLoc
    v: str

class QmdTermDefinition(QmdEnrich):
    loc: QmdLoc
    loc_defn: QmdLoc

class QmdHyperlink(QmdEnrich):
    loc: QmdLoc
    url: str

class QmdImage(QmdEnrich):
    loc: QmdLoc
    fp: str
    label: Optional[str]
    alt: Optional[str]

class QmdCitation(QmdEnrich):
    loc: QmdLoc
    page: Optional[int | tuple[int, int]]
    chapter: Optional[int]

def qmd_enrich(
    s: str,
    m: QmdEnrich,
    updates: list[Optional[QmdLocUpdate]],
):
    loc=update_qmd_loc(
        m.loc, updates
    )
    prefix = None
    postfix = None
    if isinstance(m, QmdSubScript):
        prefix = ""
        postfix = f"~{m.v}~"
    elif isinstance(m, QmdSupScript):
        prefix = ""
        postfix = f"^{m.v}^"
    elif isinstance(m, QmdTermDefinition):
        loc_defn = update_qmd_loc(
            m.loc, updates
        )
        if not loc_defn.i[0] == loc.i[1]:
            raise ValueError(m)
        prefix = postfix = "\n"
        s, u1 = qmd_surround_string(
            s, loc, prefix, postfix
        )
        prefix = ": "
        postfix = "\n"
        s, u2 = qmd_surround_string(
            s, loc, prefix, postfix
        )
        return s, QmdLocUpdate(u1, [u2])
    elif isinstance(m, QmdHyperlink):
        prefix = "["
        postfix = f"]({m.url})"
    elif isinstance(m, QmdImage):
        prefix = "[!["
        postfix = f"]({m.fp})"
        if m.alt:
            postfix += "{" + f'fig-alt="{m.alt}"' + "}"
        if m.label:
            postfix += "{" + f"#{m.label}" + "}"
    elif isinstance(m, QmdCitation):
        if m.page is None and m.chapter is None:
            prefix = "@"
            postfix = ""
        else:
            prefix = "[@"
            postfix = ""
            if isinstance(m.page, int):
                postfix += f", p.{m.page}"
            elif isinstance(m.page, tuple):
                il, ir = m.page
                postfix += f", pp.{il}-{ir}"
            else:
                pass
            if m.chapter is not None:
                postfix += f", chap. {m.chapter}"
            postfix += "]"
    else:
        raise ValueError(m)
    return qmd_surround_string(
        s, loc, prefix, postfix
    )

# NOTE: for citation, image caption, assumes text just needs to be wrapped (no database lookups or even string replace)
# therefore upstream might need to inject / replace the citation label for you (Eg. based on looking up in a database of citations, for the label you want to use for that ref, given the logical tag on the text)

# ------------------------------------

# TODO:
# Here is a footnote reference,[^1] and another.[^longnote]

# [^1]: Here is the footnote.

# [^longnote]: Here's one with multiple blocks.

#     Subsequent paragraphs are indented to show that they
# belong to the previous footnote.

#         { some.code }

#     The whole paragraph can be indented, or just the first
#     line.  In this way, multi-paragraph footnotes work like
#     multi-paragraph list items.

# This paragraph won't be part of the note, because it
# isn't indented.

# ------------------------------------

class QmdEmbed(QmdMarkup):
    loc: QmdLoc

    def sort_key(self):
        return ORDER_EMBED, self.loc.sort_key()

class QmdHtml(QmdEmbed):
    loc: QmdLoc
    fp: str
    label: Optional[str]
    width: Optional[int]
    height: Optional[int]
    # eg. pretty tables

class QmdPython(QmdEmbed):
    loc: QmdLoc
    py: str
    label: Optional[str]
    caption: Optional[str]
    table: bool

class QmdTable(QmdEmbed):
    loc: QmdLoc
    df: polars.DataFrame
    label: Optional[str]
    # headers, etc.

class QmdReferences(QmdEmbed):
    loc: QmdLoc
    
# TODO: QmdMermaid
# https://quarto.org/docs/authoring/diagrams.html#mermaid-formats
# ```{mermaid}
# flowchart LR
#   A[Hard edge] --> B(Round edge)
#   B --> C{Decision}
#   C --> D[Result one]
#   C --> E[Result two]
# ```

def qmd_embed(
    s: str,
    m: QmdEmbed,
    updates: list[Optional[QmdLocUpdate]],
):
    loc=update_qmd_loc(
        m.loc, updates
    )
    if isinstance(m, QmdHtml):
        height = 500 if m.height is None else m.height
        width = 800 if m.width is None else m.width
        label = "" if m.label is None else f"# | label: {m.label}"
        s, e = loc.i
        title = s[s:e]        
        rep = "\n".join([
           "```{=html}",
           label,
           f'<iframe width="{width}" height="{height}" src="{m.fp}" title="{title}"></iframe>',
           "```"
        ])
    elif isinstance(m, QmdPython):
        yml = "\n"
        if m.label:
            yml = f"{yml}# | label: {m.label}\n"
        if m.caption and not m.table:
            yml = f"{yml}# | fig-cap: {m.caption}"
        elif m.caption and m.table:
            yml = f"{yml}# | tbl-cap: {m.caption}"
        if yml == "\n":
            yml = None
        rep = qmd_code_block(
            m.py,
            yml=yml,
        )
    elif isinstance(m, QmdTable):
        df = m.df
        hs = list(df.schema.keys())
        rs = df.iter_rows(named=False)
        rep = "\n".join([
            "|" + "|".join(hs) + "|"
        ] + [
            "|" + "|".join([
                "---" for _ in hs
            ]) + "|"
        ] + [
            "|" + "|".join(r) + "|"
            for r in rs
        ])
    elif isinstance(m, QmdReferences):
        rep = ":::{#refs}\n:::"
    return qmd_update_string(
        s, loc, rep
    )

# ------------------------------------

# https://quarto.org/docs/authoring/tables.html
# from IPython.display import Markdown
# from tabulate import tabulate
# table = [["Sun","696,000",1.989e30],
#          ["Earth","6,371",5.972e24],
#          ["Moon","1,737",7.34e22],
#          ["Mars","3,390",6.39e23]]
# Markdown(tabulate(
#   table, 
#   headers=["Astronomical object","R (km)", "mass (kg)"]
# ))

# ------------------------------------

def qmd_markup(
    s: str,
    markups: list[QmdMarkup],
):
    markups = list(sorted(
        markups,
        key = lambda m: m.sort_key()
    ))
    loc_updates: list[
        Optional[QmdLocUpdate]
    ] = []
    for m in markups:
        if isinstance(m, QmdFormat):
            s, loc_update = qmd_format(
                s, m, loc_updates
            )
        elif isinstance(m, QmdEnrich):
            s, loc_update = qmd_enrich(
                s, m, loc_updates
            )
        elif isinstance(m, QmdEmbed):
            s, loc_update = qmd_embed(
                s, m, loc_updates
            )
        else:
            raise ValueError(m)
        loc_updates.append(loc_update)
    return s

# ------------------------------------