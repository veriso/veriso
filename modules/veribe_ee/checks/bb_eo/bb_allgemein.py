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
            self.iface.messageBar().pushMessage("Error",  _translate("VeriSO_EE_BB_allgemein", "project_id not set", None), level=QgsMessageBar.CRITICAL, duration=5)                                
            return

        QApplication.setOverrideCursor(Qt.WaitCursor)
        try:
            group = _translate("VeriSO_EE_BB_allgemein", "BB Allgemein", None)
            group += " (" + str(project_id) + ")"         
            layer = {}
            layer["type"] = "postgres"
            layer["title"] =  _translate("VeriSO_EE_BB_allgemein", "Liegenschaften", None)
            layer["readonly"] = True
            layer["featuretype"] = "liegenschaften_liegenschaft"
            layer["geom"] = "geometrie"
            layer["key"] = "ogc_fid"
            layer["group"] = group
            layer["sql"] = ""
            layer["style"] = "bodenbedeckung/ls.qml"
            vlayer = self.layerLoader.load(layer, False, True)
            layer = {}
            layer["type"] = "postgres" 
            layer["title"] =  _translate("VeriSO_EE_BB_allgemein", "Bodenbedeckung", None)
            layer["readonly"] = True
            layer["featuretype"] = "bodenbedeckung_boflaeche"
            layer["geom"] = "geometrie"
            layer["key"] = "ogc_fid"
            layer["group"] = group
            layer["sql"] = ""
            layer["style"] = "bodenbedeckung/bb.qml"
            vlayer = self.layerLoader.load(layer)
            layer = {}
            layer["type"] = "postgres" 
            layer["title"] =  _translate("VeriSO_EE_BB_allgemein", "Objektname", None)
            layer["readonly"] = True
            layer["featuretype"] = "bodenbedeckung_objektnamepos_v"
            layer["geom"] = "pos"
            layer["group"] = group
            layer["key"] = "ogc_fid"
            layer["sql"] = ""
            layer["style"] = "bodenbedeckung/objektnamen.qml"
            vlayer = self.layerLoader.load(layer, False, True)
 
            layer = {}
            layer["type"] = "postgres"     
            layer["title"] =  _translate("VeriSO_EE_BB_allgemein", "BEGID (BB)", None)
            layer["readonly"] = True
            layer["featuretype"] = "z_gebaeudenummer_pos"
            layer["key"] = "ogc_fid"
            layer["geom"] = "pos"
            layer["group"] = group
            layer["sql"] = ""
            layer["style"] = "gebaeudeadressen/BEGIDbb.qml"
            vlayer = self.layerLoader.load(layer, False, True)

            layer = {}
            layer["type"] = "postgres"     
            layer["title"] =  _translate("VeriSO_EE_BB_allgemein", "BB Symbole", None)
            layer["readonly"] = True
            layer["featuretype"] = "t_bb_sym"
            layer["key"] = "ogc_fid"
            layer["geom"] = "pos"
            layer["group"] = group
            layer["sql"] = ""
            layer["style"] = "bodenbedeckung/bb_symbol.qml"
            vlayer = self.layerLoader.load(layer, False, True)
 
        except Exception:
          QApplication.restoreOverrideCursor()            
          exc_type, exc_value, exc_traceback = sys.exc_info()
          self.iface.messageBar().pushMessage("Error", str(traceback.format_exc(exc_traceback)), level=QgsMessageBar.CRITICAL, duration=5)                    
        QApplication.restoreOverrideCursor()         
 

