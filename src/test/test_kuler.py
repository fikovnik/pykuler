import os
import unittest
import logging

from mock import Mock

import kuler

def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        return f.read()

class KulerTest(unittest.TestCase):

    def __init__(self, methodName='runTest'):
        super(KulerTest, self).__init__(methodName)

    def setUp(self):
        logging.basicConfig(level=logging.DEBUG)

    def tearDown(self):
        pass

    def testListingWithMaxItemsCount(self, count=10):
        k = kuler.Kuler('key1')

        k._urlFetch = Mock()
        k._urlFetch.return_value = read(os.path.join('test_data','one_result_per_page.xml'))

        l = k.list(maxItems=count, itemsPerPage=1)

        self.assertEquals(count, len(list(l)))
        self.assertEquals(count, k._urlFetch.call_count)

        args = [(('http://kuler-api.adobe.com/rss/get.cfm?listType=raiting&itemsPerPage=1&timeSpan=0&startIndex=%d&key=key1'
           % i,), {}) for i in range(count)]
        self.assertEquals(args, k._urlFetch.call_args_list)

    def testSearch(self):
        k = kuler.Kuler('key1')

        k._urlFetch = Mock()
        return_files = ['no-values.xml', 'no-values.xml', 'search-result.xml']
        k._urlFetch.side_effect = lambda x : read(os.path.join('test_data',
                                                               return_files.pop()))

        l = list(k.search(themeID='themeId'))

        self.assertEquals(1, len(l))
        self.assertEquals('Tech Office', l[0].title)

if __name__ == '__main__':
    unittest.main()

