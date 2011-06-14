#!/usr/bin/python
"""
Unofficial API for Adobe Kuler service (kuler.adobe.com).

Sample example that prints out TOP 10 themes sorted by raiting (default)

  k = Kuler(apiKey)
  for (i, theme) in enumerate(k.list(maxItems=10)):
    print '%d. %s' % (i, theme)

More information: http://learn.adobe.com/wiki/display/kulerdev/B.+Feeds
"""

import BeautifulSoup
import urllib2
import logging

class Color:
    """
    Class wrapping an RGB color
    """

    def __init__(
        self,
        r,
        g,
        b,
        ):
        self.r = r
        self.g = g
        self.b = b

    def __str__(self):
        return '(%d, %d, %d)' % (self.r, self.g, self.b)

    def asRGB(self):
        return (self.r, self.g, self.b)

    def asRGB16(self):
        return tuple([(c * 256 if c < 256 else c) for c in
                     self.asRGB()])

    @classmethod
    def fromHexRGB(cls, hexrgb):
        """
        Factory method that creates a Color instance from HTML like color string
        #rrggbb with 8 or 16 bit.
        """
        # http://stackoverflow.com/questions/214359/converting-hex-to-rgb-and-vice-versa
        hexrgb = hexrgb.lstrip('#')
        lv = len(hexrgb)
        return cls(*tuple(int(hexrgb[i:i + lv / 3], 16) for i in
                   range(0, lv, lv / 3)))

    @classmethod
    def fromRGB(
        cls,
        r,
        g,
        b,
        ):
        return cls(r, g, b)


class Theme:
    """
    Class wrapping a Kuler theme.

    Properties:
    title: theme title name
    themeId: theme ID
    colors: a tuple of Color instances in defined in the theme
    """

    def __init__(
        self,
        themeID,
        title,
        colors,
        ):
        """
        colors: Mandatory. Parameter that is an iterable object containing Color instances.
        """
        self.themeID = themeID
        self.title = title
        self.colors = tuple(colors)

    def __getitem__(self, index):
        return self.colors[index]

    def __len__(self):
        return len(self.colors)

    def __iter__(self):
        return iter(self.colors)

    def __str__(self):
        return 'Theme: %s (%s)' % (self.themeID, self.title)

    def items(self):
        return self.colors

class Kuler:
    """
    Facade of the Kuler API
    """

    def __init__(self, apiKey):
        """
        apiKey: Mandatory. API key obtained from the Kuler service. (You can
        get it from http://kuler.adobe.com/api)
        """
        self.apiKey = apiKey

    def search(
        self,
        themeID=None,
        userID=None,
        email=None,
        tag=None,
        hex=None,
        title=None,
        startIndex=0,
        itemsPerPage=20,
        maxItems=100,
        ):
        """
        Returns a generator of themes from a feeds that meet specified search criteria.

        Caller needs to specify one of the following parameter:
        themeID: search on a specific themeID
        userID: search on a specific userID
        email: search on a specific email
        tag: search on a tag word
        hex: search on a hex color value (can be in the format "ABCDEF" or "0xABCDEF")
        title: search on a theme title

        startIndex: Optional. A 0-based index into the list that specifies the
        first item to display. Default is 0, which displays the first item in
        the list.

        itemsPerPage: Optional. The maximum number of items to display on a
        page, in the range 1..100. Default is 20.

        maxItems: Optional. The number of items returned at most.  """

        searchQuery = None
        if themeID:
            searchQuery = 'themeID:%s' % themeID
        elif userID:
            searchQuery = 'userID:%s' % userID
        elif email:
            searchQuery = 'email:%s' % email
        elif tag:
            searchQuery = 'tag:%s' % tag
        elif hex:
            searchQuery = 'hex:%s' % hex
        elif title:
            searchQuery = 'title:%s' % title
        else:
            raise AttributeException('At least one seach query must be specified'
                    )

        return self._fetch('rss/search.cfm', searchQuery=searchQuery,
                           startIndex=startIndex,
                           itemsPerPage=itemsPerPage, maxItems=maxItems)

    def list(
        self,
        listType='raiting',
        startIndex=0,
        itemsPerPage=20,
        timeSpan=0,
        maxItems=100,
        ):
        """
        Returns a generator of themes from a feeds of a specified type. 

        listType: Optional. One of the strings recent (the default), popular,
        rating, or random.

        startIndex: Optional. A 0-based index into the list that specifies the
        first item to display. Default is 0, which displays the first item in
        the list.

        itemsPerPage: Optional. The maximum number of items to display on a
        page, in the range 1..100. Default is 20.

        timeSpan: Optional. Value in days to limit the set of themes retrieved.
        Default is 0, which retrieves all themes without time limit.  

        maxItems: Optional. The number of items returned at most.  """

        # Fetch HTML data from url

        return self._fetch(
            'rss/get.cfm',
            listType=listType,
            startIndex=startIndex,
            itemsPerPage=itemsPerPage,
            timeSpan=timeSpan,
            maxItems=maxItems,
            )

    def _fetch(
        self,
        service,
        startIndex=0,
        itemsPerPage=20,
        maxItems=100,
        **options
        ):
        itemsCount = 0
        while maxItems == None or itemsCount < maxItems:
            url = \
                'http://kuler-api.adobe.com/%s?%s&startIndex=%d&key=%s' \
                % (service, '&'.join('%s=%s' % (i, str(j)) for (i,
                   j) in options.items()), startIndex, self.apiKey)
            logging.debug('Fetching URL: %s' % url)

            # get the data

            data = Kuler._urlFetch(url)

            # create the soup

            soup = BeautifulSoup.BeautifulSoup(data)

            # Note: all lower-case element names

            dataThemes = soup.findAll('kuler:themeitem')

            logging.debug('Found %d themes' % len(dataThemes))

            if len(dataThemes) == 0:
                # no items found
                break

            for dataTheme in dataThemes:
                themeId = dataTheme.find('kuler:themeid').contents[0]
                title = dataTheme.find('kuler:themetitle').contents[0]
                themeswatches = dataTheme.find('kuler:themeswatches')
                colors = [Color.fromHexRGB(color.contents[0])
                          for color in
                          themeswatches.findAll('kuler:swatchhexcolor')]
                itemsCount += 1
                theme = Theme(themeId, title, colors)
                logging.debug('Decoded theme: %s' % theme)
                yield theme

            if len(dataThemes) < itemsPerPage:
                # last page
                break

            startIndex += 1

    @staticmethod
    def _urlFetch(url):
        """
        Helper function that returns a content of the given url using the urllib2
        library.
        """
        conn = None
        try:
            conn = urllib2.urlopen(url)
            return conn.read()
        finally:
            conn.close()


def main():
    """
    Sample example
    """
    import sys

    if not len(sys.argv) in [2,3]:
        print 'Usage: %s <apiKey> [<themeID>]' % sys.argv[0]
        sys.exit(1)

    k = Kuler(sys.argv[1])
    themes = k.search(themeID=sys.argv[2]) if len(sys.argv) == 3 else k.list()
    for (i, theme) in enumerate(themes):
        print '%d. %s' % (i, theme)


if __name__ == '__main__':
    main()
