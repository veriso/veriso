 # -*- coding: utf-8 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *


class ComplexCheck(QObject):

    def __init__(self, iface):
        self.iface = iface

    def run(self):        
        try:    
            _temp = __import__("utils_realestate", globals(), locals(), ['ComplexCheck'])
            c = _temp.ComplexCheck(self.iface)
            c.run()
            
            _temp = __import__("bb_checklayer", globals(), locals(), ['ComplexCheck'])
            c = _temp.ComplexCheck(self.iface)
            c.run()

            _temp = __import__("bb_overview", globals(), locals(), ['ComplexCheck'])
            c = _temp.ComplexCheck(self.iface)
            c.run()  
            
        except Exception, e:
            self.iface.messageBar().pushMessage("Error", str(e), level=QgsMessageBar.CRITICAL, duration=5)                    
