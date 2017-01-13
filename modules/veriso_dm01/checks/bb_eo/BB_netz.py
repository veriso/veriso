 # -*- coding: utf-8 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *

import sys
import traceback


try:
    _encoding = QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig)

from veriso.modules.complexcheck_base import ComplexCheckBase


class ComplexCheck(ComplexCheckBase):

    def __init__(self, iface):
        super(ComplexCheck, self).__init__(iface)
        self.iface = iface
        
        self.root = QgsProject.instance().layerTreeRoot()        
        self.layerLoader = LoadLayer(self.iface)

    def run(self):        
        self.settings = QSettings("CatAIS","VeriSO")
        project_id = self.settings.value("project/id")
        epsg = self.settings.value("project/epsg")
        
        locale = QSettings().value('locale/userLocale')[0:2] # Für Multilingual-Legenden.

        if not project_id:
            self.iface.messageBar().pushMessage("Error",  _translate("VeriSO_EE_BB_netz", "project_id not set", None), level=QgsMessageBar.CRITICAL, duration=5)                                
            return

        QApplication.setOverrideCursor(Qt.WaitCursor)
        try:
            group = _translate("VeriSO_EE_BB_netz", "Netze", None)
            group += " (" + str(project_id) + ")"
            layer = {}
            layer["type"] = "postgres"

            layer["title"] = _translate("VeriSO_EE_BB_netz", "Gewässernetz (BB)", None)
            layer["readonly"] = True
            layer["featuretype"] = "bodenbedeckung_boflaeche"
            layer["geom"] = "geometrie"
            layer["group"] = group
            layer["key"] = "ogc_fid"
            layer["sql"] = "art in (14,15,16)"
            layer["style"] = "bodenbedeckung/gewaesser.qml"
            vlayer = self.layerLoader.load(layer, False, True)
            layer = {}
            layer["type"] = "postgres"

            layer["title"] = _translate("VeriSO_EE_BB_netz", "Verkehrsnetz (BB)", None)
            layer["readonly"] = True
            layer["featuretype"] = "bodenbedeckung_boflaeche"
            layer["geom"] = "geometrie"
            layer["group"] = group
            layer["key"] = "ogc_fid"
            layer["sql"] = "art in (1,2,3,4)"
            layer["style"] = "bodenbedeckung/verkehr.qml"
            vlayer = self.layerLoader.load(layer, False, True)
            layer = {}
            layer["type"] = "postgres"

            layer["title"] = _translate("VeriSO_EE_BB_netz", "EO-Flächenelemente (Netz)", None)
            layer["readonly"] = True
            layer["featuretype"] = "z_eo_flaeche"
            layer["geom"] = "geometrie"
            layer["group"] = group
            layer["key"] = "ctid"
            layer["sql"] = "art in (3,5,6,7,17,18,22,25,26,29,34,36)"
            layer["style"] = "bodenbedeckung/eo_verkehr.qml"
            vlayer = self.layerLoader.load(layer, False, True)
            layer = {}
            layer["type"] = "postgres"

            layer["title"] = _translate("VeriSO_EE_BB_netz", "EO-Linienelemente (Netz)", None)
            layer["readonly"] = True
            layer["featuretype"] = "z_eo_linie"
            layer["geom"] = "geometrie"
            layer["group"] = group
            layer["key"] = "ctid"
            layer["sql"] = "art in (3,5,6,7,17,18,22,25,26,29,34,36)"
            layer["style"] = "bodenbedeckung/eo_linie_verkehr.qml"
            vlayer = self.layerLoader.load(layer, False, True)
            layer = {}
            layer["type"] = "postgres"

            layer["title"] = _translate("VeriSO_EE_BB_netz", "EO-Punkt", None)
            layer["readonly"] = True
            layer["featuretype"] = "z_eo_punkt"
            layer["geom"] = "geometrie"
            layer["group"] = group
            layer["key"] = "ctid"
            layer["sql"] = ""
            layer["style"] = "bodenbedeckung/eo_punk.qml"
            vlayer = self.layerLoader.load(layer, False, True)
        except Exception:
            QApplication.restoreOverrideCursor()            
            exc_type, exc_value, exc_traceback = sys.exc_info()
            self.iface.messageBar().pushMessage("Error", str(traceback.format_exc(exc_traceback)), level=QgsMessageBar.CRITICAL, duration=5)                    
        QApplication.restoreOverrideCursor()      
 

