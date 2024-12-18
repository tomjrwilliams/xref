from __future__ import annotations

from typing import (
    Optional,
    Union,
    NamedTuple,
    TYPE_CHECKING,
)

from ..utils import *
from . import qmd

# ------------------------------------


class Annotation(NamedTuple):
    pass


# ------------------------------------

# separate type for markups?

class Term(Annotation):
    pass

class Definition(Annotation):
    pass

class Reference(Annotation):
    # infer if internal or external
    # and / or just a link
    pass

class Code(Annotation):
    # exec or just display
    pass

class Math(Annotation):
    # inline or not
    pass

class Hyperlink(Annotation):
    pass

class Image(Annotation):
    pass

class Table(Annotation):
    # optionally even a pretty table html blob
    # saved as a file in the relevant dir (on build)
    pass

class Markup(Annotation):
    q: qmd.QmdMarkup

# ------------------------------------

# tags are used for index building, and hence page auto generation (primarily listicles)
# we define them up front, and import them into articles (so no circular references)

class Tag(Annotation):
    pass

class Topic(Tag):
    pass

class Person(Tag):
    pass

class Organisation(Tag):
    pass

class Technology(Tag):
    pass

# sources are how we pull out citation keys from the central references index
# so presumably centrally defined and imported into articles
# and with fields required for citation generation
class Source(Tag):
    pass

class Article(Source):
    pass

# ------------------------------------

class Paragraph(NamedTupleBase):

    # marker locs in the text using eg. #label(.{...}.{...}etc.), get stripped out / replaced
    # that are then tagged by key name in annotations to get loc indices in string
    # optional as none means whole paragraph
    # then process as required for qmd (eg. term definition together)
    # or looking up citation keys by source tags

    text: str
    annotations: dict[
        Optional[str], list[Annotation]
    ]
    # NOTE: annotations on key str so changing order / adding new doesnt change (as it would if index based)

# ------------------------------------


# used both for listicle generation, and for building the hierarchical side nav
# and for central reference index

class Index(NamedTupleBase):
    pass


# ------------------------------------


class Page(NamedTuple):
    q: qmd.Page


class Article(Page):
    q: qmd.Page
    paragraphs: list[Paragraph]


class Listicle(Page):
    q: qmd.ListingPage
    articles: list[Article]
    # write meta-data to yml, create a listicle referencing the yml file


class Glossary(Page):
    q: Page
    paragraphs: list[Paragraph]

    # NOTE: pull out and sort (eg. alpha etise) every term-definition on the site
    # optionally that intersect with a given tag on a page (eg. by topic)
    # or group by topics

# ------------------------------------


class Site:
    # sources?
    indices: list[Index]
    pages: list[Page]


# ------------------------------------
