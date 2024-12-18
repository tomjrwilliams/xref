from __future__ import annotations

from typing import (
    NamedTuple,
    TYPE_CHECKING,
)

from ..utils import *

from .core import *

from .yml import *
from .navs import *

# ------------------------------------


class FieldsSite(NamedTuple):
    title: str
    top: NavTop
    side: list[NavSide]
    footer: Footer

    # TODO: social, comments
    # search


class Site(
    FieldsSite,
    TraitYmlHasRepr,
    TraitYmlHasFieldMap,
):
    r"""
    >>> site = (
    ...     Site.new(title="tbc")
    ...     .set(top=NavTop.new(
    ...         title="top",
    ...         tools=[
    ...             NavTool.new(href="tool.qmd"),
    ...             "test.qmd",
    ...             NavItem.new(
    ...                 href="text.qmd",
    ...                 text="Test"
    ...             ),
    ...         ],
    ...         left = [
    ...             "test.qmd",
    ...             NavItem.new(
    ...                 href="text.qmd",
    ...                 text="Test",
    ...                 contents=["abc.qmd", NavItem.new(text="new", href="")]
    ...             ),
    ...             "def.qmd",
    ...             NavItem.new(href="b", text="")
    ...         ]
    ...     ))
    ... )
    >>> map_print(write_yaml(site).split("\n"))
    title: "tbc"
    navbar:
      title: "top"
      tools:
      - href: tool.qmd
      - test.qmd
      - href: text.qmd
        text: "Test"
      left:
      - test.qmd
      - href: text.qmd
        text: "Test"
        contents:
        - abc.qmd
        - href: ''
          text: "new"
      - def.qmd
      - href: b
        text: ""
    """

    # @classmethod
    # def cls(cls, self: Site):
    #     return self

    @classmethod
    def yml_field_map(cls):
        return dict(
            top="navbar",
            side="sidebar",
            footer="page-footer",
        )


# ------------------------------------


class FieldsFooter(NamedTuple):
    left: Optional[str | NavMenuItem]
    right: Optional[str | NavMenuItem]
    center: Optional[str | NavMenuItem]


class Footer(
    FieldsFooter,
    TraitYmlHasRepr,
):
    pass


#   page-footer:
#     left: "Copyright 2021, Norah Jones"
#     right:
#       - icon: github
#         href: https://github.com/
#       - icon: twitter
#         href: https://twitter.com/

# ------------------------------------

# theme: cosmo
# css: styles.css
# toc: true


class FieldsFormatting(NamedTuple):
    theme: str
    css: str
    toc: bool


class Formatting(
    FieldsFormatting,
    TraitYmlHasRepr,
    TraitYmlHasFieldMap,
):
    pass


# ------------------------------------


class FieldsProject(NamedTuple):
    type: str
    site: Site
    format: Formatting

    @classmethod
    def yml_field_map(cls):
        return dict(site="website")

    top: NavTop
    # navbar
    side: list[NavSide]
    # sidebar

    footer: Footer


class Project(
    FieldsProject,
    TraitYmlHasRepr,
    TraitYmlHasFieldMap,
):
    pass


# ------------------------------------

# -> _quarto.yml

# ------------------------------------

if TYPE_CHECKING:
    nav = (
        fTree.new(Site.new())
        .fork(NavTop.new)
        .call("set", title="top")
        .merge(lambda site, top: site.set(top=top))
        .done()
    )

# ------------------------------------
