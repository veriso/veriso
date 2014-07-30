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


#        locale = QSettings().value('locale/userLocale')[0:2]
#        locale_path = os.path.join(
#            self.plugin_dir,
#            'i18n',
#            'veriso_{}.qm'.format(locale))
#
#        if os.path.exists(locale_path):
#            self.translator = QTranslator()
#            self.translator.load(locale_path)
#
#            if qVersion() > '4.3.3':
#                QCoreApplication.installTranslator(self.translator)

    # Hier (also beim Laden des Layers in QGIS) machen die Umlaute extreme Probleme.
    # Das scheint eine Lösung zu sein. Im Gegensatz zu anderen "tr"-Methoden, ist sie
    # bisschen komplizierter.
    def tr(self, message):
        _encoding = QCoreApplication.UnicodeUTF8
        return QCoreApplication.translate('VeriSO_EE_FP3', message.decode('utf-8'), encoding=_encoding)

    def run(self):        
        self.settings = QSettings("CatAIS","VeriSO")
        project_id = self.settings.value("project/id")
        epsg = self.settings.value("project/epsg")
        
        locale = QSettings().value('locale/userLocale')[0:2] # Für Multilingual-Legenden.

        if not project_id:
            self.iface.messageBar().pushMessage("Error",  _translate("VeriSO_EE_FP3", "project_id not set", None), level=QgsMessageBar.CRITICAL, duration=5)                                
            return

        QApplication.setOverrideCursor(Qt.WaitCursor)
        try:
            group = _translate("VeriSO_EE_FP3", "FixpunkteKategorie3", None)
            group += " (" + str(project_id) + ")"
            
            layer = {}
            layer["type"] = "postgres"
            layer["title"] = _translate("VeriSO_EE_FP3", "Toleranzstufen", None) # Mit Linguist übersetzen. Deutsche Übersetzugn nicht unbedingt nötig, da dieser Text hier verwendet wird, falls die Übersetzung für eine bestimmte Sprache fehlt.
            layer["featuretype"] = "tseinteilung_toleranzstufe"
            layer["geom"] = "geometrie"
            layer["key"] = "ogc_fid"            
            layer["sql"] = ""
            layer["readonly"] = True
            layer["group"] = group
            layer["style"] = "tseinteilung/toleranzstufe_"+locale+".qml"
            
            # Die Sichtbarkeit des Layer und ob die Legende
            # und die Gruppe zusammengeklappt sein sollen:
            # self.layerLoader.load(layer, True, True, True)
            # Legende = vorletztes True (default is False)
            # Gruppe = letztes True (default is False)
            # Sichtbarkeit des Layers = erstes True (default is True)
            vlayer = self.layerLoader.load(layer)
            
            layer = {}
            layer["type"] = "postgres"
#            layer["title"] = self.tr("LFP3 Nachführung") # Mit Linguist übersetzen. -> Achtung: Testen ob Übersetzungen mit Umlauten funktionieren...
            layer["title"] = _translate("VeriSO_EE_FP3", "LFP3 Nachführung", None)
            layer["featuretype"] = "fixpunktekategorie3_lfp3nachfuehrung"
            layer["geom"] = "perimeter" # Falls layer["geom"] bei Tabellen/Layern mit einer Geomtriespalte weggelassen wird, wird die Tabelle als "geometryless" geladen.
            layer["key"] = "ogc_fid"            
            layer["sql"] = ""
            layer["readonly"] = True            
            layer["group"] = group
            
            vlayer = self.layerLoader.load(layer, False, True)            
            
            layer = {}
            layer["type"] = "postgres"
            layer["title"] = _translate("VeriSO_EE_FP3", "LFP3", None)
            layer["featuretype"] = "fixpunktekategorie3_lfp3"
            layer["geom"] = "geometrie"
            layer["key"] = "ogc_fid"            
            layer["sql"] = ""
            layer["readonly"] = True            
            layer["group"] = group
            layer["style"] = "fixpunkte/lfp3.qml"

            vlayer = self.layerLoader.load(layer)
            
            layer = {}
            layer["type"] = "postgres"
            layer["title"] = _translate("VeriSO_EE_FP3", "LFP3 ausserhalb Gemeinde", None)
            layer["featuretype"] = "v_lfp3_ausserhalb_gemeinde"
            layer["geom"] = "geometrie"
            layer["key"] = "ogc_fid"            
            layer["sql"] = ""
            layer["readonly"] = True            
            layer["group"] = group
            layer["style"] = "fixpunkte/lfp3ausserhalb.qml"
            
            vlayer = self.layerLoader.load(layer)

            layer = {}
            layer["type"] = "postgres"
            layer["title"] = _translate("VeriSO_EE_FP3", "Gemeindegrenze", None)
            layer["featuretype"] = "gemeindegrenzen_gemeindegrenze"
            layer["geom"] = "geometrie"
            layer["key"] = "ogc_fid"            
            layer["sql"] = ""
            layer["readonly"] = True
            layer["group"] = group
            layer["style"] = "gemeindegrenze/gemgre_strichliert.qml"

            gemgrelayer = self.layerLoader.load(layer)

            # Kartenausschnit verändern. 
            # Bug (?) in QGIS: http://hub.qgis.org/issues/10980
            if gemgrelayer:
                rect = gemgrelayer.extent()
                rect.scale(5)
                self.iface.mapCanvas().setExtent(rect)        
                self.iface.mapCanvas().refresh() 
            # Bei gewissen Fragestellungen sicher sinnvoller
            # auf den ganzen Kartenausschnitt zu zoomen:
            # self.iface.mapCanvas().zoomToFullExtent()
            
                
        except Exception, e:
            QApplication.restoreOverrideCursor()            
            exc_type, exc_value, exc_traceback = sys.exc_info()
            self.iface.messageBar().pushMessage("Error", str(traceback.format_exc(exc_traceback)), level=QgsMessageBar.CRITICAL, duration=5)                    
        QApplication.restoreOverrideCursor()      

        # Geometryless Bug scheint behoben.
        # Falscher EPSG-Code und falsche 
        # Scale-Unit waren eingestellt, falls
        # der erste geladene Layer OHNE
        # Geometrie war.
        # Habe es mit LFP3Nachfuehrung 
        # OHNE "geom" getestet.
        # Workaround war notwendig.
