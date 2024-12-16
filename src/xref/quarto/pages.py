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


def make_header(hide_code=True, **kwargs):
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


# footer

# website:
#   page-footer:
#     left: "Copyright 2021, Norah Jones"
#     right:
#       - icon: github
#         href: https://github.com/
#       - icon: twitter
#         href: https://twitter.com/
