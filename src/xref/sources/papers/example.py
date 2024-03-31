
from ... import core

# eg. context is passed the parent object

# that we assign back to on close
# how we do know what to return?

# dot methods always return the original object, but mutated
# to edit the object, have to do with original.child() as child:

# ie. method vs free func, free func is the context manager
# or page.pipe(core.section)

# if you know where on the parent the child has come from, on close can edit the parent? 

# page = core.Aticle(

# ).summary(
#     # ... summary args, kwargs
# )

# page, (
#     section_a,
#     # ...
# ) = core.Article(
#     ...
# ).add(
#     section(...).add(
#         summary(...)
#         .add(
#             explanation(...)
#             .example(...)
#         )
#         .definition(...)
#     )
# ).with_sections()

# # with sections, with hcildren etc. return the node and whatever children you've selected (for eg. the above style tuple unpacking of the pipeline)


# section = (
#     section_a.()...
# )

# page = page.update(section)

# # also juts update(page, section)

# # so they all still need ids, so we can update by id after the fact


# # select operates likewise
# # either page.select( in context )

# # or select(...)

# # with given selectors

# so eg. 


# # ie. with allows you to build up a child object
# # using the same syntax, but with the parent assigned after

# # versus .child_type(...)
# # which just passes to the child func and assigns

# # so if you need ot pipe, use add

# # else .child_type() convenience methods for appending at the same parent level


# # so no state store necessary
# # as each of the above returns all that is required
# # for the object
# # or mutates directly and returns to the flow

# # it's not obviosu when you'd ever need to lnik back?
# # we don't even have a data structure for such a link

# # the point is rather that we can extract our links after
# # eg. terms, topics, categorics, quotes / citationsm etc.


# section, summary = section.with_summary()

# summary = summary.

#     # the with then just assigns an id, temporarily puts that in the page
#     # so that when you call page.update, it can replace by id
#     with core.section(page) as section:

#         # with section.summary(

#         # ).definition() as defin:

#         #     defin.explanation(

#         #     ).close(defin)


#         with section.pipe(core.summary, ...) as summ:

#             with summ.definition() as defn:
                
#                 summ = defn.explanation(

#                 ).pipe(core.update, summ)

#             section = section.update(summ)

#         page = page.update(section)

#         # etc.

#         # eg. inner layer, is only added ot the outer layer
#         # on context close

#         # so you can incrementally build up 

#         # definition, explanation then presumably acc onto the 


# page = (
#     core.Article()
#     .summary(

#     )
# )

# page, section_x = (
#     page.section(

#     )
#     .summary()
#     .defintion(
#         term="",
#     )
#     .explanation(

#     )
#     .s
#     .comment()
#     .s
#     .question()
#     .explanation()
#     .answer(core.select.last_question())
#     .s
#     .question()
#     .answer()
#     .example()
#     .example()
#     .ps
# )

# so, top right nav: (order tbc)

# blog posts (our own more free form writing - eg. cross sectional, market map type stuff, versus article / company vertical dives)
# startups (when we have them)
# articles / sources etc.
# topics
# terms

# people as well, at least once we have interviews
# and can get papers linked to for the person?
# corporates i suppose fall under the startups page

# these i guess can be added as tags wherever we want

# even defined inline on the page

# then left nav (local to the above):

# cross sectional blog posts - presumably by category?
# startups (when we have them), per startup, per write up (eg. if we plot a whole series per fund-raising, different conversations - pre meeting vs post, etc.) - presmably again by category (?)
# for article, is all the pages (by cateogry / article type)
# for topics, the search page per topic (by category)
# for terms, the definition and links / search for the term
# presumably group by topic (and topic by category?)

# or one page for each topic of the terms (?), so fewer pages, but with just the defintion / twisty hidden explanation
