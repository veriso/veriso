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
            self.iface.messageBar().pushMessage("Error",  _translate("VeriSO_EE_Hoheitsgrenze_GP_Linie", "project_id not set", None), level=QgsMessageBar.CRITICAL, duration=5)                                
            return

        QApplication.setOverrideCursor(Qt.WaitCursor)
        try:
            group = _translate("VeriSO_EE_Hoheitsgrenze_GP_Linie", "GP aussherhalb", None)
            group += " (" + str(project_id) + ")"           
            layer = {}
            layer["type"] = "postgres"
            layer["title"] = _translate("VeriSO_EE_Hoheitsgrenze_GP_Linie","HGP's ausserhalb Grenzlinien", None)
            layer["readonly"] = True 
            layer["featuretype"] = "z_hgp_ls_linie"
            layer["geom"] = "geometrie"
            layer["key"] = "ogc_fid"            
            layer["sql"] = ""
            layer["group"] = group
            layer["style"] = "liegenschaften/GP_ausserhalb.qml"
#            layer["style"] = "gebaeudeadressen/lokalisationsnamepos_newlabel_"+_locale+".qml"
            vlayerHGP = self.layerLoader.load(layer)            
            
            HGP = vlayerHGP.featureCount()

            QMessageBox.information( None, "PL territoriale pas sur limite de commune ", "<b>HGP nicht auf Gemeindegrenze:</b> <br>" 
                                    + "<table>" 
                                    + "<tr> <td>Nombre / Anzahl: </td> <td>" + str(HGP) +  "</td> </tr>" 
                                    + "</table>")
  
        except Exception:
            QApplication.restoreOverrideCursor()            
            exc_type, exc_value, exc_traceback = sys.exc_info()
            self.iface.messageBar().pushMessage("Error", str(traceback.format_exc(exc_traceback)), level=QgsMessageBar.CRITICAL, duration=5)                    
        QApplication.restoreOverrideCursor() 
