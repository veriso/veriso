# coding=utf-8
import sys
import traceback
from builtins import str
from qgis.PyQt.QtCore import QObject, QSettings
from qgis.PyQt.QtWidgets import QApplication
from qgis.core import QgsProject, QgsVectorLayer
from qgis.gui import QgsMessageBar

from veriso.base.utils.loadlayer import LoadLayer
from veriso.base.utils.utils import tr


class LoadDefects(QObject):
    def __init__(self, iface, module, tr_tag):

        #import pydevd
        #pydevd.settrace('localhost', port=53100, stdoutToServer=True,
        # stderrToServer=True)

        QObject.__init__(self)
        self.iface = iface
        self.message_bar = self.iface.messageBar()
        self.canvas = self.iface.mapCanvas()

        self.root = QgsProject.instance().layerTreeRoot()
        self.layer_loader = LoadLayer(self.iface)
        self.settings = QSettings("CatAIS", "VeriSO")
        self.project_id = None
        self.epsg = None

        self.tr_tag = tr_tag  # "VeriSO_V+D_Defects" or "VeriSO_EE_Defects"

    def run(self):
        try:
            self.project_id = self.settings.value("project/id")
            self.epsg = self.settings.value("project/epsg")

            group = tr(u"Mängel", self.tr_tag, None)
            group += " (" + str(self.project_id) + ")"

            layer = {
                "type": "postgres",
                "title": tr(u"Mängelliste (Punkte)", self.tr_tag, None),
                "featuretype": "t_maengel_punkt", "geom": "the_geom",
                "key": "ogc_fid", "readonly": False, "sql": "",
                "group": group, "style": "global_qml/maengel/maengel_punkt.qml"
            }

            vlayer = self.layer_loader.load(layer)
            if vlayer:
                vlayer.setEditorLayout(QgsVectorLayer.GeneratedLayout)

                ogc_fid_idx = vlayer.fieldNameIndex("ogc_fid")
                topic_idx = vlayer.fieldNameIndex("topic")
                bemerkung_idx = vlayer.fieldNameIndex("bemerkung")
                datum_idx = vlayer.fieldNameIndex("datum")

                vlayer.addAttributeAlias(topic_idx,
                                         tr("Topic:", self.tr_tag,
                                            None))
                vlayer.addAttributeAlias(bemerkung_idx,
                                         tr("bemekung:", self.tr_tag,
                                            None))

                vlayer.setEditorWidgetV2(ogc_fid_idx, "Hidden")
                vlayer.setEditorWidgetV2(topic_idx, "Enumeration")
                vlayer.setEditorWidgetV2(bemerkung_idx, "TextEdit")
                vlayer.setEditorWidgetV2Config(bemerkung_idx, {
                    "IsMultiline": True
                })  # See gui/editorwidgets/qgstexteditwrapper.cpp for all
                # the parameters.
                vlayer.setEditorWidgetV2(datum_idx, "Hidden")

            layer = {
                "type": "postgres",
                "title": tr(u"Mängelliste (Linien)", self.tr_tag, None),
                "featuretype": "t_maengel_linie", "geom": "the_geom",
                "key": "ogc_fid", "readonly": False, "sql": "",
                "group": group, "style": "global_qml/maengel/maengel_linie.qml"
            }

            vlayer = self.layer_loader.load(layer)
            if vlayer:
                vlayer.setEditorLayout(QgsVectorLayer.GeneratedLayout)

                ogc_fid_idx = vlayer.fieldNameIndex("ogc_fid")
                topic_idx = vlayer.fieldNameIndex("topic")
                bemerkung_idx = vlayer.fieldNameIndex("bemerkung")
                datum_idx = vlayer.fieldNameIndex("datum")

                vlayer.addAttributeAlias(topic_idx,
                                         tr("Topic:", self.tr_tag,
                                            None))
                vlayer.addAttributeAlias(bemerkung_idx,
                                         tr("Bemerkung:", self.tr_tag, None))

                vlayer.setEditorWidgetV2(ogc_fid_idx, "Hidden")
                vlayer.setEditorWidgetV2(topic_idx, "Enumeration")
                vlayer.setEditorWidgetV2(bemerkung_idx, "TextEdit")
                vlayer.setEditorWidgetV2Config(bemerkung_idx, {
                    "IsMultiline": True
                })  # See gui/editorwidgets/qgstexteditwrapper.cpp for all
                # the parameters.
                vlayer.setEditorWidgetV2(datum_idx, "Hidden")

                layer = {
                    "type": "postgres",
                    "title": tr(u"Mängelliste (Polygone)", self.tr_tag, None),
                    "featuretype": "t_maengel_polygon", "geom": "the_geom",
                    "key": "ogc_fid", "readonly": False, "sql": "",
                    "group": group,
                    "style": "global_qml/maengel/maengel_polygon.qml"
                }

                vlayer = self.layer_loader.load(layer)
                if vlayer:
                    vlayer.setEditorLayout(QgsVectorLayer.GeneratedLayout)

                    ogc_fid_idx = vlayer.fieldNameIndex("ogc_fid")
                    topic_idx = vlayer.fieldNameIndex("topic")
                    bemerkung_idx = vlayer.fieldNameIndex("bemerkung")
                    datum_idx = vlayer.fieldNameIndex("datum")

                    vlayer.addAttributeAlias(topic_idx,
                                             tr("Topic:", self.tr_tag,
                                                None))
                    vlayer.addAttributeAlias(bemerkung_idx,
                                             tr("Bemerkung:", self.tr_tag,
                                                None))

                    vlayer.setEditorWidgetV2(ogc_fid_idx, "Hidden")
                    vlayer.setEditorWidgetV2(topic_idx, "Enumeration")
                    vlayer.setEditorWidgetV2(bemerkung_idx, "TextEdit")
                    vlayer.setEditorWidgetV2Config(bemerkung_idx, {
                        "IsMultiline": True
                    })  # See gui/editorwidgets/qgstexteditwrapper.cpp for all
                    # the parameters.
                    vlayer.setEditorWidgetV2(datum_idx, "Hidden")

        except Exception:
            QApplication.restoreOverrideCursor()
            exc_type, exc_value, exc_traceback = sys.exc_info()
            self.message_bar.pushMessage("Error", str(
                    traceback.format_exc(exc_traceback)),
                                         level=QgsMessageBar.CRITICAL,
                                         duration=0)
        QApplication.restoreOverrideCursor()
