from __future__ import annotations

from typing import NamedTuple

# ------------------------------------


class TraitQuarto(NamedTuple):

    @classmethod
    def new(cls, **kws):
        fields = cls._fields
        defaults = cls._field_defaults
        if not all(k in fields for k in kws.keys()):
            raise ValueError("Invalid:", cls, kws)
        return cls(
            **{
                k: kws.get(k, defaults.get(k, None))
                for k in fields
            }
        )

    def set(self, **kws):
        return self._replace(**kws)


# ------------------------------------
