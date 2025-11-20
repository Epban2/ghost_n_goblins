import unittest
from unittest.mock import Mock
from platform import Platform
from gravestone import Gravestone


class TestObstacles(unittest.TestCase):

    def test_platform_pos_size(self):
        p = Platform((10, 20), (30, 40))
        self.assertEqual(p.pos(), (10, 20))
        self.assertEqual(p.size(), (30, 40))

    def test_gravestone_hit(self):
        g = Gravestone((50, 50), (20, 20))
        arena = Mock()

        g.hit(arena)
        arena.kill.assert_called_with(g)