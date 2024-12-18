from __future__ import annotations

import datetime

from typing import (
    TYPE_CHECKING,
)

from ...utils import *

from .navs import *

# ------------------------------------


class FieldsHtmlFormat(NamedTuple):
    code_fold: bool
    echo: Optional[bool]

    toc: Optional[bool]
    toc_title: Optional[str]
    toc_depth: Optional[int]
    # how many layers of headers to include in toc (default 3)
    toc_expand: Optional[int | bool]
    # true start with all expanded (default 1)
    toc_location: Optional[str]  # default right

    smooth_scroll: Optional[bool]

    anchor_sections: Optional[bool]
    number_sections: Optional[bool]

    citations_hover: Optional[bool]
    footnotes_hover: Optional[bool]
    crossrefs_hover: Optional[bool]

    self_contained: Optional[bool]


class HtmlFormat(
    FieldsHtmlFormat,
    TraitYmlHasRepr,
    # TraitYmlHasFieldMap,
    TraitYmlHasQuoteMap,
):

    @classmethod
    def yml_quote_map(cls):
        return dict(
            toc_location=False,
        )


# ------------------------------------


class FieldsPageFormat(NamedTuple):
    html: HtmlFormat


class PageFormat(
    FieldsPageFormat,
    TraitYmlHasRepr,
    # TraitYmlHasFieldMap,
    # TraitYmlHasQuoteMap,
):
    pass


# ------------------------------------


class FieldsPage(NamedTuple):
    title: str
    subtitle: Optional[str]
    date: Optional[datetime.date]
    date_modified: Optional[datetime.date]
    author: Optional[str]
    abstract: Optional[str]
    abstract_title: Optional[str]
    doi: Optional[bool]
    order: Optional[int]
    format: PageFormat
    page_layout: str
    # = full


class Page(
    FieldsPage,
    TraitYmlHasRepr,
    # TraitYmlHasFieldMap,
    TraitYmlHasQuoteMap,
):

    @classmethod
    def yml_quote_map(cls):
        return dict(
            page_layout=False,
        )


# ------------------------------------


class FieldsAbout(NamedTuple):
    template: str
    links: Optional[list[NavLink]]
    image_width: Optional[str]
    image_shape: Optional[str]


class About(
    FieldsAbout, TraitYmlHasRepr, TraitYmlHasQuoteMap
):

    @classmethod
    def yml_quote_map(cls):
        return dict(
            template=False,
            image_width=False,
            image_shape=False,
        )


# ------------------------------------


class FieldsAboutPage(NamedTuple):
    title: str
    image: str
    about: About


class AboutPage(
    FieldsAboutPage, TraitYmlHasRepr, TraitYmlHasQuoteMap
):

    @classmethod
    def yml_quote_map(cls):
        return dict(
            image=False,
        )


# ------------------------------------


class FieldsListing(NamedTuple):
    contents: list[str]
    # glob file paths or yaml file (with the meta data needed for listing eg. title, author, description, date, path, categories, etc.)
    type: str
    # default or table or grid
    sort: Optional[bool | str | list[str]]
    # eg. date, title desc

    categories: bool

    fields: Optional[list[str]]

    page_size: Optional[int]

    # not all these are available for each type, but cba to spell out which for which
    max_items: Optional[int]
    image_align: Optional[str]
    image_height: Optional[int]
    image_placeholder: Optional[str]

    # grid
    grid_columns: Optional[int]  # defualt 3 if grid
    grid_item_border: Optional[bool]
    grid_item_align: Optional[str]

    # table...


class Listing(
    FieldsListing, TraitYmlHasRepr, TraitYmlHasQuoteMap
):

    @classmethod
    def yml_quote_map(cls):
        return dict(
            type=False,
            fields=False,
            image_align=False,
            grid_item_align=False,
        )


class FieldsListingPage(NamedTuple):
    title: str
    listing: Listing


class ListingPage(
    FieldsListingPage,
    TraitYmlHasRepr,
    # TraitYmlHasQuoteMap
):
    pass


# ------------------------------------
