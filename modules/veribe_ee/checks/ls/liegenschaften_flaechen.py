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
            self.iface.messageBar().pushMessage("Error",  _translate("VeriSO_EE_liegenschaften_flaechen", "project_id not set", None), level=QgsMessageBar.CRITICAL, duration=5)                                
            return

        QApplication.setOverrideCursor(Qt.WaitCursor)
        try:
            group = _translate("VeriSO_EE_liegenschaften_flaechen", u"Flächendifferenzen", None)
            group += " (" + str(project_id) + ")"
            layer = {}
            layer["type"] = "postgres"
            layer["title"] = _translate("VeriSO_EE_liegenschaften_flaechen",u"Liegenschaften mit Flächendifferenzen", None)
            layer["readonly"] = True 
            layer["featuretype"] = "z_liegenschaft_flaeche"
            layer["geom"] = "geometrie"
            layer["key"] = "ogc_fid"            
#            layer["sql"] = "((st_area(geometrie)+0.55 < flaechenmass) or st_area(geometrie)-0.55 > flaechenmass)"
            layer["sql"] = ""
            layer["group"] = group
            layer["style"] = "liegenschaften/ls_flaechen.qml"
#            layer["style"] = "gebaeudeadressen/lokalisationsnamepos_newlabel_"+_locale+".qml"
            vlayerLS = self.layerLoader.load(layer)     

            layer = {}
            layer["type"] = "postgres"
            layer["title"] = _translate("VeriSO_EE_liegenschaften_flaechen","Selbstrecht mit Flaechendifferenzen", None)
            layer["readonly"] = True 
            layer["featuretype"] = "z_selbstrecht_flaeche"
            layer["geom"] = "geometrie"
            layer["key"] = "ogc_fid"            
#            layer["sql"] = "((st_area(geometrie)+0.55 < flaechenmass) or st_area(geometrie)-0.55 > flaechenmass)"
            layer["sql"] = ""
            layer["group"] = group
            layer["style"] = "liegenschaften/ls_flaechen.qml"
#            layer["style"] = "gebaeudeadressen/lokalisationsnamepos_newlabel_"+_locale+".qml"
            vlayer3 = self.layerLoader.load(layer, False, True)      
           
            layer = {}
            layer["type"] = "postgres"
            layer["title"] = _translate("VeriSO_EE_liegenschaften_flaechen","GRUDIS-LS-Aufruf", None)
            layer["readonly"] = True 
            layer["featuretype"] = "liegenschaften_liegenschaft_v2"
            layer["geom"] = "geometrie"
            layer["key"] = "ogc_fid"            
            layer["sql"] = ""
            layer["group"] = group
            layer["style"] = "liegenschaften/grudis.qml"
#            layer["style"] = "gebaeudeadressen/lokalisationsnamepos_newlabel_"+_locale+".qml"
            vlayerGRUDIS = self.layerLoader.load(layer)  


#            LS = vlayerLS.featureCount()
#           TS3 = vlayer3.featureCount()
#
#
 #           QMessageBox.information( None, u"diffèrences de surface", "<b>Flaechendifferenzen:</b> <br>" 
  #                                  + "<table>" 
   #                                     + "<tr> <td>Nombre BF / Anzahl LS: </td> <td>" + str(LS) +  "</td> </tr>" 
    #                                + "<tr> <td>Nombre DDP / Anzahl SDR: </td> <td>" + str(TS3) +  "</td> </tr>" 
#
#
 #                                   + "</table>")

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
