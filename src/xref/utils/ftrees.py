from __future__ import annotations

from typing import (
    NamedTuple,
    Generic,
    TypeVar,
    Optional,
    Callable,
    Iterable,
    overload,
)


def map_print(v: Iterable):
    list(map(print, v))


# ------------------------------------

CH = TypeVar("CH", bound="fTree")

T = TypeVar("T")
P = TypeVar("P")
C = TypeVar("C")

GP2 = TypeVar("GP2")
GP = TypeVar("GP")
GC = TypeVar("GC")


class fTree(NamedTuple, Generic[P, C]):

    parent: P
    child: C

    prev: Optional[fTree]

    @classmethod
    def new(cls, child: C):
        return cls(None, child, None)

    @overload
    def done(self) -> C: ...

    @overload
    def done(self, f: Callable[[C], T]) -> T: ...

    def done(self, f: Optional[Callable[[C], T]] = None):
        assert self.prev is None, self
        assert self.parent is None, self
        res = self.child
        if f is None:
            return res
        return f(res)

    @overload
    def merge(
        self,
        f: Callable[[P, C], P],
        p: Callable[[GP], GP],
        *args,
        **kwargs,
    ) -> fTree[GP, P]: ...

    @overload
    def merge(
        self,
        f: Callable[[P, C], P],
        p=None,
        *args,
        **kwargs,
    ) -> fTree[None, P]: ...

    def merge(
        self,
        f: Callable[[P, C], P],
        p: Optional[Callable[[GP], GP]] = None,
        *args,
        **kwargs,
    ) -> fTree[GP, P]:
        c = f(self.parent, self.child, *args, **kwargs)
        assert self.prev.parent is None, self.prev
        if p is not None:
            par = p(self.prev.parent)
            return self.prev._replace(parent=par, child=c)
        return self.prev._replace(child=c)

    @overload
    def fork(
        self,
        f: Callable[..., Callable[[C], GC]],
        *args,
        **kwargs,
    ) -> fTree[C, GC]: ...

    # paramspec

    @overload
    def fork(
        self, f: Callable[..., GC], *args, **kwargs
    ) -> fTree[C, GC]: ...

    def fork(self, f: Callable[[C], GC], *args, **kwargs):
        """
        new child calling f with child, args, kwargs
        """
        gc = f(*args, **kwargs)
        if isinstance(gc, Callable):
            gc = gc(self.child)
        return fTree(
            self.child,
            gc,
            self,
        )

    def call(self, k, *args, **kwargs):
        f = getattr(self.child, k)
        c = f(*args, **kwargs)
        return self._replace(child=c)

    def pipe(self, f: Callable[[C], C], *args, **kwargs):
        c = f(self.child, *args, **kwargs)
        return self._replace(child=c)


# ------------------------------------
