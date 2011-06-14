#Help on module kuler:

###NAME
    kuler - Unofficial API for Adobe Kuler service (kuler.adobe.com).

###FILE
    /Users/krikava/Documents/Projects/pykuler/src/kuler.py

###DESCRIPTION
    Sample example that prints out TOP 10 themes sorted by raiting (default)
    
    k = Kuler(apiKey)
    for (i, theme) in enumerate(k.list(maxItems=10)):
        print '%d. %s' % (i, theme)
    
    More information: http://learn.adobe.com/wiki/display/kulerdev/B.+Feeds

###CLASSES
     Color
     Kuler
     Theme
    
     class Color
     |  Class wrapping an RGB color
     |  
     |  Methods defined here:
     |  
     |  __init__(self, r, g, b)
     |  
     |  __str__(self)
     |  
     |  asRGB(self)
     |  
     |  asRGB16(self)
     |  
     |  ----------------------------------------------------------------------
     |  Class methods defined here:
     |  
     |  fromHexRGB(cls, hexrgb) from __builtin__.classobj
     |      Factory method that creates a Color instance from HTML like color string
     |      #rrggbb with 8 or 16 bit.
     |  
     |  fromRGB(cls, r, g, b) from __builtin__.classobj
    
    class Kuler
     |  Facade of the Kuler API
     |  
     |  Methods defined here:
     |  
     |  __init__(self, apiKey)
     |      apiKey: Mandatory. API key obtained from the Kuler service. (You can
     |      get it from http://kuler.adobe.com/api)
     |  
     |  list(self, listType='raiting', startIndex=0, itemsPerPage=20, timeSpan=0, maxItems=100)
     |      Returns a generator of themes from a feeds of a specified type. 
     |      
     |      listType: Optional. One of the strings recent (the default), popular,
     |      rating, or random.
     |      
     |      startIndex: Optional. A 0-based index into the list that specifies the
     |      first item to display. Default is 0, which displays the first item in
     |      the list.
     |      
     |      itemsPerPage: Optional. The maximum number of items to display on a
     |      page, in the range 1..100. Default is 20.
     |      
     |      timeSpan: Optional. Value in days to limit the set of themes retrieved.
     |      Default is 0, which retrieves all themes without time limit.  
     |      
     |      maxItems: Optional. The number of items returned at most.
     |  
     |  search(self, themeID=None, userID=None, email=None, tag=None, hex=None, title=None, startIndex=0, itemsPerPage=20, maxItems=100)
     |      Returns a generator of themes from a feeds that meet specified search criteria.
     |      
     |      Caller needs to specify one of the following parameter:
     |      themeID: search on a specific themeID
     |      userID: search on a specific userID
     |      email: search on a specific email
     |      tag: search on a tag word
     |      hex: search on a hex color value (can be in the format "ABCDEF" or "0xABCDEF")
     |      title: search on a theme title
     |      
     |      startIndex: Optional. A 0-based index into the list that specifies the
     |      first item to display. Default is 0, which displays the first item in
     |      the list.
     |      
     |      itemsPerPage: Optional. The maximum number of items to display on a
     |      page, in the range 1..100. Default is 20.
     |      
     |      maxItems: Optional. The number of items returned at most.
    
    class Theme
     |  Class wrapping a Kuler theme.
     |  
     |  Properties:
     |  title: theme title name
     |  themeId: theme ID
     |  colors: a tuple of Color instances in defined in the theme
     |  
     |  Methods defined here:
     |  
     |  __getitem__(self, index)
     |  
     |  __init__(self, themeID, title, colors)
     |      colors: Mandatory. Parameter that is an iterable object containing Color instances.
     |  
     |  __iter__(self)
     |  
     |  __len__(self)
     |  
     |  __str__(self)
     |  
     |  items(self)

###FUNCTIONS
    main()
        Sample example


