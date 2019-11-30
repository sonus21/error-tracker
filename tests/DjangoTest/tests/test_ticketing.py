# -*- coding: utf-8 -*-
#
#    Ticketing feature test, this tests whether raise_ticket method is called or not.
#
#    :copyright: 2019 Sonu Kumar
#    :license: BSD-3-Clause
#


import unittest
from django.test import LiveServerTestCase
from error_tracker.django.middleware import ticketing
from util import TestBase


class TicketingTest(LiveServerTestCase, TestBase):
    def test_tickets_are_raise(self):
        ticketing.clear()
        self.get('/value-error')
        self.assertEqual(len(ticketing.get_tickets()), 1)
        self.get('/value-error')
        self.assertEqual(len(ticketing.get_tickets()), 2)
        self.post('/value-error')
        self.assertEqual(len(ticketing.get_tickets()), 3)
        ticketing.clear()


if __name__ == '__main__':
    unittest.main()
