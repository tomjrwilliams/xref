
from attrs import field
from attrs_strict import type_validator

def typed_field(
    *args,
    validator = type_validator(), #
    **kwargs
):
    return field(
        *args,
        validator=validator,
        **kwargs
    )

def optional_field(
    *args,
    default=None,
    validator = type_validator(), #
    **kwargs
):
    if "factory" not in kwargs:
        kwargs["default"] = default
    return field(
        *args,
        validator=validator,
        **kwargs
    )