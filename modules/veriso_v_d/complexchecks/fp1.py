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
        
        self.root = QgsProject.instance().layerTreeRoot()        
        self.layer_loader = LoadLayer(self.iface)

    def run(self):        
        self.settings = QSettings("CatAIS","VeriSO")
        project_id = self.settings.value("project/id")
        epsg = self.settings.value("project/epsg")
        
        locale = QSettings().value('locale/userLocale')[0:2] # this is for multilingual legends
        
        # If locale is different to frence or italian, german will be used.
        # Otherwise we get into troubles with the legends, e.g. locale = "en" but 
        # there is no english legend (qml file).
        if locale == "fr":
            pass
        elif locale == "it":
            pass
        else:
            locale = "de"

        if not project_id:
            self.iface.messageBar().pushMessage("Error",  _translate("VeriSO_V+D_FP1", "project_id not set", None), level=QgsMessageBar.CRITICAL, duration=5)                                
            return

        QApplication.setOverrideCursor(Qt.WaitCursor)
        try:
            group = _translate("VeriSO_V+D_FP1", "FixpunkteKategorie1", None)
            group += " (" + str(project_id) + ")"
            
            # Lagefixpunkte 1
             
            layer = {}
            layer["type"] = "postgres"
            layer["title"] = _translate("VeriSO_V+D_FP1", "LFP1 Nachführung", None)
            layer["featuretype"] = "fixpunktekategorie1_lfp1nachfuehrung"
            layer["geom"] = "perimeter" # If no geometry attribute is set, the layer will be loaded as geoemtryless.
            layer["key"] = "ogc_fid"            
            layer["sql"] = ""
            layer["readonly"] = True            
            layer["group"] = group
            
            # Visibility and if legend and/or groupd should be collapsed can
            # be set with parameters in the self.layer_loader.load()
            # method:
            # load(layer, visibility=True, collapsed_legend=False, collapsed_group=False)
            vlayer_lfp1_nf = self.layer_loader.load(layer, False, True)            
            
            layer = {}
            layer["type"] = "postgres"
            layer["title"] = _translate("VeriSO_V+D_FP1", "LFP1", None)
            layer["featuretype"] = "fixpunktekategorie1_lfp1"
            layer["geom"] = "geometrie"
            layer["key"] = "ogc_fid"            
            layer["sql"] = ""
            layer["readonly"] = True            
            layer["group"] = group
            layer["style"] = "fixpunkte/lfp2.qml"
    
            vlayer_lfp1 = self.layer_loader.load(layer)
            
            # Join two layers (lfp1 and lfp1nachfuehrung)
            lfp1_field = "entstehung"
            lfp1_nf_field = "ogc_fid"
            join_obj = QgsVectorJoinInfo()
            join_obj.joinLayerId = vlayer_lfp1_nf.id()
            join_obj.joinFieldName = lfp1_nf_field
            join_obj.targetFieldName = lfp1_field
            join_obj.memoryCache = True
            join_obj.prefix = "lfp1_nf_"
            vlayer_lfp1.addJoin(join_obj)
            
            # This is how WMS layer work.
            layer = {}
            layer["type"] = "wms"
            layer["title"] = _translate("VeriSO_V+D_FP1", "LFP1 Schweiz (WMS)", None)
            layer["url"] = "http://wms.geo.admin.ch/"
            layer["layers"] = "ch.swisstopo.fixpunkte-lfp1"
            layer["format"] = "image/png"          
            layer["crs"] = "EPSG:" + str(epsg)
            layer["group"] = group

            vlayer = self.layer_loader.load(layer, False, True)
            
            # Höhenfixpunkte 1
            layer = {}
            layer["type"] = "postgres"
            layer["title"] = _translate("VeriSO_V+D_FP1", "HFP1 Nachführung", None)
            layer["featuretype"] = "fixpunktekategorie1_hfp1nachfuehrung"
            layer["geom"] = "perimeter"
            layer["key"] = "ogc_fid"            
            layer["sql"] = ""
            layer["readonly"] = True            
            layer["group"] = group
            
            vlayer_hfp1_nf = self.layer_loader.load(layer, False, True)            
            
            layer = {}
            layer["type"] = "postgres"
            layer["title"] = _translate("VeriSO_V+D_FP1", "HFP1", None)
            layer["featuretype"] = "fixpunktekategorie1_hfp1"
            layer["geom"] = "geometrie"
            layer["key"] = "ogc_fid"            
            layer["sql"] = ""
            layer["readonly"] = True            
            layer["group"] = group
            layer["style"] = "fixpunkte/hfp2.qml"
    
            vlayer_hfp1 = self.layer_loader.load(layer)

            # Join two layers (hfp1 and hfp1nachfuehrung)
            hfp1_field = "entstehung"
            hfp1_nf_field = "ogc_fid"
            join_obj = QgsVectorJoinInfo()
            join_obj.joinLayerId = vlayer_hfp1_nf.id()
            join_obj.joinFieldName = hfp1_nf_field
            join_obj.targetFieldName = hfp1_field
            join_obj.memoryCache = True
            join_obj.prefix = "hfp1_nf_"
            vlayer_hfp1.addJoin(join_obj)

            layer = {}
            layer["type"] = "wms"
            layer["title"] = _translate("VeriSO_V+D_FP1", "HFP1 Schweiz (WMS)", None)
            layer["url"] = "http://wms.geo.admin.ch/"
            layer["layers"] = "ch.swisstopo.fixpunkte-hfp1"
            layer["format"] = "image/png"          
            layer["crs"] = "EPSG:" + str(epsg)
            layer["group"] = group

            vlayer = self.layer_loader.load(layer, False, True)

            # Business as usual: Gemeindegrenzen
            layer = {}
            layer["type"] = "postgres"
            layer["title"] = _translate("VeriSO_V+D_FP1", "Gemeindegrenze", None)
            layer["featuretype"] = "gemeindegrenzen_gemeindegrenze"
            layer["geom"] = "geometrie"
            layer["key"] = "ogc_fid"            
            layer["sql"] = ""
            layer["readonly"] = True
            layer["group"] = group
            layer["style"] = "gemeindegrenze/gemgre_strichliert.qml"

            gemgrelayer = self.layer_loader.load(layer)

            # Change map extent.
            # Bug (?) in QGIS: http://hub.qgis.org/issues/10980
            # Closed for the lack of feedback. Upsi...
            # Still a problem? (sz / 2015-04-12)
            if gemgrelayer:
                rect = gemgrelayer.extent()
                rect.scale(5)
                self.iface.mapCanvas().setExtent(rect)        
                self.iface.mapCanvas().refresh() 
            # Sometimes it does make much more sense
            # to zoom to maximal extent:
            # self.iface.mapCanvas().zoomToFullExtent()
            
                
        except Exception:
            QApplication.restoreOverrideCursor()            
            exc_type, exc_value, exc_traceback = sys.exc_info()
            self.iface.messageBar().pushMessage("Error", str(traceback.format_exc(exc_traceback)), level=QgsMessageBar.CRITICAL, duration=5)                    
        QApplication.restoreOverrideCursor()
