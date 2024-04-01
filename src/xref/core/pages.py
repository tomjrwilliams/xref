
from __future__ import annotations

import datetime

import pprint
import io

import yaml
import attrs

from typing import (
    Optional, Any, Type, Callable, Union
)

import xtuples

from . import utils
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

# ie. Header: Papers, then list of the above
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

    @classmethod
    def nav_folder(cls):
        return "terms"

    @classmethod
    def nav_title(cls):
        return "Terms"

    def title(self):
        return self.target

    def handle(self):
        return self.target


term = Term.new

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

    @classmethod
    def nav_folder(cls):
        return "topics"

    @classmethod
    def nav_title(cls):
        return "Topics"

    def title(self):
        return self.target

    def handle(self):
        return self.target


topic = Topic.new

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


person = Person.new

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

organisation = Organisation.new

# -----------------------------------------------

@attrs.define(frozen=True)
class Brief(Page):
    # eg, of a startup

    # formal write up of something that's not specifically a paper
    # but is still of an external thing

    title: str = fields.typed_field()
    created: datetime.date = fields.typed_field()

    active: bool = fields.typed_field(default=True)

    handle: Optional[str] = fields.optional_field()

    @classmethod
    def nav_folder(cls):
        return "briefs"

    @classmethod
    def nav_title(cls):
        return "Briefs"

brief = Brief.new
  
@attrs.define(frozen=True)
class Paper(Page):

    title: str = fields.typed_field()
    created: datetime.date = fields.typed_field()
    
    active: bool = fields.typed_field(default=True)

    handle: Optional[str] = fields.optional_field()

    def allowed_children(self):
        return [nodes.Summary]

    @classmethod
    def nav_folder(cls):
        return "papers"

    @classmethod
    def nav_title(cls):
        return "Papers"

    def header_qmd(self):
        yml = dict(
            title=self.get_string_like("title"),
            # description: "Post description"
            # author: "Fizz McPhee"
            date=self.created.strftime("%m/%d/%Y"),
            # date: "5/22/2021"
            # categories:
            # - news
            # - code
            # - analysis
        )
        s = utils.qmd_header(yml)
        return s

article = Paper.new

@attrs.define(frozen=True)
class Post(Page):
    # the most 'internal' in that it can be cross sectional content
    # rank first?

    # papers second, then briefs

    title: str = fields.typed_field()
    created: datetime.date = fields.typed_field()
    
    active: bool = fields.typed_field(default=True)

    handle: Optional[str] = fields.optional_field()

    @classmethod
    def nav_folder(cls):
        return "posts"

    @classmethod
    def nav_title(cls):
        return "Posts"

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

post = Post.new

# above are the written kind, just show as is

# and appear in the feed

# below are only via the top nav into side nav

# -----------------------------------------------
