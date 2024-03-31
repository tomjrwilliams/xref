from __future__ import annotations

from typing import Optional

import functools
import itertools
import time
import dataclasses

import datetime

import functools

import abc
import collections.abc
import typing
import csv

import hashlib

import sys

import functools

import tempfile
import pathlib

import contextlib
import typing
import json

import dataclasses

import distutils.dir_util
import hashlib

import subprocess

import hashlib

# -------------------------------------------------------------------

# code

def indent(code: str, n=1):
    return "\n".join([("    " * n) + l for l in code.split("\n")])


def print_error(
    filter_ends_with: list[str] = [],
    filter_starts_with: list[str] = [],
):
    filts = [
        f"""not l.strip().startswith('{s}')"""
        for s in filter_starts_with
    ] + [
        f"""not l.strip().startswith('{s}')"""
        for s in filter_ends_with
    ]
    return indent(
        "\n".join(
            [
                "if error:",
                """    ls = tb.split("\\n")""",
                """    ls = [""",
                """        l for l in ls""",
                """        if not any([""",
            ] + filts + [
                """        ])""",
                """    ]""",
                """    assert False, "\\n".join(ls)""",
            ]
        )
    )

def catch_error(
    code: str,
    print: bool = True,
    **print_kwargs
):
    return indent(
        "\n".join(
            [
                "error = False",
                "tb = ''",
                "try:",
            ]
            + [indent(code)]
            + [
                "except Exception:",
                "    sys.stdout.flush()",
                "    sys.stderr.flush()",
                "    error = True",
                "    tb = traceback.format_exc()",
            ]
        )
    ) + ("" if not print else print_error(
        **print_kwargs
    ))


def code_block(
    code,
    catch=True,
    print=True,
    **print_kwargs
):
    return "\n".join(
        [
            "```{" + "python}",
            # "#| error: true",
            "#| warning: false",
            "#| fig-align: center",
            "#| layout-align: center",
            (
                code 
                if catch is False 
                else catch_error(code, print=print, **print_kwargs)
            ),
            "```",
        ]
    )

# text

# *italics*, **bold**, ***bold italics***
# italics, bold, bold italics

# superscript^2^ / subscript~2~
# superscript2 / subscript2

# ~~strikethrough~~
# strikethrough

# `verbatim code`
# verbatim code

# > Blockquote

# Header 1 to 6, number of hashes

# * unordered list
#     + sub-item 1
#     + sub-item 2
#         - sub-sub-item 1

# unordered list
# sub-item 1
# sub-item 2
# sub-sub-item 1

# *   item 2

#     Continued (indent 4 spaces)

# item 2

# Continued (indent 4 spaces)

# 1. ordered list
# 2. item 2
#     i) sub-item 1
#          A.  sub-sub-item 1

# ordered list
# item 2
# sub-item 1
# sub-sub-item 1

# (@)  A list whose numbering

# continues after

# (@)  an interruption

# A list whose numbering
# continues after
# an interruption

# ::: {}
# 1. A list
# :::

# ::: {}
# 1. Followed by another list
# :::

# A list
# Followed by another list

# term
# : definition

# term
# definition


# <https://quarto.org>
# https://quarto.org

# [Quarto](https://quarto.org)
# Quarto

# ![Caption](elephant.png)
# A line drawing of an elephant.

# Caption
# [![Caption](elephant.png)](https://quarto.org)

# Caption
# [![Caption](elephant.png "An elephant")](https://quarto.org)

# A line drawing of an elephant.
# [![](elephant.png){fig-alt="Alt text"}](https://quarto.org)

# # maths

# inline math: $E = mc^{2}$
# inline math: 

# display math:
# $$E = mc^{2}$$

# # -------------------------------------------------------------------

# # tables

# | Right | Left | Default | Center |
# |------:|:-----|---------|:------:|
# |   12  |  12  |    12   |    12  |
# |  123  |  123 |   123   |   123  |
# |    1  |    1 |     1   |     1  |

# -------------------------------------------------------------------
# To provide a citation for an article published to the web, include author and date metadata as well as a citation url. For example:

# ---
# title: "Summarizing Output for Reproducible Documents"
# description: | 
#   A summary of the best practices for summarizing output of reproducible scientific documents.
# date: 5/4/2018
# author:
#   - name: Norah Jones 
#     url: https://example.com/norahjones
#     affiliation: Spacely Sprockets
#     affiliation-url: https://example.com/spacelysprockets
# citation:
#   url: https://example.com/summarizing-output
# bibliography: biblio.bib
# ---


# page

# title

# Document title

# subtitle

# Identifies the subtitle of the document.

# date

# Document date

# date-modified

# Document date modified

# author

# Author or authors of the document

# abstract

# Summary of document

# abstract-title

# Title used to label document abstract

# doi

# Displays the document Digital Object Identifier in the header.

# order

# Order for document when included in a website automatic sidebar menu.

# todo:

# toc-depth: n
# toc-expand: n
# toc-title
# toc-location: left / right / left-body / right-body

# smooth-scroll: true

# format:
#   html:
    # link-external-icon: true
    # link-external-newwindow: true
    # link-external-filter: '^(?:http:|https:)\/\/www\.quarto\.org\/custom'

# format:
#   html:
#     citations-hover: false
#     footnotes-hover: false
#     crossrefs-hover: false

# format:
#   html:
#     include-in-header:
#       - text: |
#           <script src="https://examples.org/demo.js"></script>
#       - file: analytics.html
#       - comments.html
#     include-before-body: header.html

# --
# format:
#   html:
#     other-links:
#       - text: NASA Open Data
#         href: https://data.nasa.gov/
#     code-links:
#       - text: Data Import Code
#         icon: file-code
#         href: data-import.py
# --- txt, href, icon, rel, target

def make_header(hide_code = True, **kwargs):
    res = """---
title: "{title}"
page-layout: full
format:
  html:
    toc: true
    number-sections: true
    code-fold: true
    self-contained: true
---
""".format(
        **kwargs
    )
    if hide_code:
        res = res.replace("code-fold: true", "echo: false")
    return res

# -------------------------------------------------------------------


# ```{python}
# | label: fig-polar
# | fig-cap: "A line plot on a polar axis"

# import xyz
# ```

# -------------------------------------------------------------------

# website

# _quarto.yml

# project:
#   type: website

# website:
#   title: "today"
#   navbar:
# ...

# website:
#   navbar:
#     background: primary
#     search: true
#     left:
#       - text: "Home"
#         file: index.qmd
#       - talks.qmd
#       - about.qmd

# title
# Navbar title (uses the site: title if none is specified). Use title: false to suppress the display of the title on the navbar.
# logo
# Logo image to be displayed left of the title.
# logo-alt
# Alternate text for the logo image.
# logo-href
# Target href from navbar logo / title. By default, the logo and title link to the root page of the site (/index.html).
# background
# Background color (“primary”, “secondary”, “success”, “danger”, “warning”, “info”, “light”, “dark”, or hex color).
# foreground
# Foreground color (“primary”, “secondary”, “success”, “danger”, “warning”, “info”, “light”, “dark”, or hex color). The foreground color will be used to color navigation elements, text and links that appear in the navbar.
# search
# Include a search box (true or false).
# tools
# List of navbar tools (e.g. link to github or twitter, etc.). See Navbar Tools for details.
# left / right
# Lists of navigation items for left and right side of navbar.
# pinned
# Always show the navbar (true or false). Defaults to false, and uses headroom.js to automatically show the navbar when the user scrolls up on the page.
# collapse
# Collapse the navbar items into a hamburger menu when the display gets narrow (defaults to true).
# collapse-below
# Responsive breakpoint at which to collapse navbar items to a hamburger menu (“sm”, “md”, “lg”, “xl”, or “xxl”, defaults to “lg”).
# toggle-position
# The position of the collapsed navbar hamburger menu when in responsive mode (“left” or “right”, defaults to “left”).

# per nav item:

# href
# Link to file contained with the project or external URL.
# text
# Text to display for navigation item (defaults to the document title if not provided).
# icon
# Name of one of the standard Bootstrap 5 icons (e.g. “github”, “twitter”, “share”, etc.).
# aria-label
# Accessible label for the navigation item.
# rel
# Value for rel attribute. Multiple space-separated values are permitted.
# menu
# List of navigation items to populate a drop-down menu

# side nav:
# website:
#   sidebar:
#     style: "docked"
#     search: true
#     contents:
#       - section: "Basics"
#         contents:
#           - index.qmd
#           - basics-knitr.qmd
#           - basics-jupyter.qmd
#       - section: "Layout"
#         contents:
#           - layout.qmd
#           - layout-knitr.qmd
#           - layout-jupyter.qmd

# # side nav options

# id
# Optional identifier (used only for hybrid navigation, described below).
# title
# Sidebar title (uses the project title if none is specified).
# subtitle
# Optional subtitle.
# logo
# Optional logo image.
# search
# Include a search box (true or false). Note that if there is already a search box on the top navigation bar it won’t be displayed on the sidebar.
# tools
# List of sidebar tools (e.g. link to github or twitter, etc.). See the next section for details.
# contents
# List of navigation items to display (typically top level items will in turn have a list of sub-items).
# style
# “docked” or “floating”.
# type
# “dark” or “light” (hint to make sure the text color is the inverse of the background).
# background
# Background color (“none”, “primary”, “secondary”, “success”, “danger”, “warning”, “info”, “light”, “dark”, or “white”). Defaults to “light”.
# foreground
# Foreground color (“primary”, “secondary”, “success”, “danger”, “warning”, “info”, “light”, “dark”, or hex color). The foreground color will be used to color navigation elements, text and links that appear in the sidebar.
# border
# Whether to show a border on the sidebar. “true” or “false”.
# alignment
# Alignment (“left”, “right”, or “center”).
# collapse-level
# Whether to show sidebar navigation collapsed by default. The default is 2, which shows the top and next level fully expanded (but leaves the 3rd and subsequent levels collapsed).
# pinned
# Always show a title bar that expands to show the sidebar at narrower screen widths (true or false). Defaults to false, and uses headroom.js to automatically show the navigation bar when the user scrolls up on the page.
# A single sidebar item without an id or title will result in a global sidebar applied to all pages. A sidebar with an id or title will only be applied to pages within the contents of the sidebar or pages that specify the sidebar id.

# example hybrid:

# To do this, provide a group of sidebar entries and link each group of sidebar entries with a navbar entry by matching their titles and listing the page linked from the navbar as the first content in the sidebar group

# A page that doesn’t appear in any sidebar will inherit and display the first sidebar without an id or title - you can prevent the sidebar from showing on a page by setting sidebar: false in it’s front matter.

    #   - text: "---"
    # for use as separator in sidenav

# website:
#   title: ProjectX
#   navbar:
#     background: primary
#     search: true
#     left:
#       - text: "Home"
#         file: index.qmd
#       - text: "Tutorials"
#         file: tutorials.qmd
#       - text: "How-To"
#         file: howto.qmd
#       - text: "Fundamentals"
#         file: fundamentals.qmd
#       - text: "Reference"
#         file: reference.qmd

#   sidebar:
#     - title: "Tutorials"
#       style: "docked"
#       background: light
#       contents:
#         - tutorials.qmd
#         - tutorial-1.qmd
#         - tutorial-2.qmd

#     - title: "How-To"
#       contents:
#         - howto.qmd
#         # navigation items

#     - title: "Fundamentals"
#       contents:
#         - fundamentals.qmd
#         # navigation items

#     - title: "Reference"
#       contents:
#         - reference.qmd
#         # navigation items
    

# Note that the first sidebar definition contains a few options (e.g. style and background). These options are automatically inherited by the other sidebars.



# footer

# website:
#   page-footer: 
#     left: "Copyright 2021, Norah Jones" 
#     right: 
#       - icon: github
#         href: https://github.com/
#       - icon: twitter 
#         href: https://twitter.com/ 



# citations

# Citation Syntax
# Quarto uses the standard Pandoc markdown representation for citations (e.g. [@citation]) — citations go inside square brackets and are separated by semicolons. Each citation must have a key, composed of ‘@’ + the citation identifier from the database, and may optionally have a prefix, a locator, and a suffix. The citation key must begin with a letter, digit, or _, and may contain alphanumerics, _, and internal punctuation characters (:.#$%&-+?<>~/). Here are some examples:

# Markdown Format
# Output (default)
# Output(csl: diabetologia.csl, see Section 1.3)

# Blah Blah [see @knuth1984, pp. 33-35;
# also @wickham2015, chap. 1]
# Blah Blah (see Knuth 1984, 33–35; also Wickham 2015, chap. 1)
# Blah Blah see [1], pp. 33-35; also [1], chap. 1

# Blah Blah [@knuth1984, pp. 33-35,
# 38-39 and passim]
# Blah Blah (Knuth 1984, 33–35, 38–39 and passim)
# Blah Blah [1], pp. 33-35, 38-39 and passim

# Blah Blah [@wickham2015; @knuth1984].
# Blah Blah (Wickham 2015; Knuth 1984).
# Blah Blah [1, 2].

# Wickham says blah [-@wickham2015]
# Wickham says blah (2015)
# Wickham says blah [1]

# # in text:


# Markdown Format
# Output (author-date format)
# Output (numerical format)

# @knuth1984 says blah.
# Knuth (1984) says blah.
# [1] says blah.

# @knuth1984 [p. 33] says blah.
# Knuth (1984, 33) says blah.
# [1] [p. 33] says blah.

# https://github.com/citation-style-language/styles

# Quarto uses Pandoc to format citations and bibliographies. By default, Pandoc will use the Chicago Manual of Style author-date format, but you can specify a custom formatting using CSL (Citation Style Language). To provide a custom citation stylesheet, provide a path to a CSL file using the csl metadata field in your document, for example:

# ---
# title: "My Document"
# bibliography: references.bib
# csl: nature.csl
# ---

### References

# ::: {#refs}
# :::