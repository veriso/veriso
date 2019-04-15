# coding=utf-8

import unicodedata

from qgis.PyQt.QtCore import Qt, QDateTime, QSettings
from qgis.PyQt.QtWidgets import QTableWidgetItem, QDockWidget

from qgis.core import QgsFeatureRequest

from veriso.modules.tools.defect_list_columns_choice import (
    DefectsListColumnsChoice)
from veriso.base.utils.utils import (get_ui_class)

FORM_CLASS = get_ui_class('defect_list.ui')


class DefectsListDock(QDockWidget, FORM_CLASS):
    """

    """

    def __init__(self, iface, parent=None):
        QDockWidget.__init__(self, parent)
        self.setupUi(self)
        self.iface = iface
        self.message_bar = self.iface.messageBar()
        self.layer = None

        self._gui_elements = [
            self.layers_combo,
            self.unfinished_only_check,
            self.unfinished_fields_combo,
            self.previous_button,
            self.next_button,
            self.defects_list,
            self.columns_choice_button]

        self._toggle_gui_elements(False)

        self.settings = QSettings("CatAIS", "VeriSO")

        self.next_button.clicked.connect(self.next_button_clicked)
        self.previous_button.clicked.connect(self.previous_button_clicked)
        self.defects_list.currentItemChanged.connect(
            self.defects_list_currentItemChanged)
        self.layers_combo.currentIndexChanged.connect(
            self.layers_combo_currentIndexChanged)
        self.unfinished_fields_combo.currentIndexChanged.connect(
            self.unfinished_fields_combo_currentIndexChanged)
        self.unfinished_only_check.toggled.connect(
            self.unfinished_only_check_toggled)
        self.columns_choice_button.clicked.connect(
            self.columns_choice_button_clicked)

    def clear(self):
        self.layer = None
        self.layers_combo.clear()
        self.unfinished_fields_combo.clear()
        self._clear_defects_list()
        self._toggle_gui_elements(False)

    def load_layers(self, layers):
        self.layers_combo.clear()
        for layer in sorted(layers):
            info = layers[layer]['info']
            layer_name = '%s - %s' % (info['group'], info['title'])
            self.layers_combo.addItem(layer_name, layers[layer]['qgis_layer'])

    def _layer_changed(self):
        self._toggle_gui_elements((self.layer is not None))
        if self.layer is not None:
            self._refresh_unfinished_only_gui()
            self._refresh_defects_list()

    def _clear_defects_list(self):
        self.defects_list.clear()
        self.defects_list.setRowCount(0)
        self.defects_list.setColumnCount(0)

    def _refresh_defects_list(self):
        if self.layer is None:
            return
        self._clear_defects_list()

        excluded_fields = self._get_excluded_columns_list()

        fields = []
        for f in self.layer.fields():
            if not f.name() in excluded_fields:
                fields.append(f.name())

        self.defects_list.setColumnCount(len(fields))
        self.defects_list.setHorizontalHeaderLabels(fields)

        row = 0
        for feature in self._get_features():
            self.defects_list.insertRow(row)
            column = 0
            for field in fields:
                if type(feature[field]) is QDateTime:
                    item = QTableWidgetItem(feature[field].toString())
                elif type(feature[field]) is long \
                        or type(feature[field]) is int:
                    item = QCustomTableWidgetItem(str(feature[field]))
                else:
                    item = QTableWidgetItem(str(feature[field]))
                item.setData(Qt.UserRole, feature.id())
                item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                self.defects_list.setItem(row, column, item)
                column += 1
            row += 1
        self.defects_list.resizeColumnsToContents()

    def _get_excluded_columns_list(self):
        """Load from the settings the list of columns to hide in the defect list
        for the layer

        :return list: a list with the excluded field names"""

        # Normalize the layer name to ascii, to be used as part of the
        # setting key
        layer_name_normalized = unicodedata.normalize(
            'NFD', self.layer.name()).encode('ascii', 'ignore').decode('ascii')

        excluded_fields = self.settings.value(
            'defect_list/excluded_fields_{}'.format(layer_name_normalized))

        if not excluded_fields:
            excluded_fields = []

        return excluded_fields

    def _toggle_gui_elements(self, enable):
        for element in self._gui_elements:
            element.setEnabled(enable)
        self.unfinished_fields_combo.setEnabled(
            self.unfinished_only_check.isChecked())

    def _refresh_unfinished_only_gui(self):
        # get al boolean fields
        fields = [f.name() for f
                  in self.layer.fields()
                  if f.typeName() == 'bool']

        fields_available = len(fields) > 0
        self.unfinished_fields_combo.clear()
        self.unfinished_fields_combo.addItems(fields)
        self.unfinished_only_check.setEnabled(fields_available)

    def _get_features(self):
        if self.unfinished_only_check.isChecked():
            return self._get_unfinished_features()
        return self.layer.getFeatures()

    def _get_unfinished_features(self):
        request = QgsFeatureRequest()
        field = self.unfinished_fields_combo.currentText()
        expression = '"{0}" != True or "{0}" is NULL'.format(field)
        request.setFilterExpression(expression)
        return self.layer.getFeatures(request)

    def _zoom_to_feature(self, fid):
        request = QgsFeatureRequest(fid)
        feature = next(self.layer.getFeatures(request))

        self.layer.setSelectedFeatures([fid])

        self.iface.mapCanvas().zoomToSelected(self.layer)
        self.iface.mapCanvas().refresh()

        self.iface.openFeatureForm(self.layer,
                                   feature,
                                   updateFeatureOnly=False,
                                   showModal=True)

    def next_button_clicked(self):
        row = self.defects_list.currentRow() + 1
        if row == self.defects_list.rowCount():
            row = 0
        self.defects_list.setCurrentCell(row, 0)

    def previous_button_clicked(self):
        row = self.defects_list.currentRow()
        if row > 0:
            row -= 1
        else:
            row = self.defects_list.rowCount() - 1
        self.defects_list.setCurrentCell(row, 0)

    def defects_list_currentItemChanged(self, current_item, previous_item):
        if self.layer is None or current_item is None:
            return
        if previous_item is None or current_item.row() != previous_item.row():
            fid = current_item.data(Qt.UserRole)
            self._zoom_to_feature(fid)

    def layers_combo_currentIndexChanged(self, index):
        self.layer = self.layers_combo.itemData(index)
        self._layer_changed()

    def unfinished_fields_combo_currentIndexChanged(self, _):
        self._refresh_defects_list()

    def unfinished_only_check_toggled(self, state):
        self.unfinished_fields_combo.setEnabled(state)
        self._refresh_defects_list()

    def columns_choice_button_clicked(self):
        """Open the dialog to set the visibility of the fields in the table
        """

        self.defects_list_columns_choice_dialog = DefectsListColumnsChoice(
            self.layer, self)
        self.defects_list_columns_choice_dialog.setVisible(True)
        self.defects_list_columns_choice_dialog.raise_()


class QCustomTableWidgetItem (QTableWidgetItem):
    """Custom Table Widget Item used to sort in number order instead of
    alphabetical order (i.e. 1, 2, ..., 10 instead of 1, 10, 2, ...

    Source https://stackoverflow.com/a/25539830
    """

    def __init__(self, value):
        super(QCustomTableWidgetItem, self).__init__(value)

    def __lt__(self, other):
        if isinstance(other, QCustomTableWidgetItem):
            self_data_value = float(self.data(Qt.EditRole))
            other_data_value = float(other.data(Qt.EditRole))
            return self_data_value < other_data_value
        else:
            return QTableWidgetItem.__lt__(self, other)
