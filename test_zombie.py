from unittest import TestCase
from unittest.mock import Mock
from zombie import Zombie


class TestZombie(TestCase):

    def setUp(self):
        self.arena = Mock()
        self.arena.size.return_value = (800, 400) # Dimensioni arena

    def test_zombie_walks_left(self):
        z = Zombie(200, "left") # Sinistra
        x0, _ = z.pos() # Prendo solo la x

        # Forza automaticamente la fine dello spawn
        z._isspawning = False
        z._iswalking = True

        z.move(self.arena)
        x1, _ = z.pos()

        self.assertLess(x1, x0) # Verifico che la x aggiornata sia minore della x di partenza

    def test_zombie_walks_right(self):
        z = Zombie(200, "right") # Destra
        x0, _ = z.pos()

        z._isspawning = False
        z._iswalking = True

        z.move(self.arena)
        x1, _ = z.pos()

        self.assertGreater(x1, x0) # Verifico che la x aggiornata sia maggiore della x di partenza

    def test_zombie_despawns(self):
        z = Zombie(200, "right")
        z._isspawning = False
        z._iswalking = False
        z._isdespawning = False

        z.move(self.arena)

        self.arena.kill.assert_called_with(z) # Funzione kill() dello zombie chiamata 