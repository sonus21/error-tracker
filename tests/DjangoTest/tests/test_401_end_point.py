# -*- coding: utf-8 -*-
#
#    Test all end points are working as expected
#
#    :copyright: 2019 Sonu Kumar
# -*- coding: utf-8 -*-
#
#    Test view permission feature
#
#    :copyright: 2020 Sonu Kumar
#    :license: BSD-3-Clause
#


import unittest

from django.test import TestCase
from util import TestBase


class View401Test(TestCase, TestBase):
    def verify(self, url):
        response = self.get(url, follow=True)
        self.assertEqual(401, response.status_code)

    def test_list_view(self):
        self.verify("/dev")

    def test_detail_view(self):
        self.verify('/dev/xyz')

    def test_delete_view(self):
        self.verify("/dev/xyz/delete")


if __name__ == '__main__':
    unittest.main()
