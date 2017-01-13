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
            self.iface.messageBar().pushMessage("Error",  _translate("VeriSO_EE_nk_allgemein", "project_id not set", None), level=QgsMessageBar.CRITICAL, duration=5)                                
            return

        QApplication.setOverrideCursor(Qt.WaitCursor)
        try:
            group = _translate("VeriSO_EE_nk_allgemein", u"Nomenklatur Übersicht", None)
            group += " (" + str(project_id) + ")" 

 




            layer = {}
            layer["type"] = "postgres"

            layer["title"] =  _translate("VeriSO_EE_nk_allgemein", u"Liegenschaften", None)
            layer["readonly"] = True
            layer["featuretype"] = "liegenschaften_liegenschaft"
            layer["geom"] = "geometrie"
            layer["group"] = group
            layer["key"] = "ogc_fid"
            layer["sql"] = ""
            layer["style"] = "liegenschaften/liegenschaft.qml"
            vlayer = self.layerLoader.load(layer, False, True) 
            layer = {}
            layer["type"] = "postgres"

            layer["title"] =  _translate("VeriSO_EE_nk_allgemein", u"SDR", None)
            layer["readonly"] = True
            layer["featuretype"] = "liegenschaften_selbstrecht"
            layer["geom"] = "geometrie"
            layer["group"] = group
            layer["key"] = "ogc_fid"
            layer["sql"] = ""
            layer["style"] = "liegenschaften/selbstrecht.qml"
            vlayer = self.layerLoader.load(layer, False, True) 
            layer = {}
            layer["type"] = "postgres"

            layer["title"] =  _translate("VeriSO_EE_nk_allgemein", u"proj. Liegenschaften", None)
            layer["readonly"] = True
            layer["featuretype"] = "liegenschaften_projliegenschaft"
            layer["geom"] = "geometrie"
            layer["group"] = group
            layer["key"] = "ogc_fid"
            layer["sql"] = ""
            layer["style"] = "liegenschaften/projliegenschaft.qml"
            vlayer = self.layerLoader.load(layer, False, True) 
            layer = {}
            layer["type"] = "postgres"

            layer["title"] =  _translate("VeriSO_EE_nk_allgemein", u"proj. SDR", None)
            layer["readonly"] = True
            layer["featuretype"] = "liegenschaften_projselbstrecht"
            layer["geom"] = "geometrie"
            layer["group"] = group
            layer["key"] = "ogc_fid"
            layer["sql"] = ""
            layer["style"] = "liegenschaften/projselbstrecht.qml"
            vlayer = self.layerLoader.load(layer, False, True) 
            layer = {}
            layer["type"] = "postgres"

            layer["title"] =  _translate("VeriSO_EE_nk_allgemein", u"Grst-Nr", None)
            layer["readonly"] = True
            layer["featuretype"] = "z_gs_nr"
            layer["geom"] = "pos"
            layer["group"] = group
            layer["key"] = "ogc_fid"
            layer["sql"] = ""
            layer["style"] = "liegenschaften/GS_NR.qml"
            vlayer = self.layerLoader.load(layer, False, True) 
            layer = {}
            layer["type"] = "postgres"

            layer["title"] =  _translate("VeriSO_EE_nk_allgemein", u"proj Grst-Nr", None)
            layer["readonly"] = True
            layer["featuretype"] = "z_projgs_nr"
            layer["geom"] = "pos"
            layer["group"] = group
            layer["key"] = "ogc_fid"
            layer["sql"] = ""
            layer["style"] = "liegenschaften/proj_GS_NR.qml"
            vlayer = self.layerLoader.load(layer, False, True) 

            layer = {}
            layer["type"] = "postgres"

            layer["title"] =  _translate("VeriSO_EE_nk_allgemein", u"Flurnamen", None)
            layer["readonly"] = True
            layer["featuretype"] = "nomenklatur_flurname"
            layer["geom"] = "geometrie"
            layer["group"] = group
            layer["key"] = "ogc_fid"
            layer["sql"] = ""
            layer["style"] = "nomenklatur/nomenklatur.qml"
            vlayerNKpkt = self.layerLoader.load(layer)

            layer = {}
            layer["type"] = "postgres"

            layer["title"] =  _translate("VeriSO_EE_nk_allgemein", u"Geländename", None)
            layer["readonly"] = True
            layer["featuretype"] = "nomenklatur_gelaendenamepos_v"
            layer["geom"] = "pos"
            layer["group"] = group
            layer["key"] = "ogc_fid"
            layer["sql"] = ""
            layer["style"] = "nomenklatur/gelaendenamen.qml"
            vlayer = self.layerLoader.load(layer)

            layer = {}
            layer["type"] = "postgres"

            layer["title"] =  _translate("VeriSO_EE_nk_allgemein", u"Ortsname", None)
            layer["readonly"] = True
            layer["featuretype"] = "nomenklatur_ortsname"
            layer["geom"] = "geometrie"
            layer["group"] = group
            layer["key"] = "ogc_fid"
            layer["sql"] = ""
            layer["style"] = "nomenklatur/ortsname.qml"
            vlayer = self.layerLoader.load(layer)


        except Exception:
            QApplication.restoreOverrideCursor()            
            exc_type, exc_value, exc_traceback = sys.exc_info()
            self.iface.messageBar().pushMessage("Error", str(traceback.format_exc(exc_traceback)), level=QgsMessageBar.CRITICAL, duration=5)                    
        QApplication.restoreOverrideCursor()      
 

