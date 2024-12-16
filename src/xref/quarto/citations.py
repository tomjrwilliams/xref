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
