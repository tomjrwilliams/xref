
from __future__ import annotations

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
        raise NotImplementedError()

    # -- 

    def generate_pages(self):
        acc: dict[
            Type[pages.Page]: dict[Any, pages.Page]
        ] = {
            pages.Term: {},
        }

        for page in self.pages:
            acc = page.generate_pages(acc)
            
        # call classmethod from each page type
        # eg. term, that gets all terms
        # and creates a page object for each
        # mostly its just that: iterating over all the content 
        # to find various data types (terms, topics, startups, etc.)
        # so can have a single recursive iter, where for each node we then iter through the page types for a hit

        # also collect content for the page on the way (eg. for the term, the node and children that contained the term text)
        return

    # --

    def create_pages(self):
        # assign url and write empty page
        # given the map from page type to pages
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
