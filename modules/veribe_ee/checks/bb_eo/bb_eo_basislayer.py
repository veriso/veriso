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
            self.iface.messageBar().pushMessage("Error",  _translate("VeriSO_EE_BB_EO", "project_id not set", None), level=QgsMessageBar.CRITICAL, duration=5)                                
            return

        QApplication.setOverrideCursor(Qt.WaitCursor)
        try:

            group = _translate("VeriSO_EE_BB_EO", "bb_eo_allgemein", None)
            group += " (" + str(project_id) + ")"

            layer = {}
            layer["type"] = "postgres"
            layer["title"] = _translate("VeriSO_EE_BB_EO", "BB Nachfuehrung", None)
            
            layer["featuretype"] = "bodenbedeckung_bbnachfuehrung"

            layer["key"] = "ogc_fid"            

            layer["readonly"] = True
            layer["group"] = group   
            vlayerBBNachfuehrung = self.layerLoader.load(layer, False, True)              
            
            layer = {}
            layer["type"] = "postgres"
            layer["title"] = _translate("VeriSO_EE_BB_EO", "EO Nachfuehrung", None)
            
            layer["featuretype"] = "einzelobjekte_eonachfuehrung"

            layer["key"] = "ogc_fid"            
            layer["sql"] = ""
            layer["readonly"] = True
            layer["group"] = group   
            vlayerEONachfuehrung = self.layerLoader.load(layer, False, True)              
                        
            layer = {}
            layer["type"] = "postgres"
            layer["title"] = _translate("VeriSO_EE_BB_EO", "Bodenbedeckung", None)
            
            layer["featuretype"] = "bodenbedeckung_boflaeche"
            layer["geom"] = "geometrie"
            layer["key"] = "ogc_fid"            
            layer["sql"] = ""
            layer["readonly"] = True
            layer["group"] = group   
            layer["style"] = "bodenbedeckung/bb.qml"
            vlayerBodenbedeckung = self.layerLoader.load(layer, False, True)  

            layer = {}
            layer["type"] = "postgres"
            layer["title"] = _translate("VeriSO_EE_BB_EO", "Einzelobjekte Flaechenelement", None)
            
            layer["featuretype"] = "einzelobjekte_flaechenelement_v"
            layer["geom"] = "geometrie"
            layer["key"] = "ogc_fid"            
            layer["sql"] = ""
            layer["readonly"] = True
            layer["group"] = group   
            layer["style"] = "bodenbedeckung/eo_fl.qml"
            vlayerEOFlaechen = self.layerLoader.load(layer, False, True)  

            layer = {}
            layer["type"] = "postgres"
            layer["title"] = _translate("VeriSO_EE_BB_EO", "Einzelobjekte Linienelement", None)
            
            layer["featuretype"] = "einzelobjekte_linienelement_v"
            layer["geom"] = "geometrie"
            layer["key"] = "ogc_fid"            
            layer["sql"] = ""
            layer["readonly"] = True
            layer["group"] = group   
            layer["style"] = "bodenbedeckung/eo_li.qml"
            vlayerEOLinien = self.layerLoader.load(layer, False, True)  

            layer = {}
            layer["type"] = "postgres"
            layer["title"] = _translate("VeriSO_EE_BB_EO", "Einzelobjekte Punktelement", None)
            
            layer["featuretype"] = "einzelobjekte_punktelement_v"
            layer["geom"] = "geometrie"
            layer["key"] = "ogc_fid"            
            layer["sql"] = ""
            layer["readonly"] = True
            layer["group"] = group   
            layer["style"] = "bodenbedeckung/eo_pkt.qml"
            vlayerEOLinien = self.layerLoader.load(layer, False, True)  

            layer = {}
            layer["type"] = "postgres"
            layer["title"] = _translate("VeriSO_EE_BB_EO", "Gebaeudenummer", None)
            
            layer["featuretype"] = "bodenbedeckung_gebaeudenummer"

            layer["key"] = "ogc_fid"            
            layer["sql"] = ""
            layer["readonly"] = True
            layer["group"] = group   
            vlayerGebaeudenummer = self.layerLoader.load(layer, False, True)          
            
            layer = {}
            layer["type"] = "postgres"
            layer["title"] = _translate("VeriSO_EE_BB_EO", "Objektnummer", None)
            
            layer["featuretype"] = "einzelobjekte_objektnummer"

            layer["key"] = "ogc_fid"            
            layer["sql"] = ""
            layer["readonly"] = True
            layer["group"] = group   
            vlayerObjektnummer = self.layerLoader.load(layer, False, True)                   
        
            layer = {}
            layer["type"] = "postgres"
            layer["title"] = _translate("VeriSO_EE_BB_EO", "Gemeindegrenze", None)
            
            layer["featuretype"] = "gemeindegrenzen_gemeindegrenze"
            layer["geom"] = "geometrie"
            layer["key"] = "ogc_fid"            
            layer["sql"] = ""
            layer["readonly"] = True
            layer["group"] = group   
            layer["style"] = "gemeindegrenze/gemeindegrenze.qml"
            vlayerGemeinde = self.layerLoader.load(layer, False, True)  

        except Exception:
            QApplication.restoreOverrideCursor()            
            exc_type, exc_value, exc_traceback = sys.exc_info()
            self.iface.messageBar().pushMessage("Error", str(traceback.format_exc(exc_traceback)), level=QgsMessageBar.CRITICAL, duration=5)                    
        QApplication.restoreOverrideCursor() 


