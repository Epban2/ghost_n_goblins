import unittest
from unittest.mock import Mock
from flame import Flame
from zombie import Zombie


class TestFlame(unittest.TestCase):

    def setUp(self):
        self.arena = Mock()
        self.arena.size.return_value = (800, 400)

    def test_flame_lifetime(self):
        f = Flame((100, 100))
        f._lifetime = 1

        f.move(self.arena)
        self.arena.kill.assert_called_with(f)

    def test_flame_kills_zombies(self):
        z = Zombie(100, "left")
        self.arena.actors.return_value = [z]

        def always_hit(a, b): return True
        from actor import check_collision as original
        import actor
        actor.check_collision = always_hit

        f = Flame((100, 100))
        f.move(self.arena)

        self.arena.kill.assert_called_with(z)

        actor.check_collision = original