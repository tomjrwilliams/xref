from __future__ import annotations

import pprint

import datetime
import pathlib

import io

from typing import (
    Type,
    Any,
    Optional,
    Union,
)

import yaml
import attrs

from . import utils
from . import fields
from . import nodes
from . import pages

import xtuples

# -----------------------------------------------


def _example_site():
    p = pages.Paper.new(
        "Example", datetime.date(2024, 1, 1)
    ).add(nodes.summary("a b c").term("a"))
    s = Site.new("Example").add(p)
    return s


def init_site(ps):
    acc: dict[Type[pages.Page] : dict[Any, pages.Page]] = {
        pages.Post: {},
        pages.Paper: {},
        pages.Brief: {},
        pages.Term: {},
        pages.Topic: {},
        pages.Person: {},
        pages.Organisation: {},
    }
    for p in ps:
        for t in [pages.Post, pages.Paper, pages.Brief]:
            if isinstance(p, t):
                acc[t][p.title] = p
    return acc


def drop_dp(dp, fp):
    if isinstance(fp, (str, pathlib.Path)):
        res = pathlib.Path(str(fp).replace(str(dp), "."))
        return str(res)
    return [drop_dp(dp, _fp) for _fp in fp]


@attrs.define(frozen=True)
class Site:

    title: str = fields.typed_field()
    pages: xtuples.iTuple[pages.Page] = fields.typed_field()

    def add(self, page: pages.Page):
        return attrs.evolve(
            self, pages=self.pages.append(page)
        )

    @classmethod
    def new(cls, title, pages=xtuples.iTuple()):
        return cls(title, pages)

    # TODO: all index pages (startup,t erm, topci) with a page get a category?

    # TODO: need a way to flag out terms eg. as not being worthy of their own page?
    # ie. set to profile=false

    # TODO: ah, so both that, adn a flag for if they have a category (else default to profile)

    # TODO: to exteact the content, also pass a list of flattened page contents
    # with the pages
    # because can then find the id in the list, and then extract content from nodes within a certain number of indices
    # flatten will be in the order of .to_qmd calls

    # --

    def generate_pages(self):
        # """
        # >>> s = _example_site()
        # >>> acc = s.generate_pages()
        # >>> for t, t_acc in acc.items():
        # ...     print(t)
        # ...     for k, v in t_acc.items():
        # ...         print(k, ":", v)
        # <class 'xref.core.pages.Term'>
        # a : Term(children=iTuple(), target='a', occurences=iTuple(), active=True)
        # """
        acc = init_site(self.pages)
        for page in self.pages:
            acc = page.generate_pages(acc)
        return {
            t: k_ps for t, k_ps in acc.items() if len(k_ps)
        }

    def accumulate_content(self, acc=None):
        # """
        # >>> s = _example_site()
        # >>> acc = s.accumulate_content()
        # >>> for t, t_acc in acc.items():
        # ...     print(t)
        # ...     for k, v in t_acc.items():
        # ...         print(k, ":", v)
        # <class 'xref.core.pages.Term'>
        # a : Term(children=iTuple(), target='a', occurences=iTuple(5), active=True)
        # """
        if acc is None:
            acc = self.generate_pages()
        for page in self.pages:
            acc = page.accumulate_content(acc)
        return {
            t: k_ps for t, k_ps in acc.items() if len(k_ps)
        }

    # --

    def create_pages(self, dp, acc=None):

        res = {}

        if acc is None:
            acc = self.accumulate_content()

        dp = pathlib.Path(dp)
        dp.mkdir(exist_ok=True, parents=True)

        for t, k_ps in acc.items():

            res[t] = {}

            if not t.nav_folder():
                continue

            t_dp = dp / t.nav_folder()
            t_dp.mkdir(exist_ok=True, parents=True)

            for k, p in k_ps.items():

                handle = p.get_string_like("handle")
                if handle is None:
                    handle = p.get_string_like(
                        "title"
                    ).replace(" ", "_")

                fp = t_dp / f"{handle}.qmd"

                qmd = p.to_qmd()

                with fp.open("w+") as f:
                    f.write(qmd)

                res[t][fp] = p

        return res

    def write_roots(self, dp, res):
        dp = pathlib.Path(dp)

        roots = {}

        for t, fp_ps in res.items():

            if not t.nav_folder():
                continue

            t_dp = dp / t.nav_folder()
            t_dp.mkdir(exist_ok=True, parents=True)

            root_fp = t_dp / "index.qmd"

            with root_fp.open("w+") as f:
                f.write(t.index_qmd(fp_ps))

            roots[t] = root_fp

        return roots

    def write_index(self, dp, res):
        dp = pathlib.Path(dp)

        index_fp = dp / "index.qmd"

        yml = dict(
            title="Home",
            listing=dict(
                contents=drop_dp(
                    dp,
                    sum(
                        (
                            [fp for fp in res[t].keys()]
                            for t in [
                                pages.Post,
                                pages.Paper,
                                pages.Brief,
                            ]
                            if t in res
                        ),
                        [],
                    ),
                )
            ),
        )
        s = utils.qmd_header(yml)
        with index_fp.open("w+") as f:
            f.write(s)
        return index_fp

    def write_yaml(
        self,
        dp,
        res,
        roots,
        index_fp,
    ):
        dp = pathlib.Path(dp)

        sidebar = {
            "style": "floating",
            "search": True,
            "collapse-level": 1,
        }
        side_contents = []

        for t, fp_ps in res.items():

            root_fp = roots[t]

            side_contents.append(
                dict(
                    section=t.nav_title(),
                    # style="docked",
                    # background="light",
                    contents=drop_dp(
                        dp,
                        [
                            # root_fp
                        ]
                        + list(fp_ps.keys()),
                    ),
                    # TODO: relative paths?
                )
            )

        sidebar["contents"] = side_contents

        navbar = {
            "background": "primary",
            "search": True,
            "right": [
                dict(
                    text="Home",
                    file=drop_dp(dp, index_fp),
                )
            ]
            + [
                dict(
                    text=t.nav_title(),
                    file=drop_dp(dp, roots[t]),
                )
                for t, fp_ps in res.items()
            ],
        }

        yml = {
            "project": {
                "type": "website",
            },
            "format": {
                "html": {"theme": "flatly"},
            },
            "website": {
                "title": self.title,
                "navbar": navbar,
                "sidebar": sidebar,
            },
        }

        fp = dp / "_quarto.yml"

        with fp.open("w+") as f:
            yaml.dump(yml, f, default_flow_style=False)

        return fp

    def write_qmd(self, dp, acc=None):
        """
        >>> s = _example_site()
        >>> s.write_qmd("./example")
        """

        if acc is None:
            acc = self.accumulate_content()

        res = self.create_pages(dp, acc=acc)
        roots = self.write_roots(dp, res)
        index_fp = self.write_index(dp, res)

        yaml_fp = self.write_yaml(
            dp,
            res,
            roots,
            index_fp,
        )

        return

    # --

    def merge_static(self, dp, *static_dps):
        # merge in the constants - eg. about page
        # eg. just merge in a given directory of static content
        return

    # --

    def render_site(self):
        # call render on the directory
        return

    # --


# -----------------------------------------------
