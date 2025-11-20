from unittest import TestCase
from unittest.mock import Mock
from torch import Torch
from flame import Flame
from zombie import Zombie
from global_variables import GROUND_H, FLOOR_H


class TestTorch(TestCase):

    def setUp(self):
        self.arena = Mock()
        self.arena.size.return_value = (800, 400)
        self.arena.actors.return_value = []

    def test_horizontal_movement(self):
        t = Torch((100, 100), "right")
        x0, _ = t.pos()

        t.move(self.arena)
        x1, _ = t.pos()

        self.assertGreater(x1, x0) # Verifico che la x aggiornata sia minore della x di partenza

    def test_gravity(self):
        t = Torch((100, 50), "right")
        y0 = t.pos()[1]

        t.move(self.arena) # Applico gravità alla torcia
        y1 = t.pos()[1]

        self.assertGreater(y1, y0) # Verifico che la y aggiornata sia minore della y di partenza

    def test_spawn_flame_on_ground(self):
        t = Torch((100, 999), "right")
        t._y = 500  # Forza caduta

        t._y = GROUND_H + 1

        t.move(self.arena)
        self.arena.spawn.assert_called() # Verifo che venga chiamta la funzione spawn (flame)
        self.arena.kill.assert_called_with(t) # Controllo che la torcia venga eliminata

    def test_torch_kills_zombie(self):
        # Creo uno zombie nella stessa posizione della torcia
        z = Zombie(100, "left")
        self.arena.actors.return_value = [z]

        z.hit = Mock() # Verifico metodo hit per uccidere lo zombie

        # Creo la torcia nello stesso punto dello zombie
        t = Torch((100, FLOOR_H + 20), "right")
        t.move(self.arena)

        # Controllo che lo zombie sia stato ucciso
        z.hit.assert_called_with(self.arena)