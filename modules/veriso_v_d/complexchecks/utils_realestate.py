 # -*- coding: utf-8 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *

import os
import sys
import traceback

from veriso.base.utils.loadlayer import LoadLayer

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
        self.layer_loader = LoadLayer(self.iface)

    def run(self):        
        self.settings = QSettings("CatAIS","VeriSO")
        project_id = self.settings.value("project/id")
        epsg = self.settings.value("project/epsg")
        self.project_dir = self.settings.value("project/projectdir")        
        self.project_id = self.settings.value("project/id")

        locale = QSettings().value('locale/userLocale')[0:2] # this is for multilingual legends
        
        if locale == "fr":
            pass
        elif locale == "it":
            pass
        else:
            locale = "de"

        if not project_id:
            self.iface.messageBar().pushMessage("Error",  _translate("VeriSO_V+D_BB", "project_id not set", None), level=QgsMessageBar.CRITICAL, duration=5)                                
            return

        QApplication.setOverrideCursor(Qt.WaitCursor)
        try:
            group = _translate("VeriSO_V+D_BB", "Grundstücke", None)
            group += " (" + str(project_id) + ")"

            layer = {}
            layer["type"] = "postgres"
            layer["title"] = _translate("VeriSO_V+D_BB", "LS.Liegenschaften", None) 
            layer["featuretype"] = "v_liegenschaften_liegenschaft"
            layer["geom"] = "geometrie"
            layer["key"] = "ogc_fid"            
            layer["sql"] = ""
            layer["readonly"] = True
            layer["group"] = group
            layer["style"] = "grundstuecke/liegenschaften.qml"
            vlayer = self.layer_loader.load(layer, False, True)          
   
            layer = {}
            layer["type"] = "postgres"
            layer["title"] = _translate("VeriSO_V+D_BB", "LS.GrundstueckPos (Liegenschaften)", None) 
            layer["featuretype"] = "v_liegenschaften_grundstueckpos"
            layer["geom"] = "pos"
            layer["key"] = "ogc_fid"            
            layer["sql"] = "art = 'Liegenschaft'"
            layer["readonly"] = True
            layer["group"] = group
            layer["style"] = "grundstuecke/grundstueckpos.qml"
            vlayer = self.layer_loader.load(layer, False, True)          

        except Exception:
            QApplication.restoreOverrideCursor()            
            exc_type, exc_value, exc_traceback = sys.exc_info()
            self.iface.messageBar().pushMessage("Error", str(traceback.format_exc(exc_traceback)), level=QgsMessageBar.CRITICAL, duration=5)                    
        QApplication.restoreOverrideCursor()


