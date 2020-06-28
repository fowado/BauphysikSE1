import unittest

import Calculation
from TabData import TabData
from LayerData import LayerData

class TestScript_029(unittest.TestCase):
    """
    Temperaturverlaufs-Berechnung 2 Schichten
    analog manuellem TestScript_017
    """
    def setUp(self):
        self.layer_1 = LayerData()
        self.layer_1.r = 0.25

        self.layer_2 = LayerData()
        self.layer_2.r = 2.86

        self.tab = TabData(0, "Test_029")
        self.tab.rright = 0.04
        self.tab.rleft = 0.13
        self.tab.tright = 20
        self.tab.tleft = -7.5

        self.tab.add_layer(self.layer_1)
        self.tab.add_layer(self.layer_2)

    def test_3(self):
        """
        Calculate R_ges, R_T, U for Tab
        """
        self.tab.calculate()
        self.assertTrue(self.tab.rsum == 3.11)
        self.assertTrue(self.tab.rt == 3.28)
        self.assertTrue(round(self.tab.u,4) == 0.3049)

    def test_4(self):
        """
            Check calculated temperature
        """
        self.tab.calculate()
        self.assertTrue(round(self.tab.layers[0].t_left, 2) == 18.91)
        self.assertTrue(round(self.tab.layers[0].t_right, 2) == 16.81)
        self.assertTrue(round(self.tab.layers[1].t_left, 2) == 16.81)
        self.assertTrue(round(self.tab.layers[1].t_right, 2) == -7.16)


if __name__ == '__main__':
    unittest.main()
