from unittest import TestCase
from unittest.mock import Mock
from flame import Flame
from zombie import Zombie
from global_variables import FLOOR_H


class TestFlame(TestCase):

    def setUp(self):
        self.arena = Mock()
        self.arena.size.return_value = (800, 400)

    def test_flame_lifetime(self):
        f = Flame((100, 100))
        f._lifetime = 1

        f.move(self.arena)
        self.arena.kill.assert_called_with(f) # Controllo che la torcia venga eliminata una volta finito il suo lifetime

    def test_flame_kills_zombies(self):
        # Creo uno zombie vicino alla fiamma per forzare la collisione
        z = Zombie(100, "left")
        self.arena.actors.return_value = [z]

        z.hit = Mock() # Verifico metodo hit per uccidere lo zombie

        # Creo una fiamma nello stesso punto dello zombie
        f = Flame((100, FLOOR_H + 20)) # Stessa y dello zombie
        f.move(self.arena)

        z.hit.assert_called_with(self.arena)
