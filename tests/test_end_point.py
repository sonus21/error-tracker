import unittest

import pyquery

from utils import TestCaseMixin


class ViewTestCase(TestCaseMixin, unittest.TestCase):
    db_prefix = "ViewTestCase"

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
        self.tearDownApp(db)

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
        self.tearDownApp(db)

    def test_delete_view(self):
        db_name = "test_delete_view"
        app, db, error_manager = self.setUpApp(db_name)
        with app.test_client() as c:
            c.get('/value-error')
            response = c.get('/dev/error', follow_redirects=True)
            html = response.data
            url = [node.attrib['href'] for node in pyquery.PyQuery(html)('.delete')][0]
            c.get(url, follow_redirects=True)
            self.assertEqual(len(error_manager.get_all_errors()), 0)
        self.tearDownApp(db)


if __name__ == '__main__':
    unittest.main()
