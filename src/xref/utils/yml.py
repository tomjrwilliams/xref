import enum
from typing import NamedTuple, Optional, Any, Union
from functools import partial

import yaml

from .nts import NamedTupleBase

# ------------------------------------


class TraitYml(NamedTupleBase):
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


class Quoted(str):
    pass


def quoted_presenter(dumper: yaml.Dumper, data):
    return dumper.represent_scalar(
        "tag:yaml.org,2002:str", data, style='"'
    )


yaml.add_representer(Quoted, quoted_presenter)


def yml_quote(s: str | enum.StrEnum):
    if isinstance(s, enum.StrEnum):
        s = s.value
    return Quoted(s)


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


def rec_to_yaml_dict(
    obj: Union[
        None,
        int,
        bool,
        str,
        TraitYmlHasRepr,
        list,
    ],
):
    if isinstance(obj, list):
        return [rec_to_yaml_dict(v) for v in obj]
    elif isinstance(obj, TraitYmlHasRepr):
        fields = obj._fields
        field_map: dict[str, str] = {}
        if isinstance(obj, TraitYmlHasFieldMap):
            field_map = obj.yml_field_map()
        quote_map: dict[str, bool] = {}
        if isinstance(obj, TraitYmlHasQuoteMap):
            quote_map = obj.yml_quote_map()
        keep_nulls = isinstance(obj, TraitYmlKeepNullFields)
        res = {}
        for k in fields:
            v = getattr(obj, k)
            quote = yml_should_quote(k, v, quote_map)
            if v is None and not keep_nulls:
                continue
            elif isinstance(v, list):
                v = [rec_to_yaml_dict(vv) for vv in v]
            elif isinstance(v, TraitYmlMergeParent):
                res = {**res, **rec_to_yaml_dict(v)}
            elif isinstance(v, TraitYmlHasRepr):
                v = rec_to_yaml_dict(v)
            elif isinstance(v, str) and quote:
                v = yml_quote(v)
            else:
                assert isinstance(v, (bool, int, str))
            res[field_map.get(k, k).replace("_", "-")] = v
        return res
    else:
        assert isinstance(obj, (bool, int, str))
    return obj


def write_yaml(obj: TraitYml, **kwargs):
    d: dict = rec_to_yaml_dict(obj)
    return yaml.dump(
        d,
        default_flow_style=kwargs.get(
            "default_flow_style", False
        ),
        sort_keys=kwargs.get("sort_keys", False),
    ).strip()


# ------------------------------------
