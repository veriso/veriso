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

    def run(self):        
        self.settings = QSettings("CatAIS","VeriSO")
        project_id = self.settings.value("project/id")
        epsg = self.settings.value("project/epsg")
        
        locale = QSettings().value('locale/userLocale')[0:2] # Für Multilingual-Legenden.

        if not project_id:
            self.iface.messageBar().pushMessage("Error",  _translate("VeriSO_EE_EO_Minimalflaechen", "project_id not set", None), level=QgsMessageBar.CRITICAL, duration=5)                                
            return

        QApplication.setOverrideCursor(Qt.WaitCursor)
        try:
            group = _translate("VeriSO_EE_EO_Minimalflaechen", "EO Flaechenkriterien", None)
            group += " (" + str(project_id) + ")"          
            layer = {}
            layer["type"] = "postgres"
            layer["title"] = _translate("VeriSO_EE_EO_Minimalflaechen","schmale bestockte Fläche > 800 qm", None)
            layer["readonly"] = True 
            layer["featuretype"] = "einzelobjekte_flaechenelement_v"
            layer["geom"] = "geometrie"
            layer["key"] = "ogc_fid"            
            layer["sql"] = "art=24 AND st_area(geometrie) > 800"
            layer["group"] = group
            layer["style"] = "bodenbedeckung/kleiner_wald.qml"
            vlayerWald = self.layer_loader.load(layer)

            Wald = vlayerWald.featureCount()

            QMessageBox.information( None, "Criteres de surface OD", "<b>EO Flaechenkriterien:</b> <br>" 
                                    + "<table>" 
                                   + "<tr> <td>schmale bestockte Flaeche / cordon_boise (>800m2): </td> <td>" + str(Wald) +  "</td> </tr>" 
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
