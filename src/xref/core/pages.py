
from __future__ import annotations

import pprint

import attrs

from typing import (
    Optional, Any, Type, Callable, Union
)

import xtuples

from . import fields
from . import nodes

from .nodes import Page, Node

from attrs_strict import type_validator

# -----------------------------------------------

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


# TODO: papers, posts, etc. - written stuff - just show the content

# topic is the same as term, but what - instead of the bottom being topics (as it is for all the others), instead its terms?

# term: definition

# then list of any summary and explanation / examples if given, that are attached specifically to a term node

# in quote style, so start with the link, and then the quote block

# then page break

# and then the same style, but broken by each of the other page types
# eg. articles referenced in, startup write ups, etc.

# ie. Header: Articles, then list of the above
# Header: Startups, etc.

# here, it's instead the node with the term, and one either side, with ... beyomd

# with the link again before the quote block


# page break between each type


# startups, people, similar, just without definition presumably?

# maybe there's an equivalent to a definition


# flat organisation, so can drop the category
# no hierarchy, as term can be in several topics (same for startups etc.)

# topics otherwise exactly like terms


# so the references are always to written pieces, from the derived pieces


# can perhaps then have at the bottom, a topics set of links

# with topic and definition



# then the written ones, have at the bottom as foot note

# the terms, topics, etc.

# with links

# just the definition / tagline

# in the form: [hyperlinl]: defijnition

# small page sep line between each section



# the derived ones use extract for the extraction

# make the target name bold

# and any headers extracted (but they're now the same font size as normal, not large)



# -----------------------------------------------

@attrs.define(frozen=True)
class Briefing(Page):
    # eg, of a startup

    # formal write up of something that's not specifically a paper
    # but is still of an external thing
    
    active: bool = fields.typed_field(default=True)
  
@attrs.define(frozen=True)
class Article(Page):
    
    active: bool = fields.typed_field(default=True)

    def allowed_children(self):
        return [nodes.Summary]


@attrs.define(frozen=True)
class Post(Page):
    # the most 'internal' in that it can be cross sectional content
    # rank first?

    # papers second, then briefings
    
    active: bool = fields.typed_field(default=True)

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

# above are the written kind, just show as is

# and appear in the feed

# below are only via the top nav into side nav

# -----------------------------------------------


def init_if_type(
    node: Node,
    acc: dict[Any, Page],
    T: Type[Node],
    P: Type[Page],
    node_func: Union[str, Callable],
    key_func: Optional[Union[str, Callable]]=None,
    and_func: Optional[Callable] = None,
):
    if key_func is None:
        key_func = node_func
    if isinstance(node, T):
        if isinstance(key_func, str):
            k = getattr(node, key_func)
        else:
            k = key_func(node)
        if k not in acc:
            if and_func is not None:
                if not and_func(node):
                    return acc
            if isinstance(node_func, str):
                n = P.new(getattr(node, node_func))
            else:
                n = node_func(node)
                if isinstance(n, tuple):
                    n = P.new(*n)
            acc[k] = n
    return acc

def extract_text_containing(
    self, node, txt
):
    if isinstance(node, nodes.Text):
        if txt in node.text:
            return self.update(
                occurences=self.occurences.append(node.id)
            )
        return self
    return self

def extract_text_with_child(
    self,
    node,
    child,
    clean_func: Optional[Callable] = None,
):
    if isinstance(node, nodes.Text):
        for ch in node.children:
            if clean_func is not None:
                ch = clean_func(ch)
            if child == ch:
                return self.update(
                    occurences=self.occurences.append(node.id)
                )
        return self
    return self

# -----------------------------------------------



@attrs.define(frozen=True)
class Term(Page):
    
    target: str = fields.typed_field()

    occurences: xtuples.iTuple[int] = fields.typed_field(
        default=xtuples.iTuple()
    )
    active: bool = fields.typed_field(default=True)

    @classmethod
    def init_pages(
        cls, node: Node, acc: dict[Any, Page]
    ):
        return init_if_type(
            node, acc, nodes.Term, cls, "text",
        )

    def extract_content(
        self, node: Node,
    ):
        return extract_text_containing(self, node, self.target)

@attrs.define(frozen=True)
class Topic(Page):
    
    target: str = fields.typed_field()

    occurences: xtuples.iTuple[int] = fields.typed_field(
        default=xtuples.iTuple()
    )
    active: bool = fields.typed_field(default=True)

    @classmethod
    def init_pages(
        cls, node: Node, acc: dict[Any, Page]
    ):
        return init_if_type(
            node, acc, nodes.Topic, cls, "text",
        )

    def extract_content(
        self, node: Node,
    ):
        return extract_text_containing(self, node, self.target)



# -----------------------------------------------

@attrs.define(frozen=True)
class Person(Page):

    target: nodes.Person = fields.typed_field()

    occurences: xtuples.iTuple[int] = fields.typed_field(
        default=xtuples.iTuple()
    )
    active: bool = fields.typed_field(default=True)
    
    @classmethod
    def init_pages(
        cls, node: Node, acc: dict[Any, Page]
    ):
        return init_if_type(
            node,
            acc,
            nodes.Person,
            cls,
            nodes.remove_children,
            and_func = lambda n: n.profile,
        )

    def extract_content(
        self, node: Node,
    ):
        return extract_text_with_child(
            self,
            node,
            self.target,
            clean_func=nodes.remove_children,
        )


@attrs.define(frozen=True)
class Organisation(Page):

    target: nodes.Person = fields.typed_field()

    occurences: xtuples.iTuple[int] = fields.typed_field(
        default=xtuples.iTuple()
    )
    active: bool = fields.typed_field(default=True)
    
    @classmethod
    def init_pages(
        cls, node: Node, acc: dict[Any, Page]
    ):
        return init_if_type(
            node,
            acc,
            nodes.Organisation,
            cls,
            nodes.remove_children,
            and_func = lambda n: n.profile,
        )

    def extract_content(
        self, node: Node,
    ):
        return extract_text_containing(
            self,
            node,
            self.target,
            clean_func=nodes.remove_children,
        )


# -----------------------------------------------
