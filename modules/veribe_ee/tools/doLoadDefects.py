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

from veriso.base.utils.doLoadLayer import LoadLayer

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
            layer["title"] = _translate("VeriSO_EE_Defects", "Informationsebenen", None)
            layer["featuretype"] = "t_maengel_topics"
            layer["key"] = "ogc_fid"            
            layer["sql"] = ""
            layer["readonly"] = True
            layer["group"] = group

            vlayer_topics = self.layerLoader.load(layer)
            
            # Es wird versucht die Namen der Informationsebenen
            # der gewünschten Sprache zu finden. Gibt es sie nicht,
            # wird das Attribut "topic_name" verwendet. Das MUSS
            # vorhanden sein. (Gibts sonst eh keinen Sinn.)
            locale = QSettings().value('locale/userLocale')[0:2]                    
            key_idx = vlayer_topics.fieldNameIndex("topic_name_" + str(locale))
            if key_idx < 0:
                topic_name = "topic_name"
            else:
                topic_name = "topic_name_" + str(locale)

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
                
                vlayer.setEditType(ogc_fid_idx, 11)
                vlayer.setEditType(topic_idx, QgsVectorLayer.ValueRelation)
                vlayer.setEditType(bemerkung_idx, 12)            
                vlayer.setEditType(datum_idx, 11) 
                
                vlayer.setLabelOnTop(topic_idx, True)
                vlayer.setLabelOnTop(bemerkung_idx, True)
                
                config = vlayer.editorWidgetV2Config(topic_idx)
                config["Layer"] = vlayer_topics.id()
                config["Key"] = topic_name
                config["Value"] = topic_name
                config["OrderByValue"] = False
                config["AllowNull"] = False
                config["AllowMulti"] = False

                vlayer.setEditorWidgetV2Config(topic_idx, config)

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
      
                vlayer.setEditType(ogc_fid_idx, 11)
                vlayer.setEditType(topic_idx, QgsVectorLayer.ValueRelation) # Ich bin mir nicht sicher, ob es jetzt nicht eine ganze andere Methode gibt, um den EditType zu setzen?
                vlayer.setEditType(bemerkung_idx, 12)            
                vlayer.setEditType(datum_idx, 11) 
                
                vlayer.setLabelOnTop(topic_idx, True)
                vlayer.setLabelOnTop(bemerkung_idx, True)
                
                config = vlayer.editorWidgetV2Config(topic_idx)
                config["Layer"] = vlayer_topics.id()
                config["Key"] = topic_name
                config["Value"] = topic_name
                config["OrderByValue"] = False
                config["AllowNull"] = False
                config["AllowMulti"] = False

                vlayer.setEditorWidgetV2Config(topic_idx, config)

        except Exception:
            QApplication.restoreOverrideCursor()            
            exc_type, exc_value, exc_traceback = sys.exc_info()
            self.iface.messageBar().pushMessage("Error", str(traceback.format_exc(exc_traceback)), level=QgsMessageBar.CRITICAL, duration=10)                    
        QApplication.restoreOverrideCursor()      

