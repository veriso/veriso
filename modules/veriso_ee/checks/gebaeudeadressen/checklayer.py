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

from veriso.modules.complexcheck_base import ComplexCheckBase


class ComplexCheck(ComplexCheckBase):
    name = 'Checklayer'

    def __init__(self, iface):
        super(ComplexCheck, self).__init__(iface)

    def run(self):
        project_id = self.settings.value("project/id")
        epsg = self.settings.value("project/epsg")

        locale = QSettings().value('locale/userLocale')[0:2]

        if not project_id:
            self.message_bar.pushCritical("Error", _translate(
                    "VeriSO_EE_Geb_Check", "project_id not set", None))
            return

        QApplication.setOverrideCursor(Qt.WaitCursor)
        try:
            group = _translate("VeriSO_EE_Geb_Check",
                               "Gebaeudeadressen - Checklayer", None)
            group += " (" + str(project_id) + ")"

            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_EE_Geb_Check", "Spinnennetz",
                                    None),
                "featuretype": "t_gebaeudeadressen_spinnennetz",
                "geom": "line", "key": "ogc_fid", "sql": "",
                "readonly": True, "group": group,
                "style": "global_qml/gebaeudeadressen/spinnennetz_blau.qml"
            }

            vlayer = self.layer_loader.load(layer, False)

            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_EE_Geb_Check",
                                    "Kürzeste Linie", None),
                "featuretype": "t_shortestline_hausnummerpos",
                "geom": "the_geom", "key": "ogc_fid", "sql": "",
                "readonly": True, "group": group,
                "style": "global_qml/gebaeudeadressen/shortestline_linie.qml"
            }

            vlayer = self.layer_loader.load(layer)

            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_EE_Geb_Check", "HausnummerPos",
                                    None),
                "featuretype": "v_gebaeudeadressen_hausnummerpos",
                "geom": "pos", "key": "ogc_fid", "sql": "", "group": group,
                "style":
                    "global_qml/gebaeudeadressen/shortestline_hausnummerpos.qml"
            }

            vlayer = self.layer_loader.load(layer)

            layer = {
                "type": "postgres",
                "title": _translate("VeriSO_EE_Geb_Check",
                                    "Gebaeude > 12m2 ohne Eingang", None),
                "featuretype": "t_gebaeude_groesser_12m2_ohne_eingang",
                "geom": "geometrie", "key": "ogc_fid", "sql": "",
                "group": group,
                "style":
                    "global_qml/gebaeudeadressen/gebaeude_12m2_ohne_eingang.qml"
            }

            vlayer = self.layer_loader.load(layer)

        except Exception as e:
            QApplication.restoreOverrideCursor()
            exc_type, exc_value, exc_traceback = sys.exc_info()
            self.message_bar.pushMessage("Error", str(
                    traceback.format_exc(exc_traceback)),
                                         level=QgsMessageBar.CRITICAL,
                                         duration=0)
        QApplication.restoreOverrideCursor()
