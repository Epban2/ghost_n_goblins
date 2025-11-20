import unittest
from unittest.mock import Mock
from arthur import Arthur
from global_variables import FLOOR_H, GRAVITY, holes
from zombie import Zombie
from torch import Torch
from actor import check_collision


class TestArthur(unittest.TestCase):

    def setUp(self):
        self.arena = Mock()
        self.arena.size.return_value = (800, 300)
        self.arena.actors.return_value = []
        self.arena.current_keys.return_value = []

    # ----------------------------------------
    # MOVIMENTO ORIZZONTALE PARAMETRIZZATO
    # ----------------------------------------
    def test_horizontal_movement(self):
        cases = [
            (["ArrowRight"], 3),
            (["ArrowLeft"], -3),
            ([], 0),
        ]

        for keys, dx in cases:
            with self.subTest(keys=keys):
                self.arena.current_keys.return_value = keys
                a = Arthur((100, FLOOR_H))
                x0, _ = a.pos()

                a.move(self.arena)
                x1, _ = a.pos()

                self.assertEqual(x1, x0 + dx)

    # ----------------------------------------
    # SALTO
    # ----------------------------------------
    def test_jump_starts(self):
        self.arena.current_keys.return_value = ["ArrowUp"]
        a = Arthur((100, FLOOR_H))

        a.move(self.arena)
        self.assertTrue(a._jumping)
        self.assertLess(a._falling_speed, 0)

    # ----------------------------------------
    # GRAVITÀ APPLICATA
    # ----------------------------------------
    def test_gravity(self):
        a = Arthur((100, FLOOR_H - 40))
        y0 = a.pos()[1]

        a.move(self.arena)
        y1 = a.pos()[1]

        self.assertGreater(y1, y0)

    # ----------------------------------------
    # CADUTA NEL BUCO
    # ----------------------------------------
    def test_fall_in_hole(self):
        hx, hw = holes[0]
        a = Arthur((hx + 5, FLOOR_H))

        a.move(self.arena)
        self.assertTrue(a._is_falling)

    # ----------------------------------------
    # COLLISIONE CON ZOMBIE → MUORE
    # ----------------------------------------
    def test_collision_zombie(self):
        z = Zombie(50, "right")
        self.arena.actors.return_value = [z]

        # forziamo check_collision = True
        def always_hit(a, b): return True
        from actor import check_collision as original
        import actor
        actor.check_collision = always_hit

        a = Arthur((100, 100))
        a.move(self.arena)

        self.arena.kill.assert_called_with(a)

        actor.check_collision = original

    # ----------------------------------------
    # SPRITE CORRETTO DA FERMO
    # ----------------------------------------
    def test_idle_sprite_right(self):
        a = Arthur((100, FLOOR_H))
        a.move(self.arena)
        self.assertEqual(a.sprite(), a._idle_rigth_sprite)

    # ----------------------------------------
    # LANCIO TORCIA
    # ----------------------------------------
    def test_torch_spawn(self):
        self.arena.current_keys.return_value = ["Spacebar"]
        a = Arthur((100, FLOOR_H))
        a._torch_cooldown = 0

        a.move(self.arena)
        self.arena.spawn.assert_called()