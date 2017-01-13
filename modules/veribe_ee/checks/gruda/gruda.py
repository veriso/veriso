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
            self.iface.messageBar().pushMessage("Error",  _translate("VeriSO_EE_gruda", "project_id not set", None), level=QgsMessageBar.CRITICAL, duration=5)                                
            return

        QApplication.setOverrideCursor(Qt.WaitCursor)
        try:
            group1 = _translate("VeriSO_EE_gruda", "Planeinteilung", None)
            group1 += " (" + str(project_id) + ")" 

            group2 = _translate("VeriSO_EE_gruda", "Bodenbedeckung", None)
            group2 += " (" + str(project_id) + ")" 

            group3 = _translate("VeriSO_EE_gruda", "Liegenschaften", None)
            group3 += " (" + str(project_id) + ")" 

            group4 = _translate("VeriSO_EE_gruda", "Adressen", None)
            group4 += " (" + str(project_id) + ")" 

            group5 = _translate("VeriSO_EE_gruda", "Fixpunkte", None)
            group5 += " (" + str(project_id) + ")" 

            layer = {}
            layer["type"] = "postgres"
            layer["title"] = _translate("VeriSO_EE_gruda","Bodenbedeckung", None)
            layer["readonly"] = True 
            layer["featuretype"] = "bodenbedeckung_boflaeche"
            layer["key"] = "ogc_fid"
            layer["geom"] = "geometrie"
            layer["sql"] = ""
            layer["group"] = group2
            layer["style"] = "bodenbedeckung/bb.qml"
            vlayerBB = self.layerLoader.load(layer)


            layer = {}
            layer["type"] = "postgres"
            layer["title"] = _translate("VeriSO_EE_gruda","BEGID (BB)", None)
            layer["readonly"] = True
            layer["featuretype"] = "z_gebaeudenummer_pos"
            layer["key"] = "ogc_fid"
            layer["group"] = group2
            layer["geom"] = "pos"
            layer["sql"] = ""
            layer["style"] = "gebaeudeadressen/BEGIDeo.qml"
            vlayer = self.layerLoader.load(layer, False, True)

  
            layer = {}
            layer["type"] = "postgres"
            layer["title"] = _translate("VeriSO_EE_gruda","BEGID (EO)", None)
            layer["readonly"] = True
            layer["featuretype"] = "z_objektnummer_pos"
            layer["key"] = "ogc_fid"
            layer["group"] = group2
            layer["geom"] = "pos"
            layer["sql"] = ""
            layer["style"] = "gebaeudeadressen/BEGIDeo.qml"
            vlayer = self.layerLoader.load(layer, False, True)



            layer = {}
            layer["type"] = "postgres"
            layer["title"] = _translate("VeriSO_EE_gruda","Plangeometrie", None)
            layer["readonly"] = True 
            layer["featuretype"] = "planeinteilungen_plan_v"
            layer["geom"] = "geometrie"
            layer["key"] = "ogc_fid"            
            layer["sql"] = ""
            layer["group"] = group1
            layer["style"] = "planeinteilung/plangeometrie.qml"
            vlayer = self.layerLoader.load(layer, False, True)


            layer = {}
            layer["type"] = "postgres"
            layer["title"] = _translate("VeriSO_EE_gruda","Flurnamen", None)
            layer["readonly"] = True 
            layer["featuretype"] = "nomenklatur_flurname"
            layer["geom"] = "geometrie"
            layer["key"] = "ogc_fid"            
            layer["sql"] = ""
            layer["group"] = group1
            layer["style"] = "nomenklatur/nomenklatur.qml"
            vlayer = self.layerLoader.load(layer, False, True)


            layer = {}
            layer["type"] = "postgres"
            layer["title"] = _translate("VeriSO_EE_gruda","PlanPos", None)
            layer["readonly"] = True
            layer["featuretype"] = "planeinteilungen_plan_v"
            layer["geom"] = "geometrie"
            layer["key"] = "ogc_fid"            
            layer["sql"] = ""
            layer["group"] = group1
            layer["style"] = "planeinteilung/planpos.qml"
            vlayer = self.layerLoader.load(layer, False, True)

            layer = {}
            layer["type"] = "postgres"
            layer["title"] = _translate("VeriSO_EE_gruda","Gemeindegrenze", None)
            layer["readonly"] = True 
            layer["featuretype"] = "gemeindegrenzen_gemeindegrenze"
            layer["geom"] = "geometrie"
            layer["key"] = "ogc_fid"
            layer["sql"] = ""
            layer["group"] = group3
            layer["style"] = "gemeindegrenze/gemeindegrenze.qml"
            vlayer = self.layerLoader.load(layer, False, True)


            layer = {}
            layer["type"] = "postgres"
            layer["title"] = _translate("VeriSO_EE_gruda","Grundstueck", None)
            layer["readonly"] = True 
            layer["featuretype"] = "liegenschaften_grundstueck"
            layer["key"] = "ogc_fid"
            layer["sql"] = ""
            layer["group"] = group3
            vlayerGSTab = self.layerLoader.load(layer)

            layer = {}
            layer["type"] = "postgres"
            layer["title"] = _translate("VeriSO_EE_gruda","proj. SDR", None)
            layer["readonly"] = True 
            layer["featuretype"] = "liegenschaften_projselbstrecht"
            layer["geom"] = "geometrie"
            layer["key"] = "ogc_fid"
            layer["sql"] = ""
            layer["group"] = group3
            layer["style"] = "liegenschaften/projselbstrecht.qml"
            vlayerprojSDR = self.layerLoader.load(layer)

            layer = {}
            layer["type"] = "postgres"
            layer["title"] = _translate("VeriSO_EE_gruda","SDR", None)
            layer["readonly"] = True
            layer["featuretype"] = "liegenschaften_selbstrecht"
            layer["geom"] = "geometrie"
            layer["key"] = "ogc_fid"
            layer["sql"] = ""
            layer["group"] = group3
            layer["style"] = "liegenschaften/selbstrecht.qml"
            vlayer = self.layerLoader.load(layer, False, True)


            layer = {}
            layer["type"] = "postgres"
            layer["title"] = _translate("VeriSO_EE_gruda","proj. Liegenschaften", None)
            layer["readonly"] = True
            layer["featuretype"] = "liegenschaften_projliegenschaft"
            layer["geom"] = "geometrie"
            layer["key"] = "ogc_fid"
            layer["group"] = group3
            layer["sql"] = ""
            layer["style"] = "liegenschaften/projliegenschaft.qml"
            vlayerprojLS = self.layerLoader.load(layer)

            layer = {}
            layer["type"] = "postgres"
            layer["title"] = _translate("VeriSO_EE_gruda","Liegenschaften", None)
            layer["readonly"] = True
            layer["featuretype"] = "liegenschaften_liegenschaft"
            layer["geom"] = "geometrie"
            layer["key"] = "ogc_fid"
            layer["group"] = group3
            layer["sql"] = ""
            layer["style"] = "liegenschaften/liegenschaft.qml"
            vlayer = self.layerLoader.load(layer, False, True)


            layer = {}
            layer["type"] = "postgres"
            layer["title"] = _translate("VeriSO_EE_gruda","Hilfslinie", None)
            layer["readonly"] = True
            layer["featuretype"] = "liegenschaften_grundstueckpos"
            layer["geom"] = "hilfslinie"
            layer["key"] = "ogc_fid"
            layer["sql"] = ""
            layer["group"] = group3
            layer["style"] = "liegenschaften/hilfslinie.qml"
            vlayerHilfe = self.layerLoader.load(layer)	

            layer = {}
            layer["type"] = "postgres"
            layer["title"] = _translate("VeriSO_EE_gruda","proj_Grst-Nr", None)
            layer["readonly"] = True
            layer["featuretype"] = "z_projgs_nr"
            layer["geom"] = "pos"
            layer["key"] = "ogc_fid"
            layer["sql"] = ""
            layer["group"] = group3
            layer["style"] = "liegenschaften/proj_GS_NR.qml"
            vlayerprojNrLS = self.layerLoader.load(layer)	

            layer = {}
            layer["type"] = "postgres"
            layer["title"] = _translate("VeriSO_EE_gruda","Nr Gs(LS)", None)
            layer["readonly"] = True
            layer["featuretype"] = "z_nr_gs"
            layer["geom"] = "pos"
            layer["key"] = "ogc_fid"
            layer["sql"] = "(art=0) and (gesamteflaechenmass is NULL)"
            layer["group"] = group3
            layer["style"] = "liegenschaften/nr_ls_ganz.qml"
            vlayerNrGS = self.layerLoader.load(layer)

            layer = {}
            layer["type"] = "postgres"
            layer["title"] = _translate("VeriSO_EE_gruda","Nr Gs(SDR)", None)
            layer["readonly"] = True
            layer["featuretype"] = "z_nr_gs"
            layer["geom"] = "pos"
            layer["key"] = "ogc_fid"
            layer["group"] = group3
            layer["sql"] = "(art>0) and (gesamteflaechenmass is NULL)"
            layer["style"] = "liegenschaften/nr_sdr_ganz.qml"
            vlayerNRGSSDR = self.layerLoader.load(layer) 

            layer = {}
            layer["type"] = "postgres"
            layer["title"] = _translate("VeriSO_EE_gruda","Nr Gs(LS-Teil)", None)
            layer["readonly"] = True
            layer["featuretype"] = "z_nr_gs"
            layer["geom"] = "pos"
            layer["key"] = "ogc_fid"
            layer["sql"] = "(art=0) and (gesamteflaechenmass>0)"
            layer["group"] = group3
            layer["style"] = "liegenschaften/nr_ls_teil.qml"
            vlayerNTGSTeil = self.layerLoader.load(layer)

            layer = {}
            layer["type"] = "postgres"
            layer["title"] = _translate("VeriSO_EE_gruda","Nr Gs(SDR Teil)", None)
            layer["readonly"] = True
            layer["featuretype"] = "z_nr_gs"
            layer["geom"] = "pos"
            layer["key"] = "ogc_fid"
            layer["sql"] = "(art>0) and (gesamteflaechenmass>0)"
            layer["group"] = group3
            layer["style"] = "liegenschaften/nr_sdr_teil.qml"
            vlayerGSRNSDRTeil = self.layerLoader.load(layer)

            layer = {}
            layer["type"] = "postgres"
            layer["title"] =  _translate("VeriSO_EE_gruda", u"unvollständige Liegenschaften", None)
            layer["readonly"] = True 
            layer["featuretype"] = "liegenschaften_liegenschaft_v2"
            layer["geom"] = "geometrie"
            layer["key"] = "ogc_fid"            
            layer["sql"] = "Vollstaendigkeit=1"
            layer["group"] = group3
            layer["style"] = "liegenschaften/voll_ls.qml"
            vlayerunvollLS = self.layerLoader.load(layer)

            layer = {}
            layer["type"] = "postgres"
            layer["title"] = _translate("VeriSO_EE_gruda","streitige SDR", None)
            layer["readonly"] = True 
            layer["featuretype"] = "liegenschaften_selbstrecht_v"
            layer["geom"] = "geometrie"
            layer["key"] = "ogc_fid"            
            layer["sql"] = "Gueltigkeit=1"
            layer["group"] = group3
            layer["style"] = "liegenschaften/voll_ls.qml"
            vlayerstreitigSDR = self.layerLoader.load(layer)

            layer = {}
            layer["type"] = "postgres"
            layer["title"] =  _translate("VeriSO_EE_gruda",u"unvollständige SDR", None)
            layer["readonly"] = True 
            layer["featuretype"] = "liegenschaften_selbstrecht_v"
            layer["geom"] = "geometrie"
            layer["key"] = "ogc_fid"            
            layer["sql"] = "Vollstaendigkeit=1"
            layer["group"] = group3
            layer["style"] = "liegenschaften/voll_ls.qml"
            vlayerunvollSDR = self.layerLoader.load(layer)


            vlayerLunvollSDR = self.layerLoader.load(layer)
            layer = {}
            layer["type"] = "postgres"
            layer["title"] = _translate("VeriSO_EE_gruda","streitige Liegenschaften", None)
            layer["readonly"] = True 
            layer["featuretype"] = "liegenschaften_liegenschaft_v2"
            layer["geom"] = "geometrie"
            layer["key"] = "ogc_fid"            
            layer["sql"] = "Gueltigkeit=1"
            layer["group"] = group3
            layer["style"] = "liegenschaften/voll_ls.qml"
            vlayerstreitigLS = self.layerLoader.load(layer)

            

            layer = {}
            layer["type"] = "postgres"
            layer["title"] = _translate("VeriSO_EE_gruda","PLZ", None)
            layer["readonly"] = True 
            layer["featuretype"] = "plzortschaft_plz6"
            layer["geom"] = "flaeche"
            layer["key"] = "ogc_fid"
            layer["sql"] = ""
            layer["group"] = group4
            layer["style"] = "gebaeudeadressen/plz.qml"
            vlayerPLZ = self.layerLoader.load(layer)

            layer = {}
            layer["type"] = "postgres"
            layer["title"] = _translate("VeriSO_EE_gruda","Ortschaften", None)
            layer["readonly"] = True 
            layer["featuretype"] = "z_ortschaftsnamen_geom"
            layer["geom"] = "flaeche"
            layer["key"] = "ogc_fid"
            layer["sql"] = ""
            layer["group"] = group4
            layer["style"] = "gebaeudeadressen/ortschaft.qml"
            vlayerortschaft = self.layerLoader.load(layer)
 

            layer = {}
            layer["type"] = "postgres"
            layer["title"] = _translate("VeriSO_EE_gruda","benanntes Gebiet", None)
            layer["readonly"] = True 
            layer["featuretype"] = "gebaeudeadressen_benanntesgebiet"
            layer["geom"] = "flaeche"
            layer["key"] = "ogc_fid"
            layer["sql"] = ""
            layer["group"] = group4
            layer["style"] = "gebaeudeadressen/benanntesGebiet.qml"
            vlayerGeb = self.layerLoader.load(layer)


            layer = {}
            layer["type"] = "postgres"
            layer["title"] = _translate("VeriSO_EE_gruda","proj. Gebaeude", None)
            layer["readonly"] = True 
            layer["featuretype"] = "bodenbedeckung_projboflaeche"
            layer["geom"] = "geometrie"
            layer["key"] = "ogc_fid"
            layer["sql"] = "art = 0"
            layer["group"] = group4
            layer["style"] = "bodenbedeckung/projGebaeude.qml"
            vlayerprojGeb = self.layerLoader.load(layer)

            layer = {}
            layer["type"] = "postgres"
            layer["title"] = _translate("VeriSO_EE_gruda","adressierbare EOs", None)
            layer["readonly"] = True 
            layer["featuretype"] = "z_eo_flaeche"
            layer["geom"] = "geometrie"
            layer["key"] = "ctid"
            layer["sql"] = "art in (1,2,6,11)"
            layer["group"] = group4
            layer["style"] = "gebaeudeadressen/EO_Gebaeude.qml"
            vlayerEO = self.layerLoader.load(layer)

            layer = {}
            layer["title"] = _translate("VeriSO_EE_gruda","Strassenstueck Anfangspunkt", None)
            layer["readonly"] = True
            layer["featuretype"] = "gebaeudeadressen_strassenstueck"
            layer["geom"] = "anfangspunkt"
            layer["group"] = group4
            layer["key"] = "ogc_fid"
            layer["sql"] = ""
            layer["style"] = "gebaeudeadressen/Anfangspunkt.qml"
            vlayer = self.layerLoader.load(layer, False, True)

            layer = {}
            layer["title"] = _translate("VeriSO_EE_gruda","Strassenstueck (Geometrie)", None)
            layer["readonly"] = True
            layer["featuretype"] = "gebaeudeadressen_strassenstueck"
            layer["geom"] = "geometrie"
            layer["group"] = group4
            layer["sql"] = ""
            layer["key"] = "ogc_fid"
            layer["style"] = "gebaeudeadressen/strassenachsen_Pfeil.qml"
            vlayer = self.layerLoader.load(layer, False, True)
    

            layer = {}
            layer["type"] = "postgres"
            layer["title"] = _translate("VeriSO_EE_gruda","Spinnennetz", None)
            layer["readonly"] = True 
            layer["featuretype"] = "t_gebaeudeadressen_spinnennetz"
            layer["geom"] = "line"
            layer["key"] = "ogc_fid"
            layer["sql"] = ""
            layer["group"] = group4
            layer["style"] = "gebaeudeadressen/spinnennetz_blau.qml"
            vlayerSpinnen = self.layerLoader.load(layer)

            layer = {}
            layer["type"] = "postgres"
            layer["title"] = _translate("VeriSO_EE_gruda","Gebaeudeeingang BB/EO", None)
            layer["readonly"] = True 
            layer["featuretype"] = "gebaeudeadressen_gebaeudeeingang"
            layer["geom"] = "lage"
            layer["key"] = "ogc_fid"
            layer["sql"] = ""
            layer["group"] = group4
            layer["style"] = "gebaeudeadressen/GebEingang_BB_EO.qml"  
            vlayerGebein = self.layerLoader.load(layer)
 
            layer = {}
            layer["type"] = "postgres"
            layer["title"] = _translate("VeriSO_EE_gruda","LokalisationsNamePos", None)
            layer["readonly"] = True 
            layer["featuretype"] = "gebaeudeadressen_lokalisationsnamepos_v"
            layer["geom"] = "pos"
            layer["key"] = "ogc_fid"
            layer["sql"] = ""
            layer["group"] = group4
            layer["style"] = "gebaeudeadressen/lokalisationsnamepos.qml"   
            vlayerLokPos = self.layerLoader.load(layer)

            layer = {}
            layer["type"] = "postgres"
            layer["title"] = _translate("VeriSO_EE_gruda","LFP2", None)
            layer["readonly"] = True 
            layer["featuretype"] = "fixpunktekategorie2_lfp2"
            layer["geom"] = "geometrie"
            layer["key"] = "ogc_fid"            
            layer["sql"] = ""
            layer["group"] = group5        
            layer["style"] = "fixpunkte/lfp2.qml"
            vlayerLFP2 = self.layerLoader.load(layer)

            layer = {}
            layer["type"] = "postgres"
            layer["title"] = _translate("VeriSO_EE_gruda","LFP1", None)
            layer["readonly"] = True 
            layer["featuretype"] = "fixpunktekategorie1_lfp1"
            layer["geom"] = "geometrie"
            layer["key"] = "ogc_fid"            
            layer["sql"] = ""
            layer["group"] = group5      
            layer["style"] = "fixpunkte/lfp1.qml"
            vlayerLFP1 = self.layerLoader.load(layer)



             
        except Exception:
            QApplication.restoreOverrideCursor()            
            exc_type, exc_value, exc_traceback = sys.exc_info()
            self.iface.messageBar().pushMessage("Error", str(traceback.format_exc(exc_traceback)), level=QgsMessageBar.CRITICAL, duration=5)                    
        QApplication.restoreOverrideCursor()  

