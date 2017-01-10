from __future__ import absolute_import, print_function

from builtins import next, range, str

from qgis.PyQt.QtCore import pyqtSignal, pyqtSlot, Qt, QObject
from qgis.PyQt.QtGui import QTableWidgetItem, QDockWidget

from qgis.core import QgsFeatureRequest

from veriso.base.utils.utils import (get_ui_class)
from veriso.base.utils.exceptions import VerisoError

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
        self.defects_list.clear()
        fields = [f.name() for f in self.layer.pendingFields()]
        self.defects_list.setRowCount(self.layer.featureCount())
        self.defects_list.setColumnCount(len(fields))
        self.defects_list.setHorizontalHeaderLabels(fields)

        row = 0
        for feature in self.layer.getFeatures():
            column = 0
            for field in fields:
                item = QTableWidgetItem(str(feature[field]))
                item.setData(Qt.UserRole, feature.id())
                self.defects_list.setItem(row, column, item)
                column += 1
            row += 1



    def _get_unfinished_features(self):
        pass

    def _zoom_to_feature(self, fid):
        self.layer.setSelectedFeatures([fid])

        box = self.layer.boundingBoxOfSelected()
        self.iface.mapCanvas().setExtent(box)
        self.iface.mapCanvas().refresh()

    def _get_features(self):
        # Select all features along with their attributes1
        all_attrs = self.layer.pendingAllAttributesList()
        self.layer.select(all_attrs)
        # Get all the features to start
        all_features = {
            feature.id(): feature for (feature) in
            self.layer.getFeatures()}
        return all_features

    @pyqtSlot(QTableWidgetItem, QTableWidgetItem)
    def on_defects_list_currentItemChanged(self, current_item, previous_item):
        if previous_item is None or current_item.row() != previous_item.row():
            fid = current_item.data(Qt.UserRole)
            self._zoom_to_feature(fid)

    @pyqtSlot(int)
    def on_layers_combo_currentIndexChanged(self, index):
        self.layer = self.layers_combo.itemData(index)
        self._refresh_defects_list()
