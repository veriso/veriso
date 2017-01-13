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
            self.iface.messageBar().pushMessage("Error",  _translate("VeriSO_EE_BB_Minimalflaechen", "project_id not set", None), level=QgsMessageBar.CRITICAL, duration=5)                                
            return

        QApplication.setOverrideCursor(Qt.WaitCursor)
        try:
            group = _translate("VeriSO_EE_BB_Minimalflaechen", "BB Minimalflächen", None)
            group += " (" + str(project_id) + ")"            
            layer = {}
            layer["type"] = "postgres"
            layer["title"] = _translate("VeriSO_EE_BB_Minimalflaechen", "Toleranzstufen", None)
            layer["readonly"] = True 
            layer["featuretype"] = "tseinteilung_toleranzstufe"
            layer["geom"] = "geometrie"
            layer["key"] = "ogc_fid"            
            layer["sql"] = ""
            layer["group"] = group
            layer["style"] = "liegenschaften/TS.qml"
            vlayer = self.layerLoader.load(layer, False, True)
 
            layer = {}
            layer["type"] = "postgres"
            layer["title"] = _translate("VeriSO_EE_BB_Minimalflaechen", "Bodenbedeckungskanten", None)
            layer["readonly"] = True 
            layer["featuretype"] = "bodenbedeckung_boflaeche"
            layer["geom"] = "geometrie"
            layer["key"] = "ogc_fid"            
            layer["sql"] = ""
            layer["group"] = group
            layer["style"] = "bodenbedeckung/bb_kante.qml"
            vlayer = self.layerLoader.load(layer)

            layer = {}
            layer["type"] = "postgres"
            layer["title"] = _translate("VeriSO_EE_BB_Minimalflaechen", "BB-Flächen TS4/TS5 kleiner 2500qm", None)
            layer["readonly"] = True 
            layer["featuretype"] = "z_v_bb_ts"
            layer["geom"] = "geometrie"
            layer["key"] = "ogc_fid"            
            layer["sql"] = "ts_art in(3,4) and bb_art not in (0,3,6,15) and flaeche < 2500"
            layer["group"] = group
            layer["style"] = "bodenbedeckung/kleiner_wald.qml"
            vlayer45 = self.layerLoader.load(layer, False, True)

            layer = {}
            layer["type"] = "postgres"
            layer["title"] = _translate("VeriSO_EE_BB_Minimalflaechen", "BB-Flächen TS3 kleiner 1000qm", None)
            layer["readonly"] = True 
            layer["featuretype"] = "z_v_bb_ts"
            layer["geom"] = "geometrie"
            layer["key"] = "ogc_fid"            
            layer["sql"] = "ts_art=2 and bb_art not in (0,3,6,15) and flaeche < 1000"
            layer["group"] = group
            layer["style"] = "bodenbedeckung/kleiner_wald.qml"
            vlayer3 = self.layerLoader.load(layer, False, True)

            layer = {}
            layer["type"] = "postgres"
            layer["title"] = _translate("VeriSO_EE_BB_Minimalflaechen", "BB-Flächen TS1/TS2 kleiner 100qm", None)
            layer["readonly"] = True 
            layer["featuretype"] = "z_v_bb_ts"
            layer["geom"] = "geometrie"
            layer["key"] = "ogc_fid"            
            layer["sql"] = "ts_art IN (0,1) AND bb_art NOT IN (0,3,6,15) AND flaeche < 100"
            layer["group"] = group
            layer["style"] = "bodenbedeckung/kleiner_wald.qml"
            vlayerklein = self.layerLoader.load(layer, False, True)
           
            layer = {}
            layer["type"] = "postgres"
            layer["title"] = _translate("VeriSO_EE_BB_Minimalflaechen", "Wald kleiner 800qm", None)
            layer["readonly"] = True 
            layer["featuretype"] = "bodenbedeckung_boflaeche"
            layer["geom"] = "geometrie"
            layer["key"] = "ogc_fid"            
            layer["sql"] = "art IN (17,18,19,20) AND st_area(geometrie) < 800"
            layer["group"] = group
            layer["style"] = "bodenbedeckung/kleiner_wald.qml"
            vlayerWald = self.layerLoader.load(layer, False, True)

            layer = {}
            layer["type"] = "postgres"
            layer["title"] = _translate("VeriSO_EE_BB_Minimalflaechen", "Gebäude kleiner 12qm", None)
            layer["readonly"] = True 
            layer["featuretype"] = "bodenbedeckung_boflaeche"
            layer["geom"] = "geometrie"
            layer["key"] = "ogc_fid"            
            layer["sql"] = "art in(0) AND st_area(geometrie) < 12"
            layer["group"] = group
            layer["style"] = "bodenbedeckung/kleiner_wald.qml"
            vlayerGeb = self.layerLoader.load(layer, False, True)

            layer = {}
            layer["type"] = "postgres"
            layer["title"] = _translate("VeriSO_EE_BB_Minimalflaechen", "Wasserbecken kleiner 20qm", None)
            layer["readonly"] = True 
            layer["featuretype"] = "bodenbedeckung_boflaeche"
            layer["geom"] = "geometrie"
            layer["key"] = "ogc_fid"            
            layer["sql"] = "art IN (6) AND st_area(geometrie) < 20"
            layer["group"] = group
            layer["style"] = "bodenbedeckung/kleiner_wald.qml"
            vlayerWb = self.layerLoader.load(layer, False, True)

            layer = {}
            layer["type"] = "postgres"
            layer["title"] = _translate("VeriSO_EE_BB_Minimalflaechen", "BB-Flächen kleiner 10qm pro LS", None)
            layer["readonly"] = True 
            layer["featuretype"] = "z_v_bb_ls"
            layer["geom"] = "geometrie"
            layer["key"] = "ogc_fid"            
            layer["sql"] = "art<26 and art>0 AND flaeche>.1 and flaeche <10"
            layer["group"] = group
            layer["style"] = "bodenbedeckung/kleiner_wald.qml"
            vlayerBB = self.layerLoader.load(layer)


            TS1 = vlayerklein.featureCount()
            TS3 = vlayer3.featureCount()
            TS4 = vlayer45.featureCount()
            Geb = vlayerGeb.featureCount()
            Wb = vlayerWb.featureCount()
            Wald = vlayerWald.featureCount()
            BB = vlayerBB.featureCount()

            QMessageBox.information( None, "Surfaces plus petites que criteres de surface", "<b>Flaechen unterhalb Flaechenkriterien:</b> <br>" 
                                    + "<table>" 
				    + "<tr> <td>BB pro LS / CS par BF (10m2): </td> <td>" + str(BB) +  "</td> </tr>"
                                    + "<tr> <td>Wasserbecken /bassin (20m2): </td> <td>" + str(Wb) +  "</td> </tr>"                                + "<tr> <td>Gebaeude / batiment (12m2): </td> <td>" + str(Geb) +  "</td> </tr>"                                + "<tr> <td>Wald / foret (800m2): </td> <td>" + str(Wald) +  "</td> </tr>" 
                                    + "<tr> <td>TS 1/2 / NT 1/2 (100m2) : </td> <td>" + str(TS1) +  "</td> </tr>" 
                                    + "<tr> <td>TS 3 / NT 3 (1000m2): </td> <td>" + str(TS3) +  "</td> </tr>" 
                                    + "<tr> <td>TS 4/5  / NT 4/5 (2500m2): </td> <td>" + str(TS4) +  "</td> </tr>" 
                                    + "</table>")

        except Exception:
            QApplication.restoreOverrideCursor()            
            exc_type, exc_value, exc_traceback = sys.exc_info()
            self.iface.messageBar().pushMessage("Error", str(traceback.format_exc(exc_traceback)), level=QgsMessageBar.CRITICAL, duration=5)                    
        QApplication.restoreOverrideCursor()          



#        eingangOhneLokalisation = vlayerEingangOhneLokalisation.featureCount()
#        lokalisationsNameOhneEingang = vlayerLokalisationsNameOhneEingang.featureCount()
#        strassenstueckLinieIstAchse = vlayerStrassenstueckLinieIstAchse.featureCount()
#
#        QMessageBox.information( None, "Statistik Einzelobjekte", "<b>Statistik Einzelobjekte:</b> <br>" 
#                                + "<table>" 
#                                + u"<tr> <td>Mast_Leitung als Fläche: </td> <td>" + str(mastLeitungFlaeche) +  "</td> </tr>" 
#                                + u"<tr> <td>schmaler_Weg als Fläche: </td> <td>" + str(schmalerWegFlaeche) +  "</td> </tr>" 
#                                + "<tr> <td>Fahrspur als Linie: </td> <td>" + str(fahrspurLinie) +  "</td> </tr>" 
#                                + "</table>")
