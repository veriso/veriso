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
            self.iface.messageBar().pushMessage("Error",  _translate("VeriSO_EE_GemGrenz", "project_id not set", None), level=QgsMessageBar.CRITICAL, duration=5)                                
            return

        QApplication.setOverrideCursor(Qt.WaitCursor)
        try:
            group = _translate("VeriSO_EE_GemGrenz", "Gemeindegrenzen", None)
            group += " (" + str(project_id) + ")" 

            layer = {}
            layer["type"] = "wms"
            layer["url"] = "http://wms.geo.admin.ch/?"
            layer["layers"] = "ch.swisstopo.swissboundaries3d-kanton-flaeche.fill"
#            layer["crs"] = "EPSG:21781"
            layer["format"] = "image/png"
            layer["title"] = _translate("VeriSO_EE_GemGrenz", "Kantonsgrenze", None)
            layer["group"] = group
            vlayer = self.layerLoader.load(layer, False, True)

            layer = {}
            layer["type"] = "wms"
            layer["title"] = _translate("VeriSO_EE_GemGrenz", "Gemeindegrenzen-swisstopo", None)
            layer["url"] ="http://wms.geo.admin.ch/?"            
            layer["layers"] ="ch.swisstopo.swissboundaries3d-gemeinde-flaeche.fill"
            layer["format"] ="image/png"
            layer["group"] = group
#            layer["crs"] ="EPSG:21781"
            vlayer = self.layerLoader.load(layer, False, True) 
          

            layer = {}
            layer["type"] = "postgres"

            layer["title"] = _translate("VeriSO_EE_GemGrenz", "Gemeinde", None)
            layer["readonly"] = True
            layer["featuretype"] = "gemeindegrenzen_gemeindegrenze"
            layer["geom"] = "geometrie"
            layer["group"] = group
            layer["key"] = "ogc_fid"
            layer["sql"] = ""
            layer["style"] = "gemeindegrenze/gemeindegrenze.qml"
            vlayer = self.layerLoader.load(layer, False, True)  
            layer = {}
            layer["type"] = "postgres"

            layer["title"] = _translate("VeriSO_EE_GemGrenz", "Hoheitsgrenzpunkte unversichert", None)
            layer["readonly"] = True
            layer["featuretype"] = "gemeindegrenzen_hoheitsgrenzpunkt"
            layer["geom"] = "geometrie"
            layer["group"] = group
            layer["key"] = "ogc_fid"
            layer["sql"] = "punktzeichen=6"
            layer["style"] = "liegenschaften/GP_unver.qml"
            vlayer = self.layerLoader.load(layer, False, True)
            layer = {}
            layer["type"] = "postgres"

            layer["title"] = _translate("VeriSO_EE_GemGrenz", "Hoheitsgrenzpunkte nicht exakt definiert", None)
            layer["readonly"] = True
            layer["featuretype"] = "gemeindegrenzen_hoheitsgrenzpunkt"
            layer["geom"] = "geometrie"
            layer["group"] = group
            layer["key"] = "ogc_fid"
            layer["sql"] = "exaktdefiniert=1"
            layer["style"] = "liegenschaften/GP_exakt.qml"
            vlayer = self.layerLoader.load(layer, False, True)
            layer = {}
            layer["type"] = "postgres"

            layer["title"] = _translate("VeriSO_EE_GemGrenz", "Hoheitsgrenzpunkte (schoener Stein)", None)
            layer["readonly"] = True
            layer["featuretype"] = "gemeindegrenzen_hoheitsgrenzpunkt"
            layer["geom"] = "geometrie"
            layer["key"] = "ogc_fid"
            layer["group"] = group
            layer["sql"] = "Hoheitsgrenzstein=0"
            layer["style"] = "liegenschaften/HP_schoen.qml"
            vlayer = self.layerLoader.load(layer, False, True)
            layer = {}
            layer["type"] = "postgres"

            layer["title"] = _translate("VeriSO_EE_GemGrenz", u"Hoheitsgrenzpunkte Zuverlässigkeit", None)
            layer["readonly"] = True
            layer["featuretype"] = "gemeindegrenzen_hoheitsgrenzpunkt"
            layer["geom"] = "geometrie"
            layer["group"] = group
            layer["key"] = "ogc_fid"
            layer["sql"] = ""
            layer["style"] = "liegenschaften/GP_zuv.qml"
            vlayer = self.layerLoader.load(layer, False, True)
            layer = {}
            layer["type"] = "postgres"

            layer["title"] = _translate("VeriSO_EE_GemGrenz", "Hoheitsgrenzpunkte Genauigkeit", None)
            layer["readonly"] = True
            layer["featuretype"] = "gemeindegrenzen_hoheitsgrenzpunkt"
            layer["geom"] = "geometrie"
            layer["group"] = group
            layer["key"] = "ogc_fid"
            layer["sql"] = ""
            layer["style"] = "liegenschaften/GP_gen.qml"
            vlayer = self.layerLoader.load(layer, False, True)

            layer = {}
            layer["type"] = "postgres"

            layer["title"] = _translate("VeriSO_EE_GemGrenz", "proj. Gemeindegrenze", None)
            layer["readonly"] = True
            layer["featuretype"] = "gemeindegrenzen_projgemeindegrenze"
            layer["geom"] = "geometrie"
            layer["group"] = group
            layer["key"] = "ogc_fid"
            layer["sql"] = ""
            layer["style"] = "liegenschaften/projliegenschaft.qml"
            vlayer = self.layerLoader.load(layer, False, True)

            layer = {}
            layer["type"] = "postgres"

            layer["title"] = _translate("VeriSO_EE_GemGrenz", "Liegenschaften", None)
            layer["readonly"] = True
            layer["featuretype"] = "liegenschaften_liegenschaft"
            layer["geom"] = "geometrie"
            layer["group"] = group
            layer["key"] = "ogc_fid"
            layer["sql"] = ""
            layer["style"] = "liegenschaften/ls_quali.qml"
            vlayer = self.layerLoader.load(layer, False, True)

        except Exception:
            QApplication.restoreOverrideCursor()            
            exc_type, exc_value, exc_traceback = sys.exc_info()
            self.iface.messageBar().pushMessage("Error", str(traceback.format_exc(exc_traceback)), level=QgsMessageBar.CRITICAL, duration=5)                    
        QApplication.restoreOverrideCursor()         
 

