from __future__ import annotations

from typing import NamedTuple, Generic, TypeVar, Optional, Callable, Any, overload

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

CH = TypeVar("CH", bound = "Chain")

T = TypeVar("T")
P = TypeVar("P")
C = TypeVar("C")

GP2 = TypeVar("GP2")
GP = TypeVar("GP")
GC = TypeVar("GC")

class Chain(NamedTuple, Generic[P, C]):

    parent: P
    child: C

    prev: Optional[Chain]

    @classmethod
    def new(cls, child: C):
        return cls(None, child, None)

    @overload
    def done(self) -> C: ...
    
    @overload
    def done(self, f: Callable[[C], T]) -> T:...

    def done(self, f: Optional[Callable[[C], T]]=None):
        assert self.prev is None, self
        assert self.parent is None, self
        res = self.child
        if f is None:
            return res
        return f(res)

    @overload
    def close(
        self,
        f: Callable[[P, C], P], 
        p: Callable[[GP], GP],
        *args, 
        **kwargs
    ) -> Chain[GP, P]: ...

    @overload
    def close(
        self,
        f: Callable[[P, C], P], 
        p=None,
        *args, 
        **kwargs
    ) -> Chain[None, P]: ...

    def close(
        self,
        f: Callable[[P, C], P], 
        p: Optional[Callable[[GP], GP]]=None,
        *args, 
        **kwargs
    ) -> Chain[GP, P]:
        c = f(self.parent, self.child, *args, **kwargs)
        assert self.prev.parent is None, self.prev
        if p is not None:
            par = p(self.prev.parent)
            return self.prev._replace(
                parent=par, child=c
            )
        return self.prev._replace(child=c)

    def with_next(
        self, f: Callable[..., GC], *args, **kwargs
    ):
        """
        new child calling f with args, kwargs
        """
        gc = f(self.child, *args, **kwargs)
        return Chain(
            self.child, gc, self,
        )

    @overload
    def into(
        self, f: Callable[..., Callable[[C], GC]], *args, **kwargs
    ) -> Chain[C, GC]: ...
    # paramspec

    @overload
    def into(
        self, f: Callable[..., GC], *args, **kwargs
    ) -> Chain[C, GC]: ...

    def into(
        self, f: Callable[[C], GC], *args, **kwargs
    ):
        """
        new child calling f with child, args, kwargs
        """
        gc = f(*args, **kwargs)
        if isinstance(gc, Callable):
            gc = gc(self.child)
        return Chain(
            self.child, gc, self,
        )

    def call(
        self, k, *args, **kwargs
    ):
        f = getattr(self.child, k)
        c = f(*args, **kwargs)
        return self._replace(child=c)

    def pipe(
        self, f: Callable[[C], C], *args, **kwargs
    ):
        c = f(self.child, *args, **kwargs)
        return self._replace(child=c)

# ------------------------------------
