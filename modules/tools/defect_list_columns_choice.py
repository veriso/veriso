# coding=utf-8

from __future__ import absolute_import, print_function

import unicodedata

from builtins import next, range, str

from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtGui import QTableWidgetItem, QDialog, QCheckBox
from PyQt4.QtCore import QSettings

from veriso.base.utils.utils import (get_ui_class)

FORM_CLASS = get_ui_class('defect_list_columns_choice.ui')


class DefectsListColumnsChoice(QDialog, FORM_CLASS):
    """This class represent the dialog allowing to set the visibility of the
    columns in the defects list
    """

    def __init__(self, defects_layer, defects_list_dock, parent=None):
        """Constructor

        :param QgsVectorLayer defects_layer: The concerned defect layer
        :param DefectsListDock defects_list_dock: The instance of the defect
            list dock. This is used to refresh the dock when the dialog is
            closed."""

        QDialog.__init__(self, parent)
        self.setupUi(self)

        self.layer = defects_layer
        self.defects_list_dock = defects_list_dock
        
        self.setWindowTitle(self.layer.name())

        # Normalize the layer name to ascii, to be used as part of the
        # setting key
        self.layer_name_normalized = unicodedata.normalize(
            'NFD', self.layer.name()).encode('ascii', 'ignore').decode('ascii')

        self.settings = QSettings("CatAIS", "VeriSO")

        self._load_fields_table()

    def _load_fields_table(self):
        """Populate the table with the fields and the checkboxes
        """
        self.columns_table.clear()
        self.columns_table.setRowCount(0)
        self.columns_table.setColumnCount(2)

        self.columns_table.setHorizontalHeaderLabels(['Visible', 'Column'])

        excluded_fields = self._get_excluded_columns_list()

        row = 0
        for field in self.layer.pendingFields():
            self.columns_table.insertRow(row)

            cb = QCheckBox()
            cb.setCheckState(Qt.Checked)
            if field.name() in excluded_fields:
                cb.setCheckState(Qt.Unchecked)

            self.columns_table.setCellWidget(row, 0, cb)

            item = QTableWidgetItem(field.name())
            self.columns_table.setItem(row, 1, item)

            row += 1

        self.columns_table.resizeColumnsToContents()

    def _get_excluded_columns_list(self):
        """Load from the settings the list of columns to hide in the defect list
        for the layer

        :return list: a list with the excluded field names"""

        excluded_fields = self.settings.value(
            'defect_list/excluded_fields_{}'.format(self.layer_name_normalized))

        if not excluded_fields:
            excluded_fields = []

        return excluded_fields

    def accept(self):
        """Store the fields to hide into the settings and refresh the dock
        list"""

        excluded_fields = []

        for i in range(self.columns_table.rowCount()):

            if self.columns_table.cellWidget(i, 0).checkState() == Qt.Unchecked:
                excluded_fields.append(self.columns_table.item(i, 1).text())

        self.settings.setValue(
            'defect_list/excluded_fields_{}'.format(self.layer_name_normalized),
            excluded_fields)

        self.defects_list_dock._refresh_defects_list()
        self.close()