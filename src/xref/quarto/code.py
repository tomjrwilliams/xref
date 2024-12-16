from __future__ import annotations

from typing import Optional

import functools
import itertools
import time
import dataclasses

import datetime

import functools

import abc
import collections.abc
import typing
import csv

import hashlib

import sys

import functools

import tempfile
import pathlib

import contextlib
import typing
import json

import dataclasses

import distutils.dir_util
import hashlib

import subprocess

import hashlib

# -------------------------------------------------------------------

# code


def indent(code: str, n=1):
    return "\n".join(
        [("    " * n) + l for l in code.split("\n")]
    )


def print_error(
    filter_ends_with: list[str] = [],
    filter_starts_with: list[str] = [],
):
    filts = [
        f"""not l.strip().startswith('{s}')"""
        for s in filter_starts_with
    ] + [
        f"""not l.strip().startswith('{s}')"""
        for s in filter_ends_with
    ]
    return indent(
        "\n".join(
            [
                "if error:",
                """    ls = tb.split("\\n")""",
                """    ls = [""",
                """        l for l in ls""",
                """        if not any([""",
            ]
            + filts
            + [
                """        ])""",
                """    ]""",
                """    assert False, "\\n".join(ls)""",
            ]
        )
    )


def catch_error(
    code: str, print: bool = True, **print_kwargs
):
    return indent(
        "\n".join(
            [
                "error = False",
                "tb = ''",
                "try:",
            ]
            + [indent(code)]
            + [
                "except Exception:",
                "    sys.stdout.flush()",
                "    sys.stderr.flush()",
                "    error = True",
                "    tb = traceback.format_exc()",
            ]
        )
    ) + ("" if not print else print_error(**print_kwargs))


def code_block(
    code, catch=True, print=True, **print_kwargs
):
    return "\n".join(
        [
            "```{" + "python}",
            # "#| error: true",
            "#| warning: false",
            "#| fig-align: center",
            "#| layout-align: center",
            (
                code
                if catch is False
                else catch_error(
                    code, print=print, **print_kwargs
                )
            ),
            "```",
        ]
    )
