
from __future__ import annotations

from typing import (
    Any,
    Type,
    Optional,
    Union,
)

import attrs

from . import fields

import xtuples

# -----------------------------------------------

global ID
ID: int = 0

def id():
    global ID 
    res = ID
    ID += 1
    return res

# -----------------------------------------------

@attrs.define(frozen=True)
class Node:
    """
    >>> n = Node(id(), xtuples.iTuple())
    >>> n
    Node(children=iTuple())
    >>> Node.new().id > n.id
    True
    """

    id: int = fields.typed_field(repr=False)
    children: xtuples.iTuple[Node] = fields.typed_field()

    def generate_pages(
        self, acc: dict[
            Type[Page]: dict[Any, Page]
        ]
    ):
        acc = {
            t: t.accumulate_node(self, t_acc)
            for t, t_acc in acc.items()
        }

        for child in self.children:
            acc = child.generate_pages(acc)
        
        return acc

    @classmethod
    def new(cls, *args, children = xtuples.iTuple(), **kwargs):
        return cls(id(), children, *args, **kwargs)

    # --

    def allowed_children(self):
        return []

    def add(self, child: Node):
        assert type(child) in self.allowed_children(), dict(
            self=self, allowed=self.allowed_children(), child=child,
        )
        return attrs.evolve(
            self,
            children = self.children.append(child)
        )

    # -- 

    # def person(self):
    #     return self.add(Person.new())

    def academic(self, *args, **kwargs):
        return self.add(Academic.new())

    def founder(self, *args, **kwargs):
        return self.add(Founder.new(*args, **kwargs))

    def investor(self, *args, **kwargs):
        return self.add(Investor.new(*args, **kwargs))

    # --

    # def organisation(self):
    #     return self.add(Organisation.new())

    def corporate(self, *args, **kwargs):
        return self.add(Corporate.new(*args, **kwargs))

    def startup(self, *args, **kwargs):
        return self.add(Startup.new(*args, **kwargs))

    def university(self, *args, **kwargs):
        return self.add(University.new(*args, **kwargs))

    def fund(self, *args, **kwargs):
        return self.add(Fund.new(*args, **kwargs))

    # --

    def section(self, *args, **kwargs):
        return self.add(Section.new(*args, **kwargs))

    # --

    def term(self, *args, **kwargs):
        return self.add(Term.new(*args, **kwargs))
        
    def topic(self, *args, **kwargs):
        return self.add(Topic.new(*args, **kwargs))

    def category(self, *args, **kwargs):
        return self.add(Category.new(*args, **kwargs))

    # --

    def citation(self, *args, **kwargs):
        return self.add(Citation.new(*args, **kwargs))

    def reference(self, *args, **kwargs):
        return self.add(Reference.new(*args, **kwargs))

    # --

    # def text(self, *args, **kwargs):
    #     return self.add(Text.new(*args, **kwargs))

    def quote(self, *args, **kwargs):
        """
        >>> Section.new("a").quote("a")
        Section(children=iTuple(Quote(children=iTuple(), text='a')), title='a')
        """
        return self.add(Quote.new(*args, **kwargs))

    def summary(self, *args, **kwargs):
        return self.add(Summary.new(*args, **kwargs))

    def question(self, *args, **kwargs):
        return self.add(Question.new(*args, **kwargs))

    def answer(self, *args, **kwargs):
        return self.add(Answer.new(*args, **kwargs))

    def definition(self, *args, **kwargs):
        return self.add(Definition.new(*args, **kwargs))

    def explanation(self, *args, **kwargs):
        return self.add(Explanation.new(*args, **kwargs))

    def example(self, *args, **kwargs):
        return self.add(Example.new(*args, **kwargs))

    def transition(self, *args, **kwargs):
        return self.add(Transition.new(*args, **kwargs))

    def comment(self, *args, **kwargs):
        return self.add(Comment.new(*args, **kwargs))

    # --

    def code(self, *args, **kwargs):
        return self.add(Code.new(*args, **kwargs))

    # --


# -----------------------------------------------

@attrs.define(frozen=True)
class Page(Node):
    active: bool = fields.typed_field()

    def accumulate_node(
        self, node: Node, acc: dict[Any, Page]
    ):
        raise NotImplementedError()

# -----------------------------------------------

# these eventually have their own page
# field for eg. job title / history, education, name

# and then we build up links eg. to / from papers, company write ups


@attrs.define(frozen=True)
class Person(Node):
    pass


person = Person.new


@attrs.define(frozen=True)
class Academic(Person):
    pass


academic = Academic.new


@attrs.define(frozen=True)
class Founder(Person):
    pass


founder = Founder.new


@attrs.define(frozen=True)
class Investor(Person):
    pass


investor = Investor.new

# -----------------------------------------------


@attrs.define(frozen=True)
class Organisation(Node):
    pass


organisation = Organisation.new


@attrs.define(frozen=True)
class Corporate(Organisation):
    pass


corporate = Corporate.new


@attrs.define(frozen=True)
class Startup(Organisation):
    pass


startup = Startup.new


@attrs.define(frozen=True)
class University(Organisation):
    pass


university = University.new


@attrs.define(frozen=True)
class Fund(Organisation):
    pass


fund = Fund.new

# separate for academic, founder?

# separate for startup, corporate, university?


# -----------------------------------------------



@attrs.define(frozen=True)
class Section(Node):
    title: str = fields.typed_field()

    def allowed_children(self):
        return [
            Quote,
            #
        ]

section = Section.new


# -----------------------------------------------

# inline term in a text block is given a link to the entry in the glossary page (or relevant page if the glossary is split)
# ideally also hover over to see the definition (? otional flag to turn off for this doc: "... Term(x, hover=False) ..." etc.)
# eg. peptide
@attrs.define(frozen=True)
class Term(Node):
    pass


term = Term.new

# terms / articles / sectiosn can be tagged with topics
# topics can be used? presumably pull out the relevant sections (decide what level of depth to pull out)
# to build up a page of effectively static search results for that topic, that links to the location in the actual article

# eg. peptide
@attrs.define(frozen=True)
class Topic(Node):
    pass


topic = Topic.new


@attrs.define(frozen=True)
class Category(Node):
    pass


category = Category.new


# -----------------------------------------------

# follow the format you get provided for you
# don't have to be rendered to be added to page 
# for referencing, either there or elsewhere
@attrs.define(frozen=True)
class Citation(Node):
    pass


citation = Citation.new


# can eg. have the same as above, pull out the relevant nodes with the reference
# to build up again what's effectively a static search page of times that reference was used
@attrs.define(frozen=True)
class Reference(Node):
    pass


reference = Reference.new

# not sure about these for now?

# do need a citation mechanism but that's a second draft presuambly


# class Source(Node):
#     pass

# # take both external link etc.
# # reference node
# # and an internal link (to pdf / txt etc. - allow plural eg. for latex source vs output)
# class Paper(Source):
#     pass

# # sub type of paper?
# class Post(Source):
#     pass

# -----------------------------------------------

@attrs.define(frozen=True)
class Text(Node):
    text: str = fields.typed_field()

text = Text.new

# -----------------------------------------------

@attrs.define(frozen=True)
class Quote(Text):
    pass


quote = Quote.new

# eg. of a particular bit of a source
# a document as a whole
# depnending on what the source is, change the format
# eg. abstract for document as a whole
# versus a section of a document, can be a kind of inline quote, greyed out say at the top fo the section
# or Summary: italics (For section)

@attrs.define(frozen=True)
class Summary(Text):
    ref: Node = fields.typed_field()
    pass

summary = Summary.new

# the idea with questioons is that they essentially form sub headers
# where the answer is then likely a series of points

@attrs.define(frozen=True)
class Question(Text):
    pass


question = Question.new

# need to be able to make inline term references
# ideally without breaking flow, so literally as below
# ie. ".... Term(x) ..."

# direct response to question
# can break and continue over a term definition
# with additional explanation / examples that can be hidden on eg. compilation pages of questions
@attrs.define(frozen=True)
class Answer(Text):
    pass


answer = Answer.new


# so without breaking flow in an answer, so smaller (body size) font, versus the question being the header
# definition is indent formatted: Term: x
@attrs.define(frozen=True)
class Definition(Text):
    pass


definition = Definition.new

# eg. of definition? ie. explanations and examples attach to particular answers (Say)
# definitions, summaries
# ie. extra text that isn't strictly necessary but is helpful
@attrs.define(frozen=True)
class Explanation(Text):
    pass


explanation = Explanation.new

# examples being a particular kind of explanation
# eg. link to explanation / definition
@attrs.define(frozen=True)
class Example(Text):
    pass


example = Example.new


# for just joinign between sections, essentially text meta data, doesn't need to be pulled out, just makes the finished article flow
@attrs.define(frozen=True)
class Transition(Text):
    pass


transition = Transition.new


# not rendered?
@attrs.define(frozen=True)
class Comment(Text):
    pass


comment = Comment.new

# -----------------------------------------------

# code snippets
@attrs.define(frozen=True)
class Code(Node):
    pass

code = Code.new

# -----------------------------------------------

# all format tbc: figures are presumably just an image
# graphs likewise

# tables ideally inline?

# graphs want to disambiguate reproducing from data vs taking imge
# thats just a figure then? a graph in image form

# class Figure(Node):
#     pass

# class Table(Figure):
#     pass

# class Graph(Figure):
#     pass

# class Image(Figure):
#     pass

# -----------------------------------------------

# recursively unpack all nodes in the module
# optional (later) filtering predicates on the paths / nodes / module names
# including unpacking out of pages
# all are frozen so hashable

# can even then build a site out of pages
# where we can acc back into the page modules
# to get everything we need to build the site?

def index(module, acc = None):
    pass

# -----------------------------------------------


# data structures to hold

# paper

# quote / reference to a text snippet from a paper

# store the paper in repo, so can ref, can read the pdf, extract the page etc. for the text


# also for terms

# allow re identifying if re use the same quote in another



# auto build a glossary from the terms

# a bibliography from the refs, grouped by paper (and where referenced) 


# where the above is across the whole site, but generatable per post


# q&a as separately referenceable and a collective entity


# in the context of what linked to in paper, eg. a term


# but as above, aliasable in another context


# so posts are then python modules

# built up from the paper organised source data modules (can traverse the module)


# which render the quotes inline, extra text snippets, etc.


# so separate the data we construct it from, from the final output construction


# in a sense the posts can then become their own reference data source for others


# reconcile down to a json database? on build maybe not necessary

# and then build back up the posts as qmd?


# eg. flags on a term to show a list on the page of other uses, and just include a link to the glossary page (that also includes uses)

# all essentialyl a wrapper aroudn quarto



# ie you want it searchable both by us for research, and evne clone the repo and use the command line

# but also viewable as just a blog