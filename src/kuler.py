#!/usr/bin/env python

import BeautifulSoup
import urllib2
import logging

def _urllib2Fetch(url):
    conn = None
    try:
        conn = urllib2.urlopen(url)
        return conn.read()
    finally:
        conn.close()

class Color:

    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

    def __str__(self):
        return '(%d, %d, %d)' % (self.r, self.g, self.b)

    def asRGB(self):
        return (self.r, self.g, self.b)

    def asRGB16(self):
        return tuple([c*256 if c < 256 else c for c in self.as_rgb()])

    @classmethod
    def fromHexRGB(cls, hexrgb):
        # http://stackoverflow.com/questions/214359/converting-hex-to-rgb-and-vice-versa
        hexrgb = hexrgb.lstrip('#')
        lv = len(hexrgb)
        return cls(*tuple(int(hexrgb[i:i+lv/3], 16) for i in range(0, lv, lv/3)))

    @classmethod
    def fromRGB(cls, r, g, b):
        return cls(r, g, b)

class Theme:

    def __init__(self, theme_id, title, colors):
        self.theme_id = theme_id
        self.title = title
        self.colors = colors

    def __getitem__(self, index):
        return self.colors[index]

    def __len__(self):
        return len(self.colors)

    def __iter__(self):
        return iter(self.colors)

    def __str__(self):
        return 'Theme: %s (%s)' % (self.theme_id, self.title)

    def items(self):
        return self.colors


# TODO: make it testable
class Kuler:

    def __init__(self, apiKey, urlFetch=_urllib2Fetch):
        self.apiKey = apiKey
        self.urlFetch = urlFetch

    def search(self, themeID=None, userID=None, email=None, tag=None,
               hex=None, title=None, startIndex=0, itemsPerPage=20, maxItems=100):
        """
        themeID - search on a specific themeID
        userID - search on a specific userID
        email - search on a specific email
        tag - search on a tag word
        hex - search on a hex color value (can be in the format "ABCDEF" or "0xABCDEF")
        title - search on a theme title
        """

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
            raise AttributeException('At least one seach query must be specified')

        return self._fetch('rss/search.cfm', searchQuery=searchQuery,
                           startIndex=startIndex, itemsPerPage=itemsPerPage,
                           maxItems=maxItems)

    def list(self, listType='raiting', startIndex=0, itemsPerPage=20,
             timeSpan=0, maxItems=100):
        """
            @param listType: Optional. One of the strings recent (the default), popular, rating, or random.
            @param startIndex: Optional. A 0-based index into the list that specifies the first item to display. Default is 0, which displays the first item in the list.
            @param itemsPerPage: Optional. The maximum number of items to display on a page, in the range 1..100. Default is 20.
            @param timeSpan: Optional. Value in days to limit the set of themes retrieved. Default is 0, which retrieves all themes without time limit.
            {@link http://learn.adobe.com/wiki/display/kulerdev/B.+Feeds}
        """

        # Fetch HTML data from url

        return self._fetch('rss/get.cfm', listType=listType,
                           startIndex=startIndex, itemsPerPage=itemsPerPage,
                           timeSpan=timeSpan, maxItems=maxItems)

    def _fetch(self, service, startIndex=0, maxItems=100, **options):
        itemsCount = 0
        while maxItems == None or itemsCount < maxItems:
            url = 'http://kuler-api.adobe.com/%s?%s&startIndex=%d&key=%s' % (service,
                                                                            '&'.join('%s=%s' %
                                                                                     (i,str(j)) for i,j
                                                                                     in
                                                                                     options.items()),
                                                                            startIndex,
                                                                            self.apiKey)
            logging.debug('Fetching URL: %s' % url)

            # get the data
            data = self.urlFetch(url)

            # create the soup
            soup = BeautifulSoup.BeautifulSoup(data)

            # Note: all lower-case element names
            dataThemes = soup.findAll('kuler:themeitem')

            logging.debug('Found %d themes' % len(dataThemes))

            if len(dataThemes) == 0:
               break

            for dataTheme in dataThemes:
                themeId = dataTheme.find('kuler:themeid').contents[0]
                title = dataTheme.find('kuler:themetitle').contents[0]
                themeswatches = dataTheme.find('kuler:themeswatches')
                colors = [Color.fromHexRGB(color.contents[0]) for color in themeswatches.findAll('kuler:swatchhexcolor')]
                itemsCount += 1
                theme = Theme(themeId, title, colors)
                logging.debug('Decoded theme: %s' % theme)
                yield theme

            startIndex += 1

def main():
    import sys

    if len(sys.argv) != 2:
        print 'Usage: %s <apiKey>' % sys.argv[0]
        sys.exit(1)

    k = Kuler(sys.argv[1])
    for i, theme in enumerate(k.list()):
        print '%d. %s' % (i, theme)

if __name__ == '__main__':
    main()
