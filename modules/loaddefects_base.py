# coding=utf-8

import sys
import traceback
from qgis.PyQt.QtCore import QObject, QSettings
from qgis.PyQt.QtWidgets import QApplication
from qgis.core import QgsProject, QgsEditFormConfig, Qgis

from veriso.base.utils.loadlayer import LoadLayer
from veriso.base.utils.utils import tr, db_user_has_role


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
        self.dbuser = self.settings.value("project/dbuser")

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
                loaded_layers[layer] = {'qgis_layer': loaded_layer,
                                        'info': self.layers[layer]}
            except Exception:
                QApplication.restoreOverrideCursor()
                exc_type, exc_value, exc_traceback = sys.exc_info()
                self.message_bar.pushMessage("Error", str(
                    traceback.format_exc(exc_traceback)),
                    level=Qgis.Critical,
                    duration=0)
        QApplication.restoreOverrideCursor()
        return loaded_layers

    def _load_defect_layer(self, layer):

        combo_box_code = ("    if {0}.currentIndex() == -1:\n"
                          "        i = {0}.findText('{1}')\n"
                          "        {0}.setCurrentIndex(i)\n")
        line_edit_code = ("    if {0}.text() in ['', 'NULL']:\n"
                          "        {0}.setText('{1}')\n")
        text_edit_code = ("    if {0}.toPlainText() in ['', 'NULL']:\n"
                          "        {0}.setPlainText('{1}')\n")
        widget_type_map = {'Enumeration': ['QComboBox', combo_box_code],
                           'TextEdit': ['QLineEdit', line_edit_code],
                           'PlainTextEdit': ['QPlainTextEdit', text_edit_code]}

        code_imports = []
        generated_code = ''

        loaded_layer = self.layer_loader.load(layer)
        if loaded_layer:
            loaded_layer.editFormConfig().setLayout(
                QgsEditFormConfig.GeneratedLayout)
            edit_form_config = loaded_layer.editFormConfig()
            for field_name in layer['fields']:
                field = layer['fields'][field_name]
                idx = loaded_layer.fields().indexFromName(field_name)
                if 'alias' in field:
                    loaded_layer.setFieldAlias(
                        idx, tr(field['alias'], self.tr_tag, None))

                if 'widget' in field:
                    widget = loaded_layer.editorWidgetSetup(idx)
                    loaded_layer.setEditorWidgetSetup(idx, widget)
                if 'default' in field:

                    try:
                        loaded_layer.setDefaultValueExpression(
                            field_name, "'%s'" % field['default'])
                    except AttributeError:

                        if field['widget'] in widget_type_map:
                            widget = field['widget']
                            try:
                                multiline = field['config']['IsMultiline']
                            except KeyError:
                                multiline = False
                            if multiline:
                                widget = 'PlainTextEdit'
                            widget_type = widget_type_map[widget][0]
                            widget_code = widget_type_map[widget][1]
                            if widget_type not in code_imports:
                                code_imports.append(widget_type)

                            widget_name = 'widget_{}'.format(field_name)
                            default_value = field['default']
                            code = (
                                "{0} = dialog.findChild({1}, '{2}')\n".format(
                                    widget_name,
                                    widget_type,
                                    field_name))

                            code += widget_code.format(
                                widget_name, default_value)
                            generated_code += code

                if 'readonly' in field:
                    edit_form_config.setReadOnly(
                        idx, field['readonly'])
                if 'config' in field:
                    # See gui/editorwidgets/ for all the parameters.
                    widget = loaded_layer.editorWidgetSetup(idx)
                    loaded_layer.setEditorWidgetSetup(idx, widget)
                if 'writable_only_by' in field:
                    if not db_user_has_role(
                            self.dbuser, field['writable_only_by']):
                        edit_form_config.setReadOnly(idx, True)

            if code_imports:
                code = ("# -*- coding: utf-8 -*-\n"
                        "from PyQt4.QtGui import %s\n"
                        "def form_open(dialog, layer, feature):\n")\
                    % ', '.join(code_imports)
                code += generated_code
                edit_form_config.setInitFunction('form_open')
                edit_form_config.setInitCode(code)
                edit_form_config.setInitCodeSource(
                    QgsEditFormConfig.CodeSourceDialog)

            return loaded_layer
