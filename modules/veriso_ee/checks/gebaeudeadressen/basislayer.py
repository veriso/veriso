# coding=utf-8
import sys
import traceback
from builtins import str
from qgis.PyQt.QtCore import QObject, QSettings, Qt
from qgis.PyQt.QtWidgets import QApplication
from qgis.core import QgsProject
from qgis.gui import QgsMessageBar

from veriso.base.utils.loadlayer import LoadLayer

try:
    _encoding = QApplication.UnicodeUTF8


    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig)

from collections import OrderedDict
from veriso.modules.complexcheck_base import ComplexCheckBase


class ComplexCheck(ComplexCheckBase):
    names = OrderedDict()
    names['de'] = 'Basislayer'
    names['fr'] = 'Couche de base'

    def __init__(self, iface):
        super(ComplexCheck, self).__init__(iface)

    def run(self):
        project_id = self.settings.value("project/id")
        epsg = self.settings.value("project/epsg")

        locale = QSettings().value('locale/userLocale')[0:2]

        if not project_id:
            self.message_bar.pushCritical("Error", _translate(
                    "VeriSO_EE_Geb_Basis", "project_id not set", None))
            return

        QApplication.setOverrideCursor(Qt.WaitCursor)
        try:
            group = _translate("VeriSO_EE_Geb_Basis",
                               "Gebaeudeadressen - Basislayer", None)
            group += " (" + str(project_id) + ")"

            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_EE_Geb_Basis",
                                    "Bodenbedeckung", None),
                "featuretype": "bodenbedeckung_boflaeche",
                "geom": "geometrie", "key": "ogc_fid",
                "sql": "art_txt LIKE 'Gebaeude%' OR art_txt LIKE "
                       "'befestigt.Strasse_Weg%' OR art_txt LIKE "
                       "'befestigt.Trottoir%' OR art_txt LIKE "
                       "'befestigt.uebrige_befestigte%'",
                "readonly": True, "group": group,
                "style":
                    "bodenbedeckung/gebaeude_strassen_trottoir_erschliessung"
                    ".qml"
            }
            # Use 'LIKE' instead of 'IN' or '='. Now you can model extensions
            #  like different kinds of 'uebrige_befestigte'.

            # Visibility and if legend and/or groupd should be collapsed can
            # be set with parameters in the self.layer_loader.load()
            # method:
            # load(layer, visibility=True, collapsed_legend=False,
            # collapsed_group=False)
            vlayer = self.layer_loader.load(layer)

            # noinspection PyPep8
            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_EE_Geb_Basis",
                                    "EO.Flaechenelemente", None),
                "featuretype": "v_einzelobjekte_flaechenelement",
                "geom": "geometrie", "key": "ogc_fid",
                "sql": "art_txt LIKE 'unterirdisches_Gebaeude%' OR "
                       "art_txt LIKE 'uebriger_Gebaeudeteil%' OR art_txt "
                       "LIKE 'Reservoir%' OR art_txt LIKE 'Unterstand%'",
                "readonly": True, "group": group,
                "style":
                    "einzelobjekte/eo_flaeche_gebdetail_unterstand_reservoir_unterirdisch.qml"
            }

            vlayer = self.layer_loader.load(layer)

            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_EE_Geb_Basis",
                                    "EO.Linienelemente", None),
                "featuretype": "v_einzelobjekte_linienelement",
                "geom": "geometrie", "key": "ogc_fid",
                "sql": "art_txt LIKE 'uebriger_Gebaeudeteil%'",
                "readonly": True, "group": group,
                "style": "einzelobjekte/eo_linie_gebdetail.qml"
            }

            vlayer = self.layer_loader.load(layer)

            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_EE_Geb_Basis",
                                    "GEB.Nachführung", None),
                "featuretype": "gebaeudeadressen_gebnachfuehrung",
                "key": "ogc_fid", "sql": "", "readonly": True,
                "group": group
            }
            # layer["geom"] = "perimeter" # Will be loaded as geometryless
            # layer.

            vlayer = self.layer_loader.load(layer)

            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_EE_Geb_Basis",
                                    "Benanntes Gebiet", None),
                "featuretype": "gebaeudeadressen_benanntesgebiet",
                "geom": "flaeche", "key": "ogc_fid", "sql": "",
                "readonly": True, "group": group,
                "style": "global_qml/gebaeudeadressen/benanntesgebiet_gruen.qml"
            }

            vlayer = self.layer_loader.load(layer)

            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_EE_Geb_Basis",
                                    "Strassenstueck (geometrie)", None),
                "featuretype": "gebaeudeadressen_strassenstueck",
                "geom": "geometrie", "key": "ogc_fid", "sql": "",
                "group": group,
                "style": "global_qml/gebaeudeadressen/strassenachsen_gruen.qml"
            }

            vlayer = self.layer_loader.load(layer)

            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_EE_Geb_Basis",
                                    "Strassenstueck (anfangspunkt)", None),
                "featuretype": "gebaeudeadressen_strassenstueck",
                "geom": "anfangspunkt", "key": "ogc_fid", "sql": "",
                "group": group,
                "style": "global_qml/gebaeudeadressen/anfangspunkt_gruen.qml"
            }

            vlayer = self.layer_loader.load(layer)

            # noinspection PyPep8
            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_EE_Geb_Basis",
                                    "Gebaeudeeingang", None),
                "featuretype": "gebaeudeadressen_gebaeudeeingang",
                "geom": "lage", "key": "ogc_fid", "sql": "",
                "group": group,
                "style":
                    "global_qml/gebaeudeadressen/gebaeudeeingang_blaues_viereck_mit_label.qml"
            }

            vlayer = self.layer_loader.load(layer)

            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_EE_Geb_Basis", "HausnummerPos",
                                    None),
                "featuretype": "v_gebaeudeadressen_hausnummerpos",
                "geom": "pos", "key": "ogc_fid", "sql": "", "group": group,
                "style": "global_qml/gebaeudeadressen/hausnummerpos.qml"
            }

            vlayer = self.layer_loader.load(layer)

            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_EE_Geb_Basis",
                                    "LokalisationsName", None),
                "featuretype": "gebaeudeadressen_lokalisationsname",
                "key": "ogc_fid", "sql": "", "group": group
            }

            vlayer = self.layer_loader.load(layer)

            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_EE_Geb_Basis",
                                    "LokalisationsNamePos", None),
                "featuretype": "t_gebaeudeadressen_lokalisationsnamepos",
                "geom": "pos", "key": "ogc_fid", "sql": "", "group": group,
                "style": "global_qml/gebaeudeadressen/lokalisationsnamepos.qml"
            }

            vlayer = self.layer_loader.load(layer)

            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_EE_Geb_Basis",
                                    "Gemeindegrenze", None),
                "featuretype": "gemeindegrenzen_gemeindegrenze",
                "geom": "geometrie", "key": "ogc_fid", "sql": "",
                "readonly": True, "group": group,
                "style": "global_qml/gemeindegrenze/gemgre_strichliert.qml"
            }

            gemgrelayer = self.layer_loader.load(layer)

            if gemgrelayer:
                rect = gemgrelayer.extent()
                rect.scale(5)
                self.iface.mapCanvas().setExtent(rect)
                self.iface.mapCanvas().refresh()

        except Exception as e:
            QApplication.restoreOverrideCursor()
            exc_type, exc_value, exc_traceback = sys.exc_info()
            self.message_bar.pushMessage("Error", str(
                    traceback.format_exc(exc_traceback)),
                                         level=QgsMessageBar.CRITICAL,
                                         duration=0)
        QApplication.restoreOverrideCursor()
