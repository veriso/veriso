 # -*- coding: utf-8 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *

import utils
import os
import time


class LoadDefects(QObject):

    def __init__(self, iface):
        self.iface = iface
        self.canvas = self.iface.mapCanvas()

    def run(self):       
        try:
            self.settings = QSettings("CatAIS","Qcadastre")
            self.project_id = str(self.settings.value("project/id"))
            self.epsg = str(self.settings.value("project/epsg"))
                    
            layer = {}
            layer["type"] = "postgres"
            layer["title"] = "Informationsebenen"
            layer["featuretype"] = "t_maengel_topics"
            layer["key"] = "ogc_fid"            
            layer["sql"] = ""
            layer["readonly"] = True
            layer["group"] = u"Mängel" + " (" + self.project_id + ")"

            layer_topics = utils.loadLayer(self.iface, layer)

            layer = {}
            layer["type"] = "postgres"
            layer["title"] = "Maengelliste (Punkte)"
            layer["featuretype"] = "t_maengel_punkt"
            layer["geom"] = "the_geom"
            layer["key"] = "ogc_fid"
            layer["readonly"] = False
            layer["sql"] = ""                        
            layer["group"] = u"Mängel" + " (" + self.project_id + ")"
            layer["style"] = "maengel/maengel_punkt.qml"
        
            vlayer = utils.loadLayer(self.iface, layer)  
            if vlayer:
                self.iface.legendInterface().setLayerVisible(vlayer, True) 
                vlayer.setLayerName(u"Mängelliste (Punkte)")

                ogc_fid_idx = vlayer.fieldNameIndex("ogc_fid")
                topic_idx = vlayer.fieldNameIndex("topic")                
                bemerkung_idx = vlayer.fieldNameIndex("bemerkung")                
                datum_idx = vlayer.fieldNameIndex("datum")
            
                vlayer.addAttributeAlias(topic_idx, "Topic:")
                vlayer.addAttributeAlias(bemerkung_idx, "Bemerkung:")
      
                vlayer.setEditType(ogc_fid_idx, 11)
                vlayer.setEditType(topic_idx, 15)
                vlayer.setEditType(bemerkung_idx, 12)            
                vlayer.setEditType(datum_idx, 11) 

                topic_valrel = vlayer.valueRelation(topic_idx)
                topic_valrel.mLayer = layer_topics.id()
                topic_valrel.mKey = "topic_name"
                topic_valrel.mValue = "topic_name"
                topic_valrel.mOrderByValue = False
                topic_valrel.mAllowNull = True
                topic_valrel.mAllowMulti = False
                
            layer = {}
            layer["type"] = "postgres"
            layer["title"] = u"Maengelliste (Linien)"
            layer["featuretype"] = "t_maengel_linie"
            layer["geom"] = "the_geom"
            layer["key"] = "ogc_fid"
            layer["readonly"] = False
            layer["sql"] = ""                        
            layer["group"] = u"Mängel" + " (" + self.project_id + ")"
            layer["style"] = "maengel/maengel_linie.qml"

            vlayer = utils.loadLayer(self.iface, layer)  
            if vlayer:
                self.iface.legendInterface().setLayerVisible(vlayer, True) 
                vlayer.setLayerName(u"Mängelliste (Linien)")

                ogc_fid_idx = vlayer.fieldNameIndex("ogc_fid")
                topic_idx = vlayer.fieldNameIndex("topic")                
                bemerkung_idx = vlayer.fieldNameIndex("bemerkung")                
                datum_idx = vlayer.fieldNameIndex("datum")
            
                vlayer.addAttributeAlias(topic_idx, "Topic:")
                vlayer.addAttributeAlias(bemerkung_idx, "Bemerkung:")
      
                vlayer.setEditType(ogc_fid_idx, 11)
                vlayer.setEditType(topic_idx, 15)
                vlayer.setEditType(bemerkung_idx, 12)            
                vlayer.setEditType(datum_idx, 11) 

                topic_valrel = vlayer.valueRelation(topic_idx)
                topic_valrel.mLayer = layer_topics.id()
                topic_valrel.mKey = "topic_name"
                topic_valrel.mValue = "topic_name"
                topic_valrel.mOrderByValue = False
                topic_valrel.mAllowNull = True
                topic_valrel.mAllowMulti = False
        except Exception, e:
            QApplication.setOverrideCursor(Qt.WaitCursor)            
            print "Couldn't do it: %s" % e            
            self.iface.messageBar().pushMessage("Error",  QCoreApplication.translate("QcadastreModule", str(e)), level=QgsMessageBar.CRITICAL, duration=5)                    
        
        QApplication.restoreOverrideCursor()        

        # Workaround for geometryless-tables-wgs84-bug.
        try:
            self.canvas.setMapUnits(0)		
            srs = QgsCoordinateReferenceSystem()
            srs.createFromSrid(int(self.epsg))
            renderer = self.canvas.mapRenderer()
            renderer.setDestinationCrs(srs)
        except Exception, e:
            print "Couldn't do it: %s" % e            
            self.iface.messageBar().pushMessage("Error",  QCoreApplication.translate("QcadastreModule", str(e)), level=QgsMessageBar.CRITICAL, duration=5)                    
            
