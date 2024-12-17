from __future__ import annotations

from typing import (
    TYPE_CHECKING,
)

from ..utils import *
from .. import quarto as q

# ------------------------------------


# virtual repr of site
# can be re-indexed / parsed after the fact


# create all the pages up front in a single page
# so they can be imported into the articles
# even before they havecontent
# so no cirular referenes (eg if two articles co-depend), and eg. you can tag with a listicle before you've filled the listicle


class Site:
    pass


class Page:
    pass


# the difference between orgs, people, topics is where the relevant header appears in the nav
# and what level of depth listicles are generated for them

# where can have listicles that are the system generated blogs based on eg. author date, tags

# but then can also have a "manually" created listicle that just lists the pages in an article as paragraphs


# so each is a subclass of tag
# added as an annotation


# and then the page / navs are created from a given parent type (eg. all people, all topics, etc.)

# can separate types of people / org (startup vs uni)
# that might imply separate nav sections, or that could be a label on the page (or both)

# separate nav sections perhaps, collapsible, within the one nav (so hierarchy is people / org / topic)
# and then within those, founder vs academic, etc.

# the label could even be in the title "name: (type eg. startup)"


class Article(Page):
    pass


class Listicle(Page):
    pass


class Element:
    pass


class Annotated:

    text: str
    key: str

    def __repr__(self):
        return


class Annotation:
    pass


class Label(Annotation):
    pass


# bold, strike through, italics, etc.


class Hyperlink(Annotation):
    pass


class Tag(Annotation):
    pass


# some are logical annoations (for indexing), some are content / formatting (eg. hyperlink)
# field to indicate which?

# term and def, presume (assert) appear after one another?


# one might want to use block quotes for eg. building up the one-article listicles (to quote the doc being refd)


# have a paraghraph level tag for eg. (non format, logical annotation) for which to use as the summary for the article
# which could also be between two tags (ie. a slice)


# so for labels, if provided twice, indicates a start end (int range)


# in that case, can apply more than once
# so also need to be able to write a lbael with no content which is then dropped from format, space removed, hence just used as an int slicer


class Paragraph(Element):

    # need to be able to tag the paragraph as a whole

    text: str
    keys: dict[int, str]
    annotations: dict[
        str, list[Annotation]
    ]  # on key str so changing order / adding new doesnt change

    # formats, str (?) that correspond to the various markup formats in quarto.text

    def add_text(self):
        # text as
        return

    def with_label(self):
        return  #


class Header:
    pass
