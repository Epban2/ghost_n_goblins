import unittest
from unittest.mock import Mock
from zombie import Zombie


class TestZombie(unittest.TestCase):

    def setUp(self):
        self.arena = Mock()
        self.arena.size.return_value = (800, 400)

    def test_zombie_walks_left(self):
        z = Zombie(200, "left")
        x0, _ = z.pos()

        # forza automaticamente la fine dello spawn
        z._isspawning = False
        z._iswalking = True

        z.move(self.arena)
        x1, _ = z.pos()

        self.assertLess(x1, x0)

    def test_zombie_walks_right(self):
        z = Zombie(200, "right")
        x0, _ = z.pos()

        z._isspawning = False
        z._iswalking = True

        z.move(self.arena)
        x1, _ = z.pos()

        self.assertGreater(x1, x0)

    def test_zombie_despawns(self):
        z = Zombie(200, "right")
        z._isspawning = False
        z._iswalking = False
        z._isdespawning = False

        z.move(self.arena)

        self.arena.kill.assert_called_with(z)