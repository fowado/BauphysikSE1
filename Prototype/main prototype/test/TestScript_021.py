import unittest

import Calculation
from TabData import TabData
from LayerData import LayerData

class TestScript_021(unittest.TestCase):
    """
    U-Berechnung 4 Schichten
    analog manuellem TestScript_009
    """
    def setUp(self):
        #erstelle erste Schicht
        self.layer_1 = LayerData()
        self.layer_1.widthUnit = 1
        self.layer_1.width = 0.02
        self.layer_1.lambda_ = 0.350

        #erstelle zweite Schicht
        self.layer_2 = LayerData()
        self.layer_2.widthUnit = 1
        self.layer_2.width = 0.24
        self.layer_2.lambda_ = 0.560

        #erstelle dritte Schicht
        self.layer_3 = LayerData()
        self.layer_3.widthUnit = 1
        self.layer_3.width = 0.05
        self.layer_3.lambda_ = 0.045

        #erstelle vierte Schicht
        self.layer_4 = LayerData()
        self.layer_4.widthUnit = 1
        self.layer_4.width = 0.01
        self.layer_4.lambda_ = 0.700

        #erstelle Tab
        self.tab = TabData(0, "Test_021")
        self.tab.rright = 0.04
        self.tab.rleft = 0.13

        #Schichten in Tab hinzufügen
        self.tab.add_layer(self.layer_1)
        self.tab.add_layer(self.layer_2)
        self.tab.add_layer(self.layer_3)
        self.tab.add_layer(self.layer_4)

    def test_1(self):
        """
        Calculate R for Layer_1
        """
        self.layer_1.calculate()
        self.assertTrue(round(self.layer_1.r,5) == 0.05714)

    def test_2(self):
        """
        Calculate R for Layer_2
        """
        self.layer_2.calculate()
        self.assertTrue(round(self.layer_2.r,5) == 0.42857)

    def test_3(self):
        """
        Calculate R for Layer_3
        """
        self.layer_3.calculate()
        self.assertTrue(round(self.layer_3.r,5) == 1.11111)

    def test_4(self):
        """
        Calculate R for Layer_4
        """
        self.layer_4.calculate()
        self.assertTrue(round(self.layer_4.r,5) == 0.01429)

    def test_5(self):
        """
        Calculate R_ges, R_T, U for Tab (R_ges)
        """
        self.tab.calculate()
        self.assertTrue(round(self.tab.rsum,4) == 1.6111)
        self.assertTrue(round(self.tab.rt,4) == 1.7811)
        self.assertTrue(round(self.tab.u,4) == 0.5614)


if __name__ == '__main__':
    unittest.main()
