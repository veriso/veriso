 # -*- coding: utf-8 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *
import sys
import traceback


from veriso.modules.complexcheck_base import ComplexCheckBase


class ComplexCheck(ComplexCheckBase):

    def __init__(self, iface):
        super(ComplexCheck, self).__init__(iface)
        self.iface = iface

    def run(self):        
        try:    
            _temp = __import__("gebaeudeadressen_checklayer", globals(), locals(), ['ComplexCheck'])
            c = _temp.ComplexCheck(self.iface)
            c.run()
            
            _temp = __import__("gebaeudeadressen_basislayer", globals(), locals(), ['ComplexCheck'])
            c = _temp.ComplexCheck(self.iface)
            c.run()  

            _temp = __import__("gebaeudeadressen_lokalisation", globals(), locals(), ['ComplexCheck'])
            c = _temp.ComplexCheck(self.iface)
            c.run()

        except Exception, e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            self.iface.messageBar().pushMessage("Error", str(e), level=QgsMessageBar.CRITICAL, duration=10)                    



