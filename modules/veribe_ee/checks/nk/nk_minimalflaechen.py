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
            self.iface.messageBar().pushMessage("Error",  _translate("VeriSO_EE_nk_minimalflaechen", "project_id not set", None), level=QgsMessageBar.CRITICAL, duration=5)                                
            return

        QApplication.setOverrideCursor(Qt.WaitCursor)
        try:
            group = _translate("VeriSO_EE_nk_minimalflaechen", "Nk Minimalflächen", None)
            group += " (" + str(project_id) + ")" 
         

            layer = {}
            layer["type"] = "postgres"
            layer["title"] = _translate("VeriSO_EE_nk_minimalflaechen",u"NK Mini-Flächen (Punkt)", None)
            layer["readonly"] = True 
            layer["featuretype"] = "z_v_ls_nk_pkt"
            layer["geom"] = "geometrie"
            layer["key"] = "z_ls_nk_pkt_fid"            
            layer["sql"] = "flaeche < 20.00 and flaeche > 0.3"
            layer["group"] = group
            layer["style"] = "nomenklatur/pkt_nk.qml"
            vlayerNKpkt = self.layerLoader.load(layer)


            NK = vlayerNKpkt.featureCount()

            QMessageBox.information( None, "surfaces résiduelles NO par BF", "<b>Kleinflaechen NK pro Liegenschaft:</b> <br>" 
                                    + "<table>" 

                                    + "<tr> <td>Nombre / Anzahl (kleiner/ moins de 20m2): </td> <td>" + str(NK) +  "</td> </tr>"                                
                                    + "</table>")


        except:        
            QApplication.restoreOverrideCursor()
 
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
