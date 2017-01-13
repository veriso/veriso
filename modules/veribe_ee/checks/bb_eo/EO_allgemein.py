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
            self.iface.messageBar().pushMessage("Error",  _translate("VeriSO_EE_EO_allgemein", "project_id not set", None), level=QgsMessageBar.CRITICAL, duration=5)                                
            return

        QApplication.setOverrideCursor(Qt.WaitCursor)
        try:
            group = _translate("VeriSO_EE_EO_allgemein", "EO Allgemein", None)
            group += " (" + str(project_id) + ")"
           
            layer = {}
            layer["type"] = "postgres"
            layer["title"] = _translate("VeriSO_EE_EO_allgemein", "EO Flaechenelemete", None)
            layer["readonly"] = True
            layer["featuretype"] = "einzelobjekte_flaechenelement_v"
            layer["geom"] = "geometrie"
            layer["key"] = "ogc_fid"
            layer["group"] = group
            layer["sql"] = ""
            layer["style"] = "bodenbedeckung/eo_fl.qml"
            vlayer = self.layerLoader.load(layer, False, True)     
            layer = {}
            layer["type"] = "postgres"
            layer["title"] = _translate("VeriSO_EE_EO_allgemein", "EO Linienelemente", None)
            layer["readonly"] = True
            layer["featuretype"] = "einzelobjekte_linienelement_v"
            layer["geom"] = "geometrie"
            layer["key"] = "ogc_fid"
            layer["group"] = group
            layer["sql"] = ""
            layer["style"] = "bodenbedeckung/eo_li.qml"
            vlayer = self.layerLoader.load(layer, False, True)
            layer = {}
            layer["type"] = "postgres"
            layer["title"] = _translate("VeriSO_EE_EO_allgemein", "EO Punktelemente", None)
            layer["readonly"] = True
            layer["featuretype"] = "einzelobjekte_punktelement_v"
            layer["geom"] = "geometrie"
            layer["key"] = "ogc_fid"
            layer["group"] = group
            layer["sql"] = ""
            layer["style"] = "bodenbedeckung/eo_pkt.qml"
            vlayer = self.layerLoader.load(layer, False, True)
            layer = {}
            layer["type"] = "postgres"
            layer["title"] = _translate("VeriSO_EE_EO_allgemein", "Objektname", None)
            layer["readonly"] = True
            layer["featuretype"] = "einzelobjekte_objektnamepos_v"
            layer["geom"] = "pos"
            layer["key"] = "ogc_fid"
            layer["group"] = group
            layer["sql"] = ""
            layer["style"] = "bodenbedeckung/objektnamen.qml"
            vlayer = self.layerLoader.load(layer, False, True)  
            layer = {}
            layer["type"] = "postgres"
            layer["title"] = _translate("VeriSO_EE_EO_allgemein", "BEGID (EO)", None)
            layer["readonly"] = True
            layer["featuretype"] = "z_objektnummer_pos"
            layer["key"] = "ogc_fid"
            layer["group"] = group
            layer["geom"] = "pos"
            layer["sql"] = ""
            layer["style"] = "gebaeudeadressen/BEGIDeo.qml"
            vlayer = self.layerLoader.load(layer, False, True)
 
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
#                                + """)



