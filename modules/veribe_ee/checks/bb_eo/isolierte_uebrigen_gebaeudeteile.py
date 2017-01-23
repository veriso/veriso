# coding=utf-8
from __future__ import print_function
from collections import OrderedDict

import sys
import traceback
from builtins import range, str
from qgis.PyQt.QtCore import QObject, QSettings, QSizeF, Qt
from qgis.PyQt.QtGui import QColor, QTextDocument
from qgis.PyQt.QtWidgets import QApplication
from qgis.core import QgsFeature, QgsMapLayer, QgsMapLayerRegistry, QgsPoint, \
    QgsProject, QgsRectangle
from qgis.gui import QgsMessageBar, QgsTextAnnotationItem
from qgis.core import QgsDataSourceURI, QgsVectorLayer

from veriso.base.utils.loadlayer import LoadLayer
from veriso.modules.complexcheck_base import ComplexCheckBase

try:
    _encoding = QApplication.UnicodeUTF8

    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig)


class ComplexCheck(ComplexCheckBase):

    names = OrderedDict()
    names['de'] = u'Isolierte Übrigen Gebäudeteile'
    names['fr'] = u'Parties isolées des bâtiments'

    def __init__(self, iface):
        super(ComplexCheck, self).__init__(iface)
        self.iface = iface
        self.message_bar = self.iface.messageBar()
        self.canvas = self.iface.mapCanvas()

        self.settings = QSettings("CatAIS", "VeriSO")
        self.root = QgsProject.instance().layerTreeRoot()
        self.layer_loader = LoadLayer(self.iface)

    def run(self):

        project_id = self.settings.value("project/id")
        epsg = self.settings.value("project/epsg")

        locale = QSettings().value('locale/userLocale')[0:2]  # this is for multilingual legends

        # If locale is different to frence or italian, german will be used.
        # Otherwise we get into troubles with the legends, e.g. locale = "en"
        # but
        # there is no english legend (qml file).
        if locale == "fr":
            pass
        elif locale == "it":
            pass
        else:
            locale = "de"

        if not project_id:
            self.message_bar.pushCritical("Error", _translate("Isolierte Uebrigen Gebaeudeteile", "project_id not set", None))
            return

        QApplication.setOverrideCursor(Qt.WaitCursor)
        try:
            group = _translate("Veribe", "Isolierte_Uebrigen_Gebaeudeteile", None)
            group += " (" + str(project_id) + ")"

            layer = {
                "type": "postgres",
                "title": _translate("Veribe", "Isolierte Uebrigen Gebaeudeteile Flachen", None),
                "featuretype": "v_uebriger_gebaeudeteil_isolierte_flaeche",
                "geom": "geometrie", "key": "ogc_fid", "sql": "",
                "readonly": True, "group": group,
            }

            vlayer = self.layer_loader.load(layer)

            layer = {
                "type": "postgres",
                "title": _translate("Veribe", "Isolierte Uebrigen Gebaeudeteile Linien", None),
                "featuretype": "v_uebriger_gebaeudeteil_isolierte_linien",
                "geom": "geometrie", "key": "ogc_fid", "sql": "",
                "readonly": True, "group": group,
            }

            vlayer = self.layer_loader.load(layer)

            layer = {
                "type": "postgres",
                "title": _translate("Veribe", "Isolierte Uebrigen Gebaeudeteile Punkte", None),
                "featuretype": "v_uebriger_gebaeudeteil_isolierte_punkte",
                "geom": "geometrie", "key": "ogc_fid", "sql": "",
                "readonly": True, "group": group,
            }

            vlayer = self.layer_loader.load(layer)

            # Visibility and if legend and/or groupd should be collapsed can
            # be set with parameters in the self.layer_loader.load()
            # method:
            # load(layer, visibility=True, collapsed_legend=False,
            # collapsed_group=False)
            #vlayer = self.layer_loader.load(layer)

        except Exception:
            QApplication.restoreOverrideCursor()
            exc_type, exc_value, exc_traceback = sys.exc_info()
            self.message_bar.pushMessage("Error", str(
                    traceback.format_exc(exc_traceback)),
                                         level=QgsMessageBar.CRITICAL,
                                         duration=0)
        QApplication.restoreOverrideCursor()