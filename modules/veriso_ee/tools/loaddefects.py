 # -*- coding: utf-8 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *

import utils
import os
import time
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

class LoadDefects(QObject):

    def __init__(self, iface):
        self.iface = iface
        self.canvas = self.iface.mapCanvas()
        
        self.root = QgsProject.instance().layerTreeRoot()        
        self.layerLoader = LoadLayer(self.iface)        

    def run(self):       
        try:
            self.settings = QSettings("CatAIS","VeriSO")
            self.project_id = self.settings.value("project/id")
            self.epsg = self.settings.value("project/epsg")
                    
            group = _translate("VeriSO_EE_Defects", "Mängel", None)
            group += " (" + str(self.project_id) + ")"                    

            layer = {}
            layer["type"] = "postgres"
            layer["title"] = _translate("VeriSO_EE_Defects", "Mängelliste (Punkte)", None)
            layer["featuretype"] = "t_maengel_punkt"
            layer["geom"] = "the_geom"
            layer["key"] = "ogc_fid"
            layer["readonly"] = False
            layer["sql"] = ""                        
            layer["group"] = group
            layer["style"] = "maengel/maengel_punkt.qml"
        
            vlayer = self.layerLoader.load(layer)
            if vlayer:
                vlayer.setEditorLayout(QgsVectorLayer.GeneratedLayout)
                
                ogc_fid_idx = vlayer.fieldNameIndex("ogc_fid")
                topic_idx = vlayer.fieldNameIndex("topic")                
                bemerkung_idx = vlayer.fieldNameIndex("bemerkung")                
                datum_idx = vlayer.fieldNameIndex("datum")
            
                vlayer.addAttributeAlias(topic_idx, _translate("VeriSO_EE_Defects", "Topic:", None))
                vlayer.addAttributeAlias(bemerkung_idx, _translate("VeriSO_EE_Defects", "Bemerkung:", None))
                
                vlayer.setEditorWidgetV2(ogc_fid_idx, "Hidden")
                vlayer.setEditorWidgetV2(topic_idx, "Enumeration")
                vlayer.setEditorWidgetV2(bemerkung_idx, "TextEdit") 
                vlayer.setEditorWidgetV2Config(bemerkung_idx, {"IsMultiline": True}) # See gui/editorwidgets/qgstexteditwrapper.cpp for all the parameters.
                vlayer.setEditorWidgetV2(datum_idx, "Hidden") 
                
            layer = {}
            layer["type"] = "postgres"
            layer["title"] = _translate("VeriSO_EE_Defects", "Mängelliste (Linien)", None)
            layer["featuretype"] = "t_maengel_linie"
            layer["geom"] = "the_geom"
            layer["key"] = "ogc_fid"
            layer["readonly"] = False
            layer["sql"] = ""                        
            layer["group"] = group
            layer["style"] = "maengel/maengel_linie.qml"

            vlayer = self.layerLoader.load(layer)
            if vlayer:
                vlayer.setEditorLayout(QgsVectorLayer.GeneratedLayout)
                
                ogc_fid_idx = vlayer.fieldNameIndex("ogc_fid")
                topic_idx = vlayer.fieldNameIndex("topic")                
                bemerkung_idx = vlayer.fieldNameIndex("bemerkung")                
                datum_idx = vlayer.fieldNameIndex("datum")
            
                vlayer.addAttributeAlias(topic_idx, _translate("VeriSO_EE_Defects", "Topic:", None))
                vlayer.addAttributeAlias(bemerkung_idx, _translate("VeriSO_EE_Defects", "Bemerkung:", None))
      
                vlayer.setEditorWidgetV2(ogc_fid_idx, "Hidden")
                vlayer.setEditorWidgetV2(topic_idx, "Enumeration")
                vlayer.setEditorWidgetV2(bemerkung_idx, "TextEdit") 
                vlayer.setEditorWidgetV2Config(bemerkung_idx, {"IsMultiline": True}) # See gui/editorwidgets/qgstexteditwrapper.cpp for all the parameters.
                vlayer.setEditorWidgetV2(datum_idx, "Hidden") 

        except Exception:
            QApplication.restoreOverrideCursor()            
            exc_type, exc_value, exc_traceback = sys.exc_info()
            self.iface.messageBar().pushMessage("Error", str(traceback.format_exc(exc_traceback)), level=QgsMessageBar.CRITICAL, duration=10)                    
        QApplication.restoreOverrideCursor()      

