
from __future__ import annotations

import pprint

from typing import (
    Type,
    Any,
    Optional,
    Union,
)

import attrs

from . import fields
from . import nodes
from . import pages

import xtuples

# -----------------------------------------------


@attrs.define(frozen=True)
class Site:

    pages: xtuples.iTuple[pages.Page]

    def add(self, page: pages.Page):
        return attrs.evolve(self, pages=self.pages.append(page))

    @classmethod
    def new(cls, pages = xtuples.iTuple()):
        return cls(pages)

    # -- 

    def generate_pages(self):
        acc: dict[
            Type[pages.Page]: dict[Any, pages.Page]
        ] = {
            pages.Term: {},
        }
        for page in self.pages:
            acc = page.generate_pages(acc)
        return acc

    def accumulate_content(self, acc):
        """
        >>> p = pages.Article.new().add(nodes.summary("a b c").term("a"))
        >>> s = Site.new().add(p)
        >>> acc = s.generate_pages()
        >>> for t, t_acc in acc.items():
        ...     print(t)
        ...     for k, v in t_acc.items():
        ...         print(k, ":", v)
        <class 'xref.core.pages.Term'>
        a : Term(children=iTuple(), target='a', occurences=iTuple(), active=True)
        >>> acc = s.accumulate_content(acc)
        >>> for t, t_acc in acc.items():
        ...     print(t)
        ...     for k, v in t_acc.items():
        ...         print(k, ":", v)
        <class 'xref.core.pages.Term'>
        a : Term(children=iTuple(), target='a', occurences=iTuple(5), active=True)
        """
        for page in self.pages:
            acc = page.accumulate_content(acc)
        return acc

    # --

    def create_pages(self):
        # assign url and write empty page
        # given the map from page type to pages
        raise NotImplementedError()

    def build_feed(self):
        # of all the written posts
        raise NotImplementedError()

    # --

    def generate_yaml(self):
        # each page type gets its own sub-header in the yaml page
        # linking to the relevant pages

        # together with top nav nodes, if we haves pages of the relevant type
        # plus a generic startng template with eg. about page link
        raise NotImplementedError()

    # --

    def write_content(self):
        # generate qmd for each page, write to the .qmd file url 
        # given eg. a root directory for the stie
        raise NotImplementedError()

    def merge_content(self):
        # merge in the constants - eg. about page
        # eg. just merge in a given directory of static content
        raise NotImplementedError()

    # --

    def render_site(self):
        # call render on the directory
        return NotImplementedError()
    
    # deploy etc.?

    # --
    
# -----------------------------------------------
