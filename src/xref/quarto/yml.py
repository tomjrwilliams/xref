import enum
from typing import NamedTuple, Optional, Any
from functools import partial

from .core import *

# ------------------------------------


class TraitYml(TraitQuarto):
    pass


class TraitYmlHasRepr(TraitYml):
    pass


class TraitYmlMergeParent(TraitYml):
    pass


class TraitYmlKeepNullFields(TraitYml):
    pass


class TraitYmlHasFieldMap(TraitYml):

    @classmethod
    def yml_field_map(cls):
        raise ValueError(cls)


class TraitYmlHasQuoteMap(TraitYml):
    # default to yes unless href or id

    @classmethod
    def yml_quote_map(cls):
        raise ValueError(cls)


# ------------------------------------


class YmlLine(NamedTuple):
    indent: int
    is_list: bool
    key: Optional[str]
    value: Optional[str]


NULL = "null"

# ------------------------------------


def yml_quote(s: str | enum.StrEnum):
    if isinstance(s, enum.StrEnum):
        s = s.value
    return f'"{s}"'


def yml_should_quote(
    k: str,
    v: Any | str | enum.StrEnum,
    quote_map: dict[str, bool],
):
    if not isinstance(v, str):
        return False
    if k == "id":
        return False
    elif "href" in k:
        return False
    elif isinstance(v, enum.StrEnum):
        return quote_map.get(k, False)
    else:
        return quote_map.get(k, True)


# ------------------------------------


def gen_yaml_lines(
    obj: TraitYml,
    indent: int = -1,
    ix: Optional[int] = None,
):
    # what a cluster fuck
    if not isinstance(obj, TraitYmlHasRepr):
        raise ValueError(obj)
    field_map: dict[str, str] = {}
    if isinstance(obj, TraitYmlHasFieldMap):
        field_map = obj.yml_field_map()
    quote_map: dict[str, bool] = {}
    if isinstance(obj, TraitYmlHasQuoteMap):
        quote_map = obj.yml_quote_map()
    keep_nulls = isinstance(obj, TraitYmlKeepNullFields)
    if not isinstance(obj, TraitYmlMergeParent):
        indent += 1
    ks = obj._fields
    is_lists = [
        isinstance(getattr(obj, k), list) for k in ks
    ]
    k_ixs = sum(
        [
            (
                [(k, None)]
                if not is_list
                else [
                    (k, i)
                    for i in range(len(getattr(obj, k)))
                ]
            )
            for k, is_list in zip(ks, is_lists)
        ],
        [],
    )
    n_null = 0
    for k, k_ix in k_ixs:
        v = getattr(obj, k)
        quote = yml_should_quote(k, v, quote_map)
        k = field_map.get(k, k)

        # ix = child of list node
        # k_ix = list field

        if k_ix is not None:
            v = v[k_ix]

        if v is None:
            if not keep_nulls:
                continue
            v = NULL

        k_list = isinstance(k_ix, int)
        p_list = isinstance(ix, int) and n_null == 0

        if k_ix == 0:
            # in theory cant be none as was list
            yield YmlLine(
                indent
                + (isinstance(ix, int) and not p_list),
                p_list,
                key=k,
                value=None,
            )
        elif isinstance(k_ix, int):
            k = None

        if isinstance(v, TraitYmlHasRepr):
            yield from gen_yaml_lines(
                v,
                indent=indent
                + (isinstance(ix, int) and not p_list),
                ix=k_ix,
            )
            n_null += 1
            continue

        if isinstance(v, str) and quote:
            v = yml_quote(v)
        elif not isinstance(v, str):
            v = str(v).lower()

        yield YmlLine(
            indent
            + (
                isinstance(k_ix, int)
                + (isinstance(ix, int) and not p_list)
            ),
            p_list or k_list,
            key=None if k_list else k,
            value=v,
        )
        n_null += 1

    return


def write_yaml_line(pad: str, yl: YmlLine):
    return (
        (pad * yl.indent)
        + (
            ""
            if not yl.is_list
            else ((len(pad) - 2) * pad[0]) + ("- ")
        )
        + ("" if not yl.key else f"{yl.key}: ")
        + ("" if not yl.value else yl.value)
    )


def write_yaml(
    obj: TraitYml,
    pad: str = "  ",
    indent: int = -1,
    ix: Optional[int] = None,
):
    return "\n".join(
        map(
            partial(write_yaml_line, pad),
            gen_yaml_lines(obj, indent=indent, ix=ix),
        )
    )


# ------------------------------------
