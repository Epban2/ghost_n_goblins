from unittest import TestCase
from unittest.mock import Mock
from arthur import Arthur
from global_variables import FLOOR_H, GRAVITY, holes
from zombie import Zombie
from torch import Torch
from actor import check_collision


class TestArthur(TestCase):

    # Creo un'arena finta con metodi simulati.
    def setUp(self):
        self.arena = Mock()
        self.arena.size.return_value = (800, 300) # Dimensione arena simulata (w, h)
        self.arena.actors.return_value = []
        self.arena.current_keys.return_value = []   

    # Test movimento orizzonatale
    def test_horizontal_movement(self):
        # Casi di movimento
        cases = [
            (["ArrowRight"], 3),
            (["ArrowLeft"], -3),
            ([], 0),
        ]

        for keys, dx in cases:
            with self.subTest(keys=keys): # Tratto caso per caso con test separati
                self.arena.current_keys.return_value = keys
                a = Arthur((100, FLOOR_H))
                x0, _ = a.pos()

                a.move(self.arena)
                x1, _ = a.pos()

                self.assertEqual(x1, x0 + dx) # posizione nuova == posizione vecchia + spostamento previsto

    # Test salto
    def test_jump_starts(self):
        self.arena.current_keys.return_value = ["ArrowUp"]
        a = Arthur((100, FLOOR_H))

        a.move(self.arena)
        self.assertTrue(a._jumping) # Verico che stia saltando
        self.assertLess(a._falling_speed, 0) # Verifico che la velocità di caduta sia minore di 0

    # Test gravità
    def test_gravity(self):
        a = Arthur((100, FLOOR_H - 40))
        y0 = a.pos()[1]

        a.move(self.arena)
        y1 = a.pos()[1]

        self.assertGreater(y1, y0) # Verifico y1 > y0

    # Test caduta nel buco
    def test_fall_in_hole(self):
        hx, hw = holes[0]
        a = Arthur((hx + 5, FLOOR_H))

        a.move(self.arena)
        self.assertTrue(a._is_falling) # Verifico che Arthur stia cadendo

    # Test collisione con zombie
    def test_collision_zombie(self):
        # Creo uno zombie vicino ad Arthur
        z = Zombie(100, "right")  # stessa x di Arthur per forzare collisione
        self.arena.actors.return_value = [z]

        # Creo Arthur nello stesso punto
        a = Arthur((100, FLOOR_H))

        a.move(self.arena)

        self.arena.kill.assert_called_with(a) # # Controllo che Arthur sia stato ucciso


   # Test sprite da fermo
    def test_idle_sprite_right(self):
        a = Arthur((100, FLOOR_H))
        a.move(self.arena)
        self.assertEqual(a.sprite(), a._idle_rigth_sprite)

    # Test lancio torcia
    def test_torch_spawn(self):
        self.arena.current_keys.return_value = ["Spacebar"]
        a = Arthur((100, FLOOR_H))
        a._torch_cooldown = 0

        a.move(self.arena)
        self.arena.spawn.assert_called() # Verifico che il metodo spawn sia stato chiamato