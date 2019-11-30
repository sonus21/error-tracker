# -*- coding: utf-8 -*-
#
#    Ticketing feature test, this tests whether raise_ticket method is called or not.
#
#    :copyright: 2018 Sonu Kumar
#    :license: BSD-3-Clause
#


import unittest
from tests.utils import TicketingSystem
from .utils import TestCaseMixin


class TicketingTest(TestCaseMixin, unittest.TestCase):
    db_prefix = "Ticketing"
    ticketing = TicketingSystem()
    kwargs = dict(ticketing=ticketing)

    def test_tickets_are_raise(self):
        db_name = "test_tickets_are_raise"
        app, db, error_tracker = self.setUpApp(db_name)
        with app.test_client() as c:
            result = c.get('/value-error')
            self.assertEqual(u'500', result.data.decode('utf-8'))
            self.assertEqual(len(self.ticketing.get_tickets()), 1)
            c.get('/value-error')
            self.assertEqual(len(self.ticketing.get_tickets()), 2)

            c.post('/value-error')

            self.assertEqual(len(self.ticketing.get_tickets()), 3)
            self.ticketing.clear()


if __name__ == '__main__':
    unittest.main()
