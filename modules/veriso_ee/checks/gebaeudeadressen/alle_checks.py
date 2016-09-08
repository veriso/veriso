# coding=utf-8
import sys
from builtins import str

from qgis.gui import QgsMessageBar

from collections import OrderedDict

from veriso.base.utils.utils import dynamic_import
from veriso.modules.complexcheck_base import ComplexCheckBase


class ComplexCheck(ComplexCheckBase):
    names = OrderedDict()
    names['de'] = 'Alle Checks'
    names['fr'] = 'Touts les Checks'

    def __init__(self, iface):
        super(ComplexCheck, self).__init__(iface)

    def run(self):
        package = "veriso.modules.veriso_ee.checks.gebaeudeadressen"
        try:
            module = "%s.lokalisation" % package
            _temp = dynamic_import(module)
            c = _temp.ComplexCheck(self.iface)
            c.run()

            module = "%s.checklayer" % package
            _temp = dynamic_import(module)
            c = _temp.ComplexCheck(self.iface)
            c.run()

            module = "%s.basislayer" % package
            _temp = dynamic_import(module)
            c = _temp.ComplexCheck(self.iface)
            c.run()

        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            self.message_bar.pushMessage("Error", str(e),
                                         level=QgsMessageBar.CRITICAL,
                                         duration=0)
