from __future__ import absolute_import, print_function

from builtins import next, range, str

from qgis.PyQt.QtCore import pyqtSignal, pyqtSlot, Qt, QObject
from qgis.PyQt.QtGui import QTableWidgetItem, QDockWidget

from qgis.core import QgsFeatureRequest

from veriso.base.utils.utils import (get_ui_class)

FORM_CLASS = get_ui_class('./defect_list.ui')


class DefectsListDock(QDockWidget, FORM_CLASS):
    """

    """
    projectsDatabaseHasChanged = pyqtSignal()

    def __init__(self, iface, parent=None):
        QDockWidget.__init__(self, parent)
        self.setupUi(self)
        self.iface = iface
        self.message_bar = self.iface.messageBar()
        self.layer = None

    def refresh(self, layers):
        self.layers_combo.clear()
        for layer in sorted(layers):
            self.layers_combo.addItem(layer, layers[layer])

    def _refresh_defects_list(self):
        self._refresh_unfinished_only_gui()
        self.defects_list.clear()
        self.defects_list.setRowCount(0)
        fields = [f.name() for f in self.layer.pendingFields()]
        self.defects_list.setColumnCount(len(fields))
        self.defects_list.setHorizontalHeaderLabels(fields)

        row = 0
        for feature in self._get_features():
            self.defects_list.insertRow(row)
            column = 0
            for field in fields:
                item = QTableWidgetItem(str(feature[field]))
                item.setData(Qt.UserRole, feature.id())
                self.defects_list.setItem(row, column, item)
                column += 1
            row += 1
        self.defects_list.resizeColumnsToContents()

    def _refresh_unfinished_only_gui(self):
        # get al boolean fields
        fields = [f.name() for f
                  in self.layer.pendingFields()
                  if f.typeName() == 'bool']

        fields_available = len(fields) > 0
        self.unfinished_fields_combo.blockSignals(True)
        self.unfinished_only_check.blockSignals(True)
        self.unfinished_fields_combo.clear()
        self.unfinished_fields_combo.addItems(fields)
        self.unfinished_fields_combo.setEnabled(fields_available)
        self.unfinished_only_check.setEnabled(fields_available)
        self.unfinished_fields_combo.blockSignals(False)
        self.unfinished_only_check.blockSignals(False)

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
        feature = self.layer.getFeatures(request).next()

        self.iface.openFeatureForm(self.layer,
                                   feature,
                                   updateFeatureOnly=False,
                                   showModal=True)
        self.layer.setSelectedFeatures([fid])

        self.iface.mapCanvas().zoomToSelected(self.layer)
        self.iface.mapCanvas().refresh()

    @pyqtSlot()
    def on_next_button_clicked(self):
        row = self.defects_list.currentRow() + 1
        if row == self.defects_list.rowCount():
            row = 0
        self.defects_list.setCurrentCell(row, 0)

    @pyqtSlot()
    def on_previous_button_clicked(self):
        row = self.defects_list.currentRow() - 1
        if row == -1:
            row = self.defects_list.rowCount() - 1
        self.defects_list.setCurrentCell(row, 0)

    @pyqtSlot(QTableWidgetItem, QTableWidgetItem)
    def on_defects_list_currentItemChanged(self, current_item, previous_item):
        if previous_item is None or current_item.row() != previous_item.row():
            fid = current_item.data(Qt.UserRole)
            self._zoom_to_feature(fid)

    @pyqtSlot(int)
    def on_layers_combo_currentIndexChanged(self, index):
        self.layer = self.layers_combo.itemData(index)
        self._refresh_defects_list()

    @pyqtSlot(int)
    def on_unfinished_fields_combo_currentIndexChanged(self, _):
        self._refresh_defects_list()

    @pyqtSlot(bool)
    def on_unfinished_only_check_toggled(self, state):
        self.unfinished_fields_combo.setEnabled(state)
        self._refresh_defects_list()

