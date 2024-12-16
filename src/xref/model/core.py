# virtaul repr of site
# can be re-indexed / parsed after the fact


# create all the pages up front in a single page
# so they can be imported into the articles
# even before they havecontent
# so no cirular referenes (eg if two articles co-depend), and eg. you can tag with a listicle before you've filled the listicle


class Site:
    pass


class Page:
    pass


# the difference between orgs, people, topics is where the relevant header appears in the nav
# and what level of depth listicles are generated for them


# so each is a subclass of tag
# added as an annotation


# and then the page / navs are created from a given parent type (eg. all people, all topics, etc.)

# can separate types of people / org (startup vs uni)
# that might imply separate nav sections, or that could be a label on the page (or both)

# separate nav sections perhaps, collapsible, within the one nav (so hierarchy is people / org / topic)
# and then within those, founder vs academic, etc.

# the label could even be in the title "name: (type eg. startup)"


class Article(Page):
    pass


class Listicle(Page):
    pass


class Element:
    pass


class Annotated:

    text: str
    key: str

    def __repr__(self):
        return


class Annotation:
    pass


class Label(Annotation):
    pass


class Hyperlink(Annotation):
    pass


class Tag(Annotation):
    pass


# some are logical annoations (for indexing), some are content / formatting (eg. hyperlink)
# field to indicate which?


class Paragraph(Element):

    text: str
    keys: dict[int, str]
    annotations: dict[
        str, list[Annotation]
    ]  # on key str so changing order / adding new doesnt change

    # formats, str (?) that correspond to the various markup formats in quarto.text

    def add_text(self):
        # text as
        return

    def with_label(self):
        return  #


class Header:
    pass
