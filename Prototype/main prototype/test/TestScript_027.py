import unittest

import Calculation
from TabData import TabData
from LayerData import LayerData

class TestScript_027(unittest.TestCase):
    """
    U-Berechnung 2 Schichten
    analog manuellem TestScript_015
    """
    def setUp(self):
        self.layer_1 = LayerData()
        self.layer_1.widthUnit = 1
        self.layer_1.width = 0.365       #Werte stehen im Layer in Meter
        self.layer_1.lambda_ = 0.72

        self.layer_2 = LayerData()
        self.layer_2.widthUnit = 1
        self.layer_2.width = 0.02
        self.layer_2.lambda_ = 0.87

        self.tab = TabData(0, "Test_027")
        self.tab.rright = 0.04
        self.tab.rleft = 0.13

        self.tab.add_layer(self.layer_1)
        self.tab.add_layer(self.layer_2)

    def test_1(self):
        """
        Calculate R for Layer_1
        """
        self.layer_1.calculate()
        self.assertTrue(round(self.layer_1.r,5) == 0.50694)

    def test_2(self):
        """
        Calculate R for Layer_2
        """
        self.layer_2.calculate()
        self.assertTrue(round(self.layer_2.r,5) == 0.02299)

    def test_3(self):
        """
        Calculate R_ges, R_T, U for Tab
        """
        self.tab.calculate()
        self.assertTrue(round(self.tab.rsum,4) == 0.5299)
        self.assertTrue(round(self.tab.rt,4) == 0.6999)
        self.assertTrue(round(self.tab.u,4) == 1.4287)


if __name__ == '__main__':
    unittest.main()
