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

    def run(self):        
        self.settings = QSettings("CatAIS","VeriSO")
        project_id = self.settings.value("project/id")
        epsg = self.settings.value("project/epsg")
        
        locale = QSettings().value('locale/userLocale')[0:2] # Für Multilingual-Legenden.

        if not project_id:
            self.iface.messageBar().pushMessage("Error",  _translate("VeriSO_EE_plan_allgemein", "project_id not set", None), level=QgsMessageBar.CRITICAL, duration=5)                                
            return

        QApplication.setOverrideCursor(Qt.WaitCursor)
        try:
            group = _translate("VeriSO_EE_plan_allgemein", "Plan-Einteilung", None)
            group += " (" + str(project_id) + ")"  
            layer = {}
            layer["type"] = "postgres"

            layer["title"] = _translate("VeriSO_EE_plan_allgemein", "Gemeinde", None)
            layer["readonly"] = True
            layer["featuretype"] = "gemeindegrenzen_gemeindegrenze"
            layer["geom"] = "geometrie"
            layer["group"] = group
            layer["key"] = "ogc_fid"
            layer["sql"] = ""
            layer["style"] = "planeinteilung/gemeinde.qml"
            vlayer = self.layer_loader.load(layer, False, True)
            layer = {}
            layer["type"] = "postgres"

            layer["title"] = _translate("VeriSO_EE_plan_allgemein", "Bodenbedeckungskanten", None)
            layer["readonly"] = True
            layer["featuretype"] = "bodenbedeckung_boflaeche"
            layer["geom"] = "geometrie"
            layer["group"] = group
            layer["key"] = "ogc_fid"
            layer["sql"] = ""
            layer["style"] = "planeinteilung/bbkanten.qml"
            vlayer = self.layer_loader.load(layer, False, True)
            layer = {}
            layer["type"] = "postgres"

            layer["title"] = _translate("VeriSO_EE_plan_allgemein", "Liegenschaften", None)
            layer["readonly"] = True
            layer["featuretype"] = "liegenschaften_liegenschaft"
            layer["geom"] = "geometrie"
            layer["group"] = group
            layer["key"] = "ogc_fid"
            layer["sql"] = ""
            layer["style"] = "planeinteilung/liegenschaften.qml"
            vlayer = self.layer_loader.load(layer, False, True)
            layer = {}
            layer["type"] = "postgres"

            layer["title"] = _translate("VeriSO_EE_plan_allgemein", "Planeinteilung", None)
            layer["readonly"] = True
            layer["featuretype"] = "planeinteilungen_plan_v"
            layer["geom"] = "geometrie"
            layer["group"] = group
            layer["key"] = "ogc_fid"
            layer["sql"] = ""
            layer["style"] = "planeinteilung/plan.qml"
            vlayer = self.layer_loader.load(layer)
            layer = {}
            layer["type"] = "postgres"

            layer["title"] = _translate("VeriSO_EE_plan_allgemein", "Plan-Nr. Pos", None)
            layer["readonly"] = True
            layer["featuretype"] = "planeinteilungen_planpos"
            layer["geom"] = "pos"
            layer["group"] = group
            layer["key"] = "ogc_fid"
            layer["sql"] = ""
            layer["style"] = "planeinteilung/nr_pos.qml"
            vlayer = self.layer_loader.load(layer, False, True)



        except Exception:
            QApplication.restoreOverrideCursor()            
            exc_type, exc_value, exc_traceback = sys.exc_info()
            self.iface.messageBar().pushMessage("Error", str(traceback.format_exc(exc_traceback)), level=QgsMessageBar.CRITICAL, duration=5)                    
        QApplication.restoreOverrideCursor()          
 

