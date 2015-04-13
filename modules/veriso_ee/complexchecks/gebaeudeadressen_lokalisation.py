 # -*- coding: utf-8 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *

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
        self.canvas = self.iface.mapCanvas()
        
        self.root = QgsProject.instance().layerTreeRoot()        
        self.layer_loader = LoadLayer(self.iface)

    def run(self):        
        self.settings = QSettings("CatAIS","VeriSO")
        project_id = self.settings.value("project/id")
        epsg = self.settings.value("project/epsg")
        
        locale = QSettings().value('locale/userLocale')[0:2] 

        if not project_id:
            self.iface.messageBar().pushMessage("Error",  _translate("VeriSO_EE_Geb_LokTest", "project_id not set", None), level=QgsMessageBar.CRITICAL, duration=5)                                
            return

        QApplication.setOverrideCursor(Qt.WaitCursor)
        try:
            group = _translate("VeriSO_EE_Geb_LokTest", "Gebaeudeadressen - Lokalisationstest", None)
            group += " (" + str(project_id) + ")"
            
            
            # TODO: Check "tid" vs. t_ili_tid... in queries. Do not import i_ili_tid?
            
            # define layer names here
            lokalisation = _translate("VeriSO_EE_Geb_LokTest", "Lokalisation Lokalisationstest", None) 
            strassenstueck_geometrie = _translate("VeriSO_EE_Geb_LokTest", "Strassenstueck (geometrie) Lokalisationstest", None)  
            strassenstueck_anfangspunkt = _translate("VeriSO_EE_Geb_LokTest", "Strassenstueck (anfangspunkt) Lokalisationstest", None)  
            benanntesgebiet = _translate("VeriSO_EE_Geb_LokTest", "Benanntes Gebiet Lokalisationstest", None)  
            gebaeudeeingang = _translate("VeriSO_EE_Geb_LokTest", "Gebaeudeeingang Lokalisationstest", None)  
            shortestline = _translate("VeriSO_EE_Geb_LokTest", "Kuerzeste Linie Lokalisationstest", None)  
            hausnummerpos = _translate("VeriSO_EE_Geb_LokTest", "HausnummerPos Lokalisationstest", None)  
            lokalisationsname = _translate("VeriSO_EE_Geb_LokTest", "LokalisationsName", None)  
            
            vlayer_lokalisation = self.get_vector_layer_by_name(lokalisation)
            if not vlayer_lokalisation:
                layer = {}
                layer["type"] = "postgres"
                layer["title"] = lokalisation
                layer["featuretype"] = "gebaeudeadressen_lokalisation"
                layer["key"] = "ogc_fid"            
                layer["sql"] = "ogc_fid = -1"
                layer["readonly"] = True
                layer["group"] = group
                vlayer_lokalisation = self.layer_loader.load(layer)

            vlayer_strassenstueck_geometrie = self.get_vector_layer_by_name(strassenstueck_geometrie)
            if not vlayer_strassenstueck_geometrie:
                layer = {}
                layer["type"] = "postgres"
                layer["title"] = "Strassenstueck (geometrie) Lokalisationstest"
                layer["featuretype"] = "gebaeudeadressen_strassenstueck"
                layer["geom"] = "geometrie"
                layer["key"] = "ogc_fid"            
                layer["sql"] = "strassenstueck_von = -1"
                layer["readonly"] = True                
                layer["group"] = group
                layer["style"] = "gebaeudeadressen/strassenachsen_rot.qml"
                vlayer_strassenstueck_geometrie = self.layer_loader.load(layer)

            vlayer_strassenstueck_anfangspunkt = self.get_vector_layer_by_name(strassenstueck_anfangspunkt)
            if not vlayer_strassenstueck_anfangspunkt:
                layer = {}
                layer["type"] = "postgres"
                layer["title"] = "Strassenstueck (anfangspunkt) Lokalisationstest"
                layer["featuretype"] = "gebaeudeadressen_strassenstueck"
                layer["geom"] = "anfangspunkt"
                layer["key"] = "ogc_fid"            
                layer["sql"] = "strassenstueck_von = -1"
                layer["readonly"] = True                
                layer["group"] = group
                layer["style"] = "gebaeudeadressen/anfangspunkt_rot.qml"
                vlayer_strassenstueck_anfangspunkt = self.layer_loader.load(layer)

            vlayer_benanntesgebiet = self.get_vector_layer_by_name(benanntesgebiet)
            if not vlayer_benanntesgebiet:
                layer = {}
                layer["type"] = "postgres"
                layer["title"] = "Benanntes Gebiet Lokalisationstest"
                layer["featuretype"] = "gebaeudeadressen_benanntesgebiet"
                layer["geom"] = "flaeche"
                layer["key"] = "ogc_fid"            
                layer["sql"] = "benanntesgebiet_von = -1"
                layer["readonly"] = True                
                layer["group"] = group
                layer["style"] = "gebaeudeadressen/benanntesgebiet_rot.qml"
                vlayer_benanntesgebiet = self.layer_loader.load(layer)

            vlayer_gebaeudeeingang = self.get_vector_layer_by_name(gebaeudeeingang)
            if not vlayer_gebaeudeeingang:
                layer = {}
                layer["type"] = "postgres"
                layer["title"] = "Gebaeudeeingang Lokalisationstest"
                layer["featuretype"] = "gebaeudeadressen_gebaeudeeingang"
                layer["geom"] = "lage"
                layer["key"] = "ogc_fid"            
                layer["sql"] = "gebaeudeeingang_von = -1"
                layer["readonly"] = True                
                layer["group"] = group
                layer["style"] = "gebaeudeadressen/gebaeudeeingang_rot.qml"
                vlayer_gebaeudeeingang = self.layer_loader.load(layer)

            vlayer_shortestline = self.get_vector_layer_by_name(shortestline)
            if not vlayer_shortestline:
                layer = {}
                layer["type"] = "postgres"
                layer["title"] = "Kuerzeste Linie Lokalisationstest"
                layer["featuretype"] = "t_shortestline_hausnummerpos"
                layer["geom"] = "the_geom"
                layer["key"] = "ogc_fid"            
                layer["sql"] = "lok_tid = -1"
                layer["readonly"] = True                
                layer["group"] = group
                layer["style"] = "gebaeudeadressen/shortestline_linie_rot.qml"
                vlayer_shortestline = self.layer_loader.load(layer)

            vlayer_hausnummerpos = self.get_vector_layer_by_name(hausnummerpos)
            if not vlayer_hausnummerpos:
                layer = {}
                layer["type"] = "postgres"
                layer["title"] = "HausnummerPos Lokalisationstest"
                layer["featuretype"] = "v_gebaeudeadressen_hausnummerpos"
                layer["geom"] = "pos"
                layer["key"] = "ogc_fid"            
                layer["sql"] = "lok_tid = -1"
                layer["readonly"] = True                
                layer["group"] = group
                layer["style"] = "gebaeudeadressen/hausnummerpos_rot.qml"
                vlayer_hausnummerpos = self.layer_loader.load(layer)

            vlayer_lokalisationsname = self.get_vector_layer_by_name(lokalisationsname)
            if not vlayer_lokalisationsname:
                self.iface.messageBar().pushMessage("Error",  _translate("VeriSO_EE_Geb_LokTest", "Layer _LokalisationsName_ not found.", None), level=QgsMessageBar.CRITICAL, duration=10)                    
                QApplication.restoreOverrideCursor()   
                return         
            
            iter = vlayer_lokalisationsname.getFeatures()
            ids = []

            for feature in iter:
                ids.append(feature.id())

            if vlayer_lokalisationsname.selectedFeatureCount() < 1:
                self.iface.messageBar().pushMessage("Error",  _translate("VeriSO_EE_Geb_LokTest", "No _LokalisationsName_ selected.", None), level=QgsMessageBar.WARNING, duration=10)                    
                QApplication.restoreOverrideCursor()   
                return         
                
            if vlayer_lokalisationsname.selectedFeatureCount() > 1:
                self.iface.messageBar().pushMessage("Error",  _translate("VeriSO_EE_Geb_LokTest", "Please select only one (1) _LokalisationsName_.", None), level=QgsMessageBar.WARNING, duration=10)                                    
                QApplication.restoreOverrideCursor()   
                return         

            feat = QgsFeature()
            id = vlayer_lokalisationsname.selectedFeaturesIds()[0]            
            feat = vlayer_lokalisationsname.selectedFeatures()[0]
            idx = ids.index(id)
            
            benannte_idx = vlayer_lokalisationsname.fieldNameIndex("benannte")
            text_idx = vlayer_lokalisationsname.fieldNameIndex("atext")
            
            if benannte_idx == -1 or text_idx == -1:
                self.iface.messageBar().pushMessage("Error",  _translate("VeriSO_EE_Geb_LokTest", "Field _benannte_ or _text_ not found.", None), level=QgsMessageBar.CRITICAL, duration=10)                                                    
                QApplication.restoreOverrideCursor()
                return

            benannte =  feat.attributes()[benannte_idx]
            lokalisationsname = feat.attributes()[text_idx]
        
            vlayer_strassenstueck_geometrie.setSubsetString("(strassenstueck_von = "+str(benannte)+")")
            vlayer_strassenstueck_anfangspunkt.setSubsetString("(strassenstueck_von = "+str(benannte)+")")
            vlayer_benanntesgebiet.setSubsetString("(benanntesgebiet_von = "+str(benannte)+")")
            vlayer_gebaeudeeingang.setSubsetString("(gebaeudeeingang_von = "+str(benannte)+")")
            vlayer_lokalisation.setSubsetString("(ogc_fid = "+str(benannte)+")")
            vlayer_shortestline.setSubsetString("(lok_tid = "+str(benannte)+")")
            vlayer_hausnummerpos.setSubsetString("(lok_tid = "+str(benannte)+")")

            if vlayer_strassenstueck_geometrie.featureCount() > 0:
                xMin = vlayer_strassenstueck_geometrie.extent().xMinimum()
                yMin = vlayer_strassenstueck_geometrie.extent().yMinimum()
                xMax = vlayer_strassenstueck_geometrie.extent().xMaximum()
                yMax = vlayer_strassenstueck_geometrie.extent().yMaximum()
                
            if vlayer_benanntesgebiet.featureCount() > 0:
                xMin = vlayer_benanntesgebiet.extent().xMinimum()
                yMin = vlayer_benanntesgebiet.extent().yMinimum()
                xMax = vlayer_benanntesgebiet.extent().xMaximum()
                yMax = vlayer_benanntesgebiet.extent().yMaximum()
               
            try:
                if vlayer_gebaeudeeingang.featureCount() > 0:
                    if vlayer_gebaeudeeingang.extent().xMinimum() < xMin:
                        xMin = vlayer_gebaeudeeingang.extent().xMinimum()
                    if vlayer_gebaeudeeingang.extent().yMinimum() < yMin:
                        yMin = vlayer_gebaeudeeingang.extent().yMinimum()
                    if vlayer_gebaeudeeingang.extent().xMaximum() > xMax:
                        xMax = vlayer_gebaeudeeingang.extent().xMaximum()
                    if vlayer_gebaeudeeingang.extent().yMaximum() > yMax:
                        yMax = vlayer_gebaeudeeingang.extent().yMaximum()                
                        
                rect = QgsRectangle(xMin,  yMin,  xMax,  yMax)
                rect.scale(1.3)
        
            except UnboundLocalError, e:
                vlayer_gemeindegrenze = self.getVectorLayerByName("Gemeindegrenze")
                if vlayer_gemeindegrenze == None:
                    rect = self.canvas.fullExtent()
                else:
                    rect = vlayer_gemeindegrenze.extent()

            self.iface.mapCanvas().setExtent(rect)
            self.iface.mapCanvas().refresh()                
            
            iter = vlayer_lokalisation.getFeatures()
            
            # only one feature is selected
            for feature in iter:
                prinzip_idx = vlayer_lokalisation.fieldNameIndex("nummerierungsprinzip_txt")
                attributeprovisorisch_idx = vlayer_lokalisation.fieldNameIndex("attributeprovisorisch_txt")
                offiziell_idx = vlayer_lokalisation.fieldNameIndex("istoffiziellebezeichnung_txt")
                status_idx = vlayer_lokalisation.fieldNameIndex("status_txt")
                inaenderung_idx = vlayer_lokalisation.fieldNameIndex("inaenderung_txt")
                art_idx = vlayer_lokalisation.fieldNameIndex("art_txt")
                
                if prinzip_idx == -1 or attributeprovisorisch_idx == -1 or offiziell_idx == -1 or status_idx == -1 or inaenderung_idx == -1 or art_idx == -1:
                    self.iface.messageBar().pushMessage("Error",  _translate("VeriSO_EE_Geb_LokTest", "Field not found.", None), level=QgsMessageBar.CRITICAL, duration=10)                                                                        
                    QApplication.restoreOverrideCursor()
                    return

                prinzip = feature.attributes()[prinzip_idx]
                attributeprovisorisch = feature.attributes()[attributeprovisorisch_idx]            
                offiziell = feature.attributes()[offiziell_idx]
                status = feature.attributes()[status_idx]
                inaenderung = feature.attributes()[inaenderung_idx]
                art = feature.attributes()[art_idx]

                map_extent = self.canvas.extent()
                x = map_extent.xMinimum()
                y = map_extent.yMaximum()

            text_item_found = False
            items = self.iface.mapCanvas().scene().items()
            for i in range (len(items)):
                try:
                    name =  items[i].data(0)
                    print name
                    if str(name) == "LokalisationsInfo":
                        text_item = items[i]
                        text_item_found = True
                except Exception, e:
                    pass
            
            if not text_item_found:
                text_item = QgsTextAnnotationItem(self.canvas)
                text_item.setData(0, "LokalisationsInfo")

            text_item.setMapPosition(QgsPoint(x+10*self.canvas.mapUnitsPerPixel(), y-10*self.canvas.mapUnitsPerPixel()))
            text_item.setMapPositionFixed(False)
            text_item.setFrameBorderWidth(0.0)   
            text_item.setFrameColor(QColor(250, 250, 250, 255))
            text_item.setFrameBackgroundColor(QColor(250, 250, 250, 123))
            text_item.setFrameSize(QSizeF(250,150))
            text_document = QTextDocument()
            text_document.setHtml("<table style='font-size:12px;'><tr><td>Lok.Name: </td><td>"+lokalisationsname+"</td></tr><tr><td>TID: </td><td>"+str(benannte)+"</td></tr> <tr><td>Num.prinzip: </td><td>"+str(prinzip)+"</td></tr> <tr><td>Attr. prov.: </td><td>"+str(attributeprovisorisch)+"</td></tr> <tr><td>ist offiziell: </td><td>"+str(offiziell)+"</td></tr> <tr><td>Status: </td><td>"+str(status)+"</td></tr> <tr><td>in Aenderung: </td><td>"+str(inaenderung)+"</td></tr> <tr><td>Art: </td><td>"+str(art)+"</td></tr>  </table>")
            text_item.setDocument(text_document)
            
            # This is a workaround: first ever position is not correct.
            # Workaround: das erste Mal passt die Position nicht...???
            text_item.setMapPosition(QgsPoint(x+10*self.canvas.mapUnitsPerPixel(), y-10*self.canvas.mapUnitsPerPixel()))        
            text_item.update()               

            self.iface.mapCanvas().refresh()          

            try:
                vlayer_lokalisationsname.setSelectedFeatures([ids[idx+1]])
            except IndexError:
                self.iface.messageBar().pushMessage("Information",  _translate("VeriSO_EE_Geb_LokTest", "End of table.", None), level=QgsMessageBar.INFO, duration=10)                                                                        

        except Exception, e:
            QApplication.restoreOverrideCursor()            
            exc_type, exc_value, exc_traceback = sys.exc_info()
            self.iface.messageBar().pushMessage("Error", str(traceback.format_exc(exc_traceback)), level=QgsMessageBar.CRITICAL, duration=5)                    
        QApplication.restoreOverrideCursor()      
        QApplication.restoreOverrideCursor()      


    # Return QgsVectorLayer from a layer name ( as string )
    # (c) Carson Farmer / fTools
    def get_vector_layer_by_name(self, myName):
        layermap = QgsMapLayerRegistry.instance().mapLayers()
        for name, layer in layermap.iteritems():
            if layer.type() == QgsMapLayer.VectorLayer and layer.name() == myName:
                if layer.isValid():
                    return layer
                else:
                    return None 
