 # -*- coding: utf-8 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *

import sys
import traceback

from veriso.base.utils.doLoadLayer import LoadLayer

try:
    _encoding = QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig)

class ComplexCheck(QObject):

    def __init__(self, iface):
        self.iface = iface
        
        self.root = QgsProject.instance().layerTreeRoot()        
        self.layerLoader = LoadLayer(self.iface)

    def run(self):        
        self.settings = QSettings("CatAIS","VeriSO")
        project_id = self.settings.value("project/id")
        epsg = self.settings.value("project/epsg")
        
        locale = QSettings().value('locale/userLocale')[0:2] # Für Multilingual-Legenden.

        if not project_id:
            self.iface.messageBar().pushMessage("Error",  _translate("VeriSO_EE_aktuell", "project_id not set", None), level=QgsMessageBar.CRITICAL, duration=5)                                
            return

        QApplication.setOverrideCursor(Qt.WaitCursor)
        try:
            group = _translate("VeriSO_EE_aktuell", "Orthofoto", None)
            group += " (" + str(project_id) + ")"
            layer = {}
            layer["type"] = "postgres"
            layer["title"] = _translate("VeriSO_EE_aktuell", "Bodenbedeckung", None)
            layer["readonly"] = True 
            layer["featuretype"] = "bodenbedeckung_boflaeche"
            layer["geom"] = "geometrie"
            layer["key"] = "ogc_fid"  
            layer["sql"] = ""
            layer["group"] = group
            layer["style"] = "bodenbedeckung/bb_kante_ortho.qml"
            vlayerBB = self.layerLoader.load(layer)

            #layer = {}
            #layer["type"] = "postgres"
            #layer["title"] = "Liegenschaften"
            #layer["readonly"] = True 
            #layer["featuretype"] = "liegenschaften_liegenschaft"
            #layer["geom"] = "geometrie"
            #layer["key"] = "ogc_fid"  
            #layer["sql"] = ""
            #layer["group"] = group
            #layer["style"] = "bodenbedeckung/ls_kante.qml"
            #vlayerLS = self.layerLoader.load(layer)

            layer = {}
            layer["type"] = "postgres"
            layer["title"] = _translate("VeriSO_EE_aktuell", "Einzelobjekte Flaechenelement", None)
            layer["readonly"] = True 
            layer["featuretype"] = "einzelobjekte_flaechenelement_v"
            layer["geom"] = "geometrie"
            layer["key"] = "ogc_fid"            
            layer["sql"] = ""
            layer["group"] = group
            layer["style"] = "bodenbedeckung/eo_fl_muster.qml"
            vlayerEOFlaechen = self.layerLoader.load(layer)

            layer = {}
            layer["type"] = "postgres"
            layer["title"] = _translate("VeriSO_EE_aktuell", "Einzelobjekte Linienelement", None)
            layer["readonly"] = True 
            layer["featuretype"] = "einzelobjekte_linienelement_v"
            layer["geom"] = "geometrie"
            layer["key"] = "ogc_fid"            
            layer["sql"] = ""
            layer["group"] = group
            layer["style"] = "bodenbedeckung/eo_linie_ortho.qml"
            vlayerEOLinien = self.layerLoader.load(layer)
 
            layer = {}
            layer["type"] = "postgres"
            layer["title"] = _translate("VeriSO_EE_aktuell", "Einzelobjekte Punktelement", None)
            layer["readonly"] = True 
            layer["featuretype"] = "einzelobjekte_punktelement_v"
            layer["geom"] = "geometrie"
            layer["key"] = "ogc_fid"            
            layer["sql"] = ""
            layer["group"] = group
            layer["style"] = "bodenbedeckung/eo_punkt_ortho.qml"
            vlayerEOPkt = self.layerLoader.load(layer)


        except Exception:
            QApplication.restoreOverrideCursor()            
            exc_type, exc_value, exc_traceback = sys.exc_info()
            self.iface.messageBar().pushMessage("Error", str(traceback.format_exc(exc_traceback)), level=QgsMessageBar.CRITICAL, duration=5)                    
        QApplication.restoreOverrideCursor()   

