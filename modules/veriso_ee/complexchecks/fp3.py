 # -*- coding: utf-8 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *

import sys
import traceback

from veriso.base.utils.doLoadLayer import LoadLayer

class ComplexCheck(QObject):

    def __init__(self, iface):
        self.iface = iface
        
        self.root = QgsProject.instance().layerTreeRoot()        
        self.layerLoader = LoadLayer(self.iface)

    # Hier (also beim Laden des Layers in QGIS) machen die Umlaute extreme Probleme.
    # Das scheint eine Lösung zu sein. Im Gegensatz zu anderen "tr"-Methoden, ist sie
    # bisschen komplizierter.
    def tr(self, message):
        _encoding = QCoreApplication.UnicodeUTF8
        return QCoreApplication.translate('VeriSOModule.veriso_ee.fp3', message.decode('utf-8'), encoding=_encoding)

    def run(self):        
        self.settings = QSettings("CatAIS","VeriSO")
        project_id = self.settings.value("project/id")
        epsg = self.settings.value("project/epsg")
        
        if not project_id:
            self.iface.messageBar().pushMessage("Error",  self.tr("project_id not set"), level=QgsMessageBar.CRITICAL, duration=5)                                
            return

        QApplication.setOverrideCursor(Qt.WaitCursor)
        try:
            group = self.tr("FixpunkteKategorie3")
            group += " (" + str(project_id) + ")"
            
            layer = {}
            layer["type"] = "postgres"
            layer["title"] = self.tr("Toleranzstufen") # Mit Linguist übersetzen. Deutsche Übersetzugn nicht unbedingt nötig, da dieser Text hier verwendet wird, falls die Übersetzung für eine bestimmte Sprache fehlt.
            layer["featuretype"] = "tseinteilung_toleranzstufe"
            layer["geom"] = "geometrie"
            layer["key"] = "ogc_fid"            
            layer["sql"] = ""
            layer["readonly"] = True
            layer["group"] = group
            layer["style"] = "tseinteilung/toleranzstufe.qml"
            
            # Die Sichtbarkeit des Layer und ob die Legende
            # und die Gruppe zusammengeklappt sein sollen:
            # self.layerLoader.load(layer, True, True, True)
            # Legende = vorletztes True (default is False)
            # Gruppe = letztes True (default is False)
            # Sichtbarkeit des Layers = erstes True (default is True)
            vlayer = self.layerLoader.load(layer)
            
            layer = {}
            layer["type"] = "postgres"
            layer["title"] = self.tr("LFP3 Nachführung") # Mit Linguist übersetzen. -> Achtung: Testen ob Übersetzungen mit Umlauten funktionieren...
            layer["featuretype"] = "fixpunktekategorie3_lfp3nachfuehrung"
            layer["geom"] = "perimeter" # Falls layer["geom"] bei Tabellen/Layern mit einer Geomtriespalte weggelassen wird, wird die Tabelle als "geometryless" geladen.
            layer["key"] = "ogc_fid"            
            layer["sql"] = ""
            layer["readonly"] = True            
            layer["group"] = group
            
            vlayer = self.layerLoader.load(layer, False, True)            
            
            layer = {}
            layer["type"] = "postgres"
            layer["title"] = self.tr("LFP3")
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
            layer["title"] = self.tr("LFP3 ausserhalb Gemeinde")
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
            layer["title"] = self.tr("Gemeindegrenze")
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
