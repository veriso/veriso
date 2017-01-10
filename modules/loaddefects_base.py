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


class LoadDefectsBase(QObject):
    def __init__(self, iface, tr_tag):

        QObject.__init__(self)
        self.iface = iface
        self.message_bar = self.iface.messageBar()
        self.canvas = self.iface.mapCanvas()

        self.root = QgsProject.instance().layerTreeRoot()
        self.layer_loader = LoadLayer(self.iface)
        self.settings = QSettings("CatAIS", "VeriSO")
        self.project_id = None
        self.epsg = None
        self.tr_tag = tr_tag  # "VeriSO (V+D)", "VeriSO (EE)"

        self.project_id = self.settings.value("project/id")
        self.epsg = self.settings.value("project/epsg")

        self.group = tr(u"Mängel", self.tr_tag, None)
        self.group += " (" + str(self.project_id) + ")"

        # this can be overriden in ApplicationModule.do_load_defects before
        # calling ApplicationModule.run()
        self.layers = {
            'point': {
                "type": "postgres",
                "title": tr(u"Mängelliste (Punkte)", self.tr_tag, None),
                "featuretype": "t_maengel_punkt",
                "geom": "the_geom",
                "key": "ogc_fid",
                "readonly": False,
                "sql": "",
                "group": self.group,
                "style": "global_qml/maengel/maengel_punkt.qml",
                "fields": {
                    'ogc_fid': {'widget': 'Hidden'},
                    'topic': {
                        'widget': 'Enumeration',
                        'alias': 'Topic:'
                    },
                    'bemerkung': {
                        'widget': 'TextEdit',
                        'alias': 'Bemekung:',
                        'config': {"IsMultiline": True}
                    },
                    'datum': {'widget': 'Hidden'}
                }
            },
            'line': {
                "type": "postgres",
                "title": tr(u"Mängelliste (Linien)", self.tr_tag, None),
                "featuretype": "t_maengel_linie",
                "geom": "the_geom",
                "key": "ogc_fid",
                "readonly": False,
                "sql": "",
                "group": self.group,
                "style": "global_qml/maengel/maengel_linie.qml",
                "fields": {
                    'ogc_fid': {'widget': 'Hidden'},
                    'topic': {
                        'widget': 'Enumeration',
                        'alias': 'Topic:'
                    },
                    'bemerkung': {
                        'widget': 'TextEdit',
                        'alias': 'Bemekung:',
                        'config': {"IsMultiline": True}
                    },
                    'datum': {'widget': 'Hidden'}
                }
            },
            'polygon': {
                "type": "postgres",
                "title": tr(u"Mängelliste (Polygone)", self.tr_tag, None),
                "featuretype": "t_maengel_polygon",
                "geom": "the_geom",
                "key": "ogc_fid",
                "readonly": False,
                "sql": "",
                "group": self.group,
                "style": "global_qml/maengel/maengel_polygon.qml",
                "fields": {
                    'ogc_fid': {'widget': 'Hidden'},
                    'topic': {
                        'widget': 'Enumeration',
                        'alias': 'Topic:'
                    },
                    'bemerkung': {
                        'widget': 'TextEdit',
                        'alias': 'Bemekung:',
                        'config': {"IsMultiline": True}
                    },
                    'datum': {'widget': 'Hidden'}
                }
            }
        }

    def run(self):
        loaded_layers = {}
        for layer in self.layers:
            try:
                loaded_layer = self._load_defect_layer(self.layers[layer])
                loaded_layers[layer] = loaded_layer
            except Exception:
                QApplication.restoreOverrideCursor()
                exc_type, exc_value, exc_traceback = sys.exc_info()
                self.message_bar.pushMessage("Error", str(
                        traceback.format_exc(exc_traceback)),
                                             level=QgsMessageBar.CRITICAL,
                                             duration=0)
        QApplication.restoreOverrideCursor()
        return loaded_layers

    def _load_defect_layer(self, layer):
        loaded_layer = self.layer_loader.load(layer)
        if loaded_layer:
            loaded_layer.setEditorLayout(QgsVectorLayer.GeneratedLayout)
            for field_name in layer['fields']:
                field = layer['fields'][field_name]
                idx = loaded_layer.fieldNameIndex(field_name)
                if 'alias' in field:
                    loaded_layer.addAttributeAlias(
                            idx, tr(field['alias'], self.tr_tag, None))

                if 'widget' in field:
                    loaded_layer.setEditorWidgetV2(
                            idx, tr(field['widget']))
                if 'config' in field:
                    # See gui/editorwidgets/ for all the parameters.
                    loaded_layer.setEditorWidgetSetup(idx, field['config'])
            return loaded_layer
