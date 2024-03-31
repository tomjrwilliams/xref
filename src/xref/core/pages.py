
from __future__ import annotations

import attrs

import xtuples

from . import fields
from . import nodes

from attrs_strict import type_validator

# -----------------------------------------------

@attrs.define(frozen=True)
class Page(nodes.Node):
    active: bool = fields.typed_field()

    # can be any node
    # section, def, etc.
    # rendered in order, recursively downwards
    # sections hvae the same approach

    # so rendering is up to the relevant child
    # can have outer wrapping, but for the most part, just concatenate the strings

    # ie. return lists of strings that we flatten at the outer layer and join

    # arguably for terms and topics, allow that to be highlighted outside of the text, and then auto label all the text
    # so the render takes pace in the database context, text render replaes term / topic / startup etc. with the relevant page url

    def update(self, **kwargs):
        return

    def add(self, node):
        pass

    # TODO: filter?

    def to_qmd(self, fp = None, dp = None):
        # essentially map over nodes
        return

# about, contact, etc. other template pages?

# if on the toolbar or not?




# the specific kinds just usb class page, take meta / targeting data (eg. person if a eprson page)

# and then have a from_database methid (page db), that builds from db


# and then uses the parent level render() etc. methods

# which itself calls generic resolve etc methods for cross page links


# ideally we want to write to qmd files, and then just call the inbuilt quarto render


# -----------------------------------------------

# eg. glossary with index containing links to all terms (possibly filtered by a predicate)

# ranked by links, importance, etc. (ideally with in page re-sorting possible eg by title alphabetically, created time)

# @attrs.define(frozen=True)
# class Index(Page):
#     pass

# @attrs.define(frozen=True)
# class Glossary(Index):
#     # term topic or mixed
#     pass

# @attrs.define(frozen=True)
# class Blog(Index):
#     pass

# -----------------------------------------------

@attrs.define(frozen=True)
class Paper(Page):
    # can auto build
    # or manual
    # or semi manual: auto and filter func
    pass


@attrs.define(frozen=True)
class Post(Page):
    pass

    # internal node id acc

    # BELOW ARe all on theparent class

    # def resolve(self):
    #     # resolve ids to actual nodes
    #     return

    # # outbound id links eg. via selectors
    # def link(self):
    #     return

    # def render(self):
    #     return

    # def section(self):
    #     return


# all as context managers?


@attrs.define(frozen=True)
class Term(Page):
    pass

@attrs.define(frozen=True)
class Topic(Page):
    # can auto build
    # or manual
    # or semi manual: auto and filter func
    pass


@attrs.define(frozen=True)
class Category(Page):
    # can auto build
    # or manual
    # or semi manual: auto and filter func
    pass


@attrs.define(frozen=True)
class Person(Page):
    # can auto build
    # or manual
    # or semi manual: auto and filter func
    pass



@attrs.define(frozen=True)
class Paper(Page):
    pass

@attrs.define(frozen=True)
class Startup(Page):
    pass


# -----------------------------------------------
