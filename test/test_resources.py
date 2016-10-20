# coding=utf-8
"""Resources test.
"""

import unittest

from qgis.PyQt.QtGui import QIcon


class VeriSOResourcesTest(unittest.TestCase):
    """Test rerources work."""

    def setUp(self):
        """Runs before each test."""
        pass

    def tearDown(self):
        """Runs after each test."""
        pass

    # FIXME MB check and enable
    def Xtest_icon_png(self):
        """Test we can click OK."""
        path = ':/plugins/VeriSO/icon.png'
        icon = QIcon(path)
        self.assertFalse(icon.isNull())


if __name__ == "__main__":
    suite = unittest.makeSuite(VeriSOResourcesTest)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
