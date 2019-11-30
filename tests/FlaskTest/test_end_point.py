# -*- coding: utf-8 -*-
#
#    Test all end points are working as expected
#
#    :copyright: 2019 Sonu Kumar
#    :license: BSD-3-Clause
#

import unittest

import pyquery
from .utils import TestCaseMixin
from .configs import pagination_config


class ViewTest(TestCaseMixin):
    db_prefix = "ViewTestCase"
    config_module = pagination_config

    def test_list_view(self):
        db_name = "test_list_view"
        app, db, _ = self.setUpApp(db_name)
        with app.test_client() as c:
            c.get('/value-error')
            c.post('/post-view')
            response = c.get('/dev/error', follow_redirects=True)
            html = response.data
            urls = [node.attrib['href'] for node in pyquery.PyQuery(html)('a')]
            # 2 links for delete operation and 2 links to navigate
            self.assertEqual(len(urls), 2 + 2)

            urls = [node.attrib['href'] for node in pyquery.PyQuery(html)('.view-link')]
            self.assertEqual(len(urls), 2)

    def test_detail_view(self):
        db_name = "test_detail_view"
        app, db, _ = self.setUpApp(db_name)
        with app.test_client() as c:
            c.get('/value-error')
            response = c.get('/dev/error', follow_redirects=True)
            html = response.data
            url = [node.attrib['href'] for node in pyquery.PyQuery(html)('.view-link')][0]
            response = c.get(url)
            row = pyquery.PyQuery(response.data)('.row')[0]
            # row = etree.tostring(row, pretty_print=False)
            p = pyquery.PyQuery(row)('p')
            divs = pyquery.PyQuery(row)('.row div')
            self.assertEqual(len(p), 5)
            self.assertEqual(len(divs), 2)

    def test_delete_view(self):
        db_name = "test_delete_view"
        app, db, error_tracker = self.setUpApp(db_name)
        with app.test_client() as c:
            c.get('/value-error')
            response = c.get('/dev/error', follow_redirects=True)
            html = response.data
            url = [node.attrib['href'] for node in pyquery.PyQuery(html)('.delete')][0]
            c.get(url, follow_redirects=True)
            self.assertEqual(len(error_tracker.get_exceptions()), 0)

    def test_pagination(self):
        db_name = "test_pagination"
        app, db, error_tracker = self.setUpApp(db_name)
        distinct_exceptions = set()

        with app.test_client() as c:
            c.get('/value-error')
            exception = error_tracker.get_exceptions()[0]
            hashx = exception.hash
            inserted = 0
            i = 0
            while inserted < 20:
                i += 1
                idx = str(i) + hashx[2:]
                inserted += 1
                error_tracker.create_or_update_exception(idx, exception.host, exception.path,
                                                         exception.method, exception.request_data,
                                                         exception.exception_name,
                                                         exception.traceback)

            response = c.get('/dev/error', follow_redirects=True)
            urls = [node.attrib['href'] for node in pyquery.PyQuery(response.data)('a')]
            self.assertEqual(len(urls), pagination_config.APP_DEFAULT_LIST_SIZE * 2 + 1)
            self.assertTrue('/dev/error/?page=2' in urls)

            response = c.get('/dev/error?page=2', follow_redirects=True)
            urls = [node.attrib['href'] for node in pyquery.PyQuery(response.data)('a')]
            self.assertEqual(len(urls), pagination_config.APP_DEFAULT_LIST_SIZE * 2 + 2)
            self.assertTrue('/dev/error/?page=1' in urls)
            self.assertTrue('/dev/error/?page=3' in urls)

            response = c.get('/dev/error?page=5', follow_redirects=True)
            urls = [node.attrib['href'] for node in pyquery.PyQuery(response.data)('a')]
            self.assertTrue('/dev/error/?page=4' in urls)

            response = c.get('/dev/error?page=6', follow_redirects=True)
            urls = [node.attrib['href'] for node in pyquery.PyQuery(response.data)('a')]
            self.assertEqual(len(urls), 1)


if __name__ == '__main__':
    unittest.main()
