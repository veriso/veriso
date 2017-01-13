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
            self.iface.messageBar().pushMessage("Error",  _translate("VeriSO_EE_AV allgemein", "project_id not set", None), level=QgsMessageBar.CRITICAL, duration=5)                                
            return

        QApplication.setOverrideCursor(Qt.WaitCursor)
        try:
            group = _translate("VeriSO_EE_AV allgemein", "AV Allgemein", None)
            group += " (" + str(project_id) + ")" 
            layer = {}
            layer["type"] = "postgres"
            layer["title"] = _translate("VeriSO_EE_AV allgemein", "Toleranzstufen", None)
            layer["readonly"] = True
            layer["featuretype"] = "tseinteilung_toleranzstufe"
            layer["geom"] = "geometrie"
            layer["group"] = group
            layer["sql"] = ""
            layer["key"] = "ogc_fid"
            layer["style"] = "liegenschaften/TS.qml"
            vlayer = self.layerLoader.load(layer, False, True) 
            layer = {}
            layer["type"] = "postgres"
 
            layer["title"] = _translate("VeriSO_EE_AV allgemein", "Grundstuecke", None)
            layer["readonly"] = True
            layer["featuretype"] = "liegenschaften_grundstueck"
            layer["group"] = group
            layer["key"] = "ogc_fid"
            layer["sql"] = ""
            vlayer = self.layerLoader.load(layer, False, True) 
            layer = {}
            layer["type"] = "postgres"
 
            layer["title"] = _translate("VeriSO_EE_AV allgemein", "proj. SDR", None)
            layer["readonly"] = True
            layer["featuretype"] = "liegenschaften_projselbstrecht"
            layer["geom"] = "geometrie"
            layer["group"] = group
            layer["key"] = "ogc_fid"
            layer["sql"] = ""
            layer["style"] = "liegenschaften/projselbstrecht.qml"
            vlayer = self.layerLoader.load(layer)  
            layer = {}
            layer["type"] = "postgres"
 
            layer["title"] = _translate("VeriSO_EE_AV allgemein", "SDR", None)
            layer["readonly"] = True
            layer["featuretype"] = "liegenschaften_selbstrecht"
            layer["geom"] = "geometrie"
            layer["group"] = group
            layer["key"] = "ogc_fid"
            layer["sql"] = ""
            layer["style"] = "liegenschaften/selbstrecht.qml"
            vlayer = self.layerLoader.load(layer)  
            layer = {}
            layer["type"] = "postgres"
 
            layer["title"] = _translate("VeriSO_EE_AV allgemein", "proj. Liegenschaften", None)
            layer["readonly"] = True
            layer["featuretype"] = "liegenschaften_projliegenschaft"
            layer["geom"] = "geometrie"
            layer["group"] = group
            layer["key"] = "ogc_fid"
            layer["sql"] = ""
            layer["style"] = "liegenschaften/projliegenschaft.qml"
            vlayer = self.layerLoader.load(layer)  
            layer = {}
            layer["type"] = "postgres"
 
            layer["title"] = _translate("VeriSO_EE_AV allgemein", "Liegenschaften", None)
            layer["readonly"] = True
            layer["featuretype"] = "liegenschaften_liegenschaft"
            layer["geom"] = "geometrie"
            layer["group"] = group
            layer["key"] = "ogc_fid"
            layer["sql"] = ""
            layer["style"] = "liegenschaften/liegenschaft.qml"
            vlayer = self.layerLoader.load(layer)  
            layer = {}
            layer["type"] = "postgres"
 
            layer["title"] = _translate("VeriSO_EE_AV allgemein", "Hilfslinie", None)
            layer["readonly"] = True
            layer["featuretype"] = "liegenschaften_grundstueckpos"
            layer["geom"] = "hilfslinie"
            layer["group"] = group
            layer["key"] = "ogc_fid"
            layer["sql"] = ""
            layer["style"] = "liegenschaften/hilfslinie.qml"
            vlayer = self.layerLoader.load(layer, False, True) 
 
 
 
            layer = {}
            layer["type"] = "postgres"
 
            layer["title"] = _translate("VeriSO_EE_AV allgemein", "proj_Grst-Nr", None)
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
 
            layer["title"] = _translate("VeriSO_EE_AV allgemein", "Nr Gs(LS)", None)
            layer["readonly"] = True
            layer["featuretype"] = "z_nr_gs"
            layer["geom"] = "pos"
            layer["key"] = "ogc_fid"
            layer["group"] = group
            layer["sql"] = "(art=0) and (gesamteflaechenmass is NULL)"
            layer["style"] = "liegenschaften/nr_ls_ganz.qml"
            vlayer = self.layerLoader.load(layer, False, True) 
            layer = {}
            layer["type"] = "postgres"
 
            layer["title"] = _translate("VeriSO_EE_AV allgemein", "Nr Gs(SDR)", None)
            layer["readonly"] = True
            layer["featuretype"] = "z_nr_gs"
            layer["geom"] = "pos"
            layer["group"] = group
            layer["key"] = "ogc_fid"
            layer["sql"] = "(art>0) and (gesamteflaechenmass is NULL)"
            layer["style"] = "liegenschaften/nr_sdr_ganz.qml"
            vlayer = self.layerLoader.load(layer, False, True) 
            layer = {}
            layer["type"] = "postgres"
 
            layer["title"] = _translate("VeriSO_EE_AV allgemein", "Nr Gs(LS-Teil)", None)
            layer["readonly"] = True
            layer["featuretype"] = "z_nr_gs"
            layer["geom"] = "pos"
            layer["group"] = group
            layer["key"] = "ogc_fid"
            layer["sql"] = "(art=0) and (gesamteflaechenmass>0)"
            layer["style"] = "liegenschaften/nr_ls_teil.qml"
            vlayer = self.layerLoader.load(layer, False, True) 
            
            layer = {}
            layer["type"] = "postgres"
            layer["title"] = _translate("VeriSO_EE_AV allgemein", "Nr Gs(SDR Teil)", None)
            layer["readonly"] = True
            layer["featuretype"] = "z_nr_gs"
            layer["geom"] = "pos"
            layer["group"] = group
            layer["key"] = "ogc_fid"
            layer["sql"] = "art>0 and gesamteflaechenmass>0"
            layer["style"] = "liegenschaften/nr_sdr_teil.qml"
            vlayer = self.layerLoader.load(layer, False, True) 
            layer = {}
            layer["type"] = "postgres"
 
            layer["title"] = _translate("VeriSO_EE_AV allgemein", "Label ausserhalb Gs", None)
            layer["readonly"] = True
            layer["featuretype"] = "z_nr_gs"
            layer["geom"] = "pos"
            layer["group"] = group        
            layer["key"] = "ogc_fid"
            layer["sql"] = "lin=1"
            layer["style"] = "liegenschaften/lable_aussen.qml"
            vlayer = self.layerLoader.load(layer, False, True) 
            layer = {}
            layer["type"] = "postgres"
            layer["title"] = _translate("VeriSO_EE_AV allgemein", "Rutschgebiet", None)
            layer["readonly"] = True
            layer["featuretype"] = "rutschgebiete_rutschung"
            layer["geom"] = "geometrie"
            layer["group"] = group
            layer["sql"] = ""
            layer["key"] = "ogc_fid"
            layer["style"] = "liegenschaften/rutsch.qml"
            vlayer = self.layerLoader.load(layer, False, True) 
            layer = {}
            layer["type"] = "postgres"
            layer["title"] = _translate("VeriSO_EE_AV allgemein", "Rutschgebiet Pos", None)
            layer["readonly"] = True
            layer["featuretype"] = "rutschgebiete_rutschungpos"
            layer["geom"] = "pos"
            layer["group"] = group
            layer["sql"] = ""
            layer["key"] = "ogc_fid"
            layer["style"] = ""
            vlayer = self.layerLoader.load(layer, False, True) 


        except Exception:
            QApplication.restoreOverrideCursor()            
            exc_type, exc_value, exc_traceback = sys.exc_info()
            self.iface.messageBar().pushMessage("Error", str(traceback.format_exc(exc_traceback)), level=QgsMessageBar.CRITICAL, duration=5)                    
        QApplication.restoreOverrideCursor()  
   
  

