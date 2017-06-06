 # -*- coding: utf-8 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *

import sys
import traceback
import os


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
            self.iface.messageBar().pushMessage("Error",  _translate("VeriSO_EE_PNF", "project_id not set", None), level=QgsMessageBar.CRITICAL, duration=5)
            return

        QApplication.setOverrideCursor(Qt.WaitCursor)
        try:
            group_eo_allgemein = _translate("VeriSO_EE_PNF", "EO Allgemein", None)
            group_eo_allgemein += " (" + str(project_id) + ")"

            group_av_allgemein = _translate("VeriSO_EE_PNF", "AV Allgemein", None)
            group_av_allgemein += " (" + str(project_id) + ")"

            group_bb_allgemein = _translate("VeriSO_EE_PNF", "BB Allgemein", None)
            group_bb_allgemein += " (" + str(project_id) + ")"


            # Mängel
            # Call the menu action.
            self.iface.mainWindow().findChild(QAction, 'VeriSOModule.LoadDefectsAction').activate(QAction.Trigger)

            # Laufende Operate
            layer = {
                'type': 'ogr',
                'title': _translate('VeriSO_EE_PNF', 'Laufende operate_20_03_2017', None),
                'url': os.path.join(os.sep, 'share', 'Share', 'Baselayers',
                                    'laufende_operate_20_03_2017.shp'),
                'style': 'pnf/laufende_operate.qml'
            }
            vlayer = self.layer_loader.load(layer, True, True)

            # PNF2016 TS1 TS2
            layer = {
                'type': 'ogr',
                'title': _translate('VeriSO_EE_PNF', 'PNF2016_TS1_TS2', None),
                'url': os.path.join(os.sep, 'share', 'Share', 'Baselayers',
                                    'PNF2016_TS1_TS2.shp'),
                'style': 'pnf/pnf2016.qml'
            }
            vlayer = self.layer_loader.load(layer, False, True)

            # OBERN NETZ 2016
            layer = {
                'type': 'ogr',
                'title': _translate('VeriSO_EE_PNF', 'OBERN_NETZ_2016_1', None),
                'url': os.path.join(os.sep, 'share', 'Share', 'Baselayers',
                                    'OBERN_NETZBERN_2016_01.shp'),
                'style': 'pnf/obern_netz.qml'
            }
            vlayer = self.layer_loader.load(layer, False, True)

            # Wanderwege
            layer = {
                'type': 'wms',
                'title': _translate('VeriSO_EE_PNF', 'Wanderwege', None),
                'url': 'http://www.geoservice.apps.be.ch/geoservice2/services/a42geo/a42geo_transportwms_d_fk/MapServer/WMSServer?',
                'layers': 'GEODB.WANDERNS_WEGE',
                'format': 'image/png'
            }
            vlayer = self.layer_loader.load(layer, False, True)

            # BB Allgemein
            layer = {
                "type": "postgres", 
                "title": _translate("VeriSO_EE_basis", "Proj. Gebaeude", None),
                "readonly": True, 
                "featuretype": "bodenbedeckung_projboflaeche", 
                "geom": "geometrie",
                "key": "ogc_fid", 
                "sql": "art = 0", 
                "group": group_bb_allgemein, 
                "style": "basis/projGeb.qml"
            }
            vlayer = self.layer_loader.load(layer, True, True)
            
            layer = {
                "type": "postgres", 
                "title": _translate("VeriSO_EE_basis", "HausnummerPos", None),
                "featuretype": "v_gebaeudeadressen_hausnummerpos", 
                "geom": "pos", 
                "key": "ogc_fid", 
                "sql": "",
                "group": group_bb_allgemein, 
                "style": "gebaeudeadressen/hausnummerpos.qml"}
            vlayer = self.layer_loader.load(layer, True, True)

            layer = {
                "type": "postgres", 
                "title": _translate("VeriSO_EE_basis", "Bodenbedeckung Umriss", None),
                "readonly": True, 
                "featuretype": "bodenbedeckung_boflaeche", 
                "geom": "geometrie", 
                "key": "ogc_fid",
                "group": group_bb_allgemein, 
                "sql": "", 
                "style": "pnf/bb_umriss.qml"
            }
            vlayer = self.layer_loader.load(layer, True, True)

            layer = {
                "type": "postgres", 
                "title": _translate("VeriSO_EE_basis", "Bodenbedeckung", None),
                "readonly": True, 
                "featuretype": "bodenbedeckung_boflaeche", 
                "geom": "geometrie", 
                "key": "ogc_fid",
                "group": group_bb_allgemein, 
                "sql": "", 
                "style": "basis/BB.qml"
            }
            vlayer = self.layer_loader.load(layer, False, True)

            layer = {
                "type": "postgres", 
                "title": _translate("VeriSO_EE_basis", "Objektname", None), 
                "readonly": True,
                "featuretype": "bodenbedeckung_objektnamepos_v", 
                "geom": "pos", 
                "group": group_bb_allgemein, 
                "key": "ogc_fid",
                "sql": "", 
                "style": "bodenbedeckung/objektnamen.qml"
            }
            vlayer = self.layer_loader.load(layer, False, True)

            # EO Allgemein
            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_EE_basis", "EO Flaechenelemete", None),
                "readonly": True,
                "featuretype": "einzelobjekte_flaechenelement_v",
                "geom": "geometrie",
                "key": "ogc_fid",
                "group": group_eo_allgemein,
                "sql": "",
                "style": "basis/eo_flaeche.qml"
            }
            vlayer = self.layer_loader.load(layer, True, True)

            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_EE_basis", "EO Linienelemente", None),
                "readonly": True,
                "featuretype": "einzelobjekte_linienelement_v",
                "geom": "geometrie",
                "key": "ogc_fid",
                "group": group_eo_allgemein,
                "sql": "",
                "style": "basis/eo_linie.qml"}
            vlayer = self.layer_loader.load(layer, True, True)

            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_EE_basis", "EO Punktelemente", None),
                "readonly": True,
                "featuretype": "einzelobjekte_punktelement_v",
                "geom": "geometrie",
                "key": "ogc_fid",
                "group": group_eo_allgemein,
                "sql": "",
                "style": "basis/eo_pkt.qml"
            }
            vlayer = self.layer_loader.load(layer, True, True)

            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_EE_basis", "Objektname", None),
                "readonly": True,
                "featuretype": "einzelobjekte_objektnamepos_v",
                "geom": "pos",
                "key": "ogc_fid",
                "group": group_eo_allgemein,
                "sql": "",
                "style": "bodenbedeckung/objektnamen.qml"}
            vlayer = self.layer_loader.load(layer, False, True)

            # AV Allgemein
            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_EE_basis", "SDR", None),
                "readonly": True,
                "featuretype": "liegenschaften_selbstrecht",
                "geom": "geometrie",
                "group": group_av_allgemein,
                "key": "ogc_fid",
                "sql": "",
                "style": "liegenschaften/selbstrecht.qml"
            }
            vlayer = self.layer_loader.load(layer)

            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_EE_basis", "Liegenschaften", None),
                "readonly": True,
                "featuretype": "liegenschaften_liegenschaft_v2",
                "geom": "geometrie",
                "group": group_av_allgemein,
                "key": "ogc_fid",
                "sql": "",
                "style": "liegenschaften/liegenschaft.qml"}
            vlayer = self.layer_loader.load(layer)

            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_EE_basis", "Hilfslinie", None),
                "readonly": True,
                "featuretype": "liegenschaften_grundstueckpos",
                "geom": "hilfslinie",
                "group": group_av_allgemein,
                "key": "ogc_fid",
                "sql": "",
                "style": "liegenschaften/hilfslinie.qml"
            }
            vlayer = self.layer_loader.load(layer, False, True)

            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_EE_basis", "Hoheitsgrenzpunkt - unversichert", None),
                "readonly": True,
                "featuretype": "gemeindegrenzen_hoheitsgrenzpunkt",
                "geom": "geometrie",
                "group": group_av_allgemein,
                "key": "ogc_fid",
                "sql": "punktzeichen in (6)",
                "style": "bodenbedeckung/hgp_unver.qml"
            }
            vlayer = self.layer_loader.load(layer, False, True)

            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_EE_basis", "Hoheitsgrenzpunkt - Bolzen,Rohr", None),
                "readonly": True,
                "featuretype": "gemeindegrenzen_hoheitsgrenzpunkt",
                "geom": "geometrie",
                "group": group_av_allgemein,
                "key": "ogc_fid",
                "sql": "punktzeichen in (2,3)",
                "style": "bodenbedeckung/hgp_bolzen.qml"
            }
            vlayer = self.layer_loader.load(layer, False, True)

            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_EE_basis", "Hoheitsgrenzpunkt - Kreuz", None),
                "readonly": True,
                "featuretype": "gemeindegrenzen_hoheitsgrenzpunkt",
                "geom": "geometrie",
                "group": group_av_allgemein,
                "key": "ogc_fid",
                "sql": "punktzeichen in (5)",
                "style": "bodenbedeckung/hgp_kreuz.qml"
            }
            vlayer = self.layer_loader.load(layer, False, True)

            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_EE_basis", "Hoheitsgrenzpunkt - Stein", None),
                "readonly": True,
                "featuretype": "gemeindegrenzen_hoheitsgrenzpunkt",
                "geom": "geometrie",
                "group": group_av_allgemein,
                "key": "ogc_fid",
                "sql": "punktzeichen in (0)",
                "style": "bodenbedeckung/hgp_stein.qml"
            }
            vlayer = self.layer_loader.load(layer, False, True)

            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_EE_basis", "Grenzpunkt - unversichert", None),
                "readonly": True,
                "featuretype": "liegenschaften_grenzpunkt",
                "geom": "geometrie",
                "group": group_av_allgemein,
                "key": "ogc_fid",
                "sql": "punktzeichen in (6)", "style": "bodenbedeckung/gp_unver.qml"
            }
            vlayer = self.layer_loader.load(layer, False, True)

            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_EE_basis", "Grenzpunkt - Bolzen,Rohr", None),
                "readonly": True,
                "featuretype": "liegenschaften_grenzpunkt",
                "geom": "geometrie",
                "group": group_av_allgemein,
                "key": "ogc_fid",
                "sql": "punktzeichen in (2,3)",
                "style": "bodenbedeckung/gp_bolzen.qml"
            }
            vlayer = self.layer_loader.load(layer, False, True)

            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_EE_basis", "Grenzpunkt - Kreuz", None),
                "readonly": True,
                "featuretype": "liegenschaften_grenzpunkt",
                "geom": "geometrie",
                "group": group_av_allgemein,
                "key": "ogc_fid",
                "sql": "punktzeichen in (5)",
                "style": "bodenbedeckung/gp_kreuz.qml"
            }
            vlayer = self.layer_loader.load(layer, False, True)

            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_EE_basis", "Grenzpunkt - Stein", None),
                "readonly": True,
                "featuretype": "liegenschaften_grenzpunkt",
                "geom": "geometrie",
                "group": group_av_allgemein,
                "key": "ogc_fid",
                "sql": "punktzeichen in (0)",
                "style": "bodenbedeckung/gp_stein.qml"
            }
            vlayer = self.layer_loader.load(layer, False, True)

            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_EE_basis", "proj. Liegenschaften", None),
                "readonly": True,
                "featuretype": "liegenschaften_projliegenschaft",
                "geom": "geometrie",
                "group": group_av_allgemein,
                "key": "ogc_fid",
                "sql": "",
                "style": "liegenschaften/projliegenschaft.qml"
            }
            vlayer = self.layer_loader.load(layer)

            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_EE_basis", "proj. SDR", None),
                "readonly": True,
                "featuretype": "liegenschaften_projselbstrecht", "geom": "geometrie",
                "group": group_av_allgemein,
                "key": "ogc_fid",
                "sql": "",
                "style": "liegenschaften/projselbstrecht.qml"
            }
            vlayer = self.layer_loader.load(layer)

            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_EE_basis", "proj_Grst-Nr", None),
                "readonly": True,
                "featuretype": "z_projgs_nr",
                "geom": "pos",
                "group": group_av_allgemein,
                "key": "ogc_fid",
                "sql": "",
                "style": "liegenschaften/proj_GS_NR.qml"
            }
            vlayer = self.layer_loader.load(layer)

            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_EE_basis", "Nr Gs(LS)", None),
                "readonly": True,
                "featuretype": "z_nr_gs",
                "geom": "pos",
                "key": "ogc_fid",
                "group": group_av_allgemein,
                "sql": "(art=0) and (gesamteflaechenmass is NULL)",
                "style": "liegenschaften/nr_ls_ganz.qml"
            }
            vlayer = self.layer_loader.load(layer)

            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_EE_basis", "Nr Gs(SDR)", None),
                "readonly": True,
                "featuretype": "z_nr_gs",
                "geom": "pos",
                "group": group_av_allgemein,
                "key": "ogc_fid",
                "sql": "(art>0) and (gesamteflaechenmass is NULL)",
                "style": "liegenschaften/nr_sdr_ganz.qml"
            }
            vlayer = self.layer_loader.load(layer)

            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_EE_basis", "Nr Gs(LS-Teil)", None),
                "readonly": True,
                "featuretype": "z_nr_gs",
                "geom": "pos",
                "group": group_av_allgemein,
                "key": "ogc_fid",
                "sql": "(art=0) and (gesamteflaechenmass>0)",
                "style": "liegenschaften/nr_ls_teil.qml"
            }
            vlayer = self.layer_loader.load(layer)

            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_EE_basis", "Nr Gs(SDR Teil)", None),
                "readonly": True,
                "featuretype": "z_nr_gs",
                "geom": "pos",
                "group": group_av_allgemein,
                "key": "ogc_fid",
                "sql": "art>0 and gesamteflaechenmass>0",
                "style": "liegenschaften/nr_sdr_teil.qml"
            }
            vlayer = self.layer_loader.load(layer)

            # PNFBE21 HINWEISE V1
            layer = {
                'type': 'gdal',
                'title': _translate('VeriSO_EE_PNF', 'PNFBE21_HINWEISE_V1', None),
                'url': os.path.join(os.sep, 'share', 'Share', 'Baselayers',
                                    'PNFBE21_HINWEISE_V1.tif'),
                'style': 'pnf/pnfbe21.qml'
            }
            vlayer = self.layer_loader.load(layer, False, True)

            # AV EO Linien
            layer = {
                'type': 'wms',
                'title': _translate('VeriSO_EE_PNF', 'AV EO Linien', None),
                'url': 'http://www.geoservice.apps.be.ch/geoservice2/services/a42geo/a42geo_avrwms_d_fk/MapServer/WMSServer?',
                'layers': 'Einzelobjekte Linien',
                'format': 'image/png'
            }
            vlayer = self.layer_loader.load(layer, True, True)

            # AV EO Flaechen
            layer = {
                'type': 'wms',
                'title': _translate('VeriSO_EE_PNF', 'AV EO Flaechen', None),
                'url': 'http://www.geoservice.apps.be.ch/geoservice2/services/a42geo/a42geo_avrwms_d_fk/MapServer/WMSServer?',
                'layers': 'Einzelobjekte Flaeche',
                'format': 'image/png'
            }
            vlayer = self.layer_loader.load(layer, True, True)

            # AV Bodenbedeckung
            layer = {
                'type': 'wms',
                'title': _translate('VeriSO_EE_PNF', 'AV Bodenbedeckung', None),
                'url': 'http://www.geoservice.apps.be.ch/geoservice2/services/a42geo/a42geo_avrwms_d_fk/MapServer/WMSServer?',
                'layers': 'Bodenbedeckung farbig',
                'format': 'image/png'
            }
            vlayer = self.layer_loader.load(layer, False, True)

            # swissimage (50%)
            layer = {
                'type': 'wms',
                'title': _translate('VeriSO_EE_PNF', 'swissimage (50%)', None),
                'url': 'http://wms.swisstopo.admin.ch/wss/httpauth/swisstopowms?',
                'layers': 'ch.swisstopo.swissimage',
                'format': 'image/jpeg',
                'style': 'baselayer/swissimage_50.qml'
            }
            vlayer = self.layer_loader.load(layer, False, True)

            # swissimage (100%)
            layer = {
                'type': 'wms',
                'title': _translate('VeriSO_EE_PNF', 'swissimage (100%)', None),
                'url': 'http://wms.swisstopo.admin.ch/wss/httpauth/swisstopowms?',
                'layers': 'ch.swisstopo.swissimage',
                'format': 'image/jpeg',
            }
            vlayer = self.layer_loader.load(layer, False, True)

        except Exception:
            QApplication.restoreOverrideCursor()            
            exc_type, exc_value, exc_traceback = sys.exc_info()
            self.iface.messageBar().pushMessage("Error", str(traceback.format_exc(exc_traceback)), level=QgsMessageBar.CRITICAL, duration=5)                    
        QApplication.restoreOverrideCursor()  

