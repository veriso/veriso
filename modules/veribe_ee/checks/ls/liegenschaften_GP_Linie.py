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
            self.iface.messageBar().pushMessage("Error",  _translate("VeriSO_EE_liegenschaften_GP_Linie", "project_id not set", None), level=QgsMessageBar.CRITICAL, duration=5)                                
            return

        QApplication.setOverrideCursor(Qt.WaitCursor)
        try:
            group = _translate("VeriSO_EE_liegenschaften_GP_Linie", "GP ausserhalb", None)
            group += " (" + str(project_id) + ")"         
            layer = {}
            layer["type"] = "postgres"
            layer["title"] = _translate("VeriSO_EE_liegenschaften_GP_Linie", "GP's ausserhalb Grenzlinien", None)
            layer["readonly"] = True 
            layer["featuretype"] = "z_grenzen"
            layer["geom"] = "geometrie"
            layer["key"] = "ogc_fid"            
            layer["sql"] = ""
            layer["group"] = group
            layer["style"] = "liegenschaften/GP_ausserhalb.qml"
#            layer["style"] = "gebaeudeadressen/lokalisationsnamepos_newlabel_"+_locale+".qml"
            vlayerGP = self.layerLoader.load(layer)

            GP = vlayerGP.featureCount()

            QMessageBox.information( None, u"Points limites pas sur la limite", "<b>Grenzpunkte nicht auf Grenzlinie:</b> <br>" 
                                    + "<table>" 
                                    + "<tr> <td>Anzahl / Nombre: </td> <td>" + str(GP) +  "</td> </tr>" 
                                    + "</table>")
  
#            layer = {}
#            layer["type"] = "wms"
#            layer["url"] = "http://wms.geo.admin.ch/"
#            layer["layers"] = "ch.bfs.gebaeude_wohnungs_register"
#            layer["crs"] = "EPSG:21781"
#            layer["format"] = "image/png"
#            layer["title"] = "GWR"
#            layer["group"] = group
#            vlayerGWR = self.layerLoader.load(layer)


            
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
