import unittest
from unittest.mock import Mock
from torch import Torch
from flame import Flame


class TestTorch(unittest.TestCase):

    def setUp(self):
        self.arena = Mock()
        self.arena.size.return_value = (800, 400)
        self.arena.actors.return_value = []

    def test_horizontal_movement(self):
        t = Torch((100, 100), "right")
        x0, _ = t.pos()

        t.move(self.arena)
        x1, _ = t.pos()

        self.assertGreater(x1, x0)

    def test_gravity(self):
        t = Torch((100, 50), "right")
        y0 = t.pos()[1]

        t.move(self.arena)
        y1 = t.pos()[1]

        self.assertGreater(y1, y0)

    def test_spawn_flame_on_ground(self):
        t = Torch((100, 999), "right")
        t._y = 500  # forza caduta

        from global_variables import GROUND_H
        t._y = GROUND_H + 1

        t.move(self.arena)
        self.arena.spawn.assert_called()
        self.arena.kill.assert_called_with(t)