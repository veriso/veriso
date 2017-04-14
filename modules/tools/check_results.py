from __future__ import absolute_import, print_function

from qgis.PyQt.QtGui import QDockWidget, QTreeWidgetItem, QColor, QTreeWidget
#from PyQt4 import QtCore
from qgis.PyQt.QtCore import pyqtSlot, Qt, QObject, SIGNAL
from qgis.core import QgsFeatureRequest
from veriso.base.utils.utils import (get_ui_class)
import sip
import sys
import traceback

FORM_CLASS = get_ui_class('check_results.ui')


class CheckResultsDock(QDockWidget, FORM_CLASS):
    """Creates a DockWidget where show the results of the checks.
    The widget is based on TreeWidget component

    """
    result_parent = None

    def __init__(self, iface, parent=None):
        QDockWidget.__init__(self, parent)

        self.setupUi(self)
        self.iface = iface
        self.message_bar = self.iface.messageBar()
        #self.layer = None
        self._gui_elements = [
            self.treeWidget
        ]

    def clear_results(self):
        self.treeWidget.clear()

    def add_result(self, fields):
        """Add a parent result
        """
        found_items = self.treeWidget.findItems(fields[0], Qt.MatchExactly)
        if len(found_items) > 0:
            self.treeWidget.takeTopLevelItem(self.treeWidget.indexOfTopLevelItem(found_items[0]))

        itm = QTreeWidgetItem(fields)
        if(fields[2]=='OK'):
            itm.setBackgroundColor(2, QColor(0, 255, 0, 127))
        else:
            itm.setBackgroundColor(2, QColor(255, 0, 0, 127))

        self.treeWidget.addTopLevelItem(itm)
        self.result_parent = itm

    def add_child(self, fields):
        """Add a child result to the last inserted parent
        """
        QTreeWidgetItem(self.result_parent, fields)

    def select_features(self, id_list):
        # get all loaded layers
        layers = self.iface.legendInterface().layers()

        for layer in layers:
            features_it = layer.getFeatures(
                QgsFeatureRequest().setFilterExpression(
                    u'"ogc_fid" in ({})'.format(
                        ', '.join(id_list))))
            # select the wrong features
            layer.setSelectedFeatures([ f.id() for f in features_it ])

            # set visible only the layers with wrong features
            if layer.selectedFeatureCount():
                self.iface.legendInterface().setLayerVisible(
                    layer, True)
            else:
                self.iface.legendInterface().setLayerVisible(
                    layer, False)

    def on_treeWidget_itemDoubleClicked(self, item):
        #print('on_treeWidget_clicked ', item.text(0), ' ', item.text(1), '', item.text(2))

        vincolo = 'veriso.modules.veriti.checks.vincoli.'
        vincolo += item.text(0)[0].lower() + item.text(0)[1:].replace(' ', '_').strip()
        print('vincolo ', vincolo)
        try:
            _temp = __import__(vincolo, globals(), locals(), ['ComplexCheck'])
            c = _temp.ComplexCheck(self.iface)
            c.run()

        except Exception, e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print('Error ', str(e))


