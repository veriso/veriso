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

class ComplexCheck(QObject):

    def __init__(self, iface):
        self.iface = iface
        
        self.root = QgsProject.instance().layerTreeRoot()        
        self.layerLoader = LoadLayer(self.iface)

    def run(self):        
        self.settings = QSettings("CatAIS","VeriSO")
        project_id = self.settings.value("project/id")
        epsg = self.settings.value("project/epsg")
        
        locale = QSettings().value('locale/userLocale')[0:2] # Für Multilingual-Legenden.

        if not project_id:
            self.iface.messageBar().pushMessage("Error",  _translate("VeriSO_EE_gp_ts", "project_id not set", None), level=QgsMessageBar.CRITICAL, duration=5)                                
            return

        QApplication.setOverrideCursor(Qt.WaitCursor)
        try:
            group = _translate("VeriSO_EE_gp_ts", "Grenzpunkte", None)
            group += " (" + str(project_id) + ")"       
            layer = {}
            layer["type"] = "postgres"
            layer["title"] = _translate("VeriSO_EE_gp_ts", "GP unversichert", None)
            layer["readonly"] = True 
            layer["featuretype"] = "liegenschaften_grenzpunkt"
            layer["geom"] = "geometrie"
            layer["key"] = "ogc_fid"            
            layer["sql"] = "punktzeichen=6"
            layer["group"] = group
            layer["style"] = "liegenschaften/GP_unver.qml"
            vlayerunvGP = self.layerLoader.load(layer)
            unvGP = vlayerunvGP.featureCount()

            layer = {}
            layer["type"] = "postgres"
            layer["title"] = _translate("VeriSO_EE_gp_ts", "GP nicht exakt definiert", None)
            layer["readonly"] = True 
            layer["featuretype"] = "liegenschaften_grenzpunkt"
            layer["geom"] = "geometrie"
            layer["key"] = "ogc_fid"            
            layer["sql"] = "exaktdefiniert=1"
            layer["group"] = group
            layer["style"] = "liegenschaften/GP_exakt.qml"
            vlayerunex = self.layerLoader.load(layer)
            unex = vlayerunex.featureCount()

            layer = {}
            layer["type"] = "postgres"
            layer["title"] = _translate("VeriSO_EE_gp_ts", "GP Zuverlaessigkeit", None)
            layer["readonly"] = True 
            layer["featuretype"] = "liegenschaften_grenzpunkt"
            layer["geom"] = "geometrie"
            layer["key"] = "ogc_fid"            
            layer["sql"] = ""
            layer["group"] = group
            layer["style"] = "liegenschaften/GP_zuv.qml"
            vlayer = self.layerLoader.load(layer)

            layer["type"] = "postgres"
            layer["title"] = _translate("VeriSO_EE_gp_ts", "GP zuv", None)
            layer["readonly"] = True 
            layer["featuretype"] = "liegenschaften_grenzpunkt"
            layer["geom"] = "geometrie"
            layer["key"] = "ogc_fid"            
            layer["sql"] = "lagezuv=1"
            layer["group"] = group
            layer["style"] = ""
            vlayerunzuv = self.layerLoader.load(layer, False, False)
            unzuv = vlayerunzuv.featureCount()

            layer = {}
            layer["type"] = "postgres"
            layer["title"] = _translate("VeriSO_EE_gp_ts", "GP Genauigkeit", None)
            layer["readonly"] = True 
            layer["featuretype"] = "liegenschaften_grenzpunkt"
            layer["geom"] = "geometrie"
            layer["key"] = "ogc_fid"            
            layer["sql"] = ""
            layer["group"] = group
            layer["style"] = "liegenschaften/GP_gen.qml"
            vlayergenGP = self.layerLoader.load(layer)
            genGP = vlayergenGP.featureCount()

            layer = {}
            layer["type"] = "postgres"
            layer["title"] = _translate("VeriSO_EE_gp_ts", "SDR Qualitaet", None)
            layer["readonly"] = True 
            layer["featuretype"] = "liegenschaften_selbstrecht"
            layer["geom"] = "geometrie"
            layer["key"] = "ogc_fid"            
            layer["sql"] = ""
            layer["group"] = group
            layer["style"] = "liegenschaften/sdr_quali.qml"
            vlayersdr = self.layerLoader.load(layer)

            layer = {}
            layer["type"] = "postgres"
            layer["title"] = _translate("VeriSO_EE_gp_ts", "Liegenschaften Qualitaet", None)
            layer["readonly"] = True 
            layer["featuretype"] = "liegenschaften_liegenschaft"
            layer["geom"] = "geometrie"
            layer["key"] = "ogc_fid"            
            layer["sql"] = ""
            layer["group"] = group
            layer["style"] = "liegenschaften/ls_quali.qml"
            vlayerLS = self.layerLoader.load(layer)  

            layer = {}
            layer["type"] = "postgres"
            layer["title"] = _translate("VeriSO_EE_gp_ts", "proj SDR Qualitaet", None)
            layer["readonly"] = True 
            layer["featuretype"] = "liegenschaften_projselbstrecht"
            layer["geom"] = "geometrie"
            layer["key"] = "ogc_fid"            
            layer["sql"] = ""
            layer["group"] = group
            layer["style"] = "liegenschaften/q_proj_sdr.qml"
            vlayerprojsdr = self.layerLoader.load(layer)

            layer = {}
            layer["type"] = "postgres"
            layer["title"] = _translate("VeriSO_EE_gp_ts", "proj Liegenschaften Qualitaet", None)
            layer["readonly"] = True 
            layer["featuretype"] = "liegenschaften_projliegenschaft"
            layer["geom"] = "geometrie"
            layer["key"] = "ogc_fid"            
            layer["sql"] = ""
            layer["group"] = group
            layer["style"] = "liegenschaften/q_proj_ls.qml"
            vlayerprojLS = self.layerLoader.load(layer) 


            layer = {}
            layer["type"] = "postgres"
            layer["title"] = _translate("VeriSO_EE_gp_ts", "GP-Genauigkeiten schlechter AV93-Qalitaet", None)
            layer["readonly"] = True 
            layer["featuretype"] = "z_v_gp_ts"
            layer["geom"] = "geometrie"
            layer["key"] = "ogc_fid"            
            layer["sql"] = "(exaktdefiniert = 0 AND ((art <2  AND lagegen  > 5) OR (art = 2 AND lagegen > 7) OR (art = 3 AND lagegen > 15) OR (art = 4 AND lagegen > 35))) OR (exaktdefiniert = 1 AND ((art <2  AND lagegen  > 20) OR (art = 2 AND lagegen > 35) OR (art = 3 AND lagegen > 75) OR (art = 4 AND lagegen >  150)))"
            layer["group"] = group
            layer["style"] = "liegenschaften/GP_TS_Gen.qml"
            vlayerGP = self.layerLoader.load(layer)

            GP = vlayerGP.featureCount()


            QMessageBox.information( None, "Statistique points limites", "<b>Statistik Grenzpunkte:</b> <br>" 
                                    + "<table>"
+ "<tr> <td>Anzahl GP's/ Nombre PL: </td> <td>" + str(genGP) +  "</td> </tr>" 

                                    + "<tr> <td>Genauigkeit / précision < AV93 / MO93: </td> <td>" + str(GP) +  "</td> </tr>"    
+ "<tr> <td>unzuverlaessige GP's / PL fiabilité insuffisante: </td> <td>" + str(unzuv) +  "</td> </tr>"
                                    + "<tr> <td>unversicherte GP's / PL non matérialisés: </td> <td>" + str(unvGP) +  "</td> </tr>" 
+ "<tr> <td>GP nicht exakt definiert / PL pas défini exactement : </td> <td>" + str(unex) +  "</td> </tr>"
                           + "</table>")



        except Exception:
            QApplication.restoreOverrideCursor()            
            exc_type, exc_value, exc_traceback = sys.exc_info()
            self.iface.messageBar().pushMessage("Error", str(traceback.format_exc(exc_traceback)), level=QgsMessageBar.CRITICAL, duration=5)                    
        QApplication.restoreOverrideCursor()    
