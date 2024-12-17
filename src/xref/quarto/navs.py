from __future__ import annotations

import enum
from typing import NamedTuple, Optional, Union, TYPE_CHECKING

from ..utils import *

from .core import *
from .qmd import *

# ------------------------------------


class EnumNavColor(enum.StrEnum):
    primary = enum.auto()
    secondary = enum.auto()
    success = enum.auto()
    danger = enum.auto()
    warning = enum.auto()
    info = enum.auto()
    light = enum.auto()
    dark = enum.auto()


class FieldsNavColors(NamedTuple):
    background: Optional[EnumNavColor]
    background_hex: Optional[str]
    # Background color (“primary”, “secondary”, “success”, “danger”, “warning”, “info”, “light”, “dark”, or hex color).
    foreground: Optional[EnumNavColor]
    foreground_hex: Optional[str]
    # Foreground color (“primary”, “secondary”, “success”, “danger”, “warning”, “info”, “light”, “dark”, or hex color). The foreground color will be used to color navigation elements, text and links that appear in the navbar.


class NavColors(
    FieldsNavColors,
    TraitYmlHasRepr,
    TraitYmlHasFieldMap,
    TraitYmlHasQuoteMap,
    TraitYmlMergeParent,
):
    @classmethod
    def yml_quote_map(cls):
        return dict(
            background=False,
            foreground=False,
            # TODO: hex tbc
            # (quote before rename)
        )

    @classmethod
    def yml_field_map(cls):
        return dict(
            background_hex="background",
            foreground_hex="foreground",
        )


# ------------------------------------


class FieldsNavLogo(NamedTuple):
    logo: Optional[str]
    # Logo image to be displayed left of the title.
    logo_alt: Optional[str]
    # Alternate text for the logo image.
    logo_href: Optional[str]
    # Target href from navbar logo / title. By default, the logo and title link to the root page of the site (/index.html).


class NavLogo(
    FieldsNavLogo,
    TraitYmlHasRepr,
    TraitYmlMergeParent,
):
    pass


# ------------------------------------


class FieldsNavMenuItem(NamedTuple):
    text: Optional[str]
    href: Optional[str]


class NavMenuItem(
    FieldsNavMenuItem,
    TraitYmlHasRepr,
):
    pass


# ------------------------------------


class FieldsNavTool(NamedTuple):
    icon: Optional[str]
    href: Optional[str]
    menu: Optional[list[NavMenuItem]]


class NavTool(
    FieldsNavTool,
    TraitYmlHasRepr,
):
    pass


# ------------------------------------


#   - text: "---"
# for use as separator in sidenav
class FieldsNavItem(NamedTuple):
    section: Optional[str]
    # indicates is a section break

    href: Optional[str]
    # Link to file contained with the project or external URL.
    text: Optional[str]
    # Text to display for navigation item (defaults to the document title if not provided).
    icon: Optional[str]
    # Name of one of the standard Bootstrap 5 icons (e.g. “github”, “twitter”, “share”, etc.).
    aria_label: Optional[str]
    # Accessible label for the navigation item.
    rel: Optional[str]
    # Value for rel attribute. Multiple space-separated values are permitted.
    menu: Optional[list[NavItem]]
    # List of navigation items to populate a drop-down menu

    contents: Optional[list[NavItem]]


class NavItem(
    FieldsNavItem,
    TraitYmlHasRepr,
):
    pass


# ------------------------------------


class FieldsNavTop(NamedTuple):
    title: Optional[Union[bool, str]]
    # Navbar title (uses the site: title if none is specified). Use title: false to suppress the display of the title on the navbar.
    logo: Optional[NavLogo]
    color: Optional[NavColors]
    search: bool
    # Include a search box (true or false).
    tools: list[NavTool]
    # List of navbar tools (e.g. link to github or twitter, etc.). See Navbar Tools for details.
    left: Optional[list[NavItem]]  # or href str
    right: Optional[list[NavItem]]
    # Lists of navigation items for left and right side of navbar.
    pinned: bool
    # Always show the navbar (true or false). Defaults to false, and uses headroom.js to automatically show the navbar when the user scrolls up on the page.
    collapse: bool
    # Collapse the navbar items into a hamburger menu when the display gets narrow (defaults to true).
    collapse_below: str
    # Responsive breakpoint at which to collapse navbar items to a hamburger menu (“sm”, “md”, “lg”, “xl”, or “xxl”, defaults to “lg”).
    toggle_position: str
    # The position of the collapsed navbar hamburger menu when in responsive mode (“left” or “right”, defaults to “left”).


class NavTop(FieldsNavTop, TraitYmlHasRepr):
    pass


# ------------------------------------


class FieldsNavSide(NamedTuple):
    id: Optional[str]
    # Optional identifier (used only for hybrid navigation, described below).
    title: Optional[str]
    # Sidebar title (uses the project title if none is specified).
    subtitle: Optional[str]
    # Optional subtitle.
    logo: Optional[str]
    # Optional logo image.
    search: bool
    # Include a search box (true or false). Note that if there is already a search box on the top navigation bar it won’t be displayed on the sidebar.
    tools: list[NavTool]
    # List of sidebar tools (e.g. link to github or twitter, etc.). See the next section for details.
    contents: list[NavItem]
    # List of navigation items to display (typically top level items will in turn have a list of sub-items).
    style: str
    # “docked” or “floating”.
    type: str
    # “dark” or “light” (hint to make sure the text color is the inverse of the background).
    colors: NavColors
    border: bool
    # Whether to show a border on the sidebar. “true” or “false”.
    alignment: str
    # Alignment (“left”, “right”, or “center”).
    collapse_level: int
    # Whether to show sidebar navigation collapsed by default. The default is 2, which shows the top and next level fully expanded (but leaves the 3rd and subsequent levels collapsed).
    pinned: bool
    # Always show a title bar that expands to show the sidebar at narrower screen widths (true or false). Defaults to false, and uses headroom.js to automatically show the navigation bar when the user scrolls up on the page.


class NavSide(
    FieldsNavSide,
    TraitYmlHasRepr,
    TraitYmlHasFieldMap,
):

    @classmethod
    def yml_field_map(cls):
        return dict(
            background_hex="background",
            foreground_hex="foreground",
        )


# ------------------------------------


# A single sidebar item without an id or title will result in a global sidebar applied to all pages. A sidebar with an id or title will only be applied to pages within the contents of the sidebar or pages that specify the sidebar id.
class FieldsNav(NamedTuple):
    top: NavTop
    # navbar
    side: list[NavSide]
    # sidebar


class Nav(
    FieldsNav,
    TraitYmlHasRepr,
    TraitYmlHasFieldMap,
):
    r"""
    >>> nav = (
    ...     Nav.new()
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
    >>> _ = list(map(print, write_yaml(nav).split("\n")))
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
          - href:
            text: "new"
      - def.qmd
      - href: b
        text: ""
    """
    @classmethod
    def cls(cls, self: Nav):
        return self

    @classmethod
    def yml_field_map(cls):
        return dict(
            top="navbar",
            side="sidebar",
        )

# ------------------------------------

if TYPE_CHECKING:
    nav = (
        fTree.new(Nav.new())
        .fork(NavTop.new)
        .call("set", title="top")
        .merge(lambda nav, top: nav.set(top=top))
        .done()
    )

# ------------------------------------

# example hybrid:

# To do this, provide a group of sidebar entries and link each group of sidebar entries with a navbar entry by matching their titles and listing the page linked from the navbar as the first content in the sidebar group

# A page that doesn’t appear in any sidebar will inherit and display the first sidebar without an id or title - you can prevent the sidebar from showing on a page by setting sidebar: false in it’s front matter.

# website:
#   title: ProjectX
#   navbar:
#     background: primary
#     search: true
#     left:
#       - text: "Home"
#         file: index.qmd
#       - text: "Tutorials"
#         file: tutorials.qmd
#       - text: "How-To"
#         file: howto.qmd
#       - text: "Fundamentals"
#         file: fundamentals.qmd
#       - text: "Reference"
#         file: reference.qmd

#   sidebar:
#     - title: "Tutorials"
#       style: "docked"
#       background: light
#       contents:
#         - tutorials.qmd
#         - tutorial-1.qmd
#         - tutorial-2.qmd

#     - title: "How-To"
#       contents:
#         - howto.qmd
#         # navigation items

#     - title: "Fundamentals"
#       contents:
#         - fundamentals.qmd
#         # navigation items

#     - title: "Reference"
#       contents:
#         - reference.qmd
#         # navigation items


# Note that the first sidebar definition contains a few options (e.g. style and background). These options are automatically inherited by the other sidebars.

# ------------------------------------
