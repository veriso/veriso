from __future__ import absolute_import, print_function

from builtins import next, range, str

from qgis.PyQt.QtCore import pyqtSlot, Qt
from qgis.PyQt.QtGui import QTableWidgetItem, QDockWidget, QTreeWidgetItem, QColor

from qgis.core import QgsFeatureRequest

from veriso.base.utils.utils import (get_ui_class)

FORM_CLASS = get_ui_class('check_results.ui')


class CheckResultsDock(QDockWidget, FORM_CLASS):
    """

    """
    result_parent = None

    def __init__(self, iface, parent=None):
        QDockWidget.__init__(self, parent)

        self.setupUi(self)
        self.iface = iface
        self.message_bar = self.iface.messageBar()
        self.layer = None
        self._gui_elements = [
            self.treeWidget
        ]

    def clear_results(self):
        self.treeWidget.clear()


    def add_result(self, fields):
        itm = QTreeWidgetItem(fields)
        if(fields[2]=='OK'):
            itm.setBackgroundColor(2, QColor(0, 255, 0, 127))
        else:
            itm.setBackgroundColor(2, QColor(255, 0, 0, 127))
        self.treeWidget.addTopLevelItem(itm)
        self.result_parent = itm

    def add_child(self, fields):
        QTreeWidgetItem(self.result_parent, fields)
