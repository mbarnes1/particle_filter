__author__ = 'mbarnes1'
import unittest
import sys
sys.path.append('../')
from map import Map


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self._map = Map('../../data/map/wean.dat')

    def test_display(self):
        self._map.display()

    def test_query(self):
