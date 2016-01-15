from scrapy.item import Item, Field


class MovieItem(Item):
    """
    Class s pomocjo katerega hranimo vse podatke o filmu.
    """
    img_src = Field()
    name = Field()
    genre = Field()
    released = Field()
    description = Field()
    director = Field()
    url = Field()
